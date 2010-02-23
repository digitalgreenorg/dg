/**
 * CalendarView for jQuery
 *
 * Based on CalendarView for Prototype http://calendarview.org/ which is based
 * on Dynarch DHTML Calendar http://www.dynarch.com/projects/calendar/old/.
 *
 * CalendarView is licensed under the terms of the GNU Lesser General
 * Public License (LGPL)
 *
 * Usage:
 *   jQuery(document).ready(function() {
 *     $('#date_input').calendar();
 *   }
 *
 *   jQuery(document).ready(function() {
 *     $('#date_input').calendar({triggerElement: '#date_input_trigger'});
 *   }
 *
 *   jQuery(document).ready(function() {
 *     $('#date_input').calendar({parentElement: '#calendar_container'});
 *   }
 *
 * Default options:
 *   triggerElement: null, // Popup calendar
 *   parentElement: null, // Inline calendar
 *   minYear: 1900,
 *   maxYear: 2100,
 *   firstDayOfWeek: 1, // Monday
 *   weekend: "0,6", // Sunday and Saturday
 *   dateFormat: '%Y-%m-%d',
 *   selectHandler: null, // Will use default select handler
 *   closeHandler: null // Will use default close handler
 */
;(function($) {
	var Calendar = function() {
		this.date = new Date();
	};

	//------------------------------------------------------------------------------
	// Constants
	//------------------------------------------------------------------------------

	Calendar.VERSION = '1.2';
	Calendar.TODAY = 'Today';

	Calendar.DAY_NAMES = new Array(
		'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'
	);

	Calendar.SHORT_DAY_NAMES = new Array('Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa');

	Calendar.MONTH_NAMES = new Array(
		'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
		'September', 'October', 'November', 'December'
	);

	Calendar.SHORT_MONTH_NAMES = new Array(
		'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
	);

	Calendar.NAV_PREVIOUS_YEAR  = -2;
	Calendar.NAV_PREVIOUS_MONTH = -1;
	Calendar.NAV_TODAY          =  0;
	Calendar.NAV_NEXT_MONTH     =  1;
	Calendar.NAV_NEXT_YEAR      =  2;

	//------------------------------------------------------------------------------
	// Static Methods
	//------------------------------------------------------------------------------

	/**
	 * This gets called when the user presses a mouse button anywhere in the
	 * document, if the calendar is shown. If the click was outside the open
	 * calendar this function closes it.
	 *
	 * @param event
	 */
	Calendar._checkCalendar = function(event) {
		if (!window._popupCalendar) {
			return false;
		}

		if ($(event.target).parents().index($(window._popupCalendar.container)) >= 0) {
			return false;
		}

		window._popupCalendar.callCloseHandler();
		return event.preventDefault();
	}

	/**
	 * Event Handlers
	 * @param event
	 */
	Calendar.handleMouseDownEvent = function(event){
		$(document).mouseup(Calendar.handleMouseUpEvent);
		event.preventDefault();
	}

	/**
	 * Clicks of different actions
	 * @param event
	 */
	Calendar.handleMouseUpEvent = function(event) {
		var el        = event.target;
		var calendar  = el.calendar;
		var isNewDate = false;

		// If the element that was clicked on does not have an associated Calendar
		// object, return as we have nothing to do.
		if (!calendar) return false

		// Clicked on a day
		if (typeof el.navAction == 'undefined') {
			if (calendar.currentDateElement) {
				calendar.currentDateElement.removeClass('selected');
				$(el).addClass('selected');
				calendar.shouldClose = (calendar.currentDateElement == $(el));
				if (!calendar.shouldClose) {
					calendar.currentDateElement = $(el);
				}
			}
			calendar.date.setDateOnly(el.date);
			isNewDate = true;
			calendar.shouldClose = !$(el).hasClass('otherDay');
			var isOtherMonth     = !calendar.shouldClose;
			if (isOtherMonth) {
				calendar.update(calendar.date);
			}
		} else {
			// Clicked on an action button
			var date = new Date(calendar.date);

			if (el.navAction == Calendar.NAV_TODAY) {
				date.setDateOnly(new Date());
			}

			var year = date.getFullYear();
			var mon = date.getMonth();
			function setMonth(m) {
				var day = date.getDate();
				var max = date.getMonthDays(m);
				if (day > max) date.setDate(max)
					date.setMonth(m);
			}
			switch (el.navAction) {

				// Previous Year
				case Calendar.NAV_PREVIOUS_YEAR:
					if (year > calendar.minYear)
						date.setFullYear(year - 1);
					break;

				// Previous Month
				case Calendar.NAV_PREVIOUS_MONTH:
					if (mon > 0) {
						setMonth(mon - 1);
					}
					else if (year-- > calendar.minYear) {
						date.setFullYear(year);
						setMonth(11);
					}
					break;

				// Today
				case Calendar.NAV_TODAY:
					break;

				// Next Month
				case Calendar.NAV_NEXT_MONTH:
					if (mon < 11) {
						setMonth(mon + 1);
					}
					else if (year < calendar.maxYear) {
						date.setFullYear(year + 1);
						setMonth(0);
					}
					break;

				// Next Year
				case Calendar.NAV_NEXT_YEAR:
					if (year < calendar.maxYear)
						date.setFullYear(year + 1);
					break;

			}

			if (!date.equalsTo(calendar.date)) {
				calendar.shouldClose = false;
				calendar.setDate(date);
				isNewDate = true;
			} else if (el.navAction == 0) {
				isNewDate = (calendar.shouldClose = true);
			}
		}

		if (isNewDate) event && calendar.callSelectHandler();
		if (calendar.shouldClose) event && calendar.callCloseHandler();
		$(document).unbind('mouseup', Calendar.handleMouseUpEvent);
		return event.preventDefault();
	};

	Calendar.defaultSelectHandler = function(calendar) {
		if (!calendar.dateField) {
			return false;
		}

		// Update dateField value
		(calendar.dateField.attr('tagName') == 'INPUT')
			? calendar.dateField.val(calendar.date.print(calendar.dateFormat))
			: calendar.dateField.html(calendar.date.print(calendar.dateFormat));

		// Trigger the onchange callback on the dateField, if one has been defined
		calendar.dateField.trigger('change');

		// Call the close handler, if necessary
		if (calendar.shouldClose) {
			calendar.callCloseHandler();
		}

		return true;
	}

	Calendar.defaultCloseHandler = function(calendar) {
		calendar.hide();
	}

	//------------------------------------------------------------------------------
	// Calendar Instance
	//------------------------------------------------------------------------------

	Calendar.prototype = {
		// The HTML Container Element
		container: null,

		// Dates
		date: null,
		currentDateElement: null,

		// Status
		shouldClose: false,
		isPopup: true,

		/**
		 * Update / (Re)initialize Calendar
		 * @param date
		 */
		update: function(date) {
			var calendar   = this;
			var today      = new Date();
			var thisYear   = today.getFullYear();
			var thisMonth  = today.getMonth();
			var thisDay    = today.getDate();
			var month      = date.getMonth();
			var dayOfMonth = date.getDate();

			// Ensure date is within the defined range
			if (date.getFullYear() < this.minYear) {
				date.setFullYear(this.minYear);
			} else if (date.getFullYear() > this.maxYear) {
				date.setFullYear(this.maxYear);
			}
			this.date = new Date(date);

			// Calculate the first day to display (including the previous month)
			date.setDate(1);
			var day1 = (date.getDay() - this.firstDayOfWeek) % 7;
			if (day1 < 0) day1 += 7;
			date.setDate(-day1);
			date.setDate(date.getDate() + 1);

			// Fill in the days of the month
			$('tbody tr', this.container).each(function() {
				var rowHasDays = false;
				$(this).children().each(function() {
					var day            = date.getDate();
					var dayOfWeek      = date.getDay();
					var isCurrentMonth = (date.getMonth() == month);

					// Reset classes on the cell
					cell = $(this);
					cell.removeAttr('class');
					cell[0].date = new Date(date);
					cell.html(day);

					// Account for days of the month other than the current month
					if (!isCurrentMonth) {
						cell.addClass('otherDay');
					} else {
						rowHasDays = true;
					}

					// Ensure the current day is selected
					if (isCurrentMonth && day == dayOfMonth) {
						cell.addClass('selected');
						calendar.currentDateElement = cell;
					}

					// Today
					if (date.getFullYear() == thisYear && date.getMonth() == thisMonth && day == thisDay) {
						cell.addClass('today');
					}

					// Weekend
					if (calendar.weekend.indexOf(dayOfWeek.toString()) != -1) {
						cell.addClass('weekend');
					}

					// Set the date to tommorrow
					date.setDate(day + 1);
				});
				// Hide the extra row if it contains only days from another month
				!rowHasDays ? $(this).hide() : $(this).show();
			});

			$('td.title', this.container).html(Calendar.MONTH_NAMES[month] + ' ' + calendar.date.getFullYear());
		},

		create: function(parent) {

			// If no parent was specified, assume that we are creating a popup calendar.
			this.isPopup = false;
			if (!parent) {
				parent = $('body');
				this.isPopup = true;
			}

			// Calendar Table
			var table = $('<table />');

			// Calendar Header
			var thead = $('<thead />');
			table.append(thead);

			// Title Placeholder
			var row  = $('<tr />');
			var cell = $('<td colspan="7" class="title" />');
			row.append(cell);
			thead.append(row);

			// Calendar Navigation
			row = $('<tr />');
			this._drawButtonCell(row, '&#x00ab;', 1, Calendar.NAV_PREVIOUS_YEAR);
			this._drawButtonCell(row, '&#x2039;', 1, Calendar.NAV_PREVIOUS_MONTH);
			this._drawButtonCell(row, Calendar.TODAY,    3, Calendar.NAV_TODAY);
			this._drawButtonCell(row, '&#x203a;', 1, Calendar.NAV_NEXT_MONTH);
			this._drawButtonCell(row, '&#x00bb;', 1, Calendar.NAV_NEXT_YEAR);
			thead.append(row);

			// Day Names
			row = $('<tr />');
			for (var i = 0; i < 7; ++i) {
				var realDay = (i + this.firstDayOfWeek) % 7;
				cell = $('<th />').html(Calendar.SHORT_DAY_NAMES[realDay]);
				if (this.weekend.indexOf(realDay.toString()) != -1)
					cell.addClass('weekend');
				row.append(cell);
			}
			thead.append(row);

			// Calendar Days
			var tbody = table.append($('<tbody />'));
			for (i = 6; i > 0; --i) {
				row = $('<tr />').addClass('days');
				tbody.append(row);
				for (var j = 7; j > 0; --j) {
					cell = $('<td />');
					cell[0].calendar = this;
					row.append(cell);
				}
			}

			// Calendar Container (div)
			this.container = $('<div />').addClass('calendar').append(table);
			if (this.isPopup) {
				this.container.css({
					position: 'absolute',
					display: 'none'
				}).addClass('popup');
			}

			// Initialize Calendar
			this.update(this.date);

			// Observe the container for mousedown events
			this.container.mousedown(Calendar.handleMouseDownEvent);

			// Append to parent element
			parent.append(this.container);
		},

		_drawButtonCell: function(parent, text, colSpan, navAction) {
			var cell = $('<td />');
			if (colSpan > 1) cell[0].colSpan = colSpan; // IE issue attr()
			cell.addClass('button').html(text).attr('unselectable', 'on'); // IE;
			cell[0].calendar     = this;
			cell[0].navAction    = navAction;
			parent.append(cell);
			return cell;
		},

		//------------------------------------------------------------------------------
		// Callbacks
		//------------------------------------------------------------------------------

		/**
		 * Calls the Select Handler (if defined)
		 */
		callSelectHandler: function() {
			if (this.selectHandler) {
				this.selectHandler(this, this.date.print(this.dateFormat));
			}
		},

		/**
		 * Calls the Close Handler (if defined)
		 */
		callCloseHandler: function() {
			if (this.closeHandler) {
				this.closeHandler(this);
			}
		},

		//------------------------------------------------------------------------------
		// Calendar Display Functions
		//------------------------------------------------------------------------------

		/**
		 * Shows the Calendar
		 */
		show: function() {
			this.container.show();
			if (this.isPopup) {
				window._popupCalendar = this;
				$(document).mousedown(Calendar._checkCalendar);
			}
		},

		/**
		 * Shows the calendar at the given absolute position
		 * @param x
		 * @param y
		 */
		showAt: function (x, y) {
			this.container.css({
				left: x + 'px',
				top: y + 'px'
			})
			this.show();
		},

		/**
		 * Shows the Calendar at the coordinates of the provided element
		 * @param element
		 */
		showAtElement: function(element) {
			var offset = element.offset();
			this.showAt(offset.left, offset.top);
		},

		/**
		 * Hides the Calendar
		 */
		hide: function() {
			if (this.isPopup) {
				$(document).unbind('mousedown', Calendar._checkCalendar);
			}
			this.container.hide();
		},

		/**
		 * Tries to identify the date represented in a string.  If successful it also
		 * calls this.setDate which moves the calendar to the given date.
		 * @param str
		 * @param format
		 */
		parseDate: function(str, format) {
			if (!format) {
				format = this.dateFormat;
			}
			this.setDate(Date.parseDate(str, format));
		},

		setDate: function(date) {
			if (!date.equalsTo(this.date))
				this.update(date);
		},

		setRange: function(minYear, maxYear) {
			this.minYear = minYear;
			this.maxYear = maxYear;
		}
	}

	// global object that remembers the calendar
	window._popupCalendar = null;

	//==============================================================================
	// Date Object Patches
	// This is pretty much untouched from the original.
	//==============================================================================
	Date.DAYS_IN_MONTH = new Array(31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31);
	Date.SECOND        = 1000; /* milliseconds */
	Date.MINUTE        = 60 * Date.SECOND;
	Date.HOUR          = 60 * Date.MINUTE;
	Date.DAY           = 24 * Date.HOUR;
	Date.WEEK          =  7 * Date.DAY;

	// Parses Date
	Date.parseDate = function(str, fmt) {
		var today = new Date();
		var y     = 0;
		var m     = -1;
		var d     = 0;
		var a     = str.split(/\W+/);
		var b     = fmt.match(/%./g);
		var i     = 0, j = 0;
		var hr    = 0;
		var min   = 0;

		for (i = 0; i < a.length; ++i) {
			if (!a[i]) continue;
			switch (b[i]) {
				case "%d":
				case "%e":
					d = parseInt(a[i], 10);
					break;
				case "%m":
					m = parseInt(a[i], 10) - 1;
					break;
				case "%Y":
				case "%y":
					y = parseInt(a[i], 10);
					(y < 100) && (y += (y > 29) ? 1900 : 2000);
					break;
				case "%b":
				case "%B":
					for (j = 0; j < 12; ++j) {
						if (Calendar.MONTH_NAMES[j].substr(0, a[i].length).toLowerCase() == a[i].toLowerCase()) {
							m = j;
							break;
						}
					}
					break;
				case "%H":
				case "%I":
				case "%k":
				case "%l":
					hr = parseInt(a[i], 10);
					break;
				case "%P":
				case "%p":
					if (/pm/i.test(a[i]) && hr < 12)
						hr += 12;
					else if (/am/i.test(a[i]) && hr >= 12)
						hr -= 12;
					break;
				case "%M":
					min = parseInt(a[i], 10);
					break;
			}
		}
		if (isNaN(y)) y = today.getFullYear();
		if (isNaN(m)) m = today.getMonth();
		if (isNaN(d)) d = today.getDate();
		if (isNaN(hr)) hr = today.getHours();
		if (isNaN(min)) min = today.getMinutes();
		if (y != 0 && m != -1 && d != 0)
			return new Date(y, m, d, hr, min, 0);
		y = 0; m = -1; d = 0;
		for (i = 0; i < a.length; ++i) {
			if (a[i].search(/[a-zA-Z]+/) != -1) {
				var t = -1;
				for (j = 0; j < 12; ++j) {
					if (Calendar.MONTH_NAMES[j].substr(0, a[i].length).toLowerCase() == a[i].toLowerCase()) {
						t = j; break;
					}
				}
				if (t != -1) {
					if (m != -1) {
						d = m+1;
					}
					m = t;
				}
			} else if (parseInt(a[i], 10) <= 12 && m == -1) {
				m = a[i]-1;
			} else if (parseInt(a[i], 10) > 31 && y == 0) {
				y = parseInt(a[i], 10);
				(y < 100) && (y += (y > 29) ? 1900 : 2000);
			} else if (d == 0) {
				d = a[i];
			}
		}
		if (y == 0)
			y = today.getFullYear();
		if (m != -1 && d != 0)
			return new Date(y, m, d, hr, min, 0);
		return today;
	};

	// Returns the number of days in the current month
	Date.prototype.getMonthDays = function(month) {
		var year = this.getFullYear()
		if (typeof month == "undefined")
			month = this.getMonth()
		if (((0 == (year % 4)) && ( (0 != (year % 100)) || (0 == (year % 400)))) && month == 1)
			return 29
		else
			return Date.DAYS_IN_MONTH[month]
	};

	// Returns the number of day in the year
	Date.prototype.getDayOfYear = function() {
		var now = new Date(this.getFullYear(), this.getMonth(), this.getDate(), 0, 0, 0);
		var then = new Date(this.getFullYear(), 0, 0, 0, 0, 0);
		var time = now - then;
		return Math.floor(time / Date.DAY);
	};

	/** Returns the number of the week in year, as defined in ISO 8601. */
	Date.prototype.getWeekNumber = function() {
		var d = new Date(this.getFullYear(), this.getMonth(), this.getDate(), 0, 0, 0);
		var DoW = d.getDay();
		d.setDate(d.getDate() - (DoW + 6) % 7 + 3); // Nearest Thu
		var ms = d.valueOf(); // GMT
		d.setMonth(0);
		d.setDate(4); // Thu in Week 1
		return Math.round((ms - d.valueOf()) / (7 * 864e5)) + 1;
	};

	/** Checks date and time equality */
	Date.prototype.equalsTo = function(date) {
		return ((this.getFullYear() == date.getFullYear()) &&
			(this.getMonth() == date.getMonth()) &&
			(this.getDate() == date.getDate()) &&
			(this.getHours() == date.getHours()) &&
			(this.getMinutes() == date.getMinutes()));
	};

	/** Set only the year, month, date parts (keep existing time) */
	Date.prototype.setDateOnly = function(date) {
		var tmp = new Date(date);
		this.setDate(1);
		this.setFullYear(tmp.getFullYear());
		this.setMonth(tmp.getMonth());
		this.setDate(tmp.getDate());
	};

	/** Prints the date in a string according to the given format. */
	Date.prototype.print = function (str) {
		var m = this.getMonth();
		var d = this.getDate();
		var y = this.getFullYear();
		var wn = this.getWeekNumber();
		var w = this.getDay();
		var s = {};
		var hr = this.getHours();
		var pm = (hr >= 12);
		var ir = (pm) ? (hr - 12) : hr;
		var dy = this.getDayOfYear();
		if (ir == 0)
			ir = 12;
		var min = this.getMinutes();
		var sec = this.getSeconds();
		s["%a"] = Calendar.SHORT_DAY_NAMES[w]; // abbreviated weekday name [FIXME: I18N]
		s["%A"] = Calendar.DAY_NAMES[w]; // full weekday name
		s["%b"] = Calendar.SHORT_MONTH_NAMES[m]; // abbreviated month name [FIXME: I18N]
		s["%B"] = Calendar.MONTH_NAMES[m]; // full month name
		// FIXME: %c : preferred date and time representation for the current locale
		s["%C"] = 1 + Math.floor(y / 100); // the century number
		s["%d"] = (d < 10) ? ("0" + d) : d; // the day of the month (range 01 to 31)
		s["%e"] = d; // the day of the month (range 1 to 31)
		// FIXME: %D : american date style: %m/%d/%y
		// FIXME: %E, %F, %G, %g, %h (man strftime)
		s["%H"] = (hr < 10) ? ("0" + hr) : hr; // hour, range 00 to 23 (24h format)
		s["%I"] = (ir < 10) ? ("0" + ir) : ir; // hour, range 01 to 12 (12h format)
		s["%j"] = (dy < 100) ? ((dy < 10) ? ("00" + dy) : ("0" + dy)) : dy; // day of the year (range 001 to 366)
		s["%k"] = hr;   // hour, range 0 to 23 (24h format)
		s["%l"] = ir;   // hour, range 1 to 12 (12h format)
		s["%m"] = (m < 9) ? ("0" + (1+m)) : (1+m); // month, range 01 to 12
		s["%M"] = (min < 10) ? ("0" + min) : min; // minute, range 00 to 59
		s["%n"] = "\n";   // a newline character
		s["%p"] = pm ? "PM" : "AM";
		s["%P"] = pm ? "pm" : "am";
		// FIXME: %r : the time in am/pm notation %I:%M:%S %p
		// FIXME: %R : the time in 24-hour notation %H:%M
		s["%s"] = Math.floor(this.getTime() / 1000);
		s["%S"] = (sec < 10) ? ("0" + sec) : sec; // seconds, range 00 to 59
		s["%t"] = "\t";   // a tab character
		// FIXME: %T : the time in 24-hour notation (%H:%M:%S)
		s["%U"] = s["%W"] = s["%V"] = (wn < 10) ? ("0" + wn) : wn;
		s["%u"] = w + 1;  // the day of the week (range 1 to 7, 1 = MON)
		s["%w"] = w;    // the day of the week (range 0 to 6, 0 = SUN)
		// FIXME: %x : preferred date representation for the current locale without the time
		// FIXME: %X : preferred time representation for the current locale without the date
		s["%y"] = ('' + y).substr(2, 2); // year without the century (range 00 to 99)
		s["%Y"] = y;    // year with the century
		s["%%"] = "%";    // a literal '%' character

		var re = /%./g;
		var a = str.match(re);
		for (var i = 0; i < a.length; i++) {
			var tmp = s[a[i]];
			if (tmp) {
				re = new RegExp(a[i], 'g');
				str = str.replace(re, tmp);
			}
		}

		return str;
	};

	Date.prototype.__msh_oldSetFullYear = Date.prototype.setFullYear;
	Date.prototype.setFullYear = function(y) {
		var d = new Date(this);
		d.__msh_oldSetFullYear(y);
		if (d.getMonth() != this.getMonth())
			this.setDate(28);
		this.__msh_oldSetFullYear(y);
	}

	//------------------------------------------------------------------------------
	// The jQuery plugin function
	//------------------------------------------------------------------------------
	$.fn.calendar = function(options) {
		var defaults = {
			triggerElement: null, // Popup calendar
			parentElement: null, // Inline calendar
			minYear: 1900,
			maxYear: 2100,
			firstDayOfWeek: 1, // Monday
			weekend: "0,6", // Sunday and Saturday
			dateFormat: '%Y-%m-%d',
			dateField: null,
			selectHandler: null,
			closeHandler: null
		};
		var settings = $.extend({}, defaults, options);

		this.each(function() {
			var self = $(this);
			var calendar = new Calendar();

			calendar.minYear = settings.minYear;
			calendar.maxYear = settings.maxYear;

			calendar.firstDayOfWeek = settings.firstDayOfWeek;
			calendar.weekend = settings.weekend;
			calendar.dateFormat = settings.dateFormat;
			calendar.dateField = (settings.dateField || self);

			calendar.selectHandler = (settings.selectHandler || Calendar.defaultSelectHandler);

			// Inline Calendar
			var selfDate = self.html() || self.val();
			if (settings.parentElement) {
				calendar.create($(settings.parentElement));
				if (selfDate) calendar.parseDate(selfDate);
				calendar.show();
			} else {
				// Popup Calendar
				calendar.create();
				if (selfDate) calendar.parseDate(selfDate);
				var triggerElement = $(settings.triggerElement || self);
				triggerElement.click(function() {
					calendar.closeHandler = (settings.closeHandler || Calendar.defaultCloseHandler);
					calendar.showAtElement(triggerElement);
				});
			}
		});

		return this;
	}

})(jQuery);
