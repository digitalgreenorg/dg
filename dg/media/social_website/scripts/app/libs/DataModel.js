define(function(require) {
    'use strict';

    var EventManager = require('framework/EventManager');

    var DataModel = EventManager.extend({

        _state: undefined,
        _data: undefined,

        constructor: function(indexed) {
            this._state = {};

            this._state.indexed = !!indexed;

            this._initData();
        },

        _initData: function() {
            if (this._state.indexed) {
                this._data = [];
            } else {
                this._data = {};
            }
        },

        addSubModel: function(key, indexed) {
            if (key in this._data && this._data[key] instanceof DataModel) {
                return this.get(key);
            } else {
                return this.set(key, new DataModel(indexed));
            }
        },

        isSet: function(key) {
            return key in this._data && this._data[key] != undefined;
        },

        set: function(key, value) {
            this._data[key] = value;
            return this._data[key];
        },

        push: function(value) {
            if (!this._state.indexed) {
                throw new TypeError('DataModel.add(): Attempting to push to a non-indexed model');
            }

            var newArrayIndex = this._data.push(value) - 1;
            return this._data[newArrayIndex];
        },

        get: function(key) {
            if (key == undefined) {
                return this._data;
            } else {
                return this._data[key];
            }
        },

        addSubset: function(arr, start, count) {
            if (arr == undefined) {
                // TODO: Not sure if we want to throw here or exit silenthly.
                // This function will often, if not always be called as a result
                // of an ajax request, and we cannot always guarantee the structure
                // of the data that comes back; however, silent exit makes things
                // very hard to debug.

                throw new Error('DataModel.addSubset(): no data provided to add');

                return false;
            }

            if (count == undefined) {
                count = arr.length;
            }

            var i = 0;
            for (; i < count; i++) {
                this.set(start++, arr[i]);
            }
        },

        hasSubset: function(start, amount) {
            if (this.get(start) == undefined) {
                return false;
            }

            return true;
        },

        getSubset: function(start, amount) {
            if (!this._state.indexed) {
                throw new TypeError('DataModel.getSubset(): Attempting to retrieve a subset of a non-indexed model');
            }

            if (!this.hasSubset(start)) {
                return false;
            }

            var returnArr = [];

            var i = start;
            var len = start + amount;
            for (; i < len; i++) {
                var currentItem = this.get(i);
                if (currentItem == undefined) {
                    continue;
                }

                returnArr.push(currentItem);
            }

            return returnArr;
        },

        clear: function() {
            this._initData();
            return this;
        }
    });

    return DataModel;
});
