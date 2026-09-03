"""
PYME Studio — Pipeline de datos (Hito 3: pipeline de procesamiento funcional)

Une las 3 fuentes del SII en un solo dataset por (año, comuna, rubro):
  1. Aperturas       -> Ciclo_Vida.zip / PUB_actividades_inscritas.txt
  2. Cierres         -> Ciclo_Vida.zip / PUB_TG.txt
  3. Empresas activas -> PUB_COMU_RUBR.xlsb

Requiere: pandas, pyxlsb  (pip install pandas pyxlsb)

Uso:
    python pipeline.py
Genera: ../outputs/pyme_studio_unificado.csv

Los archivos de entrada no vienen incluidos en este repositorio — ver
data/README.md para la fuente oficial, la fecha de descarga y dónde
guardarlos antes de correr este script.
"""
import re
import sys
import unicodedata
import zipfile
from pathlib import Path

import pandas as pd
from pyxlsb import open_workbook

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
OUT_DIR = Path(__file__).resolve().parent.parent / "outputs"

ZIP_PATH = DATA_DIR / "Ciclo_Vida.zip"
XLSB_PATH = DATA_DIR / "PUB_COMU_RUBR.xlsb"


def parsear_recuento(serie: pd.Series) -> pd.Series:
    """'Recuento' viene en formato chileno con '.' como separador de miles
    (ej. '1.400' = mil cuatrocientos, no uno coma cuatro) — hay que quitarlo
    antes de convertir a entero."""
    return serie.str.replace(".", "", regex=False).astype(int)


def normalizar_rubro(texto: str) -> str:
    """Deja comparable el mismo rubro entre archivos con formato distinto:
    'A - Agricultura, ganadería...' y 'AGRICULTURA, GANADERIA...' -> misma clave.
    Quita el código de letra inicial, tildes, y pasa a mayúsculas."""
    texto = re.sub(r"^[A-Z]\s*-\s*", "", str(texto).strip())
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    return texto.upper().strip()


def cargar_cierres() -> pd.DataFrame:
    """PUB_TG.txt: término de giro (cierres).

    Filtra las filas 100% vacías (~27% del archivo original) — se confirmó que
    son líneas de relleno al final del export del SII, no datos reales
    (ver 04_Factibilidad.md). También descarta la categoría residual
    'Valor por Defecto' (rubro sin clasificar), igual que se hace con
    'Sin información' en el archivo de empresas activas.
    """
    with zipfile.ZipFile(ZIP_PATH) as z, z.open("PUB_TG.txt") as f:
        df = pd.read_csv(f, sep="\t", encoding="latin-1", dtype=str)
    return limpiar_cierres(df)


def limpiar_cierres(df: pd.DataFrame) -> pd.DataFrame:
    """Núcleo puro de la limpieza de PUB_TG.txt — sin I/O, para poder probarlo
    con un DataFrame sintético. Espera las columnas crudas del export del SII:
    'Año comercial', 'Comuna', 'Rubro', 'Recuento' (todas como texto)."""
    df = df.dropna(subset=["Año comercial"])  # descarta filas 100% vacías
    df = df[df["Rubro"].str.strip() != "Valor por Defecto"]

    df = df.copy()
    df["anio"] = df["Año comercial"].astype(int)
    df["cierres"] = parsear_recuento(df["Recuento"])
    df["comuna"] = df["Comuna"].str.strip().str.upper()
    df["rubro"] = df["Rubro"].apply(normalizar_rubro)

    return df.groupby(["anio", "comuna", "rubro"], as_index=False)["cierres"].sum()


def cargar_aperturas() -> pd.DataFrame:
    """PUB_actividades_inscritas.txt: aperturas de actividades (no tiene filas vacías)."""
    with zipfile.ZipFile(ZIP_PATH) as z, z.open("PUB_actividades_inscritas.txt") as f:
        df = pd.read_csv(f, sep="\t", encoding="latin-1", dtype=str)
    return limpiar_aperturas(df)


def limpiar_aperturas(df: pd.DataFrame) -> pd.DataFrame:
    """Núcleo puro de la limpieza de PUB_actividades_inscritas.txt — sin I/O.
    Espera las columnas crudas del export del SII: 'Año comercial', 'Comuna',
    'RUBRO', 'Recuento' (todas como texto)."""
    df = df[df["RUBRO"].str.strip() != "Valor por Defecto"]

    df = df.copy()
    df["anio"] = df["Año comercial"].astype(int)
    df["aperturas"] = parsear_recuento(df["Recuento"])
    df["comuna"] = df["Comuna"].str.strip().str.upper()
    df["rubro"] = df["RUBRO"].apply(normalizar_rubro)

    return df.groupby(["anio", "comuna", "rubro"], as_index=False)["aperturas"].sum()


