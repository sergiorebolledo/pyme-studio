"""
PYME Studio — Prepara la geometría de comunas para el mapa del dashboard v2.

Fuente: chilemapas (pachadotdev/chilemapas, GitHub, licencia Apache 2.0) —
ver data/README.md para instrucciones de descarga. Se espera encontrar los
16 archivos regionales + codigos_territoriales.csv en data/reference/geo_raw/
(codigos_territoriales.csv ya viene incluido en el repositorio; los 16
GeoJSON regionales hay que descargarlos aparte, no están versionados aquí
por su tamaño — ver data/README.md).

Pasos:
  1. Lee los 16 GeoJSON regionales + la tabla de códigos → nombre de comuna.
  2. Simplifica cada polígono con Shapely (tolerancia adaptativa: las regiones
     con costas muy complejas, ej. Aysén/Magallanes, necesitan más simplificación
     para no disparar el tamaño del archivo).
  3. Proyecta lon/lat a un plano simple (corrección por coseno de latitud, para
     no deformar Chile horizontalmente) y normaliza a un viewBox 0-1000 x 0-2200.
  4. Normaliza nombres de comuna (sin tildes, mayúsculas) para poder cruzarlos
     con pyme_studio_agregado_comuna_rubro.csv más adelante.
  5. Exporta geo_comunas.json: un polígono (o multipolígono) compacto por comuna.

Requiere: shapely
Uso: python preparar_geo_comunas.py
"""
import csv
import json
import math
import unicodedata
from pathlib import Path

from shapely.geometry import shape
from shapely.ops import transform

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RAW_DIR = ROOT / "data" / "reference" / "geo_raw"
OUT_PATH = ROOT / "outputs" / "geo_comunas.json"

# Tolerancia de simplificación (en grados) — regiones con costas muy recortadas
# (fiordos del sur) usan más tolerancia para no explotar el tamaño del archivo.
TOLERANCIA_POR_REGION = {
    "r10": 0.006, "r11": 0.012, "r12": 0.02, "r14": 0.006,
}
TOLERANCIA_DEFAULT = 0.003


def normalizar_comuna(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", str(texto)).encode("ascii", "ignore").decode("ascii")
    return texto.strip().upper()


def cargar_nombres() -> dict:
    nombres = {}
    with open(RAW_DIR / "codigos_territoriales.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            nombres[row["commune_id"]] = row["commune_name"]
    return nombres


def main():
    nombres = cargar_nombres()
    features_out = []
    lons, lats = [], []
    sin_nombre = 0

    for i in range(1, 17):
        key = f"r{i:02d}"
        path = RAW_DIR / f"{key}.geojson"
        data = json.loads(path.read_text(encoding="utf-8"))
        tol = TOLERANCIA_POR_REGION.get(key, TOLERANCIA_DEFAULT)

        for feat in data["features"]:
            codigo = feat["properties"]["codigo_comuna"]
            nombre = nombres.get(codigo)
            if not nombre:
                sin_nombre += 1
                continue
            geom = shape(feat["geometry"])
            geom = geom.simplify(tol, preserve_topology=True)
            if geom.is_empty:
                continue

            minx, miny, maxx, maxy = geom.bounds
            lons += [minx, maxx]
            lats += [miny, maxy]

            features_out.append({
                "codigo": codigo,
                "comuna": nombre,
                "comuna_norm": normalizar_comuna(nombre),
                "geom": geom,
            })

    print(f"Comunas procesadas: {len(features_out)} (sin nombre encontrado: {sin_nombre})")

    lon0, lon1 = min(lons), max(lons)
    lat0, lat1 = min(lats), max(lats)
    lat_mean_rad = math.radians((lat0 + lat1) / 2)
    cos_lat = math.cos(lat_mean_rad)

    def proyectar(lon, lat):
        return (lon * cos_lat, lat)

    xs, ys = [], []
    for f in features_out:
        g2 = transform(proyectar, f["geom"])
        f["geom_proj"] = g2
        b = g2.bounds
        xs += [b[0], b[2]]
        ys += [b[1], b[3]]

    x0, x1 = min(xs), max(xs)
    y0, y1 = min(ys), max(ys)
    w, h = x1 - x0, y1 - y0
    VIEW_H = 2200
    scale = VIEW_H / h
    VIEW_W = w * scale

    def a_svg_coords(x, y):
        sx = (x - x0) * scale
        sy = (y1 - y) * scale  # invertir Y (lat mayor = arriba)
        return round(sx, 1), round(sy, 1)

    def poly_a_rings(geom):
        polys = geom.geoms if geom.geom_type == "MultiPolygon" else [geom]
        rings = []
        for p in polys:
            ext = [a_svg_coords(x, y) for x, y in p.exterior.coords]
            rings.append(ext)
        return rings

    salida = []
    total_puntos = 0
    for f in features_out:
        rings = poly_a_rings(f["geom_proj"])
        total_puntos += sum(len(r) for r in rings)
        salida.append({
            "codigo": f["codigo"],
            "comuna": f["comuna"],
            "comuna_norm": f["comuna_norm"],
            "rings": rings,
        })

    resultado = {"viewW": round(VIEW_W, 1), "viewH": VIEW_H, "comunas": salida}
    OUT_PATH.write_text(json.dumps(resultado, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    size_kb = OUT_PATH.stat().st_size / 1024
    print(f"Total puntos: {total_puntos:,}")
    print(f"Guardado: {OUT_PATH} ({size_kb:.0f} KB)")


if __name__ == "__main__":
    main()
