//The entry point of application. Configures requirejs, loads "app" module
require.config({
    paths: {
        'hm': 'libs/hm',
        'jquery': 'libs/jquery.min',
        'underscore': 'libs/backbone/underscore-min',
        'backbone': 'libs/backbone/backbone-min',
        'indexeddb-backbone': 'libs/indexeddb-backbonejs-adapter/backbone-indexeddb',
        'datatable': 'libs/datatablejs_media/js/jquery.dataTables.min',
        'form_field_validator': 'libs/jquery.validate',
        'layoutmanager': 'libs/layoutmanager/backbone.layoutmanager',
        'syphon': 'libs/backbone.syphon',
        'bootstrapjs': 'libs/bootstrap/js/bootstrap.min',
        'chosen': 'libs/chosen/chosen.jquery.min',
        'date_picker': 'libs/bootstrap/js/bootstrap-datepicker',
        'time_picker': 'libs/bootstrap/js/bootstrap-timepicker.min',
        'jquery_cookie': 'libs/jquery.cookie',
        'tabletools': 'libs/tabletools_media/js/Tabletools',
        'zeroclipboard': 'libs/tabletools_media/js/ZeroClipboard.min',
        'configs': '../../../configs',
    },

    //specifying dependencies of non-amd libraries
    shim: {
        'backbone': {
            //These script dependencies should be loaded before loading backbone.js
            deps: ['underscore', 'jquery'],
            exports: 'Backbone'
        },
        'indexeddb-backbone': {
            deps: ['backbone'],
        },
        'layoutmanager': {
            deps: ['backbone'],
        },
        'bootstrapjs': {
            deps: ['jquery'],
        },
        'underscore': {
            deps: ['jquery'],
            exports: "_"
        },
        'datatable': {
            deps: ["jquery"]
        },
        'zeroclipboard': {
    		deps:['jquery']
        },
        'tabletools': {
    		deps:['jquery', 'datatable','zeroclipboard']
        },
        'form_field_validator': {
            deps: ["jquery"]
        },

        'syphon': {
            deps: ["jquery", "backbone"]
        },

        'bootstrapjs': {
            deps: ["jquery"]
        },
        'chosen': {
            deps: ["jquery"]
        },
        'date_picker': {
            deps: ["jquery"]
        },
        'time_picker': {
            deps: ["jquery"]
        },


    }
});

require(['app'], function(app) {
    //load and initialize app module
    app.initialize();
});
