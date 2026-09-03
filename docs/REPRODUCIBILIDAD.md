# Evidencia de reproducibilidad

Registro de la última ejecución completa verificada del pipeline, para que quede documentado qué se corrió realmente (no solo lo que debería funcionar en teoría).

## Última ejecución completa

- **Fecha:** 2026-09-03
- **Sistema operativo:** Windows 10 (build 19045), vía Git Bash (MINGW64)
- **Python:** 3.14.6
- **Comando:** `python run_pipeline.py` (sin `--regenerar-geo`, reutilizando `outputs/geo_comunas.json` ya versionado)

### Versiones de dependencias efectivamente usadas

| Paquete | Versión |
|---|---|
| pandas | 3.0.5 |
| numpy | 2.5.2 |
| scipy | 1.18.0 |
| matplotlib | 3.11.1 |
| shapely | 2.1.2 |
| openpyxl | 3.1.5 |
| pytest | 9.1.1 |

Todas dentro de los rangos declarados en `requirements.txt`/`requirements-dev.txt`. La integración continua (`.github/workflows/ci.yml`) valida además Python 3.11, 3.12 y 3.13 en cada push — esas versiones no se probaron localmente en esta ejecución, solo en CI.

### Etapas ejecutadas y resultado

| # | Etapa | Script | Resultado |
|---|---|---|---|
| 1 | Pipeline principal | `pipeline.py` | ✅ OK |
| 2 | Validación cruzada de calidad | `validar_cruzado.py` | ✅ OK |
| 3 | Reporte de calidad reproducible | `validar_calidad.py` | ✅ OK — 16 chequeos, 0 bloqueantes, 2 advertencias (ver abajo) |
| 4 | Análisis principal | `analisis_hito4.py` | ✅ OK |
| 5 | Alcance del universo pyme | `analisis_tamano_empresas.py` | ✅ OK |
| 6 | Sensibilidad a 2016 y concentración relativa | `analisis_metodologia.py` | ✅ OK |
| 7 | Corrección por comparaciones múltiples | `analisis_comparaciones_multiples.py` | ✅ OK |
| 8 | Estabilidad por subperíodo | `analisis_subperiodos.py` | ✅ OK |
| 9 | Gráfico de dispersión | `graficar_hito4.py` | ✅ OK |
| 10 | Gráficos de barras/serie/boxplot | `graficar_hito4_extra.py` | ✅ OK |
| 11 | Geometría del mapa | `preparar_geo_comunas.py` | **Omitida** — se reutilizó `outputs/geo_comunas.json`, ya versionado (no cambió la fuente geográfica) |
| 12 | Construcción del dashboard | `construir_dashboard.py` | ✅ OK |

**No ejecutada:** regeneración de la presentación (`docs/presentacion/build/build_deck.js`) — se hizo por separado con Node.js, no forma parte de `run_pipeline.py` por diseño (ver `docs/presentacion/presentacion.md`).

### Archivos de entrada usados

Los 8 archivos oficiales del SII, ya descargados localmente siguiendo `data/README.md` (no se volvieron a descargar para esta corrida — ya estaban disponibles). Verificados por `validar_calidad.py`:

- `Ciclo_Vida.zip` — 7.989.684 bytes, contiene `PUB_TG.txt` y `PUB_actividades_inscritas.txt`
- `PUB_COMU_RUBR.xlsb` — 16.086.175 bytes
- Los 4 archivos de clasificación de tamaño (`PUB_TRAM5_*`, `PUB_*_TRTRAB`) y `PUB_Reg_Com_Rub.xlsx` — usados sin incidencias por `analisis_tamano_empresas.py` y `validar_cruzado.py`

### Resultado del dataset unificado (sin filtrar)

| Métrica | Valor |
|---|---|
| Filas | 126.566 |
| Período | 2005–2024 |
| Comunas distintas | 348 |
| Rubros distintos | 21 |
| Combinaciones comuna+rubro (sin filtrar) | 7.064 |

### Muestra usada en el análisis por rubro (≥50 empresa-años, ≥30 comunas — la que cita el dashboard y la presentación)

| Métrica | Valor |
|---|---|
| Comunas en la muestra | 345 |
| Combinaciones comuna×rubro analizadas | 5.263 |
| Empresa-años considerados | 22.496.515 |
| % empresas pyme del universo (mín. por rubro) | 91,64% |

*Nota sobre la diferencia con la tabla anterior: "comunas distintas" (348) cuenta todas las que aparecen en el dataset crudo; "comunas en la muestra" (345) son las que además tienen ≥50 empresa-años en algún rubro analizado — 3 comunas quedan fuera del análisis por rubro por falta de exposición, aunque sí aparecen en el dataset base.*

### Reporte de calidad (`outputs/reporte_calidad.md`, no versionado — se regenera en cada corrida)

16 chequeos, **0 bloqueantes**, 2 advertencias no bloqueantes:
- 125 filas (0,10%) con `tasa_cierre > 100%` — artefacto esperado en celdas con muy pocas empresas (ver `docs/metodologia/metodologia.md`, sección 6).
- 204 combinaciones año+comuna+rubro con `tasa_cierre > 50%` (con exposición no trivial) — para revisión manual, no es un error automático.

### Archivos generados

Los 5 CSV de resultados + 6 PNG en `outputs/figures/` + `outputs/geo_comunas.json` (versionados, ver `outputs/README.md`) más los intermedios grandes no versionados (`pyme_studio_unificado.csv`, `pyme_studio_agregado_comuna_rubro*.csv`, `dashboard_data.json`, `reporte_calidad.*`).

### Confirmación de regeneración del dashboard

`dashboard/pyme_studio_dashboard.html` fue regenerado por `construir_dashboard.py` en esta corrida — el bloque de datos embebido (`<script id="dashboard-data">`) se reinyectó completo. **No se ejecutó una revisión visual completa en navegador en esta corrida puntual** — la última revisión visual completa (carga, selectores, mapa, modo claro/oscuro) está documentada por separado en este mismo trabajo de endurecimiento (ver el informe final de esta sesión). Esto se declara explícitamente para no afirmar una prueba que no se hizo en este paso.

### Tests

`python -m pytest tests/ -v` → **59 passed**, 0 failed, en Python 3.14.6 local. Ver `.github/workflows/ci.yml` para la matriz de versiones en CI.

### Lo que esta ejecución NO cubrió (y por qué)

- **Regeneración de `docs/presentacion/PYME_Studio_Presentacion.pptx`**: por diseño, `run_pipeline.py` no la incluye (depende de Node.js). Se regeneró aparte cuando cambiaron los datos que muestra — ver el commit correspondiente.
- **Ejecución de la CI en GitHub Actions**: el workflow (`.github/workflows/ci.yml`) fue validado localmente (sintaxis YAML, y cada chequeo de higiene reproducido manualmente contra este repositorio) pero no se ha ejecutado todavía en la infraestructura de GitHub Actions, porque eso requiere un push — no autorizado en esta sesión de trabajo.
