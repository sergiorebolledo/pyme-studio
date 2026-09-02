"""
PYME Studio — Robustez metodológica: sensibilidad a 2016 y concentración relativa.

No modifica ni sobrescribe analisis_hito4.py ni sus salidas — lee la misma
fuente (`pyme_studio_unificado.csv`) y genera archivos NUEVOS, separados,
para poder comparar contra los resultados originales sin perder trazabilidad.

Dos chequeos:

1. SENSIBILIDAD A 2016 — el salto de término de giro en 2016 (Ley 20.899,
   ver 09_Analisis_Hito4.md) podría estar inflando artificialmente la
   correlación concentración~cierre. Se recalcula la correlación por rubro
   incluyendo y excluyendo 2016, y se compara.

2. CONCENTRACIÓN RELATIVA — "concentración" en el análisis original es el
   promedio ABSOLUTO de empresas activas, lo que favorece naturalmente a
   comunas grandes (Santiago va a tener más empresas de cualquier rubro
   solo por ser más poblada). Se agrega una medida relativa:
   participacion_rubro_comuna = empresas activas del rubro / total de
   empresas activas de la comuna (mismo año), y se compara la correlación
   con tasa de cierre bajo ambas métricas.

Requiere: pandas, scipy, matplotlib
Uso: python analisis_metodologia.py
"""
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

OUT_DIR = Path(__file__).resolve().parent.parent / "outputs"
FIG_DIR = OUT_DIR / "figures"
FIG_DIR.mkdir(exist_ok=True, parents=True)
IN_PATH = OUT_DIR / "pyme_studio_unificado.csv"

MIN_EMPRESA_ANIOS = 50
MIN_COMUNAS = 30
ANIO_SALTO = 2016

COLOR_POS = "#1F5C8B"
COLOR_NEG = "#C2632A"
COLOR_NS = "#B9C7CE"
COLOR_INK = "#16222B"
COLOR_GRID = "#D2DEE4"


def agregar(df: pd.DataFrame) -> pd.DataFrame:
    agg = df.groupby(["comuna", "rubro"], as_index=False).agg(
        cierres_total=("cierres", "sum"),
        empresa_anios=("empresas_activas", "sum"),
        concentracion_promedio=("empresas_activas", "mean"),
    )
    agg["tasa_cierre"] = agg["cierres_total"] / agg["empresa_anios"]
    return agg


def correlacion_por_rubro(agg: pd.DataFrame, columna: str = "concentracion_promedio") -> pd.DataFrame:
    resultados = []
    for rubro, grupo in agg[agg["empresa_anios"] >= MIN_EMPRESA_ANIOS].groupby("rubro"):
        if len(grupo) < MIN_COMUNAS:
            continue
        r, p = stats.spearmanr(grupo[columna], grupo["tasa_cierre"])
        resultados.append({"rubro": rubro, "n_comunas": len(grupo), "spearman_r": r, "p_valor": p})
    return pd.DataFrame(resultados)


