# PYME Studio — Anexo: metodología, alcance y limitaciones

*Endurecimiento metodológico para la entrega final académica — revisión de alcance del universo analizado, robustez de los resultados y precisión conceptual. No reemplaza `../analisis/analisis.md`; lo complementa con chequeos hechos después del análisis original, sin sobrescribir sus resultados (ver sección "Trazabilidad" al final).*

---

## 1. Alcance real del universo: ¿"PYME Studio" mide pymes?

**La pregunta:** `pipeline.py` cuenta todo contribuyente con actividad vigente en el SII — no filtra por tamaño de empresa. El nombre "PYME Studio" asumía "pyme" sin haberlo comprobado con datos.

**Lo que se comprobó primero:** `PUB_COMU_RUBR.xlsb` (la fuente que usa el pipeline) **no permite** clasificar tamaño de empresa — es un agregado (total de ventas y trabajadores por comuna+rubro+año), no un registro por empresa individual. No trae ninguna columna de tramo.

**Lo que sí existe:** el SII publica la clasificación oficial en archivos separados, con dos criterios:
- **Por ventas anuales en UF** — la clasificación **legal/oficial** de pyme en Chile (Ley 20.416): Micro ≤2.400 UF, Pequeña ≤25.000 UF, Mediana ≤100.000 UF, Grande sobre eso. Fuente: `PUB_TRAM5_RUBR.xlsb` / `PUB_TRAM5_COMU.xlsb`.
- **Por N° de trabajadores** (0-9 / 10-49 / 50-249 / 250+) — clasificación de referencia, no la oficial. Fuente: `PUB_RUBR_TRTRAB.xlsb` / `PUB_COMU_TRTRAB.xlsb`.

**Script:** `../../src/analisis_tamano_empresas.py` → `../../outputs/pyme_studio_alcance_pyme_por_rubro.csv`, `../../outputs/pyme_studio_alcance_pyme_por_comuna.csv`.

**Resultado (clasificación oficial por ventas, 2005-2024):**

| Rubro | % pyme (oficial, ventas) | % pyme (referencia, trabajadores) |
|---|---:|---:|
| **Comercio al por mayor y al por menor** | **98,92%** | 99,83% |
| **Alojamiento y servicio de comidas** | **99,68%** | 99,78% |
| Mínimo de todos los rubros | 91,64% (Suministro eléctrico/gas) | 60,95% (Administración pública) |

A nivel comuna, el promedio nacional de empresas "grandes" es 0,60% (mediana 0,38%).

**Conclusión sobre el alcance:** el universo medido es, en la práctica, **abrumadoramente pyme** — entre 91,6% y 100% según el rubro, con los dos rubros del hallazgo central por sobre 98,9%. Esto respalda mantener "PYME Studio" como nombre del producto. **Pero el pipeline no filtra por tamaño**, así que en todos los entregables se reemplazan afirmaciones que digan "el dataset contiene exclusivamente pymes" por una redacción precisa: **"empresas registradas activas, mayoritariamente pymes (>90% en todos los rubros analizados, confirmado con la clasificación oficial de la Ley 20.416)"**. La diferencia entre "exclusivamente" y "mayoritariamente, con verificación" es la que corrige este punto.

**Por qué esto no está ya en el pipeline principal:** el cruce que haría falta para filtrar exacto — comuna × rubro × tramo — no existe publicado (probablemente por secreto estadístico: una celda comuna×rubro×tramo suele tener 0-2 empresas, lo que identificaría negocios puntuales). Filtrar por tamaño a nivel nacional o por rubro es posible (y se hizo, arriba); filtrar la tabla comuna×rubro que usa el análisis principal, no.

---

## 4b. Sensibilidad al año 2016 — detalle técnico

*(La interpretación prudente para el hallazgo principal está en `../analisis/analisis.md`, sección "Sensibilidad a 2016". Acá va el detalle metodológico completo.)*

**Script:** `../../src/analisis_metodologia.py` → `../../outputs/pyme_studio_sensibilidad_2016.csv` + `../../outputs/figures/hito4_sensibilidad_2016.png`.

**Método:** se recalculó la correlación de Spearman por rubro (misma metodología que `analisis_hito4.py`: 50+ empresa-años de exposición, 30+ comunas por rubro) dos veces — una con los 20 años completos (2005-2024, el resultado original) y otra excluyendo 2016 (el año del "barrido administrativo" de la Ley 20.899).

