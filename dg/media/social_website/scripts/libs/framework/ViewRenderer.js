define(function(require) {
    'use strict';

    var RENDERING_ENGINE = 'mustache';

    var jQuery = require('jquery');

    var ViewRenderer = function() {

        /**
         * Internal rendering function based of the desired rendering engine
         */
        this._renderingEngine = undefined;
        this._renderFunction = undefined;

        switch (RENDERING_ENGINE) {
            case 'mustache':
                this._renderingEngine = require('libs/external/mustache');
                this._renderFunction = this._mustacheRender;
                break;
            case 'dust':
                throw new Error('Not implemented');
                break;
            case 'default':
                throw new Error('No rendering engine provided');
                break;
        }
    };

    ViewRenderer.prototype._mustacheRender = function(template, data, callback) {
        var renderedTemplate = this._renderingEngine.render(template, data);

        if (callback && typeof callback == 'function') {
            callback(renderedTemplate);
        }
        
        return renderedTemplate;
    },

    ViewRenderer.prototype.render = function(template, data, callback) {
        return this._renderFunction(template, data, callback);
    };

    ViewRenderer.prototype.renderAppend = function($element, template, data, callback) {
        $element.append(this.render(template, data));
    };

    ViewRenderer.prototype.renderHTML = function($element, template, data, callback) {
        $element.html(this.render(template, data));
    };

    return new ViewRenderer();
});