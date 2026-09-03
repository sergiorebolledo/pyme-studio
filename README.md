# PYME Studio

Análisis de la relación histórica entre concentración de empresas y su tasa de cierre en Chile, por comuna y rubro económico (2005–2024), con un dashboard interactivo y un mapa de Chile por comuna.

**Autores:** Ignacio Hidalgo, Sergio Ariel Rebolledo López, Avelyn García
**Contexto académico:** Samsung Innovation Campus 2026 — Capstone, Módulo 1 (Big Data Mixto)

## Resumen ejecutivo (menos de un minuto)

PYME Studio analiza 20 años de datos del SII para estudiar si una mayor concentración de empresas del mismo rubro en una comuna se relaciona con más términos de giro. El resultado muestra que no existe una regla universal: en Comercio la relación es positiva y robusta (se sostiene excluyendo el año atípico 2016, usando una métrica de concentración relativa, y tras corregir por haber probado 19 rubros a la vez), mientras que en Agricultura es negativa. Por eso, la concentración puede representar competencia en algunos sectores y especialización productiva en otros — no hay un único significado válido para todos los rubros.

## Equipo

| Autor | Rol en el proyecto |
|---|---|
| **Ignacio Hidalgo** | Redacción de conclusiones, recomendaciones y revisión de coherencia |
| **Sergio Ariel Rebolledo López** | Exploración estadística, análisis de correlaciones, y reorganización/endurecimiento metodológico del repositorio |
| **Avelyn García** | Carga, limpieza y unión de las fuentes de datos |
| Todo el equipo | Construcción y revisión de visualizaciones |

---

## 1. El problema

Se abren negocios similares (abarrotes, restaurantes, pizzerías) agrupados en una misma calle o comuna. Emprendedores e inversionistas necesitan decidir si conviene abrir un negocio de un rubro específico en una comuna determinada, pero hasta ahora no existía una fuente accesible que mostrara la concentración histórica de negocios similares por zona junto a su tasa de cierre.

**Pregunta de investigación:** ¿cuál es la concentración de empresas por rubro y comuna en Chile, y cómo se relaciona con su tasa histórica de término de giro (cierre)?

## 2. Por qué esto es Big Data

- **Volumen:** más de medio millón de registros originales combinados (183.407 filas de términos de giro + 367.428 de aperturas + el agregado nacional de empresas activas por año/comuna/rubro), antes de limpiar y unir.
- **Variedad:** ZIP, TXT, XLSB, XLSX, CSV, JSON y GeoJSON — 8 archivos fuente en 4 formatos distintos, más los derivados que produce el pipeline.
- **Veracidad:** ~27% de filas 100% vacías en un archivo fuente, separador de miles en formato chileno ("1.400" = mil cuatrocientos), categorías de rubro con nombres distintos entre fuentes, nombres de comuna inconsistentes entre el SII y la geometría del mapa — todo documentado y corregido en `src/pipeline.py` y `src/preparar_geo_comunas.py`.
- **Valor:** apoyo a decisiones empresariales (dónde abrir un negocio) y territoriales (cómo entender la actividad económica por comuna), con las limitaciones explícitas de la sección 4.
- **Velocidad:** no es central en este proyecto — se trabaja con datos históricos publicados anualmente por el SII, no con un flujo en tiempo real.

No se utilizaron tecnologías distribuidas como Spark porque el volumen podía procesarse eficientemente con Python (el pipeline completo corre en menos de un minuto). Las herramientas se eligieron según las necesidades reales del problema, tal como propone el Módulo Capstone.

## 3. Resultado principal

Mezclando todos los rubros económicos, no hay correlación entre concentración y cierre (r ≈ 0) — el efecto de sectores con dinámicas opuestas se cancela.

**Hallazgo 1 — mezclar los rubros oculta la relación.** Cuando se analizan juntos, la correlación global es aproximadamente cero porque sectores con comportamientos positivos y negativos se compensan entre sí.

**Hallazgo 2 — Comercio es el resultado más robusto.** Separando por rubro, la correlación aparece con fuerza estadística — y se sostiene bajo cada prueba de robustez aplicada:

| Prueba | Resultado |
|---|---:|
| Correlación original (Spearman) | r = 0,575 (p < 0,0001) |
| Excluyendo 2016 | r = 0,521 (sigue significativo) |
| Con concentración relativa (no solo conteo absoluto) | r = 0,322, mismo signo |
| Tras corrección por comparaciones múltiples (FDR y Bonferroni, 19 rubros) | Sigue significativo bajo ambos criterios |

**Conclusión prudente:** en Comercio, una mayor concentración territorial está asociada de manera consistente con más términos de giro registrados.

