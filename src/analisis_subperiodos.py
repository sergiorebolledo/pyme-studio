"""
PYME Studio — Estabilidad de la correlación concentración~cierre por subperíodo.

No modifica analisis_hito4.py ni sus salidas. Recalcula la correlación por
rubro (misma metodología: Spearman, 50+ empresa-años por combinación, 30+
comunas por rubro) dentro de 4 subperíodos más los 2 períodos completos ya
usados en el análisis original y en analisis_metodologia.py:

  - 2005-2010, 2011-2015, 2016-2019, 2020-2024  (subperíodos, ~4-5 años c/u)
  - 2005-2024                                    (completo, igual que analisis_hito4.py)
  - 2005-2024 excluyendo 2016                    (igual que analisis_metodologia.py)

Dentro de CADA período se aplica corrección FDR (Benjamini-Hochberg) a su
propia familia de pruebas por rubro — un período es una familia de hipótesis
distinta de otro, no se corrigen juntos.

Advertencia esperada: los subperíodos de 4-5 años tienen mucha menos muestra
(empresa-años) que el período completo de 20 años, así que sus estimaciones
son menos estables — se marca explícitamente cuándo un rubro+período no
alcanza el umbral mínimo de exposición o de comunas.

Requiere: pandas, scipy, matplotlib
Uso: python analisis_subperiodos.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
from scipy.stats import false_discovery_control

OUT_DIR = Path(__file__).resolve().parent.parent / "outputs"
FIG_DIR = OUT_DIR / "figures"
FIG_DIR.mkdir(exist_ok=True, parents=True)
IN_PATH = OUT_DIR / "pyme_studio_unificado.csv"
OUT_PATH = OUT_DIR / "pyme_studio_estabilidad_subperiodos.csv"

MIN_EMPRESA_ANIOS = 50
MIN_COMUNAS = 30
ALPHA = 0.05

PERIODOS = [
    ("2005-2010", 2005, 2010, None),
    ("2011-2015", 2011, 2015, None),
    ("2016-2019", 2016, 2019, None),
    ("2020-2024", 2020, 2024, None),
    ("2005-2024 (completo)", 2005, 2024, None),
    ("2005-2024 (sin 2016)", 2005, 2024, 2016),
]

# Rubros centrales del hallazgo — los únicos que se grafican, para no sobrecargar
# la visualización con las 19 series (la tabla completa queda en el CSV).
RUBROS_FOCO = [
    "COMERCIO AL POR MAYOR Y AL POR MENOR; REPARACION DE VEHICULOS AUTOMOTORES Y MOTOCICLETAS",
    "ACTIVIDADES DE ALOJAMIENTO Y DE SERVICIO DE COMIDAS",
    "AGRICULTURA, GANADERIA, SILVICULTURA Y PESCA",
]
COLOR_POR_RUBRO = {
    RUBROS_FOCO[0]: "#1F5C8B",
    RUBROS_FOCO[1]: "#2F8F5B",
    RUBROS_FOCO[2]: "#C2632A",
}
NOMBRE_CORTO = {
    RUBROS_FOCO[0]: "Comercio",
    RUBROS_FOCO[1]: "Alojamiento/Comidas",
    RUBROS_FOCO[2]: "Agricultura",
}


def agregar(df: pd.DataFrame) -> pd.DataFrame:
    agg = df.groupby(["comuna", "rubro"], as_index=False).agg(
        cierres_total=("cierres", "sum"),
        empresa_anios=("empresas_activas", "sum"),
        concentracion_promedio=("empresas_activas", "mean"),
    )
    agg["tasa_cierre"] = agg["cierres_total"] / agg["empresa_anios"]
    return agg


def correlacion_por_rubro(agg: pd.DataFrame) -> pd.DataFrame:
    resultados = []
    for rubro, grupo in agg[agg["empresa_anios"] >= MIN_EMPRESA_ANIOS].groupby("rubro"):
        muestra_insuficiente = len(grupo) < MIN_COMUNAS
        if len(grupo) < 3:  # scipy no puede correlacionar con <3 puntos
            continue
        r, p = stats.spearmanr(grupo["concentracion_promedio"], grupo["tasa_cierre"])
        # Con muestras chicas puede darse una entrada constante (ej. todas las
        # comunas con tasa_cierre=0 en un subperíodo corto) -> Spearman queda
        # indefinido (NaN). Es una correlación no calculable, no un error, así
        # que se marca como muestra insuficiente en vez de propagar el NaN.
        if pd.isna(r) or pd.isna(p):
            muestra_insuficiente = True
        resultados.append({
            "rubro": rubro, "n_comunas": len(grupo), "empresa_anios": int(grupo["empresa_anios"].sum()),
            "spearman_r": r, "p_valor_original": p, "muestra_insuficiente": muestra_insuficiente,
        })
    return pd.DataFrame(resultados)


def procesar_periodo(uni: pd.DataFrame, nombre: str, anio_ini: int, anio_fin: int, excluir_anio) -> pd.DataFrame:
    sub = uni[(uni["anio"] >= anio_ini) & (uni["anio"] <= anio_fin)]
    if excluir_anio is not None:
        sub = sub[sub["anio"] != excluir_anio]

    agg = agregar(sub)
    corr = correlacion_por_rubro(agg)
    if corr.empty:
        return corr

    # false_discovery_control no acepta NaN -> se corrige solo sobre los p-valores
    # calculables; las filas con correlación indefinida quedan con p_ajustado_fdr=NaN
    # y significativo=False (ya vienen marcadas muestra_insuficiente=True).
    corr["p_ajustado_fdr"] = float("nan")
    validos = corr["p_valor_original"].notna()
    if validos.any():
        corr.loc[validos, "p_ajustado_fdr"] = false_discovery_control(corr.loc[validos, "p_valor_original"], method="bh")
    corr["significativo"] = (corr["p_ajustado_fdr"] < ALPHA) & (~corr["muestra_insuficiente"])
    corr["periodo"] = nombre
    corr["anio_inicio"] = anio_ini
    corr["anio_fin"] = anio_fin if excluir_anio is None else f"{anio_fin} (excl. {excluir_anio})"
    corr["n_combinaciones"] = len(agg[agg["empresa_anios"] >= MIN_EMPRESA_ANIOS])
    return corr


def main():
    uni = pd.read_csv(IN_PATH)

    todos = []
    for nombre, ini, fin, excluir in PERIODOS:
        r = procesar_periodo(uni, nombre, ini, fin, excluir)
        todos.append(r)
        print(f"{nombre}: {len(r)} rubros con muestra evaluable")

    df = pd.concat(todos, ignore_index=True)

    # Comparar cada período contra el período completo (2005-2024).
    base = df[df["periodo"] == "2005-2024 (completo)"][["rubro", "spearman_r", "significativo"]]
    base = base.rename(columns={"spearman_r": "r_base", "significativo": "sig_base"})
    df = df.merge(base, on="rubro", how="left")
    df["cambia_signo_vs_completo"] = (df["spearman_r"] > 0) != (df["r_base"] > 0)
    df["cambia_significancia_vs_completo"] = df["significativo"] != df["sig_base"]

    cols = [
        "periodo", "anio_inicio", "anio_fin", "rubro", "n_comunas", "n_combinaciones", "empresa_anios",
        "spearman_r", "p_valor_original", "p_ajustado_fdr", "significativo",
        "cambia_signo_vs_completo", "cambia_significancia_vs_completo", "muestra_insuficiente",
    ]
    df = df[cols].sort_values(["periodo", "spearman_r"], ascending=[True, False])
    df.to_csv(OUT_PATH, index=False, encoding="utf-8")

    print(f"\nGuardado: {OUT_PATH}")

    # Resumen de los 3 rubros centrales por período.
    print("\n--- Rubros centrales, por período ---\n")
    foco = df[df["rubro"].isin(RUBROS_FOCO)].copy()
    foco["rubro_corto"] = foco["rubro"].map(NOMBRE_CORTO)
    with pd.option_context("display.width", 140):
        print(foco[["periodo", "rubro_corto", "n_comunas", "spearman_r", "p_ajustado_fdr", "significativo", "muestra_insuficiente"]].to_string(index=False))

    # Gráfico: solo los 3 rubros centrales, un punto por período — evita sobrecarga visual.
    plt.rcParams.update({
        "figure.facecolor": "#F6F8FA", "axes.facecolor": "#FFFFFF",
        "axes.edgecolor": "#D2DEE4", "text.color": "#16222B",
        "xtick.color": "#16222B", "ytick.color": "#16222B", "font.family": "sans-serif",
    })
    orden_periodos = [p[0] for p in PERIODOS]
    fig, ax = plt.subplots(figsize=(11, 6))
    for rubro in RUBROS_FOCO:
        serie = foco[foco["rubro"] == rubro].set_index("periodo").reindex(orden_periodos)
        marcador = ["o" if not ins else "x" for ins in serie["muestra_insuficiente"]]
        ax.plot(orden_periodos, serie["spearman_r"], marker="o", linewidth=2, color=COLOR_POR_RUBRO[rubro], label=NOMBRE_CORTO[rubro])
        for i, (x, y, ins) in enumerate(zip(orden_periodos, serie["spearman_r"], serie["muestra_insuficiente"])):
            if ins:
                ax.scatter([x], [y], s=90, facecolors="none", edgecolors=COLOR_POR_RUBRO[rubro], linewidths=1.5, zorder=5)
    ax.axhline(0, color="#16222B", linewidth=0.9)
    ax.set_ylabel("Correlación de Spearman (concentración vs. tasa de cierre)")
    ax.set_title("Estabilidad temporal — 3 rubros centrales por subperíodo\n(círculo hueco = muestra insuficiente, <30 comunas)", fontsize=11, fontweight="bold", loc="left")
    plt.xticks(rotation=20, ha="right")
    ax.legend(frameon=False, loc="best")
    ax.grid(axis="y", alpha=0.4)
    ax.set_axisbelow(True)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    plt.tight_layout()
    fig_path = FIG_DIR / "hito4_estabilidad_subperiodos.png"
    plt.savefig(fig_path, dpi=150)
    plt.close(fig)
    print(f"\nGráfico guardado: {fig_path}")


if __name__ == "__main__":
    main()
