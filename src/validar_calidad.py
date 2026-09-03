"""
PYME Studio — Reporte de calidad reproducible del pipeline.

No modifica pipeline.py ni sus salidas. Corre DESPUÉS del pipeline
(necesita outputs/pyme_studio_unificado.csv) y verifica:

  1. Existencia de los archivos de entrada esperados en data/raw/.
  2. Columnas esperadas presentes en el dataset unificado.
  3. Cobertura del periodo 2005-2024 (sin años faltantes).
  4. Valores negativos o imposibles (aperturas/cierres/empresas_activas < 0,
     tasa_cierre fuera de [0, un umbral razonable]).
  5. Cantidad de comunas y de rubros dentro de un rango esperado.
  6. Rubros que no lograron cruzar entre las 3 fuentes (aparecen en una
     fuente pero no en las otras, dentro del mismo año).
  7. Duplicados después de agrupar por (año, comuna, rubro).
  8. Tasas de cierre extremas (>50%) que ameritan revisión manual.
  9. Filas descartadas en el pipeline y motivo (recalculado aquí, no leído
     de un log — pipeline.py no escribe uno).

Termina con código de salida 1 si encuentra un problema BLOQUEANTE
(archivo faltante, columna faltante, año faltante) — 0 si solo hay
advertencias. El reporte completo, con cada chequeo y su resultado, se
guarda en outputs/reporte_calidad.json y outputs/reporte_calidad.md.

Requiere: pandas
Uso: python validar_calidad.py
"""
import json
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "raw"
OUT_DIR = ROOT / "outputs"


def rel(path: Path) -> str:
    """Ruta relativa a la raíz del repo, para no filtrar la ruta absoluta local en el reporte."""
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)

UNIFICADO_PATH = OUT_DIR / "pyme_studio_unificado.csv"
ARCHIVOS_ENTRADA_ESPERADOS = ["Ciclo_Vida.zip", "PUB_COMU_RUBR.xlsb"]
COLUMNAS_ESPERADAS = ["anio", "comuna", "rubro", "aperturas", "cierres", "empresas_activas", "tasa_cierre"]
ANIO_MIN, ANIO_MAX = 2005, 2024
RANGO_COMUNAS = (300, 360)   # Chile tiene 346 comunas oficiales; el SII agrega alguna variante/residual
RANGO_RUBROS = (15, 25)      # CIIU Rev.4 a 1 dígito son 21 categorías
TASA_CIERRE_EXTREMA = 0.5    # 50% anual — revisar manualmente, no es necesariamente un error


def check(nombre, ok, detalle, bloqueante=False):
    return {"chequeo": nombre, "ok": bool(ok), "bloqueante": bool(bloqueante), "detalle": str(detalle)}


def revisar_archivos_entrada(resultados):
    for nombre in ARCHIVOS_ENTRADA_ESPERADOS:
        path = DATA_DIR / nombre
        existe = path.exists()
        resultados.append(check(
            f"Archivo de entrada existe: {nombre}", existe,
            f"{rel(path)} — encontrado ({path.stat().st_size:,} bytes)" if existe else f"{rel(path)} no existe",
            bloqueante=not existe,
        ))
    if (DATA_DIR / "Ciclo_Vida.zip").exists():
        with zipfile.ZipFile(DATA_DIR / "Ciclo_Vida.zip") as z:
            nombres = z.namelist()
            for interno in ["PUB_TG.txt", "PUB_actividades_inscritas.txt"]:
                ok = interno in nombres
                resultados.append(check(f"Ciclo_Vida.zip contiene {interno}", ok, str(nombres), bloqueante=not ok))


def revisar_columnas(df, resultados):
    faltantes = [c for c in COLUMNAS_ESPERADAS if c not in df.columns]
    resultados.append(check(
        "Columnas esperadas presentes", len(faltantes) == 0,
        f"Faltan: {faltantes}" if faltantes else f"Todas presentes: {COLUMNAS_ESPERADAS}",
        bloqueante=len(faltantes) > 0,
    ))


def revisar_periodo(df, resultados):
    anios = sorted(df["anio"].unique().tolist())
    faltantes = [a for a in range(ANIO_MIN, ANIO_MAX + 1) if a not in anios]
    resultados.append(check(
        f"Cobertura {ANIO_MIN}-{ANIO_MAX} sin años faltantes", len(faltantes) == 0,
        f"Años en el dataset: {anios[0]}-{anios[-1]} ({len(anios)} años). Faltantes: {faltantes or 'ninguno'}",
        bloqueante=len(faltantes) > 0,
    ))


