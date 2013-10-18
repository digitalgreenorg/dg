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
    
    requirejs: {
        compile: {
        	options:{
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
	    		modules: [
	    		          {
	    		        	  name: 'main' 
	    		          },
	    		          {
	    		        	  name: 'controllers/HomeController',
	    		        	  exclude: ["main"]
	    		          },
	    		          {
	    		        	  name: 'controllers/AboutController',
	    		        	  exclude: ["main"]
	    		          },
	    		          {
	    		        	  name: 'controllers/CollectionsController',
	    		        	  exclude: ["main"]
	    		          },
	    		          {
	    		        	  name: 'controllers/ProfileController',
	    		        	  exclude: ["main"]
	    		          },
	    		          {
	    		        	  name: 'controllers/ViewCollectionsController',
	    		        	  exclude: ["main"]
	    		          }
	    		         ]
        	}
        }
    }
  
  });
  
  
  grunt.loadNpmTasks('grunt-requirejs');
   
  grunt.registerTask('roptimize', ['requirejs']);

};
