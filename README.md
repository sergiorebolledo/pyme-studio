# PYME Studio

Análisis de la relación histórica entre concentración de empresas y su tasa de cierre en Chile, por comuna y rubro económico (2005–2024), con un dashboard interactivo y un mapa de Chile por comuna.

**Autores:** Ignacio Hidalgo, Sergio Ariel Rebolledo López, Avelyn García
**Contexto académico:** Samsung Innovation Campus 2026 — Capstone, Módulo 1 (Big Data Mixto)

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

## 2. Resultado principal

Mezclando todos los rubros económicos, no hay correlación entre concentración y cierre (r ≈ 0) — el efecto de sectores con dinámicas opuestas se cancela. Separando por rubro, sí aparece con fuerza estadística en los dos sectores que motivaron la pregunta original:

| Rubro | Correlación (Spearman) | Comunas | Significancia |
|---|---:|---:|---|
| Comercio al por mayor y al por menor | r = 0,575 | 342 | p < 0,0001 |
| Alojamiento y servicio de comidas | r = 0,359 | 344 | p < 0,0001 |
| Agricultura, ganadería, silvicultura y pesca | r = −0,268 (al revés) | 341 | p < 0,0001 |

![Correlación entre concentración de empresas y tasa de cierre, por rubro económico](outputs/figures/hito4_barras_correlacion_por_rubro.png)

Detalle completo, con los 19 rubros analizados, en [`docs/analisis/analisis.md`](docs/analisis/analisis.md).

## 3. Alcance y limitaciones (leer antes de citar el hallazgo)

- **¿Es esto realmente pymes?** El pipeline no filtra por tamaño de empresa — cuenta toda empresa registrada activa. Se verificó con la clasificación oficial del SII (Ley 20.416, por ventas anuales) que **entre 91,6% y 100% de las empresas de cada rubro son pyme** (98,9%+ en los 2 rubros del hallazgo central). El universo exacto es **"empresas registradas activas, mayoritariamente pymes"**, no "exclusivamente pymes".
- **Correlación, no causalidad.** El hallazgo es una **asociación histórica entre concentración empresarial y términos de giro registrados** — no se demuestra que una cause la otra. Un término de giro puede ser administrativo (ver el salto de 2016 más abajo) o voluntario (venta del negocio, cambio de giro, jubilación) — no es sinónimo de "fracaso" ni de quiebra legal.
- **No predice el cierre de una empresa individual.** La tasa es agregada por comuna+rubro. Este proyecto **no es asesoría financiera ni una recomendación de inversión**.
- **Concentración absoluta vs. relativa.** El resultado de Comercio se sostiene tanto midiendo concentración por conteo absoluto como por participación relativa dentro de la comuna. El de Alojamiento/Comidas **no** — se invierte con la métrica relativa (r=0,359 → r=−0,535). No se descartó el hallazgo, se documentó con ambas caras.
- **Sensibilidad al año 2016.** Los cierres nacionales saltan de 35.931 (2015) a 214.705 (2016) — no es una crisis económica, es la Ley 20.899 dándole al SII la facultad de declarar de oficio el término de giro de contribuyentes inactivos. Excluyendo 2016, Comercio pasa de r=0,575 a r=0,521 y Alojamiento/Comidas de r=0,359 a r=0,343 — ambos siguen significativos.

Detalle técnico completo de los 4 puntos en [`docs/metodologia/metodologia.md`](docs/metodologia/metodologia.md).

## 4. Fuentes oficiales

