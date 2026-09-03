const pptxgen = require("pptxgenjs");
const path = require("path");

// Paleta idéntica a dashboard/pyme_studio_dashboard.html
const NAVY = "0F2C42";
const NAVY_CARD = "153A54";
const NAVY_LINE = "26506E";
const PAPER = "F6F8FA";
const INK = "16222B";
const MUTED = "52697A";
const COBALT = "1F5C8B";
const COBALT_SOFT = "DCEAF4";
const RUST = "C2632A";
const RUST_SOFT = "FBE7D3";
const OK = "2F8F5B";
const OK_SOFT = "DCF0E4";
const RISK = "C0392B";
const RISK_SOFT = "F7DEDB";
const WHITE = "FFFFFF";

const HEAD = "Cambria";
const BODY = "Calibri";
const MONO = "Courier New";

const IMG = (name) => path.join(__dirname, name);

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.title = "PYME Studio";
pres.subject = "Concentración de empresas y su relación con el cierre de negocios en Chile, por comuna y rubro (SII, 2005-2024)";
pres.author = "Ignacio Hidalgo, Sergio Ariel Rebolledo López, Avelyn García";
pres.company = "Samsung Innovation Campus 2026 — Big Data Mixto";
const W = 13.33, H = 7.5;
const TOTAL = 17;

function bgFill(slide, color) { slide.background = { color }; }

function kicker(slide, text, opts = {}) {
  slide.addText(text.toUpperCase(), {
    x: opts.x ?? 0.6, y: opts.y ?? 0.5, w: opts.w ?? 9, h: 0.4,
    fontFace: MONO, fontSize: 12, color: opts.color ?? RUST, bold: true, charSpacing: 2, margin: 0,
  });
}

function pageNum(slide, n) {
  slide.addText(`${String(n).padStart(2, "0")} / ${TOTAL}`, {
    x: W - 1.3, y: H - 0.55, w: 1.0, h: 0.3,
    fontFace: MONO, fontSize: 9, color: MUTED, align: "right", margin: 0,
  });
}

function iconCircle(slide, iconFile, x, y, d, circleColor) {
  slide.addShape("ellipse", { x, y, w: d, h: d, fill: { color: circleColor }, line: { type: "none" } });
  const pad = d * 0.24;
  slide.addImage({ path: IMG(iconFile), x: x + pad, y: y + pad, w: d - pad * 2, h: d - pad * 2 });
}

// ============================================================ 1. PORTADA
{
  const s = pres.addSlide();
  bgFill(s, NAVY);
  s.addText("SIC 2026 · BIG DATA MIXTO · CAPSTONE — MÓDULO 1", {
    x: 0.9, y: 1.35, w: 10, h: 0.4, fontFace: MONO, fontSize: 13, color: "8FB4CE", charSpacing: 2, margin: 0,
  });
  s.addText("PYME Studio", { x: 0.85, y: 1.9, w: 11, h: 1.6, fontFace: HEAD, fontSize: 60, bold: true, color: WHITE, margin: 0 });
  s.addText("Concentración de pymes y su relación con el cierre de negocios en Chile", {
    x: 0.9, y: 3.4, w: 9.7, h: 0.7, fontFace: BODY, fontSize: 20, italic: true, color: "BFD8EA", margin: 0,
  });
  s.addShape("line", { x: 0.9, y: 4.3, w: 3.2, h: 0, line: { color: RUST, width: 2.5 } });
  s.addText([
    { text: "Equipo:  ", options: { bold: true, color: "8FB4CE" } },
    { text: "Ignacio Hidalgo · Sergio Ariel Rebolledo López · Avelyn García\n", options: { color: WHITE } },
    { text: "Fuente de datos:  ", options: { bold: true, color: "8FB4CE" } },
    { text: "Servicio de Impuestos Internos (SII), 2005–2024", options: { color: WHITE } },
  ], { x: 0.9, y: 4.65, w: 9.7, h: 0.8, fontFace: BODY, fontSize: 13, margin: 0, lineSpacingMultiple: 1.4 });
  iconCircle(s, "icon_problema.png", W - 2.6, H - 2.6, 1.5, NAVY_CARD);
  pageNum(s, 1);
}

// ============================================================ 2. RESUMEN EJECUTIVO (NUEVO)
{
  const s = pres.addSlide();
  bgFill(s, PAPER);
  kicker(s, "Resumen ejecutivo", { x: 0.6, y: 0.5 });
  s.addText("Si solo vas a leer una diapositiva, que sea esta", {
    x: 0.6, y: 0.95, w: 11.8, h: 0.65, fontFace: HEAD, fontSize: 25, bold: true, color: INK, margin: 0,
  });

  s.addShape("rect", { x: 0.6, y: 1.85, w: 12.15, h: 1.5, fill: { color: NAVY }, line: { type: "none" } });
  s.addText("¿La concentración de negocios similares se relaciona con más cierres?", {
    x: 0.95, y: 2.05, w: 7.4, h: 0.5, fontFace: BODY, fontSize: 13, color: "8FB4CE", margin: 0,
  });
  s.addText([
    { text: "Depende del rubro. ", options: { bold: true, color: WHITE } },
    { text: "En comercio y comida, sí — con fuerza estadística. En agricultura y salud, es al revés.", options: { color: "D9E8F2" } },
  ], { x: 0.95, y: 2.5, w: 10.8, h: 0.75, fontFace: HEAD, fontSize: 17, margin: 0, lineSpacingMultiple: 1.3 });

  const stats = [
    ["126.566", "filas analizadas", COBALT],
    ["r = 0,575", "Comercio (p<0,0001)", COBALT],
    ["r = 0,359", "Alojamiento/Comidas", COBALT],
    ["r = −0,268", "Agricultura (al revés)", RUST],
  ];
  const cw = 2.85, gap = 0.2;
  stats.forEach((st, i) => {
    const x = 0.6 + i * (cw + gap);
    s.addShape("rect", { x, y: 3.65, w: cw, h: 1.7, fill: { color: WHITE }, line: { color: "D2DEE4", width: 1 } });
    s.addText(st[0], { x: x + 0.18, y: 3.85, w: cw - 0.36, h: 0.75, fontFace: HEAD, fontSize: 24, bold: true, color: st[2], margin: 0 });
    s.addText(st[1], { x: x + 0.18, y: 4.6, w: cw - 0.36, h: 0.6, fontFace: BODY, fontSize: 11.5, color: MUTED, margin: 0, lineSpacingMultiple: 1.25 });
  });

  s.addText("Metodología: correlación de Spearman entre nº de empresas activas y tasa de cierre, comparando comunas dentro de cada rubro por separado (no mezclados) — 2005-2024, datos oficiales del SII, validados de forma cruzada.", {
    x: 0.6, y: 5.6, w: 12.15, h: 0.7, fontFace: BODY, italic: true, fontSize: 12, color: MUTED, margin: 0, lineSpacingMultiple: 1.35,
  });
  pageNum(s, 2);
}

