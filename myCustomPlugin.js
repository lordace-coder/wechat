const plugin = require('tailwindcss/plugin');


module.exports =plugin(function({ addUtilities, variants }) {
      const flex_centered = {
        '.flex-centered':{
          display:"flex",
          justifyContent:"center",
          alignItems:"center"
        },
        '.glass-morph':{
          'backgroundColor': 'rgba(255, 255, 255, 0.3)',
          boxShadow:' 0 8px 32px 0 rgba(31, 38, 135, 0.37)',
          backdropFilter: 'blur(10px)',
          '-webkitBackdropFilter': 'blur(10px)',
          border: '1px solid rgba(255, 255, 255, 0.18)'
        }
      };

      addUtilities(flex_centered, {variants:["responsive"]},('flex_centered'));


     
    })