define(function(require) {
    'use strict';

    var DigitalGreenPageController = require('controllers/DigitalGreenPageController');
    // var VrpPaymentViewController = require('app/view-controllers/VrpPaymentViewController');
    var jQuery = require('jquery');
//    var dataTables = require('libs/external/jquery.dataTables.min.js');

    var ConnectController = DigitalGreenPageController.extend({

        /**
         * Controller constructor
         * @return {CollectionsController} this
         */
        constructor: function(bootstrapConfig, globalHelpers) {
            this.base(bootstrapConfig, globalHelpers);
            var references = this._references;

            return this;
        },

        _initReferences: function() {
            this.base();
            var references = this._references;
            references.$showMoreButton = jQuery('.js-show-more');
            
        },

        _initEvents: function() {
            this.base();
            var references = this._references;
            var boundFunctions = this._boundFunctions;

            boundFunctions.onShowMoreButtonClick = this._onShowMoreButtonClick.bind(this);
            references.$showMoreButton.on('click', boundFunctions.onShowMoreButtonClick);
        },

        _onShowMoreButtonClick: function(e){
            e.preventDefault();
            var references = this._references;
            var $currentTarget = e.currentTarget;
            var $introText = $($currentTarget).parent().children('p.js-intro')[0]
            if ($($introText).hasClass('line-clamp')){
                $($introText).removeClass("line-clamp");
                $($currentTarget).text("Show Less");
            }
            else{
                $($introText).addClass("line-clamp");
                $($currentTarget).text("Show More");
            }
        },

        /**
         * Controller destructor
         * @return {void}
         */
        destroy: function() {
            this.base();
        }
    });

    return ConnectController;
});
