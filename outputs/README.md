# Outputs

Resultados del análisis. Lo que ves aquí en el repositorio es un subconjunto deliberado — no todo lo que produce el pipeline.

## Lo que está versionado en este repositorio

- **`figures/`** — los 5 gráficos finales usados en `docs/analisis/analisis.md`, el dashboard y la presentación.
- **`pyme_studio_correlacion_por_rubro.csv`** — correlación de Spearman (concentración ~ tasa de cierre) por rubro económico, 19 filas.
- **`pyme_studio_sensibilidad_2016.csv`** — la misma correlación calculada con y sin el año 2016, para comprobar que el hallazgo no depende de ese año atípico.
- **`pyme_studio_concentracion_absoluta_vs_relativa.csv`** — comparación entre medir concentración como conteo absoluto vs. como participación relativa dentro de la comuna.
- **`pyme_studio_alcance_pyme_por_rubro.csv`**, **`pyme_studio_alcance_pyme_por_comuna.csv`** — qué porcentaje del universo analizado es efectivamente pyme, según la clasificación oficial (Ley 20.416).
- **`geo_comunas.json`** — geometría simplificada de las 345 comunas de Chile (derivada de [chilemapas](https://github.com/pachadotdev/chilemapas), Apache 2.0), para el mapa del dashboard.

Estos son resultados propios (coeficientes, porcentajes, geometría procesada) — no una copia de los archivos fuente del SII.

## Lo que NO está versionado (se regenera con `python run_pipeline.py`)

- `pyme_studio_unificado.csv` y los `pyme_studio_agregado_comuna_rubro*.csv` — son las cifras del SII reagrupadas por año/comuna/rubro, muy cercanas a una redistribución tabular de los datos fuente (ver `data/README.md` sobre por qué no se redistribuyen los datos originales del SII).
- `dashboard_data.json` — archivo intermedio; una vez que `construir_dashboard.py` lo usa, sus datos ya quedan embebidos directamente en `dashboard/pyme_studio_dashboard.html`.
- `reporte_calidad.json` / `.md` — se regenera en cada corrida del pipeline; su contenido depende de la corrida local (rutas de archivos, tamaños en bytes) así que no tiene sentido versionarlo.

## Cómo regenerar todo

```bash
python run_pipeline.py
```

Ver el `README.md` principal del repositorio para los requisitos previos (dependencias, archivos de `data/raw/`).
