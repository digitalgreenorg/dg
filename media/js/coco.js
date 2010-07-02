// FROM: /media/js/jquery.deserialize.js
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



// FROM: /media/js/jquery.progressbar.js
/*
 * jQuery Progress Bar plugin
 * Version 1.1.0 (06/20/2008)
 * @requires jQuery v1.2.1 or later
 *
 * Copyright (c) 2008 Gary Teo
 * http://t.wits.sg

USAGE:
	$(".someclass").progressBar();
	$("#progressbar").progressBar();
	$("#progressbar").progressBar(45);							// percentage
	$("#progressbar").progressBar({showText: false });			// percentage with config
	$("#progressbar").progressBar(45, {showText: false });		// percentage with config
*/
(function($) {
	$.extend({
		progressBar: new function() {

			this.defaults = {
				increment	: 2,
				speed		: 15,
				showText	: true,											// show text with percentage in next to the progressbar? - default : true
				width		: 120,											// Width of the progressbar - don't forget to adjust your image too!!!
				boxImage	: 'images/progressbar.gif',		// boxImage : image around the progress bar
				barImage	: 'images/progressbg_green.gif',	// Image to use in the progressbar. Can be an array of images too.
				height		: 12											// Height of the progressbar - don't forget to adjust your image too!!!
			};
			
			/* public methods */
			this.construct = function(arg1, arg2) {
				var argpercentage	= null;
				var argconfig		= null;
				
				if (arg1 != null) {
					if (!isNaN(arg1)) {
						argpercentage 	= arg1;
						if (arg2 != null) {
							argconfig	= arg2; }
					} else {
						argconfig		= arg1; 
					}
				}
				
				return this.each(function(child) {
					var pb		= this;
					if (argpercentage != null && this.bar != null && this.config != null) {
						this.config.tpercentage	= argpercentage;
						if (argconfig != null)
							pb.config			= $.extend(this.config, argconfig);
					} else {
						var $this				= $(this);
						var config				= $.extend({}, $.progressBar.defaults, argconfig);
						var percentage			= argpercentage;
						if (argpercentage == null)
							var percentage		= $this.html().replace("%","");	// parsed percentage
						
						
						$this.html("");
						var bar					= document.createElement('img');
						var text				= document.createElement('span');
						bar.id 					= this.id + "_percentImage";
						text.id 				= this.id + "_percentText";
						bar.src					= config.boxImage;
						bar.width				= config.width;
						var $bar				= $(bar);
						var $text				= $(text);
						
						this.bar				= $bar;
						this.ntext				= $text;
						this.config				= config;
						this.config.cpercentage	= 0;
						this.config.tpercentage	= percentage;
						
						$bar.css("width", config.width + "px");
						$bar.css("height", config.height + "px");
						$bar.css("background-image", "url(" + config.barImage + ")");
						$bar.css("padding", "0");
						$bar.css("margin", "0");
						$this.append($bar);
						$this.append($text);
						
						bar.alt				= this.tpercentage;
						bar.title			= this.tpercentage;
					}
					
					
					
					var t = setInterval(function() {
						var config		= pb.config;
						var cpercentage = parseInt(config.cpercentage);
						var tpercentage = parseInt(config.tpercentage);
						var increment	= parseInt(config.increment);
						var bar			= pb.bar;
						var text		= pb.ntext;
						var pixels		= config.width / 100;			// Define how many pixels go into 1%
						
						bar.css("background-position", (((config.width * -1)) + (cpercentage * pixels)) + 'px 50%');
						
						if (config.showText)
							text.html(" " + Math.round(cpercentage) + "%");
						
						if (cpercentage > tpercentage) {
							if (cpercentage - increment  < tpercentage) {
								pb.config.cpercentage = 0 + tpercentage
							} else {
								pb.config.cpercentage -= increment;
							}
						}
						else if (pb.config.cpercentage < pb.config.tpercentage) {
							if (cpercentage + increment  > tpercentage) {
								pb.config.cpercentage = tpercentage
							} else {
								pb.config.cpercentage += increment;
							}
						} 
						else {
							clearInterval(t);
						}
					}, pb.config.speed); 
				});
			};
		}
	});
		
	$.fn.extend({
        progressBar: $.progressBar.construct
	});
	
})(jQuery);


