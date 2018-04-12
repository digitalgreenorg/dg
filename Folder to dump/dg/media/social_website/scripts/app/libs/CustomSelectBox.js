define(function(require) {

    var Controller = require('framework/controllers/Controller');
    
    var CustomSelectBox = Controller.extend({

        constructor: function($customSelectElement, params) {

            this.base($customSelectElement);

            this._init();
        },

        _initReferences: function($customSelectElement, params) {
            this.base($customSelectElement);

            var references = this._references;

            references.$customSelectElement = $customSelectElement;
            references.$selectFormElement = $customSelectElement.find('select');
            references.$selectedItemLabel = $customSelectElement.find('.js-selected-item-label');
            references.$selectOptions = $customSelectElement.find('.js-options');
        },

        _initEvents: function(params) {
            this.base();

            var references = this._references;
            var boundFunctions = this._boundFunctions;

            boundFunctions.preventDefault = function(e) {
                e.preventDefault();
            };

            boundFunctions.onCustomSelectClick = this._onCustomSelectClick.bind(this);
            references.$customSelectElement
                .on('click', boundFunctions.onCustomSelectClick)
                .on('mousedown', boundFunctions.preventDefault);

            boundFunctions.onSelectOptionClick = this._onSelectOptionClick.bind(this);
            references.$selectOptions
                .on('click', 'li', boundFunctions.onSelectOptionClick)
                .on('mousedown', boundFunctions.preventDefault);

            boundFunctions.onOutsideClick = this._onOutsideClick.bind(this);
            jQuery('body').on('click', boundFunctions.onOutsideClick);
        },

        _initState: function(params) {
            this.base();

            this._state.isOpen = false;
        },

        _init: function() {
            this.base();

            this._populateOptions();
        },

        _populateOptions: function() {
            var references = this._references;

            var $selectFormElement = references.$selectFormElement;
            var $selectOptions = references.$selectOptions;

            var $selectFormElementOptions = $selectFormElement.find('option');
            var $li;
            var $currentSelectFormElementOption;

            var foundSelected = false;

            var i = 0;
            var len = $selectFormElementOptions.length;
            for (; i < len; i++) {
                $currentSelectFormElementOption = $selectFormElementOptions.eq(i);
                
                var label = $currentSelectFormElementOption.html();
                var value = $currentSelectFormElementOption.attr('value');
                var selected = (
                    $currentSelectFormElementOption.attr('selected') != '' 
                    && $currentSelectFormElementOption.attr('selected') != undefined
                );

                if (selected) {
                    foundSelected = true;
                }

                this.addOption(label, value, selected, false);
            }

            if (!foundSelected) {
                this._markAsSelected($selectOptions.find('li').eq(0));
            }

            $selectOptions.hide();
            $selectFormElement.hide();
        },

        _onCustomSelectClick: function(e) {
            e.preventDefault();
            e.stopPropagation();

            if (!this._state.isOpen) {
                this._showOptions();
            } else {
                this._hideOptions();
            }
        },

        _onSelectOptionClick: function(e) {
            e.preventDefault();
            e.stopPropagation();

            var $option = jQuery(e.currentTarget);
            this._markAsSelected($option);

            this._hideOptions();
        },

        _onOutsideClick: function() {
            this._hideOptions();
        },

        _findByValue: function(value) {
            return this._references.$selectOptions.find('li').filter(function() {
                return (jQuery(this).data('value') == value);
            });
        },

        _markAsSelected: function($option) {
            if ($option == undefined || !$option.length) {
                return false;
            }

            var references = this._references;

            var optionLabel = $option.html();
            var optionValue = $option.data('value');

            references.$selectedItemLabel.html(optionLabel);

            // NOTE: there's a problem here if the form select box didn't have a value set
            // for each option when the _populateOptions was run
            references.$selectFormElement.find('option').attr('selected', false);
            references.$selectFormElement.find('option[value="' + optionValue + '"]').attr('selected', 'selected');

            references.$selectOptions.find('li').not($option).removeClass('selected');
            $option.addClass('selected');

            // send alerts
            this.trigger('optionChanged', optionLabel, optionValue);
        },

        _showOptions: function() {
            this._references.$selectOptions.show();
            this._state.isOpen = true;
        },

        _hideOptions: function() {
            this._references.$selectOptions.hide();
            this._state.isOpen = false;
        },

        addOption: function(label, value, selected, addToFormElement) {
            if (addToFormElement == undefined) {
                addToFormElement = true;
            }

            var references = this._references;

            var $selectOptions = references.$selectOptions;

            $li = jQuery('<li />')
                .html(label)
                .data('value', value)
                .addClass('item');

            $selectOptions.append($li);


            if (addToFormElement) {
                var $option = jQuery('<option />')
                    .html(label)
                    .attr('value', value);

                references.$selectFormElement.append($option);
            }

            if (selected) {
                this._markAsSelected($li);
            }
        },

        setOption: function(value) {
            this._markAsSelected(this._findByValue(value));
        },

        destroy: function() {
            this.base();
        }
    });

    return CustomSelectBox;

});