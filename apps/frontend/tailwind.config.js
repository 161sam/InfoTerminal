const colors = require('tailwindcss/colors');
module.exports = {
  content: [
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./lib/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: { extend: { colors: { primary: colors.blue } } },
  plugins: [require('@tailwindcss/forms'), require('@tailwindcss/typography')],
}
