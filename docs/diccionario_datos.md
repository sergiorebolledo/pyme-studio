# Diccionario de datos

Nombres reales de columnas tal como aparecen en el código y en los CSV de `outputs/` — sin traducir ni simplificar. Ver también el [glosario de conceptos](../README.md#glosario) en el README para las definiciones en lenguaje simple antes de las fórmulas.

## `outputs/pyme_studio_unificado.csv`

*Generado por `src/pipeline.py`. Una fila por (año, comuna, rubro). No versionado — se regenera con `python run_pipeline.py` (ver `data/README.md`).*

| Columna | Significado | Tipo | Unidad | Fuente | Fórmula / tratamiento | Valores ausentes |
|---|---|---|---|---|---|---|
| `anio` | Año comercial | entero | año (2005–2024) | Las 3 fuentes del SII | — | No hay ausentes (columna clave) |
| `comuna` | Comuna de Chile | texto | — | Las 3 fuentes del SII | Normalizada: sin espacios extra, mayúsculas | No hay ausentes (columna clave) |
| `rubro` | Rubro económico (CIIU Rev.4, 1 dígito) | texto | — | Las 3 fuentes del SII | Normalizado: sin código de letra inicial ("A - "), sin tildes, mayúsculas — para que el mismo rubro tenga la misma clave en las 3 fuentes | No hay ausentes (columna clave) |
| `aperturas` | N° de actividades económicas inscritas ese año/comuna/rubro | entero | conteo | `PUB_actividades_inscritas.txt` | Suma de "Recuento" tras normalizar | 0 si la combinación no aparece en la fuente (ver "Tratamiento de combinaciones ausentes" en `metodologia/metodologia.md`) |
| `cierres` | N° de términos de giro registrados ese año/comuna/rubro | entero | conteo | `PUB_TG.txt` | Suma de "Recuento" tras normalizar; se descartan ~27% de filas 100% vacías (relleno del export del SII) y la categoría residual "Valor por Defecto" | 0 si la combinación no aparece en la fuente |
| `empresas_activas` | N° de empresas activas ese año/comuna/rubro | entero | conteo (stock, no flujo) | `PUB_COMU_RUBR.xlsb` | Suma directa; se descarta la categoría residual "Sin información" | 0 si la combinación no aparece — **caso documentado como no confirmado al 100%**, ver metodología |
| `tasa_cierre` | `cierres / empresas_activas` de ese año/comuna/rubro | decimal | proporción (0–1, puede superar 1 en celdas muy chicas) | Calculado | `cierres / empresas_activas`, redondeado a 4 decimales | `NaN` cuando `empresas_activas = 0` — deliberadamente no se fuerza a 0, para no confundir "sin empresas" con "0% de cierre" |

## `outputs/pyme_studio_agregado_comuna_rubro.csv` y `..._enriquecido.csv`

*Generados por `src/analisis_hito4.py` (el primero) y `src/analisis_metodologia.py` (el segundo, agrega `participacion_promedio` sin tocar el original). Una fila por (comuna, rubro), agregando los 20 años completos. No versionados — se regeneran con el pipeline.*

| Columna | Significado | Tipo | Unidad | Fórmula |
|---|---|---|---|---|
| `aperturas_total` | Suma de aperturas 2005–2024 | entero | conteo | `sum(aperturas)` por comuna+rubro |
| `cierres_total` | Suma de cierres 2005–2024 | entero | conteo | `sum(cierres)` por comuna+rubro |
| `empresa_anios` | Exposición total — ver glosario | entero | empresa-años | `sum(empresas_activas)` a través de los 20 años. Ejemplo: 100 empresas activas × 10 años = 1.000 empresa-años |
| `concentracion_promedio` | Concentración absoluta — tamaño típico del rubro en esa comuna | decimal | empresas (promedio) | `mean(empresas_activas)` a través de los 20 años |
| `participacion_promedio` | Concentración relativa — qué proporción del tejido empresarial de la comuna representa ese rubro | decimal | proporción (0–1) | Promedio de `empresas_activas_rubro / total_empresas_activas_comuna` año a año. Solo en el archivo `_enriquecido.csv` |
| `tasa_cierre` | Tasa de cierre por empresa-año de exposición | decimal | proporción | `cierres_total / empresa_anios` — más robusta que promediar tasas anuales, porque no le da el mismo peso a un año con pocas empresas que a uno con muchas |

## `outputs/pyme_studio_correlacion_por_rubro.csv` y `..._ajustada.csv`

*El primero, de `analisis_hito4.py` (sin ajustar); el segundo, de `analisis_comparaciones_multiples.py` (con corrección FDR y Bonferroni, sin modificar el original). Una fila por rubro con muestra suficiente (≥30 comunas, ≥50 empresa-años por combinación).*

| Columna | Significado | Tipo | Fórmula / criterio |
|---|---|---|---|
| `n_comunas` | N° de comunas comparadas para ese rubro | entero | Comunas con ≥50 empresa-años en ese rubro |
| `spearman_r` | Correlación de Spearman entre `concentracion_promedio` y `tasa_cierre`, entre comunas, dentro del rubro | decimal (−1 a 1) | `scipy.stats.spearmanr` |
| `p_valor` / `p_valor_original` | Significancia estadística sin ajustar | decimal (0–1) | — |
| `p_ajustado_fdr` | Valor p ajustado por comparaciones múltiples (Benjamini-Hochberg) | decimal (0–1) | `scipy.stats.false_discovery_control`, familia = los 19 rubros |
| `p_ajustado_bonferroni` | Valor p ajustado, contraste conservador | decimal (0–1) | `p_valor_original × 19`, acotado a 1.0 |
| `significativo_original` / `_fdr` / `_bonferroni` | ¿`p < 0,05` bajo cada criterio? | booleano | — |
| `cambia_conclusion_fdr` / `_bonferroni` | ¿La significancia cambia respecto de la versión sin ajustar? | booleano | `significativo_original != significativo_X` |

## `outputs/pyme_studio_sensibilidad_2016.csv`

*De `analisis_metodologia.py`. Compara la correlación con y sin el año 2016 (ver el caso de 2016 en el README).*

| Columna | Significado |
|---|---|
| `spearman_r_con_2016` / `p_valor_con_2016` | Correlación y p-valor con los 20 años completos (= el resultado original) |
| `spearman_r_sin_2016` / `p_valor_sin_2016` | Correlación y p-valor excluyendo 2016 |
| `diferencia_r` | `spearman_r_con_2016 − spearman_r_sin_2016` |
| `cambia_signo` | ¿El signo de la correlación cambia al excluir 2016? |
| `cambia_conclusion` | ¿Cambia el signo o la significancia (`p<0,05`) al excluir 2016? |

## `outputs/pyme_studio_concentracion_absoluta_vs_relativa.csv`

*De `analisis_metodologia.py`. Compara medir concentración como conteo absoluto vs. como participación relativa dentro de la comuna.*

| Columna | Significado |
|---|---|
| `r_absoluta` / `p_absoluta` | Correlación usando `concentracion_promedio` (conteo absoluto) |
| `r_relativa` / `p_relativa` | Correlación usando `participacion_promedio` (proporción del tejido comunal) |
| `mismo_signo` | ¿Coinciden en signo ambas métricas? |
| `sig_absoluta` / `sig_relativa` | ¿`p<0,05` bajo cada métrica? |

## `outputs/pyme_studio_estabilidad_subperiodos.csv`

*De `analisis_subperiodos.py`. Repite la correlación por rubro en 4 subperíodos + el período completo (con y sin 2016).*

| Columna | Significado |
|---|---|
| `periodo` | Nombre del subperíodo (ej. "2016-2019") |
| `anio_inicio` / `anio_fin` | Límites del período (texto en `anio_fin` cuando excluye un año, ej. "2024 (excl. 2016)") |
| `n_combinaciones` | N° de combinaciones comuna+rubro con ≥50 empresa-años en ese período (antes de agrupar por rubro) |
| `p_ajustado_fdr` | Corrección FDR dentro de la familia de rubros **de ese período** — no se mezcla con la corrección del período completo |
| `significativo` | `p_ajustado_fdr < 0,05` Y no `muestra_insuficiente` |
| `cambia_signo_vs_completo` / `cambia_significancia_vs_completo` | Comparación de ese subperíodo contra el período completo 2005–2024 |
| `muestra_insuficiente` | `n_comunas < 30` para ese rubro en ese período, o la correlación quedó indefinida (muestra degenerada) — advertencia, no error |

## `outputs/pyme_studio_alcance_pyme_por_rubro.csv` y `..._por_comuna.csv`

*De `analisis_tamano_empresas.py`. Qué porcentaje del universo analizado es pyme según la clasificación oficial (Ley 20.416).*

| Columna | Significado |
|---|---|
| `pct_pyme_ventas_oficial` | % de empresas clasificadas pyme por tramo de ventas (Ley 20.416) — la cifra oficial |
| `pct_pyme_trabajadores` | % de empresas clasificadas pyme por tramo de trabajadores — referencia, no oficial |
| `diferencia_pp` | Diferencia en puntos porcentuales entre ambos criterios |
| `total_empresas` / `empresas_grandes` / `pct_grande` | (solo en `_por_comuna.csv`) conteos y porcentaje de empresas "grande" por comuna |