**Hallazgo 3 — la concentración no significa lo mismo en todos los sectores.**

| Rubro | Concentración absoluta | Concentración relativa |
|---|---:|---:|
| Alojamiento y servicio de comidas | r ≈ 0,359 | r ≈ −0,535 (**cambia de signo**) |
| Agricultura, ganadería, silvicultura y pesca | r ≈ −0,268 | — |

**Conclusión prudente:** en algunos sectores, una alta concentración puede representar mayor competencia; en otros puede reflejar especialización y condiciones territoriales favorables. El cambio de signo de Alojamiento/Comidas no se oculta — se documenta como parte del hallazgo, no como un error.

*(La tabla completa de los 19 rubros, el detalle de la corrección estadística y el análisis de estabilidad por subperíodo — que muestra que estas relaciones no son parejas en el tiempo — quedan en la documentación técnica, no en este resumen: ver [`docs/analisis/analisis.md`](docs/analisis/analisis.md) y [`docs/metodologia/metodologia.md`](docs/metodologia/metodologia.md).)*

![Correlación entre concentración de empresas y tasa de cierre, por rubro económico](outputs/figures/hito4_barras_correlacion_por_rubro.png)

## 4. Alcance y limitaciones (leer antes de citar el hallazgo)

- **¿Es esto realmente pymes?** El pipeline no filtra por tamaño de empresa — cuenta toda empresa registrada activa. Se verificó con la clasificación oficial del SII (Ley 20.416, por ventas anuales) que **entre 91,6% y 100% de las empresas de cada rubro son pyme** (98,9%+ en los 2 rubros del hallazgo central). El universo exacto es **"empresas registradas activas, mayoritariamente pymes"**, no "exclusivamente pymes".
- **Correlación, no causalidad.** El hallazgo es una **asociación histórica entre concentración empresarial y términos de giro registrados** — no se demuestra que una cause la otra.
- **Término de giro no equivale a quiebra ni a fracaso.** Puede ser administrativo (ver el caso de 2016 abajo) o voluntario (venta del negocio, cambio de giro, jubilación).
- **No predice el cierre de una empresa individual.** La tasa es agregada por comuna+rubro. Este proyecto **no es asesoría financiera ni una recomendación de inversión**.
- **Concentración absoluta vs. relativa.** El resultado de Comercio se sostiene con ambas métricas. El de Alojamiento/Comidas **no** — se invierte con la métrica relativa. No se descartó el hallazgo, se documentó con ambas caras.
- **Comparaciones múltiples.** Se probaron 19 rubros a la vez — se aplicó corrección FDR (Benjamini-Hochberg) y Bonferroni para no confundir significancia estadística con ruido. Los 3 rubros del hallazgo central se mantienen significativos bajo ambos criterios; 1 rubro marginal (Actividades Financieras y de Seguros) deja de serlo bajo Bonferroni.
- **Estabilidad temporal.** La correlación no es igual de fuerte en todos los subperíodos: Comercio y Alojamiento/Comidas se fortalecen en los años recientes (2016 en adelante), y Agricultura cambia de signo entre 2005-2010 (positivo) y 2016-2024 (negativo). El resultado del período completo es real, pero no asumas que se mantuvo constante durante los 20 años.

Detalle técnico completo en [`docs/metodologia/metodologia.md`](docs/metodologia/metodologia.md).

## 5. Glosario

- **Empresa activa:** contribuyente con actividad económica vigente ante el SII ese año — no distingue tamaño ni si tuvo ventas ese período.
- **Apertura / actividad inscrita:** trámite de inicio (o ampliación) de una actividad económica ante el SII.
- **Término de giro:** trámite formal de cese de actividad ante el SII. No es sinónimo de quiebra legal ni de fracaso — puede ser voluntario o administrativo.
- **Concentración absoluta:** número (conteo) de empresas activas de un rubro en una comuna.
- **Concentración relativa (participación):** qué proporción del total de empresas activas de la comuna representa ese rubro — no favorece a las comunas grandes por defecto, a diferencia de la absoluta.
- **Empresa-año:** unidad de exposición — una empresa activa durante un año. Ejemplo: si una comuna mantiene 100 empresas activas durante 10 años, acumula aproximadamente 1.000 empresa-años.
- **Tasa histórica de términos de giro:** términos de giro acumulados dividido por empresa-años acumulados, para un comuna+rubro — ver fórmula y matices en la sección 6.
- **Comuna–rubro:** la unidad de análisis de este proyecto: una combinación de comuna y rubro económico (ej. "Providencia + Comercio"), no una empresa individual.
- **Correlación de Spearman:** mide si dos variables suben y bajan juntas de forma consistente (no necesariamente en línea recta) — va de −1 (relación inversa perfecta) a +1 (relación directa perfecta), 0 = sin relación monótona.
- **Valor p:** la probabilidad de observar una correlación así de fuerte (o más) si en realidad no hubiera ninguna relación. Valores bajos (convencionalmente <0,05) sugieren que la relación observada no es solo azar.
- **Valor p ajustado:** el valor p corregido por haber hecho muchas pruebas a la vez (19 rubros) — más conservador que el valor p original, para no declarar significativo algo que solo parece así por probar muchas hipótesis.
- **Significancia estadística:** que la relación observada probablemente no es puro azar — **no** significa que sea grande, importante en la práctica, o causal.
- **Correlación frente a causalidad:** que dos variables se muevan juntas no prueba que una cause la otra — puede haber una tercera causa común, coincidencia, o la relación puede ir en sentido contrario.

