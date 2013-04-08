'use strict';

requirejs.config({
    baseUrl: '{{STATIC_URL}}social_website/scripts/',

    paths: {
        framework: 'libs/framework',
        controllers: 'app/controllers',
        jquery: 'libs/external/jquery-1.8.3.min'
    },
    shim: {}
});


require([
    'libs/external/requirejs/domReady',
    'framework/Bootstrap'
], function(
    domReady,
    Bootstrap
) {
    domReady(function() {
        new Bootstrap();
    });
});

