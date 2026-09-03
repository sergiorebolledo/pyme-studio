"""
PYME Studio — Gráficos adicionales del Hito 4

Complementa graficar_hito4.py (dispersogramas) con 3 tipos de gráfico
distintos, que muestran dimensiones de los datos que la dispersión no
cubre:

  1. Barras horizontales: ranking de correlación concentración~cierre
     por rubro, con los 19 rubros lado a lado (visualiza la tabla del
     análisis de un vistazo, coloreado por significancia estadística).
  2. Serie de tiempo: aperturas y cierres a nivel nacional, 2005-2024
     (dimensión temporal — ningún gráfico anterior mostraba esto).
  3. Boxplot: distribución completa de la tasa de cierre por rubro
     (muestra la variabilidad dentro de cada sector, no solo su
     promedio o su correlación con la concentración).

Requiere: pandas, matplotlib
Uso: python graficar_hito4_extra.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

OUT_DIR = Path(__file__).resolve().parent.parent / "outputs"
FIG_DIR = OUT_DIR / "figures"
FIG_DIR.mkdir(exist_ok=True, parents=True)
UNIFICADO_PATH = OUT_DIR / "pyme_studio_unificado.csv"
AGG_PATH = OUT_DIR / "pyme_studio_agregado_comuna_rubro.csv"
CORR_RUBRO_PATH = OUT_DIR / "pyme_studio_correlacion_por_rubro.csv"

# Misma paleta que dashboard/pyme_studio_dashboard.html — --line, --mark, --grid, --paper, --ink
COLOR_POS = "#1F5C8B"     # confirma la hipótesis
COLOR_NEG = "#C2632A"     # invierte la hipótesis
COLOR_NS = "#B9C7CE"      # no significativo
COLOR_BG = "#F6F8FA"
COLOR_GRID = "#D2DEE4"
COLOR_INK = "#16222B"
COLOR_INK_SOFT = "#52697A"


def _estilo():
    plt.rcParams.update({
        "figure.facecolor": COLOR_BG, "axes.facecolor": "#FFFFFF",
        "axes.edgecolor": COLOR_GRID, "axes.labelcolor": COLOR_INK_SOFT,
        "text.color": COLOR_INK, "xtick.color": COLOR_INK_SOFT, "ytick.color": COLOR_INK_SOFT,
        "grid.color": COLOR_GRID, "font.family": "sans-serif",
    })


def acortar(texto: str, n: int = 42) -> str:
    return texto if len(texto) <= n else texto[: n - 1] + "…"


def grafico_barras_correlacion():
    _estilo()
    df = pd.read_csv(CORR_RUBRO_PATH).sort_values("spearman_r")
    colores = [
        COLOR_NS if p >= 0.05 else (COLOR_POS if r > 0 else COLOR_NEG)
        for r, p in zip(df["spearman_r"], df["p_valor"])
    ]

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.barh(df["rubro"].apply(acortar), df["spearman_r"], color=colores)
    ax.axvline(0, color=COLOR_INK, linewidth=0.9)
    ax.set_xlabel("Correlación de Spearman (concentración vs. tasa de cierre)")
    ax.set_title(
        "Correlación concentración~cierre por rubro\n"
        "azul = confirma la hipótesis · naranjo = la invierte · gris = no significativo (p≥0.05)",
        fontsize=10.5, color=COLOR_INK, fontweight="bold", loc="left",
    )
    ax.grid(axis="x", alpha=0.5, linewidth=0.7)
    ax.set_axisbelow(True)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    plt.tight_layout()
    out = FIG_DIR / "hito4_barras_correlacion_por_rubro.png"
    plt.savefig(out, dpi=140)
    plt.close(fig)
    print(f"Guardado: {out}")


def grafico_serie_tiempo():
    _estilo()
    df = pd.read_csv(UNIFICADO_PATH)
    anual = df.groupby("anio", as_index=False)[["aperturas", "cierres"]].sum()

    fig, ax = plt.subplots(figsize=(11, 5.5))
    ax.plot(anual["anio"], anual["aperturas"], marker="o", color=COLOR_POS, linewidth=2.2, markersize=5, label="Aperturas")
    ax.plot(anual["anio"], anual["cierres"], marker="o", color=COLOR_NEG, linewidth=2.2, markersize=5, label="Cierres (término de giro)")
    ax.axvspan(2020, 2021, color=COLOR_INK_SOFT, alpha=0.12, label="Pandemia (2020-2021)")
    ax.set_xlabel("Año")
    ax.set_ylabel("Nº de empresas (nacional, todos los rubros)")
    ax.set_title("Aperturas y cierres de pymes a nivel nacional, 2005-2024", color=COLOR_INK, fontweight="bold")
    ax.legend(frameon=False)
    ax.grid(axis="y", alpha=0.5, linewidth=0.7)
    ax.set_axisbelow(True)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    plt.tight_layout()
    out = FIG_DIR / "hito4_serie_tiempo_nacional.png"
    plt.savefig(out, dpi=140)
    plt.close(fig)
    print(f"Guardado: {out}")


def grafico_boxplot_rubro():
    _estilo()
    agg = pd.read_csv(AGG_PATH)
    agg = agg[agg["empresa_anios"] >= 50]

    orden = agg.groupby("rubro")["tasa_cierre"].median().sort_values().index
    datos = [agg[agg["rubro"] == r]["tasa_cierre"].values for r in orden]

    fig, ax = plt.subplots(figsize=(10, 8))
    bp = ax.boxplot(datos, vert=False, tick_labels=[acortar(r) for r in orden], showfliers=False,
                     patch_artist=True, boxprops=dict(facecolor="#DCEAF4", edgecolor=COLOR_POS),
                     medianprops=dict(color=COLOR_NEG, linewidth=1.8),
                     whiskerprops=dict(color=COLOR_INK_SOFT), capprops=dict(color=COLOR_INK_SOFT))
    ax.set_xlabel("Tasa de cierre (cierres / empresa-años), por comuna dentro del rubro")
    ax.set_title("Distribución de la tasa de cierre por rubro\n(cada caja resume todas las comunas de ese rubro; sin valores atípicos extremos)",
                  fontsize=11.5, color=COLOR_INK, fontweight="bold")
    ax.grid(axis="x", alpha=0.5, linewidth=0.7)
    ax.set_axisbelow(True)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    plt.tight_layout()
    out = FIG_DIR / "hito4_boxplot_tasa_cierre_por_rubro.png"
    plt.savefig(out, dpi=140)
    plt.close(fig)
    print(f"Guardado: {out}")


if __name__ == "__main__":
    grafico_barras_correlacion()
    grafico_serie_tiempo()
    grafico_boxplot_rubro()
