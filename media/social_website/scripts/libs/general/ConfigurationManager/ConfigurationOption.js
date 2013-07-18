define(function(require) {
    'use strict';

    var Base = require('libs/external/Base');
    var Validator = require('libs/general/Validator');
    var Util = require('framework/Util');

    var ConfigurationOption = Base.extend({
    
        _name: null,
        _value: null,
        _defaultValue: null,
        _validationType: null,
        _allowedValues: null,

        constructor: function(name, value) {
            
            this._name = name;

            if (value !== undefined) {
                this.setValue(value);
            }

            this._allowedValues = [];
            return this;
        },

        setValidationType: function(type) {
            if (Util.Object.inObject(Validator.VALIDATION_TYPES, type)) {
                this._validationType = type;
            }
            return this;
        },

        setAllowedValues: function() {
            this._allowedValues = Array.prototype.slice.call(arguments)[0];

            return this;
        },

        setDefaultValue: function(value) {
            this._defaultValue = value;
            return this;
        },

        setValue: function(value) {
            this._value = value;
            return this;
        },

        getValue: function() {
            return this._value;
        },

        isValid: function() {
            if (this._validationType != null) {
                if (!Validator.validate(this._value, this._validationType)) {
                    return false;
                }
            }

            if (
                !this._isDefaultValue() &&
                this._allowedValues &&
                this._allowedValues.length > 0 &&
                !Util.Array.inArray(this._allowedValues, this._value)
            ) {
                return false;
            }


            return true;
        },

        validate: function() {
            if (!this.isValid()) {
                this._resetToDefault();
            }
        },

        _isDefaultValue: function() {
            return this._value === this._defaultValue;
        },

        _resetToDefault: function() {
            this._value = this._defaultValue;
        }
    });

    return ConfigurationOption;
});