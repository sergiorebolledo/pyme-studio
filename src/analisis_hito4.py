"""
PYME Studio — Hito 4: Primer análisis completo

Responde la pregunta de investigación:
¿Cuál es la concentración de pymes por rubro y comuna, y cómo se relaciona
con su tasa histórica de término de giro (cierre)?

Lee output/pyme_studio_unificado.csv (generado por pipeline.py) y:
  1. Agrega por comuna+rubro a lo largo de todo 2005-2024 (una tasa por
     "empresa-año" en vez de promediar tasas anuales, que es más robusto
     ante combinaciones con pocas empresas).
  2. Calcula la correlación (Pearson y Spearman) entre concentración
     (empresas activas) y tasa de cierre, filtrando combinaciones con
     muy poca exposición para reducir ruido estadístico.
  3. Identifica 3 tipos de casos: saturados y riesgosos, saludables, y
     de baja concentración — el insumo real para el producto final.

Requiere: pandas, scipy
Uso: python analisis_hito4.py
"""
from pathlib import Path

import pandas as pd
from scipy import stats

OUT_DIR = Path(__file__).resolve().parent.parent / "outputs"
IN_PATH = OUT_DIR / "pyme_studio_unificado.csv"

MIN_EMPRESA_ANIOS = 200  # umbral mínimo de exposición para evitar ruido de muestras chicas


def cargar_y_agregar() -> pd.DataFrame:
    df = pd.read_csv(IN_PATH)

    agg = df.groupby(["comuna", "rubro"], as_index=False).agg(
        aperturas_total=("aperturas", "sum"),
        cierres_total=("cierres", "sum"),
        empresa_anios=("empresas_activas", "sum"),  # suma de "empresas activas" a través de los 20 años = exposición total
        concentracion_promedio=("empresas_activas", "mean"),  # tamaño típico del rubro en esa comuna
    )
    # Tasa de cierre por "empresa-año" de exposición — más robusta que promediar tasas anuales.
    agg["tasa_cierre"] = agg["cierres_total"] / agg["empresa_anios"]
    return agg


def analizar_correlacion(agg: pd.DataFrame) -> pd.DataFrame:
    muestra = agg[agg["empresa_anios"] >= MIN_EMPRESA_ANIOS].copy()

    pearson_r, pearson_p = stats.pearsonr(muestra["concentracion_promedio"], muestra["tasa_cierre"])
    spearman_r, spearman_p = stats.spearmanr(muestra["concentracion_promedio"], muestra["tasa_cierre"])

    print(f"Combinaciones comuna+rubro totales: {len(agg):,}")
    print(f"Combinaciones con exposición suficiente (>= {MIN_EMPRESA_ANIOS} empresa-años): {len(muestra):,}")
    print()
    print("Correlación entre concentración (nº empresas activas) y tasa de cierre:")
    print(f"  Pearson  r = {pearson_r:+.4f}  (p = {pearson_p:.4g})")
    print(f"  Spearman r = {spearman_r:+.4f}  (p = {spearman_p:.4g})")

    return muestra


def segmentar_casos(muestra: pd.DataFrame):
    p75_conc = muestra["concentracion_promedio"].quantile(0.75)
    p75_cierre = muestra["tasa_cierre"].quantile(0.75)
    p25_conc = muestra["concentracion_promedio"].quantile(0.25)

    print(f"\nUmbrales usados — concentración alta: >p75 ({p75_conc:.0f} empresas); tasa de cierre alta: >p75 ({p75_cierre:.4f})")

    saturados = muestra[(muestra["concentracion_promedio"] > p75_conc) & (muestra["tasa_cierre"] > p75_cierre)]
    saludables = muestra[(muestra["concentracion_promedio"] > p75_conc) & (muestra["tasa_cierre"] <= p75_cierre)]
    nicho_bajo = muestra[muestra["concentracion_promedio"] <= p25_conc]

    print(f"\n1) SATURADOS Y RIESGOSOS (alta concentración + alta tasa de cierre): {len(saturados)} combinaciones")
    print(saturados.nlargest(8, "tasa_cierre")[["comuna", "rubro", "concentracion_promedio", "tasa_cierre"]].to_string(index=False))

    print(f"\n2) CONCENTRADOS Y SALUDABLES (alta concentración + baja tasa de cierre): {len(saludables)} combinaciones")
    print(saludables.nsmallest(8, "tasa_cierre")[["comuna", "rubro", "concentracion_promedio", "tasa_cierre"]].to_string(index=False))

    print(f"\n3) BAJA CONCENTRACIÓN (posible espacio de entrada, con la salvedad del tamaño chico de muestra): {len(nicho_bajo)} combinaciones")
    print(nicho_bajo.nsmallest(5, "tasa_cierre")[["comuna", "rubro", "concentracion_promedio", "tasa_cierre"]].to_string(index=False))

    return saturados, saludables, nicho_bajo


def correlacion_por_rubro(agg: pd.DataFrame, min_comunas: int = 30) -> pd.DataFrame:
    """La correlación global mezclando todos los rubros puede ocultar el efecto real,
    porque distintos rubros tienen niveles de rotación muy distintos (financiero vs.
    servicios personales). Aquí se calcula la correlación concentración~cierre POR
    RUBRO, comparando comunas entre sí dentro del mismo rubro — un control simple
    por sector, sin necesitar un modelo de regresión completo."""
    resultados = []
    for rubro, grupo in agg[agg["empresa_anios"] >= 50].groupby("rubro"):
        if len(grupo) < min_comunas:
            continue
        r, p = stats.spearmanr(grupo["concentracion_promedio"], grupo["tasa_cierre"])
        resultados.append({"rubro": rubro, "n_comunas": len(grupo), "spearman_r": r, "p_valor": p})

    df = pd.DataFrame(resultados).sort_values("spearman_r", ascending=False)
    print(f"\n--- Correlación concentración~cierre POR RUBRO (controlando por sector) ---")
    print(f"({min_comunas}+ comunas por rubro, 50+ empresa-años de exposición por combinación)\n")
    print(df.to_string(index=False))
    return df


def main():
    agg = cargar_y_agregar()
    agg.to_csv(OUT_DIR / "pyme_studio_agregado_comuna_rubro.csv", index=False, encoding="utf-8")

    muestra = analizar_correlacion(agg)
    segmentar_casos(muestra)
    corr_rubro = correlacion_por_rubro(agg)
    corr_rubro.to_csv(OUT_DIR / "pyme_studio_correlacion_por_rubro.csv", index=False, encoding="utf-8")


if __name__ == "__main__":
    main()
