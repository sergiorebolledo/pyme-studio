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

5. DATOS UTILIZADOS Y METODOLOGÍA

FUENTES (SII, 2005-2024, todas a nivel año-comuna-rubro CIIU)

- PUB_actividades_inscritas.txt: inicios/ampliaciones de actividad económica -> variable derivada "aperturas"
- PUB_TG.txt: términos de giro -> variable derivada "cierres"
- PUB_COMU_RUBR.xlsb: empresas activas por año-comuna-rubro (agregado oficial) -> variable derivada "empresas_activas"

Las tres fuentes se normalizan con la misma clave (función normalizar_rubro: saca el código de letra inicial, quita tildes, pasa a mayúsculas) y se agregan por (año, comuna, rubro). Se unen con un merge tipo "outer" y los NaN resultantes de exposición nula se rellenan con 0 en aperturas, cierres y empresas_activas, excepto en la tasa de cierre, donde un denominador 0 se deja como NaN en vez de forzarse a 0, para no inventar una tasa donde no hubo empresas activas ese año.

DEFINICIÓN DE LA TASA DE CIERRE

Se usan dos variantes en el notebook, y vale la pena distinguirlas en el informe:

1) Anual: tasa_cierre = cierres / empresas_activas, para cada (año, comuna, rubro).

2) Agregada por combinación (usada en Preguntas 2 y 3):
   tasa_cierre = cierres_total / empresa_años
   donde empresa_años = suma de empresas_activas sobre los 20 años.
   Esto pondera por exposición real en vez de promediar tasas anuales, evitando que años con pocas empresas (tasas ruidosas, ej. 1 de 2) pesen igual que años con miles de empresas.

PREGUNTA 1 - CONCENTRACIÓN

Promedio simple (media aritmética) de empresas_activas por combinación (comuna, rubro) a través de los 20 años. No se pondera por tiempo ni por tamaño de comuna, así que combinaciones con series cortas o discontinuas entran igual que las completas.

PREGUNTA 2 - CONCENTRACIÓN VS. TASA DE CIERRE (NACIONAL)

Correlación de Pearson y de Spearman entre concentracion_promedio y tasa_cierre a nivel de combinación comuna-rubro, filtrando a empresa_años >= 200 (umbral arbitrario para excluir combinaciones con muy poca exposición, que inflarían el ruido).

Resultado: n = 3.932 combinaciones
  Pearson  r = -0.028  (p = 0.077)
  Spearman r = +0.029  (p = 0.066)

Ambos valores son prácticamente cero y no significativos al 5%: a nivel nacional agregado no hay relación lineal ni monotónica clara entre concentración y cierre.

PREGUNTA 3 - LO MISMO, POR RUBRO

Se repite el cálculo de Spearman pero agrupando por rubro (filtro adicional: 30+ comunas y 50+ empresa-años por combinación), quedando 19 rubros con muestra suficiente. Aquí aparece la matemática interesante que el resultado nacional esconde:

- Rubros con correlación NEGATIVA significativa (más concentración -> menos cierre):
    Agricultura, ganadería, silvicultura y pesca: rho = -0.27 (p < 0.001)
    Salud humana y asistencia social:            rho = -0.25 (p < 0.001)

- Rubros con correlación POSITIVA fuerte (más concentración -> más cierre, efecto saturación):
    Comercio al por mayor y al por menor: rho = 0.575 (p ~ 10^-31)
    Transporte y almacenamiento:          rho = 0.42
    Alojamiento y servicio de comidas:    rho = 0.36

Esto es, matemáticamente, un caso de heterogeneidad que se cancela al agregar (similar a una paradoja de Simpson): el -0.03 nacional no significa "no hay efecto", sino que es el promedio de efectos opuestos por sector. Conviene decirlo explícitamente en el informe, porque es el hallazgo más fuerte del análisis. Además, el r = 0,58 citado en las recomendaciones corresponde justamente a Comercio en este análisis por rubro, no a una correlación nacional — conviene aclarar esa distinción en el texto, porque tal como está escrito puede leerse como si fuera el resultado agregado de la Pregunta 2.

PREGUNTA 4 - SERIE TEMPORAL (APERTURAS Y CIERRES 2005-2024)

Es puramente descriptiva: suma nacional de aperturas y cierres por año, sin ajuste estacional ni prueba estadística. Está bien dejarlo así si el objetivo es solo mostrar la evolución, pero para reforzar el rigor matemático se podría agregar una tasa de crecimiento año a año, o una prueba de cambio estructural (por ejemplo, un test de Chow) en el quiebre de 2016 que se menciona en las conclusiones.

PREGUNTA 5 - VOLATILIDAD

Crecimiento histórico (CAGR) sobre trabajadores totales (ponderados + honorarios) por rubro:
  CAGR = (trabajadores_2024 / trabajadores_2005)^(1/19) - 1

Volatilidad: desviación estándar de la variación porcentual interanual (no de los niveles). Mide qué tan errático es el crecimiento año a año, no la dispersión de los niveles absolutos.

Correlación concentración vs. volatilidad (n = 19 rubros):
  Pearson  r = -0.16  (p = 0.50)
  Spearman r = -0.34  (p = 0.15)

Con una muestra tan chica (19 rubros) ninguna de las dos correlaciones es significativa. Este resultado es sugerente, no concluyente — n=19 da muy poca potencia estadística a cualquier prueba de hipótesis.
