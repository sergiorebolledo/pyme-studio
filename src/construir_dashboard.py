"""
PYME Studio — construye dashboard/pyme_studio_dashboard.html, con mapa de Chile.

Incrusta los datos agregados (correlación, sensibilidad a 2016, concentración
absoluta vs. relativa, alcance del universo pyme) y la geometría de comunas
(geo_comunas.json, generado por preparar_geo_comunas.py) para dibujar un mapa
coroplético por comuna en el dashboard.

Requiere: pandas
Uso: python construir_dashboard.py
"""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "outputs"
TEMPLATE_PATH = ROOT / "dashboard" / "pyme_studio_dashboard.html"
DATA_JSON_PATH = OUT_DIR / "dashboard_data.json"
GEO_JSON_PATH = OUT_DIR / "geo_comunas.json"

# Nombres que difieren entre la geometría (chilemapas) y las estadísticas del SII.
# clave = nombre normalizado en la geometría · valor = nombre normalizado en el SII
ALIAS_GEO_A_SII = {
    "CALERA": "LA CALERA",
    "MARCHIHUE": "MARCHIGUE",
    "OHIGGINS": "O'HIGGINS",
    "PAIGUANO": "PAIHUANO",
    "TILTIL": "TITIL",
    "TREGUACO": "TREHUACO",
}


def construir_dashboard_data():
    """Igual que construir_dashboard.py, más los resultados del endurecimiento
    metodológico (Tareas 1, 4, 5 — ver 12_Metodologia_y_Limitaciones.md):
    participación relativa, sensibilidad a 2016 y alcance del universo pyme.
    Requiere haber corrido antes analisis_metodologia.py y
    analisis_tamano_empresas.py."""
    MIN_EMPRESA_ANIOS = 50
    agg = pd.read_csv(OUT_DIR / "pyme_studio_agregado_comuna_rubro.csv")
    agg = agg[agg["empresa_anios"] >= MIN_EMPRESA_ANIOS].copy()
    agg["concentracion_promedio"] = agg["concentracion_promedio"].round(1)
    agg["tasa_cierre"] = agg["tasa_cierre"].round(4)

    enriquecido_path = OUT_DIR / "pyme_studio_agregado_comuna_rubro_enriquecido.csv"
    if enriquecido_path.exists():
        enr = pd.read_csv(enriquecido_path)[["comuna", "rubro", "participacion_promedio"]]
        agg = agg.merge(enr, on=["comuna", "rubro"], how="left")
        agg["participacion_promedio"] = (agg["participacion_promedio"] * 100).round(3)
    else:
        agg["participacion_promedio"] = None

    rubros = sorted(agg["rubro"].unique().tolist())
    rubro_idx = {r: i for i, r in enumerate(rubros)}

    registros = [
        [row["comuna"], rubro_idx[row["rubro"]], int(row["aperturas_total"]), int(row["cierres_total"]),
         int(row["empresa_anios"]), row["concentracion_promedio"], row["tasa_cierre"],
         (None if pd.isna(row["participacion_promedio"]) else row["participacion_promedio"])]
        for _, row in agg.iterrows()
    ]

    corr = pd.read_csv(OUT_DIR / "pyme_studio_correlacion_por_rubro.csv")
    correlacion_por_rubro = {
        row["rubro"]: {"n_comunas": int(row["n_comunas"]), "r": round(row["spearman_r"], 4), "p": row["p_valor"]}
        for _, row in corr.iterrows()
    }

    sens_path = OUT_DIR / "pyme_studio_sensibilidad_2016.csv"
    if sens_path.exists():
        sens = pd.read_csv(sens_path)
        for _, row in sens.iterrows():
            if row["rubro"] in correlacion_por_rubro:
                correlacion_por_rubro[row["rubro"]]["r_sin_2016"] = round(row["spearman_r_sin_2016"], 4)
                correlacion_por_rubro[row["rubro"]]["p_sin_2016"] = row["p_valor_sin_2016"]
                correlacion_por_rubro[row["rubro"]]["cambia_conclusion_2016"] = bool(row["cambia_conclusion"])

    rel_path = OUT_DIR / "pyme_studio_concentracion_absoluta_vs_relativa.csv"
    if rel_path.exists():
        rel = pd.read_csv(rel_path)
        for _, row in rel.iterrows():
            if row["rubro"] in correlacion_por_rubro:
                correlacion_por_rubro[row["rubro"]]["r_relativa"] = round(row["r_relativa"], 4)
                correlacion_por_rubro[row["rubro"]]["p_relativa"] = row["p_relativa"]
                correlacion_por_rubro[row["rubro"]]["mismo_signo_relativa"] = bool(row["mismo_signo"])

    ajustada_path = OUT_DIR / "pyme_studio_correlacion_por_rubro_ajustada.csv"
    if ajustada_path.exists():
        ajustada = pd.read_csv(ajustada_path)
        for _, row in ajustada.iterrows():
            if row["rubro"] in correlacion_por_rubro:
                correlacion_por_rubro[row["rubro"]]["p_ajustado_fdr"] = row["p_ajustado_fdr"]
                correlacion_por_rubro[row["rubro"]]["significativo_fdr"] = bool(row["significativo_fdr"])
                correlacion_por_rubro[row["rubro"]]["significativo_bonferroni"] = bool(row["significativo_bonferroni"])

    uni = pd.read_csv(OUT_DIR / "pyme_studio_unificado.csv")
    serie_anual = uni.groupby("anio")[["aperturas", "cierres"]].sum().reset_index().values.tolist()

    alcance_path = OUT_DIR / "pyme_studio_alcance_pyme_por_rubro.csv"
    metodologia = {
        "periodo_min": int(uni["anio"].min()),
        "periodo_max": int(uni["anio"].max()),
        "n_comunas_muestra": int(agg["comuna"].nunique()),
        "empresa_anios_totales": int(agg["empresa_anios"].sum()),
        "umbral_min_empresa_anios": MIN_EMPRESA_ANIOS,
        "n_combinaciones": len(registros),
    }
    if alcance_path.exists():
        alc = pd.read_csv(alcance_path)
        metodologia["pct_pyme_minimo"] = round(float(alc["pct_pyme_ventas_oficial"].min()), 2)
        foco = alc[alc["rubro"].str.contains("COMERCIO AL POR MAYOR|ALOJAMIENTO", regex=True)]
        metodologia["pct_pyme_por_rubro_foco"] = {
            row["rubro"]: round(float(row["pct_pyme_ventas_oficial"]), 2) for _, row in foco.iterrows()
        }

    return {
        "rubros": rubros, "registros": registros, "correlacion_por_rubro": correlacion_por_rubro,
        "serie_anual": serie_anual, "metodologia": metodologia,
    }