# ============================================================ 1. SENSIBILIDAD A 2016
def sensibilidad_2016(uni: pd.DataFrame) -> pd.DataFrame:
    con_2016 = correlacion_por_rubro(agregar(uni))
    sin_2016 = correlacion_por_rubro(agregar(uni[uni["anio"] != ANIO_SALTO]))

    comp = con_2016.merge(sin_2016, on="rubro", suffixes=("_con_2016", "_sin_2016"))
    comp = comp.rename(columns={"n_comunas_con_2016": "n_comunas"}).drop(columns=["n_comunas_sin_2016"])
    comp["diferencia_r"] = (comp["spearman_r_con_2016"] - comp["spearman_r_sin_2016"]).round(4)
    comp["cambia_signo"] = (comp["spearman_r_con_2016"] > 0) != (comp["spearman_r_sin_2016"] > 0)
    comp["sig_con_2016"] = comp["p_valor_con_2016"] < 0.05
    comp["sig_sin_2016"] = comp["p_valor_sin_2016"] < 0.05
    comp["cambia_conclusion"] = comp["cambia_signo"] | (comp["sig_con_2016"] != comp["sig_sin_2016"])
    comp = comp.sort_values("spearman_r_con_2016", ascending=False)

    cols = [
        "rubro", "n_comunas",
        "spearman_r_con_2016", "p_valor_con_2016",
        "spearman_r_sin_2016", "p_valor_sin_2016",
        "diferencia_r", "cambia_signo", "cambia_conclusion",
    ]
    out = comp[cols]
    out_path = OUT_DIR / "pyme_studio_sensibilidad_2016.csv"
    out.to_csv(out_path, index=False, encoding="utf-8")

    print("=== Sensibilidad a 2016 ===")
    with pd.option_context("display.width", 140):
        print(out.to_string(index=False))
    n_cambia = out["cambia_conclusion"].sum()
    print(f"\nRubros cuya conclusión (signo o significancia) cambia al excluir 2016: {n_cambia} de {len(out)}")
    print(f"Guardado: {out_path}")

    # Gráfico comparativo: barras apareadas con vs. sin 2016, para los rubros con suficiente muestra.
    plt.rcParams.update({
        "figure.facecolor": "#F6F8FA", "axes.facecolor": "#FFFFFF",
        "axes.edgecolor": COLOR_GRID, "text.color": COLOR_INK,
        "xtick.color": COLOR_INK, "ytick.color": COLOR_INK, "font.family": "sans-serif",
    })
    plot_df = out.sort_values("spearman_r_con_2016")
    y = range(len(plot_df))
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.barh([i + 0.2 for i in y], plot_df["spearman_r_con_2016"], height=0.36, color=COLOR_POS, label="Con 2016 (original)")
    ax.barh([i - 0.2 for i in y], plot_df["spearman_r_sin_2016"], height=0.36, color=COLOR_NEG, label="Sin 2016")
    ax.set_yticks(list(y))
    ax.set_yticklabels([r[:42] + ("…" if len(r) > 42 else "") for r in plot_df["rubro"]], fontsize=8.5)
    ax.axvline(0, color=COLOR_INK, linewidth=0.9)
    ax.set_xlabel("Correlación de Spearman (concentración vs. tasa de cierre)")
    ax.set_title("Sensibilidad de la correlación al excluir 2016\n(Ley 20.899 — término de giro declarado de oficio)", fontsize=11, fontweight="bold", loc="left")
    ax.legend(frameon=False, loc="lower right")
    ax.grid(axis="x", alpha=0.4)
    ax.set_axisbelow(True)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    plt.tight_layout()
    fig_path = FIG_DIR / "hito4_sensibilidad_2016.png"
    plt.savefig(fig_path, dpi=150)
    plt.close(fig)
    print(f"Gráfico guardado: {fig_path}")

    return out


# ============================================================ 2. CONCENTRACIÓN RELATIVA
def concentracion_relativa(uni: pd.DataFrame) -> pd.DataFrame:
    total_comuna_anio = uni.groupby(["anio", "comuna"])["empresas_activas"].transform("sum").astype(float)
    uni = uni.copy()
    uni["participacion_rubro_comuna"] = (uni["empresas_activas"] / total_comuna_anio.replace(0, float("nan"))).round(6)

    enriquecido = uni.groupby(["comuna", "rubro"], as_index=False).agg(
        aperturas_total=("aperturas", "sum"),
        cierres_total=("cierres", "sum"),
        empresa_anios=("empresas_activas", "sum"),
        concentracion_promedio=("empresas_activas", "mean"),
        participacion_promedio=("participacion_rubro_comuna", "mean"),
    )
    enriquecido["tasa_cierre"] = enriquecido["cierres_total"] / enriquecido["empresa_anios"]

    out_path = OUT_DIR / "pyme_studio_agregado_comuna_rubro_enriquecido.csv"
    enriquecido.to_csv(out_path, index=False, encoding="utf-8")
    print(f"\n=== Concentración relativa ===")
    print(f"Dataset agregado enriquecido (con participacion_promedio) guardado en: {out_path}")
    print("(el archivo original pyme_studio_agregado_comuna_rubro.csv NO se modifica)")

    corr_abs = correlacion_por_rubro(enriquecido, "concentracion_promedio").rename(
        columns={"spearman_r": "r_absoluta", "p_valor": "p_absoluta"}
    )
    corr_rel = correlacion_por_rubro(enriquecido, "participacion_promedio").rename(
        columns={"spearman_r": "r_relativa", "p_valor": "p_relativa"}
    )
    comp = corr_abs.merge(corr_rel[["rubro", "r_relativa", "p_relativa"]], on="rubro")
    comp["mismo_signo"] = (comp["r_absoluta"] > 0) == (comp["r_relativa"] > 0)
    comp["sig_absoluta"] = comp["p_absoluta"] < 0.05
    comp["sig_relativa"] = comp["p_relativa"] < 0.05
    comp = comp.sort_values("r_absoluta", ascending=False)

    out_path2 = OUT_DIR / "pyme_studio_concentracion_absoluta_vs_relativa.csv"
    comp.to_csv(out_path2, index=False, encoding="utf-8")

    print("\n--- Concentración absoluta vs. relativa, por rubro ---\n")
    with pd.option_context("display.width", 140):
        print(comp.to_string(index=False))
    n_distinto = (~comp["mismo_signo"]).sum()
    print(f"\nRubros donde cambia el signo entre absoluta y relativa: {n_distinto} de {len(comp)}")
    print(f"Guardado: {out_path2}")

    return comp


def main():
    uni = pd.read_csv(IN_PATH)
    sensibilidad_2016(uni)
    concentracion_relativa(uni)


if __name__ == "__main__":
    main()
