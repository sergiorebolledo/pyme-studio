# Presentación final

*Entregable oficial: [`PYME_Studio_Presentacion.pptx`](PYME_Studio_Presentacion.pptx), 17 diapositivas. Una versión anterior (14 diapositivas, sin el mapa ni las diapositivas de metodología/robustez) existió durante el desarrollo pero no se incluye en este repositorio — se conserva solo como respaldo local, sin valor documental adicional sobre esta versión.*

## Qué es
El documento pensado para mostrar el proyecto completo sin necesitar que quien lo revise abra el dashboard ni lea toda la documentación. Reúne en orden narrativo el problema, la metodología, los hallazgos y sus límites.

## Estructura (17 diapositivas)

| # | Contenido | De dónde sale |
|---|---|---|
| 1 | Portada | — |
| 2 | Resumen ejecutivo | síntesis de `../analisis/analisis.md` |
| 3 | El problema (motivo visual "misma calle") | `../proceso/definicion_problema.md` |
| 4 | Pregunta de datos + alcance dentro/fuera | `../proceso/definicion_problema.md` |
| 5 | Metodología / roadmap de los 6 hitos | `../proceso/tablero.md` |
| 6 | Arquitectura del pipeline | `../proceso/checkpoints.md` |
| 7 | Fuentes SII + factibilidad + validación cruzada | `../proceso/factibilidad.md` |
| 8 | El pipeline: 4 problemas reales resueltos | `../../src/pipeline.py` |
| 9 | Hallazgo 1 — r≈0 (con escala −1/+1 y diagrama de cancelación) | `../analisis/analisis.md` |
| 10 | Hallazgo 2 — barras por rubro (imagen real) | `../../outputs/figures/hito4_barras_correlacion_por_rubro.png` |
| 11 | Hallazgo 3 — dispersión + estadísticas | `../../outputs/figures/hito4_dispersion_por_rubro.png` |
| 12 | Hallazgo inesperado — salto de 2016 | `../../outputs/figures/hito4_serie_tiempo_nacional.png` |
| 13 | El producto — mockup de navegador con el dashboard real | `../proceso/producto_dashboard.md` |
| 14 | Conclusiones — 3 hallazgos + recomendación y límite honesto | síntesis de `../analisis/analisis.md` |
| 15 | Robustez metodológica — alcance pyme, sensibilidad 2016, absoluta vs. relativa, qué NO dice el análisis, entregables oficiales | `../metodologia/metodologia.md`, `../analisis/analisis.md` |
| 16 | Equipo (4 roles) + los 6 hitos cumplidos | `../proceso/equipo.md`, `../proceso/tablero.md` |
| 17 | Cierre | — |

## Cómo está construida
- **`pptxgenjs`**, formato 16:9 (`LAYOUT_WIDE`), sin plantilla externa.
- **Paleta unificada con el dashboard:** cobalto `#1F5C8B` (confirma la hipótesis), terracota `#C2632A` (la invierte / anotaciones), verde `#2F8F5B` y rojo `#C0392B` reservados para severidad — los mismos tokens de color en dashboard, gráficos PNG y presentación.
- **Tipografías:** Cambria (títulos), Calibri (cuerpo), Courier New (etiquetas técnicas/datos) — las tres son fuentes seguras de Office.
- **Gráficos reales, no recreados:** las diapositivas 10, 11 y 12 usan las mismas imágenes PNG del análisis (`outputs/figures/hito4_*.png`).
- **Íconos:** generados con `react-icons` + `sharp` (ver `build/gen_icons.js`).
- **Diagramas construidos con formas nativas de pptxgenjs** (no imágenes): la escala de correlación, las flechas de cancelación, el roadmap de hitos y el mockup del navegador — todo editable directamente en PowerPoint si hace falta ajustar texto.

## Verificación realizada
- `validate.py` (herramienta de QA de estructura pptx): "All validations PASSED!".
- Integridad del `.zip` (`zipfile.testzip()` → `None`) y conteo de partes de diapositiva (17) verificados tras cada regeneración.
- Conversión a PDF + revisión visual, diapositiva por diapositiva: **se encontró y corrigió un caso real de texto cortado** — el subtítulo del gráfico de barras por rubro se salía del borde derecho de la figura. Corregido ensanchando la figura en `src/graficar_hito4_extra.py` y regenerando el PNG y el deck. Tras la corrección: sin texto cortado, sin superposiciones, buen contraste en las 17 diapositivas.
- Revisión de contenido: sin texto de relleno ("lorem", "TODO", placeholders no intencionales). El placeholder `[equipo]` de la diapositiva 1 es intencional (ver "Pendiente antes de entregar" abajo).
- Bug real encontrado y corregido: los íconos salían en negro en vez de blanco por una reconstrucción manual del SVG que perdía el atributo `color`.

## Pendiente antes de entregar
El campo **"Equipo: Ignacio · Sergio Ariel Rebolledo López · [equipo]"** en la portada (diapositiva 1) tiene un placeholder `[equipo]` — hay que completarlo con el resto de los integrantes reales. No se completa automáticamente para no inventar nombres.

## Cómo regenerar el deck
```bash
cd docs/presentacion/build
npm install
node gen_icons.js     # solo si cambian los íconos
node build_deck.js    # regenera ../PYME_Studio_Presentacion.pptx
```

Los gráficos PNG que usan las diapositivas 10-12 se regeneran aparte, desde `src/`:
```bash
cd src
python graficar_hito4.py
python graficar_hito4_extra.py
```
