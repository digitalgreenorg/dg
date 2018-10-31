define(function() {
    "use strict";

    var Validator = {
        // static declaration for validation type fields
        VALIDATION_TYPES: {
            // true, false, 1, 0
            BOOL: 0,
            // numeric
            NUMBER: 1,
            // integer
            INT: 2,
            // integer >= 0
            UINT: 3,
            // string
            STRING: 4
        },

        validate: function(value, type) {
            switch (type) {
                case this.VALIDATION_TYPES.BOOL:
                    return this.isBool(value);
                case this.VALIDATION_TYPES.NUMBER:
                    return this.isNumeric(value);
                case this.VALIDATION_TYPES.INT:
                    return this.isInt(value);
                case this.VALIDATION_TYPES.UINT:
                    return this.isUInt(value);
                case this.VALIDATION_TYPES.STRING:
                    return this.isString(value);
                default:
                    throw 'ERROR: Validator: Invalid validation type provided';
                    return;
            }
        },

        isBool: function(value) {
            return (value === true || value === false || value === 1 || value === 0);
        },

        isNumeric: function(value) {
            return typeof value == 'number' && isFinite(value);
        },

        isInt: function(value) {
            return this.isNumeric(value) && parseInt(value, 10) === value;
        },

        isUInt: function(value) {
            return this.isInt(value) && value >= 0;
        },

        isString: function(value) {
            return typeof value == 'string';
        }
    };

    return Validator;
});