**Resultado:** de 19 rubros, **2 cambian de conclusión** (signo o significancia) al excluir 2016 — Enseñanza y Actividades Financieras y de Seguros, ninguno de los dos parte del hallazgo central. **Los 2 rubros del hallazgo central son estables:**

| Rubro | r con 2016 | r sin 2016 | Diferencia | ¿Cambia conclusión? |
|---|---:|---:|---:|---|
| Comercio al por mayor y al por menor | 0,575 | 0,521 | 0,054 | No |
| Alojamiento y servicio de comidas | 0,359 | 0,343 | 0,017 | No |

**Interpretación:** el año 2016 sube ligeramente la correlación en la mayoría de los rubros (es de esperar — un evento que generó cierres masivos y correlacionados con el tamaño de la base de contribuyentes añade señal), pero no la crea de la nada. El hallazgo central no depende de ese año.

---

## 5b. Concentración absoluta vs. relativa — detalle técnico

*(Motivación completa y hallazgo principal en `../analisis/analisis.md`.)*

**Script:** `../../src/analisis_metodologia.py` → `../../outputs/pyme_studio_agregado_comuna_rubro_enriquecido.csv` (agrega la columna `participacion_promedio` sin tocar el archivo original) + `../../outputs/pyme_studio_concentracion_absoluta_vs_relativa.csv`.

**Definición:** `participacion_rubro_comuna = empresas activas del rubro en la comuna / total de empresas activas de la comuna`, calculada año a año (2005-2024) y promediada — igual que `concentracion_promedio`, pero como proporción del tejido empresarial local, no como conteo absoluto.

**Resultado — de 19 rubros, 8 cambian de signo entre concentración absoluta y relativa:**

| Rubro | r (absoluta) | r (relativa) | ¿Mismo signo? |
|---|---:|---:|---|
| **Comercio al por mayor y al por menor** | **0,575** | **0,322** | ✅ Sí — se mantiene, ambos significativos |
| **Alojamiento y servicio de comidas** | **0,359** | **−0,535** | ❌ **No — se invierte** |
| Suministro de agua/gestión de desechos | 0,348 | −0,644 | ❌ No |
| Administración pública | 0,099 (n.s.) | −0,812 | ❌ No (pasa a significativo) |

**Lectura honesta:** el hallazgo de **Comercio es robusto** a este cambio metodológico — se mantiene positivo y significativo tanto midiendo concentración por conteo absoluto como por participación relativa dentro de la comuna. **El hallazgo de Alojamiento/Comidas NO es robusto** — se invierte. Una lectura plausible: en comunas donde alojamiento/comidas es una porción *grande* del tejido comercial local (comunas turísticas especializadas, ej. balnearios, destinos de montaña), el rubro tiende a ser *más* estable, no menos — es la actividad económica dominante y probablemente más profesionalizada. La correlación positiva original (por conteo absoluto) puede estar reflejando que las ciudades grandes con MUCHOS locales de alojamiento/comidas en términos absolutos (Santiago, Providencia) también concentran mucha otra actividad económica y más rotación general — no necesariamente saturación de ese rubro específico.

**Qué hacer con esto:** no se retira el hallazgo de Alojamiento/Comidas del proyecto — se documenta con ambas caras. El dashboard y la presentación deben mostrar ambas métricas para este rubro, no solo la absoluta — no presentar la concentración absoluta como "saturación" sin esta advertencia (ver punto 7 más abajo).

---

## 5c. Corrección por comparaciones múltiples — detalle técnico

**Por qué hace falta:** `analisis_hito4.py` prueba 19 hipótesis independientes (una correlación por rubro). Evaluar cada una contra alpha=0,05 sin ajustar infla la probabilidad de declarar "significativo" algo que en realidad es ruido, solo por el número de pruebas realizadas.

**Script:** `../../src/analisis_comparaciones_multiples.py` → `../../outputs/pyme_studio_correlacion_por_rubro_ajustada.csv` (no modifica `pyme_studio_correlacion_por_rubro.csv`).

**Métodos aplicados a la familia principal de 19 rubros (alpha=0,05):**
- **Benjamini-Hochberg / FDR** (principal): controla la tasa esperada de falsos descubrimientos entre los rubros declarados significativos.
- **Bonferroni** (contraste conservador): controla la probabilidad de al menos un falso positivo en toda la familia.

