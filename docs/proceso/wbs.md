# PYME Studio — Paso 6: WBS

*Módulo 1, pág. 5*

> **Estado general (actualizado):** las 5 fases están completas y verificadas con código real — los 6 hitos del proyecto (`tablero.md`) están terminados. Este documento queda como registro de la planificación original; el estado real y verificable de cada hito vive en `tablero.md`.

1. **Definición** — ✅ Completa
   - Validar problema (hecho — ver `definicion_problema.md`)
   - Validar fuente SII (hecho — ver `factibilidad.md`)
   - Definir alcance final: análisis a nivel comuna (hecho y validado con cruce independiente, no solo supuesto)

2. **Datos** — ✅ Completa
   - Descargar `Ciclo_Vida.zip` (aperturas + cierres, 2005-2024) — hecho, ver `../../data/raw/`
   - Descargar `PUB_COMU_RUBR.xlsb` (empresas activas por comuna/rubro/año, 2005-2024 completo) — hecho, ver `../../data/raw/`
   - Filtrar las filas 100% vacías de `PUB_TG.txt` (~27% del archivo) — hecho, en `../../src/pipeline.py`
   - Validación cruzada de calidad contra `PUB_Reg_Com_Rub.xlsx` — hecho, en `../../src/validar_cruzado.py` (0,13% de diferencia promedio)
   - Cargar los 3 archivos en el pipeline — hecho, usando `pandas` + `pyxlsb`

3. **Procesamiento** — ✅ Completa
   - Decodificar correctamente el encoding de los TXT (latin-1) y exportar en UTF-8 — hecho
   - Corregir el formato numérico chileno de "Recuento" (punto como separador de miles) — hecho, bug real encontrado y corregido
   - Armonizar categorías de "Rubro" entre los 3 archivos (normalización: quitar código de letra, tildes, mayúsculas) — hecho, 21 categorías cruzan 1:1
   - Unir aperturas + cierres + empresas activas por año + comuna + rubro — hecho
   - Calcular `tasa_cierre` por comuna y rubro — hecho
   - **Resultado:** `../../outputs/pyme_studio_unificado.csv`, 126.566 filas, 2005-2024, 348 comunas, 21 rubros

4. **Análisis** — ✅ Completa (Hito 4)
   - Identificar comunas/rubros con mayor concentración de negocios — hecho
   - Cruzar concentración con tasa de cierre — hecho, correlación real (global y por rubro, con significancia estadística) en `../analisis/analisis.md`
   - Detectar casos atípicos (rubros que crecen sin cerrar vs. rubros saturados) — hecho
   - Endurecimiento posterior: sensibilidad a 2016, concentración absoluta vs. relativa, alcance del universo pyme — `../metodologia/metodologia.md`

5. **Producto final** — ✅ Completa (Hitos 5 y 6)
   - Dashboard por comuna/rubro con concentración y tasa de cierre — hecho, `../../dashboard/pyme_studio_dashboard.html` (entregable oficial, con mapa)
   - Documentar la arquitectura y las decisiones de tratamiento de datos — hecho, ver `producto_dashboard.md` y `../metodologia/metodologia.md`
   - Preparar presentación con hallazgos concretos — hecho, `../presentacion/PYME_Studio_Presentacion.pptx` (entregable oficial)