// ============================================================ 3. EL PROBLEMA
{
  const s = pres.addSlide();
  bgFill(s, PAPER);
  iconCircle(s, "icon_problema.png", 0.6, 0.42, 0.62, RUST);
  kicker(s, "El problema", { x: 1.45, y: 0.55 });
  s.addText("Se abren negocios similares en la misma calle. ¿Ayuda o perjudica?", {
    x: 0.6, y: 1.05, w: 11.6, h: 0.9, fontFace: HEAD, fontSize: 25, bold: true, color: INK, margin: 0,
  });

  // Motivo visual: fila de "locales" representando la observación (misma calle, negocios similares)
  const shopY = 2.05, shopW = 0.95, shopH = 0.95, shopGap = 0.18;
  const shops = [COBALT, COBALT, RUST, COBALT, COBALT, RUST, COBALT];
  shops.forEach((c, i) => {
    const x = 0.6 + i * (shopW + shopGap);
    s.addShape("rect", { x, y: shopY, w: shopW, h: shopH, fill: { color: c }, line: { type: "none" } });
    s.addShape("rect", { x: x + shopW * 0.3, y: shopY + shopH * 0.45, w: shopW * 0.4, h: shopH * 0.55, fill: { color: WHITE }, line: { type: "none" } });
  });
  s.addText("Observación real: locales similares (abarrotes, comida) agrupados en una misma cuadra", {
    x: 0.6, y: shopY + shopH + 0.12, w: 8, h: 0.35, fontFace: MONO, fontSize: 9.5, color: MUTED, margin: 0,
  });

  s.addShape("rect", {
    x: 0.6, y: 3.55, w: 7.6, h: 3.15, fill: { color: WHITE }, line: { color: "D2DEE4", width: 1 },
    shadow: { type: "outer", color: "9FB0B8", opacity: 0.3, blur: 10, offset: 3, angle: 90 },
  });
  s.addText("“", { x: 0.95, y: 3.7, w: 1, h: 0.6, fontFace: HEAD, fontSize: 36, color: RUST, bold: true, margin: 0 });
  s.addText(
    "Los emprendedores e inversionistas necesitan decidir si conviene abrir un negocio de un rubro específico en una comuna determinada, porque una mala decisión de ubicación puede llevar al cierre temprano del negocio, y hoy no pueden hacerlo con evidencia porque no existe una fuente accesible que muestre la concentración y la tasa histórica de cierre de negocios similares por zona.",
    { x: 1.15, y: 4.05, w: 6.7, h: 2.35, fontFace: HEAD, fontSize: 14, italic: true, color: INK, margin: 0, lineSpacingMultiple: 1.3 }
  );

  const cardX = 8.5, cardW = 4.25;
  s.addShape("rect", { x: cardX, y: 3.55, w: cardW, h: 1.5, fill: { color: COBALT_SOFT }, line: { type: "none" } });
  s.addText("USUARIO", { x: cardX + 0.25, y: 3.7, w: cardW - 0.5, h: 0.3, fontFace: MONO, fontSize: 10, color: COBALT, bold: true, charSpacing: 1, margin: 0 });
  s.addText("Emprendedores e inversionistas, municipios e investigadores.", {
    x: cardX + 0.25, y: 3.98, w: cardW - 0.5, h: 0.95, fontFace: BODY, fontSize: 12.5, color: INK, margin: 0, lineSpacingMultiple: 1.25,
  });
  s.addShape("rect", { x: cardX, y: 5.2, w: cardW, h: 1.5, fill: { color: RUST_SOFT }, line: { type: "none" } });
  s.addText("EVIDENCIA", { x: cardX + 0.25, y: 5.35, w: cardW - 0.5, h: 0.3, fontFace: MONO, fontSize: 10, color: RUST, bold: true, charSpacing: 1, margin: 0 });
  s.addText("A veces es plano regulador, otras son decisiones de inversión sin datos que las respalden.", {
    x: cardX + 0.25, y: 5.63, w: cardW - 0.5, h: 0.95, fontFace: BODY, fontSize: 12.5, color: INK, margin: 0, lineSpacingMultiple: 1.25,
  });
  pageNum(s, 3);
}

// ============================================================ 4. PREGUNTA Y ALCANCE
{
  const s = pres.addSlide();
  bgFill(s, PAPER);
  kicker(s, "Pregunta de datos", { x: 0.6, y: 0.55 });
  s.addText("¿Cuál es la concentración de pymes por rubro y comuna, y cómo se relaciona con su tasa histórica de término de giro (cierre)?", {
    x: 0.6, y: 1.05, w: 12.1, h: 1.6, fontFace: HEAD, fontSize: 26, bold: true, color: INK, margin: 0, lineSpacingMultiple: 1.15,
  });

  const colW = 5.9, y0 = 3.0, colH = 3.6;
  s.addShape("rect", { x: 0.6, y: y0, w: colW, h: colH, fill: { color: WHITE }, line: { color: "D2DEE4", width: 1 } });
  s.addText("DENTRO DEL ALCANCE", { x: 0.9, y: y0 + 0.25, w: colW - 0.6, h: 0.35, fontFace: MONO, fontSize: 11, color: COBALT, bold: true, charSpacing: 1, margin: 0 });
  const dentro = ["Chile completo, todas las comunas", "2005–2024 (histórico, 20 años)", "Análisis a nivel comuna", "Los 21 rubros económicos (CIIU Rev.4)", "Correlación estadística documentada"];
  s.addText(dentro.map((t) => ({ text: t, options: { bullet: { code: "2713", indent: 20 }, breakLine: true, paraSpaceAfter: 10 } })), {
    x: 0.9, y: y0 + 0.75, w: colW - 0.6, h: colH - 1.0, fontFace: BODY, fontSize: 14, color: INK, margin: 0,
  });
  s.addShape("rect", { x: 6.85, y: y0, w: colW, h: colH, fill: { color: WHITE }, line: { color: "D2DEE4", width: 1 } });
  s.addText("FUERA DEL ALCANCE", { x: 7.15, y: y0 + 0.25, w: colW - 0.6, h: 0.35, fontFace: MONO, fontSize: 11, color: RUST, bold: true, charSpacing: 1, margin: 0 });
  const fuera = ["Nivel de calle o dirección exacta", "Predicción en tiempo real", "Causalidad (solo correlación)", "Factores externos al SII (arriendo, tráfico, etc.)"];
  s.addText(fuera.map((t) => ({ text: t, options: { bullet: { code: "2717", indent: 20 }, breakLine: true, paraSpaceAfter: 10 } })), {
    x: 7.15, y: y0 + 0.75, w: colW - 0.6, h: colH - 1.0, fontFace: BODY, fontSize: 14, color: INK, margin: 0,
  });
  pageNum(s, 4);
}

