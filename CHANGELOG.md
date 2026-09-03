# Changelog

Registro de la evolución del proyecto, por categoría. No hay fechas ni números de versión confiables para todas las etapas (el trabajo se hizo en varias sesiones sin tags formales), así que se agrupa por hito en vez de inventar un calendario.

## Pipeline inicial
Unión de las 3 fuentes del SII (aperturas, cierres, empresas activas) en un dataset único por año/comuna/rubro. Corrección del formato numérico chileno, normalización de rubros, filtrado de filas vacías y categorías residuales.

## Primer análisis
Correlación de Spearman entre concentración de empresas y tasa de cierre — global (r≈0) y por rubro (Comercio r=0,575, Alojamiento/Comidas r=0,359, Agricultura r=−0,268).

## Dashboard inicial
Primera versión del dashboard HTML autocontenido: KPIs, ranking de correlación por rubro, serie de tiempo nacional, explorador por rubro con dispersión y rankings de comunas.

## Dashboard con mapa
Se agregó un mapa coroplético de Chile por comuna (geometría de chilemapas, simplificada con Shapely), sincronizado con el selector de rubro.

## Sensibilidad a 2016
El salto de términos de giro en 2016 (Ley 20.899) se investigó y se recalculó la correlación excluyendo ese año — el hallazgo central se mantiene.

## Concentración relativa
Se agregó una medida de concentración relativa (participación del rubro dentro de la comuna) junto a la absoluta — reveló que Alojamiento/Comidas invierte de signo con esta métrica.

## Validación del alcance pyme
Se verificó, con la clasificación oficial del SII (Ley 20.416), que el universo analizado es mayoritariamente pyme (91,6%–100% según el rubro) — no exclusivamente, ya que el pipeline no filtra por tamaño de empresa.

## Reorganización pública del repositorio
El proyecto se reestructuró para publicación en GitHub: separación de `src/`, `data/`, `outputs/`, `docs/`, `dashboard/`; exclusión de los datos originales del SII y de los derivados grandes; licencia MIT; `data/README.md` documentando las fuentes oficiales.

## Corrección por comparaciones múltiples
Se aplicó corrección FDR (Benjamini-Hochberg) y Bonferroni a la familia de 19 pruebas por rubro — el hallazgo central (Comercio, Alojamiento/Comidas, Agricultura) se mantiene significativo bajo ambos criterios.

## Análisis por subperíodo
Se recalculó la correlación en 4 ventanas de tiempo (2005-2010, 2011-2015, 2016-2019, 2020-2024) — reveló que Comercio y Alojamiento/Comidas se fortalecen con el tiempo, y que Agricultura cambia de signo entre la primera y la segunda mitad del período.

## Tests
Suite de pytest sobre las funciones puras del pipeline y los scripts de análisis, con datos sintéticos — no requiere los archivos del SII.

## Integración continua
Workflow de GitHub Actions: tests en Python 3.11-3.13, validación de sintaxis, chequeos de higiene del repositorio (sin datos originales versionados, sin derivados grandes, sin archivos inesperadamente grandes, sin rutas personales evidentes, enlaces Markdown válidos).

## Documentación ampliada y accesibilidad
Glosario, explicación detallada de la tasa histórica, justificación de por qué el proyecto es Big Data, diccionario de datos, guía de evaluación, guía de exposición, evidencia de reproducibilidad. Corrección de un bug real de viewport móvil (el dashboard no tenía `<meta name="viewport">`, causando zoom incorrecto en celulares) y de un desborde horizontal en las tablas de ranking en pantallas angostas.
