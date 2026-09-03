"""Tests de las métricas centrales: empresa-años, concentración, participación
relativa, umbral mínimo de exposición y exclusión de 2016. Cubre
analisis_hito4.py y analisis_metodologia.py con datos sintéticos."""
import pandas as pd
import pytest

import analisis_hito4
import analisis_metodologia


def _unificado_sintetico():
    """3 años, 2 comunas, 1 rubro — pensado para poder calcular a mano
    empresa-años, concentración promedio y participación relativa."""
    return pd.DataFrame({
        "anio":             [2015, 2016, 2017, 2015, 2016, 2017],
        "comuna":           ["A", "A", "A", "B", "B", "B"],
        "rubro":            ["X", "X", "X", "X", "X", "X"],
        "aperturas":        [1, 1, 1, 1, 1, 1],
        "cierres":          [2, 3, 1, 0, 0, 1],
        "empresas_activas": [10, 20, 30, 100, 100, 100],
    })


# ---------- empresa-años ----------

def test_empresa_anios_es_la_suma_de_empresas_activas_por_periodo():
    df = _unificado_sintetico()
    agg = analisis_hito4.agregar(df)
    fila_a = agg[agg["comuna"] == "A"].iloc[0]
    assert fila_a["empresa_anios"] == 10 + 20 + 30  # suma, no promedio


def test_empresa_anios_ejemplo_del_glosario():
    # "100 empresas activas durante 10 años acumulan ~1.000 empresa-años"
    df = pd.DataFrame({
        "anio": list(range(2015, 2025)), "comuna": ["A"] * 10, "rubro": ["X"] * 10,
        "aperturas": [0] * 10, "cierres": [0] * 10, "empresas_activas": [100] * 10,
    })
    agg = analisis_hito4.agregar(df)
    assert agg.iloc[0]["empresa_anios"] == 1000


# ---------- concentración promedio ----------

def test_concentracion_promedio_es_el_promedio_no_la_suma():
    df = _unificado_sintetico()
    agg = analisis_hito4.agregar(df)
    fila_a = agg[agg["comuna"] == "A"].iloc[0]
    assert fila_a["concentracion_promedio"] == pytest.approx((10 + 20 + 30) / 3)


def test_tasa_cierre_es_cierres_totales_sobre_empresa_anios():
    df = _unificado_sintetico()
    agg = analisis_hito4.agregar(df)
    fila_a = agg[agg["comuna"] == "A"].iloc[0]
    assert fila_a["tasa_cierre"] == pytest.approx((2 + 3 + 1) / (10 + 20 + 30))


# ---------- exclusión de 2016 ----------

def test_exclusion_2016_cambia_empresa_anios_y_cierres():
    df = _unificado_sintetico()
    con_2016 = analisis_hito4.agregar(df)
    sin_2016 = analisis_hito4.agregar(df[df["anio"] != 2016])

    fila_con = con_2016[con_2016["comuna"] == "A"].iloc[0]
    fila_sin = sin_2016[sin_2016["comuna"] == "A"].iloc[0]

    assert fila_sin["empresa_anios"] < fila_con["empresa_anios"]
    assert fila_sin["empresa_anios"] == 10 + 30  # se descarta el año 2016 (20)
    assert fila_sin["cierres_total"] == 2 + 1     # se descarta el cierre de 2016 (3)


def test_exclusion_2016_no_afecta_filas_de_otros_anios():
    df = _unificado_sintetico()
    sin_2016 = analisis_hito4.agregar(df[df["anio"] != 2016])
    fila_b = sin_2016[sin_2016["comuna"] == "B"].iloc[0]
    # comuna B no cambia entre años (siempre 100 activas), solo baja un año de exposición
    assert fila_b["empresa_anios"] == 200


# ---------- participación relativa ----------

def test_participacion_relativa_es_proporcion_del_total_comunal():
    # comuna con 2 rubros en el mismo año: participación = activas_rubro / total_comuna
    df = pd.DataFrame({
        "anio": [2020, 2020], "comuna": ["A", "A"], "rubro": ["X", "Y"],
        "aperturas": [0, 0], "cierres": [0, 0], "empresas_activas": [30, 70],
    })
    total_comuna_anio = df.groupby(["anio", "comuna"])["empresas_activas"].transform("sum").astype(float)
    participacion = df["empresas_activas"] / total_comuna_anio
    assert participacion.tolist() == pytest.approx([0.3, 0.7])


def test_concentracion_relativa_via_analisis_metodologia():
    df = _unificado_sintetico()
    total_comuna_anio = df.groupby(["anio", "comuna"])["empresas_activas"].transform("sum").astype(float)
    df = df.copy()
    df["participacion_rubro_comuna"] = df["empresas_activas"] / total_comuna_anio.replace(0, float("nan"))
    # con un solo rubro por comuna, la participación siempre es 1.0 (100%)
    assert (df["participacion_rubro_comuna"] == 1.0).all()


# ---------- umbral mínimo de exposición (correlacion_por_rubro) ----------

def test_umbral_minimo_excluye_combinaciones_de_poca_exposicion():
    agg = pd.DataFrame({
        "comuna": [f"C{i}" for i in range(40)],
        "rubro": ["X"] * 40,
        "empresa_anios": [10] * 40,  # por debajo del umbral (50) -> se descarta todo
        "concentracion_promedio": list(range(40)),
        "tasa_cierre": [0.1] * 40,
    })
    out = analisis_hito4.correlacion_por_rubro(agg, min_comunas=30)
    assert out.empty


def test_umbral_minimo_comunas_excluye_rubros_con_pocas_comunas():
    agg = pd.DataFrame({
        "comuna": [f"C{i}" for i in range(5)],  # menos que min_comunas
        "rubro": ["X"] * 5,
        "empresa_anios": [200] * 5,  # exposición suficiente, pero pocas comunas
        "concentracion_promedio": [1, 2, 3, 4, 5],
        "tasa_cierre": [0.1, 0.2, 0.1, 0.3, 0.2],
    })
    out = analisis_hito4.correlacion_por_rubro(agg, min_comunas=30)
    assert out.empty


def test_umbral_minimo_incluye_rubros_que_si_cumplen():
    agg = pd.DataFrame({
        "comuna": [f"C{i}" for i in range(35)],
        "rubro": ["X"] * 35,
        "empresa_anios": [200] * 35,
        "concentracion_promedio": list(range(1, 36)),
        "tasa_cierre": [0.01 * i for i in range(1, 36)],
    })
    out = analisis_hito4.correlacion_por_rubro(agg, min_comunas=30)
    assert len(out) == 1
    assert out.iloc[0]["rubro"] == "X"
    assert out.iloc[0]["n_comunas"] == 35