**Resultado:**

| Criterio | Rubros significativos (de 19) |
|---|---:|
| Sin ajustar | 12 |
| FDR (Benjamini-Hochberg) | 12 — **0 cambian de conclusión** |
| Bonferroni | 11 — **1 cambia de conclusión** |

El único rubro que cambia de conclusión es **Actividades Financieras y de Seguros** (p original = 0,027, ya identificado como marginal): sigue significativo bajo FDR pero deja de serlo bajo Bonferroni (p ajustado = 0,505). **Enseñanza** ya era no significativo sin ajustar (p=0,079), así que no "cambia" — nunca cruzó el umbral.

**Los 3 rubros del hallazgo central (Comercio, Alojamiento/Comidas, Agricultura) se mantienen significativos bajo ambos criterios**, con p-valores ajustados muchos órdenes de magnitud por debajo de 0,05 (ej. Comercio: p original = 1,6×10⁻³¹, p ajustado FDR = 3,1×10⁻³⁰). La corrección por comparaciones múltiples no debilita el hallazgo principal — solo aclara que el único resultado sensible a este chequeo es uno ya marcado como marginal.

**Familia de hipótesis:** esta corrección se aplica solo a la familia de 19 rubros de `analisis_hito4.py` — no se mezcla con la sensibilidad a 2016 (5b) ni con la comparación absoluta/relativa (5b arriba), que son preguntas metodológicas distintas. Cada subperíodo (5d, abajo) forma su propia familia de 19, corregida por separado.

---

## 5d. Estabilidad por subperíodo — detalle técnico

**Por qué hace falta:** el resultado principal agrega 2005-2024 completo. Antes de presentarlo como una relación estable, corresponde comprobar si se sostiene dentro de ventanas de tiempo más cortas, o si es un artefacto de promediar 20 años con comportamientos distintos.

**Script:** `../../src/analisis_subperiodos.py` → `../../outputs/pyme_studio_estabilidad_subperiodos.csv` + `../../outputs/figures/hito4_estabilidad_subperiodos.png`.

**Períodos evaluados:** 2005-2010, 2011-2015, 2016-2019, 2020-2024, el completo 2005-2024, y el completo excluyendo 2016 — misma metodología que el análisis principal (Spearman, ≥50 empresa-años por combinación, ≥30 comunas por rubro), con corrección FDR aplicada **dentro de cada período por separado** (cada subperíodo es su propia familia de 19 hipótesis).

**Resultado — los 3 rubros centrales, por período:**

| Período | Comercio | Alojamiento/Comidas | Agricultura |
|---|---:|---:|---:|
| 2005-2010 | r=0,060 (n.s.) | r=0,124 (n.s.) | r=0,214 (sig., **positivo**) |
| 2011-2015 | r=0,271 (sig.) | r=0,131 (sig., marginal) | r=0,102 (n.s.) |
| 2016-2019 | r=0,504 (sig.) | r=0,149 (sig.) | r=−0,309 (sig., **negativo**) |
| 2020-2024 | r=0,542 (sig.) | r=0,367 (sig.) | r=−0,408 (sig., **negativo**) |
| 2005-2024 (completo) | r=0,575 (sig.) | r=0,359 (sig.) | r=−0,268 (sig.) |

**Interpretación prudente — esto es un hallazgo real, no ruido de muestra chica:**

- **Comercio y Alojamiento/Comidas se fortalecen con el tiempo.** Ambos parten débiles o no significativos en 2005-2010 y se vuelven consistentemente más fuertes en cada período posterior, hasta llegar a su punto más alto en 2020-2024. El resultado del período completo (r=0,575 y r=0,359) es real, pero está más influenciado por los años recientes que por los primeros — el patrón nunca cambia de signo, solo de intensidad.
- **Agricultura cambia de signo.** Es positivo y significativo en 2005-2010, pierde significancia en 2011-2015, y se vuelve negativo y significativo desde 2016 en adelante. El resultado del período completo (r=−0,268) refleja sobre todo la segunda mitad del período — la primera mitad mostraba lo contrario. Esto no invalida el hallazgo del período completo, pero sí significa que "la concentración en Agricultura se asocia con menos cierre" es una descripción más precisa de 2016-2024 que de los 20 años completos.
- **Los subperíodos de 4-5 años tienen menos muestra que el período completo** (menos empresa-años de exposición), así que sus estimaciones son individualmente menos estables — se reconoce esto explícitamente y no se presenta un solo subperíodo como definitivo. El período 2016-2019 además contiene el evento administrativo de 2016 (ver 4b).
- No se interpretan estas variaciones como cambios estructurales abruptos — es un patrón gradual y consistente con la idea de que el tejido comercial y de servicios chileno evolucionó (más comercio electrónico, cambios post-pandemia, etc.) durante estos 20 años, no un quiebre puntual.

