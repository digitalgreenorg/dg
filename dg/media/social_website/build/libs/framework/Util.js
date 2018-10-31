define(function(require) {

    require('framework/misc/polyfills');

    var Util = {};
    Util.Array = {};
    Util.Object = {};
    Util.Math = {};
    Util.Cookie = {};

    /**
     * Object Functions
     */

    // NOTE: there is potential here for issues if the site using this has multiple frames
    Util.Object.clone = function(currentObject, deep) {
        if (deep == null) {
            deep = false;
        }

        var returnClone;
        if (currentObject instanceof Array) {
            returnClone = [];

            var key = null;

            var i = 0;
            var len = currentObject.length;
            for (; i < len; i++) {
                if (currentObject.hasOwnProperty(i)) {
                    var entry = currentObject[i];

                    if (deep && typeof entry == 'object') {
                        entry = this.clone(entry, deep);
                    }

                    returnClone[i] = entry;
                }
            }
        } else {
            returnClone = {};

            var key = null;
            for (key in currentObject) {
                if (currentObject.hasOwnProperty(key)) {
                    var entry = currentObject[key];

                    if (deep && typeof entry == 'object') {
                        entry = this.clone(entry, deep);
                    }

                    returnClone[key] = entry;
                }
            }
        }

        return returnClone;
    };

    Util.Object.extend = function(source, extension, cloneBeforeExtending) {

        if (typeof source != 'object' || typeof extension != 'object') {
            return source;
        }

        if (cloneBeforeExtending) {
            source = Util.Object.clone(source, true);
            extension = Util.Object.clone(extension, true);
        }

        var k;
        for (k in extension) {
            source[k] = extension[k];
        }

        return source;
    };

    Util.Object.inObject = function(obj, value) {
        for (var key in obj) {
            if (obj[key] == value) {
                return true;
            }
        }
        return false;
    };


    /**
     * Array Functions
     */

    Util.Array.clone = Util.Object.clone;

    // TODO: implement a frame friendly version of this?
    Util.Array.isArray = function(candidate) {
        return candidate instanceof Array;
    };

    // NOTE: this is dependent on the polyfill for older IE
    // inArray: function(arr, value) {
    //     // ERROR THROWN IN IE
    //     return (arr.indexOf(value) >= 0) ? true : false;
    // },

    Util.Array.inArray = Util.Object.inObject;


    /**
     * Math functions
     */

    Util.Math.mod = function(a, b) {
        return ((a % b) + b) % b;
    };


    /**
     *
     * @param number
     * @return {String}
     * @see http://stackoverflow.com/a/2901298
     */
    Util.integerCommaFormat = function(number){
        return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    };

    Util.leftPadWithChar = function(value, padlength, char){
        if(char == null){
            char = '0';
        }
        var string = value.toString();
        var l = string.length;
        while (l++ < padlength) {
            string = char + string;
        }
        return string;
    };

    Util.secondsToHMSFormat = function(timeInSeconds){
        var hours = Math.floor( timeInSeconds / 3600) ;
        timeInSeconds %= 3600;
        var minutes = Util.leftPadWithChar(Math.floor(timeInSeconds / 60), 2);
        var seconds = Util.leftPadWithChar(timeInSeconds % 60, 2);

        if(hours){
            var hoursOutput = Util.leftPadWithChar(hours, 2);
            return hoursOutput + ":" + minutes + ":" + seconds;
        } else {
            return minutes + ":" + seconds;
        }
    };
    
    /**
    *
    * @param number
    * @return {String}
    * @see http://stackoverflow.com/questions/9461621
    */
   Util.integerAbbreviatedFormat = function(num){
	   if (num >= 1000000000) {
		   return (num / 1000000000).toFixed(1).replace(/\.0$/, '') + 'G';
	   }
	   if (num >= 1000000) {
		   return (num / 1000000).toFixed(1).replace(/\.0$/, '') + 'M';
	   }
	   if (num >= 1000) {
		   return (num / 1000).toFixed(1).replace(/\.0$/, '') + 'k';
	   }
	   return num;
   };


    /**
     * Cookie Functions
     */
    Util.Cookie.set = function(name, value, daysUntilExpiration) {
        var expirationDate = new Date();

        if (daysUntilExpiration == undefined) {
            daysUntilExpiration = 30;
        }

        // Get unix milliseconds at current time plus number of days
        expirationDate.setTime(+ expirationDate + (daysUntilExpiration * 86400000));

        var cookieString = name + "=" + value + "; expires=" + expirationDate.toGMTString() + "; path=/"

        window.document.cookie = cookieString;
    };
    
    Util.Cookie.get = function(name) {
        return this.getAll()[name];
    };

    Util.Cookie.getAll = function() {
        var c = document.cookie, v = 0, cookies = {};
        if (document.cookie.match(/^\s*\$Version=(?:"1"|1);\s*(.*)/)) {
            c = RegExp.$1;
            v = 1;
        }
        if (v === 0) {
            c.split(/[,;]/).map(function(cookie) {
                var parts = cookie.split(/=/, 2),
                    name = decodeURIComponent(parts[0].trimLeft()),
                    value = parts.length > 1 ? decodeURIComponent(parts[1].trimRight()) : null;
                cookies[name] = value;
            });
        } else {
            c.match(/(?:^|\s+)([!#$%&'*+\-.0-9A-Z^`a-z|~]+)=([!#$%&'*+\-.0-9A-Z^`a-z|~]*|"(?:[\x20-\x7E\x80\xFF]|\\[\x00-\x7F])*")(?=\s*[,;]|$)/g).map(function($0, $1) {
                var name = $0,
                    value = $1.charAt(0) === '"'
                              ? $1.substr(1, -1).replace(/\\(.)/g, "$1")
                              : $1;
                cookies[name] = value;
            });
        }
        return cookies;
    };

    Util.Cookie.remove = function(name) {
        this.set(name, null, -1);
    };

    Util.Cookie.removeAll = function() {
        var allCookies = this.getAll();
        var key;
        for (key in allCookies) {
            this.remove(key);
        }
    };

    // TODO: remove -- testing purposes only
    window.Util = Util;

    return Util;
});