"""Tests de los chequeos puros de validar_calidad.py (reciben un DataFrame
y una lista de resultados, sin tocar disco)."""
import pandas as pd

from validar_calidad import (
    revisar_columnas,
    revisar_periodo,
    revisar_valores_imposibles,
    revisar_cardinalidad,
    revisar_duplicados,
    COLUMNAS_ESPERADAS,
)


def _df_valido():
    return pd.DataFrame({
        "anio": [2020, 2021], "comuna": ["A", "B"], "rubro": ["X", "X"],
        "aperturas": [1, 2], "cierres": [0, 1], "empresas_activas": [10, 20],
        "tasa_cierre": [0.0, 0.05],
    })


def _ultimo(resultados):
    return resultados[-1]


def test_revisar_columnas_ok_cuando_estan_todas():
    resultados = []
    revisar_columnas(_df_valido(), resultados)
    assert _ultimo(resultados)["ok"] is True
    assert _ultimo(resultados)["bloqueante"] is False


def test_revisar_columnas_detecta_columna_faltante():
    df = _df_valido().drop(columns=["tasa_cierre"])
    resultados = []
    revisar_columnas(df, resultados)
    r = _ultimo(resultados)
    assert r["ok"] is False
    assert r["bloqueante"] is True
    assert "tasa_cierre" in r["detalle"]


def test_revisar_periodo_detecta_anios_faltantes():
    df = pd.DataFrame({"anio": [2005, 2006, 2008]})  # falta 2007 dentro del rango esperado
    resultados = []
    revisar_periodo(df, resultados)
    r = _ultimo(resultados)
    assert r["ok"] is False
    assert r["bloqueante"] is True


def test_revisar_valores_imposibles_detecta_negativos():
    df = _df_valido().copy()
    df.loc[0, "cierres"] = -5
    resultados = []
    revisar_valores_imposibles(df, resultados)
    negativos = [r for r in resultados if "negativos" in r["chequeo"]][0]
    assert negativos["ok"] is False
    assert negativos["bloqueante"] is True


def test_revisar_valores_imposibles_tasa_cierre_sobre_100_no_es_bloqueante():
    df = _df_valido().copy()
    df["tasa_cierre"] = [1.5, 0.05]  # una fila > 100%, ya documentado como esperable
    resultados = []
    revisar_valores_imposibles(df, resultados)
    sobre_uno = [r for r in resultados if "> 100%" in r["chequeo"]][0]
    assert sobre_uno["bloqueante"] is False


def test_revisar_cardinalidad_detecta_fuera_de_rango():
    df = pd.DataFrame({"comuna": ["A"] * 5, "rubro": ["X"] * 5})  # muy pocas comunas y rubros
    resultados = []
    revisar_cardinalidad(df, resultados)
    comunas_check = [r for r in resultados if "comunas" in r["chequeo"]][0]
    assert comunas_check["ok"] is False
    assert comunas_check["bloqueante"] is False  # es una advertencia, no bloqueante


def test_revisar_duplicados_detecta_filas_repetidas():
    df = pd.DataFrame({
        "anio": [2020, 2020], "comuna": ["A", "A"], "rubro": ["X", "X"],
    })
    resultados = []
    revisar_duplicados(df, resultados)
    r = _ultimo(resultados)
    assert r["ok"] is False
    assert r["bloqueante"] is True
    assert "1 filas duplicadas" in r["detalle"]


def test_revisar_duplicados_sin_duplicados_pasa():
    df = pd.DataFrame({
        "anio": [2020, 2020], "comuna": ["A", "B"], "rubro": ["X", "X"],
    })
    resultados = []
    revisar_duplicados(df, resultados)
    r = _ultimo(resultados)
    assert r["ok"] is True
    assert r["bloqueante"] is False


def test_columnas_esperadas_coincide_con_el_formato_del_pipeline():
    # Ancla el contrato entre pipeline.py y validar_calidad.py: si alguien
    # renombra una columna en un lado sin actualizar el otro, este test lo detecta.
    assert COLUMNAS_ESPERADAS == [
        "anio", "comuna", "rubro", "aperturas", "cierres", "empresas_activas", "tasa_cierre",
    ]
