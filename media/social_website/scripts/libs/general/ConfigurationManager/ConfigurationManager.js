define(
[
    'libs/external/Base',
    'libs/general/ConfigurationManager/ConfigurationOption'
],
function(
    Base,
    ConfigurationOption
) {
    "use strict";

    var ConfigurationManager = Base.extend({
    
        _configurationData: null,

        constructor: function() {
            this._configurationData = {};
        },

        addOption: function(name, value) {
            return this._configurationData[name] = new ConfigurationOption(name, value);
        },
        
        importConfiguration: function(userConfiguration) {
            if (!userConfiguration || typeof userConfiguration != 'object') {
                return;
            }

            var id = null;
            for (id in userConfiguration) {
                if (id in this._configurationData) {
                    this._configurationData[id].setValue(userConfiguration[id]);
                }
            }
        },

        getValue: function(name) {
            if (!this.isOptionPresent(name)) {
                throw 'ERROR: ConfigurationManager: unable to find configuration value for ' + name;
            }

            return this._configurationData[name].getValue();
        },

        setValue: function(name, value) {
            if (!this.isOptionPresent(name)) {
                return false;
            }

            this._configurationData[name].setValue(value);
            return true;
        },

        isOptionPresent: function(name) {
            return (name in this._configurationData);
        },

        isOptionValid: function(name) {
            return this.isOptionPresent(name) && this._configurationData[name].isValid();
        },

        validate: function() {
            for (var key in this._configurationData) {
                this._configurationData[key].validate();
            }
        }
    });

    return ConfigurationManager;
});