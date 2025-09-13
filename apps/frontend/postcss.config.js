const path = require('path');

// Force Tailwind to use the local config in this package
process.env.TAILWIND_CONFIG = path.resolve(__dirname, './tailwind.config.js');

module.exports = {
  plugins: {
    // Tailwind CSS v4 PostCSS plugin
    '@tailwindcss/postcss': {},
    autoprefixer: {},
  },
};
