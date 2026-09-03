# Guía de evaluación

Para revisar este proyecto según el tiempo disponible.

```
Si dispone de 2 minutos:
→ Leer el resumen ejecutivo del README (primeras 2 pantallas).

Si dispone de 5 minutos:
→ Abrir dashboard/pyme_studio_dashboard.html (doble clic, funciona sin internet).

Si quiere revisar la metodología:
→ Abrir docs/metodologia/metodologia.md.

Si quiere reproducir los resultados:
→ Seguir data/README.md (descarga de datos) y ejecutar `python run_pipeline.py`.

Si quiere comprobar los hitos:
→ Abrir docs/proceso/tablero.md.
```

## El problema

¿Existe una asociación histórica entre la concentración de empresas de un mismo rubro en una comuna y su tasa de términos de giro? Ver [`README.md`](../README.md#1-el-problema).

## Pregunta de investigación

¿Cuál es la concentración de empresas por rubro y comuna en Chile, y cómo se relaciona con su tasa histórica de término de giro?

## Entregables oficiales

| Entregable | Ruta |
|---|---|
| Dashboard (producto) | [`dashboard/pyme_studio_dashboard.html`](../dashboard/pyme_studio_dashboard.html) |
| Presentación | [`docs/presentacion/PYME_Studio_Presentacion.pptx`](presentacion/PYME_Studio_Presentacion.pptx) |
| Análisis principal | [`docs/analisis/analisis.md`](analisis/analisis.md) |
| Metodología y límites | [`docs/metodologia/metodologia.md`](metodologia/metodologia.md) |
| Fuentes de datos | [`data/README.md`](../data/README.md) |
| Pipeline (implementación oficial) | [`src/`](../src/) — se corre con [`run_pipeline.py`](../run_pipeline.py) |
| Diccionario de datos | [`diccionario_datos.md`](diccionario_datos.md) |
| Reproducibilidad | [`REPRODUCIBILIDAD.md`](REPRODUCIBILIDAD.md) |

## Correspondencia entre los 6 hitos y su evidencia

| Hito | Evidencia |
|---|---|
| 1. Problema y fuentes validados | [`docs/proceso/definicion_problema.md`](proceso/definicion_problema.md), [`docs/proceso/factibilidad.md`](proceso/factibilidad.md) |
| 2. Datos obtenidos y almacenados | [`data/README.md`](../data/README.md) (8 archivos oficiales del SII documentados) |
| 3. Pipeline funcional | [`src/pipeline.py`](../src/pipeline.py) — 126.566 filas, 2005-2024, sin errores (ver `docs/proceso/tablero.md`) |
| 4. Primer análisis completo | [`docs/analisis/analisis.md`](analisis/analisis.md) — correlación con significancia estadística, ajustada por comparaciones múltiples |
| 5. Producto funcional | [`dashboard/pyme_studio_dashboard.html`](../dashboard/pyme_studio_dashboard.html) |
| 6. Presentación final | [`docs/presentacion/PYME_Studio_Presentacion.pptx`](presentacion/PYME_Studio_Presentacion.pptx) |

Detalle completo del estado de cada hito en [`docs/proceso/tablero.md`](proceso/tablero.md).

## Limitaciones principales (leer antes de citar el hallazgo)

1. El universo es **mayoritariamente pyme, no exclusivamente pyme** (91,6%–100% según el rubro, verificado con la clasificación oficial del SII).
2. Es una **asociación histórica, no causalidad**.
3. **Término de giro no equivale a quiebra ni a fracaso empresarial** — puede ser administrativo o voluntario.
4. La tasa es **agregada por comuna+rubro**, no predice el cierre de una empresa individual.
5. Con 19 rubros probados a la vez, se aplicó **corrección por comparaciones múltiples** (FDR y Bonferroni) — ver `docs/metodologia/metodologia.md`.
6. La correlación **no es estable en el tiempo de la misma forma en todos los rubros** — Comercio y Alojamiento/Comidas se fortalecen en los años recientes; Agricultura cambia de signo entre 2005-2010 y 2016-2024. Ver "Estabilidad por subperíodo" en la metodología.

Detalle técnico completo de las 6 en [`docs/metodologia/metodologia.md`](metodologia/metodologia.md).