def construir_geo_con_alias():
    geo = json.loads(GEO_JSON_PATH.read_text(encoding="utf-8"))
    for c in geo["comunas"]:
        c["comuna_sii"] = ALIAS_GEO_A_SII.get(c["comuna_norm"], c["comuna_norm"])
    return geo


def inyectar(html: str, marcador: str, data: dict) -> str:
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    if marcador in html:
        return html.replace(marcador, payload)
    # Ya inyectado antes: reemplaza el bloque existente por su id.
    tag_id = {"__DATA_JSON__": "dashboard-data", "__GEO_JSON__": "geo-data"}[marcador]
    start_tag = f'<script id="{tag_id}" type="application/json">'
    inicio = html.index(start_tag) + len(start_tag)
    fin = html.index("</script>", inicio)
    return html[:inicio] + "\n" + payload + "\n" + html[fin:]


def main():
    dash_data = construir_dashboard_data()
    DATA_JSON_PATH.write_text(json.dumps(dash_data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Datos rubro/comuna: {len(dash_data['registros']):,} filas")

    geo_data = construir_geo_con_alias()
    print(f"Geometría: {len(geo_data['comunas'])} comunas")

    html = TEMPLATE_PATH.read_text(encoding="utf-8")
    html = inyectar(html, "__DATA_JSON__", dash_data)
    html = inyectar(html, "__GEO_JSON__", geo_data)
    TEMPLATE_PATH.write_text(html, encoding="utf-8")
    print(f"dashboard/pyme_studio_dashboard.html actualizado ({len(html)/1024:.0f} KB)")


if __name__ == "__main__":
    main()
