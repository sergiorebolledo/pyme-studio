"""
PYME Studio — Alcance del universo analizado: ¿son pymes?

`PUB_COMU_RUBR.xlsb` (la fuente que usa pipeline.py) NO permite clasificar
tamaño de empresa — es un agregado (total de ventas/trabajadores por
comuna+rubro+año), sin desglose por tramo. El pipeline cuenta TODO
contribuyente con actividad vigente, sin filtrar por tamaño.

El SII sí publica la clasificación oficial en archivos separados, con dos
criterios que no necesariamente coinciden:

  (a) Por N° de trabajadores (0-9 / 10-49 / 50-249 / 250+):
      PUB_RUBR_TRTRAB.xlsb, PUB_COMU_TRTRAB.xlsb

  (b) Por ventas anuales en UF — la clasificación LEGAL/oficial de pyme en
      Chile (Ley 20.416): Micro <=2.400 UF, Pequeña <=25.000 UF,
      Mediana <=100.000 UF, Grande sobre eso:
      PUB_TRAM5_RUBR.xlsb, PUB_TRAM5_COMU.xlsb

Este script calcula qué % de las "empresas activas" que mide el pipeline
son pyme según cada clasificación, a nivel rubro nacional. No modifica
pipeline.py ni sus resultados — es un chequeo de alcance, cuyo resultado
se usa para documentar (no inventar) qué tan válido es llamar "pyme" al
universo medido.

Requiere: pandas, pyxlsb
Uso: python analisis_tamano_empresas.py
"""
import re
import sys
import unicodedata
from pathlib import Path

import pandas as pd
from pyxlsb import open_workbook

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
OUT_DIR = Path(__file__).resolve().parent.parent / "outputs"

TRAMO_GRANDE_TRABAJADORES = "4) 250 O MAS TRABAJADORES INFORMADOS"
TRAMO_GRANDE_VENTAS = "GRANDE"


def normalizar_texto(texto: str) -> str:
    return unicodedata.normalize("NFKD", str(texto)).encode("ascii", "ignore").decode("ascii").strip()


def normalizar_rubro(texto: str) -> str:
    texto = re.sub(r"^[A-Z]\s*-\s*", "", str(texto).strip())
    return normalizar_texto(texto).upper()


def leer_xlsb(path: Path, col_dim: int, col_tramo: int, col_n: int, es_rubro: bool) -> pd.DataFrame:
    filas = []
    with open_workbook(path) as wb, wb.get_sheet(1) as sheet:
        for i, row in enumerate(sheet.rows()):
            if i < 5:
                continue
            anio, dim, tramo, n = row[0].v, row[col_dim].v, row[col_tramo].v, row[col_n].v
            if anio is None or dim is None or tramo is None:
                continue
            dim_norm = normalizar_rubro(dim) if es_rubro else normalizar_texto(dim).upper()
            if dim_norm == "SIN INFORMACION":
                continue
            filas.append((int(anio), dim_norm, normalizar_texto(tramo).upper(), n or 0))

    col_name = "rubro" if es_rubro else "comuna"
    df = pd.DataFrame(filas, columns=["anio", col_name, "tramo", "n_empresas"])
    df["n_empresas"] = pd.to_numeric(df["n_empresas"], errors="coerce").fillna(0)
    return df


def resumen_pct_pyme(df: pd.DataFrame, dim_col: str, tramo_grande: str) -> pd.DataFrame:
    agg = df.groupby([dim_col, "tramo"], as_index=False)["n_empresas"].sum()
    total = agg.groupby(dim_col)["n_empresas"].sum().rename("total_empresas")
    grandes = agg[agg["tramo"] == tramo_grande].groupby(dim_col)["n_empresas"].sum().rename("empresas_grandes")

    r = pd.concat([total, grandes], axis=1).fillna(0)
    r["empresas_grandes"] = r["empresas_grandes"].astype(int)
    r["total_empresas"] = r["total_empresas"].astype(int)
    r["pct_grande"] = (r["empresas_grandes"] / r["total_empresas"].replace(0, pd.NA) * 100).round(2)
    r["pct_pyme"] = (100 - r["pct_grande"]).round(2)
    return r.reset_index().sort_values("pct_grande", ascending=False)


