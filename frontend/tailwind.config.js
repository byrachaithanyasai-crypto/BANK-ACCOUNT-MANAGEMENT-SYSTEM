/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        navy: {
          900: '#0a192f',
          800: '#112240',
          700: '#233554'
        },
        electric: '#64ffda',
        purple: {
          dark: '#2d1b69',
          light: '#6b46c1'
        }
      }
    },
  },
  plugins: [],
}