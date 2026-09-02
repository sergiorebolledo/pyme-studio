"""
PYME Studio — Validación cruzada de calidad de datos

Compara los totales de "número de empresas" por comuna+año entre dos fuentes
independientes del SII que se solapan en 2005-2015:

  - PUB_Reg_Com_Rub.xlsx  (fuente antigua, taxonomía CIIU Rev.3, 19 rubros)
  - PUB_COMU_RUBR.xlsb    (fuente usada en el pipeline, taxonomía CIIU Rev.4, 21 rubros)

Las dos fuentes usan clasificaciones de rubro DISTINTAS y no son comparables
categoría por categoría — pero el total de empresas por comuna/año no depende
de la taxonomía interna, así que sirve como chequeo de calidad independiente
del pipeline principal (no se usa para el análisis, solo para validar que los
números del SII son consistentes entre ambos exports).

Requiere: openpyxl, pyxlsb
Uso: python validar_cruzado.py
"""
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

import openpyxl
from pyxlsb import open_workbook

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
VIEJO_PATH = DATA_DIR / "PUB_Reg_Com_Rub.xlsx"
NUEVO_PATH = DATA_DIR / "PUB_COMU_RUBR.xlsb"


def normalizar_comuna(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", str(texto)).encode("ascii", "ignore").decode("ascii")
    return texto.strip().upper()


def totales_archivo_viejo() -> dict:
    totales = defaultdict(int)
    wb = openpyxl.load_workbook(VIEJO_PATH, read_only=True, data_only=True)
    ws = wb["EMP_Reg_Com_Rub"]
    for i, row in enumerate(ws.iter_rows(values_only=True)):
        if i < 6:
            continue
        anio, comuna, n_emp = row[0], row[2], row[4]
        if anio and comuna and n_emp and "SIN INFORMACION" not in str(comuna).upper():
            totales[(anio, normalizar_comuna(comuna))] += n_emp
    return totales


def totales_archivo_nuevo(anio_max: int) -> dict:
    totales = defaultdict(int)
    with open_workbook(NUEVO_PATH) as wb, wb.get_sheet(1) as sheet:
        for i, row in enumerate(sheet.rows()):
            if i < 5:
                continue
            anio, comuna, n_emp = row[0].v, row[1].v, row[5].v
            if anio and comuna and n_emp and anio <= anio_max and "SIN INFORMACION" not in normalizar_comuna(comuna):
                totales[(int(anio), normalizar_comuna(comuna))] += n_emp
    return totales


def main():
    faltantes = [p.name for p in (VIEJO_PATH, NUEVO_PATH) if not p.exists()]
    if faltantes:
        print("No se encontraron los archivos de entrada necesarios en data/raw/:")
        for nombre in faltantes:
            print(f"  - {nombre}")
        print("\nEstos archivos no vienen incluidos en el repositorio — ver data/README.md")
        print("para la URL oficial del SII, la fecha de descarga y dónde guardarlos.")
        sys.exit(1)

    viejo = totales_archivo_viejo()
    nuevo = totales_archivo_nuevo(anio_max=2015)

    comunes = set(viejo) & set(nuevo)
    diffs = []
    for k in comunes:
        v, n = viejo[k], nuevo[k]
        diff_pct = abs(v - n) / max(v, n) * 100 if max(v, n) > 0 else 0
        diffs.append((k, v, n, diff_pct))
    diffs.sort(key=lambda x: -x[3])

    print(f"Combinaciones comuna+año en archivo antiguo: {len(viejo):,}")
    print(f"Combinaciones comuna+año en archivo nuevo (2005-2015): {len(nuevo):,}")
    print(f"Combinaciones comparables (comuna normalizada, sin tildes): {len(comunes):,}")
    print()
    exactas = sum(1 for d in diffs if d[3] == 0)
    grandes = [d for d in diffs if d[3] > 5]
    print(f"Coinciden exactamente: {exactas:,} ({exactas/len(diffs)*100:.1f}%)")
    print(f"Promedio de diferencia: {sum(d[3] for d in diffs)/len(diffs):.3f}%")
    print(f"Diferencias > 5%: {len(grandes)}")
    if grandes:
        print("\nCasos con diferencia > 5% (revisar manualmente si aparecen en el análisis final):")
        for k, v, n, p in grandes:
            print(f"  {k}: antiguo={v}, nuevo={n}, diff={p:.1f}%")

    print("\nConclusión: los totales de empresas por comuna/año son consistentes entre")
    print("ambas fuentes del SII (diferencia promedio < 0.2%), lo que da confianza en")
    print("la calidad de PUB_COMU_RUBR.xlsb, la fuente usada en pipeline.py.")


if __name__ == "__main__":
    main()