## 6. La tasa histórica de términos de giro, en detalle

```
tasa histórica de términos de giro = términos de giro acumulados / empresa-años
```

- Es un **indicador agregado** por comuna+rubro — no una probabilidad individual de quiebra.
- **No sigue una cohorte** de empresas desde su apertura hasta su cierre — es un cociente de dos conteos acumulados en el mismo período, no una tasa de supervivencia.
- Un término de giro **puede ser voluntario o administrativo** (ver el caso de 2016 abajo).
- **No todo término de giro representa fracaso empresarial** — puede ser venta del negocio, cambio de giro, o jubilación del dueño.
- Se usa para **comparar comuna–rubro bajo un criterio común**, no para evaluar una empresa específica.
- **El proyecto no entrega asesoría financiera.**

## 7. El caso de 2016

Los cierres nacionales saltan de 35.931 (2015) a 214.705 (2016) — un salto de 6 veces que, sin contexto, podría leerse como una crisis económica. El equipo:

1. **Detectó el valor atípico** al graficar la serie de tiempo nacional de aperturas y cierres.
2. **Investigó su contexto** en vez de asumir una causa económica.
3. **Identificó la relación con la Ley 20.899** (2016), que le dio al SII la facultad de **declarar de oficio el término de giro** de contribuyentes inactivos que nunca habían avisado formalmente su cese de actividad — un "barrido administrativo", no una ola de quiebras.
4. **Repitió el análisis excluyendo 2016** (`src/analisis_metodologia.py` → `outputs/pyme_studio_sensibilidad_2016.csv`).
5. **Evaluó si los resultados principales se mantenían:** sí — Comercio pasa de r=0,575 a r=0,521 y Alojamiento/Comidas de r=0,359 a r=0,343, ambos siguen significativos.

## 8. Arquitectura visual

```
Fuentes del SII (ZIP, TXT, XLSB, XLSX — no versionadas, ver data/README.md)
Aperturas + términos de giro + empresas activas
                         ↓
                 Ingesta con Python (src/pipeline.py)
                         ↓
           Limpieza y normalización (rubros, comunas, formato numérico chileno)
                         ↓
       Unión por año + comuna + rubro (outer join, ausencias = 0)
                         ↓
      Validación y análisis estadístico (Spearman, FDR/Bonferroni, subperíodos)
                         ↓
        CSV analíticos + gráficos + mapa (outputs/ — solo los resultados pequeños
        se versionan; el dataset unificado y los agregados grandes NO se publican
        en GitHub, ver outputs/README.md)
                         ↓
             Dashboard (HTML autocontenido) y presentación (.pptx)
```

## 9. Estructura del repositorio

```
pyme-studio/
├── README.md
├── LICENSE
├── requirements.txt / requirements-dev.txt
├── run_pipeline.py              # corre todo el flujo en orden
├── .github/workflows/ci.yml     # integración continua
├── tests/                       # pytest, con datos sintéticos (no requiere el SII)
├── data/
│   ├── README.md                # fuentes oficiales, URLs, cómo descargar
│   ├── raw/                     # (vacío — los archivos del SII van aquí, no versionados)
│   └── reference/                # codigos_territoriales.csv (para el mapa)
├── src/                          # implementación oficial y reproducible
├── notebooks/
│   └── miniproyecto_empresas.ipynb   # material exploratorio previo, no oficial
├── outputs/
│   ├── figures/                  # gráficos finales (PNG)
│   ├── README.md
│   └── *.csv, geo_comunas.json   # resultados versionados (ver outputs/README.md)
├── dashboard/
│   └── pyme_studio_dashboard.html   # producto final
└── docs/
    ├── diccionario_datos.md, GUIA_EVALUACION.md, GUIA_EXPOSICION.md, REPRODUCIBILIDAD.md
    ├── metodologia/               # alcance, límites, robustez del análisis
    ├── analisis/                  # resultado principal, detallado
    ├── presentacion/              # presentación final (.pptx) + su generador
    └── proceso/                   # documentación del proceso de trabajo (planificación, equipo, checkpoints académicos)
```