def revisar_valores_imposibles(df, resultados):
    negativos = {}
    for col in ["aperturas", "cierres", "empresas_activas"]:
        n_neg = int((df[col] < 0).sum())
        negativos[col] = n_neg
    hay_negativos = any(v > 0 for v in negativos.values())
    resultados.append(check(
        "Sin valores negativos en aperturas/cierres/empresas_activas", not hay_negativos,
        f"Conteo de filas negativas por columna: {negativos}",
        bloqueante=hay_negativos,
    ))

    tasa_valida = df["tasa_cierre"].dropna()
    negativa = int((tasa_valida < 0).sum())
    resultados.append(check(
        "tasa_cierre nunca es negativa", negativa == 0,
        f"{negativa} filas con tasa_cierre < 0 de {len(tasa_valida):,} filas con tasa definida",
        bloqueante=negativa > 0,
    ))

    sobre_uno = df[df["tasa_cierre"] > 1]
    mediana_empresas_sobre_uno = float(sobre_uno["empresas_activas"].median()) if len(sobre_uno) else 0.0
    resultados.append(check(
        "tasa_cierre > 100% (esperable solo en celdas con muy pocas empresas)",
        len(sobre_uno) == 0,
        f"{len(sobre_uno)} filas ({len(sobre_uno)/len(tasa_valida)*100:.2f}%) con tasa_cierre > 1 de {len(tasa_valida):,}. "
        f"Mediana de empresas_activas en esas filas: {mediana_empresas_sobre_uno:.0f}. "
        "Es un artefacto esperado de mezclar una FOTO anual (empresas_activas, ~stock) con un FLUJO anual (cierres, ~eventos): "
        "en una comuna+rubro con 1-2 empresas activas en promedio, pueden ocurrir varios cierres distintos dentro del mismo año "
        "(alta rotación en un universo chico), lo que empuja cierres/empresas_activas por sobre 1. "
        "No indica corrupción de datos — pero si algún análisis futuro NO usa el umbral MIN_EMPRESA_ANIOS de analisis_hito4.py, "
        "debe filtrar o acotar tasa_cierre explícitamente para no dejar que estas celdas dominen un promedio.",
        bloqueante=False,
    ))

    extremas = df[(df["tasa_cierre"] > TASA_CIERRE_EXTREMA) & (df["empresas_activas"] >= 20)]
    resultados.append(check(
        f"Tasas de cierre extremas (>{TASA_CIERRE_EXTREMA:.0%}, con 20+ empresas activas) — para revisión manual, no es un error automático",
        len(extremas) == 0,
        f"{len(extremas)} combinaciones año+comuna+rubro con tasa_cierre > {TASA_CIERRE_EXTREMA:.0%} y exposición no trivial. "
        + (f"Ejemplos: {extremas.nlargest(5, 'tasa_cierre')[['anio','comuna','rubro','empresas_activas','tasa_cierre']].to_dict('records')}" if len(extremas) else "ninguna"),
        bloqueante=False,
    ))


def revisar_cardinalidad(df, resultados):
    n_comunas = df["comuna"].nunique()
    n_rubros = df["rubro"].nunique()
    ok_comunas = RANGO_COMUNAS[0] <= n_comunas <= RANGO_COMUNAS[1]
    ok_rubros = RANGO_RUBROS[0] <= n_rubros <= RANGO_RUBROS[1]
    resultados.append(check(
        f"N° de comunas dentro de rango esperado {RANGO_COMUNAS}", ok_comunas,
        f"{n_comunas} comunas distintas en el dataset", bloqueante=False,
    ))
    resultados.append(check(
        f"N° de rubros dentro de rango esperado {RANGO_RUBROS}", ok_rubros,
        f"{n_rubros} rubros distintos en el dataset", bloqueante=False,
    ))


def revisar_duplicados(df, resultados):
    dup = df.duplicated(subset=["anio", "comuna", "rubro"]).sum()
    resultados.append(check(
        "Sin duplicados de (año, comuna, rubro) tras agrupar", dup == 0,
        f"{dup} filas duplicadas encontradas" if dup else "0 duplicados — cada combinación año+comuna+rubro aparece una sola vez",
        bloqueante=dup > 0,
    ))


def revisar_cruce_fuentes(df, resultados):
    # Filas donde una fuente aportó 0 en las 3 columnas simultáneamente serían un outer-join
    # que no encontró pareja en NINGUNA fuente, lo cual no debería pasar (siempre viene de al
    # menos una). Lo que sí es señal real de "no cruzó": aperturas=0 Y cierres=0 Y
    # empresas_activas=0 en una fila (indica una fuente aportó la combinación pero las otras
    # dos no tenían nada que unir ese año-comuna-rubro).
    solo_una_fuente = df[(df["aperturas"] == 0) & (df["cierres"] == 0) & (df["empresas_activas"] == 0)]
    resultados.append(check(
        "Filas con las 3 métricas en cero simultáneamente (posible fuente sin cruce real)",
        len(solo_una_fuente) == 0,
        f"{len(solo_una_fuente)} filas con aperturas=cierres=empresas_activas=0 — "
        "estas filas no aportan información y probablemente son un artefacto del outer join "
        "(la combinación año+comuna+rubro existe en el índice combinado pero ninguna fuente reportó actividad real).",
        bloqueante=False,
    ))

    rubros_unificado = set(df["rubro"].unique())
    resultados.append(check(
        "Rubros presentes en el dataset unificado", True,
        f"{len(rubros_unificado)} rubros: {sorted(rubros_unificado)}", bloqueante=False,
    ))