// ============================================================ 5. METODOLOGÍA / ROADMAP (NUEVO)
{
  const s = pres.addSlide();
  bgFill(s, PAPER);
  kicker(s, "Cómo se llegó hasta acá", { x: 0.6, y: 0.55 });
  s.addText("6 hitos, del tema vago al hallazgo con evidencia", {
    x: 0.6, y: 1.05, w: 11.6, h: 0.7, fontFace: HEAD, fontSize: 25, bold: true, color: INK, margin: 0,
  });

  const steps = [
    ["1", "Empatizar y definir", "Design Thinking: usuario, evidencia, problema en una frase"],
    ["2", "Factibilidad", "F1-F4: ¿hay datos, técnica, tiempo y alcance realistas?"],
    ["3", "Pipeline", "3 fuentes del SII unidas en un dataset único"],
    ["4", "Análisis", "Correlación global y por rubro, con significancia"],
    ["5", "Producto", "Dashboard interactivo"],
    ["6", "Presentación", "Esta síntesis"],
  ];
  const y0 = 2.6;
  s.addShape("line", { x: 1.1, y: y0 + 0.35, w: 11.1, h: 0, line: { color: "D2DEE4", width: 2 } });
  const n = steps.length, spanW = 11.1, stepGap = spanW / (n - 1);
  steps.forEach((st, i) => {
    const cx = 1.1 + i * stepGap;
    const isLast = i === n - 1;
    s.addShape("ellipse", { x: cx - 0.35, y: y0, w: 0.7, h: 0.7, fill: { color: isLast ? RUST : COBALT }, line: { type: "none" } });
    s.addText(st[0], { x: cx - 0.35, y: y0, w: 0.7, h: 0.7, align: "center", valign: "middle", fontFace: HEAD, fontSize: 18, bold: true, color: WHITE, margin: 0 });
    s.addText(st[1], { x: cx - 0.95, y: y0 + 0.85, w: 1.9, h: 0.55, align: "center", fontFace: HEAD, fontSize: 12.5, bold: true, color: INK, margin: 0 });
    s.addText(st[2], { x: cx - 0.95, y: y0 + 1.35, w: 1.9, h: 1.3, align: "center", fontFace: BODY, fontSize: 10, color: MUTED, margin: 0, lineSpacingMultiple: 1.2 });
  });

  s.addShape("rect", { x: 0.6, y: 5.6, w: 12.15, h: 0.9, fill: { color: COBALT_SOFT }, line: { type: "none" } });
  s.addText("Cada hito quedó documentado con evidencia verificable — no solo “se hizo”, sino el archivo, el número o el gráfico que lo demuestra.", {
    x: 0.9, y: 5.75, w: 11.6, h: 0.6, fontFace: BODY, italic: true, fontSize: 13, color: INK, margin: 0, valign: "middle",
  });
  pageNum(s, 5);
}

// ============================================================ 6. ARQUITECTURA V0
{
  const s = pres.addSlide();
  bgFill(s, PAPER);
  kicker(s, "Arquitectura V0", { x: 0.6, y: 0.55 });
  s.addText("Del dato crudo al hallazgo, en 6 etapas", { x: 0.6, y: 1.05, w: 11, h: 0.7, fontFace: HEAD, fontSize: 26, bold: true, color: INK, margin: 0 });

  const steps = [
    ["Fuentes", "3 archivos SII"], ["Ingesta", "Descarga directa"], ["Almacenamiento", "DataFrames"],
    ["Procesamiento", "Limpieza, join"], ["Análisis", "Correlación"], ["Consumo", "Dashboard"],
  ];
  const n = steps.length, gap = 0.22, boxW = (11.3 - gap * (n - 1)) / n, boxY = 3.0, boxH = 2.3;
  steps.forEach((step, i) => {
    const x = 0.95 + i * (boxW + gap);
    const isLast = i === n - 1;
    s.addShape("rect", { x, y: boxY, w: boxW, h: boxH, fill: { color: isLast ? RUST : COBALT }, line: { type: "none" } });
    s.addText(String(i + 1), { x: x + 0.12, y: boxY + 0.1, w: 0.6, h: 0.4, fontFace: MONO, fontSize: 12, color: WHITE, bold: true, margin: 0 });
    s.addText(step[0], { x: x + 0.12, y: boxY + 0.6, w: boxW - 0.24, h: 0.5, fontFace: HEAD, fontSize: 14.5, bold: true, color: WHITE, margin: 0 });
    s.addText(step[1], { x: x + 0.12, y: boxY + 1.15, w: boxW - 0.24, h: 1.0, fontFace: BODY, fontSize: 10.5, color: "EAF0F5", margin: 0, lineSpacingMultiple: 1.2 });
    if (!isLast) s.addText("→", { x: x + boxW + 0.02, y: boxY + boxH / 2 - 0.25, w: gap + 0.02, h: 0.5, fontFace: BODY, fontSize: 18, color: MUTED, align: "center", margin: 0 });
  });
  s.addText("Ningún bloque asumió una tecnología concreta antes de saber qué datos había disponibles.", {
    x: 0.95, y: 5.6, w: 11.3, h: 0.5, fontFace: BODY, italic: true, fontSize: 12.5, color: MUTED, margin: 0,
  });
  pageNum(s, 6);
}

