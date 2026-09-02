# PYME Studio — Paso 4: Factibilidad

*Checklist del Módulo 1, pág. 3, aplicado a las fuentes verificadas*

## Fuentes candidatas
1. **SII — Estadísticas de Inicio de Actividades y Término de Giro**
   https://www.sii.cl/sobre_el_sii/estadisticas_inicio_de_actividades.html
2. **SII — Empresas por rubro, subrubro y actividad** (descarga directa)
   https://www.sii.cl/estadisticas/rubro/PUB_Rub_Sub_Act.xlsx

## Checklist de factibilidad

| Criterio | Evaluación | Semáforo |
|---|---|---|
| **Disponibilidad** | Portal público del SII, sin registro, descarga directa confirmada con WebFetch. | 🟢 |
| **Formato** | Excel (.xlsb) y TXT comprimido en ZIP para el histórico; .xlsx directo para el detalle por rubro. Requiere procesar formato binario de Excel, no es CSV plano. | 🟡 |
| **Cantidad** | Series 2005-2024, cobertura nacional. Volumen alto, suficiente para un análisis de tendencias. | 🟢 |
| **Actualización** | Histórico anual, no en tiempo real — adecuado para un análisis retrospectivo de concentración/cierre. | 🟢 |
| **Calidad** | Datos oficiales, pero agregados por "zona geográfica" y rubro — **no está confirmado si baja a nivel de comuna exacta**, y no georreferencia negocios individuales. | 🟡 |
| **Restricciones** | Gratis, sin licencia restrictiva declarada. | 🟢 |

## Riesgo principal a validar
El ejemplo original de Ignacio habla de negocios "en la misma calle" — un nivel de detalle muy fino. Si el SII solo desagrega hasta zona geográfica o comuna (no dirección/calle), el equipo tendría que **ajustar el alcance del proyecto** a nivel comuna en vez de calle, o buscar una fuente complementaria con geolocalización (ej. Registro de Empresas y Sociedades, o datos abiertos de patentes municipales si existen).

---

## ✅ Validación técnica realizada (Paso 4 ejecutado)

Se descargaron y abrieron los archivos reales, no solo se revisó la página web.

**Archivo probado:** `Ciclo_Vida.zip` → https://www.sii.cl/sobre_el_sii/estadisticas/ciclo_de_vida/Ciclo_Vida.zip (descarga directa, sin registro, HTTP 200)

Contiene 3 archivos TXT separados por tabulador:

| Archivo | Filas | Columnas | Años |
|---|---|---|---|
| `PUB_TG.txt` (Término de Giro = **cierres**) | 183.408 | Año comercial, Género, Rubro, **Comuna, Provincia, Región**, Recuento | 2005-2024 |
| `PUB_actividades_inscritas.txt` (**aperturas**) | 367.429 | Año comercial, Género, **Comuna, Provincia, Región**, Categoría tributaria, Rubro, Recuento | 2005-2024 |

**Hallazgo clave:** el ojo original de `PUB_Rub_Sub_Act.xlsx` (el que se había identificado primero) **no tiene columna geográfica** — pero el ZIP de "Ciclo de Vida" sí llega a **nivel de comuna** en ambos archivos (apertura y cierre), lo que permite responder la pregunta de datos original casi tal cual, solo que a nivel comuna en vez de calle exacta.

**Caveat de calidad detectado (versión inicial):** en `PUB_TG.txt`, 49.478 de 183.408 filas (≈27%) tenían el campo Comuna vacío. *(Resuelto — ver sección "🔎 Resolución del 27%" más abajo: no era un problema de datos, era otra cosa.)*

### Checklist actualizado

| Criterio | Antes | Ahora (validado) |
|---|---|---|
| Disponibilidad | 🟢 | 🟢 confirmado, descarga directa sin registro |
| Formato | 🟡 (Excel binario) | 🟢 el ZIP trae TXT plano tabulado, mucho más fácil que el .xlsb original |
| Calidad | 🟡 (sin confirmar geografía) | 🟢 geografía confirmada a nivel comuna en el 100% de los registros reales (ver resolución abajo) |

---

## 🔎 Resolución del ~27% de filas "sin comuna"

Se investigó fila por fila qué contenían exactamente esas 49.478 filas de `PUB_TG.txt`. Resultado:

**No es un problema de datos faltantes — son filas 100% vacías (año, región, comuna, rubro y recuento, todo en blanco), casi seguro líneas de relleno al final del archivo exportado por el SII.**

