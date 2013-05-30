/**
 * ProfileController Class File
 *
 * @author rdeluca
 * @version $Id$
 * @requires require.js
 * @requires jQuery
 */

define(function(require) {
    'use strict';

    var DigitalGreenPageController = require('app/controllers/DigitalGreenPageController');
    var jQuery = require('jquery');

    var GenericCollectionsDataFeed = require('app/libs/GenericCollectionsDataFeed');
    var ProfileCollectionsViewController = require('app/view-controllers/profile/ProfileCollectionsViewController');
    var ActivitiesViewController = require('app/view-controllers/profile/ActivitiesViewController');
    var PartnerFarmersViewController = require('app/view-controllers/PartnerFarmersViewController');
    var ProfileController = DigitalGreenPageController.extend({

        /**
         * Controller constructor
         * @return {ProfileController} this
         */
        constructor: function(bootstrapConfig, globalHelpers) {
            this.base(bootstrapConfig, globalHelpers);

            return this;
        },

        _initReferences: function($referenceBase, params) {
            this.base($referenceBase);

            var references = this._references;

            //var $profileWrapper = jQuery('.js-profile-wrapper');
            //references.profileCollectionsViewController = new ProfileCollectionsViewController($profileWrapper);

            //var $activitiesContainer = jQuery('.js-activities-container');
            //references.activitiesViewController = new ActivitiesViewController($activitiesContainer);
            
            var $partnerFarmersCarouselContainer = jQuery(".js-partner-farmers-carousel-container");
            references.partnerFarmersViewController = new PartnerFarmersViewController($partnerFarmersCarouselContainer);
        },

        /**
         * Controller destructor
         * @return {void}
         */
        destroy: function() {
            this.base();
        }
    });

    return ProfileController;
});
