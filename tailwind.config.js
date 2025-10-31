/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './app/templates/**/*.html',
    './static/js/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f4f1fe',
          100: '#e9e4fd',
          200: '#d6ccfb',
          300: '#b9a7f7',
          400: '#9575f1',
          500: '#7c4deb',
          600: '#6F56DA',
          700: '#5a3db5',
          800: '#4c3495',
          900: '#412d7a',
        },
        secondary: {
          50: '#f0fdf4',
          100: '#dcfce7',
          200: '#bbf7d0',
          300: '#86efac',
          400: '#5DD78A',
          500: '#22c55e',
          600: '#16a34a',
          700: '#15803d',
          800: '#166534',
          900: '#14532d',
        },
        hosting: {
          dark: '#1a202c',
          light: '#f7fafc',
          accent: '#5DD78A',
          primary: '#6F56DA',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        heading: ['Inter', 'system-ui', 'sans-serif'],
      },
      animation: {
        'fade-in-up': 'fadeInUp 0.6s ease-out',
        'bounce-slow': 'bounce 2s infinite',
      }
    },
  },
  plugins: [],
}