# PYME Studio — Paso 8: Tablero de seguimiento

*Módulo 1, pág. 5 · listo para copiar en Trello/Jira/Notion*

> Corrección respecto a la versión anterior de este archivo: el módulo no define "3 hitos" fijos — pide **entre 4 y 6 hitos comprobables** por proyecto (checkpoint "Primer plan del Capstone"). Se usa aquí el ejemplo de 6 hitos de la página 5, adaptado a PYME Studio.

## Las 5 columnas con las tarjetas reales del proyecto

| 1. Alcance y Diseño | 2. Ingesta y Datos | 3. Almacenamiento | 4. Procesamiento | 5. Dashboard/Entregable |
|---|---|---|---|---|
| **🏁 HITO 1** | | **🏁 HITO 2** | **🏁 HITO 3** | **🏁 HITO 4 · 5 · 6** |
| Enunciado del problema (hecho) | Descargar `Ciclo_Vida.zip` (hecho) | Decidir tratamiento de comunas vacías (~27%) | Corregir encoding | Calcular indicadores de concentración y tasa de cierre |
| Pregunta de datos (hecho) | Validar fuente SII (hecho) | Cargar TG + actividades inscritas en almacén de trabajo | Armonizar categorías de "Rubro" | Construir dashboard/mapa por comuna y rubro |
| Definir alcance a nivel comuna (hecho) | | | Unir aperturas + cierres por año/comuna/rubro | Documentar arquitectura y decisiones |
| | | | Calcular tasa de rotación/cierre | Preparar presentación (2-3 hallazgos) |

## Los 6 hitos comprobables de PYME Studio

| Hito | Descripción | Cómo se comprueba (no vago) | Estado |
|---|---|---|---|
| **1** | Problema y fuentes de datos validados | `definicion_problema.md` + `factibilidad.md` completos, con fuente SII confirmada | ✅ Hecho |
| **2** | Datos obtenidos y almacenados | Los 3 archivos del SII descargados en `../../data/raw/` (aperturas, cierres, empresas activas — las 3 fuentes ya cubren 2005-2024) | ✅ Hecho |
| **3** | Pipeline de procesamiento funcional | `../../src/pipeline.py` corre sin errores y entrega `../../outputs/pyme_studio_unificado.csv` — 126.566 filas, 2005-2024, 348 comunas, 21 rubros, con `tasa_cierre` calculada | ✅ Hecho |
| **4** | Primer análisis completo | Correlación concentración~cierre calculada (global y por rubro, con significancia estadística), documentada en `../analisis/analisis.md`, más un endurecimiento metodológico posterior (sensibilidad a 2016, concentración relativa, alcance del universo pyme) en `../metodologia/metodologia.md` | ✅ Hecho |
| **5** | Producto o visualización funcional | **`../../dashboard/pyme_studio_dashboard.html` es el entregable oficial** (mapa coroplético de Chile por comuna, KPIs, ranking de correlación por rubro, serie de tiempo nacional, selector de rubro con dispersión y rankings de comunas riesgosas/saludables) — ver `producto_dashboard.md` | ✅ Hecho |
| **6** | Integración y presentación final | **`../presentacion/PYME_Studio_Presentacion.pptx` es el entregable oficial** (problema, arquitectura, factibilidad, pipeline, hallazgos con imágenes reales, el dashboard, robustez metodológica, conclusiones y equipo) — ver `../presentacion/presentacion.md` | ✅ Hecho |

## Los 6 hitos del Módulo 1, completos

**PYME Studio tiene los 6 hitos resueltos, cada uno con evidencia verificable, no solo declarada:**
1. Problema y fuentes validados → `definicion_problema.md` + `factibilidad.md`
2. Datos obtenidos y almacenados → 4 archivos reales en `../../data/raw/`
3. Pipeline funcional → `../../src/pipeline.py` corre sin errores, 126.566 filas
4. Primer análisis completo → `../analisis/analisis.md`, correlación con significancia estadística
5. Producto funcional → `../../dashboard/pyme_studio_dashboard.html` (entregable oficial, con mapa), interactivo y accesible
6. Presentación final → `../presentacion/PYME_Studio_Presentacion.pptx` (entregable oficial), ver `../presentacion/presentacion.md`

**Único pendiente real:** completar el placeholder `[equipo]` en la portada de la presentación — ver la nota en `gantt.md` con la pista del mini-proyecto anterior del equipo (`miniproyecto_empresas.ipynb`), a confirmar por el equipo antes de darla por buena.
