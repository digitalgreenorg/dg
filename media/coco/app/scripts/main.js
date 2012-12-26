require.config({
  shim: {
  },

  paths: {
    hm: 'libs/hm',
    esprima: 'libs/esprima',
    jquery: 'libs/jquery.min',
    underscore: 'libs/backbone/underscore-min',
    backbone: 'libs/backbone/backbone-min',

  }
});
 
require(['app'], function(app) {
  // use app here
  console.log(app);
  app.initialize();
});