## 10. Instalación

Requiere **Python 3.14** (versión probada localmente — ver [`docs/REPRODUCIBILIDAD.md`](docs/REPRODUCIBILIDAD.md); la integración continua además valida 3.11, 3.12 y 3.13).

```bash
git clone https://github.com/sergiorebolledo/pyme-studio.git
cd pyme-studio
pip install -r requirements.txt
```

Luego descarga los archivos de datos del SII siguiendo [`data/README.md`](data/README.md) y colócalos en `data/raw/`.

Para correr los tests (no requiere los datos del SII): `pip install -r requirements-dev.txt && pytest tests/`.

## 11. Ejecución paso a paso

```bash
python run_pipeline.py
```

Corre, en orden: el pipeline principal, validación cruzada, reporte de calidad, análisis de correlación, clasificación de tamaño de empresa, sensibilidad a 2016 y concentración relativa, corrección por comparaciones múltiples, estabilidad por subperíodo, los gráficos, y la construcción del dashboard. Se detiene en el primer paso que falle con un mensaje claro (por ejemplo, si falta un archivo en `data/raw/`).

Para regenerar solo la presentación (requiere Node.js — no se regenera automáticamente):
```bash
cd docs/presentacion/build
npm install
node build_deck.js
```

## 12. Cómo abrir el dashboard

**En línea:** [sergiorebolledo.github.io/pyme-studio](https://sergiorebolledo.github.io/pyme-studio/).

**Localmente:** abre [`dashboard/pyme_studio_dashboard.html`](dashboard/pyme_studio_dashboard.html) con doble clic en cualquier navegador — es un solo archivo autocontenido, sin dependencias externas ni conexión a internet. Funciona en computador y en móvil.

## 13. Tecnologías utilizadas

- **Python** — pandas, numpy, scipy (Spearman/Pearson, corrección FDR), matplotlib, pyxlsb (lectura de `.xlsb`), openpyxl, shapely (simplificación de geometría), pytest (tests).
- **JavaScript/HTML/CSS puro** — el dashboard es Canvas + SVG dibujado a mano, sin frameworks ni librerías externas.
- **Node.js + pptxgenjs** — generación programática de la presentación (`.pptx`).
- **GitHub Actions** — integración continua (tests + higiene del repositorio en cada push).

## 14. Estado del proyecto

Los 6 hitos del Módulo 1 están completos, más un endurecimiento metodológico posterior (alcance del universo, sensibilidad a 2016, concentración relativa, corrección por comparaciones múltiples, estabilidad por subperíodo, tests automatizados, integración continua). Detalle en [`docs/proceso/tablero.md`](docs/proceso/tablero.md).

## 15. Licencia y atribución

El código de este repositorio se distribuye bajo licencia **MIT** (ver [`LICENSE`](LICENSE)).

- Los **datos del SII** no se redistribuyen — ver `data/README.md`.
- La **geometría de comunas de Chile** proviene de [chilemapas](https://github.com/pachadotdev/chilemapas) (Mauricio "Pachá" Vargas Sepúlveda), licencia Apache 2.0. El propio paquete advierte que sus mapas son **referenciales, sin validez legal** para efectos de límites territoriales.

## Sobre el notebook

`notebooks/miniproyecto_empresas.ipynb` es material exploratorio de un mini-proyecto anterior del equipo (créditos propios dentro del notebook) — documenta el razonamiento inicial paso a paso, pero **la implementación oficial y reproducible es la de `src/`**. Las cifras de ambos coinciden (ver la comparación en `docs/metodologia/metodologia.md`), pero cualquier cifra citada debe salir de `outputs/`, generado por los scripts.

## Trabajo futuro

Fuera del alcance de esta entrega — no implementado:

- Serie temporal individual por comuna–rubro en el dashboard.
- Cruce con población comunal.
- Cruce específico con turismo (relevante para el hallazgo de Alojamiento/Comidas).
- Contexto socioeconómico adicional por comuna.
- Modelos de panel (para aprovechar la dimensión temporal de forma más rigurosa que subperíodos fijos).
- Publicación opcional de una aplicación web más allá del dashboard estático.

Ver [`docs/proceso/tablero.md`](docs/proceso/tablero.md) para el estado detallado y [`CHANGELOG.md`](CHANGELOG.md) para la evolución del proyecto.