**Qué hacer con esto:** el README y la presentación citan el resultado del período completo (es la comparación más simple y la que tiene mayor muestra), pero mencionan que la relación se fortalece con el tiempo en Comercio/Alojamiento y cambia de signo en Agricultura — no se presenta el hallazgo como si hubiera sido igual de válido en 2006 que en 2024.

---

## 6. Tratamiento de combinaciones ausentes (año, comuna, rubro)

**La pregunta:** `pipeline.py` hace un `outer join` entre las 3 fuentes y rellena con 0 donde una fuente no tenga una combinación (año, comuna, rubro). ¿La ausencia significa realmente cero, o podría significar "no informado"?

**Decisión, por fuente:**

- **Aperturas (`PUB_actividades_inscritas.txt`) y cierres (`PUB_TG.txt`):** son **registros administrativos de eventos** — cada fila representa un trámite real (un inicio de actividades, un término de giro) que efectivamente ocurrió y quedó registrado en el SII ese año, en esa comuna, en ese rubro. El SII no publica filas con "0 eventos" (sería una tabla enorme y casi toda vacía) — simplemente omite la combinación. **La ausencia de una combinación en estas 2 fuentes significa, con confianza razonable, cero eventos de ese tipo ese año** — no dato faltante. `fillna(0)` es la interpretación correcta.

- **Empresas activas (`PUB_COMU_RUBR.xlsb`):** es una **medida de stock** (cuántas empresas estaban activas ese año), no un registro de eventos. Acá la ausencia es más ambigua: podría ser "cero empresas activas de ese rubro en esa comuna ese año" (interpretación más probable, dado que el SII sí publica agregados con conteos muy bajos — se ven celdas con 1 empresa activa en el dataset, ver `../../outputs/reporte_calidad.md`) o, en teoría, una supresión por secreto estadístico en celdas ultra pequeñas (como sí se confirmó que ocurre en otras publicaciones del SII con columnas de venta/renta, marcadas con `*`). **No se pudo confirmar cuál de las dos aplica para esta fuente específica** sin acceso a la metodología interna del SII.

**Qué se hizo con esto:** no se cambió el comportamiento del pipeline (`fillna(0)` se mantiene) — cambiarlo sin medir el efecto habría violado el criterio de esta revisión. Se documenta la decisión (arriba) y se agrega la advertencia correspondiente en `README.md` y en el dashboard: **el conteo de "empresas activas" en celdas con muy pocas empresas puede subestimar levemente la actividad real si el SII suprime celdas mínimas** — efecto que, de existir, sería pequeño (afecta solo a comuna+rubro con actividad ya marginal) y ya queda parcialmente mitigado por el umbral `MIN_EMPRESA_ANIOS >= 50` que usa `analisis_hito4.py` para el análisis por rubro.

---

## 7. Precisión conceptual — cómo se debe (y no se debe) describir el hallazgo

Se revisaron todos los entregables (README, análisis, dashboard, presentación) para no tratar como equivalentes:

- **Término de giro** (el hecho administrativo que mide el SII) ≠ **quiebra** (proceso legal específico) ≠ **fracaso empresarial** (juicio de valor, no observable en los datos) ≠ **probabilidad individual de cierre** (el dataset es agregado, no de nivel-empresa).

**Redacción estándar adoptada en todos los entregables**, en vez de "tasa de cierre" sin más contexto la primera vez que aparece en cada documento:

> "Asociación histórica entre concentración empresarial y términos de giro registrados — no es una medición directa de fracaso ni de quiebra legal."

**Cuatro aclaraciones que deben aparecer explícitamente en cada entregable** (README, `../analisis/analisis.md`, el dashboard, la presentación):

