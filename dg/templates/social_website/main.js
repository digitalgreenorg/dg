'use strict';

requirejs.config({
    baseUrl: '{{STATIC_URL}}social_website/build/',

    paths: {
        framework: 'libs/framework',
        controllers: 'app/controllers',
        jquery: 'libs/external/jquery-1.8.3.min',
        appConfig: 'appConfig',
        bootstrap_modal: 'libs/external/bootstrap-modal'
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
    'bootstrap_modal'
], function(
    domReady,
    Bootstrap
) {
    domReady(function() {
        new Bootstrap();
    });
});

