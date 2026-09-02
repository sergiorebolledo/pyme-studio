# Datos — cómo conseguirlos

Los archivos originales del Servicio de Impuestos Internos (SII) de Chile **no vienen incluidos en este repositorio**. Revisamos los [términos de uso del sitio del SII](https://www.sii.cl/sobre_el_sii/terminos_sitio_web.html) y, aunque reconocen una categoría "Open Data", no autorizan de forma clara la redistribución de estos archivos estadísticos en otros sitios — así que, siguiendo el criterio conservador de "si no está claro, no se redistribuye", los excluimos y documentamos su descarga aquí.

Todos son de **descarga pública y gratuita** directamente desde sii.cl — no requieren registro ni credenciales.

## 1. Archivos para el pipeline principal (`src/pipeline.py`, `src/validar_cruzado.py`)

| Archivo | Contiene | URL oficial | Fecha de consulta | Guardar en |
|---|---|---|---|---|
| `Ciclo_Vida.zip` | Aperturas (`PUB_actividades_inscritas.txt`) y cierres/término de giro (`PUB_TG.txt`), 2005–2024 | https://www.sii.cl/sobre_el_sii/estadisticas/ciclo_de_vida/Ciclo_Vida.zip | 2026-09-01 | `data/raw/Ciclo_Vida.zip` |
| `PUB_COMU_RUBR.xlsb` | Empresas activas por año, comuna y rubro económico, 2005–2024 | https://www.sii.cl/sobre_el_sii/empresas/PUB_COMU_RUBR.xlsb | 2026-09-01 | `data/raw/PUB_COMU_RUBR.xlsb` |
| `PUB_Reg_Com_Rub.xlsx` | Igual que el anterior pero de una publicación anterior del SII (taxonomía CIIU Rev.3, 2005–2015) — solo se usa para validación cruzada independiente, no para el análisis principal | https://www.sii.cl/estadisticas/region/PUB_Reg_Com_Rub.xlsx | 2026-09-01 | `data/raw/PUB_Reg_Com_Rub.xlsx` |

## 2. Archivos para la clasificación oficial de tamaño de empresa (`src/analisis_tamano_empresas.py`)

`PUB_COMU_RUBR.xlsb` no permite saber si una empresa es pyme o grande — es un agregado, no un registro por empresa. Estos 4 archivos sí publican la clasificación oficial:

| Archivo | Clasificación | URL oficial | Fecha de consulta | Guardar en |
|---|---|---|---|---|
| `PUB_TRAM5_RUBR.xlsb` | Por tramo de ventas (Ley 20.416) × rubro | https://www.sii.cl/sobre_el_sii/empresas/PUB_TRAM5_RUBR.xlsb | 2026-09-01 | `data/raw/PUB_TRAM5_RUBR.xlsb` |
| `PUB_TRAM5_COMU.xlsb` | Por tramo de ventas (Ley 20.416) × comuna | https://www.sii.cl/sobre_el_sii/empresas/PUB_TRAM5_COMU.xlsb | 2026-09-01 | `data/raw/PUB_TRAM5_COMU.xlsb` |
| `PUB_RUBR_TRTRAB.xlsb` | Por N° de trabajadores (referencia, no oficial) × rubro | https://www.sii.cl/sobre_el_sii/empresas/PUB_RUBR_TRTRAB.xlsb | 2026-09-01 | `data/raw/PUB_RUBR_TRTRAB.xlsb` |
| `PUB_COMU_TRTRAB.xlsb` | Por N° de trabajadores (referencia, no oficial) × comuna | https://www.sii.cl/sobre_el_sii/empresas/PUB_COMU_TRTRAB.xlsb | 2026-09-01 | `data/raw/PUB_COMU_TRTRAB.xlsb` |

**Clasificación oficial usada:** Ley 20.416 (ventas anuales en UF) — Micro ≤2.400 UF, Pequeña ≤25.000 UF, Mediana ≤100.000 UF, Grande sobre eso. Los archivos `PUB_TRAM5_*` clasifican en 5 tramos según esa ley.

## 3. Archivo no usado por ningún script actual

| Archivo | Por qué está listado igual | URL oficial | Fecha de consulta | Guardar en |
|---|---|---|---|---|
| `PUB_Rub_Sub_Act.xlsx` | Se descargó durante la exploración inicial del proyecto pero ningún script lo usa hoy — se documenta por transparencia, no hace falta descargarlo para reproducir el proyecto | https://www.sii.cl/sobre_el_sii/estadisticas_rubro/PUB_Rub_Sub_Act.xlsx | 2026-09-01 | `data/raw/PUB_Rub_Sub_Act.xlsx` |

> Las URLs de las tablas 1 y 3 vienen de páginas del SII que han cambiado de estructura más de una vez — si un enlace no funciona, busca el archivo por nombre desde [sii.cl/sobre_el_sii/estadisticas_de_empresas.html](https://www.sii.cl/sobre_el_sii/estadisticas_de_empresas.html) (para los archivos `PUB_*` por comuna/rubro/tramo) o [sii.cl/sobre_el_sii/estadisticas_inicio_de_actividades.html](https://www.sii.cl/sobre_el_sii/estadisticas_inicio_de_actividades.html) (para `Ciclo_Vida.zip`).

## 4. Geometría del mapa (opcional — el mapa ya viene pre-construido)

`outputs/geo_comunas.json` (incluido en este repositorio, 1.1 MB) ya trae la geometría de las 345 comunas lista para el dashboard — **no hace falta descargar nada para ver el mapa**.

Si quieres *reconstruir* esa geometría desde cero (`python src/preparar_geo_comunas.py --regenerar-geo` vía `run_pipeline.py`), descarga los 16 GeoJSON regionales + `codigos_territoriales.csv` (este último ya viene incluido en `data/reference/`) desde [chilemapas](https://github.com/pachadotdev/chilemapas/tree/master/data_geojson) (licencia Apache 2.0) y colócalos en `data/reference/geo_raw/`.

## Cómo ejecutar el pipeline una vez descargados los datos

```bash
# 1. Colocar los archivos de la tabla 1 en data/raw/ (mínimo necesario para el pipeline principal)
# 2. Colocar los 4 archivos de la tabla 2 en data/raw/ (para la clasificación de tamaño de empresa)
pip install -r requirements.txt
python run_pipeline.py
```

`run_pipeline.py` verifica que los archivos necesarios existan antes de correr cada etapa y muestra un mensaje claro (no un traceback) si falta alguno.