// ============================================================ 7. FUENTES Y FACTIBILIDAD
{
  const s = pres.addSlide();
  bgFill(s, PAPER);
  iconCircle(s, "icon_datos.png", 0.6, 0.42, 0.62, COBALT);
  kicker(s, "Factibilidad de datos", { x: 1.45, y: 0.55 });
  s.addText("3 fuentes del SII, validadas y cruzadas", { x: 0.6, y: 1.05, w: 11, h: 0.7, fontFace: HEAD, fontSize: 26, bold: true, color: INK, margin: 0 });

  const rows = [
    [{ text: "Fuente", options: { bold: true, color: WHITE, fill: { color: NAVY } } },
     { text: "Mide", options: { bold: true, color: WHITE, fill: { color: NAVY } } },
     { text: "Cobertura", options: { bold: true, color: WHITE, fill: { color: NAVY } } }],
    ["PUB_actividades_inscritas.txt", "Aperturas", "2005–2024"],
    ["PUB_TG.txt", "Cierres (término de giro)", "2005–2024"],
    ["PUB_COMU_RUBR.xlsb", "Empresas activas (concentración)", "2005–2024"],
  ];
  s.addTable(rows, { x: 0.6, y: 1.95, w: 7.6, h: 1.9, fontFace: BODY, fontSize: 12.5, color: INK, border: { type: "solid", color: "D2DEE4", pt: 0.75 }, autoPage: false, valign: "middle", colW: [3.6, 2.4, 1.6] });

  const checks = ["F1 · Datos", "F2 · Técnica", "F3 · Temporal", "F4 · Alcance"];
  checks.forEach((c, i) => {
    const x = 0.6 + i * 1.95;
    s.addShape("roundRect", { x, y: 4.15, w: 1.75, h: 0.85, rectRadius: 0.08, fill: { color: OK_SOFT }, line: { type: "none" } });
    s.addText("✓", { x, y: 4.22, w: 1.75, h: 0.4, align: "center", fontFace: BODY, fontSize: 16, bold: true, color: OK, margin: 0 });
    s.addText(c, { x, y: 4.58, w: 1.75, h: 0.35, align: "center", fontFace: MONO, fontSize: 9.5, color: "236B44", margin: 0 });
  });

  s.addShape("rect", { x: 8.55, y: 1.95, w: 4.15, h: 4.1, fill: { color: NAVY }, line: { type: "none" } });
  s.addText("VALIDACIÓN CRUZADA", { x: 8.85, y: 2.2, w: 3.6, h: 0.35, fontFace: MONO, fontSize: 10.5, color: "8FB4CE", bold: true, charSpacing: 1, margin: 0 });
  s.addText("0,13%", { x: 8.85, y: 2.6, w: 3.6, h: 1.1, fontFace: HEAD, fontSize: 46, bold: true, color: WHITE, margin: 0 });
  s.addText("diferencia promedio entre dos fuentes independientes del SII, en el período que comparten (2005–2015)", {
    x: 8.85, y: 3.7, w: 3.6, h: 1.0, fontFace: BODY, fontSize: 12, color: "BFD8EA", margin: 0, lineSpacingMultiple: 1.3,
  });
  s.addShape("line", { x: 8.85, y: 4.85, w: 3.55, h: 0, line: { color: NAVY_LINE, width: 1 } });
  s.addText("56% de las 3.619 combinaciones comuna+año coinciden de forma exacta.", {
    x: 8.85, y: 5.0, w: 3.6, h: 0.9, fontFace: BODY, italic: true, fontSize: 11.5, color: "BFD8EA", margin: 0, lineSpacingMultiple: 1.3,
  });
  pageNum(s, 7);
}

// ============================================================ 8. EL PIPELINE
{
  const s = pres.addSlide();
  bgFill(s, PAPER);
  iconCircle(s, "icon_pipeline.png", 0.6, 0.42, 0.62, COBALT);
  kicker(s, "Pipeline de procesamiento", { x: 1.45, y: 0.55 });
  s.addText("De 3 archivos crudos a un dataset único", { x: 0.6, y: 1.05, w: 11, h: 0.7, fontFace: HEAD, fontSize: 26, bold: true, color: INK, margin: 0 });

  const items = [
    ["Filas vacías descartadas", "~49.478 filas 100% en blanco en el archivo de cierres — no eran datos reales, eran relleno del export del SII."],
    ["Bug de formato numérico corregido", "“1.400” en el SII es mil cuatrocientos (separador de miles chileno), no uno coma cuatro."],
    ["Rubros normalizados entre 3 formatos distintos", "“A - Agricultura, ganadería...” y “AGRICULTURA, GANADERIA...” se unifican en una sola clave."],
    ["3 fuentes unidas por año + comuna + rubro", "126.566 filas finales, sin aproximaciones — las tres fuentes ya comparten el mismo período completo."],
  ];
  const colW = 5.55, gapX = 0.2, rowH = 1.55;
  items.forEach((it, i) => {
    const col = i % 2, row = Math.floor(i / 2);
    const x = 0.6 + col * (colW + gapX), y = 2.1 + row * (rowH + 0.25);
    s.addShape("rect", { x, y, w: colW, h: rowH, fill: { color: WHITE }, line: { color: "D2DEE4", width: 1 } });
    s.addShape("rect", { x, y, w: 0.08, h: rowH, fill: { color: RUST }, line: { type: "none" } });
    s.addText(it[0], { x: x + 0.3, y: y + 0.18, w: colW - 0.55, h: 0.5, fontFace: HEAD, fontSize: 14.5, bold: true, color: INK, margin: 0 });
    s.addText(it[1], { x: x + 0.3, y: y + 0.65, w: colW - 0.55, h: 0.85, fontFace: BODY, fontSize: 11.5, color: MUTED, margin: 0, lineSpacingMultiple: 1.25 });
  });
  pageNum(s, 8);
}

