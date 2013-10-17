module.exports = function( grunt ) {
  'use strict';
  //
  // Grunt configuration:
  //
  // https://github.com/cowboy/grunt/blob/master/docs/getting_started.md
  //
  
  grunt.initConfig({
	  
   
    // HTML minification
    html: {
      files: ['**/*.html']
    },

    
    // rjs configuration. You don't necessarily need to specify the typical
    // `path` configuration, the rjs task will parse these values from your
    // main module, using http://requirejs.org/docs/optimization.html#mainConfigFile
    //
    // name / out / mainConfig file should be used. You can let it blank if
    // you're using usemin-handler to parse rjs config from markup (default
    // setup)
    // rjs: {
    //      // no minification, is done by the min task
    //      optimize: 'none',
    //      baseUrl: './scripts',
    //      wrap: true,
    //      name: 'main'
    //    },

    // While Yeoman handles concat/min when using
    // usemin blocks, you can still use them manually
    
    requirejs: {
        compile: {
        	options:{
	            //optimize: "none",
	            appDir: "./scripts/",
	            baseUrl: "./",
	            paths: {
	                framework: 'libs/framework',
	                controllers: 'app/controllers',
	                jquery: 'libs/external/jquery-1.8.3.min',
	                appConfig: 'appConfig',
	                bootstrap_modal: 'libs/external/bootstrap-modal'
	            },
	            dir: "./build/",
	            optimize: "uglify",
	            uglify2: {
	            	output: {
	            		ascii_only: true,
	            		beautify: false
	            	}
	            },
	    		
	    		inlineText: true,
	    		
	            // name: "main"
	            // out: ""
	            // findNestedDependencies: true,
	    		
        	}
        }
    }
  
  });
  
  
  grunt.loadNpmTasks('grunt-requirejs');
   
  
  // Alias the `test` task to run the `mocha` task instead
  // grunt.registerTask('test', 'server:phantom mocha');
  // grunt.registerTask('default', 'concat min');
  grunt.registerTask('roptimize', ['requirejs']);

};
