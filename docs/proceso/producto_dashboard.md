# Producto: el dashboard

*Archivo: [`dashboard/pyme_studio_dashboard.html`](../../dashboard/pyme_studio_dashboard.html) — autocontenido, sin dependencias externas, se abre con doble clic en cualquier navegador.*

## Qué es
Un dashboard interactivo de una sola página que reúne todo el trabajo de análisis en un formato explorable, no solo leíble. Pensado para presentar el proyecto sin tener que alternar entre CSV, gráficos sueltos y documentos.

## Cómo está construido
- **Sin librerías externas**: los gráficos (barras, serie de tiempo, dispersión, mapa) están dibujados a mano con Canvas + JavaScript plano — el archivo funciona sin conexión a internet y sin instalar nada.
- **Datos embebidos**: los resultados del análisis y la geometría del mapa quedan incrustados dentro del propio HTML, así que es un solo archivo portable (~1,3 MB).
- **Modo claro/oscuro**: se adapta automáticamente a la configuración del sistema del que lo abre.

## Sección 4 — mapa de Chile por comuna
- **Geometría real de las 345 comunas continentales**, tomada de [chilemapas](https://github.com/pachadotdev/chilemapas) (licencia Apache 2.0), simplificada con Shapely (tolerancia adaptativa por región — las costas fragmentadas del sur, ej. Aysén y Magallanes, necesitan más simplificación para no disparar el tamaño del archivo) y proyectada a un plano con corrección por coseno de latitud para no deformar la silueta de Chile.
- **Cruce de nombres SII ↔ chilemapas**: ambas fuentes nombran comunas de forma distinta (con/sin tilde, variantes de escritura). Se normalizan ambos lados (sin tildes, mayúsculas) y se corrige un puñado de variantes conocidas (ej. "Titil"→"Tiltil", "Marchigüe"→"Marchihue") con un diccionario de alias en `construir_dashboard.py`. Resultado: las 345 comunas del mapa encuentran su contraparte en los datos del SII, sin excepciones.
- **Selector de métrica**: tasa de cierre (escala verde→rojo, coherente con el semáforo de riesgo que ya usan las tablas de ranking) o concentración de empresas activas (escala secuencial gris→azul cobalto).
- **Sincronizado con la sección 3**: el mapa siempre muestra el mismo rubro que el selector de "Detalle por rubro" — cambiarlo ahí (o hacer clic en una barra) actualiza el mapa sin recargar la página.
- **Comunas sin datos suficientes** (menos de 50 años-empresa de historia para ese rubro) quedan en gris, con nota explícita — no se ocultan ni se fuerza un color engañoso.
- **Tooltip por comuna** al pasar el cursor, con el mismo patrón visual que los otros gráficos del dashboard.

## Qué se puede hacer en el dashboard
0. **El problema y por qué importa** — justo bajo el título, antes que cualquier gráfico: el enunciado del problema (ver [`definicion_problema.md`](definicion_problema.md)) y el contexto de por qué la observación original (negocios similares agrupados en una misma calle) merece evidencia, no solo intuición.
1. **Franja de hallazgo central** justo debajo — el resumen ejecutivo de la respuesta, para quien solo tenga 10 segundos.
2. **KPIs arriba**: cifras clave de un vistazo, cada una con una línea de contexto (ej. "todos los rubros mezclados — no significativa").
3. **Gráfico de barras** (los 19 rubros ordenados por correlación), con leyenda de colores explícita. Al pasar el cursor se resalta la fila y aparece un tooltip con el detalle estadístico completo; al hacer clic, la página se desplaza automáticamente a la sección 3 ya con ese rubro seleccionado.
4. **Serie de tiempo nacional** — con el hallazgo del salto de cierres en 2016 marcado y explicado.
5. **Selector de rubro** — al cambiarlo (o al hacer clic en una barra), se recalculan en vivo: el resumen del rubro (r, n, p-valor), el badge de interpretación, el gráfico de dispersión con tooltip por comuna, y dos rankings con barras de intensidad visual para comparar la severidad entre comunas de un vistazo.
6. **Panel de metodología, alcance y advertencias**: periodo analizado, comunas en la muestra, combinaciones comuna×rubro, umbral mínimo usado, % de empresas pyme del universo, y las 4 advertencias conceptuales (correlación no es causalidad, no predice el cierre de una empresa individual, término de giro no es sinónimo de fracaso, no es asesoría financiera).
7. **Comparador de concentración absoluta vs. relativa**, con el resultado de sensibilidad a 2016 junto a cada rubro.

## Mejoras de UX/UI acumuladas
- **Jerarquía**: el hallazgo central va primero (resumen antes que el detalle), siguiendo cómo se escanea un dashboard, no un documento.
- **Feedback de interacción**: hover con resaltado de fila + tooltip en el gráfico de barras; clic en una barra hace scroll suave hasta el detalle correspondiente.
- **Estado codificado en forma, no solo en número**: las tablas de ranking tienen una barra de intensidad junto a cada tasa de cierre — se puede comparar severidad sin leer los decimales.
- **Accesibilidad**: cada gráfico Canvas (invisible para lectores de pantalla) tiene una descripción de texto oculta (`aria-describedby`) con el contenido equivalente; el badge de interpretación usa `aria-live` para anunciar cambios; el selector cubre por teclado la misma función que hacer clic en una barra.
- **Responsive robusto**: el redimensionado de los gráficos usa `ResizeObserver` sobre el contenedor real, no `window.resize`.
- **Accesibilidad de movimiento**: todas las transiciones (scroll suave, fundido al cambiar de rubro) respetan `prefers-reduced-motion`.
- **Estados vacíos**: si un rubro no tiene comunas suficientes en alguna categoría, la tabla lo dice explícitamente en vez de mostrarse vacía sin explicación.

## Mejoras de tipografía y color
- **Tipografía body sans-serif**: el cuerpo usa una fuente sans-serif del sistema (`-apple-system, Segoe UI, Roboto...`); el monoespaciado queda reservado solo para etiquetas técnicas puntuales.
- **Paleta refinada**: los tonos cobalto y terracota se profundizaron ligeramente (`#2B5B86`→`#1F5C8B`, `#B85C2B`→`#C2632A`) para que se vean más "diseñados" y menos apagados, tanto en modo claro como oscuro.
- **Bug de coherencia de color corregido**: el badge de "confirma/invierte la hipótesis" en la sección 3 usaba rojo/verde (semántica de "riesgo"), mientras el gráfico de barras de la sección 1 usa azul/naranjo (semántica de "dirección de la relación") — un mismo rubro se veía azul en un gráfico y rojo en el badge de al lado. Ahora ambos usan la misma paleta azul=confirma/naranjo=invierte; el rojo/verde queda reservado exclusivamente para las tablas de ranking de comunas.
- **Colores de los gráficos PNG alineados**: `graficar_hito4.py` y `graficar_hito4_extra.py` usan la misma paleta que el dashboard — coherencia visual completa entre dashboard, PNG y presentación.

## Cómo generarlo de nuevo (si cambian los datos)
```bash
cd src
python analisis_hito4.py          # regenera pyme_studio_agregado_comuna_rubro.csv y ..._correlacion_por_rubro.csv
python construir_dashboard.py     # regenera dashboard_data.json e inyecta los datos en ../dashboard/pyme_studio_dashboard.html

# solo si además cambió la geometría de comunas (normalmente no hace falta, outputs/geo_comunas.json ya viene incluido):
python preparar_geo_comunas.py    # regenera outputs/geo_comunas.json a partir de data/reference/geo_raw/ (ver data/README.md)
```

O simplemente `python run_pipeline.py` desde la raíz del repositorio, que corre todo en el orden correcto.

## Bug corregido: falta de `<meta charset="UTF-8">`
El archivo no declaraba el encoding explícitamente. Abriendo el archivo con doble clic (protocolo `file://`) los navegadores adivinan UTF-8 correctamente y no se nota, pero al servir el archivo por HTTP (ej. para probarlo con un servidor local) algunos servidores no declaran el charset en la respuesta y el navegador cae a Windows-1252, mostrando "mojibake" en todo el texto con tildes (ej. "concentraciÃ³n" en vez de "concentración") — y además rompía un regex del mapa que usa un rango Unicode de tildes, dejando la página en blanco. Se agregó `<meta charset="UTF-8">` como primera línea del archivo: no depende de cómo se sirva.

## Verificación realizada
- Corrido en navegador real: sin errores de consola, todos los canvas/SVG dibujan contenido (verificado pixel a pixel), el selector recalcula correctamente al cambiar de rubro, y el modo oscuro se ve legible.
- Ejemplo probado: al seleccionar "Agricultura, ganadería, silvicultura y pesca" el dashboard recalcula a r=-0,268 (n=341, p=5,1e-7) y cambia el badge a "invierte la hipótesis" — consistente con [`analisis.md`](../analisis/analisis.md).
- Interacción de hover/tooltip verificada disparando el evento `mousemove` directamente y confirmando que el tooltip muestra el rubro, r, n y p-valor correctos.
- Las descripciones de accesibilidad (`aria-describedby`) confirmadas presentes en el DOM para los gráficos.
- **Mapa**: las 345 comunas del GeoJSON encuentran su contraparte en los datos del SII (0 sin cruzar, verificado programáticamente). El mapa se probó cambiando de rubro (actualiza conteo de comunas con datos y recolorea) y de métrica (tasa de cierre ↔ concentración, cambia escala y leyenda). El tooltip de una comuna de prueba (Santiago, rubro Industria Manufacturera) mostró el valor exacto esperado (4.846 empresas activas, tasa de cierre 3,78%), coincidiendo con los datos fuente.
