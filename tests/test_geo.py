"""Tests de normalización y alias de comunas (mapa del dashboard)."""
from preparar_geo_comunas import normalizar_comuna
from construir_dashboard import ALIAS_GEO_A_SII


def test_normalizar_comuna_quita_tildes():
    assert normalizar_comuna("Ñuñoa") == "NUNOA"


def test_normalizar_comuna_mayuscula():
    assert normalizar_comuna("santiago") == "SANTIAGO"


def test_normalizar_comuna_quita_espacios_extra():
    assert normalizar_comuna("  Providencia  ") == "PROVIDENCIA"


def test_alias_geo_a_sii_contiene_los_casos_documentados():
    # Estos son los alias explícitamente documentados en 10/producto_dashboard.md
    # (nombres que difieren entre chilemapas y el SII) — si alguno se borra sin
    # querer, el mapa vuelve a mostrar esa comuna sin datos.
    assert ALIAS_GEO_A_SII.get("TILTIL") == "TITIL"
    assert ALIAS_GEO_A_SII.get("MARCHIHUE") == "MARCHIGUE"
    assert "OHIGGINS" in ALIAS_GEO_A_SII


def test_alias_geo_a_sii_valores_estan_normalizados():
    # los valores del alias deben estar en el mismo formato que produce
    # normalizar_comuna (mayúsculas, sin tildes), para que el cruce funcione
    for clave, valor in ALIAS_GEO_A_SII.items():
        assert clave == normalizar_comuna(clave)
        assert valor == normalizar_comuna(valor)
