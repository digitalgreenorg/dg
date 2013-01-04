module.exports = function( grunt ) {
  'use strict';
  //
  // Grunt configuration:
  //
  // https://github.com/cowboy/grunt/blob/master/docs/getting_started.md
  //
  
  grunt.initConfig({

    // Project configuration
    // ---------------------

    // specify an alternate install location for Bower
    // bower: {
    //       dir: 'app/components'
    //     },
    // 
    //     // Coffee to JS compilation
    //     coffee: {
    //       compile: {
    //         files: {
    //           'temp/scripts/*.js': 'app/scripts/**/*.coffee' 
    //         },
    //         options: {
    //           basePath: 'app/scripts'
    //         }
    //       }
    //     },
    // 
    //     // compile .scss/.sass to .css using Compass
    //     compass: {
    //       dist: {
    //         // http://compass-style.org/help/tutorials/configuration-reference/#configuration-properties
    //         options: {
    //           css_dir: 'temp/styles',
    //           sass_dir: 'app/styles',
    //           images_dir: 'app/images',
    //           javascripts_dir: 'temp/scripts',
    //           force: true
    //         }
    //       }
    //     },
    // 
    //     // generate application cache manifest
    //     manifest:{
    //       dest: ''
    //     },
    // 
    //     // headless testing through PhantomJS
    //     mocha: {
    //       all: ['test/**/*.html']
    //     },
    // 
    //     // default watch configuration
    //     watch: {
    //       coffee: {
    //         files: 'app/scripts/**/*.coffee',
    //         tasks: 'coffee reload'
    //       },
    //       compass: {
    //         files: [
    //           'app/styles/**/*.{scss,sass}'
    //         ],
    //         tasks: 'compass reload'
    //       },
    //       reload: {
    //         files: [
    //           'app/*.html',
    //           'app/styles/**/*.css',
    //           'app/scripts/**/*.js',
    //           'app/images/**/*'
    //         ],
    //         tasks: 'reload'
    //       }
    //     },
    // 
    //     // default lint configuration, change this to match your setup:
    //     // https://github.com/cowboy/grunt/blob/master/docs/task_lint.md#lint-built-in-task
        lint: {
             files: [
               // 'grunt.js'
               // 'app/scripts/**/*.js',
               //                'spec/**/*.js'
               'app/scripts/backbone_models.js'
             ]
           },
        
    //     // specifying JSHint options and globals
    //     // https://github.com/cowboy/grunt/blob/master/docs/task_lint.md#specifying-jshint-options-and-globals
        jshint: {
              options: {
                curly: true,
                eqeqeq: true,
                immed: true,
                latedef: true,
                newcap: true,
                noarg: true,
                sub: true,
                undef: true,
                boss: true,
                eqnull: true,
                browser: true
              },
              globals: {
                jQuery: true
              }
            },
        
    // Build configuration
    // -------------------

    // the staging directory used during the process
        staging: 'temp',
            // final build output
            output: 'dist',
        
            mkdirs: {
              staging: 'app/'
            },
        
        // Below, all paths are relative to the staging directory, which is a copy
    // of the app/ directory. Any .gitignore, .ignore and .buildignore file
    // that might appear in the app/ tree are used to ignore these values
    // during the copy process.

    // concat css/**/*.css files, inline @import, output a single minified css
    css: {
      'styles/main.css': ['styles/**/*.css']
    },

    // renames JS/CSS to prepend a hash of their contents for easier
    // versioning
    rev: {
      js: 'scripts/**/*.js',
      css: 'styles/**/*.css',
      img: 'images/**'
    },

    // usemin handler should point to the file containing
    // the usemin blocks to be parsed
    'usemin-handler': {
      html: 'index.html'
    },

    // update references in HTML/CSS to revved files
    usemin: {
      html: ['**/*.html'],
      css: ['**/*.css']
    },

    // HTML minification
    html: {
      files: ['**/*.html']
    },

    // Optimizes JPGs and PNGs (with jpegtran & optipng)
    img: {
      dist: '<config:rev.img>'
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
    concat: {
          'app/scripts/combined.js': ['app/scripts/main.js','app/scripts/app.js','app/scripts/router.js',
          // 'app/scripts/app.js'
          ]
          
    },

    min: {
        'app/scripts/backbone_models1.min.js':['app/scripts/backbone_models.js']
    },
    
    
    requirejs: {
        compile: {
          options: {
            appDir: "app/",
            baseUrl: "scripts",
            // mainConfigFile: "app/scripts/main.js",
            // out: "../dist",
            dir: "dist",
            paths: {
                    "jquery": "empty:",
                    "underscore": 'empty:',
                    'backbone': 'empty:',
                    // 'indexeddb-backbone': 'libs/indexeddb-backbonejs-adapter/backbone-indexeddb',
                    'indexeddb-backbone': 'empty:',
                    'datatable':'libs/datatablejs_media/js/jquery.dataTables.min',
                    'form_field_validator': 'empty:'
                },
            // name: "main"
            // out: ""
            // findNestedDependencies: true,
            modules: [
                           //Just specifying a module name means that module will be converted into
                           //a built file that contains all of its dependencies. If that module or any
                           //of its dependencies includes i18n bundles, they may not be included in the
                           //built file unless the locale: section is set above.
                                           {
                                               name: "main",
                                               include: ["router"]
                           //For build profiles that contain more than one modules entry,
                           //allow overrides for the properties that set for the whole build,
                           //for example a different set of pragmas for this module.
                           //The override's value is an object that can
                           //contain any of the other build options in this file.
                           // override: {
                           //                            pragmas: {
                           //                                fooExclude: true
                           //                            }
                           //                        }
                                           
                                              }
                     ]
            //                    // {
                   //                        name: "foo/bar/bop",
                   // 
                   //                        //For build profiles that contain more than one modules entry,
                   //                        //allow overrides for the properties that set for the whole build,
                   //                        //for example a different set of pragmas for this module.
                   //                        //The override's value is an object that can
                   //                        //contain any of the other build options in this file.
                   //                        override: {
                   //                            pragmas: {
                   //                                fooExclude: true
                   //                            }
                   //                        }
                   //                    },
                   //                    {
                   //                        name: "foo/bar/bop",
                   // 
                   //                        //For build profiles that contain more than one modules entry,
                   //                        //allow overrides for the properties that set for the whole build,
                   //                        //for example a different set of pragmas for this module.
                   //                        //The override's value is an object that can
                   //                        //contain any of the other build options in this file.
                   //                        override: {
                   //                            pragmas: {
                   //                                fooExclude: true
                   //                            }
                   //                        }
                   //                    },
                   
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
