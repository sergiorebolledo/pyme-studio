# PYME Studio — Respuestas a los Checkpoints del Módulo 1

*SIC 2026 · Big Data Mixto · Documento de evidencia para entregar*

Este documento responde, en orden, los 5 checkpoints que trae el módulo (uno por página). Cada respuesta está respaldada por un archivo de esta carpeta — se referencia entre paréntesis.

---

## Checkpoint 1 (pág. 1) — "Nuestro proyecto"

**1. ¿Qué problema o área les gustaría abordar?**
La concentración comercial y la tasa de cierre de pequeñas y medianas empresas (pymes) en Chile — por ejemplo, negocios similares (abarrotes, comida rápida) que se agrupan en una misma zona, a veces por decisiones de inversión poco fundamentadas.

**2. ¿Qué datos creen que podrían utilizar?**
Estadísticas oficiales del Servicio de Impuestos Internos (SII): inicio de actividades, término de giro (cierres) y número de empresas activas, todas desagregadas por año, comuna y rubro.

**3. ¿Qué resultado sería útil obtener a partir de esos datos?**
Un mapa o dashboard que muestre qué combinaciones de comuna+rubro están sobresaturadas y/o tienen una tasa de cierre históricamente alta, para apoyar decisiones de inversión con evidencia en vez de intuición.

**4. ¿Qué característica podría justificar un enfoque Big Data?**
**Volumen** (más de 550.000 registros combinados entre los archivos de aperturas y cierres) y **Variedad** (3 fuentes del SII con estructuras y periodos distintos que hay que integrar: 2005-2024 en dos de ellas, 2005-2015 en la tercera).

*(Fuente: `definicion_problema.md`, `factibilidad.md`)*

---

## Checkpoint 2 (pág. 2) — "Definamos nuestro problema"

**1. ¿Quién es el usuario, organización o actor relacionado con el problema?**
Emprendedores e inversionistas que evalúan dónde abrir un negocio; también instituciones públicas o investigadores interesados en fenómenos de concentración comercial.

**2. ¿Qué necesidad o dificultad tiene actualmente?**
No cuentan con una forma simple de saber si una comuna/rubro ya está saturado de negocios similares, ni cuál es su historial de cierres — deciden con intuición, no con evidencia.

**3. ¿Qué evidencia tienen de que el problema existe?**
Observación directa: es común encontrar varios negocios del mismo tipo (sushi, pizzerías, abarrotes) en una misma calle o zona. La evidencia cuantitativa se obtiene de los datos oficiales del SII, ya descargados y validados.

**4. Frase del problema:**
> Los emprendedores e inversionistas necesitan decidir si conviene abrir un negocio de un rubro específico en una comuna determinada, **porque** una mala decisión de ubicación puede llevar al cierre temprano del negocio, y hoy no pueden hacerlo con evidencia porque no existe una fuente accesible que muestre la concentración y la tasa histórica de cierre de negocios similares por zona.

**5. Pregunta del proyecto (respondible con datos):**
> ¿Cuál es la concentración de pymes por rubro y comuna, y cómo se relaciona con su tasa histórica de término de giro (cierre)?

**6. ¿Qué queda fuera del alcance?**
- Nivel de calle/dirección exacta — los datos del SII llegan hasta **comuna**, no a nivel de calle individual.
- Predicción en tiempo real — el proyecto es un análisis **histórico** (2005-2024), no un modelo predictivo.

*(Fuente: `definicion_problema.md`)*

---

## Checkpoint 3 (pág. 3) — "¿Nuestro proyecto es viable?"

**1. Datos necesarios:**
Aperturas, cierres (término de giro) y empresas activas, cada uno por año + comuna + rubro.

**2. Fuentes disponibles (verificadas, con acceso confirmado):**
- SII — Ciclo de Vida (aperturas + cierres), 2005-2024: `https://www.sii.cl/sobre_el_sii/estadisticas/ciclo_de_vida/Ciclo_Vida.zip`
- SII — Empresas por Región, Comuna y Rubro (activas), 2005-2015: `https://www.sii.cl/estadisticas/region/PUB_Reg_Com_Rub.xlsx`
- Los 3 archivos ya están descargados en `../../data/raw/`.