| Fuente | Qué aporta | Redistribución |
|---|---|---|
| [Servicio de Impuestos Internos (SII) de Chile](https://www.sii.cl/sobre_el_sii/estadisticas_de_empresas.html) | Aperturas, cierres y empresas activas por año/comuna/rubro (2005–2024); clasificación oficial de tamaño de empresa | No incluida en este repositorio — [`data/README.md`](data/README.md) documenta cómo descargarla |
| [chilemapas](https://github.com/pachadotdev/chilemapas) (Mauricio "Pachá" Vargas Sepúlveda) | Geometría de las 345 comunas de Chile para el mapa del dashboard | Apache 2.0 — geometría ya incluida y procesada en `outputs/geo_comunas.json` |

Los datos del SII no se redistribuyen en este repositorio porque sus [términos de uso](https://www.sii.cl/sobre_el_sii/terminos_sitio_web.html) no autorizan de forma clara la reproducción de estos archivos en otros sitios. Ver `data/README.md` para la URL oficial de cada archivo.

## 5. Arquitectura del flujo de datos

```
data/raw/ (SII, no versionado)
    │
    ▼
src/pipeline.py ──────────► outputs/pyme_studio_unificado.csv
    │
    ├─► src/validar_cruzado.py, src/validar_calidad.py   (control de calidad)
    │
    ▼
src/analisis_hito4.py ────► outputs/pyme_studio_correlacion_por_rubro.csv
    │
    ├─► src/analisis_tamano_empresas.py   (alcance del universo pyme)
    ├─► src/analisis_metodologia.py       (sensibilidad 2016, concentración relativa)
    ├─► src/graficar_hito4.py, graficar_hito4_extra.py   (outputs/figures/*.png)
    │
    ▼
src/construir_dashboard.py ► dashboard/pyme_studio_dashboard.html
```

`run_pipeline.py`, en la raíz, ejecuta todas estas etapas en orden y se detiene con un mensaje claro si alguna falla.

## 6. Estructura del repositorio

```
pyme-studio/
├── README.md
├── LICENSE
├── requirements.txt
├── run_pipeline.py              # corre todo el flujo en orden
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
    ├── metodologia/               # alcance, límites, robustez del análisis
    ├── analisis/                  # resultado principal, detallado
    ├── presentacion/              # presentación final (.pptx) + su generador
    └── proceso/                   # documentación del proceso de trabajo (planificación, equipo, checkpoints académicos)
```

## 7. Instalación

Requiere **Python 3.11+** (probado en 3.11–3.14).

```bash
git clone https://github.com/sergiorebolledo/pyme-studio.git
cd pyme-studio
pip install -r requirements.txt
```

Luego descarga los archivos de datos del SII siguiendo [`data/README.md`](data/README.md) y colócalos en `data/raw/`.

## 8. Ejecución paso a paso

```bash
python run_pipeline.py
```

Corre, en orden: el pipeline principal, validación cruzada, reporte de calidad, análisis de correlación, clasificación de tamaño de empresa, sensibilidad a 2016 y concentración relativa, los gráficos, y la construcción del dashboard. Se detiene en el primer paso que falle con un mensaje claro (por ejemplo, si falta un archivo en `data/raw/`).

Para regenerar solo la presentación (requiere Node.js — no se regenera automáticamente):
```bash
cd docs/presentacion/build
npm install
node build_deck.js
```

## 9. Cómo abrir el dashboard

**En línea:** [sergiorebolledo.github.io/pyme-studio](https://sergiorebolledo.github.io/pyme-studio/).

**Localmente:** abre [`dashboard/pyme_studio_dashboard.html`](dashboard/pyme_studio_dashboard.html) con doble clic en cualquier navegador — es un solo archivo autocontenido, sin dependencias externas ni conexión a internet.

## 10. Tecnologías utilizadas

- **Python** — pandas, numpy, scipy (correlación de Spearman/Pearson), matplotlib, pyxlsb (lectura de `.xlsb`), openpyxl, shapely (simplificación de geometría).
- **JavaScript/HTML/CSS puro** — el dashboard es Canvas + SVG dibujado a mano, sin frameworks ni librerías externas.
- **Node.js + pptxgenjs** — generación programática de la presentación (`.pptx`).

## 11. Estado del proyecto

Los 6 hitos del Módulo 1 están completos (problema y fuentes validados, datos obtenidos, pipeline funcional, análisis con significancia estadística, dashboard interactivo, presentación final), más un endurecimiento metodológico posterior (alcance del universo, sensibilidad a 2016, concentración relativa, precisión conceptual, control de calidad automatizado). Detalle en [`docs/proceso/tablero.md`](docs/proceso/tablero.md).

Los créditos del equipo académico ya están completos en la portada de la presentación (ver [`docs/presentacion/presentacion.md`](docs/presentacion/presentacion.md)).

## 12. Licencia y atribución

El código de este repositorio se distribuye bajo licencia **MIT** (ver [`LICENSE`](LICENSE)).

- Los **datos del SII** no se redistribuyen — ver `data/README.md`.
- La **geometría de comunas de Chile** proviene de [chilemapas](https://github.com/pachadotdev/chilemapas) (Mauricio "Pachá" Vargas Sepúlveda), licencia Apache 2.0. El propio paquete advierte que sus mapas son **referenciales, sin validez legal** para efectos de límites territoriales.

## Sobre el notebook

`notebooks/miniproyecto_empresas.ipynb` es material exploratorio de un mini-proyecto anterior del equipo (créditos propios dentro del notebook) — documenta el razonamiento inicial paso a paso, pero **la implementación oficial y reproducible es la de `src/`**. Las cifras de ambos coinciden (ver la comparación en `docs/metodologia/metodologia.md`), pero cualquier cifra citada debe salir de `outputs/`, generado por los scripts.