// ============================================================ 9. HALLAZGO 1 — con explicador "cómo leer r" + diagrama de cancelación
{
  const s = pres.addSlide();
  bgFill(s, NAVY);
  kicker(s, "Hallazgo 1", { x: 0.6, y: 0.55, color: "8FB4CE" });
  s.addText("Mezclando todos los rubros, no hay señal", { x: 0.6, y: 1.0, w: 11, h: 0.65, fontFace: HEAD, fontSize: 25, bold: true, color: WHITE, margin: 0 });

  // Escala -1 a +1 (cómo leer una correlación)
  const scaleX = 0.6, scaleY = 1.9, scaleW = 6.6, scaleH = 0.5;
  s.addShape("rect", { x: scaleX, y: scaleY, w: scaleW / 2, h: scaleH, fill: { color: RUST }, line: { type: "none" } });
  s.addShape("rect", { x: scaleX + scaleW / 2, y: scaleY, w: scaleW / 2, h: scaleH, fill: { color: COBALT }, line: { type: "none" } });
  s.addText("−1", { x: scaleX - 0.05, y: scaleY + scaleH + 0.05, w: 0.6, h: 0.3, fontFace: MONO, fontSize: 10, color: "8FB4CE", margin: 0 });
  s.addText("0", { x: scaleX + scaleW / 2 - 0.2, y: scaleY + scaleH + 0.05, w: 0.4, h: 0.3, align: "center", fontFace: MONO, fontSize: 10, color: "8FB4CE", margin: 0 });
  s.addText("+1", { x: scaleX + scaleW - 0.4, y: scaleY + scaleH + 0.05, w: 0.6, h: 0.3, align: "right", fontFace: MONO, fontSize: 10, color: "8FB4CE", margin: 0 });
  s.addShape("ellipse", { x: scaleX + scaleW / 2 - 0.09, y: scaleY - 0.09, w: 0.18, h: 0.18 + scaleH + 0.18, fill: { type: "none" }, line: { type: "none" } });
  s.addShape("triangle", { x: scaleX + scaleW / 2 - 0.12, y: scaleY - 0.28, w: 0.24, h: 0.22, fill: { color: WHITE }, line: { type: "none" }, rotate: 180 });
  s.addText("r global ≈ 0 — justo en el centro de la escala", { x: scaleX, y: scaleY + 0.7, w: scaleW, h: 0.35, fontFace: BODY, italic: true, fontSize: 11.5, color: "8FB4CE", margin: 0 });

  s.addText("r ≈ 0", { x: 0.7, y: 2.9, w: 6, h: 1.7, fontFace: HEAD, fontSize: 100, bold: true, color: RUST, margin: 0 });
  s.addText("Pearson r = −0,028 (p=0,077)  ·  Spearman r = +0,029 (p=0,066)", {
    x: 0.75, y: 4.55, w: 7, h: 0.4, fontFace: MONO, fontSize: 12, color: "BFD8EA", margin: 0,
  });
  s.addText("Ninguno es significativo. Si el análisis se hubiera quedado aquí, la conclusión habría sido: la hipótesis no se sostiene.", {
    x: 0.75, y: 5.05, w: 7.1, h: 0.9, fontFace: BODY, italic: true, fontSize: 13, color: "8FB4CE", margin: 0, lineSpacingMultiple: 1.3,
  });

  // Diagrama de cancelación
  const dx = 8.55, dw = 4.15;
  s.addShape("rect", { x: dx, y: 1.9, w: dw, h: 4.3, fill: { color: NAVY_CARD }, line: { color: NAVY_LINE, width: 1 } });
  s.addText("¿POR QUÉ SE CANCELA?", { x: dx + 0.25, y: 2.1, w: dw - 0.5, h: 0.35, fontFace: MONO, fontSize: 10, color: RUST, bold: true, charSpacing: 1, margin: 0 });

  s.addShape("chevron", { x: dx + 0.3, y: 2.65, w: 1.5, h: 0.55, fill: { color: COBALT }, line: { type: "none" } });
  s.addText("Comercio +0,58", { x: dx + 0.3, y: 3.28, w: 1.7, h: 0.5, align: "center", fontFace: BODY, fontSize: 10.5, bold: true, color: WHITE, margin: 0 });

  s.addShape("chevron", { x: dx + 2.35, y: 2.65, w: 1.5, h: 0.55, fill: { color: RUST }, line: { type: "none" }, flipH: true });
  s.addText("Financiero −0,14", { x: dx + 2.15, y: 3.28, w: 1.9, h: 0.5, align: "center", fontFace: BODY, fontSize: 10.5, bold: true, color: WHITE, margin: 0 });

  s.addText("Al promediar sectores con dinámicas opuestas, se cancelan entre sí. Había que mirar la correlación dentro de cada rubro por separado.", {
    x: dx + 0.25, y: 4.05, w: dw - 0.5, h: 1.9, fontFace: BODY, fontSize: 13, color: "EAF0F5", margin: 0, lineSpacingMultiple: 1.4,
  });
  pageNum(s, 9);
}

// ============================================================ 10. HALLAZGO 2 (bar chart)
{
  const s = pres.addSlide();
  bgFill(s, PAPER);
  kicker(s, "Hallazgo 2", { x: 0.6, y: 0.5 });
  s.addText("Por rubro, la relación sí aparece — y con fuerza", { x: 0.6, y: 0.95, w: 11.8, h: 0.65, fontFace: HEAD, fontSize: 24, bold: true, color: INK, margin: 0 });
  s.addText("Correlación de Spearman entre concentración y tasa de cierre, comparando comunas dentro de cada rubro.", {
    x: 0.6, y: 1.55, w: 11.8, h: 0.4, fontFace: BODY, fontSize: 12.5, color: MUTED, margin: 0,
  });
  s.addImage({ path: IMG("../../../outputs/figures/hito4_barras_correlacion_por_rubro.png"), x: 2.05, y: 2.0, w: 9.2, h: 5.1 });
  pageNum(s, 10);
}

