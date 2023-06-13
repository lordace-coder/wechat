{import('tailwindcss').Config}
const plugin = require('tailwindcss/plugin');


module.exports = {
  // prefix:'tw-',
  mode: 'jit',
  // purge:[],
  content: [
    './chat//*.html',
    './chat//*.js',
    './src//*.jsx',
  ],
  theme: {
    extend: {},
  },
  plugins:[require("./myCustomPlugin"),require("./baseplugins")]
}