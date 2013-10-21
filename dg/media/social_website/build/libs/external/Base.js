/**
*   Base.js, version 1.1a
*   Copyright 2006-2010, Dean Edwards
*   License: http://www.opensource.org/licenses/mit-license.php
*
*   Modified for improved performance and various bugfixes.
*   
*   Changelog
*   --------------------------------------------------
*   12/12/12    AMD support added
*/

(function(){var e=function(){};typeof define!="undefined"?define([],function(){return e}):typeof window!="undefined"?window.Base=e:module.exports=e,e.extend=function(t,n){var r=e.prototype.extend;e._prototyping=!0;var i=new this;r.call(i,t),i.base=function(){},delete e._prototyping;var s=i.constructor,o=i.constructor=function(){if(!e._prototyping)if(this._constructing||this.constructor==o)this._constructing=!0,s.apply(this,arguments),delete this._constructing;else if(arguments[0]!=null)return(arguments[0].extend||r).call(arguments[0],i)};return o.ancestor=this,o.extend=this.extend,o.forEach=this.forEach,o.implement=this.implement,o.prototype=i,o.toString=this.toString,o.valueOf=function(e){return e=="object"?o:s.valueOf()},r.call(n||{},this),r.call(o,n),typeof o.init=="function"&&o.init(),o},e.prototype={extend:function(t,n){if(arguments.length>1){var r=this[t];if(r&&typeof n=="function"&&(!r.valueOf||r.valueOf()!=n.valueOf())&&/\bbase\b/.test(n)){var i=n.valueOf();n=function(){var t,n=this.base||e.prototype.base;return this.base=r,arguments.length===0?t=i.call(this):t=i.apply(this,arguments),this.base=n,t},n.valueOf=function(e){return e=="object"?n:i},n.toString=e.toString}this[t]=n}else if(t){var s=e.prototype.extend;!e._prototyping&&typeof this!="function"&&(s=this.extend||s);var o={toSource:null},u=["constructor","toString","valueOf"],a=e._prototyping?0:1;while(f=u[a++])t[f]!=o[f]&&s.call(this,f,t[f]);for(var f in t)o[f]||s.call(this,f,t[f])}return this}},e=e.extend({constructor:function(){this.extend(arguments[0])}},{ancestor:Object,version:"1.1",forEach:function(e,t,n){for(var r in e)this.prototype[r]===undefined&&t.call(n,e[r],r,e)},implement:function(){for(var e=0;e<arguments.length;e++)typeof arguments[e]=="function"?arguments[e](this.prototype):this.prototype.extend(arguments[e]);return this},toString:function(){return String(this.valueOf())}})})();