// ============================================================ 11. HALLAZGO 3 (scatter + stats)
{
  const s = pres.addSlide();
  bgFill(s, PAPER);
  kicker(s, "Hallazgo 3", { x: 0.6, y: 0.5 });
  s.addText("Justo donde se esperaba: comercio y comida", { x: 0.6, y: 0.95, w: 11.8, h: 0.65, fontFace: HEAD, fontSize: 24, bold: true, color: INK, margin: 0 });
  s.addImage({ path: IMG("../../../outputs/figures/hito4_dispersion_por_rubro.png"), x: 0.5, y: 1.65, w: 7.6, h: 5.55 });

  const statsX = 8.4, statsW = 4.4;
  s.addShape("rect", { x: statsX, y: 1.65, w: statsW, h: 2.55, fill: { color: COBALT_SOFT }, line: { type: "none" } });
  s.addText("COMERCIO AL POR MAYOR/MENOR", { x: statsX + 0.3, y: 1.85, w: statsW - 0.6, h: 0.35, fontFace: MONO, fontSize: 10, bold: true, color: COBALT, margin: 0 });
  s.addText("r = 0,575", { x: statsX + 0.3, y: 2.2, w: statsW - 0.6, h: 0.8, fontFace: HEAD, fontSize: 40, bold: true, color: COBALT, margin: 0 });
  s.addText("342 comunas · p < 0,0001", { x: statsX + 0.3, y: 2.95, w: statsW - 0.6, h: 0.35, fontFace: BODY, fontSize: 12.5, color: INK, margin: 0 });
  s.addText("El rubro del ejemplo original: abarrotes y tiendas.", { x: statsX + 0.3, y: 3.3, w: statsW - 0.6, h: 0.8, fontFace: BODY, italic: true, fontSize: 11.5, color: MUTED, margin: 0, lineSpacingMultiple: 1.3 });

  s.addShape("rect", { x: statsX, y: 4.4, w: statsW, h: 2.55, fill: { color: RUST_SOFT }, line: { type: "none" } });
  s.addText("ALOJAMIENTO Y SERVICIO DE COMIDAS", { x: statsX + 0.3, y: 4.6, w: statsW - 0.6, h: 0.35, fontFace: MONO, fontSize: 10, bold: true, color: RUST, margin: 0 });
  s.addText("r = 0,359", { x: statsX + 0.3, y: 4.95, w: statsW - 0.6, h: 0.8, fontFace: HEAD, fontSize: 40, bold: true, color: RUST, margin: 0 });
  s.addText("344 comunas · p < 0,0001", { x: statsX + 0.3, y: 5.7, w: statsW - 0.6, h: 0.35, fontFace: BODY, fontSize: 12.5, color: INK, margin: 0 });
  s.addText("Sushi, pizzerías, restaurantes — el otro rubro del ejemplo original.", { x: statsX + 0.3, y: 6.05, w: statsW - 0.6, h: 0.8, fontFace: BODY, italic: true, fontSize: 11.5, color: MUTED, margin: 0, lineSpacingMultiple: 1.3 });
  pageNum(s, 11);
}

// ============================================================ 12. HALLAZGO INESPERADO 2016
{
  const s = pres.addSlide();
  bgFill(s, PAPER);
  kicker(s, "Hallazgo inesperado", { x: 0.6, y: 0.5 });
  s.addText("El salto de cierres en 2016 no fue una crisis", { x: 0.6, y: 0.95, w: 11.8, h: 0.65, fontFace: HEAD, fontSize: 24, bold: true, color: INK, margin: 0 });
  s.addImage({ path: IMG("../../../outputs/figures/hito4_serie_tiempo_nacional.png"), x: 0.6, y: 1.6, w: 8.0, h: 4.3 });

  const bx = 8.95, bw = 3.85;
  s.addShape("rect", { x: bx, y: 1.6, w: bw, h: 4.3, fill: { color: NAVY }, line: { type: "none" } });
  s.addText("35.931 → 214.705", { x: bx + 0.3, y: 1.85, w: bw - 0.6, h: 0.6, fontFace: HEAD, fontSize: 22, bold: true, color: WHITE, margin: 0 });
  s.addText("cierres entre 2015 y 2016 (6,0×)", { x: bx + 0.3, y: 2.4, w: bw - 0.6, h: 0.35, fontFace: MONO, fontSize: 10.5, color: "8FB4CE", margin: 0 });
  s.addShape("line", { x: bx + 0.3, y: 2.9, w: bw - 0.6, h: 0, line: { color: NAVY_LINE, width: 1 } });
  s.addText("Causa real, verificada: la Ley 20.899 (2016) le dio al SII la facultad de declarar de oficio el término de giro de contribuyentes inactivos que nunca habían avisado formalmente.", {
    x: bx + 0.3, y: 3.1, w: bw - 0.6, h: 1.7, fontFace: BODY, fontSize: 13, color: "EAF0F5", margin: 0, lineSpacingMultiple: 1.35,
  });
  s.addText("Un “barrido administrativo” de empresas ya inactivas — no una ola de quiebras ese año.", {
    x: bx + 0.3, y: 4.85, w: bw - 0.6, h: 0.9, fontFace: BODY, italic: true, fontSize: 12, color: "BFD8EA", margin: 0, lineSpacingMultiple: 1.3,
  });
  pageNum(s, 12);
}

// ============================================================ 13. EL PRODUCTO — MOCKUP DEL DASHBOARD (NUEVO)
{
  const s = pres.addSlide();
  bgFill(s, NAVY);
  kicker(s, "El producto", { x: 0.6, y: 0.5, color: "8FB4CE" });
  s.addText("Un dashboard interactivo, no solo un reporte", { x: 0.6, y: 0.95, w: 11, h: 0.65, fontFace: HEAD, fontSize: 24, bold: true, color: WHITE, margin: 0 });
  s.addText("dashboard/pyme_studio_dashboard.html — archivo único, sin dependencias externas, funciona sin internet", {
    x: 0.6, y: 1.5, w: 11, h: 0.35, fontFace: MONO, fontSize: 11.5, color: "8FB4CE", margin: 0,
  });

  // Marco tipo navegador
  const bx = 0.6, by = 2.05, bw = 7.7, bh = 5.05;
  s.addShape("rect", { x: bx, y: by, w: bw, h: bh, fill: { color: WHITE }, line: { type: "none" } });
  s.addShape("rect", { x: bx, y: by, w: bw, h: 0.4, fill: { color: "E7ECEF" }, line: { type: "none" } });
  ["C0392B", "B8862B", "2F8F5B"].forEach((c, i) => {
    s.addShape("ellipse", { x: bx + 0.18 + i * 0.24, y: by + 0.14, w: 0.12, h: 0.12, fill: { color: c }, line: { type: "none" } });
  });
  s.addShape("roundRect", { x: bx + 1.0, y: by + 0.08, w: bw - 1.4, h: 0.24, rectRadius: 0.05, fill: { color: WHITE }, line: { color: "D2DEE4", width: 0.5 } });
  s.addText("dashboard/pyme_studio_dashboard.html", { x: bx + 1.1, y: by + 0.08, w: bw - 1.6, h: 0.24, fontFace: MONO, fontSize: 8.5, color: MUTED, valign: "middle", margin: 0 });

  s.addText("PYME Studio", { x: bx + 0.25, y: by + 0.55, w: 3, h: 0.3, fontFace: HEAD, fontSize: 13, bold: true, color: INK, margin: 0 });
  const kpis2 = [["5.263", COBALT], ["≈ 0", MUTED], ["r=0,58", COBALT], ["6,0×", RUST]];
  kpis2.forEach((k, i) => {
    const x = bx + 0.25 + i * 1.85;
    s.addShape("rect", { x, y: by + 0.95, w: 1.7, h: 0.6, fill: { color: "F6F8FA" }, line: { color: "D2DEE4", width: 0.5 } });
    s.addText(k[0], { x, y: by + 1.0, w: 1.7, h: 0.5, align: "center", fontFace: HEAD, fontSize: 15, bold: true, color: k[1], margin: 0 });
  });
  s.addImage({ path: IMG("../../../outputs/figures/hito4_barras_correlacion_por_rubro.png"), x: bx + 0.35, y: by + 1.75, w: bw - 0.7, h: bh - 2.05 });

  const feats = [
    ["El problema primero", "Enunciado y contexto antes que cualquier gráfico."],
    ["Ranking interactivo", "19 rubros comparables con un clic; hover muestra el detalle."],
    ["Explorador por rubro", "Dispersión y rankings se recalculan al instante."],
    ["Accesible", "Lectores de pantalla, teclado, modo claro/oscuro."],
  ];
  const fx = 8.6, fw = 4.15;
  let fy = 2.05;
  feats.forEach((it) => {
    s.addShape("rect", { x: fx, y: fy, w: fw, h: 1.15, fill: { color: NAVY_CARD }, line: { type: "none" } });
    s.addText(it[0], { x: fx + 0.2, y: fy + 0.12, w: fw - 0.4, h: 0.35, fontFace: HEAD, fontSize: 12.5, bold: true, color: "7FC1EA", margin: 0 });
    s.addText(it[1], { x: fx + 0.2, y: fy + 0.5, w: fw - 0.4, h: 0.6, fontFace: BODY, fontSize: 10.5, color: "BFD8EA", margin: 0, lineSpacingMultiple: 1.25 });
    fy += 1.25;
  });
  pageNum(s, 13);
}

