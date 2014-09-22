'use strict';

requirejs.config({
    baseUrl: '/media/social_website/build/',

    paths: {
        framework: 'libs/framework',
        controllers: 'app/controllers',
        jquery: 'libs/external/jquery-1.8.3.min',
        appConfig: 'appConfig',
        appcommon: 'appcommon',
        bootstrap_modal: 'libs/external/bootstrap-modal',
        datatables: 'libs/external/jquery.dataTables',
        TableTools: 'libs/external/dataTables.tableTools'
    },
    shim: {
        'bootstrap_modal': {
            deps: ['jquery'],
        },
    }  
});

require([
    'libs/external/requirejs/domReady',
    'framework/Bootstrap',
    'bootstrap_modal',
    'appcommon'
], function(
    domReady,
    Bootstrap
) {
    domReady(function() {
        new Bootstrap();
    });
});