| Verificación | Resultado |
|---|---|
| Filas totalmente vacías (año Y comuna vacíos) | 49.478 |
| Filas con año presente pero comuna vacía (dato real incompleto) | **0** |
| Filas completas y utilizables | 133.929 |
| Suma de "Recuento" (empresas) en las filas vacías | **0** — no representan ninguna empresa real |
| Archivo de aperturas (`PUB_actividades_inscritas.txt`, 367.428 filas) | **0 filas vacías** — el problema es exclusivo del archivo de cierres |

**Conclusión y decisión recomendada:** esto **no requiere descartar información real ni imputar nada**. Es un simple paso de limpieza: filtrar las filas donde "Año comercial" viene vacío antes de procesar. El dataset real y utilizable de cierres queda en **133.929 filas, 100% con comuna/provincia/región**, cubriendo 2005-2024 sin excepción. El "riesgo de calidad" que se había marcado en 🟡 se cierra en 🟢.

---

## 🆕 Fuente adicional encontrada (versión 1): SII — Estadísticas de Empresas por Región, Comuna y Rubro

**URL:** https://www.sii.cl/estadisticas/region/PUB_Reg_Com_Rub.xlsx

Este archivo cruza Región+Comuna+Rubro con número de empresas activas, pero solo cubre **2005-2015**, y usa una **taxonomía de rubros distinta y más antigua** (CIIU Rev.3, 19 categorías — ej. separa "Pesca" de "Agricultura") que la fuente definitiva (CIIU Rev.4, 21 categorías). No se usa como fuente principal del pipeline — **pero no se descarta: se reutiliza como validación cruzada de calidad** (ver más abajo). Se conserva en `../../data/raw/` como registro del proceso real de búsqueda.

---

## ✅ Fuente adicional encontrada (versión definitiva): SII — `PUB_COMU_RUBR.xlsb`

Se investigó si existían los años faltantes (2016-2024) en otras páginas del sitio del SII. **Sí existen** — el archivo anterior era de una sección más antigua/desactualizada del sitio; hay una sección distinta y más completa: **"Estadísticas de Empresas"** (`https://www.sii.cl/sobre_el_sii/estadisticas_de_empresas.html`), con más de 50 archivos cruzados (comuna×rubro, región×rubro, actividad×comuna, etc.).

**URL de descarga directa (verificada):** https://www.sii.cl/sobre_el_sii/empresas/PUB_COMU_RUBR.xlsb

| Criterio | Evaluación |
|---|---|
| Disponibilidad | 🟢 descarga directa, sin registro, confirmado (16 MB, HTTP 200) |
| Formato | 🟢 Excel binario (.xlsb) — se abre con la librería `pyxlsb` en Python, no con `openpyxl` |
| Cobertura geográfica | 🟢 346 comunas reales + una categoría residual "Sin Información" en solo el 0,3% de las filas (355 de 126.095) |
| **Cobertura temporal** | 🟢 **2005-2024 completo — los 20 años, confirmado fila por fila, sin cortes** |
| Calidad | 🟢 126.095 filas, estructura consistente, incluye además ventas, trabajadores por género, honorarios |

**Esto reemplaza y mejora la fuente anterior:** ya no hace falta elegir entre las 3 opciones de "qué hacer con el corte en 2015" — el dato de concentración (número de empresas activas por comuna/rubro/año) ahora cubre **exactamente el mismo período** que las aperturas y cierres (2005-2024). Las tres fuentes del SII quedan alineadas en el tiempo.

**Nota de formato:** este archivo trae muchas más columnas de las necesarias (ventas, honorarios, desglose por género) — para el análisis solo hacen falta `Año Comercial`, `Comuna`, `Rubro económico` y `Número de empresas`; el resto se puede ignorar o guardar para un análisis futuro más rico (ej. brecha de género por rubro/comuna, fuera del alcance inicial).

---

## ✅ Validación cruzada: `PUB_Reg_Com_Rub.xlsx` vs. `PUB_COMU_RUBR.xlsb`

Aunque la fuente antigua no se usa en el pipeline (taxonomía distinta, no cubre 2016-2024), **sí sirve como chequeo de calidad independiente**: el total de empresas por comuna+año no depende de qué taxonomía de rubro se use por debajo, así que si ambas fuentes del SII son consistentes, el número total debería coincidir en el período que comparten (2005-2015).

**Script:** `../../src/validar_cruzado.py` — resultado real de la corrida:

| Métrica | Resultado |
|---|---|
| Combinaciones comuna+año comparadas (normalizando tildes) | 3.619 |
| Coinciden **exactamente** | 2.025 (56,0%) |
| Diferencia promedio | **0,133%** |
| Casos con diferencia > 5% | Solo 2 (Ercilla 2015, Isla de Pascua 2011) |

