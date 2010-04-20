/**
 * jquery.deserialize.js
 * Adds deserialize() method to jQuery
 *
 * @author Maxim Vasiliev (max-at-work@yandex.ru)
 */
(function($) {

	$.fn.extend({
		/**
		 * Fills form fields using serialized data
		 * @param {String} queryString Serialized form data
		 */
		deserialize: function(queryString) {
			var keyValuePairs = queryString.split("&");
			
			var formValues = {};
			var formElements = {};
			
			for (var i = 0; i < keyValuePairs.length; i++)
			{
				var pair = keyValuePairs[i].split("=", 2);
				if (pair.length > 1)
				{
					if (typeof formElements[pair[0]] == "undefined")
					{
					    var currInput = $("[name='" + pair[0] + "']", this);
					    if ( currInput.length == 0 ) continue;
						formElements[pair[0]] = currInput;
				    }
						
					// We need arrays for checkboxes/selects/radios
					var isSelect = formElements[pair[0]].get(0).nodeName.toLowerCase() == "select";
					var isInput = formElements[pair[0]].get(0).nodeName.toLowerCase() == "input";
					var isRadio = isInput && formElements[pair[0]].attr("type") == "radio";
					var isCheckbox = isInput && formElements[pair[0]].attr("type") == "checkbox";
					
					pair[1] = pair[1].split("+").join(" ");
					
					if ( isSelect || isRadio || isCheckbox )
					{
						if (!formValues[pair[0]]) formValues[pair[0]] = [];
						formValues[pair[0]][formValues[pair[0]].length] = decodeURIComponent(pair[1]);
					}
					else
					{
						formValues[pair[0]] = decodeURIComponent(pair[1]);
					}
				}
			}
			
			for ( var fieldName in formValues )
			{
				formElements[fieldName].val(formValues[fieldName]);	
				formElements[fieldName].change();
			}
		}
	});
})(jQuery);