// FROM: /media/js/a

/* gettext library */

var catalog = new Array();

function pluralidx(count) { return (count == 1) ? 0 : 1; }


function gettext(msgid) {
  var value = catalog[msgid];
  if (typeof(value) == 'undefined') {
    return msgid;
  } else {
    return (typeof(value) == 'string') ? value : value[0];
  }
}

function ngettext(singular, plural, count) {
  value = catalog[singular];
  if (typeof(value) == 'undefined') {
    return (count == 1) ? singular : plural;
  } else {
    return value[pluralidx(count)];
  }
}

function gettext_noop(msgid) { return msgid; }

function interpolate(fmt, obj, named) {
  if (named) {
    return fmt.replace(/%\(\w+\)s/g, function(match){return String(obj[match.slice(2,-2)])});
  } else {
    return fmt.replace(/%s/g, function(match){return String(obj.shift())});
  }
}




// FROM: /media/js/core.js
// Core javascript helper functions

// basic browser identification & version
var isOpera = (navigator.userAgent.indexOf("Opera")>=0) && parseFloat(navigator.appVersion);
var isIE = ((document.all) && (!isOpera)) && parseFloat(navigator.appVersion.split("MSIE ")[1].split(";")[0]);

// Cross-browser event handlers.
function addEvent(obj, evType, fn) {
    if (obj.addEventListener) {
        obj.addEventListener(evType, fn, false);
        return true;
    } else if (obj.attachEvent) {
        var r = obj.attachEvent("on" + evType, fn);
        return r;
    } else {
        return false;
    }
}

function removeEvent(obj, evType, fn) {
    if (obj.removeEventListener) {
        obj.removeEventListener(evType, fn, false);
        return true;
    } else if (obj.detachEvent) {
        obj.detachEvent("on" + evType, fn);
        return true;
    } else {
        return false;
    }
}

// quickElement(tagType, parentReference, textInChildNode, [, attribute, attributeValue ...]);
function quickElement() {
    var obj = document.createElement(arguments[0]);
    if (arguments[2] != '' && arguments[2] != null) {
        var textNode = document.createTextNode(arguments[2]);
        obj.appendChild(textNode);
    }
    var len = arguments.length;
    for (var i = 3; i < len; i += 2) {
        obj.setAttribute(arguments[i], arguments[i+1]);
    }
    arguments[1].appendChild(obj);
    return obj;
}

// ----------------------------------------------------------------------------
// Cross-browser xmlhttp object
// from http://jibbering.com/2002/4/httprequest.html
// ----------------------------------------------------------------------------
var xmlhttp;
/*@cc_on @*/
/*@if (@_jscript_version >= 5)
    try {
        xmlhttp = new ActiveXObject("Msxml2.XMLHTTP");
    } catch (e) {
        try {
            xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
        } catch (E) {
            xmlhttp = false;
        }
    }
@else
    xmlhttp = false;
@end @*/
if (!xmlhttp && typeof XMLHttpRequest != 'undefined') {
  xmlhttp = new XMLHttpRequest();
}

// ----------------------------------------------------------------------------
// Find-position functions by PPK
// See http://www.quirksmode.org/js/findpos.html
// ----------------------------------------------------------------------------
function findPosX(obj) {
    var curleft = 0;
    if (obj.offsetParent) {
        while (obj.offsetParent) {
            curleft += obj.offsetLeft - ((isOpera) ? 0 : obj.scrollLeft);
            obj = obj.offsetParent;
        }
        // IE offsetParent does not include the top-level 
        if (isIE && obj.parentElement){
            curleft += obj.offsetLeft - obj.scrollLeft;
        }
    } else if (obj.x) {
        curleft += obj.x;
    }
    return curleft;
}

