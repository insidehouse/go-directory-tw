/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      fontFamily: {
        sans: [
          '"Noto Sans TC"',
          '"Microsoft JhengHei"',
          'ui-sans-serif',
          'system-ui',
          '-apple-system',
          'sans-serif',
        ],
        display: ['"Noto Serif TC"', 'serif'],
      },
      colors: {
        kaya: {
          50: '#faf7f1',
          100: '#f2eadb',
          200: '#e4d4b5',
          300: '#d3b888',
          400: '#c49d63',
          500: '#b08445',
          600: '#946b37',
          700: '#77542e',
          800: '#5f4327',
          900: '#4d3722',
          950: '#2c1d10',
        },
        ink: {
          50: '#f7f6f5',
          100: '#edebe8',
          200: '#d9d6d2',
          300: '#b9b4ae',
          400: '#948e86',
          500: '#79736b',
          600: '#615c56',
          700: '#4e4a45',
          800: '#3d3a37',
          900: '#2b2926',
          950: '#1a1816',
        },
        gold: {
          50: '#fdf8ec',
          100: '#faeece',
          200: '#f5db9c',
          300: '#efc261',
          400: '#eaad38',
          500: '#e09520',
          600: '#c67418',
          700: '#a55518',
          800: '#87431b',
          900: '#6f3819',
          950: '#401b09',
        },
      },
      animation: {
        'fade-in-up': 'fadeInUp 0.6s ease-out forwards',
        'fade-in': 'fadeIn 0.8s ease-out forwards',
      },
      keyframes: {
        fadeInUp: {
          '0%': { opacity: '0', transform: 'translateY(16px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
      },
    },
  },
  plugins: [],
};
