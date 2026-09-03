"""Tests de la corrección por comparaciones múltiples (FDR/Benjamini-Hochberg
y Bonferroni) sobre la familia de pruebas por rubro."""
import pandas as pd
import pytest

from analisis_comparaciones_multiples import corregir, ALPHA


def _familia_ejemplo():
    """5 rubros: 2 muy significativos, 1 significativo solo sin ajustar,
    2 claramente no significativos — para poder verificar el comportamiento
    de cada corrección con un caso construido a mano."""
    return pd.DataFrame({
        "rubro": ["MUY_SIG_1", "MUY_SIG_2", "MARGINAL", "NO_SIG_1", "NO_SIG_2"],
        "n_comunas": [300, 300, 300, 300, 300],
        "spearman_r": [0.6, 0.5, 0.15, 0.02, -0.01],
        "p_valor": [1e-20, 1e-15, 0.03, 0.6, 0.9],
    })


def test_corregir_conserva_columnas_originales():
    out = corregir(_familia_ejemplo())
    assert "spearman_r" in out.columns
    assert "n_comunas" in out.columns


def test_corregir_agrega_las_columnas_requeridas():
    out = corregir(_familia_ejemplo())
    esperadas = {
        "p_valor_original", "p_ajustado_fdr", "p_ajustado_bonferroni",
        "significativo_original", "significativo_fdr", "significativo_bonferroni",
        "cambia_conclusion_fdr", "cambia_conclusion_bonferroni",
    }
    assert esperadas <= set(out.columns)


def test_bonferroni_es_mas_conservador_que_fdr():
    out = corregir(_familia_ejemplo())
    # Bonferroni multiplica por n (más severo) -> p_ajustado_bonferroni >= p_ajustado_fdr siempre
    assert (out["p_ajustado_bonferroni"] >= out["p_ajustado_fdr"] - 1e-12).all()


def test_bonferroni_nunca_supera_uno():
    out = corregir(_familia_ejemplo())
    assert (out["p_ajustado_bonferroni"] <= 1.0).all()


def test_significancia_original_usa_alpha_005():
    fila = pd.DataFrame({"rubro": ["X"], "n_comunas": [100], "spearman_r": [0.1], "p_valor": [0.049]})
    out = corregir(fila)
    assert bool(out.iloc[0]["significativo_original"]) is True
    fila2 = pd.DataFrame({"rubro": ["X"], "n_comunas": [100], "spearman_r": [0.1], "p_valor": [0.051]})
    out2 = corregir(fila2)
    assert bool(out2.iloc[0]["significativo_original"]) is False


def test_rubro_muy_significativo_sobrevive_ambas_correcciones():
    out = corregir(_familia_ejemplo())
    fila = out[out["rubro"] == "MUY_SIG_1"].iloc[0]
    assert fila["significativo_original"]
    assert fila["significativo_fdr"]
    assert fila["significativo_bonferroni"]
    assert not fila["cambia_conclusion_fdr"]
    assert not fila["cambia_conclusion_bonferroni"]


def test_rubro_no_significativo_se_mantiene_no_significativo():
    out = corregir(_familia_ejemplo())
    fila = out[out["rubro"] == "NO_SIG_2"].iloc[0]
    assert not fila["significativo_original"]
    assert not fila["significativo_fdr"]
    assert not fila["significativo_bonferroni"]
    assert not fila["cambia_conclusion_fdr"]
    assert not fila["cambia_conclusion_bonferroni"]


def test_rubro_marginal_puede_cambiar_de_conclusion_con_correccion():
    # p=0.03 es significativo sin ajustar (< 0.05), pero con 5 pruebas
    # Bonferroni exige p < 0.01 -> debería dejar de ser significativo
    out = corregir(_familia_ejemplo())
    fila = out[out["rubro"] == "MARGINAL"].iloc[0]
    assert fila["significativo_original"]
    assert not fila["significativo_bonferroni"]
    assert fila["cambia_conclusion_bonferroni"]


def test_clasificacion_cambia_conclusion_es_una_comparacion_booleana_correcta():
    out = corregir(_familia_ejemplo())
    esperado = out["significativo_original"] != out["significativo_fdr"]
    assert (out["cambia_conclusion_fdr"] == esperado).all()


def test_alpha_por_defecto_es_005():
    assert ALPHA == 0.05
