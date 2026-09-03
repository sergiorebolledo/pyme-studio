# PYME Studio — Paso 7: Gantt

*Módulo 1, pág. 5 · plan a 6 semanas, con responsables de ejemplo (roles definidos en `equipo.md`)*

> Roles: **[L]** Limpieza/Datos · **[A]** Análisis · **[P]** Producto final. **Confirmado:** los nombres reales, según el mini-proyecto anterior del equipo (`miniproyecto_empresas.ipynb`) — Avelyn García en carga/limpieza/unión de fuentes **[L]**, Sergio Rebolledo en exploración estadística/correlaciones **[A]**, Ignacio Hidalgo en conclusiones/recomendaciones **[P]** — ver también la sección "Equipo" del `README.md` principal.

| Fase | S1 | S2 | S3 | S4 | S5 | S6 | Responsable | Estado real |
|---|:-:|:-:|:-:|:-:|:-:|:-:|---|---|
| 1. Definición | ██ | | | | | | Todo el equipo | ✅ Hecho |
| 2. Datos | ██ | ██ | | | | | **[L]** | ✅ Hecho |
| 3. Procesamiento | | ██ | ██ | ██ | | | **[L]** | ✅ Hecho (antes de lo previsto) |
| 4. Análisis | | | | ██ | ██ | | **[A]** | ✅ Hecho |
| 5. Producto final | | | | | ██ | ██ | **[P]** | ✅ Hecho |

**Nota real de avance (final):** los 6 hitos del proyecto están terminados — ver el estado verificable de cada uno en `tablero.md`. Las fases 2 y 3 (Datos y Procesamiento) se completaron antes de lo previsto; ese tiempo se usó para profundizar el Hito 4 (correlación por rubro, no solo un ranking) y, después de la primera entrega, para un endurecimiento metodológico adicional (sensibilidad a 2016, concentración relativa, alcance del universo pyme — ver `../metodologia/metodologia.md`).

## Detalle semana a semana

**Semana 1 — Definición + arranque de Datos**
- Cerrar el enunciado del problema y la pregunta de datos (ya redactados, revisar con el equipo).
- Decidir el tratamiento de las comunas vacías en `PUB_TG.txt` (~27% de las filas).
- *(La descarga de `Ciclo_Vida.zip` ya está hecha — ver `../../data/raw/`, así que esta fase parte adelantada).*

**Semana 2 — Datos + inicio de Procesamiento**
- Cargar `PUB_TG.txt` (cierres) y `PUB_actividades_inscritas.txt` (aperturas) en el almacén de trabajo.
- Empezar a corregir el encoding de los archivos (caracteres mal codificados).

**Semana 3-4 — Procesamiento**
- Armonizar las categorías de "Rubro" entre ambos archivos.
- Unir aperturas + cierres por año + comuna + rubro.
- Calcular la tasa de rotación/cierre por comuna y rubro.

**Semana 4-5 — Análisis**
- Identificar comunas/rubros con mayor concentración de negocios.
- Cruzar concentración con tasa de cierre.
- Detectar casos atípicos.

**Semana 5-6 — Producto final**
- Construir el dashboard/mapa por comuna y rubro.
- Documentar arquitectura y decisiones de tratamiento de datos.
- Preparar la presentación con 2-3 hallazgos concretos.

## Nota sobre el enfoque ágil (de `equipo.md`)
Este Gantt es un plan de referencia, no una camisa de fuerza — el equipo definió Kanban como formato de trabajo, así que las fechas pueden correrse si una tarea toma más de lo esperado, mientras se respete el orden de dependencias (no se puede analizar antes de tener los datos unidos y limpios).
