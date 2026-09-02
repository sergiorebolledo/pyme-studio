# PYME Studio — Paso 5: Organización del equipo

*Módulo 1, pág. 4*

## Enfoque recomendado: Ágil (Kanban o Scrum corto)

### Decisiones que estaban abiertas — actualización de estado
- ~~Cómo tratar el ~27% de filas sin comuna~~ → **Resuelto**: eran filas vacías, se filtran (ver `factibilidad.md`).
- ~~Nivel de granularidad final~~ → **Resuelto**: comuna funciona bien — validado con un cruce independiente contra otra fuente del SII (0,13% de diferencia promedio, ver `factibilidad.md`).
- ~~Qué visualización final comunica mejor la relación concentración↔cierre~~ → **Resuelto**: mapa + ranking + dispersión, los tres juntos en el mismo dashboard (`../../dashboard/pyme_studio_dashboard.html`, entregable oficial — ver `producto_dashboard.md`).

Las 3 decisiones se resolvieron explorando los datos reales (no de forma teórica), lo que confirma que el enfoque ágil elegido fue el correcto para este proyecto.

### Formato sugerido
**Kanban** (metodología) funciona bien aquí porque el trabajo es mayormente de tipo ETL (extraer-transformar-cargar) con tareas bastante independientes entre sí (armonizar comuna, calcular tasas, construir visualización) — un flujo continuo **Pendiente → En progreso → En revisión → Terminado** es suficiente, sin necesidad de sprints rígidos.

*Recordatorio del módulo: Kanban es la metodología; el tablero de Trello/Notion es la herramienta que la representa — no son lo mismo.*

### Roles sugeridos (usando las 4 categorías del Módulo 1, pág. 3)
- **Coordinación** — seguimiento del proyecto, integra el trabajo del resto y organiza las reuniones de avance.
- **Datos** — búsqueda y descarga de las fuentes SII (✅ hecho: 4 archivos en `../../data/raw/`), validación cruzada de calidad (✅ hecho: `../../src/validar_cruzado.py`).
- **Procesamiento y análisis** — armonización de rubros, unión de las 3 fuentes (✅ hecho: `../../src/pipeline.py`), cálculo de tasas de rotación y correlación (✅ hecho — Hito 4, `../analisis/analisis.md`).
- **Visualización y comunicación** — dashboard/mapa final, documentación de la arquitectura, presentación (✅ hecho — Hitos 5 y 6, `../../dashboard/pyme_studio_dashboard.html` y `../presentacion/PYME_Studio_Presentacion.pptx`, entregables oficiales).

En un equipo pequeño, una persona puede cubrir más de un rol — lo importante es que cada responsabilidad tenga un dueño claro, no que haya un cargo por persona.