**3. Principal riesgo:**
Que las tres fuentes usan categorías de "rubro" ligeramente distintas entre sí (nombres/formato no idénticos) — hay que armonizarlas antes de poder cruzarlas. *(El riesgo de cobertura temporal que existía antes — una fuente solo llegaba a 2015 — ya se resolvió: se encontró `PUB_COMU_RUBR.xlsb`, que cubre 2005-2024 completo.)*

**4. Alcance:**
Concentración y tasa de cierre de pymes por comuna y rubro, a nivel nacional, período 2005-2024 (a nivel comuna, no calle; análisis histórico, no predicción).

**5. Arquitectura V0:**
`Fuentes (3 archivos SII) → Ingesta (descarga batch, ya realizada) → Almacenamiento (tabla de trabajo, ej. SQLite/Parquet) → Procesamiento (limpieza, armonización de rubros, unión) → Análisis (tasas de concentración/cierre, correlación) → Consumo (dashboard/mapa)`

**6. Responsables iniciales:**
Coordinación / Datos / Procesamiento y análisis / Visualización y comunicación — un responsable por área (ver `equipo.md`).

*(Fuente: `factibilidad.md`, `equipo.md`)*

---

## Checkpoint 4 (pág. 4) — "¿Cómo trabajará nuestro equipo?"

**1. Enfoque elegido:** Kanban.

**2. Por qué se adapta a este equipo:** El trabajo es mayormente de tipo ETL (extraer-transformar-cargar) con tareas bastante independientes entre sí. Además hay decisiones aún abiertas (ej. cómo tratar el corte de 2015 en una de las fuentes) que se resuelven mejor con un flujo continuo que con sprints rígidos.

**3. Frecuencia de revisión:** Semanal, como equipo completo (más revisiones puntuales entre quienes comparten una tarea).

**4. Cómo identifican tareas pendientes, en desarrollo y terminadas:** Tablero con columnas **Pendiente → En progreso → En revisión → Terminado** (ver `tablero.md`).

**5. Qué harán si una decisión inicial deja de ser viable:** Ajustar el alcance en vez de forzar la decisión original — por ejemplo, si armonizar las categorías de rubro entre las 3 fuentes toma demasiado tiempo, se simplifica a categorías más generales (rubros a 1 dígito en vez del detalle completo).

*(Fuente: `equipo.md`)*

---

## Checkpoint 5 (pág. 5) — "Primer plan del Capstone"

**1. WBS inicial:** Construida — 5 fases (Definición, Datos, Procesamiento, Análisis, Producto final) con tareas específicas de PYME Studio (`wbs.md`).

**2. Hitos (4 a 6, comprobables):** 6 hitos definidos, cada uno con un criterio de cumplimiento verificable, no vago (`tablero.md`):
1. Problema y fuentes de datos validados
2. Datos obtenidos y almacenados
3. Pipeline de procesamiento funcional
4. Primer análisis completo
5. Producto o visualización funcional
6. Integración y presentación final

**3. Responsables:** Asignados por rol (Coordinación / Datos / Procesamiento y análisis / Visualización), no por tarea individual — ver `equipo.md`.

**4. Representación del plan:** Gantt de 6 semanas (`gantt.md`) + tablero Kanban de 5 columnas (`tablero.md`).

**5. Próximo paso concreto que hará el equipo después de esta clase:**
*(Actualizado — este documento describe el estado al momento de responder el checkpoint; los 6 hitos ya están completos, ver `tablero.md` para el estado final verificable.)* Se construyó y probó `../../src/pipeline.py`, que filtra las filas vacías, armoniza los rubros entre las 3 fuentes y las une en `../../outputs/pyme_studio_unificado.csv` (126.566 filas). Además se validó la calidad cruzando los totales contra una fuente independiente del SII (`../../src/validar_cruzado.py`, 0,13% de diferencia promedio). Ese fue el paso que siguió al Hito 3 en su momento; desde entonces se completaron el Hito 4 (`../analisis/analisis.md`), el Hito 5 (`../../dashboard/pyme_studio_dashboard.html`) y el Hito 6 (`../presentacion/PYME_Studio_Presentacion.pptx`), más un endurecimiento metodológico posterior (`../metodologia/metodologia.md`).

*(Fuente: `wbs.md`, `gantt.md`, `tablero.md`)*
