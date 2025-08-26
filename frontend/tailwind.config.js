/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eef2ff',
          100: '#e0e7ff',
          200: '#c7d2fe',
          300: '#a5b4fc',
          400: '#818cf8',
          500: '#6366f1',
          600: '#4f46e5',
          700: '#4338ca',
          800: '#3730a3',
          900: '#312e81',
        },
        secondary: {
          50: '#f8fafc',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
        },
        gradient: {
          blue: '#3a4ad8',
          purple: '#9c4ad8',
          light: '#e8f0ff',
          lighter: '#f9f9ff',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
        'gradient-primary': 'linear-gradient(to right, #3a4ad8, #9c4ad8)',
        'gradient-bg': 'linear-gradient(135deg, #e8f0ff, #f9f9ff)',
      },
      boxShadow: {
        'soft': '0 2px 6px rgba(0,0,0,0.05)',
        'card': '0 6px 18px rgba(0,0,0,0.08)',
        'footer': '0 -2px 6px rgba(0,0,0,0.05)',
      },
      borderRadius: {
        'xl': '16px',
        '2xl': '20px',
      }
    },
  },
  plugins: [],
} 