/** PostCSS config tolerant für Dev/Tests */
const plugins = {};
try {
  plugins['@tailwindcss/postcss'] = {};
  plugins.autoprefixer = {};
} catch (_) {
  // Tests/CI ohne CSS-Pipeline: still akzeptieren
}
module.exports = { plugins };