function findPosY(obj) {
    var curtop = 0;
    if (obj.offsetParent) {
        while (obj.offsetParent) {
            curtop += obj.offsetTop - ((isOpera) ? 0 : obj.scrollTop);
            obj = obj.offsetParent;
        }
        // IE offsetParent does not include the top-level 
        if (isIE && obj.parentElement){
            curtop += obj.offsetTop - obj.scrollTop;
        }
    } else if (obj.y) {
        curtop += obj.y;
    }
    return curtop;
}

//-----------------------------------------------------------------------------
// Date object extensions
// ----------------------------------------------------------------------------
Date.prototype.getCorrectYear = function() {
    // Date.getYear() is unreliable --
    // see http://www.quirksmode.org/js/introdate.html#year
    var y = this.getYear() % 100;
    return (y < 38) ? y + 2000 : y + 1900;
}

Date.prototype.getTwoDigitMonth = function() {
    return (this.getMonth() < 9) ? '0' + (this.getMonth()+1) : (this.getMonth()+1);
}

Date.prototype.getTwoDigitDate = function() {
    return (this.getDate() < 10) ? '0' + this.getDate() : this.getDate();
}

Date.prototype.getTwoDigitHour = function() {
    return (this.getHours() < 10) ? '0' + this.getHours() : this.getHours();
}

Date.prototype.getTwoDigitMinute = function() {
    return (this.getMinutes() < 10) ? '0' + this.getMinutes() : this.getMinutes();
}

Date.prototype.getTwoDigitSecond = function() {
    return (this.getSeconds() < 10) ? '0' + this.getSeconds() : this.getSeconds();
}

Date.prototype.getISODate = function() {
    return this.getCorrectYear() + '-' + this.getTwoDigitMonth() + '-' + this.getTwoDigitDate();
}

Date.prototype.getHourMinute = function() {
    return this.getTwoDigitHour() + ':' + this.getTwoDigitMinute();
}

Date.prototype.getHourMinuteSecond = function() {
    return this.getTwoDigitHour() + ':' + this.getTwoDigitMinute() + ':' + this.getTwoDigitSecond();
}

// ----------------------------------------------------------------------------
// String object extensions
// ----------------------------------------------------------------------------
String.prototype.pad_left = function(pad_length, pad_string) {
    var new_string = this;
    for (var i = 0; new_string.length < pad_length; i++) {
        new_string = pad_string + new_string;
    }
    return new_string;
}

// ----------------------------------------------------------------------------
// Get the computed style for and element
// ----------------------------------------------------------------------------
function getStyle(oElm, strCssRule){
    var strValue = "";
    if(document.defaultView && document.defaultView.getComputedStyle){
        strValue = document.defaultView.getComputedStyle(oElm, "").getPropertyValue(strCssRule);
    }
    else if(oElm.currentStyle){
        strCssRule = strCssRule.replace(/\-(\w)/g, function (strMatch, p1){
            return p1.toUpperCase();
        });
        strValue = oElm.currentStyle[strCssRule];
    }
    return strValue;
}



// FROM: /media/js/admin/RelatedObjectLookups.js
// Handles related-objects functionality: lookup link for raw_id_fields
// and Add Another links.

