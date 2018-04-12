/* ===========================================================
 * bootstrap-customcustompopover.js v2.0.3
 * http://twitter.github.com/bootstrap/javascript.html#custompopovers
 * ===========================================================
 * Copyright 2012 Twitter, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * =========================================================== */


!function ($) {

  "use strict"; // jshint ;_;


 /* custompopover PUBLIC CLASS DEFINITION
  * =============================== */

  var custompopover = function ( element, options ) {
    this.init('custompopover', element, options)
  }


  /* NOTE: custompopover EXTENDS BOOTSTRAP-TOOLTIP.js
     ========================================== */

  custompopover.prototype = $.extend({}, $.fn.tooltip.Constructor.prototype, {

    constructor: custompopover

  , setContent: function () {
      var $tip = this.tip()
        , title = this.getTitle()
        , content = this.getContent()

      $tip.find('.custompopover-title')[this.isHTML(title) ? 'html' : 'text'](title)
      $tip.find('.custompopover-content > *')[this.isHTML(content) ? 'html' : 'text'](content)

      $tip.removeClass('fade top bottom left right in')
    }

  , hasContent: function () {
      return this.getTitle() || this.getContent()
    }

  , getContent: function () {
      var content
        , $e = this.$element
        , o = this.options

      content = $e.attr('data-content')
        || (typeof o.content == 'function' ? o.content.call($e[0]) :  o.content)

      return content
    }

  , tip: function () {
      if (!this.$tip) {
        this.$tip = $(this.options.template)
      }
      return this.$tip
    }

  })


 /* custompopover PLUGIN DEFINITION
  * ======================= */

  $.fn.custompopover = function (option) {
    return this.each(function () {
      var $this = $(this)
        , data = $this.data('custompopover')
        , options = typeof option == 'object' && option
      if (!data) $this.data('custompopover', (data = new custompopover(this, options)))
      if (typeof option == 'string') data[option]()
    })
  }

  $.fn.custompopover.Constructor = custompopover

  $.fn.custompopover.defaults = $.extend({} , $.fn.tooltip.defaults, {
    placement: 'right'
  , content: ''
  , template: '<div class="custompopover"><div class="arrow"></div><div class="custompopover-inner"><h3 class="custompopover-title"></h3><div class="custompopover-content"><p></p></div></div></div>'
  })

}(window.jQuery);