// ============================================================ 14. CONCLUSIONES (fortalecidas)
{
  const s = pres.addSlide();
  bgFill(s, PAPER);
  kicker(s, "Conclusiones", { x: 0.6, y: 0.5 });
  s.addText("Lo que el equipo puede afirmar con evidencia", { x: 0.6, y: 0.95, w: 11.6, h: 0.65, fontFace: HEAD, fontSize: 25, bold: true, color: INK, margin: 0 });

  const concl = [
    ["1", "La hipótesis de Ignacio se confirma — pero solo donde importa", "En comercio minorista y alojamiento/comidas, la saturación comercial se asocia con mayor cierre de forma estadísticamente robusta (n grande, p < 0,0001)."],
    ["2", "No es una regla universal de negocios", "En agricultura y salud pasa lo contrario: concentrarse ahí parece ser saludable — dinámicas de mercado distintas exigen lecturas distintas."],
    ["3", "El detalle sobrevive a la validación", "El salto de cierres en 2016 tenía una explicación legal real, no era ruido — y cambia cómo se debe leer cualquier análisis año a año."],
  ];
  let y = 1.85;
  concl.forEach((c) => {
    s.addShape("ellipse", { x: 0.6, y, w: 0.5, h: 0.5, fill: { color: RUST }, line: { type: "none" } });
    s.addText(c[0], { x: 0.6, y, w: 0.5, h: 0.5, align: "center", valign: "middle", fontFace: HEAD, fontSize: 16, bold: true, color: WHITE, margin: 0 });
    s.addText(c[1], { x: 1.3, y: y - 0.04, w: 11.1, h: 0.4, fontFace: HEAD, fontSize: 15, bold: true, color: INK, margin: 0 });
    s.addText(c[2], { x: 1.3, y: y + 0.38, w: 11.1, h: 0.65, fontFace: BODY, fontSize: 11.5, color: MUTED, margin: 0, lineSpacingMultiple: 1.25 });
    y += 1.28;
  });

  s.addShape("rect", { x: 0.6, y: 5.75, w: 8.0, h: 1.15, fill: { color: COBALT_SOFT }, line: { type: "none" } });
  s.addText("PARA UN INVERSIONISTA", { x: 0.85, y: 5.88, w: 7.5, h: 0.3, fontFace: MONO, fontSize: 9.5, bold: true, color: COBALT, charSpacing: 1, margin: 0 });
  s.addText("Antes de abrir un local en comercio o comida, revisar la tasa de cierre histórica de esa comuna específica — no asumir que “más locales cerca” siempre es mala señal en cualquier rubro.", {
    x: 0.85, y: 6.15, w: 7.5, h: 0.7, fontFace: BODY, fontSize: 11.5, color: INK, margin: 0, lineSpacingMultiple: 1.25,
  });

  s.addShape("rect", { x: 8.85, y: 5.75, w: 3.9, h: 1.15, fill: { color: RUST_SOFT }, line: { type: "none" } });
  s.addText("LÍMITE HONESTO", { x: 9.1, y: 5.88, w: 3.4, h: 0.3, fontFace: MONO, fontSize: 9.5, bold: true, color: RUST, charSpacing: 1, margin: 0 });
  s.addText("Es correlación, no causalidad — no mide arriendo, tráfico peatonal ni calidad del negocio.", {
    x: 9.1, y: 6.15, w: 3.4, h: 0.7, fontFace: BODY, fontSize: 10.5, color: INK, margin: 0, lineSpacingMultiple: 1.25,
  });
  pageNum(s, 14);
}

