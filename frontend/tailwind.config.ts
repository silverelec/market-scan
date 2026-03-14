import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['var(--font-jakarta)', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        display: ['var(--font-fraunces)', 'Georgia', 'serif'],
      },
      colors: {
        stone: {
          50:  '#F7F4EF',
          100: '#EDE8DE',
          200: '#D9D0C2',
          300: '#C4BAA8',
          400: '#A8998A',
          500: '#8A7B6E',
          600: '#6E5F52',
          700: '#544840',
          800: '#3A322C',
          900: '#24201A',
        },
        bronze: {
          300: '#D4B483',
          400: '#C4A060',
          500: '#B08D57',
          600: '#9A7A46',
        },
      },
    },
  },
  plugins: [],
}

export default config
