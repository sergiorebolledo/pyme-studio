"""
PYME Studio — orquestador del flujo completo.

Corre, en orden, todo lo necesario para reproducir el proyecto desde los
archivos originales de data/raw/ hasta el dashboard final. Se detiene en el
primer script que falle (código de salida distinto de 0) y muestra un
mensaje claro de en qué etapa quedó.

Requiere: las dependencias de requirements.txt (`pip install -r requirements.txt`,
corrido desde la raíz del repositorio) y los archivos de entrada descritos en
data/README.md (no vienen incluidos en el repositorio — hay que descargarlos
del SII primero).

NO regenera la presentación (docs/presentacion/*.pptx) — eso requiere Node.js
y sus dependencias, que pueden no estar instaladas. Al final imprime el
comando exacto para hacerlo manualmente.

Uso:
    python run_pipeline.py                  # corre todo (reusa outputs/geo_comunas.json ya incluido)
    python run_pipeline.py --regenerar-geo   # además reconstruye el mapa desde cero
                                              # (requiere haber descargado data/reference/geo_raw/, ver data/README.md)
"""
import os
import subprocess
import sys
import time
from pathlib import Path

# En Windows, la consola por defecto (cp1252) no puede imprimir algunos
# caracteres y el script puede morir con UnicodeEncodeError justo después de
# que un paso terminó bien. Forzar UTF-8 en stdout/stderr evita eso.
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

ROOT = Path(__file__).resolve().parent
SRC_DIR = ROOT / "src"

ETAPAS = [
    ("Pipeline principal (une las 3 fuentes en un dataset único)", "pipeline.py"),
    ("Validación cruzada de calidad", "validar_cruzado.py"),
    ("Reporte de calidad reproducible", "validar_calidad.py"),
    ("Análisis principal (correlación concentración~cierre)", "analisis_hito4.py"),
    ("Alcance del universo — clasificación oficial de tamaño de empresa", "analisis_tamano_empresas.py"),
    ("Sensibilidad a 2016 y concentración relativa", "analisis_metodologia.py"),
    ("Corrección por comparaciones múltiples (FDR y Bonferroni)", "analisis_comparaciones_multiples.py"),
    ("Estabilidad por subperíodo", "analisis_subperiodos.py"),
    ("Gráfico — dispersión por rubro", "graficar_hito4.py"),
    ("Gráficos — barras, serie de tiempo, boxplot", "graficar_hito4_extra.py"),
    ("__GEO__", "preparar_geo_comunas.py"),  # opcional, ver --regenerar-geo
    ("Construcción del dashboard", "construir_dashboard.py"),
]


def correr(nombre: str, script: str) -> bool:
    print(f"\n{'=' * 70}\n{nombre}  ({script})\n{'=' * 70}")
    t0 = time.time()
    env = {**os.environ, "PYTHONUTF8": "1"}
    resultado = subprocess.run([sys.executable, script], cwd=SRC_DIR, env=env)
    dt = time.time() - t0
    if resultado.returncode != 0:
        print(f"\n[FALLO] {script} (código {resultado.returncode}, {dt:.1f}s)")
        print(f"   Etapa: {nombre}")
        print("   El flujo se detiene aquí. Revisa el mensaje de error de arriba,")
        print("   corrige lo necesario (¿faltan archivos en data/raw/? ver data/README.md)")
        print("   y vuelve a ejecutar `python run_pipeline.py`.")
        return False
    print(f"\n[OK] {script} ({dt:.1f}s)")
    return True


def main():
    regenerar_geo = "--regenerar-geo" in sys.argv

    print("PYME Studio — ejecutando el flujo completo")
    print(f"Directorio de código fuente: {SRC_DIR}")
    if not regenerar_geo:
        print("(se reutiliza outputs/geo_comunas.json, ya incluido en el repositorio;")
        print(" usa --regenerar-geo para reconstruir el mapa desde cero)")

    for nombre, script in ETAPAS:
        if nombre == "__GEO__":
            if not regenerar_geo:
                geo_path = ROOT / "outputs" / "geo_comunas.json"
                if not geo_path.exists():
                    print(f"\n[FALLO] outputs/geo_comunas.json no existe y no se pasó --regenerar-geo.")
                    sys.exit(1)
                print(f"\n(Saltado) preparar_geo_comunas.py — se reusa outputs/geo_comunas.json")
                continue
            nombre, script = "Geometría del mapa (reconstrucción completa)", "preparar_geo_comunas.py"

        ok = correr(nombre, script)
        if not ok:
            sys.exit(1)

    print(f"\n{'=' * 70}")
    print("Flujo completo terminado sin errores.")
    print(f"{'=' * 70}")
    print("\nLo único que no se regeneró automáticamente es la presentación (usa Node.js,")
    print("no Python). Si el entorno tiene Node y npm instalados, corre:")
    print("\n  cd docs/presentacion/build")
    print("  npm install")
    print("  node gen_icons.js     # solo si cambiaron los íconos")
    print("  node build_deck.js    # regenera docs/presentacion/PYME_Studio_Presentacion.pptx")
    print("\nRevisa outputs/reporte_calidad.md para el estado de calidad de los datos.")


if __name__ == "__main__":
    main()
