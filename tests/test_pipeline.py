"""Tests de src/pipeline.py — funciones puras, sin tocar disco ni descargar datos."""
import math

import pandas as pd
import pytest

from pipeline import (
    parsear_recuento,
    normalizar_rubro,
    limpiar_cierres,
    limpiar_aperturas,
    limpiar_empresas_activas,
    combinar_fuentes,
)


# ---------- parsear_recuento (separador de miles chileno) ----------

def test_parsear_recuento_separador_miles_chileno():
    serie = pd.Series(["1.400", "27", "1.234.567"])
    resultado = parsear_recuento(serie)
    assert resultado.tolist() == [1400, 27, 1234567]


def test_parsear_recuento_no_es_decimal():
    # "1.400" es mil cuatrocientos, NO uno coma cuatro (formato chileno, no anglosajón)
    assert parsear_recuento(pd.Series(["1.400"])).iloc[0] == 1400


# ---------- normalizar_rubro ----------

def test_normalizar_rubro_quita_codigo_de_letra():
    assert normalizar_rubro("A - Agricultura, ganadería, silvicultura y pesca") == "AGRICULTURA, GANADERIA, SILVICULTURA Y PESCA"


def test_normalizar_rubro_quita_tildes_y_mayuscula():
    assert normalizar_rubro("Información y Comunicaciones") == "INFORMACION Y COMUNICACIONES"


def test_normalizar_rubro_ya_normalizado_es_idempotente():
    valor = "AGRICULTURA, GANADERIA, SILVICULTURA Y PESCA"
    assert normalizar_rubro(valor) == valor


def test_normalizar_rubro_dos_formatos_distintos_dan_la_misma_clave():
    a = normalizar_rubro("A - Agricultura, ganadería, silvicultura y pesca")
    b = normalizar_rubro("AGRICULTURA, GANADERIA, SILVICULTURA Y PESCA")
    assert a == b


# ---------- limpiar_cierres: filas vacías, categorías residuales ----------

def _df_cierres_crudo():
    return pd.DataFrame({
        "Año comercial": ["2020", "2020", None, "2021"],
        "Comuna": ["Santiago", "Santiago", None, "Providencia"],
        "Rubro": ["A - Agricultura", "Valor por Defecto", None, "A - Agricultura"],
        "Recuento": ["1.400", "50", None, "27"],
    })


def test_limpiar_cierres_descarta_filas_completamente_vacias():
    out = limpiar_cierres(_df_cierres_crudo())
    # la fila con Año comercial=None debe desaparecer
    assert out["anio"].isna().sum() == 0
    assert len(out) <= 2


def test_limpiar_cierres_descarta_categoria_residual_valor_por_defecto():
    out = limpiar_cierres(_df_cierres_crudo())
    assert "VALOR POR DEFECTO" not in out["rubro"].tolist()


def test_limpiar_cierres_agrupa_por_anio_comuna_rubro():
    df = pd.DataFrame({
        "Año comercial": ["2020", "2020"],
        "Comuna": ["Santiago", "Santiago"],
        "Rubro": ["A - Agricultura", "A - Agricultura"],
        "Recuento": ["1.000", "400"],
    })
    out = limpiar_cierres(df)
    assert len(out) == 1
    assert out.iloc[0]["cierres"] == 1400


# ---------- limpiar_aperturas: categorías residuales ----------

def test_limpiar_aperturas_descarta_categoria_residual():
    df = pd.DataFrame({
        "Año comercial": ["2020", "2020"],
        "Comuna": ["Santiago", "Santiago"],
        "RUBRO": ["A - Agricultura", "Valor por Defecto"],
        "Recuento": ["100", "5"],
    })
    out = limpiar_aperturas(df)
    assert len(out) == 1
    assert out.iloc[0]["aperturas"] == 100


# ---------- limpiar_empresas_activas: "Sin información", None -> 0 ----------

def test_limpiar_empresas_activas_descarta_sin_informacion():
    filas = [
        (2020, "Santiago", "A - Agricultura", 10),
        (2020, "Sin Información", "A - Agricultura", 5),
        (2020, "Santiago", "Sin información", 3),
    ]
    out = limpiar_empresas_activas(filas)
    assert len(out) == 1
    assert out.iloc[0]["empresas_activas"] == 10


def test_limpiar_empresas_activas_none_se_trata_como_cero():
    filas = [(2020, "Santiago", "A - Agricultura", None)]
    out = limpiar_empresas_activas(filas)
    assert out.iloc[0]["empresas_activas"] == 0


def test_limpiar_empresas_activas_descarta_filas_con_campos_clave_ausentes():
    filas = [
        (None, "Santiago", "A - Agricultura", 10),
        (2020, None, "A - Agricultura", 10),
        (2020, "Santiago", None, 10),
        (2020, "Santiago", "A - Agricultura", 10),
    ]
    out = limpiar_empresas_activas(filas)
    assert len(out) == 1


# ---------- combinar_fuentes: outer join, ausencias=0, tasa, división por cero ----------

def _fuentes_ejemplo():
    aperturas = pd.DataFrame({
        "anio": [2020, 2020], "comuna": ["A", "B"], "rubro": ["X", "X"], "aperturas": [5, 3],
    })
    cierres = pd.DataFrame({
        "anio": [2020], "comuna": ["A"], "rubro": ["X"], "cierres": [2],
    })
    activas = pd.DataFrame({
        "anio": [2020, 2020], "comuna": ["A", "B"], "rubro": ["X", "X"], "empresas_activas": [10, 0],
    })
    return aperturas, cierres, activas


def test_combinar_fuentes_ausencia_en_una_fuente_se_trata_como_cero():
    aperturas, cierres, activas = _fuentes_ejemplo()
    out = combinar_fuentes(aperturas, cierres, activas)
    fila_b = out[out["comuna"] == "B"].iloc[0]
    # comuna B no aparece en `cierres` -> outer join + fillna(0)
    assert fila_b["cierres"] == 0


def test_combinar_fuentes_tasa_cierre_con_denominador_valido():
    aperturas, cierres, activas = _fuentes_ejemplo()
    out = combinar_fuentes(aperturas, cierres, activas)
    fila_a = out[out["comuna"] == "A"].iloc[0]
    assert fila_a["tasa_cierre"] == pytest.approx(2 / 10)


def test_combinar_fuentes_division_por_cero_da_nan_no_error():
    aperturas, cierres, activas = _fuentes_ejemplo()
    out = combinar_fuentes(aperturas, cierres, activas)
    fila_b = out[out["comuna"] == "B"].iloc[0]
    # empresas_activas=0 en comuna B -> tasa_cierre debe ser NaN, no 0 ni error
    assert math.isnan(fila_b["tasa_cierre"])


def test_combinar_fuentes_no_fuerza_nan_a_cero():
    # el comportamiento documentado es preservar NaN cuando el denominador es 0,
    # no rellenarlo con 0 (que confundiría "sin empresas" con "0% de cierre")
    aperturas, cierres, activas = _fuentes_ejemplo()
    out = combinar_fuentes(aperturas, cierres, activas)
    assert out["tasa_cierre"].isna().sum() == 1


def test_combinar_fuentes_agrupa_por_anio_comuna_rubro():
    aperturas, cierres, activas = _fuentes_ejemplo()
    out = combinar_fuentes(aperturas, cierres, activas)
    assert set(out.columns) >= {"anio", "comuna", "rubro", "aperturas", "cierres", "empresas_activas", "tasa_cierre"}
    assert len(out) == 2  # comuna A y comuna B, cada una una fila
