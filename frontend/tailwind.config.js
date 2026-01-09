module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
    './app/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        'sovereign-dark': '#0f1419',
        'sovereign-light': '#1a2332',
        'sovereign-blue': '#00d9ff',
        'sovereign-green': '#00ff88',
        'sovereign-purple': '#9d4edd',
      },
      keyframes: {
        'glow': {
          '0%, 100%': { 'text-shadow': '0 0 10px #00ff88, 0 0 20px #00d9ff' },
          '50%': { 'text-shadow': '0 0 20px #00ff88, 0 0 40px #00d9ff' },
        },
        'typewriter': {
          '0%': { width: '0' },
          '100%': { width: '100%' },
        },
        'pulse-ring': {
          '0%': { transform: 'scale(1)', opacity: '1' },
          '100%': { transform: 'scale(1.5)', opacity: '0' },
        },
        'wave': {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' },
        },
      },
      animation: {
        'glow': 'glow 2s ease-in-out infinite',
        'typewriter': 'typewriter 0.5s steps(40, end)',
        'pulse-ring': 'pulse-ring 1.5s ease-out infinite',
        'wave': 'wave 0.6s ease-in-out infinite',
      },
      backdropFilter: {
        'none': 'none',
        'sm': 'blur(4px)',
        'md': 'blur(12px)',
        'lg': 'blur(20px)',
      },
    },
  },
  plugins: [],
};
