{import('tailwindcss').Config}
const plugin = require('tailwindcss/plugin');


module.exports = {
  // prefix:'tw-',
  mode: 'jit',
  // purge:[],
  content: [
    './chat/templates//*.html',
    './chat/templates/components//*.html',
    './chat/static//*.html',
    './chat/templates//*.js',
    './src//*.jsx',
  ],
  theme: {
    extend: {},
  },
  plugins:[require("./myCustomPlugin"),require("./baseplugins")]
}