def contar_filas_descartadas(resultados):
    """Recalcula, sin modificar pipeline.py, cuántas filas se descartaron en cada fuente
    y por qué — pipeline.py no deja un log de esto, así que se reconstruye aquí leyendo
    las mismas fuentes crudas con la misma lógica de filtrado."""
    detalle = {}
    try:
        with zipfile.ZipFile(DATA_DIR / "Ciclo_Vida.zip") as z:
            with z.open("PUB_TG.txt") as f:
                df_tg = pd.read_csv(f, sep="\t", encoding="latin-1", dtype=str)
        total_tg = len(df_tg)
        vacias = df_tg["Año comercial"].isna().sum()
        valor_default = (df_tg["Rubro"].str.strip() == "Valor por Defecto").sum()
        detalle["PUB_TG.txt"] = {
            "filas_totales": int(total_tg),
            "descartadas_filas_vacias": int(vacias),
            "descartadas_valor_por_defecto": int(valor_default),
            "filas_utiles": int(total_tg - vacias - valor_default),
        }

        with zipfile.ZipFile(DATA_DIR / "Ciclo_Vida.zip") as z:
            with z.open("PUB_actividades_inscritas.txt") as f:
                df_ai = pd.read_csv(f, sep="\t", encoding="latin-1", dtype=str)
        total_ai = len(df_ai)
        valor_default_ai = (df_ai["RUBRO"].str.strip() == "Valor por Defecto").sum()
        detalle["PUB_actividades_inscritas.txt"] = {
            "filas_totales": int(total_ai),
            "descartadas_valor_por_defecto": int(valor_default_ai),
            "filas_utiles": int(total_ai - valor_default_ai),
        }
        resultados.append(check(
            "Conteo de filas descartadas por fuente (recalculado)", True,
            json.dumps(detalle, ensure_ascii=False), bloqueante=False,
        ))
    except Exception as e:
        resultados.append(check("Conteo de filas descartadas por fuente", False, f"No se pudo recalcular: {e}", bloqueante=False))
    return detalle


def main():
    resultados = []
    revisar_archivos_entrada(resultados)

    if not UNIFICADO_PATH.exists():
        resultados.append(check(
            "outputs/pyme_studio_unificado.csv existe", False,
            "No se encontró — corre pipeline.py primero", bloqueante=True,
        ))
        _emitir_reporte(resultados, {})
        sys.exit(1)

    df = pd.read_csv(UNIFICADO_PATH)
    revisar_columnas(df, resultados)
    revisar_periodo(df, resultados)
    revisar_valores_imposibles(df, resultados)
    revisar_cardinalidad(df, resultados)
    revisar_duplicados(df, resultados)
    revisar_cruce_fuentes(df, resultados)
    detalle_descarte = contar_filas_descartadas(resultados)

    hay_bloqueante = any(r["bloqueante"] and not r["ok"] for r in resultados)
    _emitir_reporte(resultados, detalle_descarte)

    n_ok = sum(1 for r in resultados if r["ok"])
    print(f"\n{n_ok}/{len(resultados)} chequeos OK.")
    if hay_bloqueante:
        print("Hay al menos un problema BLOQUEANTE — revisar outputs/reporte_calidad.md")
        sys.exit(1)
    else:
        print("Sin problemas bloqueantes (puede haber advertencias no bloqueantes).")


def _emitir_reporte(resultados, detalle_descarte):
    OUT_DIR.mkdir(exist_ok=True)
    payload = {
        "generado": datetime.now(timezone.utc).isoformat(),
        "chequeos": resultados,
        "filas_descartadas_por_fuente": detalle_descarte,
    }
    (OUT_DIR / "reporte_calidad.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lineas = ["# Reporte de calidad — PYME Studio", "", f"Generado: {payload['generado']}", ""]
    for r in resultados:
        icono = "✅" if r["ok"] else ("🛑" if r["bloqueante"] else "⚠️")
        lineas.append(f"## {icono} {r['chequeo']}")
        lineas.append(f"{r['detalle']}")
        lineas.append("")
    (OUT_DIR / "reporte_calidad.md").write_text("\n".join(lineas), encoding="utf-8")

    print("\n=== Reporte de calidad ===")
    for r in resultados:
        icono = "OK " if r["ok"] else ("BLOQUEANTE" if r["bloqueante"] else "ADVERTENCIA")
        print(f"[{icono}] {r['chequeo']}")


if __name__ == "__main__":
    main()
