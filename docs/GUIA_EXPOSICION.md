# Guía de exposición — preguntas probables de los profesores

Respuestas breves, técnicamente correctas y coherentes con el resto del proyecto. Si los resultados estadísticos cambian en el futuro, actualiza estas respuestas — no dejes que queden memorizadas y desactualizadas.

## ¿Por qué esto es Big Data?

Porque integra múltiples fuentes y formatos, resuelve problemas de volumen, variedad y veracidad, implementa el ciclo completo de los datos y entrega un producto de consumo. No se utilizó procesamiento distribuido porque el volumen podía manejarse eficientemente con Python. Ver la sección 2 del README para el detalle de cada V.

## ¿La concentración provoca cierres?

No podemos afirmar causalidad. Encontramos una asociación histórica que cambia según el rubro. El resultado más robusto corresponde a Comercio — se sostiene excluyendo 2016, con concentración relativa, y tras corregir por comparaciones múltiples.

## ¿Término de giro significa quiebra?

No necesariamente. Puede responder a razones voluntarias (venta del negocio, cambio de giro, jubilación) o administrativas (como el barrido de 2016). Por eso usamos el término oficial y no lo interpretamos automáticamente como fracaso.

## ¿Por qué 2016 tiene tantos términos de giro?

Ese año existe un efecto administrativo: la Ley 20.899 le dio al SII la facultad de declarar de oficio el término de giro de contribuyentes inactivos que nunca habían avisado formalmente. Repetimos el análisis excluyendo 2016 para comprobar si el resultado principal se mantenía — se mantuvo (Comercio r=0,575→0,521; Alojamiento/Comidas r=0,359→0,343).

## ¿Analizaron exclusivamente pymes?

El dataset principal incluye empresas activas sin desglose individual por tamaño. Una validación complementaria, con la clasificación oficial del SII (Ley 20.416), muestra que el universo es mayoritariamente pyme (91,6%–100% según el rubro) — pero no afirmamos que sea exclusivamente pyme.

## ¿Por qué utilizaron Spearman?

No exige una relación lineal, es menos sensible a valores extremos que Pearson, compara ordenamientos o relaciones monotónicas, y es razonable para variables territoriales muy asimétricas (unas pocas comunas grandes, muchas chicas).

## ¿Por qué corrigieron los valores p?

Porque se probaron 19 rubros simultáneamente. La corrección FDR reduce el riesgo de declarar asociaciones significativas solo por realizar muchas pruebas a la vez. En nuestro caso, los 3 rubros centrales se mantienen significativos bajo FDR y Bonferroni — solo un rubro marginal (Actividades Financieras y de Seguros) deja de serlo bajo el criterio más estricto.

## ¿La relación se mantiene igual en el tiempo?

No completamente. Comercio y Alojamiento/Comidas se fortalecen en los años recientes (2016 en adelante); Agricultura cambia de signo entre 2005-2010 (positivo) y 2016-2024 (negativo). El resultado del período completo es real, pero no fue igual de fuerte durante los 20 años — lo documentamos explícitamente en vez de presentarlo como constante.

## ¿Por qué no usaron Spark?

Porque la tecnología debe responder al volumen y al problema. Python procesó eficientemente el conjunto disponible (el pipeline completo corre en menos de un minuto); utilizar infraestructura distribuida habría agregado complejidad sin un beneficio proporcional.

## ¿Cuál es el aporte?

Mostrar que la concentración empresarial no puede interpretarse igual en todos los sectores, y entregar una herramienta territorial para explorar esa relación con datos oficiales — con las limitaciones metodológicas explícitas, no como una fórmula mágica.

## ¿Cuál es la principal limitación?

El análisis es agregado y observacional. No sigue empresas individuales ni demuestra causalidad. La tasa histórica de términos de giro es un cociente de dos conteos acumulados, no una tasa de supervivencia de una cohorte.