function html_unescape(text) {
    // Unescape a string that was escaped using django.utils.html.escape.
    text = text.replace(/&lt;/g, '<');
    text = text.replace(/&gt;/g, '>');
    text = text.replace(/&quot;/g, '"');
    text = text.replace(/&#39;/g, "'");
    text = text.replace(/&amp;/g, '&');
    return text;
}

// IE doesn't accept periods or dashes in the window name, but the element IDs
// we use to generate popup window names may contain them, therefore we map them
// to allowed characters in a reversible way so that we can locate the correct 
// element when the popup window is dismissed.
function id_to_windowname(text) {
    text = text.replace(/\./g, '__dot__');
    text = text.replace(/\-/g, '__dash__');
    return text;
}

function windowname_to_id(text) {
    text = text.replace(/__dot__/g, '.');
    text = text.replace(/__dash__/g, '-');
    return text;
}

function showRelatedObjectLookupPopup(triggeringLink) {
    var name = triggeringLink.id.replace(/^lookup_/, '');
    name = id_to_windowname(name);
    var href;
    if (triggeringLink.href.search(/\?/) >= 0) {
        href = triggeringLink.href + '&pop=1';
    } else {
        href = triggeringLink.href + '?pop=1';
    }
    var win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
    win.focus();
    return false;
}

function dismissRelatedLookupPopup(win, chosenId) {
    var name = windowname_to_id(win.name);
    var elem = document.getElementById(name);
    if (elem.className.indexOf('vManyToManyRawIdAdminField') != -1 && elem.value) {
        elem.value += ',' + chosenId;
    } else {
        document.getElementById(name).value = chosenId;
    }
    win.close();
}

function showAddAnotherPopup(triggeringLink) {
    var name = triggeringLink.id.replace(/^add_/, '');
    name = id_to_windowname(name);
    href = triggeringLink.href
    if (href.indexOf('?') == -1) {
        href += '?_popup=1';
    } else {
        href  += '&_popup=1';
    }
    var win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
    win.focus();
    return false;
}

function dismissAddAnotherPopup(win, newId, newRepr) {
    // newId and newRepr are expected to have previously been escaped by
    // django.utils.html.escape.
    newId = html_unescape(newId);
    newRepr = html_unescape(newRepr);
    var name = windowname_to_id(win.name);
    var elem = document.getElementById(name);
    if (elem) {
        if (elem.nodeName == 'SELECT') {
            var o = new Option(newRepr, newId);
            elem.options[elem.options.length] = o;
            o.selected = true;
        } else if (elem.nodeName == 'INPUT') {
            if (elem.className.indexOf('vManyToManyRawIdAdminField') != -1 && elem.value) {
                elem.value += ',' + newId;
            } else {
                elem.value = newId;
            }
        }
    } else {
        var toId = name + "_to";
        elem = document.getElementById(toId);
        var o = new Option(newRepr, newId);
        SelectBox.add_to_cache(toId, o);
        SelectBox.redisplay(toId);
    }
    win.close();
}



// FROM: /media/js/admin/DateTimeShortcuts.js
// Inserts shortcut buttons after all of the following:
//     <input type="text" class="vDateField">
//     <input type="text" class="vTimeField">

var DateTimeShortcuts = {
    calendars: [],
    calendarInputs: [],
    clockInputs: [],
    calendarDivName1: 'calendarbox', // name of calendar <div> that gets toggled
    calendarDivName2: 'calendarin',  // name of <div> that contains calendar
    calendarLinkName: 'calendarlink',// name of the link that is used to toggle
    clockDivName: 'clockbox',        // name of clock <div> that gets toggled
    clockLinkName: 'clocklink',      // name of the link that is used to toggle
    admin_media_prefix: '',
    init: function() {
        // Deduce admin_media_prefix by looking at the <script>s in the
        // current document and finding the URL of *this* module.
        var scripts = document.getElementsByTagName('script');
        for (var i=0; i<scripts.length; i++) {
            if (scripts[i].src.match(/DateTimeShortcuts/)) {
                var idx = scripts[i].src.indexOf('js/admin/DateTimeShortcuts');
                DateTimeShortcuts.admin_media_prefix = scripts[i].src.substring(0, idx);
                break;
            }
        }

        var inputs = document.getElementsByTagName('input');
        for (i=0; i<inputs.length; i++) {
            var inp = inputs[i];
            if (inp.getAttribute('type') == 'text' && inp.className.match(/vTimeField/)) {
                DateTimeShortcuts.addClock(inp);
            }
            else if (inp.getAttribute('type') == 'text' && inp.className.match(/vDateField/)) {
                DateTimeShortcuts.addCalendar(inp);
            }
        }
    },
    // Add clock widget to a given field
    addClock: function(inp) {
        var num = DateTimeShortcuts.clockInputs.length;
        DateTimeShortcuts.clockInputs[num] = inp;

        // Shortcut links (clock icon and "Now" link)
        var shortcuts_span = document.createElement('span');
        inp.parentNode.insertBefore(shortcuts_span, inp.nextSibling);
        var now_link = document.createElement('a');
        now_link.setAttribute('href', "javascript:DateTimeShortcuts.handleClockQuicklink(" + num + ", new Date().getHourMinuteSecond());");
        now_link.appendChild(document.createTextNode(gettext('Now')));
        var clock_link = document.createElement('a');
        clock_link.setAttribute('href', 'javascript:DateTimeShortcuts.openClock(' + num + ');');
        clock_link.id = DateTimeShortcuts.clockLinkName + num;
        quickElement('img', clock_link, '', 'src', DateTimeShortcuts.admin_media_prefix + '/media/img/admin/icon_clock.gif', 'alt', gettext('Clock'));
        shortcuts_span.appendChild(document.createTextNode('\240'));
        shortcuts_span.appendChild(now_link);
        shortcuts_span.appendChild(document.createTextNode('\240|\240'));
        shortcuts_span.appendChild(clock_link);

        // Create clock link div
        //
        // Markup looks like:
        // <div id="clockbox1" class="clockbox module">
        //     <h2>Choose a time</h2>
        //     <ul class="timelist">
        //         <li><a href="#">Now</a></li>
        //         <li><a href="#">Midnight</a></li>
        //         <li><a href="#">6 a.m.</a></li>
        //         <li><a href="#">Noon</a></li>
        //     </ul>
        //     <p class="calendar-cancel"><a href="#">Cancel</a></p>
        // </div>

        var clock_box = document.createElement('div');
        clock_box.style.display = 'none';
        clock_box.style.position = 'absolute';
        clock_box.className = 'clockbox module';
        clock_box.setAttribute('id', DateTimeShortcuts.clockDivName + num);
        document.body.appendChild(clock_box);
        addEvent(clock_box, 'click', DateTimeShortcuts.cancelEventPropagation);

        quickElement('h2', clock_box, gettext('Choose a time'));
        time_list = quickElement('ul', clock_box, '');
        time_list.className = 'timelist';
        quickElement("a", quickElement("li", time_list, ""), gettext("Now"), "href", "javascript:DateTimeShortcuts.handleClockQuicklink(" + num + ", new Date().getHourMinuteSecond());")
        quickElement("a", quickElement("li", time_list, ""), gettext("Midnight"), "href", "javascript:DateTimeShortcuts.handleClockQuicklink(" + num + ", '00:00:00');")
        quickElement("a", quickElement("li", time_list, ""), gettext("6 a.m."), "href", "javascript:DateTimeShortcuts.handleClockQuicklink(" + num + ", '06:00:00');")
        quickElement("a", quickElement("li", time_list, ""), gettext("Noon"), "href", "javascript:DateTimeShortcuts.handleClockQuicklink(" + num + ", '12:00:00');")

        cancel_p = quickElement('p', clock_box, '');
        cancel_p.className = 'calendar-cancel';
        quickElement('a', cancel_p, gettext('Cancel'), 'href', 'javascript:DateTimeShortcuts.dismissClock(' + num + ');');
    },
    openClock: function(num) {
        var clock_box = document.getElementById(DateTimeShortcuts.clockDivName+num)
        var clock_link = document.getElementById(DateTimeShortcuts.clockLinkName+num)
    
        // Recalculate the clockbox position
        // is it left-to-right or right-to-left layout ?
        if (getStyle(document.body,'direction')!='rtl') {
            clock_box.style.left = findPosX(clock_link) + 17 + 'px';
        }
        else {
            // since style's width is in em, it'd be tough to calculate
            // px value of it. let's use an estimated px for now
            // TODO: IE returns wrong value for findPosX when in rtl mode
            //       (it returns as it was left aligned), needs to be fixed.
            clock_box.style.left = findPosX(clock_link) - 110 + 'px';
        }
        clock_box.style.top = findPosY(clock_link) - 30 + 'px';
    
        // Show the clock box
        clock_box.style.display = 'block';
        addEvent(window.document, 'click', function() { DateTimeShortcuts.dismissClock(num); return true; });
    },
    dismissClock: function(num) {
       document.getElementById(DateTimeShortcuts.clockDivName + num).style.display = 'none';
       window.document.onclick = null;
    },
    handleClockQuicklink: function(num, val) {
       DateTimeShortcuts.clockInputs[num].value = val;
       DateTimeShortcuts.dismissClock(num);
    },
    // Add calendar widget to a given field.
    addCalendar: function(inp) {
        var num = DateTimeShortcuts.calendars.length;

        DateTimeShortcuts.calendarInputs[num] = inp;

        // Shortcut links (calendar icon and "Today" link)
        var shortcuts_span = document.createElement('span');
        inp.parentNode.insertBefore(shortcuts_span, inp.nextSibling);
        var today_link = document.createElement('a');
        today_link.setAttribute('href', 'javascript:DateTimeShortcuts.handleCalendarQuickLink(' + num + ', 0);');
        today_link.appendChild(document.createTextNode(gettext('Today')));
        var cal_link = document.createElement('a');
        cal_link.setAttribute('href', 'javascript:DateTimeShortcuts.openCalendar(' + num + ');');
        cal_link.id = DateTimeShortcuts.calendarLinkName + num;
        quickElement('img', cal_link, '', 'src', DateTimeShortcuts.admin_media_prefix + '/media/img/admin/icon_calendar.gif', 'alt', gettext('Calendar'));
        shortcuts_span.appendChild(document.createTextNode('\240'));
        shortcuts_span.appendChild(today_link);
        shortcuts_span.appendChild(document.createTextNode('\240|\240'));
        shortcuts_span.appendChild(cal_link);

        // Create calendarbox div.
        //
        // Markup looks like:
        //
        // <div id="calendarbox3" class="calendarbox module">
        //     <h2>
        //           <a href="#" class="link-previous">&lsaquo;</a>
        //           <a href="#" class="link-next">&rsaquo;</a> February 2003
        //     </h2>
        //     <div class="calendar" id="calendarin3">
        //         <!-- (cal) -->
        //     </div>
        //     <div class="calendar-shortcuts">
        //          <a href="#">Yesterday</a> | <a href="#">Today</a> | <a href="#">Tomorrow</a>
        //     </div>
        //     <p class="calendar-cancel"><a href="#">Cancel</a></p>
        // </div>
        var cal_box = document.createElement('div');
        cal_box.style.display = 'none';
        cal_box.style.position = 'absolute';
        cal_box.className = 'calendarbox module';
        cal_box.setAttribute('id', DateTimeShortcuts.calendarDivName1 + num);
        document.body.appendChild(cal_box);
        addEvent(cal_box, 'click', DateTimeShortcuts.cancelEventPropagation);

        // next-prev links
        var cal_nav = quickElement('div', cal_box, '');
        var cal_nav_prev = quickElement('a', cal_nav, '<', 'href', 'javascript:DateTimeShortcuts.drawPrev('+num+');');
        cal_nav_prev.className = 'calendarnav-previous';
        var cal_nav_next = quickElement('a', cal_nav, '>', 'href', 'javascript:DateTimeShortcuts.drawNext('+num+');');
        cal_nav_next.className = 'calendarnav-next';

        // main box
        var cal_main = quickElement('div', cal_box, '', 'id', DateTimeShortcuts.calendarDivName2 + num);
        cal_main.className = 'calendar';
        DateTimeShortcuts.calendars[num] = new Calendar(DateTimeShortcuts.calendarDivName2 + num, DateTimeShortcuts.handleCalendarCallback(num));
        DateTimeShortcuts.calendars[num].drawCurrent();

        // calendar shortcuts
        var shortcuts = quickElement('div', cal_box, '');
        shortcuts.className = 'calendar-shortcuts';
        quickElement('a', shortcuts, gettext('Yesterday'), 'href', 'javascript:DateTimeShortcuts.handleCalendarQuickLink(' + num + ', -1);');
        shortcuts.appendChild(document.createTextNode('\240|\240'));
        quickElement('a', shortcuts, gettext('Today'), 'href', 'javascript:DateTimeShortcuts.handleCalendarQuickLink(' + num + ', 0);');
        shortcuts.appendChild(document.createTextNode('\240|\240'));
        quickElement('a', shortcuts, gettext('Tomorrow'), 'href', 'javascript:DateTimeShortcuts.handleCalendarQuickLink(' + num + ', +1);');

        // cancel bar
        var cancel_p = quickElement('p', cal_box, '');
        cancel_p.className = 'calendar-cancel';
        quickElement('a', cancel_p, gettext('Cancel'), 'href', 'javascript:DateTimeShortcuts.dismissCalendar(' + num + ');');
    },
    openCalendar: function(num) {
        var cal_box = document.getElementById(DateTimeShortcuts.calendarDivName1+num)
        var cal_link = document.getElementById(DateTimeShortcuts.calendarLinkName+num)
	var inp = DateTimeShortcuts.calendarInputs[num];

	// Determine if the current value in the input has a valid date.
	// If so, draw the calendar with that date's year and month.
	if (inp.value) {
	    var date_parts = inp.value.split('-');
	    var year = date_parts[0];
	    var month = parseFloat(date_parts[1]);
	    if (year.match(/\d\d\d\d/) && month >= 1 && month <= 12) {
		DateTimeShortcuts.calendars[num].drawDate(month, year);
	    }
	}

    
        // Recalculate the clockbox position
        // is it left-to-right or right-to-left layout ?
        if (getStyle(document.body,'direction')!='rtl') {
            cal_box.style.left = findPosX(cal_link) + 17 + 'px';
        }
        else {
            // since style's width is in em, it'd be tough to calculate
            // px value of it. let's use an estimated px for now
            // TODO: IE returns wrong value for findPosX when in rtl mode
            //       (it returns as it was left aligned), needs to be fixed.
            cal_box.style.left = findPosX(cal_link) - 180 + 'px';
        }
        cal_box.style.top = findPosY(cal_link) - 75 + 'px';
    
        cal_box.style.display = 'block';
        addEvent(window.document, 'click', function() { DateTimeShortcuts.dismissCalendar(num); return true; });
    },
    dismissCalendar: function(num) {
        document.getElementById(DateTimeShortcuts.calendarDivName1+num).style.display = 'none';
        window.document.onclick = null;
    },
    drawPrev: function(num) {
        DateTimeShortcuts.calendars[num].drawPreviousMonth();
    },
    drawNext: function(num) {
        DateTimeShortcuts.calendars[num].drawNextMonth();
    },
    handleCalendarCallback: function(num) {
        return "function(y, m, d) { DateTimeShortcuts.calendarInputs["+num+"].value = y+'-'+(m<10?'0':'')+m+'-'+(d<10?'0':'')+d; document.getElementById(DateTimeShortcuts.calendarDivName1+"+num+").style.display='none';}";
    },
    handleCalendarQuickLink: function(num, offset) {
       var d = new Date();
       d.setDate(d.getDate() + offset)
       DateTimeShortcuts.calendarInputs[num].value = d.getISODate();
       DateTimeShortcuts.dismissCalendar(num);
    },
    cancelEventPropagation: function(e) {
        if (!e) e = window.event;
        e.cancelBubble = true;
        if (e.stopPropagation) e.stopPropagation();
    }
}

addEvent(window, 'load', DateTimeShortcuts.init);



// FROM: /media/js/calendar.js
/*
calendar.js - Calendar functions by Adrian Holovaty
*/

function removeChildren(a) { // "a" is reference to an object
    while (a.hasChildNodes()) a.removeChild(a.lastChild);
}

// quickElement(tagType, parentReference, textInChildNode, [, attribute, attributeValue ...]);
function quickElement() {
    var obj = document.createElement(arguments[0]);
    if (arguments[2] != '' && arguments[2] != null) {
        var textNode = document.createTextNode(arguments[2]);
        obj.appendChild(textNode);
    }
    var len = arguments.length;
    for (var i = 3; i < len; i += 2) {
        obj.setAttribute(arguments[i], arguments[i+1]);
    }
    arguments[1].appendChild(obj);
    return obj;
}

// CalendarNamespace -- Provides a collection of HTML calendar-related helper functions
var CalendarNamespace = {
    monthsOfYear: gettext('January February March April May June July August September October November December').split(' '),
    daysOfWeek: gettext('S M T W T F S').split(' '),
    isLeapYear: function(year) {
        return (((year % 4)==0) && ((year % 100)!=0) || ((year % 400)==0));
    },
    getDaysInMonth: function(month,year) {
        var days;
        if (month==1 || month==3 || month==5 || month==7 || month==8 || month==10 || month==12) {
            days = 31;
        }
        else if (month==4 || month==6 || month==9 || month==11) {
            days = 30;
        }
        else if (month==2 && CalendarNamespace.isLeapYear(year)) {
            days = 29;
        }
        else {
            days = 28;
        }
        return days;
    },
    draw: function(month, year, div_id, callback) { // month = 1-12, year = 1-9999
        month = parseInt(month);
        year = parseInt(year);
        var calDiv = document.getElementById(div_id);
        removeChildren(calDiv);
        var calTable = document.createElement('table');
        quickElement('caption', calTable, CalendarNamespace.monthsOfYear[month-1] + ' ' + year);
        var tableBody = quickElement('tbody', calTable);

        // Draw days-of-week header
        var tableRow = quickElement('tr', tableBody);
        for (var i = 0; i < 7; i++) {
            quickElement('th', tableRow, CalendarNamespace.daysOfWeek[i]);
        }

        var startingPos = new Date(year, month-1, 1).getDay();
        var days = CalendarNamespace.getDaysInMonth(month, year);

        // Draw blanks before first of month
        tableRow = quickElement('tr', tableBody);
        for (var i = 0; i < startingPos; i++) {
            var _cell = quickElement('td', tableRow, ' ');
            _cell.style.backgroundColor = '#f3f3f3';
        }

        // Draw days of month
        var currentDay = 1;
        for (var i = startingPos; currentDay <= days; i++) {
            if (i%7 == 0 && currentDay != 1) {
                tableRow = quickElement('tr', tableBody);
            }
            var cell = quickElement('td', tableRow, '');
            quickElement('a', cell, currentDay, 'href', 'javascript:void(' + callback + '('+year+','+month+','+currentDay+'));');
            currentDay++;
        }

        // Draw blanks after end of month (optional, but makes for valid code)
        while (tableRow.childNodes.length < 7) {
            var _cell = quickElement('td', tableRow, ' ');
            _cell.style.backgroundColor = '#f3f3f3';
        }

        calDiv.appendChild(calTable);
    }
}

// Calendar -- A calendar instance
function Calendar(div_id, callback) {
    // div_id (string) is the ID of the element in which the calendar will
    //     be displayed
    // callback (string) is the name of a JavaScript function that will be
    //     called with the parameters (year, month, day) when a day in the
    //     calendar is clicked
    this.div_id = div_id;
    this.callback = callback;
    this.today = new Date();
    this.currentMonth = this.today.getMonth() + 1;
    this.currentYear = this.today.getFullYear();
}
Calendar.prototype = {
    drawCurrent: function() {
        CalendarNamespace.draw(this.currentMonth, this.currentYear, this.div_id, this.callback);
    },
    drawDate: function(month, year) {
        this.currentMonth = month;
        this.currentYear = year;
        this.drawCurrent();
    },
    drawPreviousMonth: function() {
        if (this.currentMonth == 1) {
            this.currentMonth = 12;
            this.currentYear--;
        }
        else {
            this.currentMonth--;
        }
        this.drawCurrent();
    },
    drawNextMonth: function() {
        if (this.currentMonth == 12) {
            this.currentMonth = 1;
            this.currentYear++;
        }
        else {
            this.currentMonth++;
        }
        this.drawCurrent();
    },
    drawPreviousYear: function() {
        this.currentYear--;
        this.drawCurrent();
    },
    drawNextYear: function() {
        this.currentYear++;
        this.drawCurrent();
    }
}



