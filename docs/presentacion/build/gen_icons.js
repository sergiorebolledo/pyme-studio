const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const fs = require("fs");
const {
  FaLightbulb, FaDatabase, FaCogs, FaChartBar, FaDesktop, FaUsers, FaFlagCheckered,
} = require("react-icons/fa");

const icons = {
  problema: FaLightbulb,
  datos: FaDatabase,
  pipeline: FaCogs,
  hallazgos: FaChartBar,
  dashboard: FaDesktop,
  equipo: FaUsers,
  cierre: FaFlagCheckered,
};

async function run() {
  for (const [name, Icon] of Object.entries(icons)) {
    const svg = ReactDOMServer.renderToStaticMarkup(
      React.createElement(Icon, { size: 256, color: "#FFFFFF" })
    );
    await sharp(Buffer.from(svg)).resize(256, 256).png().toFile(`icon_${name}.png`);
    console.log("done", name);
  }
}
run();
