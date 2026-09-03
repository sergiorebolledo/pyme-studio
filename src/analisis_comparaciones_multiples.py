"""
PYME Studio — Corrección por comparaciones múltiples (familia principal, 19 rubros).

No modifica pyme_studio_correlacion_por_rubro.csv ni sus conclusiones citadas
en el análisis original — lee ese archivo y genera uno NUEVO, enriquecido, con
las columnas de significancia ajustada.

Por qué hace falta: analisis_hito4.py prueba 19 hipótesis independientes (una
correlación de Spearman por rubro). Evaluar cada una contra alpha=0.05 sin
ajustar infla la probabilidad de declarar "significativo" algo que en
realidad es ruido, solo por el número de pruebas realizadas. Esta corrección
responde: ¿cuáles de las 19 conclusiones siguen siendo significativas si se
tiene en cuenta que se hicieron 19 pruebas a la vez?

Métodos:
  - Benjamini-Hochberg / FDR (principal): controla la tasa esperada de falsos
    descubrimientos entre los rubros declarados significativos — el estándar
    para análisis exploratorios con muchas pruebas relacionadas.
  - Bonferroni (contraste conservador): controla la probabilidad de al menos
    un falso positivo en toda la familia — más estricto, para ver el caso
    "peor escenario".

Esta corrección se aplica SOLO a la familia principal (19 rubros, un p-valor
cada uno, misma pregunta: ¿concentración~cierre en ese rubro?). No se mezcla
con la sensibilidad a 2016 ni con la comparación absoluta/relativa, que son
preguntas metodológicas distintas (ver docs/metodologia/metodologia.md) — y
cada subperíodo en analisis_subperiodos.py forma su propia familia de 19,
corregida por separado.

Requiere: pandas, scipy
Uso: python analisis_comparaciones_multiples.py
"""
from pathlib import Path

import pandas as pd
from scipy.stats import false_discovery_control

OUT_DIR = Path(__file__).resolve().parent.parent / "outputs"
IN_PATH = OUT_DIR / "pyme_studio_correlacion_por_rubro.csv"
OUT_PATH = OUT_DIR / "pyme_studio_correlacion_por_rubro_ajustada.csv"

ALPHA = 0.05


def corregir(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out = out.rename(columns={"p_valor": "p_valor_original"})

    n = len(out)
    out["p_ajustado_fdr"] = false_discovery_control(out["p_valor_original"], method="bh")
    out["p_ajustado_bonferroni"] = (out["p_valor_original"] * n).clip(upper=1.0)

    out["significativo_original"] = out["p_valor_original"] < ALPHA
    out["significativo_fdr"] = out["p_ajustado_fdr"] < ALPHA
    out["significativo_bonferroni"] = out["p_ajustado_bonferroni"] < ALPHA

    out["cambia_conclusion_fdr"] = out["significativo_original"] != out["significativo_fdr"]
    out["cambia_conclusion_bonferroni"] = out["significativo_original"] != out["significativo_bonferroni"]

    return out.sort_values("spearman_r", ascending=False)


def main():
    df = pd.read_csv(IN_PATH)
    out = corregir(df)
    out.to_csv(OUT_PATH, index=False, encoding="utf-8")

    print(f"=== Corrección por comparaciones múltiples (familia de {len(out)} rubros, alpha={ALPHA}) ===\n")
    cols = ["rubro", "n_comunas", "spearman_r", "p_valor_original", "p_ajustado_fdr", "p_ajustado_bonferroni",
            "significativo_original", "significativo_fdr", "significativo_bonferroni"]
    with pd.option_context("display.width", 160):
        print(out[cols].to_string(index=False))

    n_orig = int(out["significativo_original"].sum())
    n_fdr = int(out["significativo_fdr"].sum())
    n_bonf = int(out["significativo_bonferroni"].sum())
    cambia_fdr = out[out["cambia_conclusion_fdr"]]["rubro"].tolist()
    cambia_bonf = out[out["cambia_conclusion_bonferroni"]]["rubro"].tolist()

    print(f"\nSignificativos sin ajustar:  {n_orig} de {len(out)}")
    print(f"Significativos con FDR:      {n_fdr} de {len(out)}")
    print(f"Significativos con Bonferroni: {n_bonf} de {len(out)}")
    print(f"\nRubros que cambian de conclusión con FDR ({len(cambia_fdr)}): {cambia_fdr}")
    print(f"Rubros que cambian de conclusión con Bonferroni ({len(cambia_bonf)}): {cambia_bonf}")
    print(f"\nGuardado: {OUT_PATH}")
    print("(pyme_studio_correlacion_por_rubro.csv NO se modifica — ver docs/metodologia/metodologia.md)")


if __name__ == "__main__":
    main()
