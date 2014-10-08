/*
 * jQuery UI Monthpicker
 *
 * @licensed MIT <see below>
 * @licensed GPL <see below>
 *
 * @author Luciano Costa
 * http://lucianocosta.info/jquery.mtz.monthpicker/
 *
 * Depends:
 *  jquery.ui.core.js
 */

/**
 * MIT License
 * Copyright (c) 2011, Luciano Costa
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy 
 * of this software and associated documentation files (the "Software"), to deal 
 * in the Software without restriction, including without limitation the rights 
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
 * copies of the Software, and to permit persons to whom the Software is 
 * furnished to do so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

/**
 * GPL LIcense
 * Copyright (c) 2011, Luciano Costa
 * 
 * This program is free software: you can redistribute it and/or modify it 
 * under the terms of the GNU General Public License as published by the 
 * Free Software Foundation, either version 3 of the License, or 
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful, but 
 * WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY 
 * or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License 
 * for more details.
 * 
 * You should have received a copy of the GNU General Public License along 
 * with this program. If not, see <http://www.gnu.org/licenses/>.
 */

(function(e){var t={init:function(t){return this.each(function(){var n=e(this),r=n.data("monthpicker"),i=t&&t.year?t.year:(new Date).getFullYear(),s=e.extend({pattern:"mm/yyyy",selectedMonth:null,selectedMonthName:"",selectedYear:i,startYear:i-10,finalYear:i+10,monthNames:["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],id:"monthpicker_"+(Math.random()*Math.random()).toString().replace(".",""),openOnFocus:!0,disabledMonths:[]},t);s.dateSeparator=s.pattern.replace(/(mmm|mm|m|yyyy|yy|y)/ig,""),r||(e(this).data("monthpicker",{target:n,settings:s}),s.openOnFocus===!0&&n.on("focus",function(){n.monthpicker("show")}),n.monthpicker("parseInputValue",s),n.monthpicker("mountWidget",s),n.on("monthpicker-click-month",function(e,t,r){n.monthpicker("setValue",s),n.monthpicker("hide")}),n.addClass("mtz-monthpicker-widgetcontainer"),e(document).unbind("mousedown.mtzmonthpicker").on("mousedown.mtzmonthpicker",function(t){(!t.target.className||t.target.className.toString().indexOf("mtz-monthpicker")<0)&&e(this).monthpicker("hideAll")}))})},show:function(){e(this).monthpicker("hideAll");var t=e("#"+this.data("monthpicker").settings.id);t.css("top",this.offset().top+this.outerHeight()),e(window).width()>t.width()+this.offset().left?t.css("left",this.offset().left):t.css("left",this.offset().left-t.width()),t.show(),t.find("select").focus(),this.trigger("monthpicker-show")},hide:function(){var t=e("#"+this.data("monthpicker").settings.id);t.is(":visible")&&(t.hide(),this.trigger("monthpicker-hide"))},hideAll:function(){e(".mtz-monthpicker-widgetcontainer").each(function(){typeof e(this).data("monthpicker")!="undefined"&&e(this).monthpicker("hide")})},setValue:function(e){var t=e.selectedMonth,n=e.selectedYear;e.pattern.indexOf("mmm")>=0?t=e.selectedMonthName:e.pattern.indexOf("mm")>=0&&e.selectedMonth<10&&(t="0"+e.selectedMonth),e.pattern.indexOf("yyyy")<0&&(n=n.toString().substr(2,2)),e.pattern.indexOf("y")>e.pattern.indexOf(e.dateSeparator)?this.val(t+e.dateSeparator+n):this.val(n+e.dateSeparator+t),this.change()},disableMonths:function(t){var n=this.data("monthpicker").settings,r=e("#"+n.id);n.disabledMonths=t,r.find(".mtz-monthpicker-month").each(function(){var n=parseInt(e(this).data("month"));e.inArray(n,t)>=0?e(this).addClass("ui-state-disabled"):e(this).removeClass("ui-state-disabled")})},mountWidget:function(t){var n=this,r=e('<div id="'+t.id+'" class="ui-datepicker ui-widget ui-widget-content ui-helper-clearfix ui-corner-all" />'),i=e('<div class="ui-datepicker-header ui-widget-header ui-helper-clearfix ui-corner-all mtz-monthpicker" />'),s=e('<select class="mtz-monthpicker mtz-monthpicker-year" />'),o=e('<table class="mtz-monthpicker" />'),u=e('<tbody class="mtz-monthpicker" />'),a=e('<tr class="mtz-monthpicker" />'),f="",l=t.selectedYear,c=null,h=e(this).data("selected-year"),p=e(this).data("start-year"),d=e(this).data("final-year");h&&(t.selectedYear=h),p&&(t.startYear=p),d&&(t.finalYear=d),r.css({position:"absolute",zIndex:999999,whiteSpace:"nowrap",width:"250px",overflow:"hidden",textAlign:"center",display:"none",top:n.offset().top+n.outerHeight(),left:n.offset().left}),s.on("change",function(){var r=e(this).parent().parent().find("td[data-month]");r.removeClass("ui-state-active"),e(this).val()==t.selectedYear&&r.filter("td[data-month="+t.selectedMonth+"]").addClass("ui-state-active"),n.trigger("monthpicker-change-year",e(this).val())});for(var v=t.startYear;v<=t.finalYear;v++){var c=e('<option class="mtz-monthpicker" />').attr("value",v).append(v);t.selectedYear==v&&c.attr("selected","selected"),s.append(c)}i.append(s).appendTo(r);for(var v=1;v<=12;v++)f=e('<td class="ui-state-default mtz-monthpicker mtz-monthpicker-month" style="padding:5px;cursor:default;" />').attr("data-month",v),t.selectedMonth==v&&f.addClass("ui-state-active"),f.append(t.monthNames[v-1]),a.append(f).appendTo(u),v%3===0&&(a=e('<tr class="mtz-monthpicker" />'));u.find(".mtz-monthpicker-month").on("click",function(){var r=parseInt(e(this).data("month"));e.inArray(r,t.disabledMonths)<0&&(t.selectedYear=e(this).closest(".ui-datepicker").find(".mtz-monthpicker-year").first().val(),t.selectedMonth=e(this).data("month"),t.selectedMonthName=e(this).text(),n.trigger("monthpicker-click-month",e(this).data("month")),e(this).closest("table").find(".ui-state-active").removeClass("ui-state-active"),e(this).addClass("ui-state-active"))}),o.append(u).appendTo(r),r.appendTo("body")},destroy:function(){return this.each(function(){e(this).removeClass("mtz-monthpicker-widgetcontainer").unbind("focus").removeData("monthpicker")})},getDate:function(){var e=this.data("monthpicker").settings;return e.selectedMonth&&e.selectedYear?new Date(e.selectedYear,e.selectedMonth-1):null},parseInputValue:function(e){if(this.val()&&e.dateSeparator){var t=this.val().toString().split(e.dateSeparator);e.pattern.indexOf("m")===0?(e.selectedMonth=t[0],e.selectedYear=t[1]):(e.selectedMonth=t[1],e.selectedYear=t[0])}}};e.fn.monthpicker=function(n){if(t[n])return t[n].apply(this,Array.prototype.slice.call(arguments,1));if(typeof n=="object"||!n)return t.init.apply(this,arguments);e.error("Method "+n+" does not exist on jQuery.mtz.monthpicker")}})(jQuery);