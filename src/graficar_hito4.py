"""
PYME Studio — Gráficos de revisión del Hito 4

Genera dispersogramas reales (concentración vs. tasa de cierre, un punto por
comuna) para los rubros clave del análisis, de forma que el hallazgo se pueda
revisar visualmente y no solo confiar en el coeficiente de correlación.

Requiere: pandas, matplotlib
Uso: python graficar_hito4.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

OUT_DIR = Path(__file__).resolve().parent.parent / "outputs"
FIG_DIR = OUT_DIR / "figures"
FIG_DIR.mkdir(exist_ok=True, parents=True)
AGG_PATH = OUT_DIR / "pyme_studio_agregado_comuna_rubro.csv"

RUBROS_A_GRAFICAR = [
    ("COMERCIO AL POR MAYOR Y AL POR MENOR; REPARACION DE VEHICULOS AUTOMOTORES Y MOTOCICLETAS",
     "Comercio al por mayor/menor (r=0.575, p<0.0001)"),
    ("ACTIVIDADES DE ALOJAMIENTO Y DE SERVICIO DE COMIDAS",
     "Alojamiento y servicio de comidas (r=0.359, p<0.0001)"),
    ("AGRICULTURA, GANADERIA, SILVICULTURA Y PESCA",
     "Agricultura, ganadería, pesca (r=-0.268, p<0.0001)"),
    ("ACTIVIDADES FINANCIERAS Y DE SEGUROS",
     "Actividades financieras y de seguros (r=-0.141, p=0.027)"),
]

MIN_EMPRESA_ANIOS = 50

# Misma paleta que dashboard.html — --line, --mark, --paper, --grid, --ink
COLOR_POS = "#1F5C8B"    # confirma la hipótesis (puntos, dispersión)
COLOR_TREND = "#C2632A"  # línea de tendencia
COLOR_BG = "#F6F8FA"
COLOR_GRID = "#D2DEE4"
COLOR_INK = "#16222B"
COLOR_INK_SOFT = "#52697A"


def main():
    plt.rcParams.update({
        "figure.facecolor": COLOR_BG, "axes.facecolor": "#FFFFFF",
        "axes.edgecolor": COLOR_GRID, "axes.labelcolor": COLOR_INK_SOFT,
        "text.color": COLOR_INK, "xtick.color": COLOR_INK_SOFT, "ytick.color": COLOR_INK_SOFT,
        "grid.color": COLOR_GRID, "font.family": "sans-serif",
    })

    agg = pd.read_csv(AGG_PATH)
    agg = agg[agg["empresa_anios"] >= MIN_EMPRESA_ANIOS]

    fig, axes = plt.subplots(2, 2, figsize=(13, 10))
    fig.suptitle(
        "PYME Studio — Concentración vs. tasa de cierre por comuna, dentro de cada rubro\n"
        "(cada punto = una comuna; línea = tendencia lineal)",
        fontsize=13, color=COLOR_INK, fontweight="bold",
    )

    for ax, (rubro, titulo) in zip(axes.flat, RUBROS_A_GRAFICAR):
        datos = agg[agg["rubro"] == rubro]
        ax.scatter(datos["concentracion_promedio"], datos["tasa_cierre"],
                   alpha=0.55, s=24, color=COLOR_POS, edgecolors="none")

        if len(datos) > 2:
            m, b = np.polyfit(datos["concentracion_promedio"], datos["tasa_cierre"], 1)
            xs = np.linspace(datos["concentracion_promedio"].min(), datos["concentracion_promedio"].max(), 50)
            ax.plot(xs, m * xs + b, color=COLOR_TREND, linewidth=2.4)

        ax.set_title(titulo, fontsize=10.5, color=COLOR_INK)
        ax.set_xlabel("Concentración (nº promedio de empresas activas)")
        ax.set_ylabel("Tasa de cierre (cierres / empresa-años)")
        ax.set_xscale("log")
        ax.grid(axis="y", alpha=0.5, linewidth=0.7)
        ax.set_axisbelow(True)
        for spine in ("top", "right"):
            ax.spines[spine].set_visible(False)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    out_path = FIG_DIR / "hito4_dispersion_por_rubro.png"
    plt.savefig(out_path, dpi=140)
    print(f"Gráfico guardado en: {out_path}")


if __name__ == "__main__":
    main()
