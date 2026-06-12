/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        display: ['Outfit', 'sans-serif'],
      },
      colors: {
        ocean: {
          light: "#38bdf8", // sky-400
          DEFAULT: "#0ea5e9", // sky-500
          dark: "#0284c7", // sky-600
        },
        flame: {
          light: "#fbbf24", // amber-400
          DEFAULT: "#f97316", // orange-500
          dark: "#dc2626", // red-600
        },
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-out forwards',
        'slide-up': 'slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards',
        'float': 'float 3s ease-in-out infinite',
        'pulse-glow': 'pulseGlow 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'morph': 'morph 8s ease-in-out infinite alternate',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        pulseGlow: {
          '0%, 100%': { opacity: '1', transform: 'scale(1)' },
          '50%': { opacity: '0.8', transform: 'scale(1.05)' },
        },
        morph: {
          '0%': { borderRadius: '60% 40% 30% 70% / 60% 30% 70% 40%', transform: 'translate(0px, 0px) rotate(0deg)' },
          '50%': { borderRadius: '30% 60% 70% 40% / 50% 60% 30% 60%', transform: 'translate(20px, 30px) rotate(45deg)' },
          '100%': { borderRadius: '60% 40% 30% 70% / 60% 30% 70% 40%', transform: 'translate(-20px, -10px) rotate(90deg)' },
        }
      }
    },
  },
  plugins: [],
}