def cargar_empresas_activas() -> pd.DataFrame:
    """PUB_COMU_RUBR.xlsb: número de empresas activas por comuna/rubro/año (2005-2024)."""
    filas = []
    with open_workbook(XLSB_PATH) as wb, wb.get_sheet(1) as sheet:
        for i, row in enumerate(sheet.rows()):
            if i < 5:
                continue
            anio, comuna, rubro, n_empresas = row[0].v, row[1].v, row[4].v, row[5].v
            filas.append((anio, comuna, rubro, n_empresas))
    return limpiar_empresas_activas(filas)


def limpiar_empresas_activas(filas: list) -> pd.DataFrame:
    """Núcleo puro de la limpieza de PUB_COMU_RUBR.xlsb — sin I/O. `filas` es
    una lista de tuplas crudas (anio, comuna, rubro, n_empresas), tal como se
    leen fila a fila de la hoja de cálculo (n_empresas puede ser None)."""
    limpias = []
    for anio, comuna, rubro, n_empresas in filas:
        if anio is None or comuna is None or rubro is None:
            continue
        if rubro == "Sin información" or comuna == "Sin Información":
            continue
        limpias.append((int(anio), str(comuna).strip().upper(), normalizar_rubro(rubro), n_empresas or 0))

    df = pd.DataFrame(limpias, columns=["anio", "comuna", "rubro", "empresas_activas"])
    return df.groupby(["anio", "comuna", "rubro"], as_index=False)["empresas_activas"].sum()


def combinar_fuentes(aperturas: pd.DataFrame, cierres: pd.DataFrame, activas: pd.DataFrame) -> pd.DataFrame:
    """Núcleo puro de la unión — sin I/O, para poder probarlo con datos sintéticos.
    Cada argumento ya viene agrupado por (anio, comuna, rubro), como devuelven
    cargar_aperturas/cargar_cierres/cargar_empresas_activas."""
    df = aperturas.merge(cierres, on=["anio", "comuna", "rubro"], how="outer")
    df = df.merge(activas, on=["anio", "comuna", "rubro"], how="outer")

    for col in ["aperturas", "cierres", "empresas_activas"]:
        df[col] = df[col].fillna(0).astype(int)

    # Tasa de cierre: cierres del año / empresas activas ese mismo año.
    # Con empresas_activas = 0 la tasa queda indefinida (NaN), no se fuerza a 0.
    denom = df["empresas_activas"].astype(float).replace(0, float("nan"))
    df["tasa_cierre"] = (df["cierres"] / denom).round(4)

    return df.sort_values(["anio", "comuna", "rubro"]).reset_index(drop=True)


def unir_fuentes() -> pd.DataFrame:
    aperturas = cargar_aperturas()
    cierres = cargar_cierres()
    activas = cargar_empresas_activas()
    return combinar_fuentes(aperturas, cierres, activas)


def verificar_entradas() -> None:
    """Falla con un mensaje claro (en vez de un traceback críptico) si faltan
    los archivos de entrada — el caso más común al clonar el repositorio por
    primera vez, ya que data/raw/ no viene incluido (ver data/README.md)."""
    faltantes = [p.name for p in (ZIP_PATH, XLSB_PATH) if not p.exists()]
    if faltantes:
        print("No se encontraron los archivos de entrada necesarios en data/raw/:")
        for nombre in faltantes:
            print(f"  - {nombre}")
        print("\nEstos archivos no vienen incluidos en el repositorio (ver data/README.md")
        print("para la URL oficial del SII, la fecha de descarga y dónde guardarlos).")
        sys.exit(1)
    with zipfile.ZipFile(ZIP_PATH) as z:
        internos_faltantes = [n for n in ("PUB_TG.txt", "PUB_actividades_inscritas.txt") if n not in z.namelist()]
    if internos_faltantes:
        print(f"Ciclo_Vida.zip existe pero no contiene: {', '.join(internos_faltantes)}")
        print("¿Es el archivo correcto? Ver data/README.md para la fuente oficial.")
        sys.exit(1)


def main():
    verificar_entradas()
    OUT_DIR.mkdir(exist_ok=True)
    df = unir_fuentes()
    out_path = OUT_DIR / "pyme_studio_unificado.csv"
    df.to_csv(out_path, index=False, encoding="utf-8")

    print(f"Dataset unificado: {len(df):,} filas -> {out_path}")
    print(f"Años cubiertos: {df['anio'].min()}-{df['anio'].max()}")
    print(f"Comunas distintas: {df['comuna'].nunique()}")
    print(f"Rubros distintos: {df['rubro'].nunique()}")

    print("\nTop 10 comuna+rubro con mayor tasa de cierre en 2024 (min. 20 empresas activas):")
    muestra = df[(df["anio"] == 2024) & (df["empresas_activas"] >= 20)]
    top = muestra.nlargest(10, "tasa_cierre")
    print(top[["comuna", "rubro", "empresas_activas", "aperturas", "cierres", "tasa_cierre"]].to_string(index=False))


if __name__ == "__main__":
    main()