ARCHIVOS_REQUERIDOS = ["PUB_TRAM5_RUBR.xlsb", "PUB_TRAM5_COMU.xlsb", "PUB_RUBR_TRTRAB.xlsb", "PUB_COMU_TRTRAB.xlsb"]


def verificar_entradas() -> None:
    faltantes = [n for n in ARCHIVOS_REQUERIDOS if not (DATA_DIR / n).exists()]
    if faltantes:
        print("No se encontraron los archivos de entrada necesarios en data/raw/:")
        for nombre in faltantes:
            print(f"  - {nombre}")
        print("\nEstos archivos no vienen incluidos en el repositorio — ver data/README.md")
        print("para la URL oficial del SII, la fecha de descarga y dónde guardarlos.")
        sys.exit(1)


def main():
    verificar_entradas()
    print("=== Clasificación oficial por VENTAS (Ley 20.416) ===")
    df_rubro_vta = leer_xlsb(DATA_DIR / "PUB_TRAM5_RUBR.xlsb", col_dim=2, col_tramo=1, col_n=3, es_rubro=True)
    r_rubro_vta = resumen_pct_pyme(df_rubro_vta, "rubro", TRAMO_GRANDE_VENTAS)

    df_comuna_vta = leer_xlsb(DATA_DIR / "PUB_TRAM5_COMU.xlsb", col_dim=2, col_tramo=1, col_n=5, es_rubro=False)
    r_comuna_vta = resumen_pct_pyme(df_comuna_vta, "comuna", TRAMO_GRANDE_VENTAS)

    print("=== Clasificación por N° DE TRABAJADORES (referencia, no oficial) ===")
    df_rubro_trab = leer_xlsb(DATA_DIR / "PUB_RUBR_TRTRAB.xlsb", col_dim=1, col_tramo=2, col_n=3, es_rubro=True)
    r_rubro_trab = resumen_pct_pyme(df_rubro_trab, "rubro", TRAMO_GRANDE_TRABAJADORES)

    df_comuna_trab = leer_xlsb(DATA_DIR / "PUB_COMU_TRTRAB.xlsb", col_dim=1, col_tramo=4, col_n=5, es_rubro=False)
    r_comuna_trab = resumen_pct_pyme(df_comuna_trab, "comuna", TRAMO_GRANDE_TRABAJADORES)

    comp = r_rubro_vta[["rubro", "pct_pyme"]].rename(columns={"pct_pyme": "pct_pyme_ventas_oficial"}).merge(
        r_rubro_trab[["rubro", "pct_pyme"]].rename(columns={"pct_pyme": "pct_pyme_trabajadores"}), on="rubro"
    )
    comp["diferencia_pp"] = (comp["pct_pyme_ventas_oficial"] - comp["pct_pyme_trabajadores"]).round(2)
    comp = comp.sort_values("pct_pyme_ventas_oficial")

    OUT_DIR.mkdir(exist_ok=True)
    comp.to_csv(OUT_DIR / "pyme_studio_alcance_pyme_por_rubro.csv", index=False, encoding="utf-8")
    r_comuna_vta.to_csv(OUT_DIR / "pyme_studio_alcance_pyme_por_comuna.csv", index=False, encoding="utf-8")

    print("\n--- % pyme por rubro (clasificación oficial por ventas, Ley 20.416) ---\n")
    with pd.option_context("display.width", 120):
        print(comp.to_string(index=False))

    print(f"\n--- Nacional, por comuna: promedio {r_comuna_vta['pct_grande'].mean():.2f}% grande, mediana {r_comuna_vta['pct_grande'].median():.2f}% ---")

    foco = comp[comp["rubro"].str.contains("COMERCIO AL POR MAYOR|ALOJAMIENTO", regex=True)]
    print("\n--- Los 2 rubros del hallazgo central ---")
    print(foco.to_string(index=False))

    minimo = comp["pct_pyme_ventas_oficial"].min()
    print(f"\nMínimo de %pyme entre todos los rubros (clasificación oficial): {minimo:.2f}%")
    print(f"Guardado: {OUT_DIR / 'pyme_studio_alcance_pyme_por_rubro.csv'}")
    print(f"Guardado: {OUT_DIR / 'pyme_studio_alcance_pyme_por_comuna.csv'}")


if __name__ == "__main__":
    main()
