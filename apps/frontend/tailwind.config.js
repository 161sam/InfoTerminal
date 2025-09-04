const colors = require('tailwindcss/colors');
module.exports = {
  content: [
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./lib/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: colors.blue,
      },
      ringColor: {
        DEFAULT: colors.blue[500],
      },
      typography: {
        DEFAULT: {
          css: {
            h1: {
              fontWeight: '600',
            },
            h2: {
              fontWeight: '600',
            },
          },
        },
      },
    },
  },
  plugins: [require('@tailwindcss/forms'), require('@tailwindcss/typography')],
};