1. La correlación no demuestra causalidad.
2. La tasa agregada (por comuna+rubro) no predice el cierre de una empresa individual.
3. Un término de giro puede tener razones administrativas (ej. el barrido de 2016, ver `../analisis/analisis.md`) o voluntarias (venta, cambio de giro, jubilación) — no todo término de giro es un negocio que "fracasó".
4. El dashboard apoya decisiones con evidencia histórica — **no es asesoría financiera ni una recomendación de inversión**.

---

## 10. Notebook (`miniproyecto_empresas.ipynb`) frente a los scripts oficiales

**Los scripts en `../../src/` son la implementación oficial y reproducible** de PYME Studio — versionados, con `requirements.txt`, un orquestador (`run_pipeline.py`) y un reporte de calidad automático. `miniproyecto_empresas.ipynb` es un **entregable pedagógico/exploratorio previo** del mismo equipo (mini-proyecto anterior al capstone actual, con créditos propios — ver `README.md`), no parte del pipeline reproducible.

**Comparación de cifras — ¿hay divergencia?**

| Métrica | Notebook | Scripts oficiales | ¿Coincide? |
|---|---:|---:|---|
| Correlación global (Spearman) | +0,0293 (p=0,066) | +0,029 (p=0,066) | ✅ Sí |
| Correlación global (Pearson) | −0,0282 (p=0,077) | −0,028 (p=0,077) | ✅ Sí |
| Comercio, por rubro (Spearman) | 0,575183 | 0,575 | ✅ Sí |
| Alojamiento/Comidas, por rubro | 0,359460 | 0,359 | ✅ Sí |
| Agricultura, por rubro | −0,268020 | −0,268 | ✅ Sí |
| Transporte, por rubro | 0,417889 | 0,418 | ✅ Sí |

**No hay divergencia** — el notebook usa la misma lógica de limpieza (`normalizar_rubro`, mismo parseo de "Recuento", mismos umbrales `MIN_EMPRESA_ANIOS`) y llega a los mismos números, redondeo aparte. Es consistente por construcción: es el borrador del mismo análisis, hecho por el mismo equipo. No se detectaron dos implementaciones divergentes del mismo cálculo — se documenta esta verificación para que quede explícito y no quede como un supuesto.

**Recomendación:** mantener el notebook como material de referencia/proceso (muestra el razonamiento paso a paso, útil para explicar el análisis a alguien nuevo), pero **cualquier cifra citada en la entrega final debe salir de `outputs/`, generado por los scripts de `src/`** — no copiarse del notebook.

---

## Trazabilidad — qué se agregó, qué NO se tocó

- `pipeline.py` y las salidas de `analisis_hito4.py` (`pyme_studio_unificado.csv`, `pyme_studio_agregado_comuna_rubro.csv`, `pyme_studio_correlacion_por_rubro.csv`) **no cambiaron de resultado** — los valores originales siguen intactos y son los que cita el README como resultado principal. `analisis_hito4.py` sí recibió una corrección defensiva menor (evita un error si algún día ningún rubro cumpliera el umbral mínimo, un caso límite que no ocurre con los datos reales) — verificado que produce exactamente los mismos números antes y después del cambio.
- Todo lo nuevo de este anexo vive en archivos **nuevos**: `pyme_studio_alcance_pyme_por_rubro.csv`, `pyme_studio_alcance_pyme_por_comuna.csv`, `pyme_studio_sensibilidad_2016.csv`, `hito4_sensibilidad_2016.png`, `pyme_studio_agregado_comuna_rubro_enriquecido.csv`, `pyme_studio_concentracion_absoluta_vs_relativa.csv`, `pyme_studio_correlacion_por_rubro_ajustada.csv`, `pyme_studio_estabilidad_subperiodos.csv`, `hito4_estabilidad_subperiodos.png`, `reporte_calidad.json`/`.md` — todos en `outputs/` (los CSV de resultados pequeños y los PNG están versionados en este repositorio; los intermedios grandes se regeneran con `python run_pipeline.py`, ver `outputs/README.md`), generados por 5 scripts nuevos (`analisis_tamano_empresas.py`, `analisis_metodologia.py`, `validar_calidad.py`, `analisis_comparaciones_multiples.py`, `analisis_subperiodos.py`).
- Los tests (`tests/`) cubren las funciones puras de estos scripts con datos sintéticos — no dependen de los archivos del SII ni verifican los valores reales citados arriba, solo el comportamiento del código (ver `docs/REPRODUCIBILIDAD.md` para la corrida real que sí generó estos números).