// ============================================================ 15. ROBUSTEZ METODOLÓGICA (NUEVO)
{
  const s = pres.addSlide();
  bgFill(s, PAPER);
  kicker(s, "Robustez metodológica", { x: 0.6, y: 0.5 });
  s.addText("¿Esto se sostiene si lo revisamos más a fondo?", { x: 0.6, y: 0.95, w: 11.6, h: 0.6, fontFace: HEAD, fontSize: 24, bold: true, color: INK, margin: 0 });

  const checks = [
    ["¿Es realmente un universo de pymes?", "Sí — verificado con la clasificación oficial del SII (Ley 20.416, por ventas). Entre 91,6% y 100% de las empresas son pyme según el rubro; 98,9%+ en los 2 rubros centrales.", OK],
    ["¿Depende del salto de cierres de 2016?", "No. Excluyendo 2016: Comercio pasa de r=0,575 a r=0,521 y Alojamiento/Comidas de r=0,359 a r=0,343 — ambos siguen significativos.", OK],
    ["¿Favorece a las comunas grandes por diseño?", "En parte. Con concentración relativa (% del rubro en la comuna, no conteo absoluto), Comercio se sostiene (r=0,322) — pero Alojamiento/Comidas se invierte (r=−0,535). Se documentan ambas métricas, no se descarta el hallazgo.", RUST],
    ["¿Qué NO dice este análisis?", "No demuestra causalidad, no predice el cierre de una empresa individual, y un término de giro no equivale a quiebra — puede ser administrativo o voluntario. No es asesoría financiera.", RISK],
  ];
  let cy = 1.9;
  const rowH = 1.0;
  checks.forEach((c) => {
    s.addShape("rect", { x: 0.6, y: cy, w: 0.1, h: rowH - 0.18, fill: { color: c[2] }, line: { type: "none" } });
    s.addText(c[0], { x: 0.95, y: cy - 0.02, w: 11.3, h: 0.36, fontFace: HEAD, fontSize: 13.5, bold: true, color: INK, margin: 0 });
    s.addText(c[1], { x: 0.95, y: cy + 0.34, w: 11.3, h: 0.5, fontFace: BODY, fontSize: 10.3, color: MUTED, margin: 0, lineSpacingMultiple: 1.15 });
    cy += rowH;
  });

  s.addShape("rect", { x: 0.6, y: cy + 0.08, w: 12.15, h: 0.9, fill: { color: NAVY }, line: { type: "none" } });
  s.addText("ENTREGABLES OFICIALES DE ESTA ENTREGA", { x: 0.85, y: cy + 0.17, w: 11.65, h: 0.26, fontFace: MONO, fontSize: 9.5, bold: true, color: "7FC1EA", charSpacing: 1, margin: 0 });
  s.addText("dashboard/pyme_studio_dashboard.html (producto) · docs/presentacion/PYME_Studio_Presentacion.pptx (esta presentación) — versiones anteriores se conservan solo como respaldo local, fuera de este repositorio. Los 6 hitos del Módulo 1 están completos. Detalle: docs/metodologia/metodologia.md.", {
    x: 0.85, y: cy + 0.44, w: 11.65, h: 0.48, fontFace: BODY, fontSize: 10.2, color: WHITE, margin: 0, lineSpacingMultiple: 1.15,
  });
  pageNum(s, 15);
}

// ============================================================ 16. EQUIPO Y ESTADO
{
  const s = pres.addSlide();
  bgFill(s, PAPER);
  iconCircle(s, "icon_equipo.png", 0.6, 0.42, 0.62, COBALT);
  kicker(s, "Equipo y método de trabajo", { x: 1.45, y: 0.55 });
  s.addText("Kanban, 4 roles, 6 hitos comprobables", { x: 0.6, y: 1.05, w: 11, h: 0.7, fontFace: HEAD, fontSize: 26, bold: true, color: INK, margin: 0 });

  const roles = [
    [{ text: "Rol", options: { bold: true, color: WHITE, fill: { color: NAVY } } }, { text: "Responsabilidad", options: { bold: true, color: WHITE, fill: { color: NAVY } } }],
    ["Coordinación", "Seguimiento del proyecto e integración del trabajo del equipo"],
    ["Datos", "Búsqueda, descarga y validación cruzada de las fuentes SII"],
    ["Procesamiento y análisis", "Pipeline, armonización de rubros, correlación estadística"],
    ["Visualización y comunicación", "Dashboard, documentación de arquitectura, esta presentación"],
  ];
  s.addTable(roles, { x: 0.6, y: 1.95, w: 6.9, h: 3.5, fontFace: BODY, fontSize: 12, color: INK, border: { type: "solid", color: "D2DEE4", pt: 0.75 }, autoPage: false, valign: "middle", colW: [2.6, 4.3] });

  const hitos = [["1", "Problema y fuentes validados"], ["2", "Datos obtenidos y almacenados"], ["3", "Pipeline funcional"], ["4", "Primer análisis completo"], ["5", "Dashboard funcional"], ["6", "Esta presentación"]];
  s.addText("HITOS DEL MÓDULO 1", { x: 7.9, y: 1.95, w: 4.8, h: 0.35, fontFace: MONO, fontSize: 10.5, bold: true, color: MUTED, charSpacing: 1, margin: 0 });
  let hy = 2.35;
  hitos.forEach((h) => {
    s.addShape("ellipse", { x: 7.9, y: hy, w: 0.32, h: 0.32, fill: { color: OK }, line: { type: "none" } });
    s.addText("✓", { x: 7.9, y: hy, w: 0.32, h: 0.32, align: "center", valign: "middle", fontFace: BODY, fontSize: 11, bold: true, color: WHITE, margin: 0 });
    s.addText(`Hito ${h[0]} — ${h[1]}`, { x: 8.35, y: hy + 0.01, w: 4.3, h: 0.32, fontFace: BODY, fontSize: 12.5, color: INK, margin: 0, valign: "middle" });
    hy += 0.475;
  });
  pageNum(s, 16);
}

// ============================================================ 17. CIERRE
{
  const s = pres.addSlide();
  bgFill(s, NAVY);
  iconCircle(s, "icon_cierre.png", W / 2 - 0.75, 1.7, 1.5, NAVY_CARD);
  s.addText("Gracias", { x: 0, y: 3.5, w: W, h: 1.0, align: "center", fontFace: HEAD, fontSize: 46, bold: true, color: WHITE, margin: 0 });
  s.addText("PYME Studio · SIC 2026 · Big Data Mixto", { x: 0, y: 4.55, w: W, h: 0.5, align: "center", fontFace: MONO, fontSize: 13, color: "8FB4CE", charSpacing: 1, margin: 0 });
  s.addText("Dashboard interactivo, código y documentación completa disponibles en la carpeta del proyecto.", {
    x: 0, y: 5.2, w: W, h: 0.5, align: "center", fontFace: BODY, italic: true, fontSize: 12.5, color: "BFD8EA", margin: 0,
  });
  pageNum(s, 17);
}

pres.writeFile({ fileName: path.join(__dirname, "..", "PYME_Studio_Presentacion.pptx") }).then(() => {
  console.log("Deck escrito.");
});