**Nota sobre el cruce:** de las 3.806 combinaciones de cada archivo, ~187 no cruzaron ni siquiera después de normalizar tildes — son comunas que probablemente cambiaron de nombre, se crearon o se fusionaron entre 2005 y hoy (ej. Alto Biobío, Cholchol), no un problema de calidad de los datos.

**Conclusión:** el número de empresas activas de `PUB_COMU_RUBR.xlsb` (la fuente que usa el pipeline) es consistente con una fuente completamente independiente del mismo SII — da confianza real para el Hito 4, no solo "porque el SII lo dice".

---

## 🔎 Otras fuentes complementarias revisadas (verificadas, no aportan más que el SII)

| Fuente | Resultado de la verificación |
|---|---|
| **Sercotec — Explorador Territorial, Datos Abiertos** (https://explorador.sercotec.cl/datos-abiertos/) | Verificado en vivo: **solo tiene datos de Ferias Libres** (mercados callejeros) — ubicación, encuestas a clientes/feriantes/dirigentes. No cubre pymes en general por rubro/comuna. **No sirve para esta pregunta de investigación.** |
| **Sercotec — Reportes (Explorador Territorial)** | Existe un dashboard interactivo con acceso de invitado (`usuario: visita / clave: sercotec`), pero es sobre cobertura de programas de Sercotec, no un dataset descargable de concentración/cierre de pymes. Secundario, no prioritario. |
| **INE — Directorio Nacional de Empresas** (ArcGIS, geoine-ine-chile.opendata.arcgis.com) | Existe, pero es del **año 2017 únicamente** (dato estático, no serie histórica) — no aporta más que lo que ya cubre el SII 2005-2024. No se priorizó descargarlo. |

## Acción recomendada — siguiente paso
1. ~~Decidir el tratamiento de las filas sin comuna~~ → **Resuelto**: son filas vacías, se filtran y listo (no es una decisión de equipo, es un paso de limpieza mecánico).
2. ~~Decidir cómo tratar el corte en 2015~~ → **Resuelto**: `PUB_COMU_RUBR.xlsb` cubre 2005-2024 completo, ya no hay corte que decidir.
3. Cruzar los 3 archivos por año+comuna+rubro: aperturas (`PUB_actividades_inscritas.txt`) + cierres (`PUB_TG.txt`, ya filtrado) + empresas activas (`PUB_COMU_RUBR.xlsb`) — con las tres fuentes ya alineadas en el mismo período, esto es un join directo, sin aproximaciones.
4. Armonizar los nombres de rubro entre los 3 archivos (no usan exactamente el mismo texto/formato) — sigue siendo la única tarea de limpieza no trivial.
5. Los 3 archivos ya están descargados en `../../data/raw/` de esta carpeta — listos para usar en el Hito 2/3.

---

## Las 4 dimensiones de factibilidad (Módulo 1, pág. 3 — marco de nivel proyecto)

El checklist de arriba evalúa las *fuentes*. Este segundo marco evalúa el *proyecto completo* — es el que pide explícitamente el checkpoint "¿Nuestro proyecto es viable?".

| Dimensión | Pregunta | Evaluación para PYME Studio |
|---|---|---|
| **F1 — Datos** | ¿Tenemos acceso a los datos necesarios? | ✅ Sí — confirmado con descarga real (550k+ filas, nivel comuna, sin registro). |
| **F2 — Técnica** | ¿Podemos implementar la solución con las herramientas disponibles? | ✅ Sí — son archivos de texto plano (TXT/CSV), procesables con Python/pandas estándar, sin infraestructura especial. |
| **F3 — Temporal** | ¿Podemos tener un resultado funcional en ~2 meses? | 🟢 El principal riesgo de calendario (el 27% de filas vacías y el corte temporal de la fuente de concentración) ya está resuelto. Lo que queda es armonizar nombres de rubro entre 3 archivos — tarea acotada, no bloqueante. |
| **F4 — Alcance** | ¿Estamos resolviendo una parte concreta, no todo el problema? | ✅ Definido: "concentración y cierre de pymes por comuna y rubro a nivel nacional, período 2005-2024" (a nivel comuna, no calle/dirección — el dato no llega a ese detalle). |

**Alcance inicial sugerido (formato del checkpoint):**
> Analizar la concentración de pymes por rubro y comuna en Chile, y su relación con la tasa de término de giro, usando datos del SII 2005-2024 (no a nivel de dirección/calle individual, y sin predicción — solo análisis histórico).
