const plugins = {};
try {
  require.resolve('@tailwindcss/postcss');
  plugins['@tailwindcss/postcss'] = {};
} catch (e) {
  // TODO: install @tailwindcss/postcss for full PostCSS support
}
try {
  require.resolve('autoprefixer');
  plugins.autoprefixer = {};
} catch (e) {
  // TODO: install autoprefixer for proper CSS processing
}

module.exports = { plugins };
