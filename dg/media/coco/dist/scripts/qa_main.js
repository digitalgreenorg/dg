/*! jQuery v2.1.1 | (c) 2005, 2014 jQuery Foundation, Inc. | jquery.org/license */
!function(a,b){"object"==typeof module&&"object"==typeof module.exports?module.exports=a.document?b(a,!0):function(a){if(!a.document)throw new Error("jQuery requires a window with a document");return b(a)}:b(a)}("undefined"!=typeof window?window:this,function(a,b){var c=[],d=c.slice,e=c.concat,f=c.push,g=c.indexOf,h={},i=h.toString,j=h.hasOwnProperty,k={},l=a.document,m="2.1.1",n=function(a,b){return new n.fn.init(a,b)},o=/^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g,p=/^-ms-/,q=/-([\da-z])/gi,r=function(a,b){return b.toUpperCase()};n.fn=n.prototype={jquery:m,constructor:n,selector:"",length:0,toArray:function(){return d.call(this)},get:function(a){return null!=a?0>a?this[a+this.length]:this[a]:d.call(this)},pushStack:function(a){var b=n.merge(this.constructor(),a);return b.prevObject=this,b.context=this.context,b},each:function(a,b){return n.each(this,a,b)},map:function(a){return this.pushStack(n.map(this,function(b,c){return a.call(b,c,b)}))},slice:function(){return this.pushStack(d.apply(this,arguments))},first:function(){return this.eq(0)},last:function(){return this.eq(-1)},eq:function(a){var b=this.length,c=+a+(0>a?b:0);return this.pushStack(c>=0&&b>c?[this[c]]:[])},end:function(){return this.prevObject||this.constructor(null)},push:f,sort:c.sort,splice:c.splice},n.extend=n.fn.extend=function(){var a,b,c,d,e,f,g=arguments[0]||{},h=1,i=arguments.length,j=!1;for("boolean"==typeof g&&(j=g,g=arguments[h]||{},h++),"object"==typeof g||n.isFunction(g)||(g={}),h===i&&(g=this,h--);i>h;h++)if(null!=(a=arguments[h]))for(b in a)c=g[b],d=a[b],g!==d&&(j&&d&&(n.isPlainObject(d)||(e=n.isArray(d)))?(e?(e=!1,f=c&&n.isArray(c)?c:[]):f=c&&n.isPlainObject(c)?c:{},g[b]=n.extend(j,f,d)):void 0!==d&&(g[b]=d));return g},n.extend({expando:"jQuery"+(m+Math.random()).replace(/\D/g,""),isReady:!0,error:function(a){throw new Error(a)},noop:function(){},isFunction:function(a){return"function"===n.type(a)},isArray:Array.isArray,isWindow:function(a){return null!=a&&a===a.window},isNumeric:function(a){return!n.isArray(a)&&a-parseFloat(a)>=0},isPlainObject:function(a){return"object"!==n.type(a)||a.nodeType||n.isWindow(a)?!1:a.constructor&&!j.call(a.constructor.prototype,"isPrototypeOf")?!1:!0},isEmptyObject:function(a){var b;for(b in a)return!1;return!0},type:function(a){return null==a?a+"":"object"==typeof a||"function"==typeof a?h[i.call(a)]||"object":typeof a},globalEval:function(a){var b,c=eval;a=n.trim(a),a&&(1===a.indexOf("use strict")?(b=l.createElement("script"),b.text=a,l.head.appendChild(b).parentNode.removeChild(b)):c(a))},camelCase:function(a){return a.replace(p,"ms-").replace(q,r)},nodeName:function(a,b){return a.nodeName&&a.nodeName.toLowerCase()===b.toLowerCase()},each:function(a,b,c){var d,e=0,f=a.length,g=s(a);if(c){if(g){for(;f>e;e++)if(d=b.apply(a[e],c),d===!1)break}else for(e in a)if(d=b.apply(a[e],c),d===!1)break}else if(g){for(;f>e;e++)if(d=b.call(a[e],e,a[e]),d===!1)break}else for(e in a)if(d=b.call(a[e],e,a[e]),d===!1)break;return a},trim:function(a){return null==a?"":(a+"").replace(o,"")},makeArray:function(a,b){var c=b||[];return null!=a&&(s(Object(a))?n.merge(c,"string"==typeof a?[a]:a):f.call(c,a)),c},inArray:function(a,b,c){return null==b?-1:g.call(b,a,c)},merge:function(a,b){for(var c=+b.length,d=0,e=a.length;c>d;d++)a[e++]=b[d];return a.length=e,a},grep:function(a,b,c){for(var d,e=[],f=0,g=a.length,h=!c;g>f;f++)d=!b(a[f],f),d!==h&&e.push(a[f]);return e},map:function(a,b,c){var d,f=0,g=a.length,h=s(a),i=[];if(h)for(;g>f;f++)d=b(a[f],f,c),null!=d&&i.push(d);else for(f in a)d=b(a[f],f,c),null!=d&&i.push(d);return e.apply([],i)},guid:1,proxy:function(a,b){var c,e,f;return"string"==typeof b&&(c=a[b],b=a,a=c),n.isFunction(a)?(e=d.call(arguments,2),f=function(){return a.apply(b||this,e.concat(d.call(arguments)))},f.guid=a.guid=a.guid||n.guid++,f):void 0},now:Date.now,support:k}),n.each("Boolean Number String Function Array Date RegExp Object Error".split(" "),function(a,b){h["[object "+b+"]"]=b.toLowerCase()});function s(a){var b=a.length,c=n.type(a);return"function"===c||n.isWindow(a)?!1:1===a.nodeType&&b?!0:"array"===c||0===b||"number"==typeof b&&b>0&&b-1 in a}var t=function(a){var b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u="sizzle"+-new Date,v=a.document,w=0,x=0,y=gb(),z=gb(),A=gb(),B=function(a,b){return a===b&&(l=!0),0},C="undefined",D=1<<31,E={}.hasOwnProperty,F=[],G=F.pop,H=F.push,I=F.push,J=F.slice,K=F.indexOf||function(a){for(var b=0,c=this.length;c>b;b++)if(this[b]===a)return b;return-1},L="checked|selected|async|autofocus|autoplay|controls|defer|disabled|hidden|ismap|loop|multiple|open|readonly|required|scoped",M="[\\x20\\t\\r\\n\\f]",N="(?:\\\\.|[\\w-]|[^\\x00-\\xa0])+",O=N.replace("w","w#"),P="\\["+M+"*("+N+")(?:"+M+"*([*^$|!~]?=)"+M+"*(?:'((?:\\\\.|[^\\\\'])*)'|\"((?:\\\\.|[^\\\\\"])*)\"|("+O+"))|)"+M+"*\\]",Q=":("+N+")(?:\\((('((?:\\\\.|[^\\\\'])*)'|\"((?:\\\\.|[^\\\\\"])*)\")|((?:\\\\.|[^\\\\()[\\]]|"+P+")*)|.*)\\)|)",R=new RegExp("^"+M+"+|((?:^|[^\\\\])(?:\\\\.)*)"+M+"+$","g"),S=new RegExp("^"+M+"*,"+M+"*"),T=new RegExp("^"+M+"*([>+~]|"+M+")"+M+"*"),U=new RegExp("="+M+"*([^\\]'\"]*?)"+M+"*\\]","g"),V=new RegExp(Q),W=new RegExp("^"+O+"$"),X={ID:new RegExp("^#("+N+")"),CLASS:new RegExp("^\\.("+N+")"),TAG:new RegExp("^("+N.replace("w","w*")+")"),ATTR:new RegExp("^"+P),PSEUDO:new RegExp("^"+Q),CHILD:new RegExp("^:(only|first|last|nth|nth-last)-(child|of-type)(?:\\("+M+"*(even|odd|(([+-]|)(\\d*)n|)"+M+"*(?:([+-]|)"+M+"*(\\d+)|))"+M+"*\\)|)","i"),bool:new RegExp("^(?:"+L+")$","i"),needsContext:new RegExp("^"+M+"*[>+~]|:(even|odd|eq|gt|lt|nth|first|last)(?:\\("+M+"*((?:-\\d)?\\d*)"+M+"*\\)|)(?=[^-]|$)","i")},Y=/^(?:input|select|textarea|button)$/i,Z=/^h\d$/i,$=/^[^{]+\{\s*\[native \w/,_=/^(?:#([\w-]+)|(\w+)|\.([\w-]+))$/,ab=/[+~]/,bb=/'|\\/g,cb=new RegExp("\\\\([\\da-f]{1,6}"+M+"?|("+M+")|.)","ig"),db=function(a,b,c){var d="0x"+b-65536;return d!==d||c?b:0>d?String.fromCharCode(d+65536):String.fromCharCode(d>>10|55296,1023&d|56320)};try{I.apply(F=J.call(v.childNodes),v.childNodes),F[v.childNodes.length].nodeType}catch(eb){I={apply:F.length?function(a,b){H.apply(a,J.call(b))}:function(a,b){var c=a.length,d=0;while(a[c++]=b[d++]);a.length=c-1}}}function fb(a,b,d,e){var f,h,j,k,l,o,r,s,w,x;if((b?b.ownerDocument||b:v)!==n&&m(b),b=b||n,d=d||[],!a||"string"!=typeof a)return d;if(1!==(k=b.nodeType)&&9!==k)return[];if(p&&!e){if(f=_.exec(a))if(j=f[1]){if(9===k){if(h=b.getElementById(j),!h||!h.parentNode)return d;if(h.id===j)return d.push(h),d}else if(b.ownerDocument&&(h=b.ownerDocument.getElementById(j))&&t(b,h)&&h.id===j)return d.push(h),d}else{if(f[2])return I.apply(d,b.getElementsByTagName(a)),d;if((j=f[3])&&c.getElementsByClassName&&b.getElementsByClassName)return I.apply(d,b.getElementsByClassName(j)),d}if(c.qsa&&(!q||!q.test(a))){if(s=r=u,w=b,x=9===k&&a,1===k&&"object"!==b.nodeName.toLowerCase()){o=g(a),(r=b.getAttribute("id"))?s=r.replace(bb,"\\$&"):b.setAttribute("id",s),s="[id='"+s+"'] ",l=o.length;while(l--)o[l]=s+qb(o[l]);w=ab.test(a)&&ob(b.parentNode)||b,x=o.join(",")}if(x)try{return I.apply(d,w.querySelectorAll(x)),d}catch(y){}finally{r||b.removeAttribute("id")}}}return i(a.replace(R,"$1"),b,d,e)}function gb(){var a=[];function b(c,e){return a.push(c+" ")>d.cacheLength&&delete b[a.shift()],b[c+" "]=e}return b}function hb(a){return a[u]=!0,a}function ib(a){var b=n.createElement("div");try{return!!a(b)}catch(c){return!1}finally{b.parentNode&&b.parentNode.removeChild(b),b=null}}function jb(a,b){var c=a.split("|"),e=a.length;while(e--)d.attrHandle[c[e]]=b}function kb(a,b){var c=b&&a,d=c&&1===a.nodeType&&1===b.nodeType&&(~b.sourceIndex||D)-(~a.sourceIndex||D);if(d)return d;if(c)while(c=c.nextSibling)if(c===b)return-1;return a?1:-1}function lb(a){return function(b){var c=b.nodeName.toLowerCase();return"input"===c&&b.type===a}}function mb(a){return function(b){var c=b.nodeName.toLowerCase();return("input"===c||"button"===c)&&b.type===a}}function nb(a){return hb(function(b){return b=+b,hb(function(c,d){var e,f=a([],c.length,b),g=f.length;while(g--)c[e=f[g]]&&(c[e]=!(d[e]=c[e]))})})}function ob(a){return a&&typeof a.getElementsByTagName!==C&&a}c=fb.support={},f=fb.isXML=function(a){var b=a&&(a.ownerDocument||a).documentElement;return b?"HTML"!==b.nodeName:!1},m=fb.setDocument=function(a){var b,e=a?a.ownerDocument||a:v,g=e.defaultView;return e!==n&&9===e.nodeType&&e.documentElement?(n=e,o=e.documentElement,p=!f(e),g&&g!==g.top&&(g.addEventListener?g.addEventListener("unload",function(){m()},!1):g.attachEvent&&g.attachEvent("onunload",function(){m()})),c.attributes=ib(function(a){return a.className="i",!a.getAttribute("className")}),c.getElementsByTagName=ib(function(a){return a.appendChild(e.createComment("")),!a.getElementsByTagName("*").length}),c.getElementsByClassName=$.test(e.getElementsByClassName)&&ib(function(a){return a.innerHTML="<div class='a'></div><div class='a i'></div>",a.firstChild.className="i",2===a.getElementsByClassName("i").length}),c.getById=ib(function(a){return o.appendChild(a).id=u,!e.getElementsByName||!e.getElementsByName(u).length}),c.getById?(d.find.ID=function(a,b){if(typeof b.getElementById!==C&&p){var c=b.getElementById(a);return c&&c.parentNode?[c]:[]}},d.filter.ID=function(a){var b=a.replace(cb,db);return function(a){return a.getAttribute("id")===b}}):(delete d.find.ID,d.filter.ID=function(a){var b=a.replace(cb,db);return function(a){var c=typeof a.getAttributeNode!==C&&a.getAttributeNode("id");return c&&c.value===b}}),d.find.TAG=c.getElementsByTagName?function(a,b){return typeof b.getElementsByTagName!==C?b.getElementsByTagName(a):void 0}:function(a,b){var c,d=[],e=0,f=b.getElementsByTagName(a);if("*"===a){while(c=f[e++])1===c.nodeType&&d.push(c);return d}return f},d.find.CLASS=c.getElementsByClassName&&function(a,b){return typeof b.getElementsByClassName!==C&&p?b.getElementsByClassName(a):void 0},r=[],q=[],(c.qsa=$.test(e.querySelectorAll))&&(ib(function(a){a.innerHTML="<select msallowclip=''><option selected=''></option></select>",a.querySelectorAll("[msallowclip^='']").length&&q.push("[*^$]="+M+"*(?:''|\"\")"),a.querySelectorAll("[selected]").length||q.push("\\["+M+"*(?:value|"+L+")"),a.querySelectorAll(":checked").length||q.push(":checked")}),ib(function(a){var b=e.createElement("input");b.setAttribute("type","hidden"),a.appendChild(b).setAttribute("name","D"),a.querySelectorAll("[name=d]").length&&q.push("name"+M+"*[*^$|!~]?="),a.querySelectorAll(":enabled").length||q.push(":enabled",":disabled"),a.querySelectorAll("*,:x"),q.push(",.*:")})),(c.matchesSelector=$.test(s=o.matches||o.webkitMatchesSelector||o.mozMatchesSelector||o.oMatchesSelector||o.msMatchesSelector))&&ib(function(a){c.disconnectedMatch=s.call(a,"div"),s.call(a,"[s!='']:x"),r.push("!=",Q)}),q=q.length&&new RegExp(q.join("|")),r=r.length&&new RegExp(r.join("|")),b=$.test(o.compareDocumentPosition),t=b||$.test(o.contains)?function(a,b){var c=9===a.nodeType?a.documentElement:a,d=b&&b.parentNode;return a===d||!(!d||1!==d.nodeType||!(c.contains?c.contains(d):a.compareDocumentPosition&&16&a.compareDocumentPosition(d)))}:function(a,b){if(b)while(b=b.parentNode)if(b===a)return!0;return!1},B=b?function(a,b){if(a===b)return l=!0,0;var d=!a.compareDocumentPosition-!b.compareDocumentPosition;return d?d:(d=(a.ownerDocument||a)===(b.ownerDocument||b)?a.compareDocumentPosition(b):1,1&d||!c.sortDetached&&b.compareDocumentPosition(a)===d?a===e||a.ownerDocument===v&&t(v,a)?-1:b===e||b.ownerDocument===v&&t(v,b)?1:k?K.call(k,a)-K.call(k,b):0:4&d?-1:1)}:function(a,b){if(a===b)return l=!0,0;var c,d=0,f=a.parentNode,g=b.parentNode,h=[a],i=[b];if(!f||!g)return a===e?-1:b===e?1:f?-1:g?1:k?K.call(k,a)-K.call(k,b):0;if(f===g)return kb(a,b);c=a;while(c=c.parentNode)h.unshift(c);c=b;while(c=c.parentNode)i.unshift(c);while(h[d]===i[d])d++;return d?kb(h[d],i[d]):h[d]===v?-1:i[d]===v?1:0},e):n},fb.matches=function(a,b){return fb(a,null,null,b)},fb.matchesSelector=function(a,b){if((a.ownerDocument||a)!==n&&m(a),b=b.replace(U,"='$1']"),!(!c.matchesSelector||!p||r&&r.test(b)||q&&q.test(b)))try{var d=s.call(a,b);if(d||c.disconnectedMatch||a.document&&11!==a.document.nodeType)return d}catch(e){}return fb(b,n,null,[a]).length>0},fb.contains=function(a,b){return(a.ownerDocument||a)!==n&&m(a),t(a,b)},fb.attr=function(a,b){(a.ownerDocument||a)!==n&&m(a);var e=d.attrHandle[b.toLowerCase()],f=e&&E.call(d.attrHandle,b.toLowerCase())?e(a,b,!p):void 0;return void 0!==f?f:c.attributes||!p?a.getAttribute(b):(f=a.getAttributeNode(b))&&f.specified?f.value:null},fb.error=function(a){throw new Error("Syntax error, unrecognized expression: "+a)},fb.uniqueSort=function(a){var b,d=[],e=0,f=0;if(l=!c.detectDuplicates,k=!c.sortStable&&a.slice(0),a.sort(B),l){while(b=a[f++])b===a[f]&&(e=d.push(f));while(e--)a.splice(d[e],1)}return k=null,a},e=fb.getText=function(a){var b,c="",d=0,f=a.nodeType;if(f){if(1===f||9===f||11===f){if("string"==typeof a.textContent)return a.textContent;for(a=a.firstChild;a;a=a.nextSibling)c+=e(a)}else if(3===f||4===f)return a.nodeValue}else while(b=a[d++])c+=e(b);return c},d=fb.selectors={cacheLength:50,createPseudo:hb,match:X,attrHandle:{},find:{},relative:{">":{dir:"parentNode",first:!0}," ":{dir:"parentNode"},"+":{dir:"previousSibling",first:!0},"~":{dir:"previousSibling"}},preFilter:{ATTR:function(a){return a[1]=a[1].replace(cb,db),a[3]=(a[3]||a[4]||a[5]||"").replace(cb,db),"~="===a[2]&&(a[3]=" "+a[3]+" "),a.slice(0,4)},CHILD:function(a){return a[1]=a[1].toLowerCase(),"nth"===a[1].slice(0,3)?(a[3]||fb.error(a[0]),a[4]=+(a[4]?a[5]+(a[6]||1):2*("even"===a[3]||"odd"===a[3])),a[5]=+(a[7]+a[8]||"odd"===a[3])):a[3]&&fb.error(a[0]),a},PSEUDO:function(a){var b,c=!a[6]&&a[2];return X.CHILD.test(a[0])?null:(a[3]?a[2]=a[4]||a[5]||"":c&&V.test(c)&&(b=g(c,!0))&&(b=c.indexOf(")",c.length-b)-c.length)&&(a[0]=a[0].slice(0,b),a[2]=c.slice(0,b)),a.slice(0,3))}},filter:{TAG:function(a){var b=a.replace(cb,db).toLowerCase();return"*"===a?function(){return!0}:function(a){return a.nodeName&&a.nodeName.toLowerCase()===b}},CLASS:function(a){var b=y[a+" "];return b||(b=new RegExp("(^|"+M+")"+a+"("+M+"|$)"))&&y(a,function(a){return b.test("string"==typeof a.className&&a.className||typeof a.getAttribute!==C&&a.getAttribute("class")||"")})},ATTR:function(a,b,c){return function(d){var e=fb.attr(d,a);return null==e?"!="===b:b?(e+="","="===b?e===c:"!="===b?e!==c:"^="===b?c&&0===e.indexOf(c):"*="===b?c&&e.indexOf(c)>-1:"$="===b?c&&e.slice(-c.length)===c:"~="===b?(" "+e+" ").indexOf(c)>-1:"|="===b?e===c||e.slice(0,c.length+1)===c+"-":!1):!0}},CHILD:function(a,b,c,d,e){var f="nth"!==a.slice(0,3),g="last"!==a.slice(-4),h="of-type"===b;return 1===d&&0===e?function(a){return!!a.parentNode}:function(b,c,i){var j,k,l,m,n,o,p=f!==g?"nextSibling":"previousSibling",q=b.parentNode,r=h&&b.nodeName.toLowerCase(),s=!i&&!h;if(q){if(f){while(p){l=b;while(l=l[p])if(h?l.nodeName.toLowerCase()===r:1===l.nodeType)return!1;o=p="only"===a&&!o&&"nextSibling"}return!0}if(o=[g?q.firstChild:q.lastChild],g&&s){k=q[u]||(q[u]={}),j=k[a]||[],n=j[0]===w&&j[1],m=j[0]===w&&j[2],l=n&&q.childNodes[n];while(l=++n&&l&&l[p]||(m=n=0)||o.pop())if(1===l.nodeType&&++m&&l===b){k[a]=[w,n,m];break}}else if(s&&(j=(b[u]||(b[u]={}))[a])&&j[0]===w)m=j[1];else while(l=++n&&l&&l[p]||(m=n=0)||o.pop())if((h?l.nodeName.toLowerCase()===r:1===l.nodeType)&&++m&&(s&&((l[u]||(l[u]={}))[a]=[w,m]),l===b))break;return m-=e,m===d||m%d===0&&m/d>=0}}},PSEUDO:function(a,b){var c,e=d.pseudos[a]||d.setFilters[a.toLowerCase()]||fb.error("unsupported pseudo: "+a);return e[u]?e(b):e.length>1?(c=[a,a,"",b],d.setFilters.hasOwnProperty(a.toLowerCase())?hb(function(a,c){var d,f=e(a,b),g=f.length;while(g--)d=K.call(a,f[g]),a[d]=!(c[d]=f[g])}):function(a){return e(a,0,c)}):e}},pseudos:{not:hb(function(a){var b=[],c=[],d=h(a.replace(R,"$1"));return d[u]?hb(function(a,b,c,e){var f,g=d(a,null,e,[]),h=a.length;while(h--)(f=g[h])&&(a[h]=!(b[h]=f))}):function(a,e,f){return b[0]=a,d(b,null,f,c),!c.pop()}}),has:hb(function(a){return function(b){return fb(a,b).length>0}}),contains:hb(function(a){return function(b){return(b.textContent||b.innerText||e(b)).indexOf(a)>-1}}),lang:hb(function(a){return W.test(a||"")||fb.error("unsupported lang: "+a),a=a.replace(cb,db).toLowerCase(),function(b){var c;do if(c=p?b.lang:b.getAttribute("xml:lang")||b.getAttribute("lang"))return c=c.toLowerCase(),c===a||0===c.indexOf(a+"-");while((b=b.parentNode)&&1===b.nodeType);return!1}}),target:function(b){var c=a.location&&a.location.hash;return c&&c.slice(1)===b.id},root:function(a){return a===o},focus:function(a){return a===n.activeElement&&(!n.hasFocus||n.hasFocus())&&!!(a.type||a.href||~a.tabIndex)},enabled:function(a){return a.disabled===!1},disabled:function(a){return a.disabled===!0},checked:function(a){var b=a.nodeName.toLowerCase();return"input"===b&&!!a.checked||"option"===b&&!!a.selected},selected:function(a){return a.parentNode&&a.parentNode.selectedIndex,a.selected===!0},empty:function(a){for(a=a.firstChild;a;a=a.nextSibling)if(a.nodeType<6)return!1;return!0},parent:function(a){return!d.pseudos.empty(a)},header:function(a){return Z.test(a.nodeName)},input:function(a){return Y.test(a.nodeName)},button:function(a){var b=a.nodeName.toLowerCase();return"input"===b&&"button"===a.type||"button"===b},text:function(a){var b;return"input"===a.nodeName.toLowerCase()&&"text"===a.type&&(null==(b=a.getAttribute("type"))||"text"===b.toLowerCase())},first:nb(function(){return[0]}),last:nb(function(a,b){return[b-1]}),eq:nb(function(a,b,c){return[0>c?c+b:c]}),even:nb(function(a,b){for(var c=0;b>c;c+=2)a.push(c);return a}),odd:nb(function(a,b){for(var c=1;b>c;c+=2)a.push(c);return a}),lt:nb(function(a,b,c){for(var d=0>c?c+b:c;--d>=0;)a.push(d);return a}),gt:nb(function(a,b,c){for(var d=0>c?c+b:c;++d<b;)a.push(d);return a})}},d.pseudos.nth=d.pseudos.eq;for(b in{radio:!0,checkbox:!0,file:!0,password:!0,image:!0})d.pseudos[b]=lb(b);for(b in{submit:!0,reset:!0})d.pseudos[b]=mb(b);function pb(){}pb.prototype=d.filters=d.pseudos,d.setFilters=new pb,g=fb.tokenize=function(a,b){var c,e,f,g,h,i,j,k=z[a+" "];if(k)return b?0:k.slice(0);h=a,i=[],j=d.preFilter;while(h){(!c||(e=S.exec(h)))&&(e&&(h=h.slice(e[0].length)||h),i.push(f=[])),c=!1,(e=T.exec(h))&&(c=e.shift(),f.push({value:c,type:e[0].replace(R," ")}),h=h.slice(c.length));for(g in d.filter)!(e=X[g].exec(h))||j[g]&&!(e=j[g](e))||(c=e.shift(),f.push({value:c,type:g,matches:e}),h=h.slice(c.length));if(!c)break}return b?h.length:h?fb.error(a):z(a,i).slice(0)};function qb(a){for(var b=0,c=a.length,d="";c>b;b++)d+=a[b].value;return d}function rb(a,b,c){var d=b.dir,e=c&&"parentNode"===d,f=x++;return b.first?function(b,c,f){while(b=b[d])if(1===b.nodeType||e)return a(b,c,f)}:function(b,c,g){var h,i,j=[w,f];if(g){while(b=b[d])if((1===b.nodeType||e)&&a(b,c,g))return!0}else while(b=b[d])if(1===b.nodeType||e){if(i=b[u]||(b[u]={}),(h=i[d])&&h[0]===w&&h[1]===f)return j[2]=h[2];if(i[d]=j,j[2]=a(b,c,g))return!0}}}function sb(a){return a.length>1?function(b,c,d){var e=a.length;while(e--)if(!a[e](b,c,d))return!1;return!0}:a[0]}function tb(a,b,c){for(var d=0,e=b.length;e>d;d++)fb(a,b[d],c);return c}function ub(a,b,c,d,e){for(var f,g=[],h=0,i=a.length,j=null!=b;i>h;h++)(f=a[h])&&(!c||c(f,d,e))&&(g.push(f),j&&b.push(h));return g}function vb(a,b,c,d,e,f){return d&&!d[u]&&(d=vb(d)),e&&!e[u]&&(e=vb(e,f)),hb(function(f,g,h,i){var j,k,l,m=[],n=[],o=g.length,p=f||tb(b||"*",h.nodeType?[h]:h,[]),q=!a||!f&&b?p:ub(p,m,a,h,i),r=c?e||(f?a:o||d)?[]:g:q;if(c&&c(q,r,h,i),d){j=ub(r,n),d(j,[],h,i),k=j.length;while(k--)(l=j[k])&&(r[n[k]]=!(q[n[k]]=l))}if(f){if(e||a){if(e){j=[],k=r.length;while(k--)(l=r[k])&&j.push(q[k]=l);e(null,r=[],j,i)}k=r.length;while(k--)(l=r[k])&&(j=e?K.call(f,l):m[k])>-1&&(f[j]=!(g[j]=l))}}else r=ub(r===g?r.splice(o,r.length):r),e?e(null,g,r,i):I.apply(g,r)})}function wb(a){for(var b,c,e,f=a.length,g=d.relative[a[0].type],h=g||d.relative[" "],i=g?1:0,k=rb(function(a){return a===b},h,!0),l=rb(function(a){return K.call(b,a)>-1},h,!0),m=[function(a,c,d){return!g&&(d||c!==j)||((b=c).nodeType?k(a,c,d):l(a,c,d))}];f>i;i++)if(c=d.relative[a[i].type])m=[rb(sb(m),c)];else{if(c=d.filter[a[i].type].apply(null,a[i].matches),c[u]){for(e=++i;f>e;e++)if(d.relative[a[e].type])break;return vb(i>1&&sb(m),i>1&&qb(a.slice(0,i-1).concat({value:" "===a[i-2].type?"*":""})).replace(R,"$1"),c,e>i&&wb(a.slice(i,e)),f>e&&wb(a=a.slice(e)),f>e&&qb(a))}m.push(c)}return sb(m)}function xb(a,b){var c=b.length>0,e=a.length>0,f=function(f,g,h,i,k){var l,m,o,p=0,q="0",r=f&&[],s=[],t=j,u=f||e&&d.find.TAG("*",k),v=w+=null==t?1:Math.random()||.1,x=u.length;for(k&&(j=g!==n&&g);q!==x&&null!=(l=u[q]);q++){if(e&&l){m=0;while(o=a[m++])if(o(l,g,h)){i.push(l);break}k&&(w=v)}c&&((l=!o&&l)&&p--,f&&r.push(l))}if(p+=q,c&&q!==p){m=0;while(o=b[m++])o(r,s,g,h);if(f){if(p>0)while(q--)r[q]||s[q]||(s[q]=G.call(i));s=ub(s)}I.apply(i,s),k&&!f&&s.length>0&&p+b.length>1&&fb.uniqueSort(i)}return k&&(w=v,j=t),r};return c?hb(f):f}return h=fb.compile=function(a,b){var c,d=[],e=[],f=A[a+" "];if(!f){b||(b=g(a)),c=b.length;while(c--)f=wb(b[c]),f[u]?d.push(f):e.push(f);f=A(a,xb(e,d)),f.selector=a}return f},i=fb.select=function(a,b,e,f){var i,j,k,l,m,n="function"==typeof a&&a,o=!f&&g(a=n.selector||a);if(e=e||[],1===o.length){if(j=o[0]=o[0].slice(0),j.length>2&&"ID"===(k=j[0]).type&&c.getById&&9===b.nodeType&&p&&d.relative[j[1].type]){if(b=(d.find.ID(k.matches[0].replace(cb,db),b)||[])[0],!b)return e;n&&(b=b.parentNode),a=a.slice(j.shift().value.length)}i=X.needsContext.test(a)?0:j.length;while(i--){if(k=j[i],d.relative[l=k.type])break;if((m=d.find[l])&&(f=m(k.matches[0].replace(cb,db),ab.test(j[0].type)&&ob(b.parentNode)||b))){if(j.splice(i,1),a=f.length&&qb(j),!a)return I.apply(e,f),e;break}}}return(n||h(a,o))(f,b,!p,e,ab.test(a)&&ob(b.parentNode)||b),e},c.sortStable=u.split("").sort(B).join("")===u,c.detectDuplicates=!!l,m(),c.sortDetached=ib(function(a){return 1&a.compareDocumentPosition(n.createElement("div"))}),ib(function(a){return a.innerHTML="<a href='#'></a>","#"===a.firstChild.getAttribute("href")})||jb("type|href|height|width",function(a,b,c){return c?void 0:a.getAttribute(b,"type"===b.toLowerCase()?1:2)}),c.attributes&&ib(function(a){return a.innerHTML="<input/>",a.firstChild.setAttribute("value",""),""===a.firstChild.getAttribute("value")})||jb("value",function(a,b,c){return c||"input"!==a.nodeName.toLowerCase()?void 0:a.defaultValue}),ib(function(a){return null==a.getAttribute("disabled")})||jb(L,function(a,b,c){var d;return c?void 0:a[b]===!0?b.toLowerCase():(d=a.getAttributeNode(b))&&d.specified?d.value:null}),fb}(a);n.find=t,n.expr=t.selectors,n.expr[":"]=n.expr.pseudos,n.unique=t.uniqueSort,n.text=t.getText,n.isXMLDoc=t.isXML,n.contains=t.contains;var u=n.expr.match.needsContext,v=/^<(\w+)\s*\/?>(?:<\/\1>|)$/,w=/^.[^:#\[\.,]*$/;function x(a,b,c){if(n.isFunction(b))return n.grep(a,function(a,d){return!!b.call(a,d,a)!==c});if(b.nodeType)return n.grep(a,function(a){return a===b!==c});if("string"==typeof b){if(w.test(b))return n.filter(b,a,c);b=n.filter(b,a)}return n.grep(a,function(a){return g.call(b,a)>=0!==c})}n.filter=function(a,b,c){var d=b[0];return c&&(a=":not("+a+")"),1===b.length&&1===d.nodeType?n.find.matchesSelector(d,a)?[d]:[]:n.find.matches(a,n.grep(b,function(a){return 1===a.nodeType}))},n.fn.extend({find:function(a){var b,c=this.length,d=[],e=this;if("string"!=typeof a)return this.pushStack(n(a).filter(function(){for(b=0;c>b;b++)if(n.contains(e[b],this))return!0}));for(b=0;c>b;b++)n.find(a,e[b],d);return d=this.pushStack(c>1?n.unique(d):d),d.selector=this.selector?this.selector+" "+a:a,d},filter:function(a){return this.pushStack(x(this,a||[],!1))},not:function(a){return this.pushStack(x(this,a||[],!0))},is:function(a){return!!x(this,"string"==typeof a&&u.test(a)?n(a):a||[],!1).length}});var y,z=/^(?:\s*(<[\w\W]+>)[^>]*|#([\w-]*))$/,A=n.fn.init=function(a,b){var c,d;if(!a)return this;if("string"==typeof a){if(c="<"===a[0]&&">"===a[a.length-1]&&a.length>=3?[null,a,null]:z.exec(a),!c||!c[1]&&b)return!b||b.jquery?(b||y).find(a):this.constructor(b).find(a);if(c[1]){if(b=b instanceof n?b[0]:b,n.merge(this,n.parseHTML(c[1],b&&b.nodeType?b.ownerDocument||b:l,!0)),v.test(c[1])&&n.isPlainObject(b))for(c in b)n.isFunction(this[c])?this[c](b[c]):this.attr(c,b[c]);return this}return d=l.getElementById(c[2]),d&&d.parentNode&&(this.length=1,this[0]=d),this.context=l,this.selector=a,this}return a.nodeType?(this.context=this[0]=a,this.length=1,this):n.isFunction(a)?"undefined"!=typeof y.ready?y.ready(a):a(n):(void 0!==a.selector&&(this.selector=a.selector,this.context=a.context),n.makeArray(a,this))};A.prototype=n.fn,y=n(l);var B=/^(?:parents|prev(?:Until|All))/,C={children:!0,contents:!0,next:!0,prev:!0};n.extend({dir:function(a,b,c){var d=[],e=void 0!==c;while((a=a[b])&&9!==a.nodeType)if(1===a.nodeType){if(e&&n(a).is(c))break;d.push(a)}return d},sibling:function(a,b){for(var c=[];a;a=a.nextSibling)1===a.nodeType&&a!==b&&c.push(a);return c}}),n.fn.extend({has:function(a){var b=n(a,this),c=b.length;return this.filter(function(){for(var a=0;c>a;a++)if(n.contains(this,b[a]))return!0})},closest:function(a,b){for(var c,d=0,e=this.length,f=[],g=u.test(a)||"string"!=typeof a?n(a,b||this.context):0;e>d;d++)for(c=this[d];c&&c!==b;c=c.parentNode)if(c.nodeType<11&&(g?g.index(c)>-1:1===c.nodeType&&n.find.matchesSelector(c,a))){f.push(c);break}return this.pushStack(f.length>1?n.unique(f):f)},index:function(a){return a?"string"==typeof a?g.call(n(a),this[0]):g.call(this,a.jquery?a[0]:a):this[0]&&this[0].parentNode?this.first().prevAll().length:-1},add:function(a,b){return this.pushStack(n.unique(n.merge(this.get(),n(a,b))))},addBack:function(a){return this.add(null==a?this.prevObject:this.prevObject.filter(a))}});function D(a,b){while((a=a[b])&&1!==a.nodeType);return a}n.each({parent:function(a){var b=a.parentNode;return b&&11!==b.nodeType?b:null},parents:function(a){return n.dir(a,"parentNode")},parentsUntil:function(a,b,c){return n.dir(a,"parentNode",c)},next:function(a){return D(a,"nextSibling")},prev:function(a){return D(a,"previousSibling")},nextAll:function(a){return n.dir(a,"nextSibling")},prevAll:function(a){return n.dir(a,"previousSibling")},nextUntil:function(a,b,c){return n.dir(a,"nextSibling",c)},prevUntil:function(a,b,c){return n.dir(a,"previousSibling",c)},siblings:function(a){return n.sibling((a.parentNode||{}).firstChild,a)},children:function(a){return n.sibling(a.firstChild)},contents:function(a){return a.contentDocument||n.merge([],a.childNodes)}},function(a,b){n.fn[a]=function(c,d){var e=n.map(this,b,c);return"Until"!==a.slice(-5)&&(d=c),d&&"string"==typeof d&&(e=n.filter(d,e)),this.length>1&&(C[a]||n.unique(e),B.test(a)&&e.reverse()),this.pushStack(e)}});var E=/\S+/g,F={};function G(a){var b=F[a]={};return n.each(a.match(E)||[],function(a,c){b[c]=!0}),b}n.Callbacks=function(a){a="string"==typeof a?F[a]||G(a):n.extend({},a);var b,c,d,e,f,g,h=[],i=!a.once&&[],j=function(l){for(b=a.memory&&l,c=!0,g=e||0,e=0,f=h.length,d=!0;h&&f>g;g++)if(h[g].apply(l[0],l[1])===!1&&a.stopOnFalse){b=!1;break}d=!1,h&&(i?i.length&&j(i.shift()):b?h=[]:k.disable())},k={add:function(){if(h){var c=h.length;!function g(b){n.each(b,function(b,c){var d=n.type(c);"function"===d?a.unique&&k.has(c)||h.push(c):c&&c.length&&"string"!==d&&g(c)})}(arguments),d?f=h.length:b&&(e=c,j(b))}return this},remove:function(){return h&&n.each(arguments,function(a,b){var c;while((c=n.inArray(b,h,c))>-1)h.splice(c,1),d&&(f>=c&&f--,g>=c&&g--)}),this},has:function(a){return a?n.inArray(a,h)>-1:!(!h||!h.length)},empty:function(){return h=[],f=0,this},disable:function(){return h=i=b=void 0,this},disabled:function(){return!h},lock:function(){return i=void 0,b||k.disable(),this},locked:function(){return!i},fireWith:function(a,b){return!h||c&&!i||(b=b||[],b=[a,b.slice?b.slice():b],d?i.push(b):j(b)),this},fire:function(){return k.fireWith(this,arguments),this},fired:function(){return!!c}};return k},n.extend({Deferred:function(a){var b=[["resolve","done",n.Callbacks("once memory"),"resolved"],["reject","fail",n.Callbacks("once memory"),"rejected"],["notify","progress",n.Callbacks("memory")]],c="pending",d={state:function(){return c},always:function(){return e.done(arguments).fail(arguments),this},then:function(){var a=arguments;return n.Deferred(function(c){n.each(b,function(b,f){var g=n.isFunction(a[b])&&a[b];e[f[1]](function(){var a=g&&g.apply(this,arguments);a&&n.isFunction(a.promise)?a.promise().done(c.resolve).fail(c.reject).progress(c.notify):c[f[0]+"With"](this===d?c.promise():this,g?[a]:arguments)})}),a=null}).promise()},promise:function(a){return null!=a?n.extend(a,d):d}},e={};return d.pipe=d.then,n.each(b,function(a,f){var g=f[2],h=f[3];d[f[1]]=g.add,h&&g.add(function(){c=h},b[1^a][2].disable,b[2][2].lock),e[f[0]]=function(){return e[f[0]+"With"](this===e?d:this,arguments),this},e[f[0]+"With"]=g.fireWith}),d.promise(e),a&&a.call(e,e),e},when:function(a){var b=0,c=d.call(arguments),e=c.length,f=1!==e||a&&n.isFunction(a.promise)?e:0,g=1===f?a:n.Deferred(),h=function(a,b,c){return function(e){b[a]=this,c[a]=arguments.length>1?d.call(arguments):e,c===i?g.notifyWith(b,c):--f||g.resolveWith(b,c)}},i,j,k;if(e>1)for(i=new Array(e),j=new Array(e),k=new Array(e);e>b;b++)c[b]&&n.isFunction(c[b].promise)?c[b].promise().done(h(b,k,c)).fail(g.reject).progress(h(b,j,i)):--f;return f||g.resolveWith(k,c),g.promise()}});var H;n.fn.ready=function(a){return n.ready.promise().done(a),this},n.extend({isReady:!1,readyWait:1,holdReady:function(a){a?n.readyWait++:n.ready(!0)},ready:function(a){(a===!0?--n.readyWait:n.isReady)||(n.isReady=!0,a!==!0&&--n.readyWait>0||(H.resolveWith(l,[n]),n.fn.triggerHandler&&(n(l).triggerHandler("ready"),n(l).off("ready"))))}});function I(){l.removeEventListener("DOMContentLoaded",I,!1),a.removeEventListener("load",I,!1),n.ready()}n.ready.promise=function(b){return H||(H=n.Deferred(),"complete"===l.readyState?setTimeout(n.ready):(l.addEventListener("DOMContentLoaded",I,!1),a.addEventListener("load",I,!1))),H.promise(b)},n.ready.promise();var J=n.access=function(a,b,c,d,e,f,g){var h=0,i=a.length,j=null==c;if("object"===n.type(c)){e=!0;for(h in c)n.access(a,b,h,c[h],!0,f,g)}else if(void 0!==d&&(e=!0,n.isFunction(d)||(g=!0),j&&(g?(b.call(a,d),b=null):(j=b,b=function(a,b,c){return j.call(n(a),c)})),b))for(;i>h;h++)b(a[h],c,g?d:d.call(a[h],h,b(a[h],c)));return e?a:j?b.call(a):i?b(a[0],c):f};n.acceptData=function(a){return 1===a.nodeType||9===a.nodeType||!+a.nodeType};function K(){Object.defineProperty(this.cache={},0,{get:function(){return{}}}),this.expando=n.expando+Math.random()}K.uid=1,K.accepts=n.acceptData,K.prototype={key:function(a){if(!K.accepts(a))return 0;var b={},c=a[this.expando];if(!c){c=K.uid++;try{b[this.expando]={value:c},Object.defineProperties(a,b)}catch(d){b[this.expando]=c,n.extend(a,b)}}return this.cache[c]||(this.cache[c]={}),c},set:function(a,b,c){var d,e=this.key(a),f=this.cache[e];if("string"==typeof b)f[b]=c;else if(n.isEmptyObject(f))n.extend(this.cache[e],b);else for(d in b)f[d]=b[d];return f},get:function(a,b){var c=this.cache[this.key(a)];return void 0===b?c:c[b]},access:function(a,b,c){var d;return void 0===b||b&&"string"==typeof b&&void 0===c?(d=this.get(a,b),void 0!==d?d:this.get(a,n.camelCase(b))):(this.set(a,b,c),void 0!==c?c:b)},remove:function(a,b){var c,d,e,f=this.key(a),g=this.cache[f];if(void 0===b)this.cache[f]={};else{n.isArray(b)?d=b.concat(b.map(n.camelCase)):(e=n.camelCase(b),b in g?d=[b,e]:(d=e,d=d in g?[d]:d.match(E)||[])),c=d.length;while(c--)delete g[d[c]]}},hasData:function(a){return!n.isEmptyObject(this.cache[a[this.expando]]||{})},discard:function(a){a[this.expando]&&delete this.cache[a[this.expando]]}};var L=new K,M=new K,N=/^(?:\{[\w\W]*\}|\[[\w\W]*\])$/,O=/([A-Z])/g;function P(a,b,c){var d;if(void 0===c&&1===a.nodeType)if(d="data-"+b.replace(O,"-$1").toLowerCase(),c=a.getAttribute(d),"string"==typeof c){try{c="true"===c?!0:"false"===c?!1:"null"===c?null:+c+""===c?+c:N.test(c)?n.parseJSON(c):c}catch(e){}M.set(a,b,c)}else c=void 0;return c}n.extend({hasData:function(a){return M.hasData(a)||L.hasData(a)},data:function(a,b,c){return M.access(a,b,c)},removeData:function(a,b){M.remove(a,b)
},_data:function(a,b,c){return L.access(a,b,c)},_removeData:function(a,b){L.remove(a,b)}}),n.fn.extend({data:function(a,b){var c,d,e,f=this[0],g=f&&f.attributes;if(void 0===a){if(this.length&&(e=M.get(f),1===f.nodeType&&!L.get(f,"hasDataAttrs"))){c=g.length;while(c--)g[c]&&(d=g[c].name,0===d.indexOf("data-")&&(d=n.camelCase(d.slice(5)),P(f,d,e[d])));L.set(f,"hasDataAttrs",!0)}return e}return"object"==typeof a?this.each(function(){M.set(this,a)}):J(this,function(b){var c,d=n.camelCase(a);if(f&&void 0===b){if(c=M.get(f,a),void 0!==c)return c;if(c=M.get(f,d),void 0!==c)return c;if(c=P(f,d,void 0),void 0!==c)return c}else this.each(function(){var c=M.get(this,d);M.set(this,d,b),-1!==a.indexOf("-")&&void 0!==c&&M.set(this,a,b)})},null,b,arguments.length>1,null,!0)},removeData:function(a){return this.each(function(){M.remove(this,a)})}}),n.extend({queue:function(a,b,c){var d;return a?(b=(b||"fx")+"queue",d=L.get(a,b),c&&(!d||n.isArray(c)?d=L.access(a,b,n.makeArray(c)):d.push(c)),d||[]):void 0},dequeue:function(a,b){b=b||"fx";var c=n.queue(a,b),d=c.length,e=c.shift(),f=n._queueHooks(a,b),g=function(){n.dequeue(a,b)};"inprogress"===e&&(e=c.shift(),d--),e&&("fx"===b&&c.unshift("inprogress"),delete f.stop,e.call(a,g,f)),!d&&f&&f.empty.fire()},_queueHooks:function(a,b){var c=b+"queueHooks";return L.get(a,c)||L.access(a,c,{empty:n.Callbacks("once memory").add(function(){L.remove(a,[b+"queue",c])})})}}),n.fn.extend({queue:function(a,b){var c=2;return"string"!=typeof a&&(b=a,a="fx",c--),arguments.length<c?n.queue(this[0],a):void 0===b?this:this.each(function(){var c=n.queue(this,a,b);n._queueHooks(this,a),"fx"===a&&"inprogress"!==c[0]&&n.dequeue(this,a)})},dequeue:function(a){return this.each(function(){n.dequeue(this,a)})},clearQueue:function(a){return this.queue(a||"fx",[])},promise:function(a,b){var c,d=1,e=n.Deferred(),f=this,g=this.length,h=function(){--d||e.resolveWith(f,[f])};"string"!=typeof a&&(b=a,a=void 0),a=a||"fx";while(g--)c=L.get(f[g],a+"queueHooks"),c&&c.empty&&(d++,c.empty.add(h));return h(),e.promise(b)}});var Q=/[+-]?(?:\d*\.|)\d+(?:[eE][+-]?\d+|)/.source,R=["Top","Right","Bottom","Left"],S=function(a,b){return a=b||a,"none"===n.css(a,"display")||!n.contains(a.ownerDocument,a)},T=/^(?:checkbox|radio)$/i;!function(){var a=l.createDocumentFragment(),b=a.appendChild(l.createElement("div")),c=l.createElement("input");c.setAttribute("type","radio"),c.setAttribute("checked","checked"),c.setAttribute("name","t"),b.appendChild(c),k.checkClone=b.cloneNode(!0).cloneNode(!0).lastChild.checked,b.innerHTML="<textarea>x</textarea>",k.noCloneChecked=!!b.cloneNode(!0).lastChild.defaultValue}();var U="undefined";k.focusinBubbles="onfocusin"in a;var V=/^key/,W=/^(?:mouse|pointer|contextmenu)|click/,X=/^(?:focusinfocus|focusoutblur)$/,Y=/^([^.]*)(?:\.(.+)|)$/;function Z(){return!0}function $(){return!1}function _(){try{return l.activeElement}catch(a){}}n.event={global:{},add:function(a,b,c,d,e){var f,g,h,i,j,k,l,m,o,p,q,r=L.get(a);if(r){c.handler&&(f=c,c=f.handler,e=f.selector),c.guid||(c.guid=n.guid++),(i=r.events)||(i=r.events={}),(g=r.handle)||(g=r.handle=function(b){return typeof n!==U&&n.event.triggered!==b.type?n.event.dispatch.apply(a,arguments):void 0}),b=(b||"").match(E)||[""],j=b.length;while(j--)h=Y.exec(b[j])||[],o=q=h[1],p=(h[2]||"").split(".").sort(),o&&(l=n.event.special[o]||{},o=(e?l.delegateType:l.bindType)||o,l=n.event.special[o]||{},k=n.extend({type:o,origType:q,data:d,handler:c,guid:c.guid,selector:e,needsContext:e&&n.expr.match.needsContext.test(e),namespace:p.join(".")},f),(m=i[o])||(m=i[o]=[],m.delegateCount=0,l.setup&&l.setup.call(a,d,p,g)!==!1||a.addEventListener&&a.addEventListener(o,g,!1)),l.add&&(l.add.call(a,k),k.handler.guid||(k.handler.guid=c.guid)),e?m.splice(m.delegateCount++,0,k):m.push(k),n.event.global[o]=!0)}},remove:function(a,b,c,d,e){var f,g,h,i,j,k,l,m,o,p,q,r=L.hasData(a)&&L.get(a);if(r&&(i=r.events)){b=(b||"").match(E)||[""],j=b.length;while(j--)if(h=Y.exec(b[j])||[],o=q=h[1],p=(h[2]||"").split(".").sort(),o){l=n.event.special[o]||{},o=(d?l.delegateType:l.bindType)||o,m=i[o]||[],h=h[2]&&new RegExp("(^|\\.)"+p.join("\\.(?:.*\\.|)")+"(\\.|$)"),g=f=m.length;while(f--)k=m[f],!e&&q!==k.origType||c&&c.guid!==k.guid||h&&!h.test(k.namespace)||d&&d!==k.selector&&("**"!==d||!k.selector)||(m.splice(f,1),k.selector&&m.delegateCount--,l.remove&&l.remove.call(a,k));g&&!m.length&&(l.teardown&&l.teardown.call(a,p,r.handle)!==!1||n.removeEvent(a,o,r.handle),delete i[o])}else for(o in i)n.event.remove(a,o+b[j],c,d,!0);n.isEmptyObject(i)&&(delete r.handle,L.remove(a,"events"))}},trigger:function(b,c,d,e){var f,g,h,i,k,m,o,p=[d||l],q=j.call(b,"type")?b.type:b,r=j.call(b,"namespace")?b.namespace.split("."):[];if(g=h=d=d||l,3!==d.nodeType&&8!==d.nodeType&&!X.test(q+n.event.triggered)&&(q.indexOf(".")>=0&&(r=q.split("."),q=r.shift(),r.sort()),k=q.indexOf(":")<0&&"on"+q,b=b[n.expando]?b:new n.Event(q,"object"==typeof b&&b),b.isTrigger=e?2:3,b.namespace=r.join("."),b.namespace_re=b.namespace?new RegExp("(^|\\.)"+r.join("\\.(?:.*\\.|)")+"(\\.|$)"):null,b.result=void 0,b.target||(b.target=d),c=null==c?[b]:n.makeArray(c,[b]),o=n.event.special[q]||{},e||!o.trigger||o.trigger.apply(d,c)!==!1)){if(!e&&!o.noBubble&&!n.isWindow(d)){for(i=o.delegateType||q,X.test(i+q)||(g=g.parentNode);g;g=g.parentNode)p.push(g),h=g;h===(d.ownerDocument||l)&&p.push(h.defaultView||h.parentWindow||a)}f=0;while((g=p[f++])&&!b.isPropagationStopped())b.type=f>1?i:o.bindType||q,m=(L.get(g,"events")||{})[b.type]&&L.get(g,"handle"),m&&m.apply(g,c),m=k&&g[k],m&&m.apply&&n.acceptData(g)&&(b.result=m.apply(g,c),b.result===!1&&b.preventDefault());return b.type=q,e||b.isDefaultPrevented()||o._default&&o._default.apply(p.pop(),c)!==!1||!n.acceptData(d)||k&&n.isFunction(d[q])&&!n.isWindow(d)&&(h=d[k],h&&(d[k]=null),n.event.triggered=q,d[q](),n.event.triggered=void 0,h&&(d[k]=h)),b.result}},dispatch:function(a){a=n.event.fix(a);var b,c,e,f,g,h=[],i=d.call(arguments),j=(L.get(this,"events")||{})[a.type]||[],k=n.event.special[a.type]||{};if(i[0]=a,a.delegateTarget=this,!k.preDispatch||k.preDispatch.call(this,a)!==!1){h=n.event.handlers.call(this,a,j),b=0;while((f=h[b++])&&!a.isPropagationStopped()){a.currentTarget=f.elem,c=0;while((g=f.handlers[c++])&&!a.isImmediatePropagationStopped())(!a.namespace_re||a.namespace_re.test(g.namespace))&&(a.handleObj=g,a.data=g.data,e=((n.event.special[g.origType]||{}).handle||g.handler).apply(f.elem,i),void 0!==e&&(a.result=e)===!1&&(a.preventDefault(),a.stopPropagation()))}return k.postDispatch&&k.postDispatch.call(this,a),a.result}},handlers:function(a,b){var c,d,e,f,g=[],h=b.delegateCount,i=a.target;if(h&&i.nodeType&&(!a.button||"click"!==a.type))for(;i!==this;i=i.parentNode||this)if(i.disabled!==!0||"click"!==a.type){for(d=[],c=0;h>c;c++)f=b[c],e=f.selector+" ",void 0===d[e]&&(d[e]=f.needsContext?n(e,this).index(i)>=0:n.find(e,this,null,[i]).length),d[e]&&d.push(f);d.length&&g.push({elem:i,handlers:d})}return h<b.length&&g.push({elem:this,handlers:b.slice(h)}),g},props:"altKey bubbles cancelable ctrlKey currentTarget eventPhase metaKey relatedTarget shiftKey target timeStamp view which".split(" "),fixHooks:{},keyHooks:{props:"char charCode key keyCode".split(" "),filter:function(a,b){return null==a.which&&(a.which=null!=b.charCode?b.charCode:b.keyCode),a}},mouseHooks:{props:"button buttons clientX clientY offsetX offsetY pageX pageY screenX screenY toElement".split(" "),filter:function(a,b){var c,d,e,f=b.button;return null==a.pageX&&null!=b.clientX&&(c=a.target.ownerDocument||l,d=c.documentElement,e=c.body,a.pageX=b.clientX+(d&&d.scrollLeft||e&&e.scrollLeft||0)-(d&&d.clientLeft||e&&e.clientLeft||0),a.pageY=b.clientY+(d&&d.scrollTop||e&&e.scrollTop||0)-(d&&d.clientTop||e&&e.clientTop||0)),a.which||void 0===f||(a.which=1&f?1:2&f?3:4&f?2:0),a}},fix:function(a){if(a[n.expando])return a;var b,c,d,e=a.type,f=a,g=this.fixHooks[e];g||(this.fixHooks[e]=g=W.test(e)?this.mouseHooks:V.test(e)?this.keyHooks:{}),d=g.props?this.props.concat(g.props):this.props,a=new n.Event(f),b=d.length;while(b--)c=d[b],a[c]=f[c];return a.target||(a.target=l),3===a.target.nodeType&&(a.target=a.target.parentNode),g.filter?g.filter(a,f):a},special:{load:{noBubble:!0},focus:{trigger:function(){return this!==_()&&this.focus?(this.focus(),!1):void 0},delegateType:"focusin"},blur:{trigger:function(){return this===_()&&this.blur?(this.blur(),!1):void 0},delegateType:"focusout"},click:{trigger:function(){return"checkbox"===this.type&&this.click&&n.nodeName(this,"input")?(this.click(),!1):void 0},_default:function(a){return n.nodeName(a.target,"a")}},beforeunload:{postDispatch:function(a){void 0!==a.result&&a.originalEvent&&(a.originalEvent.returnValue=a.result)}}},simulate:function(a,b,c,d){var e=n.extend(new n.Event,c,{type:a,isSimulated:!0,originalEvent:{}});d?n.event.trigger(e,null,b):n.event.dispatch.call(b,e),e.isDefaultPrevented()&&c.preventDefault()}},n.removeEvent=function(a,b,c){a.removeEventListener&&a.removeEventListener(b,c,!1)},n.Event=function(a,b){return this instanceof n.Event?(a&&a.type?(this.originalEvent=a,this.type=a.type,this.isDefaultPrevented=a.defaultPrevented||void 0===a.defaultPrevented&&a.returnValue===!1?Z:$):this.type=a,b&&n.extend(this,b),this.timeStamp=a&&a.timeStamp||n.now(),void(this[n.expando]=!0)):new n.Event(a,b)},n.Event.prototype={isDefaultPrevented:$,isPropagationStopped:$,isImmediatePropagationStopped:$,preventDefault:function(){var a=this.originalEvent;this.isDefaultPrevented=Z,a&&a.preventDefault&&a.preventDefault()},stopPropagation:function(){var a=this.originalEvent;this.isPropagationStopped=Z,a&&a.stopPropagation&&a.stopPropagation()},stopImmediatePropagation:function(){var a=this.originalEvent;this.isImmediatePropagationStopped=Z,a&&a.stopImmediatePropagation&&a.stopImmediatePropagation(),this.stopPropagation()}},n.each({mouseenter:"mouseover",mouseleave:"mouseout",pointerenter:"pointerover",pointerleave:"pointerout"},function(a,b){n.event.special[a]={delegateType:b,bindType:b,handle:function(a){var c,d=this,e=a.relatedTarget,f=a.handleObj;return(!e||e!==d&&!n.contains(d,e))&&(a.type=f.origType,c=f.handler.apply(this,arguments),a.type=b),c}}}),k.focusinBubbles||n.each({focus:"focusin",blur:"focusout"},function(a,b){var c=function(a){n.event.simulate(b,a.target,n.event.fix(a),!0)};n.event.special[b]={setup:function(){var d=this.ownerDocument||this,e=L.access(d,b);e||d.addEventListener(a,c,!0),L.access(d,b,(e||0)+1)},teardown:function(){var d=this.ownerDocument||this,e=L.access(d,b)-1;e?L.access(d,b,e):(d.removeEventListener(a,c,!0),L.remove(d,b))}}}),n.fn.extend({on:function(a,b,c,d,e){var f,g;if("object"==typeof a){"string"!=typeof b&&(c=c||b,b=void 0);for(g in a)this.on(g,b,c,a[g],e);return this}if(null==c&&null==d?(d=b,c=b=void 0):null==d&&("string"==typeof b?(d=c,c=void 0):(d=c,c=b,b=void 0)),d===!1)d=$;else if(!d)return this;return 1===e&&(f=d,d=function(a){return n().off(a),f.apply(this,arguments)},d.guid=f.guid||(f.guid=n.guid++)),this.each(function(){n.event.add(this,a,d,c,b)})},one:function(a,b,c,d){return this.on(a,b,c,d,1)},off:function(a,b,c){var d,e;if(a&&a.preventDefault&&a.handleObj)return d=a.handleObj,n(a.delegateTarget).off(d.namespace?d.origType+"."+d.namespace:d.origType,d.selector,d.handler),this;if("object"==typeof a){for(e in a)this.off(e,b,a[e]);return this}return(b===!1||"function"==typeof b)&&(c=b,b=void 0),c===!1&&(c=$),this.each(function(){n.event.remove(this,a,c,b)})},trigger:function(a,b){return this.each(function(){n.event.trigger(a,b,this)})},triggerHandler:function(a,b){var c=this[0];return c?n.event.trigger(a,b,c,!0):void 0}});var ab=/<(?!area|br|col|embed|hr|img|input|link|meta|param)(([\w:]+)[^>]*)\/>/gi,bb=/<([\w:]+)/,cb=/<|&#?\w+;/,db=/<(?:script|style|link)/i,eb=/checked\s*(?:[^=]|=\s*.checked.)/i,fb=/^$|\/(?:java|ecma)script/i,gb=/^true\/(.*)/,hb=/^\s*<!(?:\[CDATA\[|--)|(?:\]\]|--)>\s*$/g,ib={option:[1,"<select multiple='multiple'>","</select>"],thead:[1,"<table>","</table>"],col:[2,"<table><colgroup>","</colgroup></table>"],tr:[2,"<table><tbody>","</tbody></table>"],td:[3,"<table><tbody><tr>","</tr></tbody></table>"],_default:[0,"",""]};ib.optgroup=ib.option,ib.tbody=ib.tfoot=ib.colgroup=ib.caption=ib.thead,ib.th=ib.td;function jb(a,b){return n.nodeName(a,"table")&&n.nodeName(11!==b.nodeType?b:b.firstChild,"tr")?a.getElementsByTagName("tbody")[0]||a.appendChild(a.ownerDocument.createElement("tbody")):a}function kb(a){return a.type=(null!==a.getAttribute("type"))+"/"+a.type,a}function lb(a){var b=gb.exec(a.type);return b?a.type=b[1]:a.removeAttribute("type"),a}function mb(a,b){for(var c=0,d=a.length;d>c;c++)L.set(a[c],"globalEval",!b||L.get(b[c],"globalEval"))}function nb(a,b){var c,d,e,f,g,h,i,j;if(1===b.nodeType){if(L.hasData(a)&&(f=L.access(a),g=L.set(b,f),j=f.events)){delete g.handle,g.events={};for(e in j)for(c=0,d=j[e].length;d>c;c++)n.event.add(b,e,j[e][c])}M.hasData(a)&&(h=M.access(a),i=n.extend({},h),M.set(b,i))}}function ob(a,b){var c=a.getElementsByTagName?a.getElementsByTagName(b||"*"):a.querySelectorAll?a.querySelectorAll(b||"*"):[];return void 0===b||b&&n.nodeName(a,b)?n.merge([a],c):c}function pb(a,b){var c=b.nodeName.toLowerCase();"input"===c&&T.test(a.type)?b.checked=a.checked:("input"===c||"textarea"===c)&&(b.defaultValue=a.defaultValue)}n.extend({clone:function(a,b,c){var d,e,f,g,h=a.cloneNode(!0),i=n.contains(a.ownerDocument,a);if(!(k.noCloneChecked||1!==a.nodeType&&11!==a.nodeType||n.isXMLDoc(a)))for(g=ob(h),f=ob(a),d=0,e=f.length;e>d;d++)pb(f[d],g[d]);if(b)if(c)for(f=f||ob(a),g=g||ob(h),d=0,e=f.length;e>d;d++)nb(f[d],g[d]);else nb(a,h);return g=ob(h,"script"),g.length>0&&mb(g,!i&&ob(a,"script")),h},buildFragment:function(a,b,c,d){for(var e,f,g,h,i,j,k=b.createDocumentFragment(),l=[],m=0,o=a.length;o>m;m++)if(e=a[m],e||0===e)if("object"===n.type(e))n.merge(l,e.nodeType?[e]:e);else if(cb.test(e)){f=f||k.appendChild(b.createElement("div")),g=(bb.exec(e)||["",""])[1].toLowerCase(),h=ib[g]||ib._default,f.innerHTML=h[1]+e.replace(ab,"<$1></$2>")+h[2],j=h[0];while(j--)f=f.lastChild;n.merge(l,f.childNodes),f=k.firstChild,f.textContent=""}else l.push(b.createTextNode(e));k.textContent="",m=0;while(e=l[m++])if((!d||-1===n.inArray(e,d))&&(i=n.contains(e.ownerDocument,e),f=ob(k.appendChild(e),"script"),i&&mb(f),c)){j=0;while(e=f[j++])fb.test(e.type||"")&&c.push(e)}return k},cleanData:function(a){for(var b,c,d,e,f=n.event.special,g=0;void 0!==(c=a[g]);g++){if(n.acceptData(c)&&(e=c[L.expando],e&&(b=L.cache[e]))){if(b.events)for(d in b.events)f[d]?n.event.remove(c,d):n.removeEvent(c,d,b.handle);L.cache[e]&&delete L.cache[e]}delete M.cache[c[M.expando]]}}}),n.fn.extend({text:function(a){return J(this,function(a){return void 0===a?n.text(this):this.empty().each(function(){(1===this.nodeType||11===this.nodeType||9===this.nodeType)&&(this.textContent=a)})},null,a,arguments.length)},append:function(){return this.domManip(arguments,function(a){if(1===this.nodeType||11===this.nodeType||9===this.nodeType){var b=jb(this,a);b.appendChild(a)}})},prepend:function(){return this.domManip(arguments,function(a){if(1===this.nodeType||11===this.nodeType||9===this.nodeType){var b=jb(this,a);b.insertBefore(a,b.firstChild)}})},before:function(){return this.domManip(arguments,function(a){this.parentNode&&this.parentNode.insertBefore(a,this)})},after:function(){return this.domManip(arguments,function(a){this.parentNode&&this.parentNode.insertBefore(a,this.nextSibling)})},remove:function(a,b){for(var c,d=a?n.filter(a,this):this,e=0;null!=(c=d[e]);e++)b||1!==c.nodeType||n.cleanData(ob(c)),c.parentNode&&(b&&n.contains(c.ownerDocument,c)&&mb(ob(c,"script")),c.parentNode.removeChild(c));return this},empty:function(){for(var a,b=0;null!=(a=this[b]);b++)1===a.nodeType&&(n.cleanData(ob(a,!1)),a.textContent="");return this},clone:function(a,b){return a=null==a?!1:a,b=null==b?a:b,this.map(function(){return n.clone(this,a,b)})},html:function(a){return J(this,function(a){var b=this[0]||{},c=0,d=this.length;if(void 0===a&&1===b.nodeType)return b.innerHTML;if("string"==typeof a&&!db.test(a)&&!ib[(bb.exec(a)||["",""])[1].toLowerCase()]){a=a.replace(ab,"<$1></$2>");try{for(;d>c;c++)b=this[c]||{},1===b.nodeType&&(n.cleanData(ob(b,!1)),b.innerHTML=a);b=0}catch(e){}}b&&this.empty().append(a)},null,a,arguments.length)},replaceWith:function(){var a=arguments[0];return this.domManip(arguments,function(b){a=this.parentNode,n.cleanData(ob(this)),a&&a.replaceChild(b,this)}),a&&(a.length||a.nodeType)?this:this.remove()},detach:function(a){return this.remove(a,!0)},domManip:function(a,b){a=e.apply([],a);var c,d,f,g,h,i,j=0,l=this.length,m=this,o=l-1,p=a[0],q=n.isFunction(p);if(q||l>1&&"string"==typeof p&&!k.checkClone&&eb.test(p))return this.each(function(c){var d=m.eq(c);q&&(a[0]=p.call(this,c,d.html())),d.domManip(a,b)});if(l&&(c=n.buildFragment(a,this[0].ownerDocument,!1,this),d=c.firstChild,1===c.childNodes.length&&(c=d),d)){for(f=n.map(ob(c,"script"),kb),g=f.length;l>j;j++)h=c,j!==o&&(h=n.clone(h,!0,!0),g&&n.merge(f,ob(h,"script"))),b.call(this[j],h,j);if(g)for(i=f[f.length-1].ownerDocument,n.map(f,lb),j=0;g>j;j++)h=f[j],fb.test(h.type||"")&&!L.access(h,"globalEval")&&n.contains(i,h)&&(h.src?n._evalUrl&&n._evalUrl(h.src):n.globalEval(h.textContent.replace(hb,"")))}return this}}),n.each({appendTo:"append",prependTo:"prepend",insertBefore:"before",insertAfter:"after",replaceAll:"replaceWith"},function(a,b){n.fn[a]=function(a){for(var c,d=[],e=n(a),g=e.length-1,h=0;g>=h;h++)c=h===g?this:this.clone(!0),n(e[h])[b](c),f.apply(d,c.get());return this.pushStack(d)}});var qb,rb={};function sb(b,c){var d,e=n(c.createElement(b)).appendTo(c.body),f=a.getDefaultComputedStyle&&(d=a.getDefaultComputedStyle(e[0]))?d.display:n.css(e[0],"display");return e.detach(),f}function tb(a){var b=l,c=rb[a];return c||(c=sb(a,b),"none"!==c&&c||(qb=(qb||n("<iframe frameborder='0' width='0' height='0'/>")).appendTo(b.documentElement),b=qb[0].contentDocument,b.write(),b.close(),c=sb(a,b),qb.detach()),rb[a]=c),c}var ub=/^margin/,vb=new RegExp("^("+Q+")(?!px)[a-z%]+$","i"),wb=function(a){return a.ownerDocument.defaultView.getComputedStyle(a,null)};function xb(a,b,c){var d,e,f,g,h=a.style;return c=c||wb(a),c&&(g=c.getPropertyValue(b)||c[b]),c&&(""!==g||n.contains(a.ownerDocument,a)||(g=n.style(a,b)),vb.test(g)&&ub.test(b)&&(d=h.width,e=h.minWidth,f=h.maxWidth,h.minWidth=h.maxWidth=h.width=g,g=c.width,h.width=d,h.minWidth=e,h.maxWidth=f)),void 0!==g?g+"":g}function yb(a,b){return{get:function(){return a()?void delete this.get:(this.get=b).apply(this,arguments)}}}!function(){var b,c,d=l.documentElement,e=l.createElement("div"),f=l.createElement("div");if(f.style){f.style.backgroundClip="content-box",f.cloneNode(!0).style.backgroundClip="",k.clearCloneStyle="content-box"===f.style.backgroundClip,e.style.cssText="border:0;width:0;height:0;top:0;left:-9999px;margin-top:1px;position:absolute",e.appendChild(f);function g(){f.style.cssText="-webkit-box-sizing:border-box;-moz-box-sizing:border-box;box-sizing:border-box;display:block;margin-top:1%;top:1%;border:1px;padding:1px;width:4px;position:absolute",f.innerHTML="",d.appendChild(e);var g=a.getComputedStyle(f,null);b="1%"!==g.top,c="4px"===g.width,d.removeChild(e)}a.getComputedStyle&&n.extend(k,{pixelPosition:function(){return g(),b},boxSizingReliable:function(){return null==c&&g(),c},reliableMarginRight:function(){var b,c=f.appendChild(l.createElement("div"));return c.style.cssText=f.style.cssText="-webkit-box-sizing:content-box;-moz-box-sizing:content-box;box-sizing:content-box;display:block;margin:0;border:0;padding:0",c.style.marginRight=c.style.width="0",f.style.width="1px",d.appendChild(e),b=!parseFloat(a.getComputedStyle(c,null).marginRight),d.removeChild(e),b}})}}(),n.swap=function(a,b,c,d){var e,f,g={};for(f in b)g[f]=a.style[f],a.style[f]=b[f];e=c.apply(a,d||[]);for(f in b)a.style[f]=g[f];return e};var zb=/^(none|table(?!-c[ea]).+)/,Ab=new RegExp("^("+Q+")(.*)$","i"),Bb=new RegExp("^([+-])=("+Q+")","i"),Cb={position:"absolute",visibility:"hidden",display:"block"},Db={letterSpacing:"0",fontWeight:"400"},Eb=["Webkit","O","Moz","ms"];function Fb(a,b){if(b in a)return b;var c=b[0].toUpperCase()+b.slice(1),d=b,e=Eb.length;while(e--)if(b=Eb[e]+c,b in a)return b;return d}function Gb(a,b,c){var d=Ab.exec(b);return d?Math.max(0,d[1]-(c||0))+(d[2]||"px"):b}function Hb(a,b,c,d,e){for(var f=c===(d?"border":"content")?4:"width"===b?1:0,g=0;4>f;f+=2)"margin"===c&&(g+=n.css(a,c+R[f],!0,e)),d?("content"===c&&(g-=n.css(a,"padding"+R[f],!0,e)),"margin"!==c&&(g-=n.css(a,"border"+R[f]+"Width",!0,e))):(g+=n.css(a,"padding"+R[f],!0,e),"padding"!==c&&(g+=n.css(a,"border"+R[f]+"Width",!0,e)));return g}function Ib(a,b,c){var d=!0,e="width"===b?a.offsetWidth:a.offsetHeight,f=wb(a),g="border-box"===n.css(a,"boxSizing",!1,f);if(0>=e||null==e){if(e=xb(a,b,f),(0>e||null==e)&&(e=a.style[b]),vb.test(e))return e;d=g&&(k.boxSizingReliable()||e===a.style[b]),e=parseFloat(e)||0}return e+Hb(a,b,c||(g?"border":"content"),d,f)+"px"}function Jb(a,b){for(var c,d,e,f=[],g=0,h=a.length;h>g;g++)d=a[g],d.style&&(f[g]=L.get(d,"olddisplay"),c=d.style.display,b?(f[g]||"none"!==c||(d.style.display=""),""===d.style.display&&S(d)&&(f[g]=L.access(d,"olddisplay",tb(d.nodeName)))):(e=S(d),"none"===c&&e||L.set(d,"olddisplay",e?c:n.css(d,"display"))));for(g=0;h>g;g++)d=a[g],d.style&&(b&&"none"!==d.style.display&&""!==d.style.display||(d.style.display=b?f[g]||"":"none"));return a}n.extend({cssHooks:{opacity:{get:function(a,b){if(b){var c=xb(a,"opacity");return""===c?"1":c}}}},cssNumber:{columnCount:!0,fillOpacity:!0,flexGrow:!0,flexShrink:!0,fontWeight:!0,lineHeight:!0,opacity:!0,order:!0,orphans:!0,widows:!0,zIndex:!0,zoom:!0},cssProps:{"float":"cssFloat"},style:function(a,b,c,d){if(a&&3!==a.nodeType&&8!==a.nodeType&&a.style){var e,f,g,h=n.camelCase(b),i=a.style;return b=n.cssProps[h]||(n.cssProps[h]=Fb(i,h)),g=n.cssHooks[b]||n.cssHooks[h],void 0===c?g&&"get"in g&&void 0!==(e=g.get(a,!1,d))?e:i[b]:(f=typeof c,"string"===f&&(e=Bb.exec(c))&&(c=(e[1]+1)*e[2]+parseFloat(n.css(a,b)),f="number"),null!=c&&c===c&&("number"!==f||n.cssNumber[h]||(c+="px"),k.clearCloneStyle||""!==c||0!==b.indexOf("background")||(i[b]="inherit"),g&&"set"in g&&void 0===(c=g.set(a,c,d))||(i[b]=c)),void 0)}},css:function(a,b,c,d){var e,f,g,h=n.camelCase(b);return b=n.cssProps[h]||(n.cssProps[h]=Fb(a.style,h)),g=n.cssHooks[b]||n.cssHooks[h],g&&"get"in g&&(e=g.get(a,!0,c)),void 0===e&&(e=xb(a,b,d)),"normal"===e&&b in Db&&(e=Db[b]),""===c||c?(f=parseFloat(e),c===!0||n.isNumeric(f)?f||0:e):e}}),n.each(["height","width"],function(a,b){n.cssHooks[b]={get:function(a,c,d){return c?zb.test(n.css(a,"display"))&&0===a.offsetWidth?n.swap(a,Cb,function(){return Ib(a,b,d)}):Ib(a,b,d):void 0},set:function(a,c,d){var e=d&&wb(a);return Gb(a,c,d?Hb(a,b,d,"border-box"===n.css(a,"boxSizing",!1,e),e):0)}}}),n.cssHooks.marginRight=yb(k.reliableMarginRight,function(a,b){return b?n.swap(a,{display:"inline-block"},xb,[a,"marginRight"]):void 0}),n.each({margin:"",padding:"",border:"Width"},function(a,b){n.cssHooks[a+b]={expand:function(c){for(var d=0,e={},f="string"==typeof c?c.split(" "):[c];4>d;d++)e[a+R[d]+b]=f[d]||f[d-2]||f[0];return e}},ub.test(a)||(n.cssHooks[a+b].set=Gb)}),n.fn.extend({css:function(a,b){return J(this,function(a,b,c){var d,e,f={},g=0;if(n.isArray(b)){for(d=wb(a),e=b.length;e>g;g++)f[b[g]]=n.css(a,b[g],!1,d);return f}return void 0!==c?n.style(a,b,c):n.css(a,b)},a,b,arguments.length>1)},show:function(){return Jb(this,!0)},hide:function(){return Jb(this)},toggle:function(a){return"boolean"==typeof a?a?this.show():this.hide():this.each(function(){S(this)?n(this).show():n(this).hide()})}});function Kb(a,b,c,d,e){return new Kb.prototype.init(a,b,c,d,e)}n.Tween=Kb,Kb.prototype={constructor:Kb,init:function(a,b,c,d,e,f){this.elem=a,this.prop=c,this.easing=e||"swing",this.options=b,this.start=this.now=this.cur(),this.end=d,this.unit=f||(n.cssNumber[c]?"":"px")},cur:function(){var a=Kb.propHooks[this.prop];return a&&a.get?a.get(this):Kb.propHooks._default.get(this)},run:function(a){var b,c=Kb.propHooks[this.prop];return this.pos=b=this.options.duration?n.easing[this.easing](a,this.options.duration*a,0,1,this.options.duration):a,this.now=(this.end-this.start)*b+this.start,this.options.step&&this.options.step.call(this.elem,this.now,this),c&&c.set?c.set(this):Kb.propHooks._default.set(this),this}},Kb.prototype.init.prototype=Kb.prototype,Kb.propHooks={_default:{get:function(a){var b;return null==a.elem[a.prop]||a.elem.style&&null!=a.elem.style[a.prop]?(b=n.css(a.elem,a.prop,""),b&&"auto"!==b?b:0):a.elem[a.prop]},set:function(a){n.fx.step[a.prop]?n.fx.step[a.prop](a):a.elem.style&&(null!=a.elem.style[n.cssProps[a.prop]]||n.cssHooks[a.prop])?n.style(a.elem,a.prop,a.now+a.unit):a.elem[a.prop]=a.now}}},Kb.propHooks.scrollTop=Kb.propHooks.scrollLeft={set:function(a){a.elem.nodeType&&a.elem.parentNode&&(a.elem[a.prop]=a.now)}},n.easing={linear:function(a){return a},swing:function(a){return.5-Math.cos(a*Math.PI)/2}},n.fx=Kb.prototype.init,n.fx.step={};var Lb,Mb,Nb=/^(?:toggle|show|hide)$/,Ob=new RegExp("^(?:([+-])=|)("+Q+")([a-z%]*)$","i"),Pb=/queueHooks$/,Qb=[Vb],Rb={"*":[function(a,b){var c=this.createTween(a,b),d=c.cur(),e=Ob.exec(b),f=e&&e[3]||(n.cssNumber[a]?"":"px"),g=(n.cssNumber[a]||"px"!==f&&+d)&&Ob.exec(n.css(c.elem,a)),h=1,i=20;if(g&&g[3]!==f){f=f||g[3],e=e||[],g=+d||1;do h=h||".5",g/=h,n.style(c.elem,a,g+f);while(h!==(h=c.cur()/d)&&1!==h&&--i)}return e&&(g=c.start=+g||+d||0,c.unit=f,c.end=e[1]?g+(e[1]+1)*e[2]:+e[2]),c}]};function Sb(){return setTimeout(function(){Lb=void 0}),Lb=n.now()}function Tb(a,b){var c,d=0,e={height:a};for(b=b?1:0;4>d;d+=2-b)c=R[d],e["margin"+c]=e["padding"+c]=a;return b&&(e.opacity=e.width=a),e}function Ub(a,b,c){for(var d,e=(Rb[b]||[]).concat(Rb["*"]),f=0,g=e.length;g>f;f++)if(d=e[f].call(c,b,a))return d}function Vb(a,b,c){var d,e,f,g,h,i,j,k,l=this,m={},o=a.style,p=a.nodeType&&S(a),q=L.get(a,"fxshow");c.queue||(h=n._queueHooks(a,"fx"),null==h.unqueued&&(h.unqueued=0,i=h.empty.fire,h.empty.fire=function(){h.unqueued||i()}),h.unqueued++,l.always(function(){l.always(function(){h.unqueued--,n.queue(a,"fx").length||h.empty.fire()})})),1===a.nodeType&&("height"in b||"width"in b)&&(c.overflow=[o.overflow,o.overflowX,o.overflowY],j=n.css(a,"display"),k="none"===j?L.get(a,"olddisplay")||tb(a.nodeName):j,"inline"===k&&"none"===n.css(a,"float")&&(o.display="inline-block")),c.overflow&&(o.overflow="hidden",l.always(function(){o.overflow=c.overflow[0],o.overflowX=c.overflow[1],o.overflowY=c.overflow[2]}));for(d in b)if(e=b[d],Nb.exec(e)){if(delete b[d],f=f||"toggle"===e,e===(p?"hide":"show")){if("show"!==e||!q||void 0===q[d])continue;p=!0}m[d]=q&&q[d]||n.style(a,d)}else j=void 0;if(n.isEmptyObject(m))"inline"===("none"===j?tb(a.nodeName):j)&&(o.display=j);else{q?"hidden"in q&&(p=q.hidden):q=L.access(a,"fxshow",{}),f&&(q.hidden=!p),p?n(a).show():l.done(function(){n(a).hide()}),l.done(function(){var b;L.remove(a,"fxshow");for(b in m)n.style(a,b,m[b])});for(d in m)g=Ub(p?q[d]:0,d,l),d in q||(q[d]=g.start,p&&(g.end=g.start,g.start="width"===d||"height"===d?1:0))}}function Wb(a,b){var c,d,e,f,g;for(c in a)if(d=n.camelCase(c),e=b[d],f=a[c],n.isArray(f)&&(e=f[1],f=a[c]=f[0]),c!==d&&(a[d]=f,delete a[c]),g=n.cssHooks[d],g&&"expand"in g){f=g.expand(f),delete a[d];for(c in f)c in a||(a[c]=f[c],b[c]=e)}else b[d]=e}function Xb(a,b,c){var d,e,f=0,g=Qb.length,h=n.Deferred().always(function(){delete i.elem}),i=function(){if(e)return!1;for(var b=Lb||Sb(),c=Math.max(0,j.startTime+j.duration-b),d=c/j.duration||0,f=1-d,g=0,i=j.tweens.length;i>g;g++)j.tweens[g].run(f);return h.notifyWith(a,[j,f,c]),1>f&&i?c:(h.resolveWith(a,[j]),!1)},j=h.promise({elem:a,props:n.extend({},b),opts:n.extend(!0,{specialEasing:{}},c),originalProperties:b,originalOptions:c,startTime:Lb||Sb(),duration:c.duration,tweens:[],createTween:function(b,c){var d=n.Tween(a,j.opts,b,c,j.opts.specialEasing[b]||j.opts.easing);return j.tweens.push(d),d},stop:function(b){var c=0,d=b?j.tweens.length:0;if(e)return this;for(e=!0;d>c;c++)j.tweens[c].run(1);return b?h.resolveWith(a,[j,b]):h.rejectWith(a,[j,b]),this}}),k=j.props;for(Wb(k,j.opts.specialEasing);g>f;f++)if(d=Qb[f].call(j,a,k,j.opts))return d;return n.map(k,Ub,j),n.isFunction(j.opts.start)&&j.opts.start.call(a,j),n.fx.timer(n.extend(i,{elem:a,anim:j,queue:j.opts.queue})),j.progress(j.opts.progress).done(j.opts.done,j.opts.complete).fail(j.opts.fail).always(j.opts.always)}n.Animation=n.extend(Xb,{tweener:function(a,b){n.isFunction(a)?(b=a,a=["*"]):a=a.split(" ");for(var c,d=0,e=a.length;e>d;d++)c=a[d],Rb[c]=Rb[c]||[],Rb[c].unshift(b)},prefilter:function(a,b){b?Qb.unshift(a):Qb.push(a)}}),n.speed=function(a,b,c){var d=a&&"object"==typeof a?n.extend({},a):{complete:c||!c&&b||n.isFunction(a)&&a,duration:a,easing:c&&b||b&&!n.isFunction(b)&&b};return d.duration=n.fx.off?0:"number"==typeof d.duration?d.duration:d.duration in n.fx.speeds?n.fx.speeds[d.duration]:n.fx.speeds._default,(null==d.queue||d.queue===!0)&&(d.queue="fx"),d.old=d.complete,d.complete=function(){n.isFunction(d.old)&&d.old.call(this),d.queue&&n.dequeue(this,d.queue)},d},n.fn.extend({fadeTo:function(a,b,c,d){return this.filter(S).css("opacity",0).show().end().animate({opacity:b},a,c,d)},animate:function(a,b,c,d){var e=n.isEmptyObject(a),f=n.speed(b,c,d),g=function(){var b=Xb(this,n.extend({},a),f);(e||L.get(this,"finish"))&&b.stop(!0)};return g.finish=g,e||f.queue===!1?this.each(g):this.queue(f.queue,g)},stop:function(a,b,c){var d=function(a){var b=a.stop;delete a.stop,b(c)};return"string"!=typeof a&&(c=b,b=a,a=void 0),b&&a!==!1&&this.queue(a||"fx",[]),this.each(function(){var b=!0,e=null!=a&&a+"queueHooks",f=n.timers,g=L.get(this);if(e)g[e]&&g[e].stop&&d(g[e]);else for(e in g)g[e]&&g[e].stop&&Pb.test(e)&&d(g[e]);for(e=f.length;e--;)f[e].elem!==this||null!=a&&f[e].queue!==a||(f[e].anim.stop(c),b=!1,f.splice(e,1));(b||!c)&&n.dequeue(this,a)})},finish:function(a){return a!==!1&&(a=a||"fx"),this.each(function(){var b,c=L.get(this),d=c[a+"queue"],e=c[a+"queueHooks"],f=n.timers,g=d?d.length:0;for(c.finish=!0,n.queue(this,a,[]),e&&e.stop&&e.stop.call(this,!0),b=f.length;b--;)f[b].elem===this&&f[b].queue===a&&(f[b].anim.stop(!0),f.splice(b,1));for(b=0;g>b;b++)d[b]&&d[b].finish&&d[b].finish.call(this);delete c.finish})}}),n.each(["toggle","show","hide"],function(a,b){var c=n.fn[b];n.fn[b]=function(a,d,e){return null==a||"boolean"==typeof a?c.apply(this,arguments):this.animate(Tb(b,!0),a,d,e)}}),n.each({slideDown:Tb("show"),slideUp:Tb("hide"),slideToggle:Tb("toggle"),fadeIn:{opacity:"show"},fadeOut:{opacity:"hide"},fadeToggle:{opacity:"toggle"}},function(a,b){n.fn[a]=function(a,c,d){return this.animate(b,a,c,d)}}),n.timers=[],n.fx.tick=function(){var a,b=0,c=n.timers;for(Lb=n.now();b<c.length;b++)a=c[b],a()||c[b]!==a||c.splice(b--,1);c.length||n.fx.stop(),Lb=void 0},n.fx.timer=function(a){n.timers.push(a),a()?n.fx.start():n.timers.pop()},n.fx.interval=13,n.fx.start=function(){Mb||(Mb=setInterval(n.fx.tick,n.fx.interval))},n.fx.stop=function(){clearInterval(Mb),Mb=null},n.fx.speeds={slow:600,fast:200,_default:400},n.fn.delay=function(a,b){return a=n.fx?n.fx.speeds[a]||a:a,b=b||"fx",this.queue(b,function(b,c){var d=setTimeout(b,a);c.stop=function(){clearTimeout(d)}})},function(){var a=l.createElement("input"),b=l.createElement("select"),c=b.appendChild(l.createElement("option"));a.type="checkbox",k.checkOn=""!==a.value,k.optSelected=c.selected,b.disabled=!0,k.optDisabled=!c.disabled,a=l.createElement("input"),a.value="t",a.type="radio",k.radioValue="t"===a.value}();var Yb,Zb,$b=n.expr.attrHandle;n.fn.extend({attr:function(a,b){return J(this,n.attr,a,b,arguments.length>1)},removeAttr:function(a){return this.each(function(){n.removeAttr(this,a)})}}),n.extend({attr:function(a,b,c){var d,e,f=a.nodeType;if(a&&3!==f&&8!==f&&2!==f)return typeof a.getAttribute===U?n.prop(a,b,c):(1===f&&n.isXMLDoc(a)||(b=b.toLowerCase(),d=n.attrHooks[b]||(n.expr.match.bool.test(b)?Zb:Yb)),void 0===c?d&&"get"in d&&null!==(e=d.get(a,b))?e:(e=n.find.attr(a,b),null==e?void 0:e):null!==c?d&&"set"in d&&void 0!==(e=d.set(a,c,b))?e:(a.setAttribute(b,c+""),c):void n.removeAttr(a,b))
},removeAttr:function(a,b){var c,d,e=0,f=b&&b.match(E);if(f&&1===a.nodeType)while(c=f[e++])d=n.propFix[c]||c,n.expr.match.bool.test(c)&&(a[d]=!1),a.removeAttribute(c)},attrHooks:{type:{set:function(a,b){if(!k.radioValue&&"radio"===b&&n.nodeName(a,"input")){var c=a.value;return a.setAttribute("type",b),c&&(a.value=c),b}}}}}),Zb={set:function(a,b,c){return b===!1?n.removeAttr(a,c):a.setAttribute(c,c),c}},n.each(n.expr.match.bool.source.match(/\w+/g),function(a,b){var c=$b[b]||n.find.attr;$b[b]=function(a,b,d){var e,f;return d||(f=$b[b],$b[b]=e,e=null!=c(a,b,d)?b.toLowerCase():null,$b[b]=f),e}});var _b=/^(?:input|select|textarea|button)$/i;n.fn.extend({prop:function(a,b){return J(this,n.prop,a,b,arguments.length>1)},removeProp:function(a){return this.each(function(){delete this[n.propFix[a]||a]})}}),n.extend({propFix:{"for":"htmlFor","class":"className"},prop:function(a,b,c){var d,e,f,g=a.nodeType;if(a&&3!==g&&8!==g&&2!==g)return f=1!==g||!n.isXMLDoc(a),f&&(b=n.propFix[b]||b,e=n.propHooks[b]),void 0!==c?e&&"set"in e&&void 0!==(d=e.set(a,c,b))?d:a[b]=c:e&&"get"in e&&null!==(d=e.get(a,b))?d:a[b]},propHooks:{tabIndex:{get:function(a){return a.hasAttribute("tabindex")||_b.test(a.nodeName)||a.href?a.tabIndex:-1}}}}),k.optSelected||(n.propHooks.selected={get:function(a){var b=a.parentNode;return b&&b.parentNode&&b.parentNode.selectedIndex,null}}),n.each(["tabIndex","readOnly","maxLength","cellSpacing","cellPadding","rowSpan","colSpan","useMap","frameBorder","contentEditable"],function(){n.propFix[this.toLowerCase()]=this});var ac=/[\t\r\n\f]/g;n.fn.extend({addClass:function(a){var b,c,d,e,f,g,h="string"==typeof a&&a,i=0,j=this.length;if(n.isFunction(a))return this.each(function(b){n(this).addClass(a.call(this,b,this.className))});if(h)for(b=(a||"").match(E)||[];j>i;i++)if(c=this[i],d=1===c.nodeType&&(c.className?(" "+c.className+" ").replace(ac," "):" ")){f=0;while(e=b[f++])d.indexOf(" "+e+" ")<0&&(d+=e+" ");g=n.trim(d),c.className!==g&&(c.className=g)}return this},removeClass:function(a){var b,c,d,e,f,g,h=0===arguments.length||"string"==typeof a&&a,i=0,j=this.length;if(n.isFunction(a))return this.each(function(b){n(this).removeClass(a.call(this,b,this.className))});if(h)for(b=(a||"").match(E)||[];j>i;i++)if(c=this[i],d=1===c.nodeType&&(c.className?(" "+c.className+" ").replace(ac," "):"")){f=0;while(e=b[f++])while(d.indexOf(" "+e+" ")>=0)d=d.replace(" "+e+" "," ");g=a?n.trim(d):"",c.className!==g&&(c.className=g)}return this},toggleClass:function(a,b){var c=typeof a;return"boolean"==typeof b&&"string"===c?b?this.addClass(a):this.removeClass(a):this.each(n.isFunction(a)?function(c){n(this).toggleClass(a.call(this,c,this.className,b),b)}:function(){if("string"===c){var b,d=0,e=n(this),f=a.match(E)||[];while(b=f[d++])e.hasClass(b)?e.removeClass(b):e.addClass(b)}else(c===U||"boolean"===c)&&(this.className&&L.set(this,"__className__",this.className),this.className=this.className||a===!1?"":L.get(this,"__className__")||"")})},hasClass:function(a){for(var b=" "+a+" ",c=0,d=this.length;d>c;c++)if(1===this[c].nodeType&&(" "+this[c].className+" ").replace(ac," ").indexOf(b)>=0)return!0;return!1}});var bc=/\r/g;n.fn.extend({val:function(a){var b,c,d,e=this[0];{if(arguments.length)return d=n.isFunction(a),this.each(function(c){var e;1===this.nodeType&&(e=d?a.call(this,c,n(this).val()):a,null==e?e="":"number"==typeof e?e+="":n.isArray(e)&&(e=n.map(e,function(a){return null==a?"":a+""})),b=n.valHooks[this.type]||n.valHooks[this.nodeName.toLowerCase()],b&&"set"in b&&void 0!==b.set(this,e,"value")||(this.value=e))});if(e)return b=n.valHooks[e.type]||n.valHooks[e.nodeName.toLowerCase()],b&&"get"in b&&void 0!==(c=b.get(e,"value"))?c:(c=e.value,"string"==typeof c?c.replace(bc,""):null==c?"":c)}}}),n.extend({valHooks:{option:{get:function(a){var b=n.find.attr(a,"value");return null!=b?b:n.trim(n.text(a))}},select:{get:function(a){for(var b,c,d=a.options,e=a.selectedIndex,f="select-one"===a.type||0>e,g=f?null:[],h=f?e+1:d.length,i=0>e?h:f?e:0;h>i;i++)if(c=d[i],!(!c.selected&&i!==e||(k.optDisabled?c.disabled:null!==c.getAttribute("disabled"))||c.parentNode.disabled&&n.nodeName(c.parentNode,"optgroup"))){if(b=n(c).val(),f)return b;g.push(b)}return g},set:function(a,b){var c,d,e=a.options,f=n.makeArray(b),g=e.length;while(g--)d=e[g],(d.selected=n.inArray(d.value,f)>=0)&&(c=!0);return c||(a.selectedIndex=-1),f}}}}),n.each(["radio","checkbox"],function(){n.valHooks[this]={set:function(a,b){return n.isArray(b)?a.checked=n.inArray(n(a).val(),b)>=0:void 0}},k.checkOn||(n.valHooks[this].get=function(a){return null===a.getAttribute("value")?"on":a.value})}),n.each("blur focus focusin focusout load resize scroll unload click dblclick mousedown mouseup mousemove mouseover mouseout mouseenter mouseleave change select submit keydown keypress keyup error contextmenu".split(" "),function(a,b){n.fn[b]=function(a,c){return arguments.length>0?this.on(b,null,a,c):this.trigger(b)}}),n.fn.extend({hover:function(a,b){return this.mouseenter(a).mouseleave(b||a)},bind:function(a,b,c){return this.on(a,null,b,c)},unbind:function(a,b){return this.off(a,null,b)},delegate:function(a,b,c,d){return this.on(b,a,c,d)},undelegate:function(a,b,c){return 1===arguments.length?this.off(a,"**"):this.off(b,a||"**",c)}});var cc=n.now(),dc=/\?/;n.parseJSON=function(a){return JSON.parse(a+"")},n.parseXML=function(a){var b,c;if(!a||"string"!=typeof a)return null;try{c=new DOMParser,b=c.parseFromString(a,"text/xml")}catch(d){b=void 0}return(!b||b.getElementsByTagName("parsererror").length)&&n.error("Invalid XML: "+a),b};var ec,fc,gc=/#.*$/,hc=/([?&])_=[^&]*/,ic=/^(.*?):[ \t]*([^\r\n]*)$/gm,jc=/^(?:about|app|app-storage|.+-extension|file|res|widget):$/,kc=/^(?:GET|HEAD)$/,lc=/^\/\//,mc=/^([\w.+-]+:)(?:\/\/(?:[^\/?#]*@|)([^\/?#:]*)(?::(\d+)|)|)/,nc={},oc={},pc="*/".concat("*");try{fc=location.href}catch(qc){fc=l.createElement("a"),fc.href="",fc=fc.href}ec=mc.exec(fc.toLowerCase())||[];function rc(a){return function(b,c){"string"!=typeof b&&(c=b,b="*");var d,e=0,f=b.toLowerCase().match(E)||[];if(n.isFunction(c))while(d=f[e++])"+"===d[0]?(d=d.slice(1)||"*",(a[d]=a[d]||[]).unshift(c)):(a[d]=a[d]||[]).push(c)}}function sc(a,b,c,d){var e={},f=a===oc;function g(h){var i;return e[h]=!0,n.each(a[h]||[],function(a,h){var j=h(b,c,d);return"string"!=typeof j||f||e[j]?f?!(i=j):void 0:(b.dataTypes.unshift(j),g(j),!1)}),i}return g(b.dataTypes[0])||!e["*"]&&g("*")}function tc(a,b){var c,d,e=n.ajaxSettings.flatOptions||{};for(c in b)void 0!==b[c]&&((e[c]?a:d||(d={}))[c]=b[c]);return d&&n.extend(!0,a,d),a}function uc(a,b,c){var d,e,f,g,h=a.contents,i=a.dataTypes;while("*"===i[0])i.shift(),void 0===d&&(d=a.mimeType||b.getResponseHeader("Content-Type"));if(d)for(e in h)if(h[e]&&h[e].test(d)){i.unshift(e);break}if(i[0]in c)f=i[0];else{for(e in c){if(!i[0]||a.converters[e+" "+i[0]]){f=e;break}g||(g=e)}f=f||g}return f?(f!==i[0]&&i.unshift(f),c[f]):void 0}function vc(a,b,c,d){var e,f,g,h,i,j={},k=a.dataTypes.slice();if(k[1])for(g in a.converters)j[g.toLowerCase()]=a.converters[g];f=k.shift();while(f)if(a.responseFields[f]&&(c[a.responseFields[f]]=b),!i&&d&&a.dataFilter&&(b=a.dataFilter(b,a.dataType)),i=f,f=k.shift())if("*"===f)f=i;else if("*"!==i&&i!==f){if(g=j[i+" "+f]||j["* "+f],!g)for(e in j)if(h=e.split(" "),h[1]===f&&(g=j[i+" "+h[0]]||j["* "+h[0]])){g===!0?g=j[e]:j[e]!==!0&&(f=h[0],k.unshift(h[1]));break}if(g!==!0)if(g&&a["throws"])b=g(b);else try{b=g(b)}catch(l){return{state:"parsererror",error:g?l:"No conversion from "+i+" to "+f}}}return{state:"success",data:b}}n.extend({active:0,lastModified:{},etag:{},ajaxSettings:{url:fc,type:"GET",isLocal:jc.test(ec[1]),global:!0,processData:!0,async:!0,contentType:"application/x-www-form-urlencoded; charset=UTF-8",accepts:{"*":pc,text:"text/plain",html:"text/html",xml:"application/xml, text/xml",json:"application/json, text/javascript"},contents:{xml:/xml/,html:/html/,json:/json/},responseFields:{xml:"responseXML",text:"responseText",json:"responseJSON"},converters:{"* text":String,"text html":!0,"text json":n.parseJSON,"text xml":n.parseXML},flatOptions:{url:!0,context:!0}},ajaxSetup:function(a,b){return b?tc(tc(a,n.ajaxSettings),b):tc(n.ajaxSettings,a)},ajaxPrefilter:rc(nc),ajaxTransport:rc(oc),ajax:function(a,b){"object"==typeof a&&(b=a,a=void 0),b=b||{};var c,d,e,f,g,h,i,j,k=n.ajaxSetup({},b),l=k.context||k,m=k.context&&(l.nodeType||l.jquery)?n(l):n.event,o=n.Deferred(),p=n.Callbacks("once memory"),q=k.statusCode||{},r={},s={},t=0,u="canceled",v={readyState:0,getResponseHeader:function(a){var b;if(2===t){if(!f){f={};while(b=ic.exec(e))f[b[1].toLowerCase()]=b[2]}b=f[a.toLowerCase()]}return null==b?null:b},getAllResponseHeaders:function(){return 2===t?e:null},setRequestHeader:function(a,b){var c=a.toLowerCase();return t||(a=s[c]=s[c]||a,r[a]=b),this},overrideMimeType:function(a){return t||(k.mimeType=a),this},statusCode:function(a){var b;if(a)if(2>t)for(b in a)q[b]=[q[b],a[b]];else v.always(a[v.status]);return this},abort:function(a){var b=a||u;return c&&c.abort(b),x(0,b),this}};if(o.promise(v).complete=p.add,v.success=v.done,v.error=v.fail,k.url=((a||k.url||fc)+"").replace(gc,"").replace(lc,ec[1]+"//"),k.type=b.method||b.type||k.method||k.type,k.dataTypes=n.trim(k.dataType||"*").toLowerCase().match(E)||[""],null==k.crossDomain&&(h=mc.exec(k.url.toLowerCase()),k.crossDomain=!(!h||h[1]===ec[1]&&h[2]===ec[2]&&(h[3]||("http:"===h[1]?"80":"443"))===(ec[3]||("http:"===ec[1]?"80":"443")))),k.data&&k.processData&&"string"!=typeof k.data&&(k.data=n.param(k.data,k.traditional)),sc(nc,k,b,v),2===t)return v;i=k.global,i&&0===n.active++&&n.event.trigger("ajaxStart"),k.type=k.type.toUpperCase(),k.hasContent=!kc.test(k.type),d=k.url,k.hasContent||(k.data&&(d=k.url+=(dc.test(d)?"&":"?")+k.data,delete k.data),k.cache===!1&&(k.url=hc.test(d)?d.replace(hc,"$1_="+cc++):d+(dc.test(d)?"&":"?")+"_="+cc++)),k.ifModified&&(n.lastModified[d]&&v.setRequestHeader("If-Modified-Since",n.lastModified[d]),n.etag[d]&&v.setRequestHeader("If-None-Match",n.etag[d])),(k.data&&k.hasContent&&k.contentType!==!1||b.contentType)&&v.setRequestHeader("Content-Type",k.contentType),v.setRequestHeader("Accept",k.dataTypes[0]&&k.accepts[k.dataTypes[0]]?k.accepts[k.dataTypes[0]]+("*"!==k.dataTypes[0]?", "+pc+"; q=0.01":""):k.accepts["*"]);for(j in k.headers)v.setRequestHeader(j,k.headers[j]);if(k.beforeSend&&(k.beforeSend.call(l,v,k)===!1||2===t))return v.abort();u="abort";for(j in{success:1,error:1,complete:1})v[j](k[j]);if(c=sc(oc,k,b,v)){v.readyState=1,i&&m.trigger("ajaxSend",[v,k]),k.async&&k.timeout>0&&(g=setTimeout(function(){v.abort("timeout")},k.timeout));try{t=1,c.send(r,x)}catch(w){if(!(2>t))throw w;x(-1,w)}}else x(-1,"No Transport");function x(a,b,f,h){var j,r,s,u,w,x=b;2!==t&&(t=2,g&&clearTimeout(g),c=void 0,e=h||"",v.readyState=a>0?4:0,j=a>=200&&300>a||304===a,f&&(u=uc(k,v,f)),u=vc(k,u,v,j),j?(k.ifModified&&(w=v.getResponseHeader("Last-Modified"),w&&(n.lastModified[d]=w),w=v.getResponseHeader("etag"),w&&(n.etag[d]=w)),204===a||"HEAD"===k.type?x="nocontent":304===a?x="notmodified":(x=u.state,r=u.data,s=u.error,j=!s)):(s=x,(a||!x)&&(x="error",0>a&&(a=0))),v.status=a,v.statusText=(b||x)+"",j?o.resolveWith(l,[r,x,v]):o.rejectWith(l,[v,x,s]),v.statusCode(q),q=void 0,i&&m.trigger(j?"ajaxSuccess":"ajaxError",[v,k,j?r:s]),p.fireWith(l,[v,x]),i&&(m.trigger("ajaxComplete",[v,k]),--n.active||n.event.trigger("ajaxStop")))}return v},getJSON:function(a,b,c){return n.get(a,b,c,"json")},getScript:function(a,b){return n.get(a,void 0,b,"script")}}),n.each(["get","post"],function(a,b){n[b]=function(a,c,d,e){return n.isFunction(c)&&(e=e||d,d=c,c=void 0),n.ajax({url:a,type:b,dataType:e,data:c,success:d})}}),n.each(["ajaxStart","ajaxStop","ajaxComplete","ajaxError","ajaxSuccess","ajaxSend"],function(a,b){n.fn[b]=function(a){return this.on(b,a)}}),n._evalUrl=function(a){return n.ajax({url:a,type:"GET",dataType:"script",async:!1,global:!1,"throws":!0})},n.fn.extend({wrapAll:function(a){var b;return n.isFunction(a)?this.each(function(b){n(this).wrapAll(a.call(this,b))}):(this[0]&&(b=n(a,this[0].ownerDocument).eq(0).clone(!0),this[0].parentNode&&b.insertBefore(this[0]),b.map(function(){var a=this;while(a.firstElementChild)a=a.firstElementChild;return a}).append(this)),this)},wrapInner:function(a){return this.each(n.isFunction(a)?function(b){n(this).wrapInner(a.call(this,b))}:function(){var b=n(this),c=b.contents();c.length?c.wrapAll(a):b.append(a)})},wrap:function(a){var b=n.isFunction(a);return this.each(function(c){n(this).wrapAll(b?a.call(this,c):a)})},unwrap:function(){return this.parent().each(function(){n.nodeName(this,"body")||n(this).replaceWith(this.childNodes)}).end()}}),n.expr.filters.hidden=function(a){return a.offsetWidth<=0&&a.offsetHeight<=0},n.expr.filters.visible=function(a){return!n.expr.filters.hidden(a)};var wc=/%20/g,xc=/\[\]$/,yc=/\r?\n/g,zc=/^(?:submit|button|image|reset|file)$/i,Ac=/^(?:input|select|textarea|keygen)/i;function Bc(a,b,c,d){var e;if(n.isArray(b))n.each(b,function(b,e){c||xc.test(a)?d(a,e):Bc(a+"["+("object"==typeof e?b:"")+"]",e,c,d)});else if(c||"object"!==n.type(b))d(a,b);else for(e in b)Bc(a+"["+e+"]",b[e],c,d)}n.param=function(a,b){var c,d=[],e=function(a,b){b=n.isFunction(b)?b():null==b?"":b,d[d.length]=encodeURIComponent(a)+"="+encodeURIComponent(b)};if(void 0===b&&(b=n.ajaxSettings&&n.ajaxSettings.traditional),n.isArray(a)||a.jquery&&!n.isPlainObject(a))n.each(a,function(){e(this.name,this.value)});else for(c in a)Bc(c,a[c],b,e);return d.join("&").replace(wc,"+")},n.fn.extend({serialize:function(){return n.param(this.serializeArray())},serializeArray:function(){return this.map(function(){var a=n.prop(this,"elements");return a?n.makeArray(a):this}).filter(function(){var a=this.type;return this.name&&!n(this).is(":disabled")&&Ac.test(this.nodeName)&&!zc.test(a)&&(this.checked||!T.test(a))}).map(function(a,b){var c=n(this).val();return null==c?null:n.isArray(c)?n.map(c,function(a){return{name:b.name,value:a.replace(yc,"\r\n")}}):{name:b.name,value:c.replace(yc,"\r\n")}}).get()}}),n.ajaxSettings.xhr=function(){try{return new XMLHttpRequest}catch(a){}};var Cc=0,Dc={},Ec={0:200,1223:204},Fc=n.ajaxSettings.xhr();a.ActiveXObject&&n(a).on("unload",function(){for(var a in Dc)Dc[a]()}),k.cors=!!Fc&&"withCredentials"in Fc,k.ajax=Fc=!!Fc,n.ajaxTransport(function(a){var b;return k.cors||Fc&&!a.crossDomain?{send:function(c,d){var e,f=a.xhr(),g=++Cc;if(f.open(a.type,a.url,a.async,a.username,a.password),a.xhrFields)for(e in a.xhrFields)f[e]=a.xhrFields[e];a.mimeType&&f.overrideMimeType&&f.overrideMimeType(a.mimeType),a.crossDomain||c["X-Requested-With"]||(c["X-Requested-With"]="XMLHttpRequest");for(e in c)f.setRequestHeader(e,c[e]);b=function(a){return function(){b&&(delete Dc[g],b=f.onload=f.onerror=null,"abort"===a?f.abort():"error"===a?d(f.status,f.statusText):d(Ec[f.status]||f.status,f.statusText,"string"==typeof f.responseText?{text:f.responseText}:void 0,f.getAllResponseHeaders()))}},f.onload=b(),f.onerror=b("error"),b=Dc[g]=b("abort");try{f.send(a.hasContent&&a.data||null)}catch(h){if(b)throw h}},abort:function(){b&&b()}}:void 0}),n.ajaxSetup({accepts:{script:"text/javascript, application/javascript, application/ecmascript, application/x-ecmascript"},contents:{script:/(?:java|ecma)script/},converters:{"text script":function(a){return n.globalEval(a),a}}}),n.ajaxPrefilter("script",function(a){void 0===a.cache&&(a.cache=!1),a.crossDomain&&(a.type="GET")}),n.ajaxTransport("script",function(a){if(a.crossDomain){var b,c;return{send:function(d,e){b=n("<script>").prop({async:!0,charset:a.scriptCharset,src:a.url}).on("load error",c=function(a){b.remove(),c=null,a&&e("error"===a.type?404:200,a.type)}),l.head.appendChild(b[0])},abort:function(){c&&c()}}}});var Gc=[],Hc=/(=)\?(?=&|$)|\?\?/;n.ajaxSetup({jsonp:"callback",jsonpCallback:function(){var a=Gc.pop()||n.expando+"_"+cc++;return this[a]=!0,a}}),n.ajaxPrefilter("json jsonp",function(b,c,d){var e,f,g,h=b.jsonp!==!1&&(Hc.test(b.url)?"url":"string"==typeof b.data&&!(b.contentType||"").indexOf("application/x-www-form-urlencoded")&&Hc.test(b.data)&&"data");return h||"jsonp"===b.dataTypes[0]?(e=b.jsonpCallback=n.isFunction(b.jsonpCallback)?b.jsonpCallback():b.jsonpCallback,h?b[h]=b[h].replace(Hc,"$1"+e):b.jsonp!==!1&&(b.url+=(dc.test(b.url)?"&":"?")+b.jsonp+"="+e),b.converters["script json"]=function(){return g||n.error(e+" was not called"),g[0]},b.dataTypes[0]="json",f=a[e],a[e]=function(){g=arguments},d.always(function(){a[e]=f,b[e]&&(b.jsonpCallback=c.jsonpCallback,Gc.push(e)),g&&n.isFunction(f)&&f(g[0]),g=f=void 0}),"script"):void 0}),n.parseHTML=function(a,b,c){if(!a||"string"!=typeof a)return null;"boolean"==typeof b&&(c=b,b=!1),b=b||l;var d=v.exec(a),e=!c&&[];return d?[b.createElement(d[1])]:(d=n.buildFragment([a],b,e),e&&e.length&&n(e).remove(),n.merge([],d.childNodes))};var Ic=n.fn.load;n.fn.load=function(a,b,c){if("string"!=typeof a&&Ic)return Ic.apply(this,arguments);var d,e,f,g=this,h=a.indexOf(" ");return h>=0&&(d=n.trim(a.slice(h)),a=a.slice(0,h)),n.isFunction(b)?(c=b,b=void 0):b&&"object"==typeof b&&(e="POST"),g.length>0&&n.ajax({url:a,type:e,dataType:"html",data:b}).done(function(a){f=arguments,g.html(d?n("<div>").append(n.parseHTML(a)).find(d):a)}).complete(c&&function(a,b){g.each(c,f||[a.responseText,b,a])}),this},n.expr.filters.animated=function(a){return n.grep(n.timers,function(b){return a===b.elem}).length};var Jc=a.document.documentElement;function Kc(a){return n.isWindow(a)?a:9===a.nodeType&&a.defaultView}n.offset={setOffset:function(a,b,c){var d,e,f,g,h,i,j,k=n.css(a,"position"),l=n(a),m={};"static"===k&&(a.style.position="relative"),h=l.offset(),f=n.css(a,"top"),i=n.css(a,"left"),j=("absolute"===k||"fixed"===k)&&(f+i).indexOf("auto")>-1,j?(d=l.position(),g=d.top,e=d.left):(g=parseFloat(f)||0,e=parseFloat(i)||0),n.isFunction(b)&&(b=b.call(a,c,h)),null!=b.top&&(m.top=b.top-h.top+g),null!=b.left&&(m.left=b.left-h.left+e),"using"in b?b.using.call(a,m):l.css(m)}},n.fn.extend({offset:function(a){if(arguments.length)return void 0===a?this:this.each(function(b){n.offset.setOffset(this,a,b)});var b,c,d=this[0],e={top:0,left:0},f=d&&d.ownerDocument;if(f)return b=f.documentElement,n.contains(b,d)?(typeof d.getBoundingClientRect!==U&&(e=d.getBoundingClientRect()),c=Kc(f),{top:e.top+c.pageYOffset-b.clientTop,left:e.left+c.pageXOffset-b.clientLeft}):e},position:function(){if(this[0]){var a,b,c=this[0],d={top:0,left:0};return"fixed"===n.css(c,"position")?b=c.getBoundingClientRect():(a=this.offsetParent(),b=this.offset(),n.nodeName(a[0],"html")||(d=a.offset()),d.top+=n.css(a[0],"borderTopWidth",!0),d.left+=n.css(a[0],"borderLeftWidth",!0)),{top:b.top-d.top-n.css(c,"marginTop",!0),left:b.left-d.left-n.css(c,"marginLeft",!0)}}},offsetParent:function(){return this.map(function(){var a=this.offsetParent||Jc;while(a&&!n.nodeName(a,"html")&&"static"===n.css(a,"position"))a=a.offsetParent;return a||Jc})}}),n.each({scrollLeft:"pageXOffset",scrollTop:"pageYOffset"},function(b,c){var d="pageYOffset"===c;n.fn[b]=function(e){return J(this,function(b,e,f){var g=Kc(b);return void 0===f?g?g[c]:b[e]:void(g?g.scrollTo(d?a.pageXOffset:f,d?f:a.pageYOffset):b[e]=f)},b,e,arguments.length,null)}}),n.each(["top","left"],function(a,b){n.cssHooks[b]=yb(k.pixelPosition,function(a,c){return c?(c=xb(a,b),vb.test(c)?n(a).position()[b]+"px":c):void 0})}),n.each({Height:"height",Width:"width"},function(a,b){n.each({padding:"inner"+a,content:b,"":"outer"+a},function(c,d){n.fn[d]=function(d,e){var f=arguments.length&&(c||"boolean"!=typeof d),g=c||(d===!0||e===!0?"margin":"border");return J(this,function(b,c,d){var e;return n.isWindow(b)?b.document.documentElement["client"+a]:9===b.nodeType?(e=b.documentElement,Math.max(b.body["scroll"+a],e["scroll"+a],b.body["offset"+a],e["offset"+a],e["client"+a])):void 0===d?n.css(b,c,g):n.style(b,c,d,g)},b,f?d:void 0,f,null)}})}),n.fn.size=function(){return this.length},n.fn.andSelf=n.fn.addBack,"function"==typeof define&&define.amd&&define("jquery",[],function(){return n});var Lc=a.jQuery,Mc=a.$;return n.noConflict=function(b){return a.$===n&&(a.$=Mc),b&&a.jQuery===n&&(a.jQuery=Lc),n},typeof b===U&&(a.jQuery=a.$=n),n});

//     Underscore.js 1.4.3
//     http://underscorejs.org
//     (c) 2009-2012 Jeremy Ashkenas, DocumentCloud Inc.
//     Underscore may be freely distributed under the MIT license.
(function(){var n=this,t=n._,r={},e=Array.prototype,u=Object.prototype,i=Function.prototype,a=e.push,o=e.slice,c=e.concat,l=u.toString,f=u.hasOwnProperty,s=e.forEach,p=e.map,v=e.reduce,h=e.reduceRight,g=e.filter,d=e.every,m=e.some,y=e.indexOf,b=e.lastIndexOf,x=Array.isArray,_=Object.keys,j=i.bind,w=function(n){return n instanceof w?n:this instanceof w?(this._wrapped=n,void 0):new w(n)};"undefined"!=typeof exports?("undefined"!=typeof module&&module.exports&&(exports=module.exports=w),exports._=w):n._=w,w.VERSION="1.4.3";var A=w.each=w.forEach=function(n,t,e){if(null!=n)if(s&&n.forEach===s)n.forEach(t,e);else if(n.length===+n.length){for(var u=0,i=n.length;i>u;u++)if(t.call(e,n[u],u,n)===r)return}else for(var a in n)if(w.has(n,a)&&t.call(e,n[a],a,n)===r)return};w.map=w.collect=function(n,t,r){var e=[];return null==n?e:p&&n.map===p?n.map(t,r):(A(n,function(n,u,i){e[e.length]=t.call(r,n,u,i)}),e)};var O="Reduce of empty array with no initial value";w.reduce=w.foldl=w.inject=function(n,t,r,e){var u=arguments.length>2;if(null==n&&(n=[]),v&&n.reduce===v)return e&&(t=w.bind(t,e)),u?n.reduce(t,r):n.reduce(t);if(A(n,function(n,i,a){u?r=t.call(e,r,n,i,a):(r=n,u=!0)}),!u)throw new TypeError(O);return r},w.reduceRight=w.foldr=function(n,t,r,e){var u=arguments.length>2;if(null==n&&(n=[]),h&&n.reduceRight===h)return e&&(t=w.bind(t,e)),u?n.reduceRight(t,r):n.reduceRight(t);var i=n.length;if(i!==+i){var a=w.keys(n);i=a.length}if(A(n,function(o,c,l){c=a?a[--i]:--i,u?r=t.call(e,r,n[c],c,l):(r=n[c],u=!0)}),!u)throw new TypeError(O);return r},w.find=w.detect=function(n,t,r){var e;return E(n,function(n,u,i){return t.call(r,n,u,i)?(e=n,!0):void 0}),e},w.filter=w.select=function(n,t,r){var e=[];return null==n?e:g&&n.filter===g?n.filter(t,r):(A(n,function(n,u,i){t.call(r,n,u,i)&&(e[e.length]=n)}),e)},w.reject=function(n,t,r){return w.filter(n,function(n,e,u){return!t.call(r,n,e,u)},r)},w.every=w.all=function(n,t,e){t||(t=w.identity);var u=!0;return null==n?u:d&&n.every===d?n.every(t,e):(A(n,function(n,i,a){return(u=u&&t.call(e,n,i,a))?void 0:r}),!!u)};var E=w.some=w.any=function(n,t,e){t||(t=w.identity);var u=!1;return null==n?u:m&&n.some===m?n.some(t,e):(A(n,function(n,i,a){return u||(u=t.call(e,n,i,a))?r:void 0}),!!u)};w.contains=w.include=function(n,t){return null==n?!1:y&&n.indexOf===y?n.indexOf(t)!=-1:E(n,function(n){return n===t})},w.invoke=function(n,t){var r=o.call(arguments,2);return w.map(n,function(n){return(w.isFunction(t)?t:n[t]).apply(n,r)})},w.pluck=function(n,t){return w.map(n,function(n){return n[t]})},w.where=function(n,t){return w.isEmpty(t)?[]:w.filter(n,function(n){for(var r in t)if(t[r]!==n[r])return!1;return!0})},w.max=function(n,t,r){if(!t&&w.isArray(n)&&n[0]===+n[0]&&65535>n.length)return Math.max.apply(Math,n);if(!t&&w.isEmpty(n))return-1/0;var e={computed:-1/0,value:-1/0};return A(n,function(n,u,i){var a=t?t.call(r,n,u,i):n;a>=e.computed&&(e={value:n,computed:a})}),e.value},w.min=function(n,t,r){if(!t&&w.isArray(n)&&n[0]===+n[0]&&65535>n.length)return Math.min.apply(Math,n);if(!t&&w.isEmpty(n))return 1/0;var e={computed:1/0,value:1/0};return A(n,function(n,u,i){var a=t?t.call(r,n,u,i):n;e.computed>a&&(e={value:n,computed:a})}),e.value},w.shuffle=function(n){var t,r=0,e=[];return A(n,function(n){t=w.random(r++),e[r-1]=e[t],e[t]=n}),e};var F=function(n){return w.isFunction(n)?n:function(t){return t[n]}};w.sortBy=function(n,t,r){var e=F(t);return w.pluck(w.map(n,function(n,t,u){return{value:n,index:t,criteria:e.call(r,n,t,u)}}).sort(function(n,t){var r=n.criteria,e=t.criteria;if(r!==e){if(r>e||r===void 0)return 1;if(e>r||e===void 0)return-1}return n.index<t.index?-1:1}),"value")};var k=function(n,t,r,e){var u={},i=F(t||w.identity);return A(n,function(t,a){var o=i.call(r,t,a,n);e(u,o,t)}),u};w.groupBy=function(n,t,r){return k(n,t,r,function(n,t,r){(w.has(n,t)?n[t]:n[t]=[]).push(r)})},w.countBy=function(n,t,r){return k(n,t,r,function(n,t){w.has(n,t)||(n[t]=0),n[t]++})},w.sortedIndex=function(n,t,r,e){r=null==r?w.identity:F(r);for(var u=r.call(e,t),i=0,a=n.length;a>i;){var o=i+a>>>1;u>r.call(e,n[o])?i=o+1:a=o}return i},w.toArray=function(n){return n?w.isArray(n)?o.call(n):n.length===+n.length?w.map(n,w.identity):w.values(n):[]},w.size=function(n){return null==n?0:n.length===+n.length?n.length:w.keys(n).length},w.first=w.head=w.take=function(n,t,r){return null==n?void 0:null==t||r?n[0]:o.call(n,0,t)},w.initial=function(n,t,r){return o.call(n,0,n.length-(null==t||r?1:t))},w.last=function(n,t,r){return null==n?void 0:null==t||r?n[n.length-1]:o.call(n,Math.max(n.length-t,0))},w.rest=w.tail=w.drop=function(n,t,r){return o.call(n,null==t||r?1:t)},w.compact=function(n){return w.filter(n,w.identity)};var R=function(n,t,r){return A(n,function(n){w.isArray(n)?t?a.apply(r,n):R(n,t,r):r.push(n)}),r};w.flatten=function(n,t){return R(n,t,[])},w.without=function(n){return w.difference(n,o.call(arguments,1))},w.uniq=w.unique=function(n,t,r,e){w.isFunction(t)&&(e=r,r=t,t=!1);var u=r?w.map(n,r,e):n,i=[],a=[];return A(u,function(r,e){(t?e&&a[a.length-1]===r:w.contains(a,r))||(a.push(r),i.push(n[e]))}),i},w.union=function(){return w.uniq(c.apply(e,arguments))},w.intersection=function(n){var t=o.call(arguments,1);return w.filter(w.uniq(n),function(n){return w.every(t,function(t){return w.indexOf(t,n)>=0})})},w.difference=function(n){var t=c.apply(e,o.call(arguments,1));return w.filter(n,function(n){return!w.contains(t,n)})},w.zip=function(){for(var n=o.call(arguments),t=w.max(w.pluck(n,"length")),r=Array(t),e=0;t>e;e++)r[e]=w.pluck(n,""+e);return r},w.object=function(n,t){if(null==n)return{};for(var r={},e=0,u=n.length;u>e;e++)t?r[n[e]]=t[e]:r[n[e][0]]=n[e][1];return r},w.indexOf=function(n,t,r){if(null==n)return-1;var e=0,u=n.length;if(r){if("number"!=typeof r)return e=w.sortedIndex(n,t),n[e]===t?e:-1;e=0>r?Math.max(0,u+r):r}if(y&&n.indexOf===y)return n.indexOf(t,r);for(;u>e;e++)if(n[e]===t)return e;return-1},w.lastIndexOf=function(n,t,r){if(null==n)return-1;var e=null!=r;if(b&&n.lastIndexOf===b)return e?n.lastIndexOf(t,r):n.lastIndexOf(t);for(var u=e?r:n.length;u--;)if(n[u]===t)return u;return-1},w.range=function(n,t,r){1>=arguments.length&&(t=n||0,n=0),r=arguments[2]||1;for(var e=Math.max(Math.ceil((t-n)/r),0),u=0,i=Array(e);e>u;)i[u++]=n,n+=r;return i};var I=function(){};w.bind=function(n,t){var r,e;if(n.bind===j&&j)return j.apply(n,o.call(arguments,1));if(!w.isFunction(n))throw new TypeError;return r=o.call(arguments,2),e=function(){if(!(this instanceof e))return n.apply(t,r.concat(o.call(arguments)));I.prototype=n.prototype;var u=new I;I.prototype=null;var i=n.apply(u,r.concat(o.call(arguments)));return Object(i)===i?i:u}},w.bindAll=function(n){var t=o.call(arguments,1);return 0===t.length&&(t=w.functions(n)),A(t,function(t){n[t]=w.bind(n[t],n)}),n},w.memoize=function(n,t){var r={};return t||(t=w.identity),function(){var e=t.apply(this,arguments);return w.has(r,e)?r[e]:r[e]=n.apply(this,arguments)}},w.delay=function(n,t){var r=o.call(arguments,2);return setTimeout(function(){return n.apply(null,r)},t)},w.defer=function(n){return w.delay.apply(w,[n,1].concat(o.call(arguments,1)))},w.throttle=function(n,t){var r,e,u,i,a=0,o=function(){a=new Date,u=null,i=n.apply(r,e)};return function(){var c=new Date,l=t-(c-a);return r=this,e=arguments,0>=l?(clearTimeout(u),u=null,a=c,i=n.apply(r,e)):u||(u=setTimeout(o,l)),i}},w.debounce=function(n,t,r){var e,u;return function(){var i=this,a=arguments,o=function(){e=null,r||(u=n.apply(i,a))},c=r&&!e;return clearTimeout(e),e=setTimeout(o,t),c&&(u=n.apply(i,a)),u}},w.once=function(n){var t,r=!1;return function(){return r?t:(r=!0,t=n.apply(this,arguments),n=null,t)}},w.wrap=function(n,t){return function(){var r=[n];return a.apply(r,arguments),t.apply(this,r)}},w.compose=function(){var n=arguments;return function(){for(var t=arguments,r=n.length-1;r>=0;r--)t=[n[r].apply(this,t)];return t[0]}},w.after=function(n,t){return 0>=n?t():function(){return 1>--n?t.apply(this,arguments):void 0}},w.keys=_||function(n){if(n!==Object(n))throw new TypeError("Invalid object");var t=[];for(var r in n)w.has(n,r)&&(t[t.length]=r);return t},w.values=function(n){var t=[];for(var r in n)w.has(n,r)&&t.push(n[r]);return t},w.pairs=function(n){var t=[];for(var r in n)w.has(n,r)&&t.push([r,n[r]]);return t},w.invert=function(n){var t={};for(var r in n)w.has(n,r)&&(t[n[r]]=r);return t},w.functions=w.methods=function(n){var t=[];for(var r in n)w.isFunction(n[r])&&t.push(r);return t.sort()},w.extend=function(n){return A(o.call(arguments,1),function(t){if(t)for(var r in t)n[r]=t[r]}),n},w.pick=function(n){var t={},r=c.apply(e,o.call(arguments,1));return A(r,function(r){r in n&&(t[r]=n[r])}),t},w.omit=function(n){var t={},r=c.apply(e,o.call(arguments,1));for(var u in n)w.contains(r,u)||(t[u]=n[u]);return t},w.defaults=function(n){return A(o.call(arguments,1),function(t){if(t)for(var r in t)null==n[r]&&(n[r]=t[r])}),n},w.clone=function(n){return w.isObject(n)?w.isArray(n)?n.slice():w.extend({},n):n},w.tap=function(n,t){return t(n),n};var S=function(n,t,r,e){if(n===t)return 0!==n||1/n==1/t;if(null==n||null==t)return n===t;n instanceof w&&(n=n._wrapped),t instanceof w&&(t=t._wrapped);var u=l.call(n);if(u!=l.call(t))return!1;switch(u){case"[object String]":return n==t+"";case"[object Number]":return n!=+n?t!=+t:0==n?1/n==1/t:n==+t;case"[object Date]":case"[object Boolean]":return+n==+t;case"[object RegExp]":return n.source==t.source&&n.global==t.global&&n.multiline==t.multiline&&n.ignoreCase==t.ignoreCase}if("object"!=typeof n||"object"!=typeof t)return!1;for(var i=r.length;i--;)if(r[i]==n)return e[i]==t;r.push(n),e.push(t);var a=0,o=!0;if("[object Array]"==u){if(a=n.length,o=a==t.length)for(;a--&&(o=S(n[a],t[a],r,e)););}else{var c=n.constructor,f=t.constructor;if(c!==f&&!(w.isFunction(c)&&c instanceof c&&w.isFunction(f)&&f instanceof f))return!1;for(var s in n)if(w.has(n,s)&&(a++,!(o=w.has(t,s)&&S(n[s],t[s],r,e))))break;if(o){for(s in t)if(w.has(t,s)&&!a--)break;o=!a}}return r.pop(),e.pop(),o};w.isEqual=function(n,t){return S(n,t,[],[])},w.isEmpty=function(n){if(null==n)return!0;if(w.isArray(n)||w.isString(n))return 0===n.length;for(var t in n)if(w.has(n,t))return!1;return!0},w.isElement=function(n){return!(!n||1!==n.nodeType)},w.isArray=x||function(n){return"[object Array]"==l.call(n)},w.isObject=function(n){return n===Object(n)},A(["Arguments","Function","String","Number","Date","RegExp"],function(n){w["is"+n]=function(t){return l.call(t)=="[object "+n+"]"}}),w.isArguments(arguments)||(w.isArguments=function(n){return!(!n||!w.has(n,"callee"))}),"function"!=typeof/./&&(w.isFunction=function(n){return"function"==typeof n}),w.isFinite=function(n){return isFinite(n)&&!isNaN(parseFloat(n))},w.isNaN=function(n){return w.isNumber(n)&&n!=+n},w.isBoolean=function(n){return n===!0||n===!1||"[object Boolean]"==l.call(n)},w.isNull=function(n){return null===n},w.isUndefined=function(n){return n===void 0},w.has=function(n,t){return f.call(n,t)},w.noConflict=function(){return n._=t,this},w.identity=function(n){return n},w.times=function(n,t,r){for(var e=Array(n),u=0;n>u;u++)e[u]=t.call(r,u);return e},w.random=function(n,t){return null==t&&(t=n,n=0),n+(0|Math.random()*(t-n+1))};var T={escape:{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#x27;","/":"&#x2F;"}};T.unescape=w.invert(T.escape);var M={escape:RegExp("["+w.keys(T.escape).join("")+"]","g"),unescape:RegExp("("+w.keys(T.unescape).join("|")+")","g")};w.each(["escape","unescape"],function(n){w[n]=function(t){return null==t?"":(""+t).replace(M[n],function(t){return T[n][t]})}}),w.result=function(n,t){if(null==n)return null;var r=n[t];return w.isFunction(r)?r.call(n):r},w.mixin=function(n){A(w.functions(n),function(t){var r=w[t]=n[t];w.prototype[t]=function(){var n=[this._wrapped];return a.apply(n,arguments),z.call(this,r.apply(w,n))}})};var N=0;w.uniqueId=function(n){var t=++N+"";return n?n+t:t},w.templateSettings={evaluate:/<%([\s\S]+?)%>/g,interpolate:/<%=([\s\S]+?)%>/g,escape:/<%-([\s\S]+?)%>/g};var q=/(.)^/,B={"'":"'","\\":"\\","\r":"r","\n":"n","	":"t","\u2028":"u2028","\u2029":"u2029"},D=/\\|'|\r|\n|\t|\u2028|\u2029/g;w.template=function(n,t,r){var e;r=w.defaults({},r,w.templateSettings);var u=RegExp([(r.escape||q).source,(r.interpolate||q).source,(r.evaluate||q).source].join("|")+"|$","g"),i=0,a="__p+='";n.replace(u,function(t,r,e,u,o){return a+=n.slice(i,o).replace(D,function(n){return"\\"+B[n]}),r&&(a+="'+\n((__t=("+r+"))==null?'':_.escape(__t))+\n'"),e&&(a+="'+\n((__t=("+e+"))==null?'':__t)+\n'"),u&&(a+="';\n"+u+"\n__p+='"),i=o+t.length,t}),a+="';\n",r.variable||(a="with(obj||{}){\n"+a+"}\n"),a="var __t,__p='',__j=Array.prototype.join,"+"print=function(){__p+=__j.call(arguments,'');};\n"+a+"return __p;\n";try{e=Function(r.variable||"obj","_",a)}catch(o){throw o.source=a,o}if(t)return e(t,w);var c=function(n){return e.call(this,n,w)};return c.source="function("+(r.variable||"obj")+"){\n"+a+"}",c},w.chain=function(n){return w(n).chain()};var z=function(n){return this._chain?w(n).chain():n};w.mixin(w),A(["pop","push","reverse","shift","sort","splice","unshift"],function(n){var t=e[n];w.prototype[n]=function(){var r=this._wrapped;return t.apply(r,arguments),"shift"!=n&&"splice"!=n||0!==r.length||delete r[0],z.call(this,r)}}),A(["concat","join","slice"],function(n){var t=e[n];w.prototype[n]=function(){return z.call(this,t.apply(this._wrapped,arguments))}}),w.extend(w.prototype,{chain:function(){return this._chain=!0,this},value:function(){return this._wrapped}})}).call(this);
define("underscore", function(){});

(function(){var t=this;var e=t.Backbone;var i=[];var r=i.push;var s=i.slice;var n=i.splice;var a;if(typeof exports!=="undefined"){a=exports}else{a=t.Backbone={}}a.VERSION="1.0.0";var h=t._;if(!h&&typeof require!=="undefined")h=require("underscore");a.$=t.jQuery||t.Zepto||t.ender||t.$;a.noConflict=function(){t.Backbone=e;return this};a.emulateHTTP=false;a.emulateJSON=false;var o=a.Events={on:function(t,e,i){if(!l(this,"on",t,[e,i])||!e)return this;this._events||(this._events={});var r=this._events[t]||(this._events[t]=[]);r.push({callback:e,context:i,ctx:i||this});return this},once:function(t,e,i){if(!l(this,"once",t,[e,i])||!e)return this;var r=this;var s=h.once(function(){r.off(t,s);e.apply(this,arguments)});s._callback=e;return this.on(t,s,i)},off:function(t,e,i){var r,s,n,a,o,u,c,f;if(!this._events||!l(this,"off",t,[e,i]))return this;if(!t&&!e&&!i){this._events={};return this}a=t?[t]:h.keys(this._events);for(o=0,u=a.length;o<u;o++){t=a[o];if(n=this._events[t]){this._events[t]=r=[];if(e||i){for(c=0,f=n.length;c<f;c++){s=n[c];if(e&&e!==s.callback&&e!==s.callback._callback||i&&i!==s.context){r.push(s)}}}if(!r.length)delete this._events[t]}}return this},trigger:function(t){if(!this._events)return this;var e=s.call(arguments,1);if(!l(this,"trigger",t,e))return this;var i=this._events[t];var r=this._events.all;if(i)c(i,e);if(r)c(r,arguments);return this},stopListening:function(t,e,i){var r=this._listeners;if(!r)return this;var s=!e&&!i;if(typeof e==="object")i=this;if(t)(r={})[t._listenerId]=t;for(var n in r){r[n].off(e,i,this);if(s)delete this._listeners[n]}return this}};var u=/\s+/;var l=function(t,e,i,r){if(!i)return true;if(typeof i==="object"){for(var s in i){t[e].apply(t,[s,i[s]].concat(r))}return false}if(u.test(i)){var n=i.split(u);for(var a=0,h=n.length;a<h;a++){t[e].apply(t,[n[a]].concat(r))}return false}return true};var c=function(t,e){var i,r=-1,s=t.length,n=e[0],a=e[1],h=e[2];switch(e.length){case 0:while(++r<s)(i=t[r]).callback.call(i.ctx);return;case 1:while(++r<s)(i=t[r]).callback.call(i.ctx,n);return;case 2:while(++r<s)(i=t[r]).callback.call(i.ctx,n,a);return;case 3:while(++r<s)(i=t[r]).callback.call(i.ctx,n,a,h);return;default:while(++r<s)(i=t[r]).callback.apply(i.ctx,e)}};var f={listenTo:"on",listenToOnce:"once"};h.each(f,function(t,e){o[e]=function(e,i,r){var s=this._listeners||(this._listeners={});var n=e._listenerId||(e._listenerId=h.uniqueId("l"));s[n]=e;if(typeof i==="object")r=this;e[t](i,r,this);return this}});o.bind=o.on;o.unbind=o.off;h.extend(a,o);var d=a.Model=function(t,e){var i;var r=t||{};e||(e={});this.cid=h.uniqueId("c");this.attributes={};h.extend(this,h.pick(e,p));if(e.parse)r=this.parse(r,e)||{};if(i=h.result(this,"defaults")){r=h.defaults({},r,i)}this.set(r,e);this.changed={};this.initialize.apply(this,arguments)};var p=["url","urlRoot","collection"];h.extend(d.prototype,o,{changed:null,validationError:null,idAttribute:"id",initialize:function(){},toJSON:function(t){return h.clone(this.attributes)},sync:function(){return a.sync.apply(this,arguments)},get:function(t){return this.attributes[t]},escape:function(t){return h.escape(this.get(t))},has:function(t){return this.get(t)!=null},set:function(t,e,i){var r,s,n,a,o,u,l,c;if(t==null)return this;if(typeof t==="object"){s=t;i=e}else{(s={})[t]=e}i||(i={});if(!this._validate(s,i))return false;n=i.unset;o=i.silent;a=[];u=this._changing;this._changing=true;if(!u){this._previousAttributes=h.clone(this.attributes);this.changed={}}c=this.attributes,l=this._previousAttributes;if(this.idAttribute in s)this.id=s[this.idAttribute];for(r in s){e=s[r];if(!h.isEqual(c[r],e))a.push(r);if(!h.isEqual(l[r],e)){this.changed[r]=e}else{delete this.changed[r]}n?delete c[r]:c[r]=e}if(!o){if(a.length)this._pending=true;for(var f=0,d=a.length;f<d;f++){this.trigger("change:"+a[f],this,c[a[f]],i)}}if(u)return this;if(!o){while(this._pending){this._pending=false;this.trigger("change",this,i)}}this._pending=false;this._changing=false;return this},unset:function(t,e){return this.set(t,void 0,h.extend({},e,{unset:true}))},clear:function(t){var e={};for(var i in this.attributes)e[i]=void 0;return this.set(e,h.extend({},t,{unset:true}))},hasChanged:function(t){if(t==null)return!h.isEmpty(this.changed);return h.has(this.changed,t)},changedAttributes:function(t){if(!t)return this.hasChanged()?h.clone(this.changed):false;var e,i=false;var r=this._changing?this._previousAttributes:this.attributes;for(var s in t){if(h.isEqual(r[s],e=t[s]))continue;(i||(i={}))[s]=e}return i},previous:function(t){if(t==null||!this._previousAttributes)return null;return this._previousAttributes[t]},previousAttributes:function(){return h.clone(this._previousAttributes)},fetch:function(t){t=t?h.clone(t):{};if(t.parse===void 0)t.parse=true;var e=this;var i=t.success;t.success=function(r){if(!e.set(e.parse(r,t),t))return false;if(i)i(e,r,t);e.trigger("sync",e,r,t)};R(this,t);return this.sync("read",this,t)},save:function(t,e,i){var r,s,n,a=this.attributes;if(t==null||typeof t==="object"){r=t;i=e}else{(r={})[t]=e}if(r&&(!i||!i.wait)&&!this.set(r,i))return false;i=h.extend({validate:true},i);if(!this._validate(r,i))return false;if(r&&i.wait){this.attributes=h.extend({},a,r)}if(i.parse===void 0)i.parse=true;var o=this;var u=i.success;i.success=function(t){o.attributes=a;var e=o.parse(t,i);if(i.wait)e=h.extend(r||{},e);if(h.isObject(e)&&!o.set(e,i)){return false}if(u)u(o,t,i);o.trigger("sync",o,t,i)};R(this,i);s=this.isNew()?"create":i.patch?"patch":"update";if(s==="patch")i.attrs=r;n=this.sync(s,this,i);if(r&&i.wait)this.attributes=a;return n},destroy:function(t){t=t?h.clone(t):{};var e=this;var i=t.success;var r=function(){e.trigger("destroy",e,e.collection,t)};t.success=function(s){if(t.wait||e.isNew())r();if(i)i(e,s,t);if(!e.isNew())e.trigger("sync",e,s,t)};if(this.isNew()){t.success();return false}R(this,t);var s=this.sync("delete",this,t);if(!t.wait)r();return s},url:function(){var t=h.result(this,"urlRoot")||h.result(this.collection,"url")||U();if(this.isNew())return t;return t+(t.charAt(t.length-1)==="/"?"":"/")+encodeURIComponent(this.id)},parse:function(t,e){return t},clone:function(){return new this.constructor(this.attributes)},isNew:function(){return this.id==null},isValid:function(t){return this._validate({},h.extend(t||{},{validate:true}))},_validate:function(t,e){if(!e.validate||!this.validate)return true;t=h.extend({},this.attributes,t);var i=this.validationError=this.validate(t,e)||null;if(!i)return true;this.trigger("invalid",this,i,h.extend(e||{},{validationError:i}));return false}});var v=["keys","values","pairs","invert","pick","omit"];h.each(v,function(t){d.prototype[t]=function(){var e=s.call(arguments);e.unshift(this.attributes);return h[t].apply(h,e)}});var g=a.Collection=function(t,e){e||(e={});if(e.url)this.url=e.url;if(e.model)this.model=e.model;if(e.comparator!==void 0)this.comparator=e.comparator;this._reset();this.initialize.apply(this,arguments);if(t)this.reset(t,h.extend({silent:true},e))};var m={add:true,remove:true,merge:true};var y={add:true,merge:false,remove:false};h.extend(g.prototype,o,{model:d,initialize:function(){},toJSON:function(t){return this.map(function(e){return e.toJSON(t)})},sync:function(){return a.sync.apply(this,arguments)},add:function(t,e){return this.set(t,h.defaults(e||{},y))},remove:function(t,e){t=h.isArray(t)?t.slice():[t];e||(e={});var i,r,s,n;for(i=0,r=t.length;i<r;i++){n=this.get(t[i]);if(!n)continue;delete this._byId[n.id];delete this._byId[n.cid];s=this.indexOf(n);this.models.splice(s,1);this.length--;if(!e.silent){e.index=s;n.trigger("remove",n,this,e)}this._removeReference(n)}return this},set:function(t,e){e=h.defaults(e||{},m);if(e.parse)t=this.parse(t,e);if(!h.isArray(t))t=t?[t]:[];var i,s,a,o,u,l;var c=e.at;var f=this.comparator&&c==null&&e.sort!==false;var d=h.isString(this.comparator)?this.comparator:null;var p=[],v=[],g={};for(i=0,s=t.length;i<s;i++){if(!(a=this._prepareModel(t[i],e)))continue;if(u=this.get(a)){if(e.remove)g[u.cid]=true;if(e.merge){u.set(a.attributes,e);if(f&&!l&&u.hasChanged(d))l=true}}else if(e.add){p.push(a);a.on("all",this._onModelEvent,this);this._byId[a.cid]=a;if(a.id!=null)this._byId[a.id]=a}}if(e.remove){for(i=0,s=this.length;i<s;++i){if(!g[(a=this.models[i]).cid])v.push(a)}if(v.length)this.remove(v,e)}if(p.length){if(f)l=true;this.length+=p.length;if(c!=null){n.apply(this.models,[c,0].concat(p))}else{r.apply(this.models,p)}}if(l)this.sort({silent:true});if(e.silent)return this;for(i=0,s=p.length;i<s;i++){(a=p[i]).trigger("add",a,this,e)}if(l)this.trigger("sort",this,e);return this},reset:function(t,e){e||(e={});for(var i=0,r=this.models.length;i<r;i++){this._removeReference(this.models[i])}e.previousModels=this.models;this._reset();this.add(t,h.extend({silent:true},e));if(!e.silent)this.trigger("reset",this,e);return this},push:function(t,e){t=this._prepareModel(t,e);this.add(t,h.extend({at:this.length},e));return t},pop:function(t){var e=this.at(this.length-1);this.remove(e,t);return e},unshift:function(t,e){t=this._prepareModel(t,e);this.add(t,h.extend({at:0},e));return t},shift:function(t){var e=this.at(0);this.remove(e,t);return e},slice:function(t,e){return this.models.slice(t,e)},get:function(t){if(t==null)return void 0;return this._byId[t.id!=null?t.id:t.cid||t]},at:function(t){return this.models[t]},where:function(t,e){if(h.isEmpty(t))return e?void 0:[];return this[e?"find":"filter"](function(e){for(var i in t){if(t[i]!==e.get(i))return false}return true})},findWhere:function(t){return this.where(t,true)},sort:function(t){if(!this.comparator)throw new Error("Cannot sort a set without a comparator");t||(t={});if(h.isString(this.comparator)||this.comparator.length===1){this.models=this.sortBy(this.comparator,this)}else{this.models.sort(h.bind(this.comparator,this))}if(!t.silent)this.trigger("sort",this,t);return this},sortedIndex:function(t,e,i){e||(e=this.comparator);var r=h.isFunction(e)?e:function(t){return t.get(e)};return h.sortedIndex(this.models,t,r,i)},pluck:function(t){return h.invoke(this.models,"get",t)},fetch:function(t){t=t?h.clone(t):{};if(t.parse===void 0)t.parse=true;var e=t.success;var i=this;t.success=function(r){var s=t.reset?"reset":"set";i[s](r,t);if(e)e(i,r,t);i.trigger("sync",i,r,t)};R(this,t);return this.sync("read",this,t)},create:function(t,e){e=e?h.clone(e):{};if(!(t=this._prepareModel(t,e)))return false;if(!e.wait)this.add(t,e);var i=this;var r=e.success;e.success=function(s){if(e.wait)i.add(t,e);if(r)r(t,s,e)};t.save(null,e);return t},parse:function(t,e){return t},clone:function(){return new this.constructor(this.models)},_reset:function(){this.length=0;this.models=[];this._byId={}},_prepareModel:function(t,e){if(t instanceof d){if(!t.collection)t.collection=this;return t}e||(e={});e.collection=this;var i=new this.model(t,e);if(!i._validate(t,e)){this.trigger("invalid",this,t,e);return false}return i},_removeReference:function(t){if(this===t.collection)delete t.collection;t.off("all",this._onModelEvent,this)},_onModelEvent:function(t,e,i,r){if((t==="add"||t==="remove")&&i!==this)return;if(t==="destroy")this.remove(e,r);if(e&&t==="change:"+e.idAttribute){delete this._byId[e.previous(e.idAttribute)];if(e.id!=null)this._byId[e.id]=e}this.trigger.apply(this,arguments)}});var _=["forEach","each","map","collect","reduce","foldl","inject","reduceRight","foldr","find","detect","filter","select","reject","every","all","some","any","include","contains","invoke","max","min","toArray","size","first","head","take","initial","rest","tail","drop","last","without","indexOf","shuffle","lastIndexOf","isEmpty","chain"];h.each(_,function(t){g.prototype[t]=function(){var e=s.call(arguments);e.unshift(this.models);return h[t].apply(h,e)}});var w=["groupBy","countBy","sortBy"];h.each(w,function(t){g.prototype[t]=function(e,i){var r=h.isFunction(e)?e:function(t){return t.get(e)};return h[t](this.models,r,i)}});var b=a.View=function(t){this.cid=h.uniqueId("view");this._configure(t||{});this._ensureElement();this.initialize.apply(this,arguments);this.delegateEvents()};var x=/^(\S+)\s*(.*)$/;var E=["model","collection","el","id","attributes","className","tagName","events"];h.extend(b.prototype,o,{tagName:"div",$:function(t){return this.$el.find(t)},initialize:function(){},render:function(){return this},remove:function(){this.$el.remove();this.stopListening();return this},setElement:function(t,e){if(this.$el)this.undelegateEvents();this.$el=t instanceof a.$?t:a.$(t);this.el=this.$el[0];if(e!==false)this.delegateEvents();return this},delegateEvents:function(t){if(!(t||(t=h.result(this,"events"))))return this;this.undelegateEvents();for(var e in t){var i=t[e];if(!h.isFunction(i))i=this[t[e]];if(!i)continue;var r=e.match(x);var s=r[1],n=r[2];i=h.bind(i,this);s+=".delegateEvents"+this.cid;if(n===""){this.$el.on(s,i)}else{this.$el.on(s,n,i)}}return this},undelegateEvents:function(){this.$el.off(".delegateEvents"+this.cid);return this},_configure:function(t){if(this.options)t=h.extend({},h.result(this,"options"),t);h.extend(this,h.pick(t,E));this.options=t},_ensureElement:function(){if(!this.el){var t=h.extend({},h.result(this,"attributes"));if(this.id)t.id=h.result(this,"id");if(this.className)t["class"]=h.result(this,"className");var e=a.$("<"+h.result(this,"tagName")+">").attr(t);this.setElement(e,false)}else{this.setElement(h.result(this,"el"),false)}}});a.sync=function(t,e,i){var r=k[t];h.defaults(i||(i={}),{emulateHTTP:a.emulateHTTP,emulateJSON:a.emulateJSON});var s={type:r,dataType:"json"};if(!i.url){s.url=h.result(e,"url")||U()}if(i.data==null&&e&&(t==="create"||t==="update"||t==="patch")){s.contentType="application/json";s.data=JSON.stringify(i.attrs||e.toJSON(i))}if(i.emulateJSON){s.contentType="application/x-www-form-urlencoded";s.data=s.data?{model:s.data}:{}}if(i.emulateHTTP&&(r==="PUT"||r==="DELETE"||r==="PATCH")){s.type="POST";if(i.emulateJSON)s.data._method=r;var n=i.beforeSend;i.beforeSend=function(t){t.setRequestHeader("X-HTTP-Method-Override",r);if(n)return n.apply(this,arguments)}}if(s.type!=="GET"&&!i.emulateJSON){s.processData=false}if(s.type==="PATCH"&&window.ActiveXObject&&!(window.external&&window.external.msActiveXFilteringEnabled)){s.xhr=function(){return new ActiveXObject("Microsoft.XMLHTTP")}}var o=i.xhr=a.ajax(h.extend(s,i));e.trigger("request",e,o,i);return o};var k={create:"POST",update:"PUT",patch:"PATCH","delete":"DELETE",read:"GET"};a.ajax=function(){return a.$.ajax.apply(a.$,arguments)};var S=a.Router=function(t){t||(t={});if(t.routes)this.routes=t.routes;this._bindRoutes();this.initialize.apply(this,arguments)};var $=/\((.*?)\)/g;var T=/(\(\?)?:\w+/g;var H=/\*\w+/g;var A=/[\-{}\[\]+?.,\\\^$|#\s]/g;h.extend(S.prototype,o,{initialize:function(){},route:function(t,e,i){if(!h.isRegExp(t))t=this._routeToRegExp(t);if(h.isFunction(e)){i=e;e=""}if(!i)i=this[e];var r=this;a.history.route(t,function(s){var n=r._extractParameters(t,s);i&&i.apply(r,n);r.trigger.apply(r,["route:"+e].concat(n));r.trigger("route",e,n);a.history.trigger("route",r,e,n)});return this},navigate:function(t,e){a.history.navigate(t,e);return this},_bindRoutes:function(){if(!this.routes)return;this.routes=h.result(this,"routes");var t,e=h.keys(this.routes);while((t=e.pop())!=null){this.route(t,this.routes[t])}},_routeToRegExp:function(t){t=t.replace(A,"\\$&").replace($,"(?:$1)?").replace(T,function(t,e){return e?t:"([^/]+)"}).replace(H,"(.*?)");return new RegExp("^"+t+"$")},_extractParameters:function(t,e){var i=t.exec(e).slice(1);return h.map(i,function(t){return t?decodeURIComponent(t):null})}});var I=a.History=function(){this.handlers=[];h.bindAll(this,"checkUrl");if(typeof window!=="undefined"){this.location=window.location;this.history=window.history}};var N=/^[#\/]|\s+$/g;var P=/^\/+|\/+$/g;var O=/msie [\w.]+/;var C=/\/$/;I.started=false;h.extend(I.prototype,o,{interval:50,getHash:function(t){var e=(t||this).location.href.match(/#(.*)$/);return e?e[1]:""},getFragment:function(t,e){if(t==null){if(this._hasPushState||!this._wantsHashChange||e){t=this.location.pathname;var i=this.root.replace(C,"");if(!t.indexOf(i))t=t.substr(i.length)}else{t=this.getHash()}}return t.replace(N,"")},start:function(t){if(I.started)throw new Error("Backbone.history has already been started");I.started=true;this.options=h.extend({},{root:"/"},this.options,t);this.root=this.options.root;this._wantsHashChange=this.options.hashChange!==false;this._wantsPushState=!!this.options.pushState;this._hasPushState=!!(this.options.pushState&&this.history&&this.history.pushState);var e=this.getFragment();var i=document.documentMode;var r=O.exec(navigator.userAgent.toLowerCase())&&(!i||i<=7);this.root=("/"+this.root+"/").replace(P,"/");if(r&&this._wantsHashChange){this.iframe=a.$('<iframe src="javascript:0" tabindex="-1" />').hide().appendTo("body")[0].contentWindow;this.navigate(e)}if(this._hasPushState){a.$(window).on("popstate",this.checkUrl)}else if(this._wantsHashChange&&"onhashchange"in window&&!r){a.$(window).on("hashchange",this.checkUrl)}else if(this._wantsHashChange){this._checkUrlInterval=setInterval(this.checkUrl,this.interval)}this.fragment=e;var s=this.location;var n=s.pathname.replace(/[^\/]$/,"$&/")===this.root;if(this._wantsHashChange&&this._wantsPushState&&!this._hasPushState&&!n){this.fragment=this.getFragment(null,true);this.location.replace(this.root+this.location.search+"#"+this.fragment);return true}else if(this._wantsPushState&&this._hasPushState&&n&&s.hash){this.fragment=this.getHash().replace(N,"");this.history.replaceState({},document.title,this.root+this.fragment+s.search)}if(!this.options.silent)return this.loadUrl()},stop:function(){a.$(window).off("popstate",this.checkUrl).off("hashchange",this.checkUrl);clearInterval(this._checkUrlInterval);I.started=false},route:function(t,e){this.handlers.unshift({route:t,callback:e})},checkUrl:function(t){var e=this.getFragment();if(e===this.fragment&&this.iframe){e=this.getFragment(this.getHash(this.iframe))}if(e===this.fragment)return false;if(this.iframe)this.navigate(e);this.loadUrl()||this.loadUrl(this.getHash())},loadUrl:function(t){var e=this.fragment=this.getFragment(t);var i=h.any(this.handlers,function(t){if(t.route.test(e)){t.callback(e);return true}});return i},navigate:function(t,e){if(!I.started)return false;if(!e||e===true)e={trigger:e};t=this.getFragment(t||"");if(this.fragment===t)return;this.fragment=t;var i=this.root+t;if(this._hasPushState){this.history[e.replace?"replaceState":"pushState"]({},document.title,i)}else if(this._wantsHashChange){this._updateHash(this.location,t,e.replace);if(this.iframe&&t!==this.getFragment(this.getHash(this.iframe))){if(!e.replace)this.iframe.document.open().close();this._updateHash(this.iframe.location,t,e.replace)}}else{return this.location.assign(i)}if(e.trigger)this.loadUrl(t)},_updateHash:function(t,e,i){if(i){var r=t.href.replace(/(javascript:|#).*$/,"");t.replace(r+"#"+e)}else{t.hash="#"+e}}});a.history=new I;var j=function(t,e){var i=this;var r;if(t&&h.has(t,"constructor")){r=t.constructor}else{r=function(){return i.apply(this,arguments)}}h.extend(r,i,e);var s=function(){this.constructor=r};s.prototype=i.prototype;r.prototype=new s;if(t)h.extend(r.prototype,t);r.__super__=i.prototype;return r};d.extend=g.extend=S.extend=b.extend=I.extend=j;var U=function(){throw new Error('A "url" property or function must be specified')};var R=function(t,e){var i=e.error;e.error=function(r){if(i)i(t,r,e);t.trigger("error",t,r,e)}}}).call(this);

define("backbone", function(){});

//Defines the config object used by backbone-indexeddb adapter - contains the offline db schema
define('indexeddb_backbone_config',['jquery', 'configs'],

function(pass, configs) {
    var idb = {
        nolog: true,
        id: "offline-database-v2",
        description: "The offline database for COCO",
        migrations: [{
            version: 1,
            migrate: function(transaction, next) {
                for (var member in configs) {
                    //creating an objectstore for each entity defined in config file
                    var entity_store = transaction.db.createObjectStore(configs[member].entity_name, {
                        autoIncrement: true,
                        keyPath: "id"
                    });
                    //creating index on online_id field in each objectstore
                    entity_store.createIndex("onlineIndex", "online_id", {
                        unique: true
                    });
                    //creating a unique index on the unique together fields of this entity to enforce uniqueness
                    var uniques = configs[member].unique_together_fields;
                    if (uniques && uniques.length) {
                        entity_store.createIndex("uniquesindex", uniques, {
                            unique: true
                        });
                    }
                }
                
                //creating uploadQ objectstore - stores objects yet to be synced with server
                transaction.db.createObjectStore("uploadqueue", {
                    autoIncrement: true,
                    keyPath: "id"
                });
                
                //creating meta_data objectstore - stores timestamps of last full download, last inc download
                var meta_store = transaction.db.createObjectStore("meta_data", {
                    autoIncrement: true,
                    keyPath: "id"
                });
                meta_store.createIndex("metaIndex", "key", {
                    unique: true
                })
                
                //creating full_download_info objectstore - stores info abt which chunks have been downloaded - used for resumable full download
                var full_download_info_store = transaction.db.createObjectStore("full_download_info", {
                    autoIncrement: true,
                    keyPath: "id"
                });
                full_download_info_store.createIndex("downloadedIndex", ["entity_name", "offset", "limit"], {
                    unique: true
                });
                
                //creating user objectstore - stores the username, password and login-status of user
                var user_store = transaction.db.createObjectStore("user", {
                    autoIncrement: true,
                    keyPath: "id"
                });
                user_store.createIndex("userIndex", "key", {
                    unique: true
                })
                console.log("indexeddb database created");
                next();
            }
        }]
    };

    return idb;

});

(function () { /*global _: false, Backbone: false */
    // Generate four random hex digits.
    function S4() {
        return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
    }

    // Generate a pseudo-GUID by concatenating random hexadecimal.
    function guid() {
        return (S4() + S4() + "-" + S4() + "-" + S4() + "-" + S4() + "-" + S4() + S4() + S4());
    }

    var Backbone, _;
    if(typeof exports !== 'undefined'){
        _ = require('underscore');
        Backbone = require('backbone');
    } else {
        _ = window._;
        Backbone = window.Backbone;
    }


     // Naming is a mess!
     var indexedDB = window.indexedDB || window.webkitIndexedDB || window.mozIndexedDB || window.msIndexedDB ;
     var IDBTransaction = window.IDBTransaction || window.webkitIDBTransaction || { READ_WRITE: "readwrite" }; // No prefix in moz
     var IDBKeyRange = window.IDBKeyRange || window.webkitIDBKeyRange ; // No prefix in moz

     window.IDBCursor = window.IDBCursor || window.webkitIDBCursor ||  window.mozIDBCursor ||  window.msIDBCursor ;


    // Driver object
    // That's the interesting part.
    // There is a driver for each schema provided. The schema is a te combination of name (for the database), a version as well as migrations to reach that
    // version of the database.
    function Driver(schema, ready, nolog) {
        this.schema         = schema;
        this.ready          = ready;
        this.error          = null;
        this.transactions   = []; // Used to list all transactions and keep track of active ones.
        this.db             = null;
        this.nolog          = nolog;
        this.supportOnUpgradeNeeded = false;
        var lastMigrationPathVersion = _.last(this.schema.migrations).version;
        if (!this.nolog) debugLog("opening database " + this.schema.id + " in version #" + lastMigrationPathVersion);
        this.dbRequest      = indexedDB.open(this.schema.id,lastMigrationPathVersion); //schema version need to be an unsigned long

        this.launchMigrationPath = function(dbVersion) {
            var transaction = this.dbRequest.transaction || versionRequest.result;
            var clonedMigrations = _.clone(schema.migrations);
            this.migrate(transaction, clonedMigrations, dbVersion, {
                success: function () {
                    this.ready();
                }.bind(this),
                error: function () {
                    this.error = "Database not up to date. " + dbVersion + " expected was " + lastMigrationPathVersion;
                }.bind(this)
            });
        };

        this.dbRequest.onblocked = function(event){
            if (!this.nolog) debugLog("blocked");
        }

        this.dbRequest.onsuccess = function (e) {
            this.db = e.target.result; // Attach the connection ot the queue.
            if(!this.supportOnUpgradeNeeded)
            {
                var currentIntDBVersion = (parseInt(this.db.version) ||  0); // we need convert beacuse chrome store in integer and ie10 DP4+ in int;
                var lastMigrationInt = (parseInt(lastMigrationPathVersion) || 0);  // And make sure we compare numbers with numbers.

                if (currentIntDBVersion === lastMigrationInt) { //if support new event onupgradeneeded will trigger the ready function
                    // No migration to perform!

                    this.ready();
                } else if (currentIntDBVersion < lastMigrationInt ) {
                    // We need to migrate up to the current migration defined in the database
                    this.launchMigrationPath(currentIntDBVersion);
                } else {
                    // Looks like the IndexedDB is at a higher version than the current driver schema.
                    this.error = "Database version is greater than current code " + currentIntDBVersion + " expected was " + lastMigrationInt;
                }
            };
        }.bind(this);



        this.dbRequest.onerror = function (e) {
            // Failed to open the database
            this.error = "Couldn't not connect to the database"
        }.bind(this);

        this.dbRequest.onabort = function (e) {
            // Failed to open the database
            this.error = "Connection to the database aborted"
        }.bind(this);



        this.dbRequest.onupgradeneeded = function(iDBVersionChangeEvent){
            this.db =iDBVersionChangeEvent.target.transaction.db;

            this.supportOnUpgradeNeeded = true;

            if (!this.nolog) debugLog("onupgradeneeded = " + iDBVersionChangeEvent.oldVersion + " => " + iDBVersionChangeEvent.newVersion);
            this.launchMigrationPath(iDBVersionChangeEvent.oldVersion);


        }.bind(this);
    }

    function debugLog(str) {
        if (typeof window !== "undefined" && typeof window.console !== "undefined" && typeof window.console.log !== "undefined") {
            window.console.log(str);
        }
        else if(console.log !== "undefined") {
            console.log(str)
        }
    }

    // Driver Prototype
    Driver.prototype = {

        // Tracks transactions. Mostly for debugging purposes. TO-IMPROVE
        _track_transaction: function(transaction) {
            this.transactions.push(transaction);
            function removeIt() {
                var idx = this.transactions.indexOf(transaction);
                if (idx !== -1) {this.transactions.splice(idx); }
            };
            transaction.oncomplete = removeIt.bind(this);
            transaction.onabort = removeIt.bind(this);
            transaction.onerror = removeIt.bind(this);
        },

        // Performs all the migrations to reach the right version of the database.
        migrate: function (transaction, migrations, version, options) {
            if (!this.nolog) debugLog("migrate begin version from #" + version);
            var that = this;
            var migration = migrations.shift();
            if (migration) {
                if (!version || version < migration.version) {
                    // We need to apply this migration-
                    if (typeof migration.before == "undefined") {
                        migration.before = function (next) {
                            next();
                        };
                    }
                    if (typeof migration.after == "undefined") {
                        migration.after = function (next) {
                            next();
                        };
                    }
                    // First, let's run the before script
                    if (!this.nolog) debugLog("migrate begin before version #" + migration.version);
                    migration.before(function () {
                        if (!this.nolog) debugLog("migrate done before version #" + migration.version);

                        var continueMigration = function (e) {
                            if (!this.nolog) debugLog("migrate begin migrate version #" + migration.version);

                            migration.migrate(transaction, function () {
                                if (!this.nolog) debugLog("migrate done migrate version #" + migration.version);
                                // Migration successfully appliedn let's go to the next one!
                                if (!this.nolog) debugLog("migrate begin after version #" + migration.version);
                                migration.after(function () {
                                    if (!this.nolog) debugLog("migrate done after version #" + migration.version);
                                    if (!this.nolog) debugLog("Migrated to " + migration.version);

                                    //last modification occurred, need finish
                                    if(migrations.length ==0) {
                                        /*if(this.supportOnUpgradeNeeded){
                                            debugLog("Done migrating");
                                            // No more migration
                                            options.success();
                                        }
                                        else{*/
                                            if (!this.nolog) debugLog("migrate setting transaction.oncomplete to finish  version #" + migration.version);
                                            transaction.oncomplete = function() {
                                                if (!that.nolog) debugLog("migrate done transaction.oncomplete version #" + migration.version);

                                                if (!that.nolog) debugLog("Done migrating");
                                                // No more migration
                                                options.success();
                                            }
                                        //}
                                    }
                                    else
                                    {
                                        if (!this.nolog) debugLog("migrate end from version #" + version + " to " + migration.version);
                                            that.migrate(transaction, migrations, version, options);
                                    }

                                }.bind(this));
                            }.bind(this));
                        }.bind(this);

                        if(!this.supportOnUpgradeNeeded){
                            if (!this.nolog) debugLog("migrate begin setVersion version #" + migration.version);
                            var versionRequest = this.db.setVersion(migration.version);
                            versionRequest.onsuccess = continueMigration;
                            versionRequest.onerror = options.error;
                        }
                        else {
                            continueMigration();
                        }

                    }.bind(this));
                } else {
                    // No need to apply this migration
                    if (!this.nolog) debugLog("Skipping migration " + migration.version);
                    this.migrate(transaction, migrations, version, options);
                }
            }
        },

        // This is the main method, called by the ExecutionQueue when the driver is ready (database open and migration performed)
        execute: function (storeName, method, object, options) {
            if (!this.nolog) debugLog("execute : " + method +  " on " + storeName + " for " + object.id);
            switch (method) {
            case "create":
                this.create(storeName, object, options);
                break;
            case "read":
                if (object.id || object.cid) {
                    this.read(storeName, object, options); // It's a model
                } else {
                    this.query(storeName, object, options); // It's a collection
                }
                break;
            case "update":
                this.update(storeName, object, options); // We may want to check that this is not a collection. TOFIX
                break;
            case "delete":
                if (object.id || object.cid) {
                    this.delete(storeName, object, options);
                } else {
                    this.clear(storeName, object, options);
                }
                break;
            default:
                // Hum what?
            }
        },

        // Writes the json to the storeName in db. It is a create operations, which means it will fail if the key already exists
        // options are just success and error callbacks.
        create: function (storeName, object, options) {
            var writeTransaction = this.db.transaction([storeName], 'readwrite');
            //this._track_transaction(writeTransaction);
            var store = writeTransaction.objectStore(storeName);
            var json = object.toJSON();
            var writeRequest;

            if (json.id === undefined && !store.autoIncrement) json.id = guid();

            writeTransaction.onerror = function (e) {
                options.error(e);
            };
            writeTransaction.oncomplete = function (e) {
                options.success(json);
            };

            if (!store.keyPath)
                writeRequest = store.add(json, json.id);
            else
                writeRequest = store.add(json);
            
            writeRequest.onsuccess = function (e) {
                if(!json.id) json.id = e.target.result;
            };    
        },

        // Writes the json to the storeName in db. It is an update operation, which means it will overwrite the value if the key already exist
        // options are just success and error callbacks.
        update: function (storeName, object, options) {
            var writeTransaction = this.db.transaction([storeName], 'readwrite');
            //this._track_transaction(writeTransaction);
            var store = writeTransaction.objectStore(storeName);
            var json = object.toJSON();
            var writeRequest;

            if (!json.id) json.id = guid();

            if (!store.keyPath)
              writeRequest = store.put(json, json.id);
            else
              writeRequest = store.put(json);

            writeRequest.onerror = function (e) {
                options.error(e);
            };
            writeTransaction.oncomplete = function (e) {
                options.success(json);
            };
        },

        // Reads from storeName in db with json.id if it's there of with any json.xxxx as long as xxx is an index in storeName
        read: function (storeName, object, options) {
            var readTransaction = this.db.transaction([storeName], "readonly");
            this._track_transaction(readTransaction);

            var store = readTransaction.objectStore(storeName);
            var json = object.toJSON();

            var getRequest = null;
            if (json.id) {
                getRequest = store.get(json.id);
            } else {
                // We need to find which index we have
                _.each(store.indexNames, function (key, index) {
                    index = store.index(key);
                    if (json[index.keyPath] && !getRequest) {
                        getRequest = index.get(json[index.keyPath]);
                    }
                });
            }
            if (getRequest) {
                getRequest.onsuccess = function (event) {
                    if (event.target.result) {
                        options.success(event.target.result);
                    } else {
                        options.error("Not Found");
                    }
                };
                getRequest.onerror = function () {
                    options.error("Not Found"); // We couldn't find the record.
                }
            } else {
                options.error("Not Found"); // We couldn't even look for it, as we don't have enough data.
            }
        },

        // Deletes the json.id key and value in storeName from db.
        delete: function (storeName, object, options) {
            var deleteTransaction = this.db.transaction([storeName], 'readwrite');
            //this._track_transaction(deleteTransaction);

            var store = deleteTransaction.objectStore(storeName);
            var json = object.toJSON();

            var deleteRequest = store.delete(json.id);

            deleteTransaction.oncomplete = function (event) {
                options.success(null);
            };
            deleteRequest.onerror = function (event) {
                options.error("Not Deleted");
            };
        },

        // Clears all records for storeName from db.
        clear: function (storeName, object, options) {
            var deleteTransaction = this.db.transaction([storeName], "readwrite");
            //this._track_transaction(deleteTransaction);

            var store = deleteTransaction.objectStore(storeName);

            var deleteRequest = store.clear();
            deleteRequest.onsuccess = function (event) {
                options.success(null);
            };
            deleteRequest.onerror = function (event) {
                options.error("Not Cleared");
            };
        },

        // Performs a query on storeName in db.
        // options may include :
        // - conditions : value of an index, or range for an index
        // - range : range for the primary key
        // - limit : max number of elements to be yielded
        // - offset : skipped items.
        query: function (storeName, collection, options) {
            var elements = [];
            var skipped = 0, processed = 0;
            var queryTransaction = this.db.transaction([storeName], "readonly");
            //this._track_transaction(queryTransaction);

            var readCursor = null;
            var store = queryTransaction.objectStore(storeName);
            var index = null,
                lower = null,
                upper = null,
                bounds = null;

            if (options.conditions) {
                // We have a condition, we need to use it for the cursor
                _.each(store.indexNames, function (key) {
                    if (!readCursor) {
                        index = store.index(key);
                        if (options.conditions[index.keyPath] instanceof Array) {
                            lower = options.conditions[index.keyPath][0] > options.conditions[index.keyPath][1] ? options.conditions[index.keyPath][1] : options.conditions[index.keyPath][0];
                            upper = options.conditions[index.keyPath][0] > options.conditions[index.keyPath][1] ? options.conditions[index.keyPath][0] : options.conditions[index.keyPath][1];
                            bounds = IDBKeyRange.bound(lower, upper, true, true);

                            if (options.conditions[index.keyPath][0] > options.conditions[index.keyPath][1]) {
                                // Looks like we want the DESC order
                                readCursor = index.openCursor(bounds, window.IDBCursor.PREV || "prev");
                            } else {
                                // We want ASC order
                                readCursor = index.openCursor(bounds, window.IDBCursor.NEXT || "next");
                            }
                        } else if (options.conditions[index.keyPath] != undefined) {
                            bounds = IDBKeyRange.only(options.conditions[index.keyPath]);
                            readCursor = index.openCursor(bounds);
                        }
                    }
                });
            } else {
                // No conditions, use the index
                if (options.range) {
                    lower = options.range[0] > options.range[1] ? options.range[1] : options.range[0];
                    upper = options.range[0] > options.range[1] ? options.range[0] : options.range[1];
                    bounds = IDBKeyRange.bound(lower, upper);
                    if (options.range[0] > options.range[1]) {
                        readCursor = store.openCursor(bounds, window.IDBCursor.PREV || "prev");
                    } else {
                        readCursor = store.openCursor(bounds, window.IDBCursor.NEXT || "next");
                    }
                } else {
                    readCursor = store.openCursor();
                }
            }

            if (typeof (readCursor) == "undefined" || !readCursor) {
                options.error("No Cursor");
            } else {
                readCursor.onerror = function(e){
                    options.error("readCursor error", e);
                };
                // Setup a handler for the cursor’s `success` event:
                readCursor.onsuccess = function (e) {
                    var cursor = e.target.result;
                    if (!cursor) {
                        if (options.addIndividually || options.clear) {
                            // nothing!
                            // We need to indicate that we're done. But, how?
                            collection.trigger("reset");
                        } else {
                            options.success(elements); // We're done. No more elements.
                        }
                    }
                    else {
                        // Cursor is not over yet.
                        if (options.limit && processed >= options.limit) {
                            // Yet, we have processed enough elements. So, let's just skip.
                            if (bounds && options.conditions[index.keyPath]) {
                                cursor.continue(options.conditions[index.keyPath][1] + 1); /* We need to 'terminate' the cursor cleany, by moving to the end */
                            } else {
                                cursor.continue(); /* We need to 'terminate' the cursor cleany, by moving to the end */
                            }
                        }
                        else if (options.offset && options.offset > skipped) {
                            skipped++;
                            cursor.continue(); /* We need to Moving the cursor forward */
                        } else {
                            // This time, it looks like it's good!
                            if (options.addIndividually) {
                                collection.add(cursor.value);
                            } else if (options.clear) {
                                var deleteRequest = store.delete(cursor.value.id);
                                deleteRequest.onsuccess = function (event) {
                                    elements.push(cursor.value);
                                };
                                deleteRequest.onerror = function (event) {
                                    elements.push(cursor.value);
                                };

                            } else {
                                elements.push(cursor.value);
                            }
                            processed++;
                            cursor.continue();
                        }
                    }
                };
            }
        },
        close :function(){
            if(this.db){
                this.db.close()
;            }
        }
    };

    // ExecutionQueue object
    // The execution queue is an abstraction to buffer up requests to the database.
    // It holds a "driver". When the driver is ready, it just fires up the queue and executes in sync.
    function ExecutionQueue(schema,next,nolog) {
        this.driver     = new Driver(schema, this.ready.bind(this), nolog);
        this.started    = false;
        this.stack      = [];
        this.version    = _.last(schema.migrations).version;
        this.next = next;
    }

    // ExecutionQueue Prototype
    ExecutionQueue.prototype = {
        // Called when the driver is ready
        // It just loops over the elements in the queue and executes them.
        ready: function () {
            this.started = true;
            _.each(this.stack, function (message) {
                this.execute(message);
            }.bind(this));
            this.next();
        },

        // Executes a given command on the driver. If not started, just stacks up one more element.
        execute: function (message) {
            if (this.started) {
                this.driver.execute(message[1].storeName, message[0], message[1], message[2]); // Upon messages, we execute the query
            } else {
                this.stack.push(message);
            }
        },

        close : function(){
            this.driver.close();
        }
    };

    // Method used by Backbone for sync of data with data store. It was initially designed to work with "server side" APIs, This wrapper makes
    // it work with the local indexedDB stuff. It uses the schema attribute provided by the object.
    // The wrapper keeps an active Executuon Queue for each "schema", and executes querues agains it, based on the object type (collection or
    // single model), but also the method... etc.
    // Keeps track of the connections
    var Databases = {};

    function sync(method, object, options) {

        if(method=="closeall"){
            _.each(Databases,function(database){
                database.close();
            });
            // Clean up active databases object.
            Databases = {}
            return;
        }

        // If a model or a collection does not define a database, fall back on ajaxSync
        if (typeof object.database === 'undefined' && typeof Backbone.ajaxSync === 'function'){
            return Backbone.ajaxSync(method, object, options);
        }

        var schema = object.database;
        if (Databases[schema.id]) {
            if(Databases[schema.id].version != _.last(schema.migrations).version){
                Databases[schema.id].close();
                delete Databases[schema.id];
            }
        }

        var promise;
        var noop = function() {};

        if (typeof($) != 'undefined' && $.Deferred) {
            var dfd = $.Deferred();
            var resolve = dfd.resolve;
            var reject = dfd.reject;

            promise = dfd.promise();
        } else {
            var resolve = noop;
            var reject = noop;
        }

        var success = options.success;
        options.success = function(resp) {
            if (success) success(resp);
            object.trigger('sync', object, resp, options);
            resolve(object);
        };

        var error = options.error;
        options.error = function(resp) {
            reject();
            if (error) error(resp);
            object.trigger('error', object, resp, options);
        };

        var next = function(){
            Databases[schema.id].execute([method, object, options]);
        };

        if (!Databases[schema.id]) {
              Databases[schema.id] = new ExecutionQueue(schema,next,schema.nolog);
        } else {
            next();
        }

    	return promise;
    };

    if(typeof exports == 'undefined'){
        Backbone.ajaxSync = Backbone.sync;
        Backbone.sync = sync;
    }
    else {
        exports.sync = sync;
        exports.debugLog = debugLog;
    }

    //window.addEventListener("unload",function(){Backbone.sync("closeall")})
})();

define("indexeddb-backbone", function(){});

define('collections/upload_collection',[
  'jquery',
  'backbone',
  'indexeddb_backbone_config',
  'indexeddb-backbone'      
  // Using the Require.js text! plugin, we are loaded raw text
  // which will be used as our views primary template
  // 'text!templates/project/list.html'
], function(jquery, backbone, indexeddb){
    
    var generic_model_offline = Backbone.Model.extend({
        database: indexeddb,
        storeName: "uploadqueue",
    });

    var generic_upload_collection = Backbone.Collection.extend({
        model: generic_model_offline,
        database: indexeddb,
        storeName: "uploadqueue",
        fetched: false
    });
    var upload_collection = new generic_upload_collection();
    upload_collection.fetch({
        success: function(coll){
            console.log("UPLOADCOLLECTION : successfully fetched");
            coll.fetched = true; 
        },
        error: function(){
            console.log("UPLOADCOLLECTION :  fetch failed")            
        }        
    });
    
    // upload_collection.on('add')
            
  // Our module now returns our view
  return upload_collection;
});
/*!
 * backbone.layoutmanager.js v0.8.1
 * Copyright 2012, Tim Branyen (@tbranyen)
 * backbone.layoutmanager.js may be freely distributed under the MIT license.
 */
(function(window) {



// Hoisted, referenced at the bottom of the source.  This caches a list of all
// LayoutManager options at definition time.
var keys;

// Localize global dependency references.
var Backbone = window.Backbone;
var _ = window._;
var $ = window.$;

// Maintain references to the two `Backbone.View` functions that are
// overwritten so that they can be proxied.
var _configure = Backbone.View.prototype._configure;
var render = Backbone.View.prototype.render;

// Cache these methods for performance.
var aPush = Array.prototype.push;
var aConcat = Array.prototype.concat;
var aSplice = Array.prototype.splice;

// LayoutManager is a wrapper around a `Backbone.View`.
var LayoutManager = Backbone.View.extend({
  // This named function allows for significantly easier debugging.
  constructor: function Layout(options) {
    // Options may not always be passed to the constructor, this ensures it is
    // always an object.
    options = options || {};

    // Grant this View superpowers.
    LayoutManager.setupView(this, options);

    // Have Backbone set up the rest of this View.
    Backbone.View.call(this, options);
  },

  // Shorthand to `setView` function with the `insert` flag set.
  insertView: function(selector, view) {
    // If the `view` argument exists, then a selector was passed in.  This code
    // path will forward the selector on to `setView`.
    if (view) {
      return this.setView(selector, view, true);
    }

    // If no `view` argument is defined, then assume the first argument is the
    // View, somewhat now confusingly named `selector`.
    return this.setView(selector, true);
  },

  // Iterate over an object and ensure every value is wrapped in an array to
  // ensure they will be inserted, then pass that object to `setViews`.
  insertViews: function(views) {
    // If an array of views was passed it should be inserted into the
    // root view. Much like calling insertView without a selector.
    if (_.isArray(views)) {
      return this.setViews({ "": views });
    }

    _.each(views, function(view, selector) {
      views[selector] = _.isArray(view) ? view : [view];
    });

    return this.setViews(views);
  },

  // Returns the View that matches the `getViews` filter function.
  getView: function(fn) {
    // If `getView` is invoked with undefined as the first argument, then the
    // second argument will be used instead.  This is to allow
    // `getViews(undefined, fn)` to work as `getViews(fn)`.  Useful for when
    // you are allowing an optional selector.
    if (typeof fn !== "function" && typeof fn !== "string") {
      fn = arguments[1];
    }

    return this.getViews(fn).first().value();
  },

  // Provide a filter function to get a flattened array of all the subviews.
  // If the filter function is omitted it will return all subviews.  If a 
  // String is passed instead, it will return the Views for that selector.
  getViews: function(fn) {
    // Generate an array of all top level (no deeply nested) Views flattened.
    var views = _.chain(this.views).map(function(view) {
      return _.isArray(view) ? view : [view];
    }, this).flatten().value();

    // If the filter argument is a String, then return a chained Version of the
    // elements.
    if (typeof fn === "string") {
      return _.chain([this.views[fn]]).flatten();
    }

    // If the argument passed is an Object, then pass it to `_.where`.
    if (typeof fn === "object") {
      return _.chain([_.where(views, fn)]).flatten();
    }

    // If a filter function is provided, run it on all Views and return a
    // wrapped chain. Otherwise, simply return a wrapped chain of all Views.
    return _.chain(typeof fn === "function" ? _.filter(views, fn) : views);
  },
  
  // Use this to remove Views, internally uses `getViews` so you can pass the
  // same argument here as you would to that method.
  removeView: function(fn) {
    // Allow an optional selector or function to find the right model and
    // remove nested Views based off the results of the selector or filter.
    return this.getViews(fn).each(function(nestedView) {
      nestedView.remove();
    });
  },

  // This takes in a partial name and view instance and assigns them to
  // the internal collection of views.  If a view is not a LayoutManager
  // instance, then mix in the LayoutManager prototype.  This ensures
  // all Views can be used successfully.
  //
  // Must definitely wrap any render method passed in or defaults to a
  // typical render function `return layout(this).render()`.
  setView: function(name, view, insert) {
    var manager, existing, options;
    // Parent view, the one you are setting a View on.
    var root = this;

    // If no name was passed, use an empty string and shift all arguments.
    if (typeof name !== "string") {
      insert = view;
      view = name;
      name = "";
    }

    // If the parent views object doesn't exist... create it.
    this.views = this.views || {};

    // Shorthand the `__manager__` property.
    manager = view.__manager__;

    // Shorthand the View that potentially already exists.
    existing = this.views[name];

    // If the View has not been properly set up, throw an Error message
    // indicating that the View needs `manage: true` set.
    if (!manager) {
      throw new Error("Please set `View#manage` property with selector '" +
        name + "' to `true`.");
    }

    // Assign options.
    options = view.getAllOptions();

    // Add reference to the parentView.
    manager.parent = root;

    // Add reference to the placement selector used.
    manager.selector = name;

    // Set up event bubbling, inspired by Backbone.ViewMaster.  Do not bubble
    // internal events that are triggered.
    view.on("all", function(name) {
      if (name !== "beforeRender" && name !== "afterRender") {
        root.trigger.apply(root, arguments);
      }
    }, view);

    // Code path is less complex for Views that are not being inserted.  Simply
    // remove existing Views and bail out with the assignment.
    if (!insert) {
      // If the View we are adding has already been rendered, simply inject it
      // into the parent.
      if (manager.hasRendered) {
        // If this View is not using a dynamically created container element,
        // use the children instead.
        if (manager.noel) {
          view.setElement(view.$el.children(), false);
        }

        // Apply the partial.
        options.partial(root.el, manager.selector, view.$el, manager.insert);
      }

      // Ensure remove is called when swapping View's.
      if (existing) {
        // If the views are an array, iterate and remove each individually.
        _.each(aConcat.call([], existing), function(nestedView) {
          nestedView.remove();
        });
      }

      // Assign to main views object and return for chainability.
      return this.views[name] = view;
    }

    // Ensure this.views[name] is an array and push this View to the end.
    this.views[name] = aConcat.call([], existing || [], view);

    // Put the view into `insert` mode.
    manager.insert = true;

    return view;
  },

  // Allows the setting of multiple views instead of a single view.
  setViews: function(views) {
    // Iterate over all the views and use the View's view method to assign.
    _.each(views, function(view, name) {
      // If the view is an array put all views into insert mode.
      if (_.isArray(view)) {
        return _.each(view, function(view) {
          this.insertView(name, view);
        }, this);
      }

      // Assign each view using the view function.
      this.setView(name, view);
    }, this);

    // Allow for chaining
    return this;
  },

  // By default this should find all nested views and render them into
  // the this.el and call done once all of them have successfully been
  // resolved.
  //
  // This function returns a promise that can be chained to determine
  // once all subviews and main view have been rendered into the view.el.
  render: function() {
    var root = this;
    var options = root.getAllOptions();
    var manager = root.__manager__;
    var parent = manager.parent;
    var rentManager = parent && parent.__manager__;
    var def = options.deferred();

    // Triggered once the render has succeeded.
    function resolve() {
      var next, afterRender;

      // If there is a parent, attach.
      if (parent) {
        if (!options.contains(parent.el, root.el)) {
          // If this View is not using a dynamically created container element,
          // use the children instead.
          if (manager.noel) {
            root.setElement(root.$el.children(), false);
          }

          // Apply the partial.
          options.partial(parent.el, manager.selector, root.$el,
            manager.insert);
        }
      }

      // Ensure events are always correctly bound after rendering.
      root.delegateEvents();

      // If no parent, ensure the elements are still set correctly.
      if (!parent && manager.noel) {
        root.setElement(root.$el.children(), false);
      }

      // Set this View as successfully rendered.
      manager.hasRendered = true;

      // Resolve the deferred.
      def.resolveWith(root, [root]);

      // Only process the queue if it exists.
      if (next = manager.queue.shift()) {
        // Ensure that the next render is only called after all other
        // `done` handlers have completed.  This will prevent `render`
        // callbacks from firing out of order.
        next();
      } else {
        // Once the queue is depleted, remove it, the render process has
        // completed.
        delete manager.queue;
      }

      // Reusable function for triggering the afterRender callback and event
      // and setting the hasRendered flag.
      function completeRender() {
        var afterRender = options.afterRender;

        if (afterRender) {
          afterRender.call(root, root);
        }

        // Always emit an afterRender event.
        root.trigger("afterRender", root);
      }

      // If the parent is currently rendering, wait until it has completed
      // until calling the nested View's `afterRender`.
      if (rentManager && rentManager.queue) {
        // Wait until the parent View has finished rendering, which could be
        // asynchronous, and trigger afterRender on this View once it has
        // compeleted.
        return parent.once("afterRender", function() {
          // Trigger the afterRender and set hasRendered.
          completeRender();
        });
      }

      // This View and its parent have both rendered.
      completeRender();
    }

    // Actually facilitate a render.
    function actuallyRender() {
      var options = root.getAllOptions();
      var manager = root.__manager__;
      var parent = manager.parent;
      var rentManager = parent && parent.__manager__;

      // The `_viewRender` method is broken out to abstract away from having
      // too much code in `processRender`.
      root._render(LayoutManager._viewRender, options).done(function() {
        // If there are no children to worry about, complete the render
        // instantly.
        if (!_.keys(root.views).length) {
          return resolve();
        }

        // Create a list of promises to wait on until rendering is done.
        // Since this method will run on all children as well, its sufficient
        // for a full hierarchical. 
        var promises = _.map(root.views, function(view) {
          var insert = _.isArray(view);

          // If items are being inserted, they will be in a non-zero length
          // Array.
          if (insert && view.length) {
            // Schedule each view to be rendered in order and return a promise
            // representing the result of the final rendering.
            return _.reduce(view.slice(1), function(prevRender, view) {
              return prevRender.then(function() {
                return view.render();
              });
            // The first view should be rendered immediately, and the resulting
            // promise used to initialize the reduction.
            }, view[0].render());
          }

          // Only return the fetch deferred, resolve the main deferred after
          // the element has been attached to it's parent.
          return !insert ? view.render() : view;
        });

        // Once all nested Views have been rendered, resolve this View's
        // deferred.
        options.when(promises).done(function() {
          resolve();
        });
      });
    }

    // Another render is currently happening if there is an existing queue, so
    // push a closure to render later into the queue.
    if (manager.queue) {
      aPush.call(manager.queue, function() {
        actuallyRender();
      });
    } else {
      manager.queue = [];

      // This the first `render`, preceeding the `queue` so render
      // immediately.
      actuallyRender(root, def);
    }

    // Add the View to the deferred so that `view.render().view.el` is
    // possible.
    def.view = root;
    
    // This is the promise that determines if the `render` function has
    // completed or not.
    return def;
  },

  // Ensure the cleanup function is called whenever remove is called.
  remove: function() {
    // Force remove itself from its parent.
    LayoutManager._removeView(this, true);

    // Call the original remove function.
    return this._remove.apply(this, arguments);
  },

  // Merge instance and global options.
  getAllOptions: function() {
    // Instance overrides take precedence, fallback to prototype options.
    return _.extend({}, this, LayoutManager.prototype.options, this.options);
  }
},
{
  // Clearable cache.
  _cache: {},

  // Creates a deferred and returns a function to call when finished.
  _makeAsync: function(options, done) {
    var handler = options.deferred();

    // Used to handle asynchronous renders.
    handler.async = function() {
      handler._isAsync = true;

      return done;
    };

    return handler;
  },

  // This gets passed to all _render methods.  The `root` value here is passed
  // from the `manage(this).render()` line in the `_render` function
  _viewRender: function(root, options) {
    var url, contents, fetchAsync;
    var manager = root.__manager__;

    // This function is responsible for pairing the rendered template into
    // the DOM element.
    function applyTemplate(rendered) {
      // Actually put the rendered contents into the element.
      if (rendered) {
        options.html(root.$el, rendered);
      }

      // Resolve only after fetch and render have succeeded.
      fetchAsync.resolveWith(root, [root]);
    }

    // Once the template is successfully fetched, use its contents to proceed.
    // Context argument is first, since it is bound for partial application
    // reasons.
    function done(context, contents) {
      // Store the rendered template someplace so it can be re-assignable.
      var rendered;
      // This allows the `render` method to be asynchronous as well as `fetch`.
      var renderAsync = LayoutManager._makeAsync(options, function(rendered) {
        applyTemplate(rendered);
      });

      // Ensure the cache is up-to-date.
      LayoutManager.cache(url, contents);

      // Render the View into the el property.
      if (contents) {
        rendered = options.render.call(renderAsync, contents, context);
      }

      // If the function was synchronous, continue execution.
      if (!renderAsync._isAsync) {
        applyTemplate(rendered);
      }
    }

    return {
      // This `render` function is what gets called inside of the View render,
      // when `manage(this).render` is called.  Returns a promise that can be
      // used to know when the element has been rendered into its parent.
      render: function() {
        var context = root.serialize || options.serialize;
        var template = root.template || options.template;

        // If data is a function, immediately call it.
        if (_.isFunction(context)) {
          context = context.call(root);
        }

        // This allows for `var done = this.async()` and then `done(contents)`.
        fetchAsync = LayoutManager._makeAsync(options, function(contents) {
          done(context, contents);
        });

        // Set the url to the prefix + the view's template property.
        if (typeof template === "string") {
          url = options.prefix + template;
        }

        // Check if contents are already cached and if they are, simply process
        // the template with the correct data.
        if (contents = LayoutManager.cache(url)) {
          done(context, contents, url);

          return fetchAsync;
        }

        // Fetch layout and template contents.
        if (typeof template === "string") {
          contents = options.fetch.call(fetchAsync, options.prefix + template);
        // If the template is already a function, simply call it.
        } else if (typeof template === "function") {
          contents = template;
        // If its not a string and not undefined, pass the value to `fetch`.
        } else if (template != null) {
          contents = options.fetch.call(fetchAsync, template);
        }

        // If the function was synchronous, continue execution.
        if (!fetchAsync._isAsync) {
          done(context, contents);
        }

        return fetchAsync;
      }
    };
  },

  // Remove all nested Views.
  _removeViews: function(root, force) {
    var views;

    // Shift arguments around.
    if (typeof root === "boolean") {
      force = root;
      root = this;
    }

    // Allow removeView to be called on instances.
    root = root || this;

    // Iterate over all of the nested View's and remove.
    root.getViews().each(function(view) {
      // Force doesn't care about if a View has rendered or not.
      if (view.__manager__.hasRendered || force) {
        LayoutManager._removeView(view, force);
      }
    });
  },

  // Remove a single nested View.
  _removeView: function(view, force) {
    var parentViews;
    // Shorthand the manager for easier access.
    var manager = view.__manager__;
    // Test for keep.
    var keep = typeof view.keep === "boolean" ? view.keep : view.options.keep;

    // Only remove views that do not have `keep` attribute set, unless the
    // View is in `insert` mode and the force flag is set.
    if (!keep && (manager.insert === true || force)) {
      // Clean out the events.
      LayoutManager.cleanViews(view);

      // Since we are removing this view, force subviews to remove
      view._removeViews(true);  
           
      // Remove the View completely.
      view.$el.remove();

      // Bail out early if no parent exists.
      if (!manager.parent) { return; }

      // Assign (if they exist) the sibling Views to a property.
      parentViews = manager.parent.views[manager.selector];

      // If this is an array of items remove items that are not marked to
      // keep.
      if (_.isArray(parentViews)) {
        // Remove duplicate Views.
        return _.each(_.clone(parentViews), function(view, i) {
          // If the managers match, splice off this View.
          if (view && view.__manager__ === manager) {
            aSplice.call(parentViews, i, 1);
          }
        });
      }

      // Otherwise delete the parent selector.
      delete manager.parent.views[manager.selector];
    }
  },

  // Cache templates into LayoutManager._cache.
  cache: function(path, contents) {
    // If template path is found in the cache, return the contents.
    if (path in this._cache && contents == null) {
      return this._cache[path];
    // Ensure path and contents aren't undefined.
    } else if (path != null && contents != null) {
      return this._cache[path] = contents;
    }

    // If the template is not in the cache, return undefined.
  },

  // Accept either a single view or an array of views to clean of all DOM
  // events internal model and collection references and all Backbone.Events.
  cleanViews: function(views) {
    // Clear out all existing views.
    _.each(aConcat.call([], views), function(view) {
      // Remove all custom events attached to this View.
      view.unbind();

      // Automatically unbind `model`.
      if (view.model instanceof Backbone.Model) {
        view.model.off(null, null, view);
      }

      // Automatically unbind `collection`.
      if (view.collection instanceof Backbone.Collection) {
        view.collection.off(null, null, view);
      }

      // Automatically unbind events bound to this View.
      view.stopListening();

      // If a custom cleanup method was provided on the view, call it after
      // the initial cleanup is done
      _.result(view, "cleanup");
    });
  },

  // This static method allows for global configuration of LayoutManager.
  configure: function(options) {
    _.extend(LayoutManager.prototype.options, options);

    // Allow LayoutManager to manage Backbone.View.prototype.
    if (options.manage) {
      Backbone.View.prototype.manage = true;
    }

    // Disable the element globally.
    if (options.el === false) {
      Backbone.View.prototype.el = false;
    }
  },
  
  // Configure a View to work with the LayoutManager plugin.
  setupView: function(views, options) {
    // Set up all Views passed.
    _.each(aConcat.call([], views), function(view) {
      // If the View has already been setup, no need to do it again.
      if (view.__manager__) {
        return;
      }

      var views, declaredViews, viewOptions;
      var proto = LayoutManager.prototype;
      var viewOverrides = _.pick(view, keys);

      // Ensure necessary properties are set.
      _.defaults(view, {
        // Ensure a view always has a views object.
        views: {},

        // Internal state object used to store whether or not a View has been
        // taken over by layout manager and if it has been rendered into the DOM.
        __manager__: {},

        // Add the ability to remove all Views.
        _removeViews: LayoutManager._removeViews,

        // Add the ability to remove itself.
        _removeView: LayoutManager._removeView

      // Mix in all LayoutManager prototype properties as well.
      }, LayoutManager.prototype);

      // Extend the options with the prototype and passed options.
      options = view.options = _.defaults(options || {}, view.options,
        proto.options);

      // Ensure view events are properly copied over.
      viewOptions = _.pick(options, aConcat.call(["events"],
        _.values(options.events)));

      // Merge the View options into the View.
      _.extend(view, viewOptions);

      // If the View still has the Backbone.View#render method, remove it.  Don't
      // want it accidentally overriding the LM render.
      if (viewOverrides.render === LayoutManager.prototype.render ||
        viewOverrides.render === Backbone.View.prototype.render) {
        delete viewOverrides.render;
      }

      // Pick out the specific properties that can be dynamically added at
      // runtime and ensure they are available on the view object.
      _.extend(options, viewOverrides);

      // By default the original Remove function is the Backbone.View one.
      view._remove = Backbone.View.prototype.remove;

      // Always use this render function when using LayoutManager.
      view._render = function(manage, options) {
        // Keep the view consistent between callbacks and deferreds.
        var view = this;
        // Shorthand the manager.
        var manager = view.__manager__;
        // Cache these properties.
        var beforeRender = options.beforeRender;

        // Ensure all nested Views are properly scrubbed if re-rendering.
        if (manager.hasRendered) {
          this._removeViews();
        }

        // If a beforeRender function is defined, call it.
        if (beforeRender) {
          beforeRender.call(this, this);
        }

        // Always emit a beforeRender event.
        this.trigger("beforeRender", this);

        // Render!
        return manage(this, options).render();
      };

      // Ensure the render is always set correctly.
      view.render = LayoutManager.prototype.render;

      // If the user provided their own remove override, use that instead of the
      // default.
      if (view.remove !== proto.remove) {
        view._remove = view.remove;
        view.remove = proto.remove;
      }
      
      // Normalize views to exist on either instance or options, default to
      // options.
      views = options.views || view.views;

      // Set the internal views, only if selectors have been provided.
      if (_.keys(views).length) {
        // Keep original object declared containing Views.
        declaredViews = views;

        // Reset the property to avoid duplication or overwritting.
        view.views = {};

        // Set the declared Views.
        view.setViews(declaredViews);
      }

      // If a template is passed use that instead.
      if (view.options.template) {
        view.options.template = options.template;
      // Ensure the template is mapped over.
      } else if (view.template) {
        options.template = view.template;

        // Remove it from the instance.
        delete view.template;
      }
    });
  }
});

// Convenience assignment to make creating Layout's slightly shorter.
Backbone.Layout = LayoutManager;
// Tack on the version.
LayoutManager.VERSION = "0.8.1";

// Override _configure to provide extra functionality that is necessary in
// order for the render function reference to be bound during initialize.
Backbone.View.prototype._configure = function(options) {
  var noel, retVal;

  // Remove the container element provided by Backbone.
  if ("el" in options ? options.el === false : this.el === false) {
    noel = true;
  }

  // Run the original _configure.
  retVal = _configure.apply(this, arguments);

  // If manage is set, do it!
  if (options.manage || this.manage) {
    // Set up this View.
    LayoutManager.setupView(this);
  }

  // Assign the `noel` property once we're sure the View we're working with is
  // mangaed by LayoutManager.
  if (this.__manager__) {
    this.__manager__.noel = noel;
  }

  // Act like nothing happened.
  return retVal;
};

// Default configuration options; designed to be overriden.
LayoutManager.prototype.options = {
  // Prefix template/layout paths.
  prefix: "",

  // Can be used to supply a different deferred implementation.
  deferred: function() {
    return $.Deferred();
  },

  // Fetch is passed a path and is expected to return template contents as a
  // function or string.
  fetch: function(path) {
    return _.template($(path).html());
  },

  // This is the most common way you will want to partially apply a view into
  // a layout.
  partial: function(root, name, $el, insert) {
    // If no selector is specified, assume the parent should be added to.
    var $root = name ? $(root).find(name) : $(root);

    // Use the insert method if insert argument is true.
    if (insert) {
      this.insert($root, $el);
    } else {
      this.html($root, $el);
    }
  },

  // Override this with a custom HTML method, passed a root element and content
  // (a jQuery collection or a string) to replace the innerHTML with.
  html: function($root, content) {
    $root.html(content);
  },

  // Very similar to HTML except this one will appendChild by default.
  insert: function($root, $el) {
    $root.append($el);
  },

  // Return a deferred for when all promises resolve/reject.
  when: function(promises) {
    return $.when.apply(null, promises);
  },

  // By default, render using underscore's templating.
  render: function(template, context) {
    return template(context);
  },

  // A method to determine if a View contains another.
  contains: function(parent, child) {
    return $.contains(parent, child);
  }
};

// Maintain a list of the keys at define time.
keys = _.keys(LayoutManager.prototype.options);

})(typeof global === "object" ? global : this);

define("layoutmanager", function(){});

/*!
 * jQuery Validation Plugin v1.13.1
 *
 * http://jqueryvalidation.org/
 *
 * Copyright (c) 2014 Jörn Zaefferer
 * Released under the MIT license
 */
(function( factory ) {
	if ( typeof define === "function" && define.amd ) {
		define( 'form_field_validator',["jquery"], factory );
	} else {
		factory( jQuery );
	}
}(function( $ ) {

$.extend($.fn, {
	// http://jqueryvalidation.org/validate/
	validate: function( options ) {

		// if nothing is selected, return nothing; can't chain anyway
		if ( !this.length ) {
			if ( options && options.debug && window.console ) {
				console.warn( "Nothing selected, can't validate, returning nothing." );
			}
			return;
		}

		// check if a validator for this form was already created
		var validator = $.data( this[ 0 ], "validator" );
		if ( validator ) {
			return validator;
		}

		// Add novalidate tag if HTML5.
		this.attr( "novalidate", "novalidate" );

		validator = new $.validator( options, this[ 0 ] );
		$.data( this[ 0 ], "validator", validator );

		if ( validator.settings.onsubmit ) {

			this.validateDelegate( ":submit", "click", function( event ) {
				if ( validator.settings.submitHandler ) {
					validator.submitButton = event.target;
				}
				// allow suppressing validation by adding a cancel class to the submit button
				if ( $( event.target ).hasClass( "cancel" ) ) {
					validator.cancelSubmit = true;
				}

				// allow suppressing validation by adding the html5 formnovalidate attribute to the submit button
				if ( $( event.target ).attr( "formnovalidate" ) !== undefined ) {
					validator.cancelSubmit = true;
				}
			});

			// validate the form on submit
			this.submit( function( event ) {
				if ( validator.settings.debug ) {
					// prevent form submit to be able to see console output
					event.preventDefault();
				}
				function handle() {
					var hidden, result;
					if ( validator.settings.submitHandler ) {
						if ( validator.submitButton ) {
							// insert a hidden input as a replacement for the missing submit button
							hidden = $( "<input type='hidden'/>" )
								.attr( "name", validator.submitButton.name )
								.val( $( validator.submitButton ).val() )
								.appendTo( validator.currentForm );
						}
						result = validator.settings.submitHandler.call( validator, validator.currentForm, event );
						if ( validator.submitButton ) {
							// and clean up afterwards; thanks to no-block-scope, hidden can be referenced
							hidden.remove();
						}
						if ( result !== undefined ) {
							return result;
						}
						return false;
					}
					return true;
				}

				// prevent submit for invalid forms or custom submit handlers
				if ( validator.cancelSubmit ) {
					validator.cancelSubmit = false;
					return handle();
				}
				if ( validator.form() ) {
					if ( validator.pendingRequest ) {
						validator.formSubmitted = true;
						return false;
					}
					return handle();
				} else {
					validator.focusInvalid();
					return false;
				}
			});
		}

		return validator;
	},
	// http://jqueryvalidation.org/valid/
	valid: function() {
		var valid, validator;

		if ( $( this[ 0 ] ).is( "form" ) ) {
			valid = this.validate().form();
		} else {
			valid = true;
			validator = $( this[ 0 ].form ).validate();
			this.each( function() {
				valid = validator.element( this ) && valid;
			});
		}
		return valid;
	},
	// attributes: space separated list of attributes to retrieve and remove
	removeAttrs: function( attributes ) {
		var result = {},
			$element = this;
		$.each( attributes.split( /\s/ ), function( index, value ) {
			result[ value ] = $element.attr( value );
			$element.removeAttr( value );
		});
		return result;
	},
	// http://jqueryvalidation.org/rules/
	rules: function( command, argument ) {
		var element = this[ 0 ],
			settings, staticRules, existingRules, data, param, filtered;

		if ( command ) {
			settings = $.data( element.form, "validator" ).settings;
			staticRules = settings.rules;
			existingRules = $.validator.staticRules( element );
			switch ( command ) {
			case "add":
				$.extend( existingRules, $.validator.normalizeRule( argument ) );
				// remove messages from rules, but allow them to be set separately
				delete existingRules.messages;
				staticRules[ element.name ] = existingRules;
				if ( argument.messages ) {
					settings.messages[ element.name ] = $.extend( settings.messages[ element.name ], argument.messages );
				}
				break;
			case "remove":
				if ( !argument ) {
					delete staticRules[ element.name ];
					return existingRules;
				}
				filtered = {};
				$.each( argument.split( /\s/ ), function( index, method ) {
					filtered[ method ] = existingRules[ method ];
					delete existingRules[ method ];
					if ( method === "required" ) {
						$( element ).removeAttr( "aria-required" );
					}
				});
				return filtered;
			}
		}

		data = $.validator.normalizeRules(
		$.extend(
			{},
			$.validator.classRules( element ),
			$.validator.attributeRules( element ),
			$.validator.dataRules( element ),
			$.validator.staticRules( element )
		), element );

		// make sure required is at front
		if ( data.required ) {
			param = data.required;
			delete data.required;
			data = $.extend( { required: param }, data );
			$( element ).attr( "aria-required", "true" );
		}

		// make sure remote is at back
		if ( data.remote ) {
			param = data.remote;
			delete data.remote;
			data = $.extend( data, { remote: param });
		}

		return data;
	}
});

// Custom selectors
$.extend( $.expr[ ":" ], {
	// http://jqueryvalidation.org/blank-selector/
	blank: function( a ) {
		return !$.trim( "" + $( a ).val() );
	},
	// http://jqueryvalidation.org/filled-selector/
	filled: function( a ) {
		return !!$.trim( "" + $( a ).val() );
	},
	// http://jqueryvalidation.org/unchecked-selector/
	unchecked: function( a ) {
		return !$( a ).prop( "checked" );
	}
});

// constructor for validator
$.validator = function( options, form ) {
	this.settings = $.extend( true, {}, $.validator.defaults, options );
	this.currentForm = form;
	this.init();
};

// http://jqueryvalidation.org/jQuery.validator.format/
$.validator.format = function( source, params ) {
	if ( arguments.length === 1 ) {
		return function() {
			var args = $.makeArray( arguments );
			args.unshift( source );
			return $.validator.format.apply( this, args );
		};
	}
	if ( arguments.length > 2 && params.constructor !== Array  ) {
		params = $.makeArray( arguments ).slice( 1 );
	}
	if ( params.constructor !== Array ) {
		params = [ params ];
	}
	$.each( params, function( i, n ) {
		source = source.replace( new RegExp( "\\{" + i + "\\}", "g" ), function() {
			return n;
		});
	});
	return source;
};

$.extend( $.validator, {

	defaults: {
		messages: {},
		groups: {},
		rules: {},
		errorClass: "error",
		validClass: "valid",
		errorElement: "label",
		focusCleanup: false,
		focusInvalid: true,
		errorContainer: $( [] ),
		errorLabelContainer: $( [] ),
		onsubmit: true,
		ignore: ":hidden",
		ignoreTitle: false,
		onfocusin: function( element ) {
			this.lastActive = element;

			// Hide error label and remove error class on focus if enabled
			if ( this.settings.focusCleanup ) {
				if ( this.settings.unhighlight ) {
					this.settings.unhighlight.call( this, element, this.settings.errorClass, this.settings.validClass );
				}
				this.hideThese( this.errorsFor( element ) );
			}
		},
		onfocusout: function( element ) {
			if ( !this.checkable( element ) && ( element.name in this.submitted || !this.optional( element ) ) ) {
				this.element( element );
			}
		},
		onkeyup: function( element, event ) {
			if ( event.which === 9 && this.elementValue( element ) === "" ) {
				return;
			} else if ( element.name in this.submitted || element === this.lastElement ) {
				this.element( element );
			}
		},
		onclick: function( element ) {
			// click on selects, radiobuttons and checkboxes
			if ( element.name in this.submitted ) {
				this.element( element );

			// or option elements, check parent select in that case
			} else if ( element.parentNode.name in this.submitted ) {
				this.element( element.parentNode );
			}
		},
		highlight: function( element, errorClass, validClass ) {
			if ( element.type === "radio" ) {
				this.findByName( element.name ).addClass( errorClass ).removeClass( validClass );
			} else {
				$( element ).addClass( errorClass ).removeClass( validClass );
			}
		},
		unhighlight: function( element, errorClass, validClass ) {
			if ( element.type === "radio" ) {
				this.findByName( element.name ).removeClass( errorClass ).addClass( validClass );
			} else {
				$( element ).removeClass( errorClass ).addClass( validClass );
			}
		}
	},

	// http://jqueryvalidation.org/jQuery.validator.setDefaults/
	setDefaults: function( settings ) {
		$.extend( $.validator.defaults, settings );
	},

	messages: {
		required: "This field is required.",
		remote: "Please fix this field.",
		email: "Please enter a valid email address.",
		url: "Please enter a valid URL.",
		date: "Please enter a valid date.",
		dateISO: "Please enter a valid date ( ISO ).",
		number: "Please enter a valid number.",
		digits: "Please enter only digits.",
		creditcard: "Please enter a valid credit card number.",
		equalTo: "Please enter the same value again.",
		maxlength: $.validator.format( "Please enter no more than {0} characters." ),
		minlength: $.validator.format( "Please enter at least {0} characters." ),
		rangelength: $.validator.format( "Please enter a value between {0} and {1} characters long." ),
		range: $.validator.format( "Please enter a value between {0} and {1}." ),
		max: $.validator.format( "Please enter a value less than or equal to {0}." ),
		min: $.validator.format( "Please enter a value greater than or equal to {0}." )
	},

	autoCreateRanges: false,

	prototype: {

		init: function() {
			this.labelContainer = $( this.settings.errorLabelContainer );
			this.errorContext = this.labelContainer.length && this.labelContainer || $( this.currentForm );
			this.containers = $( this.settings.errorContainer ).add( this.settings.errorLabelContainer );
			this.submitted = {};
			this.valueCache = {};
			this.pendingRequest = 0;
			this.pending = {};
			this.invalid = {};
			this.reset();

			var groups = ( this.groups = {} ),
				rules;
			$.each( this.settings.groups, function( key, value ) {
				if ( typeof value === "string" ) {
					value = value.split( /\s/ );
				}
				$.each( value, function( index, name ) {
					groups[ name ] = key;
				});
			});
			rules = this.settings.rules;
			$.each( rules, function( key, value ) {
				rules[ key ] = $.validator.normalizeRule( value );
			});

			function delegate( event ) {
				var validator = $.data( this[ 0 ].form, "validator" ),
					eventType = "on" + event.type.replace( /^validate/, "" ),
					settings = validator.settings;
				if ( settings[ eventType ] && !this.is( settings.ignore ) ) {
					settings[ eventType ].call( validator, this[ 0 ], event );
				}
			}
			$( this.currentForm )
				.validateDelegate( ":text, [type='password'], [type='file'], select, textarea, " +
					"[type='number'], [type='search'] ,[type='tel'], [type='url'], " +
					"[type='email'], [type='datetime'], [type='date'], [type='month'], " +
					"[type='week'], [type='time'], [type='datetime-local'], " +
					"[type='range'], [type='color'], [type='radio'], [type='checkbox']",
					"focusin focusout keyup", delegate)
				// Support: Chrome, oldIE
				// "select" is provided as event.target when clicking a option
				.validateDelegate("select, option, [type='radio'], [type='checkbox']", "click", delegate);

			if ( this.settings.invalidHandler ) {
				$( this.currentForm ).bind( "invalid-form.validate", this.settings.invalidHandler );
			}

			// Add aria-required to any Static/Data/Class required fields before first validation
			// Screen readers require this attribute to be present before the initial submission http://www.w3.org/TR/WCAG-TECHS/ARIA2.html
			$( this.currentForm ).find( "[required], [data-rule-required], .required" ).attr( "aria-required", "true" );
		},

		// http://jqueryvalidation.org/Validator.form/
		form: function() {
			this.checkForm();
			$.extend( this.submitted, this.errorMap );
			this.invalid = $.extend({}, this.errorMap );
			if ( !this.valid() ) {
				$( this.currentForm ).triggerHandler( "invalid-form", [ this ]);
			}
			this.showErrors();
			return this.valid();
		},

		checkForm: function() {
			this.prepareForm();
			for ( var i = 0, elements = ( this.currentElements = this.elements() ); elements[ i ]; i++ ) {
				this.check( elements[ i ] );
			}
			return this.valid();
		},

		// http://jqueryvalidation.org/Validator.element/
		element: function( element ) {
			var cleanElement = this.clean( element ),
				checkElement = this.validationTargetFor( cleanElement ),
				result = true;

			this.lastElement = checkElement;

			if ( checkElement === undefined ) {
				delete this.invalid[ cleanElement.name ];
			} else {
				this.prepareElement( checkElement );
				this.currentElements = $( checkElement );

				result = this.check( checkElement ) !== false;
				if ( result ) {
					delete this.invalid[ checkElement.name ];
				} else {
					this.invalid[ checkElement.name ] = true;
				}
			}
			// Add aria-invalid status for screen readers
			$( element ).attr( "aria-invalid", !result );

			if ( !this.numberOfInvalids() ) {
				// Hide error containers on last error
				this.toHide = this.toHide.add( this.containers );
			}
			this.showErrors();
			return result;
		},

		// http://jqueryvalidation.org/Validator.showErrors/
		showErrors: function( errors ) {
			if ( errors ) {
				// add items to error list and map
				$.extend( this.errorMap, errors );
				this.errorList = [];
				for ( var name in errors ) {
					this.errorList.push({
						message: errors[ name ],
						element: this.findByName( name )[ 0 ]
					});
				}
				// remove items from success list
				this.successList = $.grep( this.successList, function( element ) {
					return !( element.name in errors );
				});
			}
			if ( this.settings.showErrors ) {
				this.settings.showErrors.call( this, this.errorMap, this.errorList );
			} else {
				this.defaultShowErrors();
			}
		},

		// http://jqueryvalidation.org/Validator.resetForm/
		resetForm: function() {
			if ( $.fn.resetForm ) {
				$( this.currentForm ).resetForm();
			}
			this.submitted = {};
			this.lastElement = null;
			this.prepareForm();
			this.hideErrors();
			this.elements()
					.removeClass( this.settings.errorClass )
					.removeData( "previousValue" )
					.removeAttr( "aria-invalid" );
		},

		numberOfInvalids: function() {
			return this.objectLength( this.invalid );
		},

		objectLength: function( obj ) {
			/* jshint unused: false */
			var count = 0,
				i;
			for ( i in obj ) {
				count++;
			}
			return count;
		},

		hideErrors: function() {
			this.hideThese( this.toHide );
		},

		hideThese: function( errors ) {
			errors.not( this.containers ).text( "" );
			this.addWrapper( errors ).hide();
		},

		valid: function() {
			return this.size() === 0;
		},

		size: function() {
			return this.errorList.length;
		},

		focusInvalid: function() {
			if ( this.settings.focusInvalid ) {
				try {
					$( this.findLastActive() || this.errorList.length && this.errorList[ 0 ].element || [])
					.filter( ":visible" )
					.focus()
					// manually trigger focusin event; without it, focusin handler isn't called, findLastActive won't have anything to find
					.trigger( "focusin" );
				} catch ( e ) {
					// ignore IE throwing errors when focusing hidden elements
				}
			}
		},

		findLastActive: function() {
			var lastActive = this.lastActive;
			return lastActive && $.grep( this.errorList, function( n ) {
				return n.element.name === lastActive.name;
			}).length === 1 && lastActive;
		},

		elements: function() {
			var validator = this,
				rulesCache = {};

			// select all valid inputs inside the form (no submit or reset buttons)
			return $( this.currentForm )
			.find( "input, select, textarea" )
			.not( ":submit, :reset, :image, [disabled], [readonly]" )
			.not( this.settings.ignore )
			.filter( function() {
				if ( !this.name && validator.settings.debug && window.console ) {
					console.error( "%o has no name assigned", this );
				}

				// select only the first element for each name, and only those with rules specified
				if ( this.name in rulesCache || !validator.objectLength( $( this ).rules() ) ) {
					return false;
				}

				rulesCache[ this.name ] = true;
				return true;
			});
		},

		clean: function( selector ) {
			return $( selector )[ 0 ];
		},

		errors: function() {
			var errorClass = this.settings.errorClass.split( " " ).join( "." );
			return $( this.settings.errorElement + "." + errorClass, this.errorContext );
		},

		reset: function() {
			this.successList = [];
			this.errorList = [];
			this.errorMap = {};
			this.toShow = $( [] );
			this.toHide = $( [] );
			this.currentElements = $( [] );
		},

		prepareForm: function() {
			this.reset();
			this.toHide = this.errors().add( this.containers );
		},

		prepareElement: function( element ) {
			this.reset();
			this.toHide = this.errorsFor( element );
		},

		elementValue: function( element ) {
			var val,
				$element = $( element ),
				type = element.type;

			if ( type === "radio" || type === "checkbox" ) {
				return $( "input[name='" + element.name + "']:checked" ).val();
			} else if ( type === "number" && typeof element.validity !== "undefined" ) {
				return element.validity.badInput ? false : $element.val();
			}

			val = $element.val();
			if ( typeof val === "string" ) {
				return val.replace(/\r/g, "" );
			}
			return val;
		},

		check: function( element ) {
			element = this.validationTargetFor( this.clean( element ) );

			var rules = $( element ).rules(),
				rulesCount = $.map( rules, function( n, i ) {
					return i;
				}).length,
				dependencyMismatch = false,
				val = this.elementValue( element ),
				result, method, rule;

			for ( method in rules ) {
				rule = { method: method, parameters: rules[ method ] };
				try {

					result = $.validator.methods[ method ].call( this, val, element, rule.parameters );

					// if a method indicates that the field is optional and therefore valid,
					// don't mark it as valid when there are no other rules
					if ( result === "dependency-mismatch" && rulesCount === 1 ) {
						dependencyMismatch = true;
						continue;
					}
					dependencyMismatch = false;

					if ( result === "pending" ) {
						this.toHide = this.toHide.not( this.errorsFor( element ) );
						return;
					}

					if ( !result ) {
						this.formatAndAdd( element, rule );
						return false;
					}
				} catch ( e ) {
					if ( this.settings.debug && window.console ) {
						console.log( "Exception occurred when checking element " + element.id + ", check the '" + rule.method + "' method.", e );
					}
					throw e;
				}
			}
			if ( dependencyMismatch ) {
				return;
			}
			if ( this.objectLength( rules ) ) {
				this.successList.push( element );
			}
			return true;
		},

		// return the custom message for the given element and validation method
		// specified in the element's HTML5 data attribute
		// return the generic message if present and no method specific message is present
		customDataMessage: function( element, method ) {
			return $( element ).data( "msg" + method.charAt( 0 ).toUpperCase() +
				method.substring( 1 ).toLowerCase() ) || $( element ).data( "msg" );
		},

		// return the custom message for the given element name and validation method
		customMessage: function( name, method ) {
			var m = this.settings.messages[ name ];
			return m && ( m.constructor === String ? m : m[ method ]);
		},

		// return the first defined argument, allowing empty strings
		findDefined: function() {
			for ( var i = 0; i < arguments.length; i++) {
				if ( arguments[ i ] !== undefined ) {
					return arguments[ i ];
				}
			}
			return undefined;
		},

		defaultMessage: function( element, method ) {
			return this.findDefined(
				this.customMessage( element.name, method ),
				this.customDataMessage( element, method ),
				// title is never undefined, so handle empty string as undefined
				!this.settings.ignoreTitle && element.title || undefined,
				$.validator.messages[ method ],
				"<strong>Warning: No message defined for " + element.name + "</strong>"
			);
		},

		formatAndAdd: function( element, rule ) {
			var message = this.defaultMessage( element, rule.method ),
				theregex = /\$?\{(\d+)\}/g;
			if ( typeof message === "function" ) {
				message = message.call( this, rule.parameters, element );
			} else if ( theregex.test( message ) ) {
				message = $.validator.format( message.replace( theregex, "{$1}" ), rule.parameters );
			}
			this.errorList.push({
				message: message,
				element: element,
				method: rule.method
			});

			this.errorMap[ element.name ] = message;
			this.submitted[ element.name ] = message;
		},

		addWrapper: function( toToggle ) {
			if ( this.settings.wrapper ) {
				toToggle = toToggle.add( toToggle.parent( this.settings.wrapper ) );
			}
			return toToggle;
		},

		defaultShowErrors: function() {
			var i, elements, error;
			for ( i = 0; this.errorList[ i ]; i++ ) {
				error = this.errorList[ i ];
				if ( this.settings.highlight ) {
					this.settings.highlight.call( this, error.element, this.settings.errorClass, this.settings.validClass );
				}
				this.showLabel( error.element, error.message );
			}
			if ( this.errorList.length ) {
				this.toShow = this.toShow.add( this.containers );
			}
			if ( this.settings.success ) {
				for ( i = 0; this.successList[ i ]; i++ ) {
					this.showLabel( this.successList[ i ] );
				}
			}
			if ( this.settings.unhighlight ) {
				for ( i = 0, elements = this.validElements(); elements[ i ]; i++ ) {
					this.settings.unhighlight.call( this, elements[ i ], this.settings.errorClass, this.settings.validClass );
				}
			}
			this.toHide = this.toHide.not( this.toShow );
			this.hideErrors();
			this.addWrapper( this.toShow ).show();
		},

		validElements: function() {
			return this.currentElements.not( this.invalidElements() );
		},

		invalidElements: function() {
			return $( this.errorList ).map(function() {
				return this.element;
			});
		},

		showLabel: function( element, message ) {
			var place, group, errorID,
				error = this.errorsFor( element ),
				elementID = this.idOrName( element ),
				describedBy = $( element ).attr( "aria-describedby" );
			if ( error.length ) {
				// refresh error/success class
				error.removeClass( this.settings.validClass ).addClass( this.settings.errorClass );
				// replace message on existing label
				error.html( message );
			} else {
				// create error element
				error = $( "<" + this.settings.errorElement + ">" )
					.attr( "id", elementID + "-error" )
					.addClass( this.settings.errorClass )
					.html( message || "" );

				// Maintain reference to the element to be placed into the DOM
				place = error;
				if ( this.settings.wrapper ) {
					// make sure the element is visible, even in IE
					// actually showing the wrapped element is handled elsewhere
					place = error.hide().show().wrap( "<" + this.settings.wrapper + "/>" ).parent();
				}
				if ( this.labelContainer.length ) {
					this.labelContainer.append( place );
				} else if ( this.settings.errorPlacement ) {
					this.settings.errorPlacement( place, $( element ) );
				} else {
					place.insertAfter( element );
				}

				// Link error back to the element
				if ( error.is( "label" ) ) {
					// If the error is a label, then associate using 'for'
					error.attr( "for", elementID );
				} else if ( error.parents( "label[for='" + elementID + "']" ).length === 0 ) {
					// If the element is not a child of an associated label, then it's necessary
					// to explicitly apply aria-describedby

					errorID = error.attr( "id" ).replace( /(:|\.|\[|\])/g, "\\$1");
					// Respect existing non-error aria-describedby
					if ( !describedBy ) {
						describedBy = errorID;
					} else if ( !describedBy.match( new RegExp( "\\b" + errorID + "\\b" ) ) ) {
						// Add to end of list if not already present
						describedBy += " " + errorID;
					}
					$( element ).attr( "aria-describedby", describedBy );

					// If this element is grouped, then assign to all elements in the same group
					group = this.groups[ element.name ];
					if ( group ) {
						$.each( this.groups, function( name, testgroup ) {
							if ( testgroup === group ) {
								$( "[name='" + name + "']", this.currentForm )
									.attr( "aria-describedby", error.attr( "id" ) );
							}
						});
					}
				}
			}
			if ( !message && this.settings.success ) {
				error.text( "" );
				if ( typeof this.settings.success === "string" ) {
					error.addClass( this.settings.success );
				} else {
					this.settings.success( error, element );
				}
			}
			this.toShow = this.toShow.add( error );
		},

		errorsFor: function( element ) {
			var name = this.idOrName( element ),
				describer = $( element ).attr( "aria-describedby" ),
				selector = "label[for='" + name + "'], label[for='" + name + "'] *";

			// aria-describedby should directly reference the error element
			if ( describer ) {
				selector = selector + ", #" + describer.replace( /\s+/g, ", #" );
			}
			return this
				.errors()
				.filter( selector );
		},

		idOrName: function( element ) {
			return this.groups[ element.name ] || ( this.checkable( element ) ? element.name : element.id || element.name );
		},

		validationTargetFor: function( element ) {

			// If radio/checkbox, validate first element in group instead
			if ( this.checkable( element ) ) {
				element = this.findByName( element.name );
			}

			// Always apply ignore filter
			return $( element ).not( this.settings.ignore )[ 0 ];
		},

		checkable: function( element ) {
			return ( /radio|checkbox/i ).test( element.type );
		},

		findByName: function( name ) {
			return $( this.currentForm ).find( "[name='" + name + "']" );
		},

		getLength: function( value, element ) {
			switch ( element.nodeName.toLowerCase() ) {
			case "select":
				return $( "option:selected", element ).length;
			case "input":
				if ( this.checkable( element ) ) {
					return this.findByName( element.name ).filter( ":checked" ).length;
				}
			}
			return value.length;
		},

		depend: function( param, element ) {
			return this.dependTypes[typeof param] ? this.dependTypes[typeof param]( param, element ) : true;
		},

		dependTypes: {
			"boolean": function( param ) {
				return param;
			},
			"string": function( param, element ) {
				return !!$( param, element.form ).length;
			},
			"function": function( param, element ) {
				return param( element );
			}
		},

		optional: function( element ) {
			var val = this.elementValue( element );
			return !$.validator.methods.required.call( this, val, element ) && "dependency-mismatch";
		},

		startRequest: function( element ) {
			if ( !this.pending[ element.name ] ) {
				this.pendingRequest++;
				this.pending[ element.name ] = true;
			}
		},

		stopRequest: function( element, valid ) {
			this.pendingRequest--;
			// sometimes synchronization fails, make sure pendingRequest is never < 0
			if ( this.pendingRequest < 0 ) {
				this.pendingRequest = 0;
			}
			delete this.pending[ element.name ];
			if ( valid && this.pendingRequest === 0 && this.formSubmitted && this.form() ) {
				$( this.currentForm ).submit();
				this.formSubmitted = false;
			} else if (!valid && this.pendingRequest === 0 && this.formSubmitted ) {
				$( this.currentForm ).triggerHandler( "invalid-form", [ this ]);
				this.formSubmitted = false;
			}
		},

		previousValue: function( element ) {
			return $.data( element, "previousValue" ) || $.data( element, "previousValue", {
				old: null,
				valid: true,
				message: this.defaultMessage( element, "remote" )
			});
		}

	},

	classRuleSettings: {
		required: { required: true },
		email: { email: true },
		url: { url: true },
		date: { date: true },
		dateISO: { dateISO: true },
		number: { number: true },
		digits: { digits: true },
		creditcard: { creditcard: true }
	},

	addClassRules: function( className, rules ) {
		if ( className.constructor === String ) {
			this.classRuleSettings[ className ] = rules;
		} else {
			$.extend( this.classRuleSettings, className );
		}
	},

	classRules: function( element ) {
		var rules = {},
			classes = $( element ).attr( "class" );

		if ( classes ) {
			$.each( classes.split( " " ), function() {
				if ( this in $.validator.classRuleSettings ) {
					$.extend( rules, $.validator.classRuleSettings[ this ]);
				}
			});
		}
		return rules;
	},

	attributeRules: function( element ) {
		var rules = {},
			$element = $( element ),
			type = element.getAttribute( "type" ),
			method, value;

		for ( method in $.validator.methods ) {

			// support for <input required> in both html5 and older browsers
			if ( method === "required" ) {
				value = element.getAttribute( method );
				// Some browsers return an empty string for the required attribute
				// and non-HTML5 browsers might have required="" markup
				if ( value === "" ) {
					value = true;
				}
				// force non-HTML5 browsers to return bool
				value = !!value;
			} else {
				value = $element.attr( method );
			}

			// convert the value to a number for number inputs, and for text for backwards compability
			// allows type="date" and others to be compared as strings
			if ( /min|max/.test( method ) && ( type === null || /number|range|text/.test( type ) ) ) {
				value = Number( value );
			}

			if ( value || value === 0 ) {
				rules[ method ] = value;
			} else if ( type === method && type !== "range" ) {
				// exception: the jquery validate 'range' method
				// does not test for the html5 'range' type
				rules[ method ] = true;
			}
		}

		// maxlength may be returned as -1, 2147483647 ( IE ) and 524288 ( safari ) for text inputs
		if ( rules.maxlength && /-1|2147483647|524288/.test( rules.maxlength ) ) {
			delete rules.maxlength;
		}

		return rules;
	},

	dataRules: function( element ) {
		var method, value,
			rules = {}, $element = $( element );
		for ( method in $.validator.methods ) {
			value = $element.data( "rule" + method.charAt( 0 ).toUpperCase() + method.substring( 1 ).toLowerCase() );
			if ( value !== undefined ) {
				rules[ method ] = value;
			}
		}
		return rules;
	},

	staticRules: function( element ) {
		var rules = {},
			validator = $.data( element.form, "validator" );

		if ( validator.settings.rules ) {
			rules = $.validator.normalizeRule( validator.settings.rules[ element.name ] ) || {};
		}
		return rules;
	},

	normalizeRules: function( rules, element ) {
		// handle dependency check
		$.each( rules, function( prop, val ) {
			// ignore rule when param is explicitly false, eg. required:false
			if ( val === false ) {
				delete rules[ prop ];
				return;
			}
			if ( val.param || val.depends ) {
				var keepRule = true;
				switch ( typeof val.depends ) {
				case "string":
					keepRule = !!$( val.depends, element.form ).length;
					break;
				case "function":
					keepRule = val.depends.call( element, element );
					break;
				}
				if ( keepRule ) {
					rules[ prop ] = val.param !== undefined ? val.param : true;
				} else {
					delete rules[ prop ];
				}
			}
		});

		// evaluate parameters
		$.each( rules, function( rule, parameter ) {
			rules[ rule ] = $.isFunction( parameter ) ? parameter( element ) : parameter;
		});

		// clean number parameters
		$.each([ "minlength", "maxlength" ], function() {
			if ( rules[ this ] ) {
				rules[ this ] = Number( rules[ this ] );
			}
		});
		$.each([ "rangelength", "range" ], function() {
			var parts;
			if ( rules[ this ] ) {
				if ( $.isArray( rules[ this ] ) ) {
					rules[ this ] = [ Number( rules[ this ][ 0 ]), Number( rules[ this ][ 1 ] ) ];
				} else if ( typeof rules[ this ] === "string" ) {
					parts = rules[ this ].replace(/[\[\]]/g, "" ).split( /[\s,]+/ );
					rules[ this ] = [ Number( parts[ 0 ]), Number( parts[ 1 ] ) ];
				}
			}
		});

		if ( $.validator.autoCreateRanges ) {
			// auto-create ranges
			if ( rules.min != null && rules.max != null ) {
				rules.range = [ rules.min, rules.max ];
				delete rules.min;
				delete rules.max;
			}
			if ( rules.minlength != null && rules.maxlength != null ) {
				rules.rangelength = [ rules.minlength, rules.maxlength ];
				delete rules.minlength;
				delete rules.maxlength;
			}
		}

		return rules;
	},

	// Converts a simple string to a {string: true} rule, e.g., "required" to {required:true}
	normalizeRule: function( data ) {
		if ( typeof data === "string" ) {
			var transformed = {};
			$.each( data.split( /\s/ ), function() {
				transformed[ this ] = true;
			});
			data = transformed;
		}
		return data;
	},

	// http://jqueryvalidation.org/jQuery.validator.addMethod/
	addMethod: function( name, method, message ) {
		$.validator.methods[ name ] = method;
		$.validator.messages[ name ] = message !== undefined ? message : $.validator.messages[ name ];
		if ( method.length < 3 ) {
			$.validator.addClassRules( name, $.validator.normalizeRule( name ) );
		}
	},

	methods: {

		// http://jqueryvalidation.org/required-method/
		required: function( value, element, param ) {
			// check if dependency is met
			if ( !this.depend( param, element ) ) {
				return "dependency-mismatch";
			}
			if ( element.nodeName.toLowerCase() === "select" ) {
				// could be an array for select-multiple or a string, both are fine this way
				var val = $( element ).val();
				return val && val.length > 0;
			}
			if ( this.checkable( element ) ) {
				return this.getLength( value, element ) > 0;
			}
			return $.trim( value ).length > 0;
		},

		// http://jqueryvalidation.org/email-method/
		email: function( value, element ) {
			// From http://www.whatwg.org/specs/web-apps/current-work/multipage/states-of-the-type-attribute.html#e-mail-state-%28type=email%29
			// Retrieved 2014-01-14
			// If you have a problem with this implementation, report a bug against the above spec
			// Or use custom methods to implement your own email validation
			return this.optional( element ) || /^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/.test( value );
		},

		// http://jqueryvalidation.org/url-method/
		url: function( value, element ) {
			// contributed by Scott Gonzalez: http://projects.scottsplayground.com/iri/
			return this.optional( element ) || /^(https?|s?ftp):\/\/(((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:)*@)?(((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?)(:\d*)?)(\/((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)+(\/(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*)?)?(\?((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|[\uE000-\uF8FF]|\/|\?)*)?(#((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|\/|\?)*)?$/i.test( value );
		},

		// http://jqueryvalidation.org/date-method/
		date: function( value, element ) {
			return this.optional( element ) || !/Invalid|NaN/.test( new Date( value ).toString() );
		},

		// http://jqueryvalidation.org/dateISO-method/
		dateISO: function( value, element ) {
			return this.optional( element ) || /^\d{4}[\/\-](0?[1-9]|1[012])[\/\-](0?[1-9]|[12][0-9]|3[01])$/.test( value );
		},

		// http://jqueryvalidation.org/number-method/
		number: function( value, element ) {
			return this.optional( element ) || /^-?(?:\d+|\d{1,3}(?:,\d{3})+)?(?:\.\d+)?$/.test( value );
		},

		// http://jqueryvalidation.org/digits-method/
		digits: function( value, element ) {
			return this.optional( element ) || /^\d+$/.test( value );
		},

		// http://jqueryvalidation.org/creditcard-method/
		// based on http://en.wikipedia.org/wiki/Luhn/
		creditcard: function( value, element ) {
			if ( this.optional( element ) ) {
				return "dependency-mismatch";
			}
			// accept only spaces, digits and dashes
			if ( /[^0-9 \-]+/.test( value ) ) {
				return false;
			}
			var nCheck = 0,
				nDigit = 0,
				bEven = false,
				n, cDigit;

			value = value.replace( /\D/g, "" );

			// Basing min and max length on
			// http://developer.ean.com/general_info/Valid_Credit_Card_Types
			if ( value.length < 13 || value.length > 19 ) {
				return false;
			}

			for ( n = value.length - 1; n >= 0; n--) {
				cDigit = value.charAt( n );
				nDigit = parseInt( cDigit, 10 );
				if ( bEven ) {
					if ( ( nDigit *= 2 ) > 9 ) {
						nDigit -= 9;
					}
				}
				nCheck += nDigit;
				bEven = !bEven;
			}

			return ( nCheck % 10 ) === 0;
		},

		// http://jqueryvalidation.org/minlength-method/
		minlength: function( value, element, param ) {
			var length = $.isArray( value ) ? value.length : this.getLength( value, element );
			return this.optional( element ) || length >= param;
		},

		// http://jqueryvalidation.org/maxlength-method/
		maxlength: function( value, element, param ) {
			var length = $.isArray( value ) ? value.length : this.getLength( value, element );
			return this.optional( element ) || length <= param;
		},

		// http://jqueryvalidation.org/rangelength-method/
		rangelength: function( value, element, param ) {
			var length = $.isArray( value ) ? value.length : this.getLength( value, element );
			return this.optional( element ) || ( length >= param[ 0 ] && length <= param[ 1 ] );
		},

		// http://jqueryvalidation.org/min-method/
		min: function( value, element, param ) {
			return this.optional( element ) || value >= param;
		},

		// http://jqueryvalidation.org/max-method/
		max: function( value, element, param ) {
			return this.optional( element ) || value <= param;
		},

		// http://jqueryvalidation.org/range-method/
		range: function( value, element, param ) {
			return this.optional( element ) || ( value >= param[ 0 ] && value <= param[ 1 ] );
		},

		// http://jqueryvalidation.org/equalTo-method/
		equalTo: function( value, element, param ) {
			// bind to the blur event of the target in order to revalidate whenever the target field is updated
			// TODO find a way to bind the event just once, avoiding the unbind-rebind overhead
			var target = $( param );
			if ( this.settings.onfocusout ) {
				target.unbind( ".validate-equalTo" ).bind( "blur.validate-equalTo", function() {
					$( element ).valid();
				});
			}
			return value === target.val();
		},

		// http://jqueryvalidation.org/remote-method/
		remote: function( value, element, param ) {
			if ( this.optional( element ) ) {
				return "dependency-mismatch";
			}

			var previous = this.previousValue( element ),
				validator, data;

			if (!this.settings.messages[ element.name ] ) {
				this.settings.messages[ element.name ] = {};
			}
			previous.originalMessage = this.settings.messages[ element.name ].remote;
			this.settings.messages[ element.name ].remote = previous.message;

			param = typeof param === "string" && { url: param } || param;

			if ( previous.old === value ) {
				return previous.valid;
			}

			previous.old = value;
			validator = this;
			this.startRequest( element );
			data = {};
			data[ element.name ] = value;
			$.ajax( $.extend( true, {
				url: param,
				mode: "abort",
				port: "validate" + element.name,
				dataType: "json",
				data: data,
				context: validator.currentForm,
				success: function( response ) {
					var valid = response === true || response === "true",
						errors, message, submitted;

					validator.settings.messages[ element.name ].remote = previous.originalMessage;
					if ( valid ) {
						submitted = validator.formSubmitted;
						validator.prepareElement( element );
						validator.formSubmitted = submitted;
						validator.successList.push( element );
						delete validator.invalid[ element.name ];
						validator.showErrors();
					} else {
						errors = {};
						message = response || validator.defaultMessage( element, "remote" );
						errors[ element.name ] = previous.message = $.isFunction( message ) ? message( value ) : message;
						validator.invalid[ element.name ] = true;
						validator.showErrors( errors );
					}
					previous.valid = valid;
					validator.stopRequest( element, valid );
				}
			}, param ) );
			return "pending";
		}

	}

});

$.format = function deprecated() {
	throw "$.format has been deprecated. Please use $.validator.format instead.";
};

// ajax mode: abort
// usage: $.ajax({ mode: "abort"[, port: "uniqueport"]});
// if mode:"abort" is used, the previous request on that port (port can be undefined) is aborted via XMLHttpRequest.abort()

var pendingRequests = {},
	ajax;
// Use a prefilter if available (1.5+)
if ( $.ajaxPrefilter ) {
	$.ajaxPrefilter(function( settings, _, xhr ) {
		var port = settings.port;
		if ( settings.mode === "abort" ) {
			if ( pendingRequests[port] ) {
				pendingRequests[port].abort();
			}
			pendingRequests[port] = xhr;
		}
	});
} else {
	// Proxy ajax
	ajax = $.ajax;
	$.ajax = function( settings ) {
		var mode = ( "mode" in settings ? settings : $.ajaxSettings ).mode,
			port = ( "port" in settings ? settings : $.ajaxSettings ).port;
		if ( mode === "abort" ) {
			if ( pendingRequests[port] ) {
				pendingRequests[port].abort();
			}
			pendingRequests[port] = ajax.apply(this, arguments);
			return pendingRequests[port];
		}
		return ajax.apply(this, arguments);
	};
}

// provides delegate(type: String, delegate: Selector, handler: Callback) plugin for easier event delegation
// handler is only called when $(event.target).is(delegate), in the scope of the jquery-object for event.target

$.extend($.fn, {
	validateDelegate: function( delegate, type, handler ) {
		return this.bind(type, function( event ) {
			var target = $(event.target);
			if ( target.is(delegate) ) {
				return handler.apply(target, arguments);
			}
		});
	}
});

}));
// Backbone.Syphon, v0.3.0
// Copyright (c)2012 Derick Bailey, Muted Solutions, LLC.
// Distributed under MIT license
// http://github.com/derickbailey/backbone.syphon
Backbone.Syphon = (function(Backbone, $, _){
  var Syphon = {};

  // Ignore Element Types
  // --------------------

  // Tell Syphon to ignore all elements of these types. You can
  // push new types to ignore directly in to this array.
  Syphon.ignoredTypes = ["button", "submit", "reset"];

  // Syphon
  // ------

  // Get a JSON object that represents
  // all of the form inputs, in this view
  Syphon.serialize = function(view, options){
    var data = {};

    // Build the configuration
    var config = buildConfig(options);

    // Get all of the elements to process
    var elements = getInputElements(view, config);

    // Process all of the elements
    _.each(elements, function(el){
      var $el = $(el);
      var type = getElementType($el); 

      // Get the key for the input
      var keyExtractor = config.keyExtractors.get(type);
      var key = keyExtractor($el);

      // Get the value for the input
      var inputReader = config.inputReaders.get(type);
      var value = inputReader($el);

      // Get the key assignment validator and make sure
      // it's valid before assigning the value to the key
      var validKeyAssignment = config.keyAssignmentValidators.get(type);
      if (validKeyAssignment($el, key, value)){
        data[key] = value;
      }
    });

    // Done; send back the results.
    return data;
  };
  
  // Use the given JSON object to populate
  // all of the form inputs, in this view
  Syphon.deserialize = function(view, data, options){
    // Build the configuration
    var config = buildConfig(options);

    // Get all of the elements to process
    var elements = getInputElements(view, config);

    // Process all of the elements
    _.each(elements, function(el){
      var $el = $(el);
      var type = getElementType($el); 

      // Get the key for the input
      var keyExtractor = config.keyExtractors.get(type);
      var key = keyExtractor($el);

      // Write value to input
      var inputWriter = config.inputWriters.get(type);
      inputWriter($el, data[key]);
    });
  };

  // Helpers
  // -------

  // Retrieve all of the form inputs
  // from the view
  var getInputElements = function(view, config){
    var form = view.$el.is("form") ? view.el : view.$("form")[0];
    var elements = form.elements;

    elements = _.reject(elements, function(el){
      var reject;
      var type = getElementType(el);
      var extractor = config.keyExtractors.get(type);
      var identifier = extractor($(el));
     
      var foundInIgnored = _.include(config.ignoredTypes, type);
      var foundInInclude = _.include(config.include, identifier);
      var foundInExclude = _.include(config.exclude, identifier);

      if (foundInInclude){
        reject = false;
      } else {
        if (config.include){
          reject = true;
        } else {
          reject = (foundInExclude || foundInIgnored);
        }
      }

      return reject;
    });

    return elements;
  };

  // Determine what type of element this is. It
  // will either return the `type` attribute of
  // an `<input>` element, or the `tagName` of
  // the element when the element is not an `<input>`.
  var getElementType = function(el){
    var typeAttr;
    var $el = $(el);
    var tagName = $el[0].tagName;
    var type = tagName;

    if (tagName.toLowerCase() === "input"){
      typeAttr = $el.attr("type");
      if (typeAttr){
        type = typeAttr;
      } else {
        type = "text";
      }
    }
    
    // Always return the type as lowercase
    // so it can be matched to lowercase
    // type registrations.
    return type.toLowerCase();
  };
  
  // Build a configuration object and initialize
  // default values.
  var buildConfig = function(options){
    var config = _.clone(options) || {};
    
    config.ignoredTypes = _.clone(Syphon.ignoredTypes);
    config.inputReaders = config.inputReaders || Syphon.InputReaders;
    config.inputWriters = config.inputWriters || Syphon.InputWriters;
    config.keyExtractors = config.keyExtractors || Syphon.KeyExtractors;
    config.keyAssignmentValidators = config.keyAssignmentValidators || Syphon.KeyAssignmentValidators;
    
    return config;
  };

  return Syphon;
})(Backbone, jQuery, _);

// Type Registry
// -------------

// Type Registries allow you to register something to
// an input type, and retrieve either the item registered
// for a specific type or the default registration
Backbone.Syphon.TypeRegistry = function(){
  this.registeredTypes = {};
};

// Borrow Backbone's `extend` keyword for our TypeRegistry
Backbone.Syphon.TypeRegistry.extend = Backbone.Model.extend;

_.extend(Backbone.Syphon.TypeRegistry.prototype, {

  // Get the registered item by type. If nothing is
  // found for the specified type, the default is
  // returned.
  get: function(type){
    var item = this.registeredTypes[type];

    if (!item){
      item = this.registeredTypes["default"];
    }

    return item;
  },

  // Register a new item for a specified type
  register: function(type, item){
    this.registeredTypes[type] = item;
  },

  // Register a default item to be used when no
  // item for a specified type is found
  registerDefault: function(item){
    this.registeredTypes["default"] = item;
  },

  // Remove an item from a given type registration
  unregister: function(type){
    if (this.registeredTypes[type]){
      delete this.registeredTypes[type];
    }
  }
});




// Key Extractors
// --------------

// Key extractors produce the "key" in `{key: "value"}`
// pairs, when serializing.
Backbone.Syphon.KeyExtractorSet = Backbone.Syphon.TypeRegistry.extend();

// Built-in Key Extractors
Backbone.Syphon.KeyExtractors = new Backbone.Syphon.KeyExtractorSet();

// The default key extractor, which uses the
// input element's "id" attribute
Backbone.Syphon.KeyExtractors.registerDefault(function($el){
  return $el.prop("name");
});


// Input Readers
// -------------

// Input Readers are used to extract the value from
// an input element, for the serialized object result
Backbone.Syphon.InputReaderSet = Backbone.Syphon.TypeRegistry.extend();

// Built-in Input Readers
Backbone.Syphon.InputReaders = new Backbone.Syphon.InputReaderSet();

// The default input reader, which uses an input
// element's "value"
Backbone.Syphon.InputReaders.registerDefault(function($el){
  return $el.val();
});

// Checkbox reader, returning a boolean value for
// whether or not the checkbox is checked.
Backbone.Syphon.InputReaders.register("checkbox", function($el){
  var checked = $el.prop("checked");
  return checked;
});


// Input Writers
// -------------

// Input Writers are used to insert a value from an
// object into an input element.
Backbone.Syphon.InputWriterSet = Backbone.Syphon.TypeRegistry.extend();

// Built-in Input Writers
Backbone.Syphon.InputWriters = new Backbone.Syphon.InputWriterSet();

// The default input writer, which sets an input
// element's "value"
Backbone.Syphon.InputWriters.registerDefault(function($el, value){
  $el.val(value);
});

// Checkbox writer, set whether or not the checkbox is checked
// depending on the boolean value.
Backbone.Syphon.InputWriters.register("checkbox", function($el, value){
  $el.prop("checked", value);
});

// Radio button writer, set whether or not the radio button is
// checked.  The button should only be checked if it's value
// equals the given value.
Backbone.Syphon.InputWriters.register("radio", function($el, value){
  $el.prop("checked", $el.val() === value);
});

// Key Assignment Validators
// -------------------------

// Key Assignment Validators are used to determine whether or not a
// key should be assigned to a value, after the key and value have been
// extracted from the element. This is the last opportunity to prevent
// bad data from getting serialized to your object.

Backbone.Syphon.KeyAssignmentValidatorSet = Backbone.Syphon.TypeRegistry.extend();

// Build-in Key Assignment Validators
Backbone.Syphon.KeyAssignmentValidators = new Backbone.Syphon.KeyAssignmentValidatorSet();

// Everything is valid by default
Backbone.Syphon.KeyAssignmentValidators.registerDefault(function(){ return true; });

// But only the "checked" radio button for a given
// radio button group is valid
Backbone.Syphon.KeyAssignmentValidators.register("radio", function($el, key, value){ 
  return $el.prop("checked");
});


define("syphon", function(){});

// A custom basic notification module. User uses the add_alert method.
define('views/notification',['jquery', 'backbone', ], function($) {

    var NotificationsView = Backbone.View.extend({
        //A div with id-notifications already exists in DOM. Using the same div as this view's parent container
        el: '#notifications',
        error_notif_template: _.template($('#' + 'error_notifcation_template')
            .html()),
        success_notif_template: _.template($('#' + 'success_notifcation_template')
            .html()),

        add_alert: function(options) {
            // options contain the type of notif and the message      
            var notif_type = options.notif_type;
            var message = options.message;
            var alert_class, timeout, template;
            
            //create the notif with the message
            if (notif_type === "success") {
                template = this.success_notif_template({
                    msg: message
                });
                alert_class = ".alert-success";
                timeout = 10000;
            } else {
                template = this.error_notif_template({
                    msg: message
                });
                alert_class = ".alert-danger";
                timeout = 20000;
            }
            
            //Put the notif in view's parent element
            $(this.el)
                .append(template);
                
            //Scroll the page up..not sure why    
            $("html, body")
                .animate({
                scrollTop: 0
            }, 700);
            
            //Fade, slide and remove the notif after some time
            window.setTimeout(function() {
                //can be improved...ryt now all notifs of this type would get removed instead of only this particular notif
                $(alert_class)
                    .fadeTo(500, 0)
                    .slideUp(500, function() {
                    $(this)
                        .remove();
                });
            }, timeout);

        }
    });
    //return an initialized view - the app uses a single instance of Notification module
    return new NotificationsView;
});

define('models/user_model',[
  'jquery',
  'backbone',
  'indexeddb_backbone_config',
  'indexeddb-backbone',
  'collections/upload_collection'
  // Using the Require.js text! plugin, we are loaded raw text
  // which will be used as our views primary template
  // 'text!templates/project/list.html'
], function(jquery, backbone, indexeddb, idb_backbone_adapter, UploadCollection){
    
    var generic_model_offline = Backbone.Model.extend({
        database: indexeddb,
        storeName: "user",
        isOnline: function(){
            return navigator.onLine;
        },
        isLoggedIn: function(){
            //TODO: should fetch itself first to get latest state?
            // should this be handled by the auth module
            return this.get("loggedin");
        },
        canSaveOnline: function(){
            return this.isOnline() && UploadCollection.fetched && UploadCollection.length===0
        }
    });
    var user_model = new generic_model_offline();
    user_model.set({key: "user_info"});
    
  return user_model;
});
// This is the implementation of offline backend for authentication. Like the db on server has server/Django which provides an authentication wrapper over it, similarly this module provides that wrapper around the offline db. 
// It provides an interface to let user - login, logout, check_login against this offline backend. The user should be logged into this backend before making any requests on the offline db as the offline_utils module makes use of this module before processing any db request
// Uses a User table in offline db to store the username, password and login-state of the user
define('auth_offline_backend',[
    'models/user_model',  
  ], function(User){
      
  //sets login state = false in off db
  var logout = function(){
      var dfd = new $.Deferred();
      User.fetch({
          success: function(){
              save_login_state(User.get("username"), User.get("password"), User.get('language'), false)
                  .done(function(){
                      dfd.resolve();
                  })
                  .fail(function(){
                      dfd.reject();
                  });
          },
          error: function(){
               return dfd.reject();
          }
      });      
      return dfd.promise();
  }
  
  // if u, p matches that in user table, sets login state = true 
  var login = function(username, password, language){
      var dfd = new $.Deferred();
      User.fetch({
          success: function(){
              if(username==User.get("username") && password==User.get("password"))
              {
                  save_login_state(username, password, language, true)
                      .done(function(){
                          return dfd.resolve("Successfully Logged In (Offline Backend)");
                      })
                      .fail(function(error){
                          return dfd.reject(error);
                      });
              }
              else
              {
                  return dfd.reject("Username password did not match (Offline Backend)");
              }
          },
          error: function(){
              // No user has been found in the database. This is probably a new login, and database is yet to be created.
               save_login_state(username, password, language, true)
               .done(function (){
                   return dfd.resolve("New user registered in offline database.");
               })
               .fail(function (error){
                   return dfd.reject(error);
               });
          }
      });
      return dfd.promise();
  }
  
  //saves in offline that this username, password is logged in/out
  var save_login_state = function(username, password, language, loggedin){
      var dfd = new $.Deferred();
      User.save({'username':username, 'password':password, 'loggedin':loggedin, 'language':language},{
          success: function(){
              console.log("user state saved in offline");
              dfd.resolve();
          },
          error: function(){
              console.log("Error while saving login state in offline (Offline Backend)");
              dfd.reject("Error while saving login state in offline (Offline Backend)");
          }
      });
      return dfd;
  }
  
  // check whther user is logged in or not
  var check_login = function(){
      var dfd = new $.Deferred();
      User.fetch({
          success: function(){
              if(User.get("loggedin"))
                  return dfd.resolve();
              else
                  return dfd.reject("User is currently logged out. (Offline Backend)");
          },
          error: function(){
               return dfd.reject("User couldn't be fetched from offline db (Offline Backend)");
          }
      });
      return dfd.promise();
  }

  return {
    login: login,
    logout: logout,
    check_login: check_login
  };
});

//A module of data layer to communicate with offline DB. Since there are no fixed entities in COCO v2(as they are defined by user in config.js), there are no predefined models. This module creates backbone models/collection on the fly and enable communication with the offline DB thru the models/collections.
define('offline_utils',['jquery', 'configs', 'backbone', 'indexeddb_backbone_config', 'auth_offline_backend'], 
function($, all_configs, pa, indexeddb, OfflineAuthBackend) {
    
    var offline = {
        
        //Creates and return a new offline backbone model object for the given entity
        create_b_model: function(entity_name)
        {
            var model_offline = Backbone.Model.extend({
                database: indexeddb,
                storeName: entity_name,
            });
            return new model_offline();
        },
        
        //Creates and return a new offline backbone collection object for the given entity
        create_b_collection: function(entity_name, options){
            var model_offline = Backbone.Model.extend({
                database: indexeddb,
                storeName: entity_name,
            });
            options = $.extend({
                model: model_offline,
                database: indexeddb,
                storeName: entity_name,
            },options);
            var collection_offline = Backbone.Collection.extend(options);
            return new collection_offline();
        },
    
        //Saves object in offline DB
        save: function(off_model, entity_name, json){
            var dfd = new $.Deferred();
            console.log("SAVING THIS IN OFFLINE DB - "+JSON.stringify(json));
            if(!off_model)
            {
                //create offline model
                off_model = this.create_b_model(entity_name);
            }
            var that = this;
            //check whether user is logged in
            this.check_login_wrapper()
                .done(function(){
                    //save model with the given json
                    off_model.save(json,{
                        success: function(model){
                            return dfd.resolve(off_model);
                        },
                        error: function(model,error){
                            console.log(error);
                            //format error object to match the format of error sent by online save
                            var err_json = {};
							//get unique together fields
							var ut = eval("all_configs." + entity_name +".unique_together_fields").slice(0); 
							var utStr = that.beautify(ut);
							cap_entity_name = entity_name.charAt(0).toUpperCase() + entity_name.slice(1);
							var newerr = cap_entity_name + " with this " + utStr + " already exists";
                            err_json[entity_name] = {
                                __all__: [newerr]
                            }
                            return dfd.reject(JSON.stringify(err_json));
                        }
                    });
                })
            return dfd;
        },
		
		beautify: function(ut){
			for (var i=0; i< ut.length; i++){
				ut[i] = ut[i].charAt(0).toUpperCase() + ut[i].slice(1)
				ut[i] = ut[i].replace("_"," ");
				ut[i] = ut[i].replace(".id","");
			}
			return ut.join(", ");
		},
        
        //fetches an object from Offline DB from "entity_name" table having "value" value for "key" attribute 
        fetch_object: function(entity_name, key, value){
            var dfd = new $.Deferred();
            //create a offline model
            var off_model = this.create_b_model(entity_name);
            // set the key, value - Must have an index on key in IDB
            off_model.set(key, value);
            //check whether user is logged in
            this.check_login_wrapper()
                .done(function(){
                    // fetch the model - from offline DB
                    off_model.fetch({
                        success: function(off_model){
                            // return fetched model
                            dfd.resolve(off_model);
                        },
                        error: function(model, error){
                            dfd.reject(model, error);
                        }
                    });
                })
            return dfd;
        },
        
        //fetches whole "entity_name" table from offline DB as backbone collection 
        fetch_collection: function(entity_name){
            var dfd = new $.Deferred();
            //create backbone collection of type entity_name
            var off_coll = this.create_b_collection(entity_name);
            //check whether user is logged in 
            this.check_login_wrapper()
                .done(function(){
                    //fetch collection
                    off_coll.fetch({
                        success: function(off_coll){
                            //return fetched collection
                            dfd.resolve(off_coll);
                        },
                        error: function(error){
                            dfd.reject("Error fetching collection -"+entity_name+"- from offline - "+error);
                        }
                    });
                })
            return dfd;
        },
        
        //deletes an object from offline db - specified in either off_model or as (entity_name,id)
        delete_object: function(off_model, entity_name, id){
            var dfd = new $.Deferred();
            if(!off_model)
            {   
                //if backbone model for the object to be deleted was not provided - create one
                off_model = this.create_b_model(entity_name);
            }
            if(id)
            {
                //set id on model to delete
                off_model.set("id",id);
            }
            
            //check whether user is logged in
            this.check_login_wrapper()
                .done(function(){
                    //delete the model 
                    off_model.destroy({
                        success: function(model){
                            return dfd.resolve(model);
                        },
                        error: function(error){
                            console.log(error);
                            return dfd.reject("Error destroying object in offline - "+error.srcElement.error.name);
                        }
                    });
                })
            return dfd;
        },
        
        //wrapper to wrap db requests with - to check whether user is logged in or not before accessing DB
        check_login_wrapper: function(){
            var dfd = new $.Deferred();
            console.log("Offline Backend : Authenticating Request");
            OfflineAuthBackend.check_login()
                .done(function(){
                    dfd.resolve();
                })
                .fail(function(){
                    dfd.reject();
                    //navigate to login url if not logged in
                    window.Router.navigate("login",{trigger:true});
                });  
            return dfd;    
        },
        
        //completely deletes the offline database and refreshes the page 
        reset_database: function(){
            var request = indexedDB.deleteDatabase("offline-database-v2");
            request.onerror = function(event) {
                console.log(event);
                console.log("RESET DATABASE:Error!");
                alert("Error while resetting database! Refresh the page and try again.");
            };
            request.onsuccess = function(event) {
                console.log("RESET DATABASE:Success!");
                location.reload();
            }
            request.onblocked = function(event) {
                console.log("RESET DATABASE:Blocked!");
                //reloading when blocked might be causing the unproper deletion of db 
                location.reload();
            };
        }    
        
        
    }
    
    return offline;

});

// takes an object and the foreign entities description for the object. Using the descrip iterates over json,identifies the foreign values and denormalizes them. Same object passed is denormalised. New object is not created.
// converts a foreign element like person:23131 to person:{id:23131, name:"Shrey Jairath"}
// To use - call the denormalize method
define('denormalize',['jquery', 'configs', 'backbone', 'indexeddb_backbone_config'],

    function($, configs, pa, indexeddb) {
        var denormalize = {

            // get the name of the id field of foreign element in object's json - for eg - id or person_id
            _get_id_field: function(entity, element, f_entities) {
                return f_entities[entity][element].id_field || "id";
            },

            // get name of the name_field of the foreign element in object's json - for eg - name or person_name
            _get_name_field: function(entity, element, f_entities) {
                return f_entities[entity][element].name_field;
            },

            denormalize: function(json, f_entities) {
                console.log("FORMCONTROLLER:denormalize: json before denormalizing" + JSON.stringify(json));
                var that = this;
                // is filled with a dfd for each foreign element to be denormalised - when all dfds resolve - denormalisation is complete
                this.field_dfds = [];
                // iterate over the foreign elements of the object and denpormalise them asynchronously - fills the field_dfds with a dfd for each conversion
                this._iterate_foreign_fields(json, f_entities);
                return $.when.apply($, this.field_dfds);
            },

            // iterates over the foreign elements of the object and denormalises them asynchronously - fills the field_dfds with a dfd for each conversion
            _iterate_foreign_fields: function(json, f_entities) {
                // use the foreign entities definition of this object's entity to iterate over the foreign elements in the object 
                for (var entity in f_entities) {
                    for (var element in f_entities[entity]) {
                        // get details of the foreign element bieng denormalised
                        var id_field = this._get_id_field(entity, element, f_entities);
                        var name_field = this._get_name_field(entity, element, f_entities);
                        var field_desc = {
                            entity_name: entity,
                            id_attribute: id_field,
                            name_attribute: name_field
                        };

                        //  if the foreign element doesn't exist, put an empty object and return
                        if (!(json[element])) {
                            json[element] = {};
                            json[element][field_desc.id_attribute] = null;
                            json[element][field_desc.name_attribute] = null;
                            continue;
                        }

                        // the foreign element is an expanded
                        if (f_entities[entity][element].expanded) {
                            // and has its own foreign elements
                            if (f_entities[entity][element].expanded.foreign_entities) {
                                // recursively denormalise the foreign elements of expanded objects
                                _.each(json[element], function(object, index) {
                                    this._iterate_foreign_fields(object, f_entities[entity][element].expanded.foreign_entities);
                                }, this);
                            }
                            return;
                        }

                        //foreign element is a multi-select dropdown
                        if (json[element] instanceof Array) {
                            // denormalise each object of the multi-select
                            _.each(json[element], function(val, index) {
                                json[element][index] = {};
                                json[element][index][id_field] = parseInt(val);
                                // denormalise the element and put its dfd in field_dfds list 
                                this.field_dfds.push(this._denormalize_object(json[element][index], field_desc));
                            }, this);
                        }
                        //foreign element is a single-select dropdown
                        else {
                            var temp = {};
                            temp[id_field] = parseInt(json[element]);
                            json[element] = temp;
                            // denormalise the element and put its dfd in field_dfds list 
                            this.field_dfds.push(this._denormalize_object(json[element], field_desc));
                        }

                    }
                }
            },

            // denormalises a single foreign element asynchronously and returns a dfd to wait upon
            _denormalize_object: function(obj, field_desc) {
                console.log("Denormalize: dnormalizing object", JSON.stringify(obj), JSON.stringify(field_desc));
                var dfd = new $.Deferred();
                // foreign element is empty - convert to {id:null, name:null} 
                if (!obj[field_desc.id_attribute]) {
                    obj[field_desc.id_attribute] = null;
                    obj[field_desc.name_attribute] = null;
                    return dfd.resolve();
                }
                //  fetch the foreign element from offline db  
                // TODO:remove this and use the offline_utils module instead
                var generic_model_offline = Backbone.Model.extend({
                    database: indexeddb,
                    storeName: field_desc.entity_name,
                });
                var f_model = new generic_model_offline();
                f_model.set("id", parseInt(obj[field_desc.id_attribute]));
                var that = this;
                f_model.fetch({
                    success: function(model) {
                        // put in the name attribute - denormalization completed for this element
                        obj[field_desc.name_attribute] = model.get(field_desc.name_attribute);
                        return dfd.resolve();
                    },
                    error: function(model, error) {
                        // the foreign element doesn't exists in offline db
                        console.log("Denormalize: unexpected error.fetch failed", error);
                        return dfd.reject(error);
                    }
                });
                return dfd.promise();
            }

        }


        return denormalize;

    });

/* Chosen v1.1.0 | (c) 2011-2013 by Harvest | MIT License, https://github.com/harvesthq/chosen/blob/master/LICENSE.md */
!function(){var a,AbstractChosen,Chosen,SelectParser,b,c={}.hasOwnProperty,d=function(a,b){function d(){this.constructor=a}for(var e in b)c.call(b,e)&&(a[e]=b[e]);return d.prototype=b.prototype,a.prototype=new d,a.__super__=b.prototype,a};SelectParser=function(){function SelectParser(){this.options_index=0,this.parsed=[]}return SelectParser.prototype.add_node=function(a){return"OPTGROUP"===a.nodeName.toUpperCase()?this.add_group(a):this.add_option(a)},SelectParser.prototype.add_group=function(a){var b,c,d,e,f,g;for(b=this.parsed.length,this.parsed.push({array_index:b,group:!0,label:this.escapeExpression(a.label),children:0,disabled:a.disabled}),f=a.childNodes,g=[],d=0,e=f.length;e>d;d++)c=f[d],g.push(this.add_option(c,b,a.disabled));return g},SelectParser.prototype.add_option=function(a,b,c){return"OPTION"===a.nodeName.toUpperCase()?(""!==a.text?(null!=b&&(this.parsed[b].children+=1),this.parsed.push({array_index:this.parsed.length,options_index:this.options_index,value:a.value,text:a.text,html:a.innerHTML,selected:a.selected,disabled:c===!0?c:a.disabled,group_array_index:b,classes:a.className,style:a.style.cssText})):this.parsed.push({array_index:this.parsed.length,options_index:this.options_index,empty:!0}),this.options_index+=1):void 0},SelectParser.prototype.escapeExpression=function(a){var b,c;return null==a||a===!1?"":/[\&\<\>\"\'\`]/.test(a)?(b={"<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#x27;","`":"&#x60;"},c=/&(?!\w+;)|[\<\>\"\'\`]/g,a.replace(c,function(a){return b[a]||"&amp;"})):a},SelectParser}(),SelectParser.select_to_array=function(a){var b,c,d,e,f;for(c=new SelectParser,f=a.childNodes,d=0,e=f.length;e>d;d++)b=f[d],c.add_node(b);return c.parsed},AbstractChosen=function(){function AbstractChosen(a,b){this.form_field=a,this.options=null!=b?b:{},AbstractChosen.browser_is_supported()&&(this.is_multiple=this.form_field.multiple,this.set_default_text(),this.set_default_values(),this.setup(),this.set_up_html(),this.register_observers())}return AbstractChosen.prototype.set_default_values=function(){var a=this;return this.click_test_action=function(b){return a.test_active_click(b)},this.activate_action=function(b){return a.activate_field(b)},this.active_field=!1,this.mouse_on_container=!1,this.results_showing=!1,this.result_highlighted=null,this.allow_single_deselect=null!=this.options.allow_single_deselect&&null!=this.form_field.options[0]&&""===this.form_field.options[0].text?this.options.allow_single_deselect:!1,this.disable_search_threshold=this.options.disable_search_threshold||0,this.disable_search=this.options.disable_search||!1,this.enable_split_word_search=null!=this.options.enable_split_word_search?this.options.enable_split_word_search:!0,this.group_search=null!=this.options.group_search?this.options.group_search:!0,this.search_contains=this.options.search_contains||!1,this.single_backstroke_delete=null!=this.options.single_backstroke_delete?this.options.single_backstroke_delete:!0,this.max_selected_options=this.options.max_selected_options||1/0,this.inherit_select_classes=this.options.inherit_select_classes||!1,this.display_selected_options=null!=this.options.display_selected_options?this.options.display_selected_options:!0,this.display_disabled_options=null!=this.options.display_disabled_options?this.options.display_disabled_options:!0},AbstractChosen.prototype.set_default_text=function(){return this.default_text=this.form_field.getAttribute("data-placeholder")?this.form_field.getAttribute("data-placeholder"):this.is_multiple?this.options.placeholder_text_multiple||this.options.placeholder_text||AbstractChosen.default_multiple_text:this.options.placeholder_text_single||this.options.placeholder_text||AbstractChosen.default_single_text,this.results_none_found=this.form_field.getAttribute("data-no_results_text")||this.options.no_results_text||AbstractChosen.default_no_result_text},AbstractChosen.prototype.mouse_enter=function(){return this.mouse_on_container=!0},AbstractChosen.prototype.mouse_leave=function(){return this.mouse_on_container=!1},AbstractChosen.prototype.input_focus=function(){var a=this;if(this.is_multiple){if(!this.active_field)return setTimeout(function(){return a.container_mousedown()},50)}else if(!this.active_field)return this.activate_field()},AbstractChosen.prototype.input_blur=function(){var a=this;return this.mouse_on_container?void 0:(this.active_field=!1,setTimeout(function(){return a.blur_test()},100))},AbstractChosen.prototype.results_option_build=function(a){var b,c,d,e,f;for(b="",f=this.results_data,d=0,e=f.length;e>d;d++)c=f[d],b+=c.group?this.result_add_group(c):this.result_add_option(c),(null!=a?a.first:void 0)&&(c.selected&&this.is_multiple?this.choice_build(c):c.selected&&!this.is_multiple&&this.single_set_selected_text(c.text));return b},AbstractChosen.prototype.result_add_option=function(a){var b,c;return a.search_match?this.include_option_in_results(a)?(b=[],a.disabled||a.selected&&this.is_multiple||b.push("active-result"),!a.disabled||a.selected&&this.is_multiple||b.push("disabled-result"),a.selected&&b.push("result-selected"),null!=a.group_array_index&&b.push("group-option"),""!==a.classes&&b.push(a.classes),c=document.createElement("li"),c.className=b.join(" "),c.style.cssText=a.style,c.setAttribute("data-option-array-index",a.array_index),c.innerHTML=a.search_text,this.outerHTML(c)):"":""},AbstractChosen.prototype.result_add_group=function(a){var b;return a.search_match||a.group_match?a.active_options>0?(b=document.createElement("li"),b.className="group-result",b.innerHTML=a.search_text,this.outerHTML(b)):"":""},AbstractChosen.prototype.results_update_field=function(){return this.set_default_text(),this.is_multiple||this.results_reset_cleanup(),this.result_clear_highlight(),this.results_build(),this.results_showing?this.winnow_results():void 0},AbstractChosen.prototype.reset_single_select_options=function(){var a,b,c,d,e;for(d=this.results_data,e=[],b=0,c=d.length;c>b;b++)a=d[b],a.selected?e.push(a.selected=!1):e.push(void 0);return e},AbstractChosen.prototype.results_toggle=function(){return this.results_showing?this.results_hide():this.results_show()},AbstractChosen.prototype.results_search=function(){return this.results_showing?this.winnow_results():this.results_show()},AbstractChosen.prototype.winnow_results=function(){var a,b,c,d,e,f,g,h,i,j,k,l,m;for(this.no_results_clear(),e=0,g=this.get_search_text(),a=g.replace(/[-[\]{}()*+?.,\\^$|#\s]/g,"\\$&"),d=this.search_contains?"":"^",c=new RegExp(d+a,"i"),j=new RegExp(a,"i"),m=this.results_data,k=0,l=m.length;l>k;k++)b=m[k],b.search_match=!1,f=null,this.include_option_in_results(b)&&(b.group&&(b.group_match=!1,b.active_options=0),null!=b.group_array_index&&this.results_data[b.group_array_index]&&(f=this.results_data[b.group_array_index],0===f.active_options&&f.search_match&&(e+=1),f.active_options+=1),(!b.group||this.group_search)&&(b.search_text=b.group?b.label:b.html,b.search_match=this.search_string_match(b.search_text,c),b.search_match&&!b.group&&(e+=1),b.search_match?(g.length&&(h=b.search_text.search(j),i=b.search_text.substr(0,h+g.length)+"</em>"+b.search_text.substr(h+g.length),b.search_text=i.substr(0,h)+"<em>"+i.substr(h)),null!=f&&(f.group_match=!0)):null!=b.group_array_index&&this.results_data[b.group_array_index].search_match&&(b.search_match=!0)));return this.result_clear_highlight(),1>e&&g.length?(this.update_results_content(""),this.no_results(g)):(this.update_results_content(this.results_option_build()),this.winnow_results_set_highlight())},AbstractChosen.prototype.search_string_match=function(a,b){var c,d,e,f;if(b.test(a))return!0;if(this.enable_split_word_search&&(a.indexOf(" ")>=0||0===a.indexOf("["))&&(d=a.replace(/\[|\]/g,"").split(" "),d.length))for(e=0,f=d.length;f>e;e++)if(c=d[e],b.test(c))return!0},AbstractChosen.prototype.choices_count=function(){var a,b,c,d;if(null!=this.selected_option_count)return this.selected_option_count;for(this.selected_option_count=0,d=this.form_field.options,b=0,c=d.length;c>b;b++)a=d[b],a.selected&&(this.selected_option_count+=1);return this.selected_option_count},AbstractChosen.prototype.choices_click=function(a){return a.preventDefault(),this.results_showing||this.is_disabled?void 0:this.results_show()},AbstractChosen.prototype.keyup_checker=function(a){var b,c;switch(b=null!=(c=a.which)?c:a.keyCode,this.search_field_scale(),b){case 8:if(this.is_multiple&&this.backstroke_length<1&&this.choices_count()>0)return this.keydown_backstroke();if(!this.pending_backstroke)return this.result_clear_highlight(),this.results_search();break;case 13:if(a.preventDefault(),this.results_showing)return this.result_select(a);break;case 27:return this.results_showing&&this.results_hide(),!0;case 9:case 38:case 40:case 16:case 91:case 17:break;default:return this.results_search()}},AbstractChosen.prototype.clipboard_event_checker=function(){var a=this;return setTimeout(function(){return a.results_search()},50)},AbstractChosen.prototype.container_width=function(){return null!=this.options.width?this.options.width:""+this.form_field.offsetWidth+"px"},AbstractChosen.prototype.include_option_in_results=function(a){return this.is_multiple&&!this.display_selected_options&&a.selected?!1:!this.display_disabled_options&&a.disabled?!1:a.empty?!1:!0},AbstractChosen.prototype.search_results_touchstart=function(a){return this.touch_started=!0,this.search_results_mouseover(a)},AbstractChosen.prototype.search_results_touchmove=function(a){return this.touch_started=!1,this.search_results_mouseout(a)},AbstractChosen.prototype.search_results_touchend=function(a){return this.touch_started?this.search_results_mouseup(a):void 0},AbstractChosen.prototype.outerHTML=function(a){var b;return a.outerHTML?a.outerHTML:(b=document.createElement("div"),b.appendChild(a),b.innerHTML)},AbstractChosen.browser_is_supported=function(){return"Microsoft Internet Explorer"===window.navigator.appName?document.documentMode>=8:/iP(od|hone)/i.test(window.navigator.userAgent)?!1:/Android/i.test(window.navigator.userAgent)&&/Mobile/i.test(window.navigator.userAgent)?!1:!0},AbstractChosen.default_multiple_text="Select Some Options",AbstractChosen.default_single_text="Select an Option",AbstractChosen.default_no_result_text="No results match",AbstractChosen}(),a=jQuery,a.fn.extend({chosen:function(b){return AbstractChosen.browser_is_supported()?this.each(function(){var c,d;c=a(this),d=c.data("chosen"),"destroy"===b&&d?d.destroy():d||c.data("chosen",new Chosen(this,b))}):this}}),Chosen=function(c){function Chosen(){return b=Chosen.__super__.constructor.apply(this,arguments)}return d(Chosen,c),Chosen.prototype.setup=function(){return this.form_field_jq=a(this.form_field),this.current_selectedIndex=this.form_field.selectedIndex,this.is_rtl=this.form_field_jq.hasClass("chosen-rtl")},Chosen.prototype.set_up_html=function(){var b,c;return b=["chosen-container"],b.push("chosen-container-"+(this.is_multiple?"multi":"single")),this.inherit_select_classes&&this.form_field.className&&b.push(this.form_field.className),this.is_rtl&&b.push("chosen-rtl"),c={"class":b.join(" "),style:"width: "+this.container_width()+";",title:this.form_field.title},this.form_field.id.length&&(c.id=this.form_field.id.replace(/[^\w]/g,"_")+"_chosen"),this.container=a("<div />",c),this.is_multiple?this.container.html('<ul class="chosen-choices"><li class="search-field"><input type="text" value="'+this.default_text+'" class="default" autocomplete="off" style="width:25px;" /></li></ul><div class="chosen-drop"><ul class="chosen-results"></ul></div>'):this.container.html('<a class="chosen-single chosen-default" tabindex="-1"><span>'+this.default_text+'</span><div><b></b></div></a><div class="chosen-drop"><div class="chosen-search"><input type="text" autocomplete="off" /></div><ul class="chosen-results"></ul></div>'),this.form_field_jq.hide().after(this.container),this.dropdown=this.container.find("div.chosen-drop").first(),this.search_field=this.container.find("input").first(),this.search_results=this.container.find("ul.chosen-results").first(),this.search_field_scale(),this.search_no_results=this.container.find("li.no-results").first(),this.is_multiple?(this.search_choices=this.container.find("ul.chosen-choices").first(),this.search_container=this.container.find("li.search-field").first()):(this.search_container=this.container.find("div.chosen-search").first(),this.selected_item=this.container.find(".chosen-single").first()),this.results_build(),this.set_tab_index(),this.set_label_behavior(),this.form_field_jq.trigger("chosen:ready",{chosen:this})},Chosen.prototype.register_observers=function(){var a=this;return this.container.bind("mousedown.chosen",function(b){a.container_mousedown(b)}),this.container.bind("mouseup.chosen",function(b){a.container_mouseup(b)}),this.container.bind("mouseenter.chosen",function(b){a.mouse_enter(b)}),this.container.bind("mouseleave.chosen",function(b){a.mouse_leave(b)}),this.search_results.bind("mouseup.chosen",function(b){a.search_results_mouseup(b)}),this.search_results.bind("mouseover.chosen",function(b){a.search_results_mouseover(b)}),this.search_results.bind("mouseout.chosen",function(b){a.search_results_mouseout(b)}),this.search_results.bind("mousewheel.chosen DOMMouseScroll.chosen",function(b){a.search_results_mousewheel(b)}),this.search_results.bind("touchstart.chosen",function(b){a.search_results_touchstart(b)}),this.search_results.bind("touchmove.chosen",function(b){a.search_results_touchmove(b)}),this.search_results.bind("touchend.chosen",function(b){a.search_results_touchend(b)}),this.form_field_jq.bind("chosen:updated.chosen",function(b){a.results_update_field(b)}),this.form_field_jq.bind("chosen:activate.chosen",function(b){a.activate_field(b)}),this.form_field_jq.bind("chosen:open.chosen",function(b){a.container_mousedown(b)}),this.form_field_jq.bind("chosen:close.chosen",function(b){a.input_blur(b)}),this.search_field.bind("blur.chosen",function(b){a.input_blur(b)}),this.search_field.bind("keyup.chosen",function(b){a.keyup_checker(b)}),this.search_field.bind("keydown.chosen",function(b){a.keydown_checker(b)}),this.search_field.bind("focus.chosen",function(b){a.input_focus(b)}),this.search_field.bind("cut.chosen",function(b){a.clipboard_event_checker(b)}),this.search_field.bind("paste.chosen",function(b){a.clipboard_event_checker(b)}),this.is_multiple?this.search_choices.bind("click.chosen",function(b){a.choices_click(b)}):this.container.bind("click.chosen",function(a){a.preventDefault()})},Chosen.prototype.destroy=function(){return a(this.container[0].ownerDocument).unbind("click.chosen",this.click_test_action),this.search_field[0].tabIndex&&(this.form_field_jq[0].tabIndex=this.search_field[0].tabIndex),this.container.remove(),this.form_field_jq.removeData("chosen"),this.form_field_jq.show()},Chosen.prototype.search_field_disabled=function(){return this.is_disabled=this.form_field_jq[0].disabled,this.is_disabled?(this.container.addClass("chosen-disabled"),this.search_field[0].disabled=!0,this.is_multiple||this.selected_item.unbind("focus.chosen",this.activate_action),this.close_field()):(this.container.removeClass("chosen-disabled"),this.search_field[0].disabled=!1,this.is_multiple?void 0:this.selected_item.bind("focus.chosen",this.activate_action))},Chosen.prototype.container_mousedown=function(b){return this.is_disabled||(b&&"mousedown"===b.type&&!this.results_showing&&b.preventDefault(),null!=b&&a(b.target).hasClass("search-choice-close"))?void 0:(this.active_field?this.is_multiple||!b||a(b.target)[0]!==this.selected_item[0]&&!a(b.target).parents("a.chosen-single").length||(b.preventDefault(),this.results_toggle()):(this.is_multiple&&this.search_field.val(""),a(this.container[0].ownerDocument).bind("click.chosen",this.click_test_action),this.results_show()),this.activate_field())},Chosen.prototype.container_mouseup=function(a){return"ABBR"!==a.target.nodeName||this.is_disabled?void 0:this.results_reset(a)},Chosen.prototype.search_results_mousewheel=function(a){var b;return a.originalEvent&&(b=-a.originalEvent.wheelDelta||a.originalEvent.detail),null!=b?(a.preventDefault(),"DOMMouseScroll"===a.type&&(b=40*b),this.search_results.scrollTop(b+this.search_results.scrollTop())):void 0},Chosen.prototype.blur_test=function(){return!this.active_field&&this.container.hasClass("chosen-container-active")?this.close_field():void 0},Chosen.prototype.close_field=function(){return a(this.container[0].ownerDocument).unbind("click.chosen",this.click_test_action),this.active_field=!1,this.results_hide(),this.container.removeClass("chosen-container-active"),this.clear_backstroke(),this.show_search_field_default(),this.search_field_scale()},Chosen.prototype.activate_field=function(){return this.container.addClass("chosen-container-active"),this.active_field=!0,this.search_field.val(this.search_field.val()),this.search_field.focus()},Chosen.prototype.test_active_click=function(b){var c;return c=a(b.target).closest(".chosen-container"),c.length&&this.container[0]===c[0]?this.active_field=!0:this.close_field()},Chosen.prototype.results_build=function(){return this.parsing=!0,this.selected_option_count=null,this.results_data=SelectParser.select_to_array(this.form_field),this.is_multiple?this.search_choices.find("li.search-choice").remove():this.is_multiple||(this.single_set_selected_text(),this.disable_search||this.form_field.options.length<=this.disable_search_threshold?(this.search_field[0].readOnly=!0,this.container.addClass("chosen-container-single-nosearch")):(this.search_field[0].readOnly=!1,this.container.removeClass("chosen-container-single-nosearch"))),this.update_results_content(this.results_option_build({first:!0})),this.search_field_disabled(),this.show_search_field_default(),this.search_field_scale(),this.parsing=!1},Chosen.prototype.result_do_highlight=function(a){var b,c,d,e,f;if(a.length){if(this.result_clear_highlight(),this.result_highlight=a,this.result_highlight.addClass("highlighted"),d=parseInt(this.search_results.css("maxHeight"),10),f=this.search_results.scrollTop(),e=d+f,c=this.result_highlight.position().top+this.search_results.scrollTop(),b=c+this.result_highlight.outerHeight(),b>=e)return this.search_results.scrollTop(b-d>0?b-d:0);if(f>c)return this.search_results.scrollTop(c)}},Chosen.prototype.result_clear_highlight=function(){return this.result_highlight&&this.result_highlight.removeClass("highlighted"),this.result_highlight=null},Chosen.prototype.results_show=function(){return this.is_multiple&&this.max_selected_options<=this.choices_count()?(this.form_field_jq.trigger("chosen:maxselected",{chosen:this}),!1):(this.container.addClass("chosen-with-drop"),this.results_showing=!0,this.search_field.focus(),this.search_field.val(this.search_field.val()),this.winnow_results(),this.form_field_jq.trigger("chosen:showing_dropdown",{chosen:this}))},Chosen.prototype.update_results_content=function(a){return this.search_results.html(a)},Chosen.prototype.results_hide=function(){return this.results_showing&&(this.result_clear_highlight(),this.container.removeClass("chosen-with-drop"),this.form_field_jq.trigger("chosen:hiding_dropdown",{chosen:this})),this.results_showing=!1},Chosen.prototype.set_tab_index=function(){var a;return this.form_field.tabIndex?(a=this.form_field.tabIndex,this.form_field.tabIndex=-1,this.search_field[0].tabIndex=a):void 0},Chosen.prototype.set_label_behavior=function(){var b=this;return this.form_field_label=this.form_field_jq.parents("label"),!this.form_field_label.length&&this.form_field.id.length&&(this.form_field_label=a("label[for='"+this.form_field.id+"']")),this.form_field_label.length>0?this.form_field_label.bind("click.chosen",function(a){return b.is_multiple?b.container_mousedown(a):b.activate_field()}):void 0},Chosen.prototype.show_search_field_default=function(){return this.is_multiple&&this.choices_count()<1&&!this.active_field?(this.search_field.val(this.default_text),this.search_field.addClass("default")):(this.search_field.val(""),this.search_field.removeClass("default"))},Chosen.prototype.search_results_mouseup=function(b){var c;return c=a(b.target).hasClass("active-result")?a(b.target):a(b.target).parents(".active-result").first(),c.length?(this.result_highlight=c,this.result_select(b),this.search_field.focus()):void 0},Chosen.prototype.search_results_mouseover=function(b){var c;return c=a(b.target).hasClass("active-result")?a(b.target):a(b.target).parents(".active-result").first(),c?this.result_do_highlight(c):void 0},Chosen.prototype.search_results_mouseout=function(b){return a(b.target).hasClass("active-result")?this.result_clear_highlight():void 0},Chosen.prototype.choice_build=function(b){var c,d,e=this;return c=a("<li />",{"class":"search-choice"}).html("<span>"+b.html+"</span>"),b.disabled?c.addClass("search-choice-disabled"):(d=a("<a />",{"class":"search-choice-close","data-option-array-index":b.array_index}),d.bind("click.chosen",function(a){return e.choice_destroy_link_click(a)}),c.append(d)),this.search_container.before(c)},Chosen.prototype.choice_destroy_link_click=function(b){return b.preventDefault(),b.stopPropagation(),this.is_disabled?void 0:this.choice_destroy(a(b.target))},Chosen.prototype.choice_destroy=function(a){return this.result_deselect(a[0].getAttribute("data-option-array-index"))?(this.show_search_field_default(),this.is_multiple&&this.choices_count()>0&&this.search_field.val().length<1&&this.results_hide(),a.parents("li").first().remove(),this.search_field_scale()):void 0},Chosen.prototype.results_reset=function(){return this.reset_single_select_options(),this.form_field.options[0].selected=!0,this.single_set_selected_text(),this.show_search_field_default(),this.results_reset_cleanup(),this.form_field_jq.trigger("change"),this.active_field?this.results_hide():void 0},Chosen.prototype.results_reset_cleanup=function(){return this.current_selectedIndex=this.form_field.selectedIndex,this.selected_item.find("abbr").remove()},Chosen.prototype.result_select=function(a){var b,c;return this.result_highlight?(b=this.result_highlight,this.result_clear_highlight(),this.is_multiple&&this.max_selected_options<=this.choices_count()?(this.form_field_jq.trigger("chosen:maxselected",{chosen:this}),!1):(this.is_multiple?b.removeClass("active-result"):this.reset_single_select_options(),c=this.results_data[b[0].getAttribute("data-option-array-index")],c.selected=!0,this.form_field.options[c.options_index].selected=!0,this.selected_option_count=null,this.is_multiple?this.choice_build(c):this.single_set_selected_text(c.text),(a.metaKey||a.ctrlKey)&&this.is_multiple||this.results_hide(),this.search_field.val(""),(this.is_multiple||this.form_field.selectedIndex!==this.current_selectedIndex)&&this.form_field_jq.trigger("change",{selected:this.form_field.options[c.options_index].value}),this.current_selectedIndex=this.form_field.selectedIndex,this.search_field_scale())):void 0},Chosen.prototype.single_set_selected_text=function(a){return null==a&&(a=this.default_text),a===this.default_text?this.selected_item.addClass("chosen-default"):(this.single_deselect_control_build(),this.selected_item.removeClass("chosen-default")),this.selected_item.find("span").text(a)},Chosen.prototype.result_deselect=function(a){var b;return b=this.results_data[a],this.form_field.options[b.options_index].disabled?!1:(b.selected=!1,this.form_field.options[b.options_index].selected=!1,this.selected_option_count=null,this.result_clear_highlight(),this.results_showing&&this.winnow_results(),this.form_field_jq.trigger("change",{deselected:this.form_field.options[b.options_index].value}),this.search_field_scale(),!0)},Chosen.prototype.single_deselect_control_build=function(){return this.allow_single_deselect?(this.selected_item.find("abbr").length||this.selected_item.find("span").first().after('<abbr class="search-choice-close"></abbr>'),this.selected_item.addClass("chosen-single-with-deselect")):void 0},Chosen.prototype.get_search_text=function(){return this.search_field.val()===this.default_text?"":a("<div/>").text(a.trim(this.search_field.val())).html()},Chosen.prototype.winnow_results_set_highlight=function(){var a,b;return b=this.is_multiple?[]:this.search_results.find(".result-selected.active-result"),a=b.length?b.first():this.search_results.find(".active-result").first(),null!=a?this.result_do_highlight(a):void 0},Chosen.prototype.no_results=function(b){var c;return c=a('<li class="no-results">'+this.results_none_found+' "<span></span>"</li>'),c.find("span").first().html(b),this.search_results.append(c),this.form_field_jq.trigger("chosen:no_results",{chosen:this})},Chosen.prototype.no_results_clear=function(){return this.search_results.find(".no-results").remove()},Chosen.prototype.keydown_arrow=function(){var a;return this.results_showing&&this.result_highlight?(a=this.result_highlight.nextAll("li.active-result").first())?this.result_do_highlight(a):void 0:this.results_show()},Chosen.prototype.keyup_arrow=function(){var a;return this.results_showing||this.is_multiple?this.result_highlight?(a=this.result_highlight.prevAll("li.active-result"),a.length?this.result_do_highlight(a.first()):(this.choices_count()>0&&this.results_hide(),this.result_clear_highlight())):void 0:this.results_show()},Chosen.prototype.keydown_backstroke=function(){var a;return this.pending_backstroke?(this.choice_destroy(this.pending_backstroke.find("a").first()),this.clear_backstroke()):(a=this.search_container.siblings("li.search-choice").last(),a.length&&!a.hasClass("search-choice-disabled")?(this.pending_backstroke=a,this.single_backstroke_delete?this.keydown_backstroke():this.pending_backstroke.addClass("search-choice-focus")):void 0)},Chosen.prototype.clear_backstroke=function(){return this.pending_backstroke&&this.pending_backstroke.removeClass("search-choice-focus"),this.pending_backstroke=null},Chosen.prototype.keydown_checker=function(a){var b,c;switch(b=null!=(c=a.which)?c:a.keyCode,this.search_field_scale(),8!==b&&this.pending_backstroke&&this.clear_backstroke(),b){case 8:this.backstroke_length=this.search_field.val().length;break;case 9:this.results_showing&&!this.is_multiple&&this.result_select(a),this.mouse_on_container=!1;break;case 13:a.preventDefault();break;case 38:a.preventDefault(),this.keyup_arrow();break;case 40:a.preventDefault(),this.keydown_arrow()}},Chosen.prototype.search_field_scale=function(){var b,c,d,e,f,g,h,i,j;if(this.is_multiple){for(d=0,h=0,f="position:absolute; left: -1000px; top: -1000px; display:none;",g=["font-size","font-style","font-weight","font-family","line-height","text-transform","letter-spacing"],i=0,j=g.length;j>i;i++)e=g[i],f+=e+":"+this.search_field.css(e)+";";return b=a("<div />",{style:f}),b.text(this.search_field.val()),a("body").append(b),h=b.width()+25,b.remove(),c=this.container.outerWidth(),h>c-10&&(h=c-10),this.search_field.css({width:h+"px"})}},Chosen}(AbstractChosen)}.call(this);
define("chosen", function(){});

/* =========================================================
 * bootstrap-datepicker.js
 * http://www.eyecon.ro/bootstrap-datepicker
 * =========================================================
 * Copyright 2012 Stefan Petre
 * Improvements by Andrew Rowls
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
 * ========================================================= */

(function( $ ) {

	function UTCDate(){
		return new Date(Date.UTC.apply(Date, arguments));
	}
	function UTCToday(){
		var today = new Date();
		return UTCDate(today.getUTCFullYear(), today.getUTCMonth(), today.getUTCDate());
	}

	// Picker object

	var Datepicker = function(element, options) {
		var that = this;

		this._process_options(options);

		this.element = $(element);
		this.isInline = false;
		this.isInput = this.element.is('input');
		this.component = this.element.is('.date') ? this.element.find('.add-on, .btn') : false;
		this.hasInput = this.component && this.element.find('input').length;
		if(this.component && this.component.length === 0)
			this.component = false;

		this.picker = $(DPGlobal.template);
		this._buildEvents();
		this._attachEvents();

		if(this.isInline) {
			this.picker.addClass('datepicker-inline').appendTo(this.element);
		} else {
			this.picker.addClass('datepicker-dropdown dropdown-menu');
		}
		// Classes have been changed below FROM -->> "icon-arrow-left"     TO -->> "glyphicon-arrow-left"  (same with right arrow)
		// This was done because we have upgraded to BootStrap 3 while the library used BootStrap 2 classes and it wasn't under development
		if (this.o.rtl){
			this.picker.addClass('datepicker-rtl');
			this.picker.find('.prev i, .next i')
						.toggleClass('glyphicon glyphicon-arrow-left glyphicon glyphicon-arrow-right');
		}


		this.viewMode = this.o.startView;

		if (this.o.calendarWeeks)
			this.picker.find('tfoot th.today')
						.attr('colspan', function(i, val){
							return parseInt(val) + 1;
						});

		this._allow_update = false;

		this.setStartDate(this.o.startDate);
		this.setEndDate(this.o.endDate);
		this.setDaysOfWeekDisabled(this.o.daysOfWeekDisabled);

		this.fillDow();
		this.fillMonths();

		this._allow_update = true;

		this.update();
		this.showMode();

		if(this.isInline) {
			this.show();
		}
	};

	Datepicker.prototype = {
		constructor: Datepicker,

		_process_options: function(opts){
			// Store raw options for reference
			this._o = $.extend({}, this._o, opts);
			// Processed options
			var o = this.o = $.extend({}, this._o);

			// Check if "de-DE" style date is available, if not language should
			// fallback to 2 letter code eg "de"
			var lang = o.language;
			if (!dates[lang]) {
				lang = lang.split('-')[0];
				if (!dates[lang])
					lang = $.fn.datepicker.defaults.language;
			}
			o.language = lang;

			switch(o.startView){
				case 2:
				case 'decade':
					o.startView = 2;
					break;
				case 1:
				case 'year':
					o.startView = 1;
					break;
				default:
					o.startView = 0;
			}

			switch (o.minViewMode) {
				case 1:
				case 'months':
					o.minViewMode = 1;
					break;
				case 2:
				case 'years':
					o.minViewMode = 2;
					break;
				default:
					o.minViewMode = 0;
			}

			o.startView = Math.max(o.startView, o.minViewMode);

			o.weekStart %= 7;
			o.weekEnd = ((o.weekStart + 6) % 7);

			var format = DPGlobal.parseFormat(o.format)
			if (o.startDate !== -Infinity) {
				o.startDate = DPGlobal.parseDate(o.startDate, format, o.language);
			}
			if (o.endDate !== Infinity) {
				o.endDate = DPGlobal.parseDate(o.endDate, format, o.language);
			}

			o.daysOfWeekDisabled = o.daysOfWeekDisabled||[];
			if (!$.isArray(o.daysOfWeekDisabled))
				o.daysOfWeekDisabled = o.daysOfWeekDisabled.split(/[,\s]*/);
			o.daysOfWeekDisabled = $.map(o.daysOfWeekDisabled, function (d) {
				return parseInt(d, 10);
			});
		},
		_events: [],
		_secondaryEvents: [],
		_applyEvents: function(evs){
			for (var i=0, el, ev; i<evs.length; i++){
				el = evs[i][0];
				ev = evs[i][1];
				el.on(ev);
			}
		},
		_unapplyEvents: function(evs){
			for (var i=0, el, ev; i<evs.length; i++){
				el = evs[i][0];
				ev = evs[i][1];
				el.off(ev);
			}
		},
		_buildEvents: function(){
			if (this.isInput) { // single input
				this._events = [
					[this.element, {
						focus: $.proxy(this.show, this),
						keyup: $.proxy(this.update, this),
						keydown: $.proxy(this.keydown, this)
					}]
				];
			}
			else if (this.component && this.hasInput){ // component: input + button
				this._events = [
					// For components that are not readonly, allow keyboard nav
					[this.element.find('input'), {
						focus: $.proxy(this.show, this),
						keyup: $.proxy(this.update, this),
						keydown: $.proxy(this.keydown, this)
					}],
					[this.component, {
						click: $.proxy(this.show, this)
					}]
				];
			}
			else if (this.element.is('div')) {  // inline datepicker
				this.isInline = true;
			}
			else {
				this._events = [
					[this.element, {
						click: $.proxy(this.show, this)
					}]
				];
			}

			this._secondaryEvents = [
				[this.picker, {
					click: $.proxy(this.click, this)
				}],
				[$(window), {
					resize: $.proxy(this.place, this)
				}],
				[$(document), {
					mousedown: $.proxy(function (e) {
						// Clicked outside the datepicker, hide it
						if (!(
							this.element.is(e.target) ||
							this.element.find(e.target).size() ||
							this.picker.is(e.target) ||
							this.picker.find(e.target).size()
						)) {
							this.hide();
						}
					}, this)
				}]
			];
		},
		_attachEvents: function(){
			this._detachEvents();
			this._applyEvents(this._events);
		},
		_detachEvents: function(){
			this._unapplyEvents(this._events);
		},
		_attachSecondaryEvents: function(){
			this._detachSecondaryEvents();
			this._applyEvents(this._secondaryEvents);
		},
		_detachSecondaryEvents: function(){
			this._unapplyEvents(this._secondaryEvents);
		},
		_trigger: function(event, altdate){
			var date = altdate || this.date,
				local_date = new Date(date.getTime() + (date.getTimezoneOffset()*60000));

			this.element.trigger({
				type: event,
				date: local_date,
				format: $.proxy(function(altformat){
					var format = altformat || this.o.format;
					return DPGlobal.formatDate(date, format, this.o.language);
				}, this)
			});
		},

		show: function(e) {
			if (!this.isInline)
				this.picker.appendTo('body');
			this.picker.show();
			this.height = this.component ? this.component.outerHeight() : this.element.outerHeight();
			this.place();
			this._attachSecondaryEvents();
			if (e) {
				e.preventDefault();
			}
			this._trigger('show');
		},

		hide: function(e){
			if(this.isInline) return;
			if (!this.picker.is(':visible')) return;
			this.picker.hide().detach();
			this._detachSecondaryEvents();
			this.viewMode = this.o.startView;
			this.showMode();

			if (
				this.o.forceParse &&
				(
					this.isInput && this.element.val() ||
					this.hasInput && this.element.find('input').val()
				)
			)
				this.setValue();
			this._trigger('hide');
		},

		remove: function() {
			this.hide();
			this._detachEvents();
			this._detachSecondaryEvents();
			this.picker.remove();
			delete this.element.data().datepicker;
			if (!this.isInput) {
				delete this.element.data().date;
			}
		},

		getDate: function() {
			var d = this.getUTCDate();
			return new Date(d.getTime() + (d.getTimezoneOffset()*60000));
		},

		getUTCDate: function() {
			return this.date;
		},

		setDate: function(d) {
			this.setUTCDate(new Date(d.getTime() - (d.getTimezoneOffset()*60000)));
		},

		setUTCDate: function(d) {
			this.date = d;
			this.setValue();
		},

		setValue: function() {
			var formatted = this.getFormattedDate();
			if (!this.isInput) {
				if (this.component){
					this.element.find('input').val(formatted);
				}
			} else {
				this.element.val(formatted);
			}
		},

		getFormattedDate: function(format) {
			if (format === undefined)
				format = this.o.format;
			return DPGlobal.formatDate(this.date, format, this.o.language);
		},

		setStartDate: function(startDate){
			this._process_options({startDate: startDate});
			this.update();
			this.updateNavArrows();
		},

		setEndDate: function(endDate){
			this._process_options({endDate: endDate});
			this.update();
			this.updateNavArrows();
		},

		setDaysOfWeekDisabled: function(daysOfWeekDisabled){
			this._process_options({daysOfWeekDisabled: daysOfWeekDisabled});
			this.update();
			this.updateNavArrows();
		},

		place: function(){
						if(this.isInline) return;
			var zIndex = parseInt(this.element.parents().filter(function() {
							return $(this).css('z-index') != 'auto';
						}).first().css('z-index'))+10;
			var offset = this.component ? this.component.parent().offset() : this.element.offset();
			var height = this.component ? this.component.outerHeight(true) : this.element.outerHeight(true);
			this.picker.css({
				top: offset.top + height,
				left: offset.left,
				zIndex: zIndex
			});
		},

		_allow_update: true,
		update: function(){
			if (!this._allow_update) return;

			var date, fromArgs = false;
			if(arguments && arguments.length && (typeof arguments[0] === 'string' || arguments[0] instanceof Date)) {
				date = arguments[0];
				fromArgs = true;
			} else {
				date = this.isInput ? this.element.val() : this.element.data('date') || this.element.find('input').val();
				delete this.element.data().date;
			}

			this.date = DPGlobal.parseDate(date, this.o.format, this.o.language);

			if(fromArgs) this.setValue();

			if (this.date < this.o.startDate) {
				this.viewDate = new Date(this.o.startDate);
			} else if (this.date > this.o.endDate) {
				this.viewDate = new Date(this.o.endDate);
			} else {
				this.viewDate = new Date(this.date);
			}
			this.fill();
		},

		fillDow: function(){
			var dowCnt = this.o.weekStart,
			html = '<tr>';
			if(this.o.calendarWeeks){
				var cell = '<th class="cw">&nbsp;</th>';
				html += cell;
				this.picker.find('.datepicker-days thead tr:first-child').prepend(cell);
			}
			while (dowCnt < this.o.weekStart + 7) {
				html += '<th class="dow">'+dates[this.o.language].daysMin[(dowCnt++)%7]+'</th>';
			}
			html += '</tr>';
			this.picker.find('.datepicker-days thead').append(html);
		},

		fillMonths: function(){
			var html = '',
			i = 0;
			while (i < 12) {
				html += '<span class="month">'+dates[this.o.language].monthsShort[i++]+'</span>';
			}
			this.picker.find('.datepicker-months td').html(html);
		},

		setRange: function(range){
			if (!range || !range.length)
				delete this.range;
			else
				this.range = $.map(range, function(d){ return d.valueOf(); });
			this.fill();
		},

		getClassNames: function(date){
			var cls = [],
				year = this.viewDate.getUTCFullYear(),
				month = this.viewDate.getUTCMonth(),
				currentDate = this.date.valueOf(),
				today = new Date();
			if (date.getUTCFullYear() < year || (date.getUTCFullYear() == year && date.getUTCMonth() < month)) {
				cls.push('old');
			} else if (date.getUTCFullYear() > year || (date.getUTCFullYear() == year && date.getUTCMonth() > month)) {
				cls.push('new');
			}
			// Compare internal UTC date with local today, not UTC today
			if (this.o.todayHighlight &&
				date.getUTCFullYear() == today.getFullYear() &&
				date.getUTCMonth() == today.getMonth() &&
				date.getUTCDate() == today.getDate()) {
				cls.push('today');
			}
			if (currentDate && date.valueOf() == currentDate) {
				cls.push('active');
			}
			if (date.valueOf() < this.o.startDate || date.valueOf() > this.o.endDate ||
				$.inArray(date.getUTCDay(), this.o.daysOfWeekDisabled) !== -1) {
				cls.push('disabled');
			}
			if (this.range){
				if (date > this.range[0] && date < this.range[this.range.length-1]){
					cls.push('range');
				}
				if ($.inArray(date.valueOf(), this.range) != -1){
					cls.push('selected');
				}
			}
			return cls;
		},

		fill: function() {
			var d = new Date(this.viewDate),
				year = d.getUTCFullYear(),
				month = d.getUTCMonth(),
				startYear = this.o.startDate !== -Infinity ? this.o.startDate.getUTCFullYear() : -Infinity,
				startMonth = this.o.startDate !== -Infinity ? this.o.startDate.getUTCMonth() : -Infinity,
				endYear = this.o.endDate !== Infinity ? this.o.endDate.getUTCFullYear() : Infinity,
				endMonth = this.o.endDate !== Infinity ? this.o.endDate.getUTCMonth() : Infinity,
				currentDate = this.date && this.date.valueOf(),
				tooltip;
			this.picker.find('.datepicker-days thead th.datepicker-switch')
						.text(dates[this.o.language].months[month]+' '+year);
			this.picker.find('tfoot th.today')
						.text(dates[this.o.language].today)
						.toggle(this.o.todayBtn !== false);
			this.picker.find('tfoot th.clear')
						.text(dates[this.o.language].clear)
						.toggle(this.o.clearBtn !== false);
			this.updateNavArrows();
			this.fillMonths();
			var prevMonth = UTCDate(year, month-1, 28,0,0,0,0),
				day = DPGlobal.getDaysInMonth(prevMonth.getUTCFullYear(), prevMonth.getUTCMonth());
			prevMonth.setUTCDate(day);
			prevMonth.setUTCDate(day - (prevMonth.getUTCDay() - this.o.weekStart + 7)%7);
			var nextMonth = new Date(prevMonth);
			nextMonth.setUTCDate(nextMonth.getUTCDate() + 42);
			nextMonth = nextMonth.valueOf();
			var html = [];
			var clsName;
			while(prevMonth.valueOf() < nextMonth) {
				if (prevMonth.getUTCDay() == this.o.weekStart) {
					html.push('<tr>');
					if(this.o.calendarWeeks){
						// ISO 8601: First week contains first thursday.
						// ISO also states week starts on Monday, but we can be more abstract here.
						var
							// Start of current week: based on weekstart/current date
							ws = new Date(+prevMonth + (this.o.weekStart - prevMonth.getUTCDay() - 7) % 7 * 864e5),
							// Thursday of this week
							th = new Date(+ws + (7 + 4 - ws.getUTCDay()) % 7 * 864e5),
							// First Thursday of year, year from thursday
							yth = new Date(+(yth = UTCDate(th.getUTCFullYear(), 0, 1)) + (7 + 4 - yth.getUTCDay())%7*864e5),
							// Calendar week: ms between thursdays, div ms per day, div 7 days
							calWeek =  (th - yth) / 864e5 / 7 + 1;
						html.push('<td class="cw">'+ calWeek +'</td>');

					}
				}
				clsName = this.getClassNames(prevMonth);
				clsName.push('day');

				var before = this.o.beforeShowDay(prevMonth);
				if (before === undefined)
					before = {};
				else if (typeof(before) === 'boolean')
					before = {enabled: before};
				else if (typeof(before) === 'string')
					before = {classes: before};
				if (before.enabled === false)
					clsName.push('disabled');
				if (before.classes)
					clsName = clsName.concat(before.classes.split(/\s+/));
				if (before.tooltip)
					tooltip = before.tooltip;

				clsName = $.unique(clsName);
				html.push('<td class="'+clsName.join(' ')+'"' + (tooltip ? ' title="'+tooltip+'"' : '') + '>'+prevMonth.getUTCDate() + '</td>');
				if (prevMonth.getUTCDay() == this.o.weekEnd) {
					html.push('</tr>');
				}
				prevMonth.setUTCDate(prevMonth.getUTCDate()+1);
			}
			this.picker.find('.datepicker-days tbody').empty().append(html.join(''));
			var currentYear = this.date && this.date.getUTCFullYear();

			var months = this.picker.find('.datepicker-months')
						.find('th:eq(1)')
							.text(year)
							.end()
						.find('span').removeClass('active');
			if (currentYear && currentYear == year) {
				months.eq(this.date.getUTCMonth()).addClass('active');
			}
			if (year < startYear || year > endYear) {
				months.addClass('disabled');
			}
			if (year == startYear) {
				months.slice(0, startMonth).addClass('disabled');
			}
			if (year == endYear) {
				months.slice(endMonth+1).addClass('disabled');
			}

			html = '';
			year = parseInt(year/10, 10) * 10;
			var yearCont = this.picker.find('.datepicker-years')
								.find('th:eq(1)')
									.text(year + '-' + (year + 9))
									.end()
								.find('td');
			year -= 1;
			for (var i = -1; i < 11; i++) {
				html += '<span class="year'+(i == -1 ? ' old' : i == 10 ? ' new' : '')+(currentYear == year ? ' active' : '')+(year < startYear || year > endYear ? ' disabled' : '')+'">'+year+'</span>';
				year += 1;
			}
			yearCont.html(html);
		},

		updateNavArrows: function() {
			if (!this._allow_update) return;

			var d = new Date(this.viewDate),
				year = d.getUTCFullYear(),
				month = d.getUTCMonth();
			switch (this.viewMode) {
				case 0:
					if (this.o.startDate !== -Infinity && year <= this.o.startDate.getUTCFullYear() && month <= this.o.startDate.getUTCMonth()) {
						this.picker.find('.prev').css({visibility: 'hidden'});
					} else {
						this.picker.find('.prev').css({visibility: 'visible'});
					}
					if (this.o.endDate !== Infinity && year >= this.o.endDate.getUTCFullYear() && month >= this.o.endDate.getUTCMonth()) {
						this.picker.find('.next').css({visibility: 'hidden'});
					} else {
						this.picker.find('.next').css({visibility: 'visible'});
					}
					break;
				case 1:
				case 2:
					if (this.o.startDate !== -Infinity && year <= this.o.startDate.getUTCFullYear()) {
						this.picker.find('.prev').css({visibility: 'hidden'});
					} else {
						this.picker.find('.prev').css({visibility: 'visible'});
					}
					if (this.o.endDate !== Infinity && year >= this.o.endDate.getUTCFullYear()) {
						this.picker.find('.next').css({visibility: 'hidden'});
					} else {
						this.picker.find('.next').css({visibility: 'visible'});
					}
					break;
			}
		},

		click: function(e) {
			e.preventDefault();
			var target = $(e.target).closest('span, td, th');
			if (target.length == 1) {
				switch(target[0].nodeName.toLowerCase()) {
					case 'th':
						switch(target[0].className) {
							case 'datepicker-switch':
								this.showMode(1);
								break;
							case 'prev':
							case 'next':
								var dir = DPGlobal.modes[this.viewMode].navStep * (target[0].className == 'prev' ? -1 : 1);
								switch(this.viewMode){
									case 0:
										this.viewDate = this.moveMonth(this.viewDate, dir);
										break;
									case 1:
									case 2:
										this.viewDate = this.moveYear(this.viewDate, dir);
										break;
								}
								this.fill();
								break;
							case 'today':
								var date = new Date();
								date = UTCDate(date.getFullYear(), date.getMonth(), date.getDate(), 0, 0, 0);

								this.showMode(-2);
								var which = this.o.todayBtn == 'linked' ? null : 'view';
								this._setDate(date, which);
								break;
							case 'clear':
								var element;
								if (this.isInput)
									element = this.element;
								else if (this.component)
									element = this.element.find('input');
								if (element)
									element.val("").change();
								this._trigger('changeDate');
								this.update();
								if (this.o.autoclose)
									this.hide();
								break;
						}
						break;
					case 'span':
						if (!target.is('.disabled')) {
							this.viewDate.setUTCDate(1);
							if (target.is('.month')) {
								var day = 1;
								var month = target.parent().find('span').index(target);
								var year = this.viewDate.getUTCFullYear();
								this.viewDate.setUTCMonth(month);
								this._trigger('changeMonth', this.viewDate);
								if (this.o.minViewMode === 1) {
									this._setDate(UTCDate(year, month, day,0,0,0,0));
								}
							} else {
								var year = parseInt(target.text(), 10)||0;
								var day = 1;
								var month = 0;
								this.viewDate.setUTCFullYear(year);
								this._trigger('changeYear', this.viewDate);
								if (this.o.minViewMode === 2) {
									this._setDate(UTCDate(year, month, day,0,0,0,0));
								}
							}
							this.showMode(-1);
							this.fill();
						}
						break;
					case 'td':
						if (target.is('.day') && !target.is('.disabled')){
							var day = parseInt(target.text(), 10)||1;
							var year = this.viewDate.getUTCFullYear(),
								month = this.viewDate.getUTCMonth();
							if (target.is('.old')) {
								if (month === 0) {
									month = 11;
									year -= 1;
								} else {
									month -= 1;
								}
							} else if (target.is('.new')) {
								if (month == 11) {
									month = 0;
									year += 1;
								} else {
									month += 1;
								}
							}
							this._setDate(UTCDate(year, month, day,0,0,0,0));
						}
						break;
				}
			}
		},

		_setDate: function(date, which){
			if (!which || which == 'date')
				this.date = new Date(date);
			if (!which || which  == 'view')
				this.viewDate = new Date(date);
			this.fill();
			this.setValue();
			this._trigger('changeDate');
			var element;
			if (this.isInput) {
				element = this.element;
			} else if (this.component){
				element = this.element.find('input');
			}
			if (element) {
				element.change();
				if (this.o.autoclose && (!which || which == 'date')) {
					this.hide();
				}
			}
		},

		moveMonth: function(date, dir){
			if (!dir) return date;
			var new_date = new Date(date.valueOf()),
				day = new_date.getUTCDate(),
				month = new_date.getUTCMonth(),
				mag = Math.abs(dir),
				new_month, test;
			dir = dir > 0 ? 1 : -1;
			if (mag == 1){
				test = dir == -1
					// If going back one month, make sure month is not current month
					// (eg, Mar 31 -> Feb 31 == Feb 28, not Mar 02)
					? function(){ return new_date.getUTCMonth() == month; }
					// If going forward one month, make sure month is as expected
					// (eg, Jan 31 -> Feb 31 == Feb 28, not Mar 02)
					: function(){ return new_date.getUTCMonth() != new_month; };
				new_month = month + dir;
				new_date.setUTCMonth(new_month);
				// Dec -> Jan (12) or Jan -> Dec (-1) -- limit expected date to 0-11
				if (new_month < 0 || new_month > 11)
					new_month = (new_month + 12) % 12;
			} else {
				// For magnitudes >1, move one month at a time...
				for (var i=0; i<mag; i++)
					// ...which might decrease the day (eg, Jan 31 to Feb 28, etc)...
					new_date = this.moveMonth(new_date, dir);
				// ...then reset the day, keeping it in the new month
				new_month = new_date.getUTCMonth();
				new_date.setUTCDate(day);
				test = function(){ return new_month != new_date.getUTCMonth(); };
			}
			// Common date-resetting loop -- if date is beyond end of month, make it
			// end of month
			while (test()){
				new_date.setUTCDate(--day);
				new_date.setUTCMonth(new_month);
			}
			return new_date;
		},

		moveYear: function(date, dir){
			return this.moveMonth(date, dir*12);
		},

		dateWithinRange: function(date){
			return date >= this.o.startDate && date <= this.o.endDate;
		},

		keydown: function(e){
			if (this.picker.is(':not(:visible)')){
				if (e.keyCode == 27) // allow escape to hide and re-show picker
					this.show();
				return;
			}
			var dateChanged = false,
				dir, day, month,
				newDate, newViewDate;
			switch(e.keyCode){
				case 27: // escape
					this.hide();
					e.preventDefault();
					break;
				case 37: // left
				case 39: // right
					if (!this.o.keyboardNavigation) break;
					dir = e.keyCode == 37 ? -1 : 1;
					if (e.ctrlKey){
						newDate = this.moveYear(this.date, dir);
						newViewDate = this.moveYear(this.viewDate, dir);
					} else if (e.shiftKey){
						newDate = this.moveMonth(this.date, dir);
						newViewDate = this.moveMonth(this.viewDate, dir);
					} else {
						newDate = new Date(this.date);
						newDate.setUTCDate(this.date.getUTCDate() + dir);
						newViewDate = new Date(this.viewDate);
						newViewDate.setUTCDate(this.viewDate.getUTCDate() + dir);
					}
					if (this.dateWithinRange(newDate)){
						this.date = newDate;
						this.viewDate = newViewDate;
						this.setValue();
						this.update();
						e.preventDefault();
						dateChanged = true;
					}
					break;
				case 38: // up
				case 40: // down
					if (!this.o.keyboardNavigation) break;
					dir = e.keyCode == 38 ? -1 : 1;
					if (e.ctrlKey){
						newDate = this.moveYear(this.date, dir);
						newViewDate = this.moveYear(this.viewDate, dir);
					} else if (e.shiftKey){
						newDate = this.moveMonth(this.date, dir);
						newViewDate = this.moveMonth(this.viewDate, dir);
					} else {
						newDate = new Date(this.date);
						newDate.setUTCDate(this.date.getUTCDate() + dir * 7);
						newViewDate = new Date(this.viewDate);
						newViewDate.setUTCDate(this.viewDate.getUTCDate() + dir * 7);
					}
					if (this.dateWithinRange(newDate)){
						this.date = newDate;
						this.viewDate = newViewDate;
						this.setValue();
						this.update();
						e.preventDefault();
						dateChanged = true;
					}
					break;
				case 13: // enter
					this.hide();
					e.preventDefault();
					break;
				case 9: // tab
					this.hide();
					break;
			}
			if (dateChanged){
				this._trigger('changeDate');
				var element;
				if (this.isInput) {
					element = this.element;
				} else if (this.component){
					element = this.element.find('input');
				}
				if (element) {
					element.change();
				}
			}
		},

		showMode: function(dir) {
			if (dir) {
				this.viewMode = Math.max(this.o.minViewMode, Math.min(2, this.viewMode + dir));
			}
			/*
				vitalets: fixing bug of very special conditions:
				jquery 1.7.1 + webkit + show inline datepicker in bootstrap popover.
				Method show() does not set display css correctly and datepicker is not shown.
				Changed to .css('display', 'block') solve the problem.
				See https://github.com/vitalets/x-editable/issues/37

				In jquery 1.7.2+ everything works fine.
			*/
			//this.picker.find('>div').hide().filter('.datepicker-'+DPGlobal.modes[this.viewMode].clsName).show();
			this.picker.find('>div').hide().filter('.datepicker-'+DPGlobal.modes[this.viewMode].clsName).css('display', 'block');
			this.updateNavArrows();
		}
	};

	var DateRangePicker = function(element, options){
		this.element = $(element);
		this.inputs = $.map(options.inputs, function(i){ return i.jquery ? i[0] : i; });
		delete options.inputs;

		$(this.inputs)
			.datepicker(options)
			.bind('changeDate', $.proxy(this.dateUpdated, this));

		this.pickers = $.map(this.inputs, function(i){ return $(i).data('datepicker'); });
		this.updateDates();
	};
	DateRangePicker.prototype = {
		updateDates: function(){
			this.dates = $.map(this.pickers, function(i){ return i.date; });
			this.updateRanges();
		},
		updateRanges: function(){
			var range = $.map(this.dates, function(d){ return d.valueOf(); });
			$.each(this.pickers, function(i, p){
				p.setRange(range);
			});
		},
		dateUpdated: function(e){
			var dp = $(e.target).data('datepicker'),
				new_date = dp.getUTCDate(),
				i = $.inArray(e.target, this.inputs),
				l = this.inputs.length;
			if (i == -1) return;

			if (new_date < this.dates[i]){
				// Date being moved earlier/left
				while (i>=0 && new_date < this.dates[i]){
					this.pickers[i--].setUTCDate(new_date);
				}
			}
			else if (new_date > this.dates[i]){
				// Date being moved later/right
				while (i<l && new_date > this.dates[i]){
					this.pickers[i++].setUTCDate(new_date);
				}
			}
			this.updateDates();
		},
		remove: function(){
			$.map(this.pickers, function(p){ p.remove(); });
			delete this.element.data().datepicker;
		}
	};

	function opts_from_el(el, prefix){
		// Derive options from element data-attrs
		var data = $(el).data(),
			out = {}, inkey,
			replace = new RegExp('^' + prefix.toLowerCase() + '([A-Z])'),
			prefix = new RegExp('^' + prefix.toLowerCase());
		for (var key in data)
			if (prefix.test(key)){
				inkey = key.replace(replace, function(_,a){ return a.toLowerCase(); });
				out[inkey] = data[key];
			}
		return out;
	}

	function opts_from_locale(lang){
		// Derive options from locale plugins
		var out = {};
		// Check if "de-DE" style date is available, if not language should
		// fallback to 2 letter code eg "de"
		if (!dates[lang]) {
			lang = lang.split('-')[0]
			if (!dates[lang])
				return;
		}
		var d = dates[lang];
		$.each($.fn.datepicker.locale_opts, function(i,k){
			if (k in d)
				out[k] = d[k];
		});
		return out;
	}

	var old = $.fn.datepicker;
	$.fn.datepicker = function ( option ) {
		var args = Array.apply(null, arguments);
		args.shift();
		var internal_return,
			this_return;
		this.each(function () {
			var $this = $(this),
				data = $this.data('datepicker'),
				options = typeof option == 'object' && option;
			if (!data) {
				var elopts = opts_from_el(this, 'date'),
					// Preliminary otions
					xopts = $.extend({}, $.fn.datepicker.defaults, elopts, options),
					locopts = opts_from_locale(xopts.language),
					// Options priority: js args, data-attrs, locales, defaults
					opts = $.extend({}, $.fn.datepicker.defaults, locopts, elopts, options);
				if ($this.is('.input-daterange') || opts.inputs){
					var ropts = {
						inputs: opts.inputs || $this.find('input').toArray()
					};
					$this.data('datepicker', (data = new DateRangePicker(this, $.extend(opts, ropts))));
				}
				else{
					$this.data('datepicker', (data = new Datepicker(this, opts)));
				}
			}
			if (typeof option == 'string' && typeof data[option] == 'function') {
				internal_return = data[option].apply(data, args);
				if (internal_return !== undefined)
					return false;
			}
		});
		if (internal_return !== undefined)
			return internal_return;
		else
			return this;
	};

	$.fn.datepicker.defaults = {
		autoclose: false,
		beforeShowDay: $.noop,
		calendarWeeks: false,
		clearBtn: false,
		daysOfWeekDisabled: [],
		endDate: Infinity,
		forceParse: true,
		format: 'mm/dd/yyyy',
		keyboardNavigation: true,
		language: 'en',
		minViewMode: 0,
		rtl: false,
		startDate: -Infinity,
		startView: 0,
		todayBtn: false,
		todayHighlight: false,
		weekStart: 0
	};
	$.fn.datepicker.locale_opts = [
		'format',
		'rtl',
		'weekStart'
	];
	$.fn.datepicker.Constructor = Datepicker;
	var dates = $.fn.datepicker.dates = {
		en: {
			days: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
			daysShort: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
			daysMin: ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"],
			months: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
			monthsShort: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
			today: "Today",
			clear: "Clear"
		}
	};

	var DPGlobal = {
		modes: [
			{
				clsName: 'days',
				navFnc: 'Month',
				navStep: 1
			},
			{
				clsName: 'months',
				navFnc: 'FullYear',
				navStep: 1
			},
			{
				clsName: 'years',
				navFnc: 'FullYear',
				navStep: 10
		}],
		isLeapYear: function (year) {
			return (((year % 4 === 0) && (year % 100 !== 0)) || (year % 400 === 0));
		},
		getDaysInMonth: function (year, month) {
			return [31, (DPGlobal.isLeapYear(year) ? 29 : 28), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month];
		},
		validParts: /dd?|DD?|mm?|MM?|yy(?:yy)?/g,
		nonpunctuation: /[^ -\/:-@\[\u3400-\u9fff-`{-~\t\n\r]+/g,
		parseFormat: function(format){
			// IE treats \0 as a string end in inputs (truncating the value),
			// so it's a bad format delimiter, anyway
			var separators = format.replace(this.validParts, '\0').split('\0'),
				parts = format.match(this.validParts);
			if (!separators || !separators.length || !parts || parts.length === 0){
				throw new Error("Invalid date format.");
			}
			return {separators: separators, parts: parts};
		},
		parseDate: function(date, format, language) {
			if (date instanceof Date) return date;
			if (typeof format === 'string')
				format = DPGlobal.parseFormat(format);
			if (/^[\-+]\d+[dmwy]([\s,]+[\-+]\d+[dmwy])*$/.test(date)) {
				var part_re = /([\-+]\d+)([dmwy])/,
					parts = date.match(/([\-+]\d+)([dmwy])/g),
					part, dir;
				date = new Date();
				for (var i=0; i<parts.length; i++) {
					part = part_re.exec(parts[i]);
					dir = parseInt(part[1]);
					switch(part[2]){
						case 'd':
							date.setUTCDate(date.getUTCDate() + dir);
							break;
						case 'm':
							date = Datepicker.prototype.moveMonth.call(Datepicker.prototype, date, dir);
							break;
						case 'w':
							date.setUTCDate(date.getUTCDate() + dir * 7);
							break;
						case 'y':
							date = Datepicker.prototype.moveYear.call(Datepicker.prototype, date, dir);
							break;
					}
				}
				return UTCDate(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate(), 0, 0, 0);
			}
			var parts = date && date.match(this.nonpunctuation) || [],
				date = new Date(),
				parsed = {},
				setters_order = ['yyyy', 'yy', 'M', 'MM', 'm', 'mm', 'd', 'dd'],
				setters_map = {
					yyyy: function(d,v){ return d.setUTCFullYear(v); },
					yy: function(d,v){ return d.setUTCFullYear(2000+v); },
					m: function(d,v){
						v -= 1;
						while (v<0) v += 12;
						v %= 12;
						d.setUTCMonth(v);
						while (d.getUTCMonth() != v)
							d.setUTCDate(d.getUTCDate()-1);
						return d;
					},
					d: function(d,v){ return d.setUTCDate(v); }
				},
				val, filtered, part;
			setters_map['M'] = setters_map['MM'] = setters_map['mm'] = setters_map['m'];
			setters_map['dd'] = setters_map['d'];
			date = UTCDate(date.getFullYear(), date.getMonth(), date.getDate(), 0, 0, 0);
			var fparts = format.parts.slice();
			// Remove noop parts
			if (parts.length != fparts.length) {
				fparts = $(fparts).filter(function(i,p){
					return $.inArray(p, setters_order) !== -1;
				}).toArray();
			}
			// Process remainder
			if (parts.length == fparts.length) {
				for (var i=0, cnt = fparts.length; i < cnt; i++) {
					val = parseInt(parts[i], 10);
					part = fparts[i];
					if (isNaN(val)) {
						switch(part) {
							case 'MM':
								filtered = $(dates[language].months).filter(function(){
									var m = this.slice(0, parts[i].length),
										p = parts[i].slice(0, m.length);
									return m == p;
								});
								val = $.inArray(filtered[0], dates[language].months) + 1;
								break;
							case 'M':
								filtered = $(dates[language].monthsShort).filter(function(){
									var m = this.slice(0, parts[i].length),
										p = parts[i].slice(0, m.length);
									return m == p;
								});
								val = $.inArray(filtered[0], dates[language].monthsShort) + 1;
								break;
						}
					}
					parsed[part] = val;
				}
				for (var i=0, s; i<setters_order.length; i++){
					s = setters_order[i];
					if (s in parsed && !isNaN(parsed[s]))
						setters_map[s](date, parsed[s]);
				}
			}
			return date;
		},
		formatDate: function(date, format, language){
			if (typeof format === 'string')
				format = DPGlobal.parseFormat(format);
			var val = {
				d: date.getUTCDate(),
				D: dates[language].daysShort[date.getUTCDay()],
				DD: dates[language].days[date.getUTCDay()],
				m: date.getUTCMonth() + 1,
				M: dates[language].monthsShort[date.getUTCMonth()],
				MM: dates[language].months[date.getUTCMonth()],
				yy: date.getUTCFullYear().toString().substring(2),
				yyyy: date.getUTCFullYear()
			};
			val.dd = (val.d < 10 ? '0' : '') + val.d;
			val.mm = (val.m < 10 ? '0' : '') + val.m;
			var date = [],
				seps = $.extend([], format.separators);
			for (var i=0, cnt = format.parts.length; i <= cnt; i++) {
				if (seps.length)
					date.push(seps.shift());
				date.push(val[format.parts[i]]);
			}
			return date.join('');
		}, 
		// Classes have been changed below FROM -->> "icon-arrow-left"    TO -->> "glyphicon-arrow-left"  (same with right arrow)
		// This was done because we have upgraded to BootStrap 3 while the library used BootStrap 2 classes and it wasn't under development
		headTemplate: '<thead>'+
							'<tr>'+
								'<th class="prev"><i class="glyphicon glyphicon-arrow-left"/></th>'+
								'<th colspan="5" class="datepicker-switch"></th>'+
								'<th class="next"><i class="glyphicon glyphicon-arrow-right"/></th>'+
							'</tr>'+
						'</thead>',
		contTemplate: '<tbody><tr><td colspan="7"></td></tr></tbody>',
		footTemplate: '<tfoot><tr><th colspan="7" class="today"></th></tr><tr><th colspan="7" class="clear"></th></tr></tfoot>'
	};
	DPGlobal.template = '<div class="datepicker">'+
							'<div class="datepicker-days">'+
								'<table class=" table-condensed">'+
									DPGlobal.headTemplate+
									'<tbody></tbody>'+
									DPGlobal.footTemplate+
								'</table>'+
							'</div>'+
							'<div class="datepicker-months">'+
								'<table class="table-condensed">'+
									DPGlobal.headTemplate+
									DPGlobal.contTemplate+
									DPGlobal.footTemplate+
								'</table>'+
							'</div>'+
							'<div class="datepicker-years">'+
								'<table class="table-condensed">'+
									DPGlobal.headTemplate+
									DPGlobal.contTemplate+
									DPGlobal.footTemplate+
								'</table>'+
							'</div>'+
						'</div>';

	$.fn.datepicker.DPGlobal = DPGlobal;


	/* DATEPICKER NO CONFLICT
	* =================== */

	$.fn.datepicker.noConflict = function(){
		$.fn.datepicker = old;
		return this;
	};


	/* DATEPICKER DATA-API
	* ================== */

	$(document).on(
		'focus.datepicker.data-api click.datepicker.data-api',
		'[data-provide="datepicker"]',
		function(e){
			var $this = $(this);
			if ($this.data('datepicker')) return;
			e.preventDefault();
			// component click requires us to explicitly show it
			$this.datepicker('show');
		}
	);
	$(function(){
		$('[data-provide="datepicker-inline"]').datepicker();
	});

}( window.jQuery ));

define("date_picker", function(){});

/*! Bootstrap-Timepicker v0.1.0 
* http://jdewit.github.com/bootstrap-timepicker 
* Copyright (c) 2013 Joris de Wit 
* MIT License 
*/
(function(e,t,n,r){"use strict";var i=function(t,n){this.widget="",this.$element=e(t),this.defaultTime=n.defaultTime,this.disableFocus=n.disableFocus,this.isOpen=n.isOpen,this.minuteStep=n.minuteStep,this.modalBackdrop=n.modalBackdrop,this.secondStep=n.secondStep,this.showInputs=n.showInputs,this.showMeridian=n.showMeridian,this.showSeconds=n.showSeconds,this.template=n.template,this.appendWidgetTo=n.appendWidgetTo,this._init()};i.prototype={constructor:i,_init:function(){var t=this;this.$element.parent().hasClass("input-append")||this.$element.parent().hasClass("input-prepend")?(this.$element.parent(".input-append, .input-prepend").find(".add-on").on({"click.timepicker":e.proxy(this.showWidget,this)}),this.$element.on({"focus.timepicker":e.proxy(this.highlightUnit,this),"click.timepicker":e.proxy(this.highlightUnit,this),"keydown.timepicker":e.proxy(this.elementKeydown,this),"blur.timepicker":e.proxy(this.blurElement,this)})):this.template?this.$element.on({"focus.timepicker":e.proxy(this.showWidget,this),"click.timepicker":e.proxy(this.showWidget,this),"blur.timepicker":e.proxy(this.blurElement,this)}):this.$element.on({"focus.timepicker":e.proxy(this.highlightUnit,this),"click.timepicker":e.proxy(this.highlightUnit,this),"keydown.timepicker":e.proxy(this.elementKeydown,this),"blur.timepicker":e.proxy(this.blurElement,this)}),this.template!==!1?this.$widget=e(this.getTemplate()).appendTo(this.$element.parents(this.appendWidgetTo)).on("click",e.proxy(this.widgetClick,this)):this.$widget=!1,this.showInputs&&this.$widget!==!1&&this.$widget.find("input").each(function(){e(this).on({"click.timepicker":function(){e(this).select()},"keydown.timepicker":e.proxy(t.widgetKeydown,t)})}),this.setDefaultTime(this.defaultTime)},blurElement:function(){this.highlightedUnit=r,this.updateFromElementVal()},decrementHour:function(){if(this.showMeridian)if(this.hour===1)this.hour=12;else{if(this.hour===12)return this.hour--,this.toggleMeridian();if(this.hour===0)return this.hour=11,this.toggleMeridian();this.hour--}else this.hour===0?this.hour=23:this.hour--;this.update()},decrementMinute:function(e){var t;e?t=this.minute-e:t=this.minute-this.minuteStep,t<0?(this.decrementHour(),this.minute=t+60):this.minute=t,this.update()},decrementSecond:function(){var e=this.second-this.secondStep;e<0?(this.decrementMinute(!0),this.second=e+60):this.second=e,this.update()},elementKeydown:function(e){switch(e.keyCode){case 9:this.updateFromElementVal();switch(this.highlightedUnit){case"hour":e.preventDefault(),this.highlightNextUnit();break;case"minute":if(this.showMeridian||this.showSeconds)e.preventDefault(),this.highlightNextUnit();break;case"second":this.showMeridian&&(e.preventDefault(),this.highlightNextUnit())}break;case 27:this.updateFromElementVal();break;case 37:e.preventDefault(),this.highlightPrevUnit(),this.updateFromElementVal();break;case 38:e.preventDefault();switch(this.highlightedUnit){case"hour":this.incrementHour(),this.highlightHour();break;case"minute":this.incrementMinute(),this.highlightMinute();break;case"second":this.incrementSecond(),this.highlightSecond();break;case"meridian":this.toggleMeridian(),this.highlightMeridian()}break;case 39:e.preventDefault(),this.updateFromElementVal(),this.highlightNextUnit();break;case 40:e.preventDefault();switch(this.highlightedUnit){case"hour":this.decrementHour(),this.highlightHour();break;case"minute":this.decrementMinute(),this.highlightMinute();break;case"second":this.decrementSecond(),this.highlightSecond();break;case"meridian":this.toggleMeridian(),this.highlightMeridian()}}},formatTime:function(e,t,n,r){return e=e<10?"0"+e:e,t=t<10?"0"+t:t,n=n<10?"0"+n:n,e+":"+t+(this.showSeconds?":"+n:"")+(this.showMeridian?" "+r:"")},getCursorPosition:function(){var e=this.$element.get(0);if("selectionStart"in e)return e.selectionStart;if(n.selection){e.focus();var t=n.selection.createRange(),r=n.selection.createRange().text.length;return t.moveStart("character",-e.value.length),t.text.length-r}},getTemplate:function(){var e,t,n,r,i,s;this.showInputs?(t='<input type="text" name="hour" class="bootstrap-timepicker-hour" maxlength="2"/>',n='<input type="text" name="minute" class="bootstrap-timepicker-minute" maxlength="2"/>',r='<input type="text" name="second" class="bootstrap-timepicker-second" maxlength="2"/>',i='<input type="text" name="meridian" class="bootstrap-timepicker-meridian" maxlength="2"/>'):(t='<span class="bootstrap-timepicker-hour"></span>',n='<span class="bootstrap-timepicker-minute"></span>',r='<span class="bootstrap-timepicker-second"></span>',i='<span class="bootstrap-timepicker-meridian"></span>'),s='<table><tr><td><a href="#" data-action="incrementHour"><i class="glyphicon glyphicon-chevron-up"></i></a></td><td class="separator">&nbsp;</td><td><a href="#" data-action="incrementMinute"><i class="glyphicon glyphicon-chevron-up"></i></a></td>'+(this.showSeconds?'<td class="separator">&nbsp;</td><td><a href="#" data-action="incrementSecond"><i class="glyphicon glyphicon-chevron-up"></i></a></td>':"")+(this.showMeridian?'<td class="separator">&nbsp;</td><td class="meridian-column"><a href="#" data-action="toggleMeridian"><i class="glyphicon glyphicon-chevron-up"></i></a></td>':"")+"</tr>"+"<tr>"+"<td>"+t+"</td> "+'<td class="separator">:</td>'+"<td>"+n+"</td> "+(this.showSeconds?'<td class="separator">:</td><td>'+r+"</td>":"")+(this.showMeridian?'<td class="separator">&nbsp;</td><td>'+i+"</td>":"")+"</tr>"+"<tr>"+'<td><a href="#" data-action="decrementHour"><i class="glyphicon glyphicon-chevron-down"></i></a></td>'+'<td class="separator"></td>'+'<td><a href="#" data-action="decrementMinute"><i class="glyphicon glyphicon-chevron-down"></i></a></td>'+(this.showSeconds?'<td class="separator">&nbsp;</td><td><a href="#" data-action="decrementSecond"><i class="glyphicon glyphicon-chevron-down"></i></a></td>':"")+(this.showMeridian?'<td class="separator">&nbsp;</td><td><a href="#" data-action="toggleMeridian"><i class="glyphicon glyphicon-chevron-down"></i></a></td>':"")+"</tr>"+"</table>";switch(this.template){case"modal":e='<div class="bootstrap-timepicker-widget modal hide fade in" data-backdrop="'+(this.modalBackdrop?"true":"false")+'">'+'<div class="modal-header">'+'<a href="#" class="close" data-dismiss="modal">×</a>'+"<h3>Pick a Time</h3>"+"</div>"+'<div class="modal-content">'+s+"</div>"+'<div class="modal-footer">'+'<a href="#" class="btn btn-primary" data-dismiss="modal">OK</a>'+"</div>"+"</div>";break;case"dropdown":e='<div class="bootstrap-timepicker-widget dropdown-menu">'+s+"</div>"}return e},getTime:function(){return this.formatTime(this.hour,this.minute,this.second,this.meridian)},hideWidget:function(){if(this.isOpen===!1)return;this.showInputs&&this.updateFromWidgetInputs(),this.$element.trigger({type:"hide.timepicker",time:{value:this.getTime(),hours:this.hour,minutes:this.minute,seconds:this.second,meridian:this.meridian}}),this.template==="modal"?this.$widget.modal("hide"):this.$widget.removeClass("open"),e(n).off("mousedown.timepicker"),this.isOpen=!1},highlightUnit:function(){this.position=this.getCursorPosition(),this.position>=0&&this.position<=2?this.highlightHour():this.position>=3&&this.position<=5?this.highlightMinute():this.position>=6&&this.position<=8?this.showSeconds?this.highlightSecond():this.highlightMeridian():this.position>=9&&this.position<=11&&this.highlightMeridian()},highlightNextUnit:function(){switch(this.highlightedUnit){case"hour":this.highlightMinute();break;case"minute":this.showSeconds?this.highlightSecond():this.showMeridian?this.highlightMeridian():this.highlightHour();break;case"second":this.showMeridian?this.highlightMeridian():this.highlightHour();break;case"meridian":this.highlightHour()}},highlightPrevUnit:function(){switch(this.highlightedUnit){case"hour":this.highlightMeridian();break;case"minute":this.highlightHour();break;case"second":this.highlightMinute();break;case"meridian":this.showSeconds?this.highlightSecond():this.highlightMinute()}},highlightHour:function(){var e=this.$element.get(0);this.highlightedUnit="hour",e.setSelectionRange&&setTimeout(function(){e.setSelectionRange(0,2)},0)},highlightMinute:function(){var e=this.$element.get(0);this.highlightedUnit="minute",e.setSelectionRange&&setTimeout(function(){e.setSelectionRange(3,5)},0)},highlightSecond:function(){var e=this.$element.get(0);this.highlightedUnit="second",e.setSelectionRange&&setTimeout(function(){e.setSelectionRange(6,8)},0)},highlightMeridian:function(){var e=this.$element.get(0);this.highlightedUnit="meridian",e.setSelectionRange&&(this.showSeconds?setTimeout(function(){e.setSelectionRange(9,11)},0):setTimeout(function(){e.setSelectionRange(6,8)},0))},incrementHour:function(){if(this.showMeridian){if(this.hour===11)return this.hour++,this.toggleMeridian();this.hour===12&&(this.hour=0)}if(this.hour===23)return this.hour=0;this.hour++,this.update()},incrementMinute:function(e){var t;e?t=this.minute+e:t=this.minute+this.minuteStep-this.minute%this.minuteStep,t>59?(this.incrementHour(),this.minute=t-60):this.minute=t,this.update()},incrementSecond:function(){var e=this.second+this.secondStep-this.second%this.secondStep;e>59?(this.incrementMinute(!0),this.second=e-60):this.second=e,this.update()},remove:function(){e("document").off(".timepicker"),this.$widget&&this.$widget.remove(),delete this.$element.data().timepicker},setDefaultTime:function(e){if(!this.$element.val())if(e==="current"){var t=new Date,n=t.getHours(),r=Math.floor(t.getMinutes()/this.minuteStep)*this.minuteStep,i=Math.floor(t.getSeconds()/this.secondStep)*this.secondStep,s="AM";this.showMeridian&&(n===0?n=12:n>=12?(n>12&&(n-=12),s="PM"):s="AM"),this.hour=n,this.minute=r,this.second=i,this.meridian=s,this.update()}else e===!1?(this.hour=0,this.minute=0,this.second=0,this.meridian="AM"):this.setTime(e);else this.updateFromElementVal()},setTime:function(e){var t,n;this.showMeridian?(t=e.split(" "),n=t[0].split(":"),this.meridian=t[1]):n=e.split(":"),this.hour=parseInt(n[0],10),this.minute=parseInt(n[1],10),this.second=parseInt(n[2],10),isNaN(this.hour)&&(this.hour=0),isNaN(this.minute)&&(this.minute=0);if(this.showMeridian){this.hour>12?this.hour=12:this.hour<1&&(this.hour=12);if(this.meridian==="am"||this.meridian==="a")this.meridian="AM";else if(this.meridian==="pm"||this.meridian==="p")this.meridian="PM";this.meridian!=="AM"&&this.meridian!=="PM"&&(this.meridian="AM")}else this.hour>=24?this.hour=23:this.hour<0&&(this.hour=0);this.minute<0?this.minute=0:this.minute>=60&&(this.minute=59),this.showSeconds&&(isNaN(this.second)?this.second=0:this.second<0?this.second=0:this.second>=60&&(this.second=59)),this.update()},showWidget:function(){if(this.isOpen)return;var t=this;e(n).on("mousedown.timepicker",function(n){e(n.target).closest(".bootstrap-timepicker-widget").length===0&&t.hideWidget()}),this.$element.trigger({type:"show.timepicker",time:{value:this.getTime(),hours:this.hour,minutes:this.minute,seconds:this.second,meridian:this.meridian}}),this.disableFocus&&this.$element.blur(),this.updateFromElementVal(),this.template==="modal"?this.$widget.modal("show").on("hidden",e.proxy(this.hideWidget,this)):this.isOpen===!1&&this.$widget.addClass("open"),this.isOpen=!0},toggleMeridian:function(){this.meridian=this.meridian==="AM"?"PM":"AM",this.update()},update:function(){this.$element.trigger({type:"changeTime.timepicker",time:{value:this.getTime(),hours:this.hour,minutes:this.minute,seconds:this.second,meridian:this.meridian}}),this.updateElement(),this.updateWidget()},updateElement:function(){this.$element.val(this.getTime()).change()},updateFromElementVal:function(){var e=this.$element.val();e&&this.setTime(e)},updateWidget:function(){if(this.$widget===!1)return;var e=this.hour<10?"0"+this.hour:this.hour,t=this.minute<10?"0"+this.minute:this.minute,n=this.second<10?"0"+this.second:this.second;this.showInputs?(this.$widget.find("input.bootstrap-timepicker-hour").val(e),this.$widget.find("input.bootstrap-timepicker-minute").val(t),this.showSeconds&&this.$widget.find("input.bootstrap-timepicker-second").val(n),this.showMeridian&&this.$widget.find("input.bootstrap-timepicker-meridian").val(this.meridian)):(this.$widget.find("span.bootstrap-timepicker-hour").text(e),this.$widget.find("span.bootstrap-timepicker-minute").text(t),this.showSeconds&&this.$widget.find("span.bootstrap-timepicker-second").text(n),this.showMeridian&&this.$widget.find("span.bootstrap-timepicker-meridian").text(this.meridian))},updateFromWidgetInputs:function(){if(this.$widget===!1)return;var t=e("input.bootstrap-timepicker-hour",this.$widget).val()+":"+e("input.bootstrap-timepicker-minute",this.$widget).val()+(this.showSeconds?":"+e("input.bootstrap-timepicker-second",this.$widget).val():"")+(this.showMeridian?" "+e("input.bootstrap-timepicker-meridian",this.$widget).val():"");this.setTime(t)},widgetClick:function(t){t.stopPropagation(),t.preventDefault();var n=e(t.target).closest("a").data("action");n&&this[n]()},widgetKeydown:function(t){var n=e(t.target).closest("input"),r=n.attr("name");switch(t.keyCode){case 9:if(this.showMeridian){if(r==="meridian")return this.hideWidget()}else if(this.showSeconds){if(r==="second")return this.hideWidget()}else if(r==="minute")return this.hideWidget();this.updateFromWidgetInputs();break;case 27:this.hideWidget();break;case 38:t.preventDefault();switch(r){case"hour":this.incrementHour();break;case"minute":this.incrementMinute();break;case"second":this.incrementSecond();break;case"meridian":this.toggleMeridian()}break;case 40:t.preventDefault();switch(r){case"hour":this.decrementHour();break;case"minute":this.decrementMinute();break;case"second":this.decrementSecond();break;case"meridian":this.toggleMeridian()}}}},e.fn.timepicker=function(t){var n=Array.apply(null,arguments);return n.shift(),this.each(function(){var r=e(this),s=r.data("timepicker"),o=typeof t=="object"&&t;s||r.data("timepicker",s=new i(this,e.extend({},e.fn.timepicker.defaults,o,e(this).data()))),typeof t=="string"&&s[t].apply(s,n)})},e.fn.timepicker.defaults={defaultTime:"current",disableFocus:!1,isOpen:!1,minuteStep:15,modalBackdrop:!1,secondStep:15,showSeconds:!1,showInputs:!0,showMeridian:!0,template:"dropdown",appendWidgetTo:".bootstrap-timepicker"},e.fn.timepicker.Constructor=i})(jQuery,window,document);
define("time_picker", function(){});

// Responsible for preparing form - for both Add and Edit, converting form to json, cleaning json, denormalising json and then triggering "save_clicked" event.
// Supports 2 buttons - first button does the above mentioned tasks from converting form to json to triggering "save_clicked" event.
// seond button - sends "button2_clicked" directly. 
// Used by Upload.js and form_controller.js. Both listen to the save_clicked and button2_clicked events to process the json generated by form
define('views/form',[
    'jquery',
    'underscore',
    'layoutmanager',
    'form_field_validator',
    'syphon',
    'views/notification',
    'indexeddb_backbone_config',
    'configs',
    'offline_utils',
    'denormalize',
    'models/user_model',
    'indexeddb-backbone',
    'chosen',
    'date_picker',
    'time_picker'
], function(jquery, underscore, layoutmanager, pass, pass, notifs_view, indexeddb, all_configs, Offline, Denormalizer, User) {


    var ShowAddEditFormView = Backbone.Layout.extend({

        events: {
            'click #button2': 'button2_clicked',
            // used in inline form
            'click #add_rows': 'append_new_inlines'
        },
        template: '#form_template',
        options_inner_template: _.template($('#options_template')
            .html()),

        //would be called when render is called       
        serialize: function() {
            // send the following info to template
            // already contains the names of the buttons
            var s_passed = this.options.serialize;
            var language = User.get('language');
            this.entity_config = all_configs[this.entity_name];
            // HTML for form 
            //s_passed["form_template"] = this.form_template;
            // whether its an inline form
            s_passed["inline"] = (this.inline) ? true : false;
            // name of the entity bieng added/edited
            s_passed["entity_name"] = this.entity_name;
            s_passed["language"] = language;
            s_passed["add_row"] = this.entity_config['labels_'+language]['add_row'];
            return s_passed;
        },

        
        // Identifies the action of this form - add/ edit_id/ edit_json  
//         Sets the result on the view object 
//         this.edit_case_id, this.edit_case_json, this.edit_case
        identify_form_action: function(params) {
            // There are two ways in which edit is true - when the ID is given, and the second is when a json is given(LIMIT: can be add too if json is missing id?).
            this.edit_case = false;
            this.edit_id = null;
            if (params.model_json) {
                // edit_case_upload
                this.edit_case_json = true; 
                this.model_json = params.model_json;
                this.edit_case = true;
                this.edit_id = this.model_json.id;
            } else if (params.model_id) {
                this.edit_case_id = true;
                this.edit_case = true;
                this.edit_id = params.model_id;
            }
        },

        
        // Refactor possible
//         Reads entity_config and sets basic properties on view object for easy access
        read_form_config: function(params) {
            var language = User.get("language");
            this.entity_name = params.entity_name;
            this.entity_config = all_configs[this.entity_name];
            //default locations - 
            this.foreign_entities = this.entity_config.foreign_entities;
            this.inline = this.entity_config.inline;
            this.bulk = this.entity_config.bulk;
            this.labels = this.entity_config['labels_'+language]
            if (this.edit_case) {
                this.form_template = _.template($('#' + this.entity_config.edit_template_name).html());
                if (this.entity_config.edit) {
                    this.foreign_entities = this.entity_config.edit.foreign_entities;
                    this.inline = this.entity_config.edit.inline;
                    this.bulk = this.entity_config.edit.bulk;
                }
            } else {
                this.form_template = _.template($('#' + this.entity_config.add_template_name).html());
                if (this.entity_config.add) {
                    this.foreign_entities = this.entity_config.add.foreign_entities;
                    this.inline = this.entity_config.add.inline;
                    this.bulk = this.entity_config.add.bulk;
                }
            }
        },

        // Relies on view object's context 
        // Gets foreign entities, create their offline collection to be fetched in afterRender
        // Sets up datastructures to setup in-form change events
        // Shamelessly polluting the view object
        setup_foreign_elements: function() {
            //stores the foreign entities' collections
            this.f_colls = []; 
            //stores the index of an entity to access its collection in f_colls            
            this.f_index = []; 
            //stores the dependency mapping between form elements
            this.source_dependents_map = {}; 
            //stores maping between filters and their dependent elements
            this.source_filter_dependent_map = {};
            //stores the mapping between foreign element and their entity
            this.element_entity_map = {}; 
            //stores whether a foreign element has been rendered
            this.foreign_elements_rendered = {}; 
            //stores the number of sources for a dependent element
            this.num_sources = {}; 
            //create a collection for each distinct entity, put them in this.f_colls, remem their index in f_colls using f_index
            for (f_entity in this.foreign_entities) {
                var f_collection = Offline.create_b_collection(f_entity, {
                    comparator: function(model) {
                        return model.get(all_configs[this.storeName].sort_field).toLowerCase();
                    }
                });
                this.f_index.push(f_entity);
                this.f_colls.push(f_collection);
                //create entity_map, dependency map, foreign_elements_rendered, for each foreign element
                for (var element in this.foreign_entities[f_entity]) {
                    //created mapping of element - entity
                    this.element_entity_map[element] = f_entity;
                    this.foreign_elements_rendered[element] = false;
                    // creating source - dependency mapping to be used for in-form events
                    var dependency = this.foreign_entities[f_entity][element]["dependency"];
                    var filter_dependency = this.foreign_entities[f_entity][element]["filter_dependency"];
                    if (dependency)
                        this.num_sources[element] = dependency.length;
                    else
                        this.num_sources[element] = 0;
                    if (dependency) {
                        var f_ens = this.foreign_entities;
                        var that = this;
                        $.each(dependency, function(index, dep) {
                            var source_elm = dep.source_form_element;
                            if (source_elm in that.source_dependents_map)
                                that.source_dependents_map[source_elm].push(element);
                            else {
                                that.source_dependents_map[source_elm] = [];
                                that.source_dependents_map[source_elm].push(element);
                            }
                        });
                        console.log("source_dependents_map = " + JSON.stringify(this.source_dependents_map));
                    }

                    if (filter_dependency) {
                        var f_ens = this.foreign_entities;
                        var that = this;
                        $.each(filter_dependency, function(index, dep) {
                            var source_elm = dep.source_form_element;
                            if (source_elm in that.source_filter_dependent_map)
                                that.source_filter_dependent_map[source_elm].push(element);
                            else {
                                that.source_filter_dependent_map[source_elm] = [];
                                that.source_filter_dependent_map[source_elm].push(element);
                            }
                        });
                        console.log("source_filter_dependent_map = " + JSON.stringify(this.source_filter_dependent_map)); 
                    }

                }
            }
        },

        /*
        params = {
            serialiaze:{
                //name of first button, not shown if ==""
                button1: "...",
                //name of sec button, not shown if ==""
                button2: "..."
            },
            //name of entity to be added/edited
            entity_name:,
            //id of model if edit case
            model_id:,
            //json of model to be shown in edit form - used when json!= json(model_id)
            model_json:,
        }
        */
        initialize: function(params) {
            console.log("ADD/EDIT: params to add/edit view: ");
            console.log(params);
            this.final_json = null;
            _.bindAll(this);

            //sets this.edit_case, and  this.edit_case_id, or this.edit_case_json
            this.identify_form_action(params);

            //read entity_config and sets main properties on view object for easy access
            this.read_form_config(params);

            //reads this.foreign_entities and setsup the collections, source_dependents_map
            this.setup_foreign_elements();
        },

        afterRender: function() {
            var that = this;
            
            //rendering labels
            this.render_labels();
            //no foreign element has been rendered yet so disabling all - they get enabled as and when they get rendered
            this.disable_foreign_elements();

            //start in-form change events
            this.start_change_events();

            //fetch all foreign collections and render them when all are fetched
            this.fetch_and_render_foreign_entities();

            //if edit case - fill form with the model
            if (this.edit_case)
                this.render_edit_model();

            //if inline case - render inlines
            if (this.inline)
                this.render_inlines();

            // call validator on the form
            this.initiate_form_field_validation();

            this.initiate_form_widgets();
        },

        render_labels: function(){
            $f_el = this.$("#form_template_render");
            $f_el.append(this.form_template(this.labels));
        },
        
        //fetches all foreign collections and renders them when all are fetched
        fetch_and_render_foreign_entities: function() {
            var for_entities_fetch_dfds = []
            for (var i = 0; i < this.f_colls.length; i++) {
                console.log("fetching f coll");
                var f_dfd = this.f_colls[i].fetch();
                for_entities_fetch_dfds.push(f_dfd);
            }
            // wait till all foreign collections are fetched and then render the non-dependent foreign elements - the dependent foreign elements gets rendered through in-form events
            $.when.apply($, for_entities_fetch_dfds)
                .done(this.render_non_dep_for_elements)
                .fail(function() {
                    //TODO: handle error callback
                    alert("Atleast one foreign entity could not be fetched!");
                })
        },

        //fill non-dependent foreign elements - dependent gets filled on change events
        render_non_dep_for_elements: function() {
            console.log("Rendering non dependent f elements");
            _.each(this.element_entity_map, function(entity, element) {
                if (!this.foreign_entities[entity][element]["dependency"])
                    this.render_foreign_element(element, this.get_collection_of_element(element).toArray());
            }, this);
        },

        // fetch edit object and render it into form
        render_edit_model: function() {
            var that = this;
            // if this is edit_Case_json case (used by UPLOAD ) - we have the json
            if (this.edit_case_json) {
                // normalise json to put into form
                this.normalize_json(this.model_json);
                // put into form
                this.fill_form();
            } else if (this.edit_case_id) {
                // fetch edit object
                Offline.fetch_object(this.entity_config.entity_name, "id", this.edit_id)
                    .done(function(model) {
                        console.log("EDIT: edit model fetched");
                        that.model_json = model.toJSON();
                        // normalise json to put into form
                        that.normalize_json(that.model_json);
                        // put into form
                        that.fill_form();
                    })
                    .fail(function() {
                        // edit object could not be fetched from offline db
                        //TODO: error handling
                        console.log("ERROR: EDIT: Edit model could not be fetched!");
                        alert("ERROR: EDIT: Edit model could not be fetched!");
                    });
            }
        },

        //disable dropdowns of all foreign elements - they would be enabled as and when they get populated
        disable_foreign_elements: function() {
            for (f_entity in this.foreign_entities) {
                for (element in this.foreign_entities[f_entity]) {
                    if (!this.foreign_entities[f_entity][element].expanded) {
                        this.$('[name=' + element + ']').prop("disabled", true);
                    }
                }
            }
        },

        //render header, empty inlines if add case, fetch and render related inlines if edit case
        render_inlines: function() {
            var that = this;
            var temp = _.template($('#' + this.inline.header).html());
            $f_el = this.$('#inline_header');
            $f_el.append(temp(this.labels));
            //if add case put in empty inlines
            if (!this.edit_case)
                this.append_new_inlines(this.inline.default_num_rows);
            else if (this.edit_case_id) {
                console.log("FORM:EDIT: Fteching inline collection");
                // fetch inline entity's whole collection! can be improved
                Offline.fetch_collection(this.inline.entity)
                    .done(function(collection) {
                        // id-json dictionary of inline models - later used to extend the modified inlines
                        that.inl_models_dict = {};
                        // filter inline collection to get only the ones related to the parent object
                        var inl_models = collection.filter(function(model) {
                            if (model.get(that.inline.joining_attribute.inline_attribute).id == that.edit_id) {
                                that.inl_models_dict[model.get("id")] = model.toJSON();
                                return true
                            }
                            return false;
                        });
                        console.log(inl_models);
                        // render the inlines into the form
                        that.fill_inlines(inl_models);
                    })
                    .fail(function() {
                        console.log("ERROR: EDIT: Inline collection could not be fetched!");
                    });
            }
            //not showing the inlines in case of edit_case_json
        },

        // fills the inline objects in their templates and puts them into form
        fill_inlines: function(model_array) {
            console.log("Filling inlines");
            var that = this;
            var inline_t = _.template($('#' + this.inline.template).html());

            $.each(model_array, function(index, model) {
                var tr = inline_t({
                    index: index
                });
                var filled_tr = that.fill_form_elements($(tr), model.toJSON());
                $(filled_tr).find(':input').removeClass("donotvalidate");
                that.$('#inline_body').append(filled_tr);
                $(filled_tr).on('change', that.switch_validation_for_inlines);
            });
        },

        // appends new empty inlines into form
        append_new_inlines: function(num_rows) {
            // compile the template of inline
            var inline_t = _.template($('#' + this.inline.template).html());
            if (typeof(num_rows) != "number")
                num_rows = this.inline.add_row;
            var start_index = get_index_to_start_from();
            // append the new inlines
            for (var i = start_index; i < start_index + num_rows; i++) {
                var tr = $(inline_t({
                    index: i
                }));
                this.$('#inline_body').append(tr);
                // switch validation on/off based on whether the inline is empty or not
                tr.on('change', this.switch_validation_for_inlines);
            }

            // get last index of already existing inlines
            function get_index_to_start_from() {
                var all_present_inlines = this.$('#inline_body tr').not(".form_error");
                if (!all_present_inlines.length)
                    return 0
                var max_index = $(_.last(all_present_inlines)).attr("index");
                return parseInt(max_index) + 1;
            }
        },

        // to prevent validation of empty inline rows
        switch_validation_for_inlines: function(ev) {
            //get the changed row
            var elem = ev.delegateTarget;
            var empty = true;
            $(elem).find(':input').each(function() {
                if ($(this).val())
                    empty = false;
            });
            if (!empty) {
                // if row is not emoty - turn on validation
                $(elem).find(':input').each(function() {
                    $(this).removeClass("donotvalidate");
                });
            } else {
                // if row is empty - turn off validation
                $(elem).find(':input').each(function() {
                    $(this).addClass("donotvalidate");
                });
            }
        },

        //takes a jquery object containgg form elements and a json. Fills all elements with the corrsponding value in json
        fill_form_elements: function(container, o_json) {
            container.attr("model_id", o_json.id);
            container.find(':input').each(function() {
                if (!$(this).attr('name'))
                    return;
                var attr_name = $(this).attr("name").replace(new RegExp("[0-9]", "g"), "");
                switch (this.type) {
                    case 'password':
                    case 'select-multiple':
                    case 'select-one':
                    case 'text':
                    case 'textarea':
                        $(this).val(o_json[attr_name]);
                        break;
                    case 'checkbox':
                    case 'radio':
                        this.checked = o_json[attr_name];
                }
            });
            return container;
        },

        // start listening to in-form events
        start_change_events: function() {
            for (element in this.source_dependents_map) {
                console.log("creating changeevent for - " + element);
                // put change-event listeners on source elements
                this.$('[name=' + element + ']').change(this.render_dep_for_elements);
            }
            for (element in this.source_filter_dependent_map) {
                console.log("creating changeevent for - " + element);
                // put change-event listeners on source elements
                this.$('[name=' + element + ']').change(this.render_dep_for_elements);
            }
        },

        // initiate the jquery validation plugin on the form
        initiate_form_field_validation: function() {
            var that = this;
            // pass the config defined in entity's config
            var validate_obj = $.extend(this.entity_config.form_field_validation, {
                "submitHandler": function() {
                    that.save();
                }
            });
            console.log()
            this.$('form')
                .validate(validate_obj);
        },

        // initiate the dropdown and date, time widgets
        initiate_form_widgets: function() {
            $(".chosen-select").chosen({
                'search_contains': true,
                'width': '100%'
            });


            var eDate = new Date();
            enddate = eDate.getFullYear() + "-" + (eDate.getMonth() + 1) + "-" + eDate.getDate();
            $(".date-picker")
                .datepicker({
                    format: 'yyyy-mm-dd',
                    startDate: '2009-01-01',
                    endDate: enddate,
                }).on('changeDate', function(ev) {
                    $(this).datepicker('hide');
                });

            $(".time-picker")
                .timepicker({
                    minuteStep: 1,
                    defaultTime: false,
                    showMeridian: false
                });
        },

        get_collection_of_element: function(element) {
            var entity = this.element_entity_map[element];
            var index = this.f_index.indexOf(entity);
            return this.f_colls[index];
        },

        get_sources_of_element: function(element) {
            var entity = this.element_entity_map[element];
            return this.foreign_entities[entity][element].dependency;
        },

        get_curr_value_of_element: function(element) {
            return $('[name=' + element + ']').val();
        },

        // render dependent foreign elements - executes when a source element changes
        render_dep_for_elements: function(ev) {
            var source = $(ev.target).attr("name"); //source changed
            console.log("FILLING DEP ENTITIES OF -" + source);
            // Iterate over its dependents
            _.each(this.source_dependents_map[source], function(dep_el) {
                var filtered_models = this.filter_dep_for_element(dep_el);
                this.render_foreign_element(dep_el, filtered_models);
            }, this);

            _.each(this.source_filter_dependent_map[source], function(dep_el) {
                var filtered_models = this.filter_dep_for_element(dep_el);
                this.render_foreign_element(dep_el, filtered_models);
            }, this);
        },

        // Fully Reset the dependent foreign element by looking at all its sources.
        filter_dep_for_element: function(element) {
            //get dependent element's entity's collection - to be filtered
            var dep_collection = this.get_collection_of_element(element);
            // get all sources of this element - to filter by
            var all_sources = this.get_sources_of_element(element);
            //model array to be finally inserted into dom
            var final_models = [];
            var that = this;

            if (!dep_collection.length)
                return [];

            $.each(all_sources, function(index, dep_desc) {
                var dep_attr = dep_desc.dep_attr;
                var source_form_element = dep_desc.source_form_element;
                var filtered_models = [];

                //LIMITS: source can't be an expanded right now, bcoz won't get its value
                var source_curr_value = that.get_curr_value_of_element(source_form_element);
                if (!source_curr_value)
                    return;
                else if (!(source_curr_value instanceof Array)) {
                    //if source is single select - convert its value to array -make it like a multiselect
                    var temp = source_curr_value;
                    source_curr_value = [];
                    source_curr_value.push((temp));
                }

                // many-to-many relation between source and dependent
                if (dep_collection.at(0).get(dep_desc.dep_attr) instanceof Array) {
                    filtered_models = dep_collection.filter(function(model) {
                        var exists = false;
                        //LIMITS: array assumed to contain objects - its an array so possibly other case not possible
                        $.each(model.get(dep_desc.dep_attr), function(index, object) {
                            if ($.inArray(String(object.id), source_curr_value) > -1)
                                exists = true;
                        });
                        return exists;
                    });
                } else {
                    filtered_models = dep_collection.filter(function(model) {
                        var exists = false;
                        var compare = null;
                        if (typeof model.get(dep_desc.dep_attr) == "object")
                            compare = model.get(dep_desc.dep_attr).id;
                        else
                            compare = model.get(dep_desc.dep_attr)

                        if (dep_desc.src_attr && dep_desc.src_attr != "id") {
                            var s_collection = that.get_collection_of_element(source_form_element);
                            var s_model = s_collection.get(parseInt(source_curr_value[0]));
                            if (s_model.get(dep_desc.src_attr) instanceof Array) {
                                //LIMITS: array assumed to contain objects - its an array so possibly other case not possible
                                $.each(s_model.get(dep_desc.src_attr), function(index, src_compare) {
                                    if (compare == src_compare.id)
                                        exists = true;
                                });
                            }
                            return exists;
                        } else {
                            if (!($.inArray(String(compare), source_curr_value) == -1))
                                exists = true;
                            return exists;
                        }
                    });
                }
                final_models = final_models.concat(filtered_models);
            });
            return final_models;
        },

        // filter an array of modal based on a filter defined in configs
        filter_model_array: function(model_array, filter) {
            var filter_attr = filter.attr;
            var filter_value = filter.value;
            filtered = [];
            $.each(model_array, function(index, obj) {
                //LIMIT: assumed to be an object
                if (obj.get(filter_attr).id == filter_value) {
                    filtered.push(obj);
                }
            });
            return filtered;
        },

        filter_dependent_model_array: function(model_array, filter) {
            if(model_array.length == 0) return model_array;
            var that = this;
            var source_form_element = filter['source_form_element'];
            var source_curr_value = that.get_curr_value_of_element(source_form_element);
            var dep_attr = filter['dep_attr'];
            filtered = [];
            if (!source_curr_value)
                return;
            else if (!(source_curr_value instanceof Array)) {
                //if source is single select - convert its value to array -make it like a multiselect
                var temp = source_curr_value;
                source_curr_value = [];
                source_curr_value.push(temp);
            }
            if(model_array[0].get(dep_attr) instanceof Array) {
                model_array = model_array.filter(function(model) {
                    var exists = false;
                    //LIMITS: array assumed to contain objects - its an array so possibly other case not possible
                    $.each(model.get(filter.dep_attr), function(index, object) {
                        if ($.inArray(String(object.id), source_curr_value) > -1)
                            exists = true;
                    });
                    return exists;
                });
            } else {
                model_array = model_array.filter(function(model) {
                    var exists = false;
                    var compare = null;
                    if (typeof model.get(filter.dep_attr) == "object")
                        compare = model.get(filter.dep_attr).id;
                    else
                        compare = model.get(filter.dep_attr);

                    if (filter.src_attr && filter.src_attr != "id") {
                        var s_collection = that.get_collection_of_element(source_form_element);
                        var s_model = s_collection.get(parseInt(source_curr_value[0]));
                        if (s_model.get(filter.src_attr) instanceof Array) {
                            //LIMITS: array assumed to contain objects - its an array so possibly other case not possible
                            $.each(s_model.get(dep_desc.src_attr), function(index, src_compare) {
                                if (compare == src_compare.id)
                                    exists = true;
                            });
                        }
                        return exists;
                    } else {
                        if ($.inArray(String(compare), source_curr_value) > -1)
                            exists = true;
                        return exists;
                    }
                });
            }
            return model_array;
        },

        // renders a foreign element - dropdown or expanded templates - into the form
        render_foreign_element: function(element, model_array) {
            console.log("FILLING FOREIGN ENTITY - " + element);
            var that = this;
            this.num_sources[element]--;
            var f_entity_desc = this.foreign_entities[this.element_entity_map[element]][element];

            //if any defined, filter the model array before putting into dom
            if (f_entity_desc.filter)
                model_array = this.filter_model_array(model_array, f_entity_desc.filter);
            //for filtering based on dependent fields
            if (f_entity_desc.filter_dependency)
                for(var i=0; i<f_entity_desc.filter_dependency.length; i ++){
                   model_array = this.filter_dependent_model_array(model_array, f_entity_desc.filter_dependency[i]);
                }
    
            if (f_entity_desc.expanded) {
                // get the expanded template
                var expanded_template = _.template($('#' + f_entity_desc.expanded.template).html());
                $f_el = this.$('#' + f_entity_desc.expanded.placeholder);
                $f_el.html('');
                //LIMIT: there can be only one expanded foreign element!
                this.expanded = element;

                //Its edit case and edit model is not yet rendered - so render it
                if (this.edit_case && !this.foreign_elements_rendered[element]) {
                    var id_field = "id"
                    if (f_entity_desc.id_field)
                        id_field = f_entity_desc.id_field;
                    var collection = this.get_collection_of_element(element);
                    $.each(this.model_json[element], function(index, f_json) {
                        model = collection.get(f_json[id_field]);
                        if (!model)
                            return;
                        var t_json = model.toJSON();
                        t_json["index"] = index;
                        $.each(f_entity_desc.expanded.extra_fields, function(index, field) {
                            t_json[field] = f_json[field];
                        });
                        console.log(t_json);
                        $f_el.append(expanded_template(t_json));
                    });
                    if (this.num_sources[element] <= 0)
                        this.foreign_elements_rendered[element] = true;
                } else {
                    $.each(model_array, function(index, f_model) {
                        var t_json = f_model.toJSON();
                        t_json["index"] = index;
                        $f_el.append(expanded_template(t_json));
                    });
                }
                this.initiate_form_widgets();
                $('.inline_table').show();
            } else {
                console.log("NOT EXPANDED");
                $f_el = this.$('#' + f_entity_desc.placeholder);
                if ($f_el.is('select[multiple]'))
                    $f_el.html('');
                else
                    $f_el.html(this.options_inner_template({
                        id: "",
                        name: "------------"
                    }));
                $.each(model_array, function (index, f_model) {
                    var f_json = f_model;
                    if (f_model instanceof Backbone.Model)
                        f_json = f_model.toJSON();
                    if (f_json[f_entity_desc.name_field_extra_info]) {
                        var extra_info_group_name = "";
                        var extra_info_person_id = "";
                        var extra_info_father_name = "";
                        if(f_json[f_entity_desc.name_field_father_name] != null){
                            extra_info_father_name = f_json[f_entity_desc.name_field_father_name]
                        }
                        if (f_json[f_entity_desc.name_field_extra_info][f_entity_desc.name_field_group_name] != null) {
                            extra_info_group_name = f_json[f_entity_desc.name_field_extra_info][f_entity_desc.name_field_group_name];
                        }
                        if (f_json[f_entity_desc.name_field_person_id] != null) {
                            extra_info_person_id = f_json[f_entity_desc.name_field_person_id]
                        }
                        $f_el.append(that.options_inner_template({
                            id: parseInt(f_json["id"]),
                            name: f_json[f_entity_desc.name_field] + (extra_info_father_name != "" ? ' (' + extra_info_father_name + ')' : "") + (extra_info_group_name != "" ? ' (' + extra_info_group_name + ')' : "") + (extra_info_person_id !="" ? ' (' + extra_info_person_id + ')' : "")
                        }));
                    }
                    else {
                        $f_el.append(that.options_inner_template({
                            id: parseInt(f_json["id"]),
                            name: f_json[f_entity_desc.name_field]
                        }));
                    }
                });
                $f_el.prop("disabled", false);
                $f_el.trigger("chosen:updated");

                //select the options selected in edit model
                if (this.edit_case && !this.foreign_elements_rendered[element]) {
                    this.$('form [name=' + element + ']').val(this.model_json[element]).change();
                    this.$('form [name=' + element + ']').trigger("chosen:updated");
                    if (this.num_sources[element] <= 0)
                        this.foreign_elements_rendered[element] = true;
                }
            }
        },

        // normalises the json before putting into form
        normalize_json: function(d_json) {
            console.log("FORM: Before Normalised json = " + JSON.stringify(d_json));
            var f_entities = this.foreign_entities;
            for (member in f_entities) {
                for (element in f_entities[member]) {
                    if ((element in d_json) && !(f_entities[member][element].expanded)) {
                        if (d_json[element] instanceof Array) {
                            var el_array = [];
                            $.each(d_json[element], function(index, object) {
                                el_array.push(parseInt(object["id"]));
                            });
                            d_json[element] = el_array;
                        } else {
                            d_json[element] = parseInt(d_json[element]["id"]);
                        }
                    }
                }
            }
            console.log("FORM: Normalised json = " + JSON.stringify(d_json));
            return d_json;
        },

        // Using Backbone.Syphon library to put normalised json into form
        fill_form: function() {
            console.log("FORM: filling form with the model - " + JSON.stringify(this.model_json));
            Backbone.Syphon.deserialize(this, this.model_json);
        },

        // used to disable the save button while save is in progress
        set_submit_button_state: function(state) {
            if (state == "disabled")
                this.$(".action_button").attr("disabled", true);
            else
                this.$(".action_button").button(state);
        },

        //err format - {"mediator": {"__all__": ["Animator with this Name, Gender and Partner already exists."]}}
        // {"form_name": {"element name": [list of errors]}}
        show_errors: function(errors, disable_submit) {
            // used to clear form errors
            if (errors == null) {
                $('.form_error').remove();
                $('.error').removeClass("error");
                return;
            }

            this.set_submit_button_state('reset');
            if (disable_submit)
                this.set_submit_button_state('disabled');

            if (typeof(errors) !== "object")
                errors = $.parseJSON(errors);
            console.log("Showing this error");
            console.log(errors);
            try {
                _.each(errors, function(errors_obj, parent) {
                    var parent_el = this.$('[name=' + parent + ']');
                    $.each(errors_obj, function(error_el_name, error_list) {
                        var error_ul = null;
                        all_li = "<li>" + error_list.join("</li><li>") + "</li>";
                        error_ul = "<tr class='form_error'><td colspan='100%'><ul>" + all_li + "</ul></td></tr>";
                        if (error_el_name == "__all__") {
                            parent_el.before(error_ul); //insert error message
                            parent_el.addClass("error"); //highlight
                        } else {
                            var error_el = parent_el.find('[name=' + error_el_name + ']');
                            error_el
                                .parent('div')
                                .parent('div')
                                .addClass("error"); //highlight
                            error_el.parent().append(error_ul); // insert error message after the element
                        }
                    });
                }, this);
            } catch (err) {
                //if the error object has an unknown format - show it as it is on top of form
                var parent_el = this.$('[name=' + this.entity_name + ']');
                parent_el.before("<div class='form_error'>" + JSON.stringify(errors) + "</div>"); //insert error message
            }

        },

        // TODO: the following 3 methods can be combined into single generic one
        // fetch inline from the form as a list of objects
        parse_inlines: function(raw_json) {
            console.log("FORM: fetching inlines");
            var all_inlines = $('#inline_body tr').not(".form_error");
            raw_json["inlines"] = [];
            var that = this;
            var inline_attrs = [];
            $.each(all_inlines, function(index, inl) {
                var inl_obj = {};
                var ignore = true;
                inl_obj.index = $(inl).attr("index");
                if ($(inl).attr("model_id"))
                    inl_obj.id = parseInt($(inl).attr("model_id"));
                $(inl).find(':input').each(function() {
                    if (!$(this).attr('name'))
                        return;
                    else
                        inline_attrs.push($(this).attr("name"));
                    var attr_name = $(this).attr("name").replace(new RegExp("[0-9]", "g"), "");
                    switch (this.type) {
                        case 'password':
                        case 'select-multiple':
                        case 'select-one':
                        case 'text':
                        case 'textarea':
                            inl_obj[attr_name] = $(this).val();
                            break;
                        case 'checkbox':
                        case 'radio':
                            inl_obj[attr_name] = this.checked;
                    }
                    if (inl_obj[attr_name] != "")
                        ignore = false;
                });
                if (!ignore)
                    raw_json["inlines"].push(inl_obj);
            });

            //remove inline attrs from raw_json...let them be inside raw_json.inlines only
            $.each(inline_attrs, function(index, attr) {
                delete raw_json[attr];
            });
            console.log(inline_attrs);


        },

        // fetch expandeds from the form as a list of objects
        parse_expanded: function(raw_json) {
            console.log("FORM: fetching expandeds");
            var element = this.expanded;
            var entity = this.element_entity_map[element];
            var desc = this.foreign_entities[entity][element]
            console.log("FORM:expande desc -" + JSON.stringify(desc));
            var placeholder = desc.expanded.placeholder;
            var all_inlines = $('#' + placeholder + ' tr');
            raw_json[element] = [];
            var that = this;
            var inline_attrs = [];
            $.each(all_inlines, function(index, inl) {
                var inl_obj = {};
                inl_obj["index"] = $(inl).attr("index");
                $(inl).find(':input').each(function(){
                    if(!$(this).attr('name'))
                        return;
                    inline_attrs.push($(this).attr("name"));
                    var attr_name = $(this).attr("name").replace(new RegExp("[0-9]", "g"), "");
    				switch(this.type) {
    					case 'password':
    					case 'select-multiple':
    					case 'select-one':
    					case 'text':
    					case 'textarea':
    						inl_obj[attr_name] = $(this).val();
    						break;
    					case 'checkbox':
    					case 'radio':
    						inl_obj[attr_name] = this.checked;
    				}
                });
                raw_json[element].push(inl_obj);
            });

            //remove inline attrs from raw_json...let them be inside raw_json.inlines only
            $.each(inline_attrs, function(index, attr) {
                delete raw_json[attr];
            });
            // console.log(inline_attrs);
        },

        // fetch bulks from the form as a list of objects
        parse_bulk: function(raw_json) {
            console.log("FORM: fetching bulks");
            var all_inlines = $('#bulk tr').not(".form_error");
            raw_json["bulk"] = [];
            var that = this;
            $.each(all_inlines, function(index, inl) {
                var inl_obj = {};
                inl_obj["index"] = $(inl).attr("index");
                $(inl).find(':input').each(function() {
                    if (!$(this).attr('name'))
                        return;
                    var attr_name = $(this).attr("name").replace(new RegExp("[0-9]", "g"), "");
                    switch (this.type) {
                        case 'password':
                        case 'select-multiple':
                        case 'select-one':
                        case 'text':
                        case 'textarea':
                            inl_obj[attr_name] = $(this).val();
                            break;
                        case 'checkbox':
                        case 'radio':
                            inl_obj[attr_name] = this.checked;
                    }
                    if (inl_obj[attr_name] != "")
                        ignore = false;
                });
                if (!ignore)
                    raw_json["bulk"].push(inl_obj);
            });
        },

        //preserve the background fields - not entered through form
        extend_edit_json: function(o_json) {
            o_json = $.extend(this.model_json, o_json);
            if (this.inline) {
                _.each(o_json.inlines, function(inl, index) {
                    var old_json = this.inl_models_dict[inl.id];
                    o_json.inlines[index] = $.extend(old_json, inl);
                }, this);
            }
            return o_json;
        },

        // clean the json before saving
        clean_json: function(form_json) {
            console.log("FORM: Before cleaning json - " + JSON.stringify(form_json))

            if (this.bulk) {
                $.each(form_json.bulk, function(index, obj) {
                    clean_object(obj);
                });
            } else {
                clean_object(form_json);
                if (this.inline) {
                    $.each(form_json.inlines, function(index, obj) {
                        clean_object(obj);
                    });
                }
            }

            function clean_object(obj) {
                for (member in obj) {
                    if (member == "")
                        delete obj[member];
                    else if (!obj[member]) {
                        obj[member] = null
                        if (this.$('[name=' + member + ']').is('select[multiple]')) {
                            obj[member] = [];
                        }
                    }
                    else if(typeof(obj[member])=="string"){
                        obj[member] = obj[member].trim();
                    }
                }
            }
            console.log("FORM: After cleaning json - " + JSON.stringify(form_json))

        },

        include_borrowed_attributes: function(o_json, fields) {
            _.each(o_json.bulk, function(bulk, index) {
                _.each(fields, function(field, index) {
                    bulk[field] = parseInt(this.$('[name=' + field + ']').val());
                }, this);
            }, this);
        },

        //initialize the Denormalize module to denormalize the form's objects
        denormalize_json: function(json) {
            var dfds = [];
            if (this.bulk) {
                _.each(json.bulk, function(bulk, index) {
                    var dfd = Denormalizer.denormalize(bulk, this.bulk.foreign_fields);
                    dfds.push(dfd);
                }, this);
            } else {
                var dfd = Denormalizer.denormalize(json, this.foreign_entities);
                dfds.push(dfd);
                if (this.inline) {
                    _.each(json.inlines, function(inline, index) {
                        var dfd = Denormalizer.denormalize(inline, this.inline.foreign_entities);
                        dfds.push(dfd);
                    }, this);
                }
            }
            return $.when.apply($, dfds);
        },

        //converts form into json object
        serialize_form: function() {
            var json = {};
            if (this.bulk) {
                this.parse_bulk(json);
                this.include_borrowed_attributes(json, this.bulk.borrow_fields);
            } else {
                json = Backbone.Syphon.serialize(this);
                if (this.expanded)
                    this.parse_expanded(json);
                if (this.inline)
                    this.parse_inlines(json);
            }
            return json;
        },


        save: function() {
            //clear old errors
            this.show_errors(null);
            //set state to loading
            this.set_submit_button_state('loading');
            //get a json object out of the form
            this.final_json = this.serialize_form();
            //clean json to be able to send to server
            this.clean_json(this.final_json);
            //denormalise the foreign elements in json
            var that = this;
            this.denormalize_json(this.final_json)
                .done(function() {
                    //preserve the background fields - not entered through form:
                    if (that.edit_case)
                        that.final_json = that.extend_edit_json(that.final_json);
                    /*form rendered, form filled by user, save clicked, savable json prepared,
                    this module's work is done for now, sending event*/
                    var ev_data = {
                        context: that,
                    };
                    that.trigger("save_clicked", ev_data);
                })
                .fail(function() {
                    console.log("Denormalising json failed!");
                });
        },

        button2_clicked: function() {
            var ev_data = {
                context: this,
            };
            this.trigger("button2_clicked", ev_data);
        }


    });

    // Our module now returns our view
    return ShowAddEditFormView;
});

// This module converts an object of an entity from one namespace to another.
// takes a denormalised object and the foreign entities description for the object. Using the descrip iterates over json,identifies the foreign values and substitute their online ids with offline ids or the opposite. 
// Used by incremental_download, upload, form_controller.
// To use - call the convert method
define('convert_namespace',['jquery', 'configs', 'backbone', 'indexeddb_backbone_config'

], function($, configs, pa, indexeddb) {
    var convert_namespace = {
        // converts from offline to online by default
        which_to_which: "offlinetoonline",
        // declared to make conversion code generic
        conv_dict: {
            "onlinetooffline": {
                replace_this: "online_id",
                replace_with: "id"
            },
            "offlinetoonline": {
                replace_this: "id",
                replace_with: "online_id"
            }
        },

        // returns the id_field declared in the foreign entity definition of this 'element' in configs of 'entity'
        get_id_field: function(entity, element, f_entities) {
            return f_entities[entity][element].id_field || "id";
        },

        // recieves the object to be converted, conversion-way and the foreign entity definition of the object
        convert: function(json, f_entities, which_to_which) {
            var dfd = new $.Deferred();
            if (which_to_which)
                this.which_to_which = which_to_which;
            var that = this;
            // making a deep copy of received object...this copy would be altered
            var conv_json = $.extend(true, null, json);
            console.log("FORMCONTROLLER:convert_namespace: json before converting" + JSON.stringify(json));
            // is filled with a dfd for each foreign element to be converted - when all dfds resolve - conversion is complete
            this.field_dfds = [];
            // iterate over the foreign elements of the object and converts them asynchronously - fills the field_dfds with a dfd for each conversion
            this.iterate_foreign_fields(conv_json, f_entities);

            var object_jsons = null;
            // set the return object based on conversion-way
            switch (this.which_to_which) {
                case "onlinetooffline":
                    object_jsons = {
                        off_json: conv_json,
                        on_json: json
                    }
                    break;
                default:
                    object_jsons = {
                        off_json: json,
                        on_json: conv_json
                    }
            }
            if (this.field_dfds.length) {
                // wait till all foreign elements resolve(all dfds in field_dfds resolve)
                $.when.apply($, this.field_dfds)
                    .done(function() {
                        // object successfully converted - return
                        return dfd.resolve(object_jsons);
                    })
                    .fail(function() {
                        // atleast one foreign element failed to be converted - abort and return
                        return dfd.reject();
                    });
            } else {
                // no conversion taking place - return immediately
                console.log("FORMCONTROLLER:convert_namespace: Nothing to convert.");
                return dfd.resolve(object_jsons);
            }

            return dfd.promise();
        },

        // iterates over the foreign elements of the object and converts them asynchronously - fills the field_dfds with a dfd for each conversion
        iterate_foreign_fields: function(json, f_entities) {
            // use the foreign entities definition of this object's entity to iterate over the foreign elements in the object
            for (var entity in f_entities) {
                for (var element in f_entities[entity]) {
                    // the foreign element doesn't exists in the object 
                    if (!(json[element]))
                        continue;

                    //  get the name of the id_field of the foreign element - for eg - id or person_id 
                    var id_field = this.get_id_field(entity, element, f_entities);
                    var field_desc = {
                        entity_name: entity,
                        id_attribute: id_field
                    };

                    //foreign elements is a multi-select (dropdown or expanded)
                    if (json[element] instanceof Array)
                        _.each(json[element], function(object, index) {
                            // convert each value of this multi-select 
                            this.field_dfds.push(this.convert_object(object, field_desc));
                        }, this);
                    else //foreign elements is a single-select (dropdown)
                        this.field_dfds.push(this.convert_object(json[element], field_desc));
                    //if foreign element is an expanded and contains its own foreign elements - recursively iterate the expanded objects to convert their foreign elements
                    if (f_entities[entity][element].expanded)
                        if (f_entities[entity][element].expanded.foreign_entities)
                            _.each(json[element], function(object, index) {

                                this.iterate_foreign_fields(object, f_entities[entity][element].expanded.foreign_entities);
                            }, this);
                }
            }
        },

        // converts a single foreign element asynchronously and returns a dfd to wait upon
        convert_object: function(obj, field_desc) {
            console.log("ConvertNamespace: converting object", JSON.stringify(obj), JSON.stringify(field_desc));
            var dfd = new $.Deferred();
            // the forein element is empty - return
            if (!obj[field_desc.id_attribute])
                return dfd.resolve();
            //  fetch the foreign element from offline db  
            // TODO:remove this and use the offline_utils module instead
            var generic_model_offline = Backbone.Model.extend({
                database: indexeddb,
                storeName: field_desc.entity_name,
            });
            var f_model = new generic_model_offline();
            // the object is to be fetched based on "id" or "online_id" depending upon the conversion-way(on-to-off or off-to-on)
            f_model.set(this.conv_dict[this.which_to_which].replace_this, parseInt(obj[field_desc.id_attribute]));
            var that = this;
            f_model.fetch({
                success: function(model) {
                    // replace id with online_id or the opposite depending upon the conversion-way
                    obj[field_desc.id_attribute] = model.get(that.conv_dict[that.which_to_which].replace_with);
                    return dfd.resolve();
                },
                error: function(model, error) {
                    //TODO: OOPS! What should be done now????
                    // alert("unexpected error. check console log "+error);
                    console.log("CONVERTNAMESPACE: unexpected error.",error);
                    // the foreign element object doesn't exists
                    return dfd.reject(error);
                }
            });
            return dfd.promise();
        }

    }


    return convert_namespace;

});

//A module of data layer to communicate with server. Since there are no fixed entities in COCO v2(as they are defined by user in config.js), there are no predefined models. This module creates backbone models/collection on the fly and enable communication with the server thru the models.
define('online_utils',['jquery', 'configs', 'backbone', 'indexeddb_backbone_config'], 

function($, all_configs, pa, indexeddb) {
    
    var online = {
        
        //Creates and return a new online backbone model object for the given entity
        create_b_model: function(entity_name)
        {
            var generic_model_online = Backbone.Model.extend({
                //configure the model to with the server
                sync: Backbone.ajaxSync,
                //read rest api endpoint for this entity from config.js and set it on model
                url: function() {
                    return this.id ? all_configs[entity_name].rest_api_url + this.id + "/" : all_configs[entity_name].rest_api_url;
                },
            });
            return new generic_model_online();
        },
    
        //Saves object on Server
        save: function(on_model, entity_name, json){
            var dfd = new $.Deferred();
            console.log("SAVING THIS IN ONLINE DB - "+JSON.stringify(json));
            if(!on_model)
            {
                //create a backbone model of entity type if one is not passed 
                on_model = this.create_b_model(entity_name);
            }
            //save model with the given json - backbone sends the request to save it on the server
            on_model.save(json,{
                success: function(model){
                    return dfd.resolve(model);
                },
                error: function(error, xhr, options){
                    return dfd.reject(xhr);
                }
            });
            return dfd;
        },
        
        //deletes an object referenced by off_model or by (entity_name, id) from server
        delete_object: function(on_model, entity_name, id){
            var dfd = new $.Deferred();
            if(!on_model)
            {
                //create a backbone model of entity type if one is not passed
                on_model = this.create_b_model(entity_name);
            }
            if(id)
            {
                //set the id on the model
                on_model.set("id",id);
            }
            //call model's destroy method - this sends delete request to server
            on_model.destroy({
                success: function(model){
                    return dfd.resolve(model);
                },
                error: function(error){
                    console.log(error);
                    return dfd.reject("Error destroying object in offline - "+xhr.responseText);
                }
            });
            return dfd;
        },
        
        
    }
    
    return online;

});

//this view displays upload status of collections in upload_q i.e. number of enteries uploaded and are pending to be uploaded, when connection with server is aborted
define('views/upload_status',[
    'jquery',
    'underscore',
    'layoutmanager',
    'collections/upload_collection',
    'models/user_model',
    'configs'
    ], function(jquery, underscore, layoutmanager, upload_collection, User, configs) {

        var UploadStatusView = Backbone.Layout.extend({

        initialize: function() {
            console.log("UPLOAD: initializing new upload status view");
             _(this).bindAll('tear_down');
        },

        template: "#upload_status_template",

        events: {
            "click #Ok": "tear_down"
        },
        
        serialize: function () {
            //send these to the list page template
            var language = User.get('language');
            return {
                language: language,
                configs: configs,
            };
        },

        //removes the view
        tear_down: function() {
            $('#upload_status_modal').modal('hide');
            $('.modal-backdrop').remove();
        },

        //update the status on the view 
        update_total: function(total) {
            $('#upl_total').html(total);
        },

        update_done: function(uploaded){
            $('#upl_done').html(uploaded);
        },

        update_pending: function(pending){
            $('#upl_pending').html(pending);
        },

        //feeds data to template
        get_status: function(total, uploaded, pending) {
            this.update_total(total);
            this.update_done(uploaded);
            this.update_pending(pending);
        }

    });

    // Our module now returns our view
    return UploadStatusView;
});

/*!
 * jQuery Cookie Plugin v1.4.1
 * https://github.com/carhartl/jquery-cookie
 *
 * Copyright 2013 Klaus Hartl
 * Released under the MIT license
 */
(function (factory) {
	if (typeof define === 'function' && define.amd) {
		// AMD
		define('jquery_cookie',['jquery'], factory);
	} else if (typeof exports === 'object') {
		// CommonJS
		factory(require('jquery'));
	} else {
		// Browser globals
		factory(jQuery);
	}
}(function ($) {

	var pluses = /\+/g;

	function encode(s) {
		return config.raw ? s : encodeURIComponent(s);
	}

	function decode(s) {
		return config.raw ? s : decodeURIComponent(s);
	}

	function stringifyCookieValue(value) {
		return encode(config.json ? JSON.stringify(value) : String(value));
	}

	function parseCookieValue(s) {
		if (s.indexOf('"') === 0) {
			// This is a quoted cookie as according to RFC2068, unescape...
			s = s.slice(1, -1).replace(/\\"/g, '"').replace(/\\\\/g, '\\');
		}

		try {
			// Replace server-side written pluses with spaces.
			// If we can't decode the cookie, ignore it, it's unusable.
			// If we can't parse the cookie, ignore it, it's unusable.
			s = decodeURIComponent(s.replace(pluses, ' '));
			return config.json ? JSON.parse(s) : s;
		} catch(e) {}
	}

	function read(s, converter) {
		var value = config.raw ? s : parseCookieValue(s);
		return $.isFunction(converter) ? converter(value) : value;
	}

	var config = $.cookie = function (key, value, options) {

		// Write

		if (value !== undefined && !$.isFunction(value)) {
			options = $.extend({}, config.defaults, options);

			if (typeof options.expires === 'number') {
				var days = options.expires, t = options.expires = new Date();
				t.setTime(+t + days * 864e+5);
			}

			return (document.cookie = [
				encode(key), '=', stringifyCookieValue(value),
				options.expires ? '; expires=' + options.expires.toUTCString() : '', // use expires attribute, max-age is not supported by IE
				options.path    ? '; path=' + options.path : '',
				options.domain  ? '; domain=' + options.domain : '',
				options.secure  ? '; secure' : ''
			].join(''));
		}

		// Read

		var result = key ? undefined : {};

		// To prevent the for loop in the first place assign an empty array
		// in case there are no cookies at all. Also prevents odd result when
		// calling $.cookie().
		var cookies = document.cookie ? document.cookie.split('; ') : [];

		for (var i = 0, l = cookies.length; i < l; i++) {
			var parts = cookies[i].split('=');
			var name = decode(parts.shift());
			var cookie = parts.join('=');

			if (key && key === name) {
				// If second argument (value) is a function it's a converter...
				result = read(cookie, value);
				break;
			}

			// Prevent storing a cookie that we couldn't decode.
			if (!key && (cookie = read(cookie)) !== undefined) {
				result[name] = cookie;
			}
		}

		return result;
	};

	config.defaults = {};

	$.removeCookie = function (key, options) {
		if ($.cookie(key) === undefined) {
			return false;
		}

		// Must not alter options, thus extending a fresh object...
		$.cookie(key, '', $.extend({}, options, { expires: -1 }));
		return !$.cookie(key);
	};

}));

// The client agent to communicate with backends to process authentication requests
// Exports an interface providng 3 methods - login, logout, check_login - for login view to use
// Based on internet-connectivity, it runs the authentication requests against the - server and the offline backend
define('auth',[
    'models/user_model',
    'auth_offline_backend',
    'configs',
    'offline_utils',
    'jquery_cookie'
], function(User, OfflineAuthBackend, all_configs, Offline) {

    var internet_connected = function() {
        return navigator.onLine;
    }

    // checks whether the user is logged in or not in both backends- based on internet connectivity 
    var check_login = function() {
        var dfd = new $.Deferred()
        console.log("checking login");
        if (check_online_login()) {
            OfflineAuthBackend.check_login()
                .done(function() {
                    dfd.resolve();
                })
                .fail(function(error) {
                    dfd.reject(error);
                });
        } else {
            dfd.reject("Not logged in on server");
        }
        return dfd.promise();
    }

    
    //ideally shd have been exacty same as the server uses. But approximating it to avoid network request.
    var check_online_login = function() {
        if (!internet_connected || $.cookie('sessionid'))
            return true;
        return false;
    }
    
    // logs out of the offline backend, if internet accessible- logs out of the server backend
    var logout = function() {
        var dfd = new $.Deferred();
        var that = this;
        online_logout()
            .always(function() {
                OfflineAuthBackend.logout()
                    .always(function() {
                        dfd.resolve();
                    })
            });
        return dfd;
    }
    
    // logs out of the online backend if internet accessible
    var online_logout = function() {
        var dfd = new $.Deferred();

        if (!internet_connected())
            dfd.resolve();
            
        // the logout endpoint should be made configurable
        $.post("/coco/logout/")
            .done(function(resp) {
                return dfd.resolve();
            })
            .fail(function(resp) {
                return dfd.reject(resp);
            });

        return dfd.promise();
    }
    
    // logs-in to the offline backend, if internet accessible - logs-in to the server backend
    var login = function(username, password, language) {
        var dfd = new $.Deferred();
        console.log("Attemting login");
        // internet accessible - login to server backend - when successfull - login to offline backend
        if (internet_connected()) {
            // try server backend login
            online_login(username, password)
                .fail(function(error) {
                    console.log("Online login failed - " + error);
                    dfd.reject(error);
                })
                .done(function() {
                    // online login successful, try offline backend login
                    OfflineAuthBackend.login(username, password, language)
                        .done(function() {
                            // login successful
                            console.log("Login Successful");
                            post_login_success();
                            dfd.resolve();
                        })
                        .fail(function (error){
                            console.log("Offline login failed - " + error);
                            dfd.reject(error);
                        });
                });
        } else {
            // internet not accessible - only try logging into offline backend
            OfflineAuthBackend.login(username, password, language)
                .done(function() {
                    console.log("Login Successful");
                    post_login_success();
                    dfd.resolve();
                })
                .fail(function (error) {
                    console.log("Offline login failed - " + error);
                    dfd.reject(error);
                });
        }
        return dfd;
    }
    
    // run any onLogin logic defined by user
    var post_login_success = function (){
        if (all_configs.misc.onLogin)
            all_configs.misc.onLogin(Offline, this);
            return;
    }

    // resolves if server returns 1 or internet is not connected otherwise rejects
    var online_login = function(username, password) {
        var dfd = new $.Deferred();
        if (!internet_connected())
            return dfd.resolve();
        //the endpoint should be made configurable     
        $.post("/coco/login/", {
            "username": username,
            "password": password
        })
            .done(function(resp) {
                if (resp == "1")
                    return dfd.resolve();
                else
                    return dfd.reject("Username or password is incorrect (Server)");
            })
            .fail(function(resp) {
                return dfd.reject("Could not contact server. Try again in a minute.");
            });
        return dfd.promise();
    }
    
    return {
        check_login: check_login,
        logout: logout,
        login: login
    };
});

/*!
 * Bootstrap v3.2.0 (http://getbootstrap.com)
 * Copyright 2011-2014 Twitter, Inc.
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 */

/*!
 * Generated using the Bootstrap Customizer (http://getbootstrap.com/customize/?id=ce6915ce5ec86b748fec)
 * Config saved to config.json and https://gist.github.com/ce6915ce5ec86b748fec
 */
if("undefined"==typeof jQuery)throw new Error("Bootstrap's JavaScript requires jQuery");+function(t){"use strict";function e(e){return this.each(function(){var i=t(this),s=i.data("bs.alert");s||i.data("bs.alert",s=new o(this)),"string"==typeof e&&s[e].call(i)})}var i='[data-dismiss="alert"]',o=function(e){t(e).on("click",i,this.close)};o.VERSION="3.2.0",o.prototype.close=function(e){function i(){n.detach().trigger("closed.bs.alert").remove()}var o=t(this),s=o.attr("data-target");s||(s=o.attr("href"),s=s&&s.replace(/.*(?=#[^\s]*$)/,""));var n=t(s);e&&e.preventDefault(),n.length||(n=o.hasClass("alert")?o:o.parent()),n.trigger(e=t.Event("close.bs.alert")),e.isDefaultPrevented()||(n.removeClass("in"),t.support.transition&&n.hasClass("fade")?n.one("bsTransitionEnd",i).emulateTransitionEnd(150):i())};var s=t.fn.alert;t.fn.alert=e,t.fn.alert.Constructor=o,t.fn.alert.noConflict=function(){return t.fn.alert=s,this},t(document).on("click.bs.alert.data-api",i,o.prototype.close)}(jQuery),+function(t){"use strict";function e(e){return this.each(function(){var o=t(this),s=o.data("bs.button"),n="object"==typeof e&&e;s||o.data("bs.button",s=new i(this,n)),"toggle"==e?s.toggle():e&&s.setState(e)})}var i=function(e,o){this.$element=t(e),this.options=t.extend({},i.DEFAULTS,o),this.isLoading=!1};i.VERSION="3.2.0",i.DEFAULTS={loadingText:"loading..."},i.prototype.setState=function(e){var i="disabled",o=this.$element,s=o.is("input")?"val":"html",n=o.data();e+="Text",null==n.resetText&&o.data("resetText",o[s]()),o[s](null==n[e]?this.options[e]:n[e]),setTimeout(t.proxy(function(){"loadingText"==e?(this.isLoading=!0,o.addClass(i).attr(i,i)):this.isLoading&&(this.isLoading=!1,o.removeClass(i).removeAttr(i))},this),0)},i.prototype.toggle=function(){var t=!0,e=this.$element.closest('[data-toggle="buttons"]');if(e.length){var i=this.$element.find("input");"radio"==i.prop("type")&&(i.prop("checked")&&this.$element.hasClass("active")?t=!1:e.find(".active").removeClass("active")),t&&i.prop("checked",!this.$element.hasClass("active")).trigger("change")}t&&this.$element.toggleClass("active")};var o=t.fn.button;t.fn.button=e,t.fn.button.Constructor=i,t.fn.button.noConflict=function(){return t.fn.button=o,this},t(document).on("click.bs.button.data-api",'[data-toggle^="button"]',function(i){var o=t(i.target);o.hasClass("btn")||(o=o.closest(".btn")),e.call(o,"toggle"),i.preventDefault()})}(jQuery),+function(t){"use strict";function e(e){return this.each(function(){var o=t(this),s=o.data("bs.carousel"),n=t.extend({},i.DEFAULTS,o.data(),"object"==typeof e&&e),r="string"==typeof e?e:n.slide;s||o.data("bs.carousel",s=new i(this,n)),"number"==typeof e?s.to(e):r?s[r]():n.interval&&s.pause().cycle()})}var i=function(e,i){this.$element=t(e).on("keydown.bs.carousel",t.proxy(this.keydown,this)),this.$indicators=this.$element.find(".carousel-indicators"),this.options=i,this.paused=this.sliding=this.interval=this.$active=this.$items=null,"hover"==this.options.pause&&this.$element.on("mouseenter.bs.carousel",t.proxy(this.pause,this)).on("mouseleave.bs.carousel",t.proxy(this.cycle,this))};i.VERSION="3.2.0",i.DEFAULTS={interval:5e3,pause:"hover",wrap:!0},i.prototype.keydown=function(t){switch(t.which){case 37:this.prev();break;case 39:this.next();break;default:return}t.preventDefault()},i.prototype.cycle=function(e){return e||(this.paused=!1),this.interval&&clearInterval(this.interval),this.options.interval&&!this.paused&&(this.interval=setInterval(t.proxy(this.next,this),this.options.interval)),this},i.prototype.getItemIndex=function(t){return this.$items=t.parent().children(".item"),this.$items.index(t||this.$active)},i.prototype.to=function(e){var i=this,o=this.getItemIndex(this.$active=this.$element.find(".item.active"));return e>this.$items.length-1||0>e?void 0:this.sliding?this.$element.one("slid.bs.carousel",function(){i.to(e)}):o==e?this.pause().cycle():this.slide(e>o?"next":"prev",t(this.$items[e]))},i.prototype.pause=function(e){return e||(this.paused=!0),this.$element.find(".next, .prev").length&&t.support.transition&&(this.$element.trigger(t.support.transition.end),this.cycle(!0)),this.interval=clearInterval(this.interval),this},i.prototype.next=function(){return this.sliding?void 0:this.slide("next")},i.prototype.prev=function(){return this.sliding?void 0:this.slide("prev")},i.prototype.slide=function(e,i){var o=this.$element.find(".item.active"),s=i||o[e](),n=this.interval,r="next"==e?"left":"right",a="next"==e?"first":"last",l=this;if(!s.length){if(!this.options.wrap)return;s=this.$element.find(".item")[a]()}if(s.hasClass("active"))return this.sliding=!1;var h=s[0],p=t.Event("slide.bs.carousel",{relatedTarget:h,direction:r});if(this.$element.trigger(p),!p.isDefaultPrevented()){if(this.sliding=!0,n&&this.pause(),this.$indicators.length){this.$indicators.find(".active").removeClass("active");var c=t(this.$indicators.children()[this.getItemIndex(s)]);c&&c.addClass("active")}var d=t.Event("slid.bs.carousel",{relatedTarget:h,direction:r});return t.support.transition&&this.$element.hasClass("slide")?(s.addClass(e),s[0].offsetWidth,o.addClass(r),s.addClass(r),o.one("bsTransitionEnd",function(){s.removeClass([e,r].join(" ")).addClass("active"),o.removeClass(["active",r].join(" ")),l.sliding=!1,setTimeout(function(){l.$element.trigger(d)},0)}).emulateTransitionEnd(1e3*o.css("transition-duration").slice(0,-1))):(o.removeClass("active"),s.addClass("active"),this.sliding=!1,this.$element.trigger(d)),n&&this.cycle(),this}};var o=t.fn.carousel;t.fn.carousel=e,t.fn.carousel.Constructor=i,t.fn.carousel.noConflict=function(){return t.fn.carousel=o,this},t(document).on("click.bs.carousel.data-api","[data-slide], [data-slide-to]",function(i){var o,s=t(this),n=t(s.attr("data-target")||(o=s.attr("href"))&&o.replace(/.*(?=#[^\s]+$)/,""));if(n.hasClass("carousel")){var r=t.extend({},n.data(),s.data()),a=s.attr("data-slide-to");a&&(r.interval=!1),e.call(n,r),a&&n.data("bs.carousel").to(a),i.preventDefault()}}),t(window).on("load",function(){t('[data-ride="carousel"]').each(function(){var i=t(this);e.call(i,i.data())})})}(jQuery),+function(t){"use strict";function e(e){e&&3===e.which||(t(s).remove(),t(n).each(function(){var o=i(t(this)),s={relatedTarget:this};o.hasClass("open")&&(o.trigger(e=t.Event("hide.bs.dropdown",s)),e.isDefaultPrevented()||o.removeClass("open").trigger("hidden.bs.dropdown",s))}))}function i(e){var i=e.attr("data-target");i||(i=e.attr("href"),i=i&&/#[A-Za-z]/.test(i)&&i.replace(/.*(?=#[^\s]*$)/,""));var o=i&&t(i);return o&&o.length?o:e.parent()}function o(e){return this.each(function(){var i=t(this),o=i.data("bs.dropdown");o||i.data("bs.dropdown",o=new r(this)),"string"==typeof e&&o[e].call(i)})}var s=".dropdown-backdrop",n='[data-toggle="dropdown"]',r=function(e){t(e).on("click.bs.dropdown",this.toggle)};r.VERSION="3.2.0",r.prototype.toggle=function(o){var s=t(this);if(!s.is(".disabled, :disabled")){var n=i(s),r=n.hasClass("open");if(e(),!r){"ontouchstart"in document.documentElement&&!n.closest(".navbar-nav").length&&t('<div class="dropdown-backdrop"/>').insertAfter(t(this)).on("click",e);var a={relatedTarget:this};if(n.trigger(o=t.Event("show.bs.dropdown",a)),o.isDefaultPrevented())return;s.trigger("focus"),n.toggleClass("open").trigger("shown.bs.dropdown",a)}return!1}},r.prototype.keydown=function(e){if(/(38|40|27)/.test(e.keyCode)){var o=t(this);if(e.preventDefault(),e.stopPropagation(),!o.is(".disabled, :disabled")){var s=i(o),r=s.hasClass("open");if(!r||r&&27==e.keyCode)return 27==e.which&&s.find(n).trigger("focus"),o.trigger("click");var a=" li:not(.divider):visible a",l=s.find('[role="menu"]'+a+', [role="listbox"]'+a);if(l.length){var h=l.index(l.filter(":focus"));38==e.keyCode&&h>0&&h--,40==e.keyCode&&h<l.length-1&&h++,~h||(h=0),l.eq(h).trigger("focus")}}}};var a=t.fn.dropdown;t.fn.dropdown=o,t.fn.dropdown.Constructor=r,t.fn.dropdown.noConflict=function(){return t.fn.dropdown=a,this},t(document).on("click.bs.dropdown.data-api",e).on("click.bs.dropdown.data-api",".dropdown form",function(t){t.stopPropagation()}).on("click.bs.dropdown.data-api",n,r.prototype.toggle).on("keydown.bs.dropdown.data-api",n+', [role="menu"], [role="listbox"]',r.prototype.keydown)}(jQuery),+function(t){"use strict";function e(e,o){return this.each(function(){var s=t(this),n=s.data("bs.modal"),r=t.extend({},i.DEFAULTS,s.data(),"object"==typeof e&&e);n||s.data("bs.modal",n=new i(this,r)),"string"==typeof e?n[e](o):r.show&&n.show(o)})}var i=function(e,i){this.options=i,this.$body=t(document.body),this.$element=t(e),this.$backdrop=this.isShown=null,this.scrollbarWidth=0,this.options.remote&&this.$element.find(".modal-content").load(this.options.remote,t.proxy(function(){this.$element.trigger("loaded.bs.modal")},this))};i.VERSION="3.2.0",i.DEFAULTS={backdrop:!0,keyboard:!0,show:!0},i.prototype.toggle=function(t){return this.isShown?this.hide():this.show(t)},i.prototype.show=function(e){var i=this,o=t.Event("show.bs.modal",{relatedTarget:e});this.$element.trigger(o),this.isShown||o.isDefaultPrevented()||(this.isShown=!0,this.checkScrollbar(),this.$body.addClass("modal-open"),this.setScrollbar(),this.escape(),this.$element.on("click.dismiss.bs.modal",'[data-dismiss="modal"]',t.proxy(this.hide,this)),this.backdrop(function(){var o=t.support.transition&&i.$element.hasClass("fade");i.$element.parent().length||i.$element.appendTo(i.$body),i.$element.show().scrollTop(0),o&&i.$element[0].offsetWidth,i.$element.addClass("in").attr("aria-hidden",!1),i.enforceFocus();var s=t.Event("shown.bs.modal",{relatedTarget:e});o?i.$element.find(".modal-dialog").one("bsTransitionEnd",function(){i.$element.trigger("focus").trigger(s)}).emulateTransitionEnd(300):i.$element.trigger("focus").trigger(s)}))},i.prototype.hide=function(e){e&&e.preventDefault(),e=t.Event("hide.bs.modal"),this.$element.trigger(e),this.isShown&&!e.isDefaultPrevented()&&(this.isShown=!1,this.$body.removeClass("modal-open"),this.resetScrollbar(),this.escape(),t(document).off("focusin.bs.modal"),this.$element.removeClass("in").attr("aria-hidden",!0).off("click.dismiss.bs.modal"),t.support.transition&&this.$element.hasClass("fade")?this.$element.one("bsTransitionEnd",t.proxy(this.hideModal,this)).emulateTransitionEnd(300):this.hideModal())},i.prototype.enforceFocus=function(){t(document).off("focusin.bs.modal").on("focusin.bs.modal",t.proxy(function(t){this.$element[0]===t.target||this.$element.has(t.target).length||this.$element.trigger("focus")},this))},i.prototype.escape=function(){this.isShown&&this.options.keyboard?this.$element.on("keyup.dismiss.bs.modal",t.proxy(function(t){27==t.which&&this.hide()},this)):this.isShown||this.$element.off("keyup.dismiss.bs.modal")},i.prototype.hideModal=function(){var t=this;this.$element.hide(),this.backdrop(function(){t.$element.trigger("hidden.bs.modal")})},i.prototype.removeBackdrop=function(){this.$backdrop&&this.$backdrop.remove(),this.$backdrop=null},i.prototype.backdrop=function(e){var i=this,o=this.$element.hasClass("fade")?"fade":"";if(this.isShown&&this.options.backdrop){var s=t.support.transition&&o;if(this.$backdrop=t('<div class="modal-backdrop '+o+'" />').appendTo(this.$body),this.$element.on("click.dismiss.bs.modal",t.proxy(function(t){t.target===t.currentTarget&&("static"==this.options.backdrop?this.$element[0].focus.call(this.$element[0]):this.hide.call(this))},this)),s&&this.$backdrop[0].offsetWidth,this.$backdrop.addClass("in"),!e)return;s?this.$backdrop.one("bsTransitionEnd",e).emulateTransitionEnd(150):e()}else if(!this.isShown&&this.$backdrop){this.$backdrop.removeClass("in");var n=function(){i.removeBackdrop(),e&&e()};t.support.transition&&this.$element.hasClass("fade")?this.$backdrop.one("bsTransitionEnd",n).emulateTransitionEnd(150):n()}else e&&e()},i.prototype.checkScrollbar=function(){document.body.clientWidth>=window.innerWidth||(this.scrollbarWidth=this.scrollbarWidth||this.measureScrollbar())},i.prototype.setScrollbar=function(){var t=parseInt(this.$body.css("padding-right")||0,10);this.scrollbarWidth&&this.$body.css("padding-right",t+this.scrollbarWidth)},i.prototype.resetScrollbar=function(){this.$body.css("padding-right","")},i.prototype.measureScrollbar=function(){var t=document.createElement("div");t.className="modal-scrollbar-measure",this.$body.append(t);var e=t.offsetWidth-t.clientWidth;return this.$body[0].removeChild(t),e};var o=t.fn.modal;t.fn.modal=e,t.fn.modal.Constructor=i,t.fn.modal.noConflict=function(){return t.fn.modal=o,this},t(document).on("click.bs.modal.data-api",'[data-toggle="modal"]',function(i){var o=t(this),s=o.attr("href"),n=t(o.attr("data-target")||s&&s.replace(/.*(?=#[^\s]+$)/,"")),r=n.data("bs.modal")?"toggle":t.extend({remote:!/#/.test(s)&&s},n.data(),o.data());o.is("a")&&i.preventDefault(),n.one("show.bs.modal",function(t){t.isDefaultPrevented()||n.one("hidden.bs.modal",function(){o.is(":visible")&&o.trigger("focus")})}),e.call(n,r,this)})}(jQuery),+function(t){"use strict";function e(e){return this.each(function(){var o=t(this),s=o.data("bs.tooltip"),n="object"==typeof e&&e;(s||"destroy"!=e)&&(s||o.data("bs.tooltip",s=new i(this,n)),"string"==typeof e&&s[e]())})}var i=function(t,e){this.type=this.options=this.enabled=this.timeout=this.hoverState=this.$element=null,this.init("tooltip",t,e)};i.VERSION="3.2.0",i.DEFAULTS={animation:!0,placement:"top",selector:!1,template:'<div class="tooltip" role="tooltip"><div class="tooltip-arrow"></div><div class="tooltip-inner"></div></div>',trigger:"hover focus",title:"",delay:0,html:!1,container:!1,viewport:{selector:"body",padding:0}},i.prototype.init=function(e,i,o){this.enabled=!0,this.type=e,this.$element=t(i),this.options=this.getOptions(o),this.$viewport=this.options.viewport&&t(this.options.viewport.selector||this.options.viewport);for(var s=this.options.trigger.split(" "),n=s.length;n--;){var r=s[n];if("click"==r)this.$element.on("click."+this.type,this.options.selector,t.proxy(this.toggle,this));else if("manual"!=r){var a="hover"==r?"mouseenter":"focusin",l="hover"==r?"mouseleave":"focusout";this.$element.on(a+"."+this.type,this.options.selector,t.proxy(this.enter,this)),this.$element.on(l+"."+this.type,this.options.selector,t.proxy(this.leave,this))}}this.options.selector?this._options=t.extend({},this.options,{trigger:"manual",selector:""}):this.fixTitle()},i.prototype.getDefaults=function(){return i.DEFAULTS},i.prototype.getOptions=function(e){return e=t.extend({},this.getDefaults(),this.$element.data(),e),e.delay&&"number"==typeof e.delay&&(e.delay={show:e.delay,hide:e.delay}),e},i.prototype.getDelegateOptions=function(){var e={},i=this.getDefaults();return this._options&&t.each(this._options,function(t,o){i[t]!=o&&(e[t]=o)}),e},i.prototype.enter=function(e){var i=e instanceof this.constructor?e:t(e.currentTarget).data("bs."+this.type);return i||(i=new this.constructor(e.currentTarget,this.getDelegateOptions()),t(e.currentTarget).data("bs."+this.type,i)),clearTimeout(i.timeout),i.hoverState="in",i.options.delay&&i.options.delay.show?void(i.timeout=setTimeout(function(){"in"==i.hoverState&&i.show()},i.options.delay.show)):i.show()},i.prototype.leave=function(e){var i=e instanceof this.constructor?e:t(e.currentTarget).data("bs."+this.type);return i||(i=new this.constructor(e.currentTarget,this.getDelegateOptions()),t(e.currentTarget).data("bs."+this.type,i)),clearTimeout(i.timeout),i.hoverState="out",i.options.delay&&i.options.delay.hide?void(i.timeout=setTimeout(function(){"out"==i.hoverState&&i.hide()},i.options.delay.hide)):i.hide()},i.prototype.show=function(){var e=t.Event("show.bs."+this.type);if(this.hasContent()&&this.enabled){this.$element.trigger(e);var i=t.contains(document.documentElement,this.$element[0]);if(e.isDefaultPrevented()||!i)return;var o=this,s=this.tip(),n=this.getUID(this.type);this.setContent(),s.attr("id",n),this.$element.attr("aria-describedby",n),this.options.animation&&s.addClass("fade");var r="function"==typeof this.options.placement?this.options.placement.call(this,s[0],this.$element[0]):this.options.placement,a=/\s?auto?\s?/i,l=a.test(r);l&&(r=r.replace(a,"")||"top"),s.detach().css({top:0,left:0,display:"block"}).addClass(r).data("bs."+this.type,this),this.options.container?s.appendTo(this.options.container):s.insertAfter(this.$element);var h=this.getPosition(),p=s[0].offsetWidth,c=s[0].offsetHeight;if(l){var d=r,f=this.$element.parent(),u=this.getPosition(f);r="bottom"==r&&h.top+h.height+c-u.scroll>u.height?"top":"top"==r&&h.top-u.scroll-c<0?"bottom":"right"==r&&h.right+p>u.width?"left":"left"==r&&h.left-p<u.left?"right":r,s.removeClass(d).addClass(r)}var g=this.getCalculatedOffset(r,h,p,c);this.applyPlacement(g,r);var v=function(){o.$element.trigger("shown.bs."+o.type),o.hoverState=null};t.support.transition&&this.$tip.hasClass("fade")?s.one("bsTransitionEnd",v).emulateTransitionEnd(150):v()}},i.prototype.applyPlacement=function(e,i){var o=this.tip(),s=o[0].offsetWidth,n=o[0].offsetHeight,r=parseInt(o.css("margin-top"),10),a=parseInt(o.css("margin-left"),10);isNaN(r)&&(r=0),isNaN(a)&&(a=0),e.top=e.top+r,e.left=e.left+a,t.offset.setOffset(o[0],t.extend({using:function(t){o.css({top:Math.round(t.top),left:Math.round(t.left)})}},e),0),o.addClass("in");var l=o[0].offsetWidth,h=o[0].offsetHeight;"top"==i&&h!=n&&(e.top=e.top+n-h);var p=this.getViewportAdjustedDelta(i,e,l,h);p.left?e.left+=p.left:e.top+=p.top;var c=p.left?2*p.left-s+l:2*p.top-n+h,d=p.left?"left":"top",f=p.left?"offsetWidth":"offsetHeight";o.offset(e),this.replaceArrow(c,o[0][f],d)},i.prototype.replaceArrow=function(t,e,i){this.arrow().css(i,t?50*(1-t/e)+"%":"")},i.prototype.setContent=function(){var t=this.tip(),e=this.getTitle();t.find(".tooltip-inner")[this.options.html?"html":"text"](e),t.removeClass("fade in top bottom left right")},i.prototype.hide=function(){function e(){"in"!=i.hoverState&&o.detach(),i.$element.trigger("hidden.bs."+i.type)}var i=this,o=this.tip(),s=t.Event("hide.bs."+this.type);return this.$element.removeAttr("aria-describedby"),this.$element.trigger(s),s.isDefaultPrevented()?void 0:(o.removeClass("in"),t.support.transition&&this.$tip.hasClass("fade")?o.one("bsTransitionEnd",e).emulateTransitionEnd(150):e(),this.hoverState=null,this)},i.prototype.fixTitle=function(){var t=this.$element;(t.attr("title")||"string"!=typeof t.attr("data-original-title"))&&t.attr("data-original-title",t.attr("title")||"").attr("title","")},i.prototype.hasContent=function(){return this.getTitle()},i.prototype.getPosition=function(e){e=e||this.$element;var i=e[0],o="BODY"==i.tagName;return t.extend({},"function"==typeof i.getBoundingClientRect?i.getBoundingClientRect():null,{scroll:o?document.documentElement.scrollTop||document.body.scrollTop:e.scrollTop(),width:o?t(window).width():e.outerWidth(),height:o?t(window).height():e.outerHeight()},o?{top:0,left:0}:e.offset())},i.prototype.getCalculatedOffset=function(t,e,i,o){return"bottom"==t?{top:e.top+e.height,left:e.left+e.width/2-i/2}:"top"==t?{top:e.top-o,left:e.left+e.width/2-i/2}:"left"==t?{top:e.top+e.height/2-o/2,left:e.left-i}:{top:e.top+e.height/2-o/2,left:e.left+e.width}},i.prototype.getViewportAdjustedDelta=function(t,e,i,o){var s={top:0,left:0};if(!this.$viewport)return s;var n=this.options.viewport&&this.options.viewport.padding||0,r=this.getPosition(this.$viewport);if(/right|left/.test(t)){var a=e.top-n-r.scroll,l=e.top+n-r.scroll+o;a<r.top?s.top=r.top-a:l>r.top+r.height&&(s.top=r.top+r.height-l)}else{var h=e.left-n,p=e.left+n+i;h<r.left?s.left=r.left-h:p>r.width&&(s.left=r.left+r.width-p)}return s},i.prototype.getTitle=function(){var t,e=this.$element,i=this.options;return t=e.attr("data-original-title")||("function"==typeof i.title?i.title.call(e[0]):i.title)},i.prototype.getUID=function(t){do t+=~~(1e6*Math.random());while(document.getElementById(t));return t},i.prototype.tip=function(){return this.$tip=this.$tip||t(this.options.template)},i.prototype.arrow=function(){return this.$arrow=this.$arrow||this.tip().find(".tooltip-arrow")},i.prototype.validate=function(){this.$element[0].parentNode||(this.hide(),this.$element=null,this.options=null)},i.prototype.enable=function(){this.enabled=!0},i.prototype.disable=function(){this.enabled=!1},i.prototype.toggleEnabled=function(){this.enabled=!this.enabled},i.prototype.toggle=function(e){var i=this;e&&(i=t(e.currentTarget).data("bs."+this.type),i||(i=new this.constructor(e.currentTarget,this.getDelegateOptions()),t(e.currentTarget).data("bs."+this.type,i))),i.tip().hasClass("in")?i.leave(i):i.enter(i)},i.prototype.destroy=function(){clearTimeout(this.timeout),this.hide().$element.off("."+this.type).removeData("bs."+this.type)};var o=t.fn.tooltip;t.fn.tooltip=e,t.fn.tooltip.Constructor=i,t.fn.tooltip.noConflict=function(){return t.fn.tooltip=o,this}}(jQuery),+function(t){"use strict";function e(e){return this.each(function(){var o=t(this),s=o.data("bs.popover"),n="object"==typeof e&&e;(s||"destroy"!=e)&&(s||o.data("bs.popover",s=new i(this,n)),"string"==typeof e&&s[e]())})}var i=function(t,e){this.init("popover",t,e)};if(!t.fn.tooltip)throw new Error("Popover requires tooltip.js");i.VERSION="3.2.0",i.DEFAULTS=t.extend({},t.fn.tooltip.Constructor.DEFAULTS,{placement:"right",trigger:"click",content:"",template:'<div class="popover" role="tooltip"><div class="arrow"></div><h3 class="popover-title"></h3><div class="popover-content"></div></div>'}),i.prototype=t.extend({},t.fn.tooltip.Constructor.prototype),i.prototype.constructor=i,i.prototype.getDefaults=function(){return i.DEFAULTS},i.prototype.setContent=function(){var t=this.tip(),e=this.getTitle(),i=this.getContent();t.find(".popover-title")[this.options.html?"html":"text"](e),t.find(".popover-content").empty()[this.options.html?"string"==typeof i?"html":"append":"text"](i),t.removeClass("fade top bottom left right in"),t.find(".popover-title").html()||t.find(".popover-title").hide()},i.prototype.hasContent=function(){return this.getTitle()||this.getContent()},i.prototype.getContent=function(){var t=this.$element,e=this.options;return t.attr("data-content")||("function"==typeof e.content?e.content.call(t[0]):e.content)},i.prototype.arrow=function(){return this.$arrow=this.$arrow||this.tip().find(".arrow")},i.prototype.tip=function(){return this.$tip||(this.$tip=t(this.options.template)),this.$tip};var o=t.fn.popover;t.fn.popover=e,t.fn.popover.Constructor=i,t.fn.popover.noConflict=function(){return t.fn.popover=o,this}}(jQuery),+function(t){"use strict";function e(e){return this.each(function(){var o=t(this),s=o.data("bs.tab");s||o.data("bs.tab",s=new i(this)),"string"==typeof e&&s[e]()})}var i=function(e){this.element=t(e)};i.VERSION="3.2.0",i.prototype.show=function(){var e=this.element,i=e.closest("ul:not(.dropdown-menu)"),o=e.data("target");if(o||(o=e.attr("href"),o=o&&o.replace(/.*(?=#[^\s]*$)/,"")),!e.parent("li").hasClass("active")){var s=i.find(".active:last a")[0],n=t.Event("show.bs.tab",{relatedTarget:s});if(e.trigger(n),!n.isDefaultPrevented()){var r=t(o);this.activate(e.closest("li"),i),this.activate(r,r.parent(),function(){e.trigger({type:"shown.bs.tab",relatedTarget:s})})}}},i.prototype.activate=function(e,i,o){function s(){n.removeClass("active").find("> .dropdown-menu > .active").removeClass("active"),e.addClass("active"),r?(e[0].offsetWidth,e.addClass("in")):e.removeClass("fade"),e.parent(".dropdown-menu")&&e.closest("li.dropdown").addClass("active"),o&&o()}var n=i.find("> .active"),r=o&&t.support.transition&&n.hasClass("fade");r?n.one("bsTransitionEnd",s).emulateTransitionEnd(150):s(),n.removeClass("in")};var o=t.fn.tab;t.fn.tab=e,t.fn.tab.Constructor=i,t.fn.tab.noConflict=function(){return t.fn.tab=o,this},t(document).on("click.bs.tab.data-api",'[data-toggle="tab"], [data-toggle="pill"]',function(i){i.preventDefault(),e.call(t(this),"show")})}(jQuery),+function(t){"use strict";function e(e){return this.each(function(){var o=t(this),s=o.data("bs.affix"),n="object"==typeof e&&e;s||o.data("bs.affix",s=new i(this,n)),"string"==typeof e&&s[e]()})}var i=function(e,o){this.options=t.extend({},i.DEFAULTS,o),this.$target=t(this.options.target).on("scroll.bs.affix.data-api",t.proxy(this.checkPosition,this)).on("click.bs.affix.data-api",t.proxy(this.checkPositionWithEventLoop,this)),this.$element=t(e),this.affixed=this.unpin=this.pinnedOffset=null,this.checkPosition()};i.VERSION="3.2.0",i.RESET="affix affix-top affix-bottom",i.DEFAULTS={offset:0,target:window},i.prototype.getPinnedOffset=function(){if(this.pinnedOffset)return this.pinnedOffset;this.$element.removeClass(i.RESET).addClass("affix");var t=this.$target.scrollTop(),e=this.$element.offset();return this.pinnedOffset=e.top-t},i.prototype.checkPositionWithEventLoop=function(){setTimeout(t.proxy(this.checkPosition,this),1)},i.prototype.checkPosition=function(){if(this.$element.is(":visible")){var e=t(document).height(),o=this.$target.scrollTop(),s=this.$element.offset(),n=this.options.offset,r=n.top,a=n.bottom;"object"!=typeof n&&(a=r=n),"function"==typeof r&&(r=n.top(this.$element)),"function"==typeof a&&(a=n.bottom(this.$element));var l=null!=this.unpin&&o+this.unpin<=s.top?!1:null!=a&&s.top+this.$element.height()>=e-a?"bottom":null!=r&&r>=o?"top":!1;if(this.affixed!==l){null!=this.unpin&&this.$element.css("top","");var h="affix"+(l?"-"+l:""),p=t.Event(h+".bs.affix");this.$element.trigger(p),p.isDefaultPrevented()||(this.affixed=l,this.unpin="bottom"==l?this.getPinnedOffset():null,this.$element.removeClass(i.RESET).addClass(h).trigger(t.Event(h.replace("affix","affixed"))),"bottom"==l&&this.$element.offset({top:e-this.$element.height()-a}))}}};var o=t.fn.affix;t.fn.affix=e,t.fn.affix.Constructor=i,t.fn.affix.noConflict=function(){return t.fn.affix=o,this},t(window).on("load",function(){t('[data-spy="affix"]').each(function(){var i=t(this),o=i.data();o.offset=o.offset||{},o.offsetBottom&&(o.offset.bottom=o.offsetBottom),o.offsetTop&&(o.offset.top=o.offsetTop),e.call(i,o)})})}(jQuery),+function(t){"use strict";function e(e){return this.each(function(){var o=t(this),s=o.data("bs.collapse"),n=t.extend({},i.DEFAULTS,o.data(),"object"==typeof e&&e);!s&&n.toggle&&"show"==e&&(e=!e),s||o.data("bs.collapse",s=new i(this,n)),"string"==typeof e&&s[e]()})}var i=function(e,o){this.$element=t(e),this.options=t.extend({},i.DEFAULTS,o),this.transitioning=null,this.options.parent&&(this.$parent=t(this.options.parent)),this.options.toggle&&this.toggle()};i.VERSION="3.2.0",i.DEFAULTS={toggle:!0},i.prototype.dimension=function(){var t=this.$element.hasClass("width");return t?"width":"height"},i.prototype.show=function(){if(!this.transitioning&&!this.$element.hasClass("in")){var i=t.Event("show.bs.collapse");if(this.$element.trigger(i),!i.isDefaultPrevented()){var o=this.$parent&&this.$parent.find("> .panel > .in");if(o&&o.length){var s=o.data("bs.collapse");if(s&&s.transitioning)return;e.call(o,"hide"),s||o.data("bs.collapse",null)}var n=this.dimension();this.$element.removeClass("collapse").addClass("collapsing")[n](0),this.transitioning=1;var r=function(){this.$element.removeClass("collapsing").addClass("collapse in")[n](""),this.transitioning=0,this.$element.trigger("shown.bs.collapse")};if(!t.support.transition)return r.call(this);var a=t.camelCase(["scroll",n].join("-"));this.$element.one("bsTransitionEnd",t.proxy(r,this)).emulateTransitionEnd(350)[n](this.$element[0][a])}}},i.prototype.hide=function(){if(!this.transitioning&&this.$element.hasClass("in")){var e=t.Event("hide.bs.collapse");if(this.$element.trigger(e),!e.isDefaultPrevented()){var i=this.dimension();this.$element[i](this.$element[i]())[0].offsetHeight,this.$element.addClass("collapsing").removeClass("collapse").removeClass("in"),this.transitioning=1;var o=function(){this.transitioning=0,this.$element.trigger("hidden.bs.collapse").removeClass("collapsing").addClass("collapse")};return t.support.transition?void this.$element[i](0).one("bsTransitionEnd",t.proxy(o,this)).emulateTransitionEnd(350):o.call(this)}}},i.prototype.toggle=function(){this[this.$element.hasClass("in")?"hide":"show"]()};var o=t.fn.collapse;t.fn.collapse=e,t.fn.collapse.Constructor=i,t.fn.collapse.noConflict=function(){return t.fn.collapse=o,this},t(document).on("click.bs.collapse.data-api",'[data-toggle="collapse"]',function(i){var o,s=t(this),n=s.attr("data-target")||i.preventDefault()||(o=s.attr("href"))&&o.replace(/.*(?=#[^\s]+$)/,""),r=t(n),a=r.data("bs.collapse"),l=a?"toggle":s.data(),h=s.attr("data-parent"),p=h&&t(h);a&&a.transitioning||(p&&p.find('[data-toggle="collapse"][data-parent="'+h+'"]').not(s).addClass("collapsed"),s[r.hasClass("in")?"addClass":"removeClass"]("collapsed")),e.call(r,l)})}(jQuery),+function(t){"use strict";function e(i,o){var s=t.proxy(this.process,this);this.$body=t("body"),this.$scrollElement=t(t(i).is("body")?window:i),this.options=t.extend({},e.DEFAULTS,o),this.selector=(this.options.target||"")+" .nav li > a",this.offsets=[],this.targets=[],this.activeTarget=null,this.scrollHeight=0,this.$scrollElement.on("scroll.bs.scrollspy",s),this.refresh(),this.process()}function i(i){return this.each(function(){var o=t(this),s=o.data("bs.scrollspy"),n="object"==typeof i&&i;s||o.data("bs.scrollspy",s=new e(this,n)),"string"==typeof i&&s[i]()})}e.VERSION="3.2.0",e.DEFAULTS={offset:10},e.prototype.getScrollHeight=function(){return this.$scrollElement[0].scrollHeight||Math.max(this.$body[0].scrollHeight,document.documentElement.scrollHeight)},e.prototype.refresh=function(){var e="offset",i=0;t.isWindow(this.$scrollElement[0])||(e="position",i=this.$scrollElement.scrollTop()),this.offsets=[],this.targets=[],this.scrollHeight=this.getScrollHeight();var o=this;this.$body.find(this.selector).map(function(){var o=t(this),s=o.data("target")||o.attr("href"),n=/^#./.test(s)&&t(s);return n&&n.length&&n.is(":visible")&&[[n[e]().top+i,s]]||null}).sort(function(t,e){return t[0]-e[0]}).each(function(){o.offsets.push(this[0]),o.targets.push(this[1])})},e.prototype.process=function(){var t,e=this.$scrollElement.scrollTop()+this.options.offset,i=this.getScrollHeight(),o=this.options.offset+i-this.$scrollElement.height(),s=this.offsets,n=this.targets,r=this.activeTarget;if(this.scrollHeight!=i&&this.refresh(),e>=o)return r!=(t=n[n.length-1])&&this.activate(t);if(r&&e<=s[0])return r!=(t=n[0])&&this.activate(t);for(t=s.length;t--;)r!=n[t]&&e>=s[t]&&(!s[t+1]||e<=s[t+1])&&this.activate(n[t])},e.prototype.activate=function(e){this.activeTarget=e,t(this.selector).parentsUntil(this.options.target,".active").removeClass("active");var i=this.selector+'[data-target="'+e+'"],'+this.selector+'[href="'+e+'"]',o=t(i).parents("li").addClass("active");o.parent(".dropdown-menu").length&&(o=o.closest("li.dropdown").addClass("active")),o.trigger("activate.bs.scrollspy")};var o=t.fn.scrollspy;t.fn.scrollspy=i,t.fn.scrollspy.Constructor=e,t.fn.scrollspy.noConflict=function(){return t.fn.scrollspy=o,this},t(window).on("load.bs.scrollspy.data-api",function(){t('[data-spy="scroll"]').each(function(){var e=t(this);i.call(e,e.data())})})}(jQuery),+function(t){"use strict";function e(){var t=document.createElement("bootstrap"),e={WebkitTransition:"webkitTransitionEnd",MozTransition:"transitionend",OTransition:"oTransitionEnd otransitionend",transition:"transitionend"};for(var i in e)if(void 0!==t.style[i])return{end:e[i]};return!1}t.fn.emulateTransitionEnd=function(e){var i=!1,o=this;t(this).one("bsTransitionEnd",function(){i=!0});var s=function(){i||t(o).trigger(t.support.transition.end)};return setTimeout(s,e),this},t(function(){t.support.transition=e(),t.support.transition&&(t.event.special.bsTransitionEnd={bindType:t.support.transition.end,delegateType:t.support.transition.end,handle:function(e){return t(e.target).is(this)?e.handleObj.handler.apply(this,arguments):void 0}})})}(jQuery);
define("bootstrapjs", function(){});

// Uploads any data that is present in the uploadq to the server
// To use the module create an instance and call start_upload on it 
define('views/upload',[
    'jquery',
    'underscore',
    'layoutmanager',
    'configs',
    'views/form',
    'collections/upload_collection',
    'convert_namespace',
    'offline_utils',
    'online_utils',
    'models/user_model',
    'views/upload_status',
    'auth',
    'indexeddb-backbone',
    'bootstrapjs'
], function(jquery, underscore, layoutmanager, configs, Form, upload_collection, ConvertNamespace, Offline, Online, User, UploadStatusView, auth) {

    var UploadView = Backbone.Layout.extend({

        initialize: function() {
            console.log("UPLOAD: initializing new upload view");
            _(this).bindAll('stop_upload');
        },

        template: "#upload_template",

        events: {
            "click #stop_upload": "stop_upload"
        },


        serialize: function () {
            //send these to the list page template
            var language = User.get('language');
            return {
                language: language,
                configs: configs,
            };
        },

        //set the user_interrupt flag when user clicks on stop button - flag is checked before starting to process each upload object. So upload would be stopped after the current object bieng uploaded is finished bieng processed
        stop_upload: function() {      
            console.log("stopping upload");
            this.user_interrupt = true;
        },

        //increment the progress bar
        increment_pb: function() {
            //get the current width of progress bar
            w = parseFloat(document.getElementById('pbar').style.width);
            //increment the width with the step
            document.getElementById('pbar').style.width = (w + progress_bar_step) + '%';
        },

        //update the status on the view - # of uploaded/# of total objects
        update_status: function(status) {
            $('#upl_status').html(status);
        },

        //update the action on the view - for eg - "uploading person"
        update_action: function(action) {
            $('#upl_action').html(action);
        },

        //initializes the global vars used, ui
        initialize_upload: function() {
            this.user_interrupt = false;
            this.server_connectivity_lost = false;
            this.in_progress = true;
            this.$('#upload_modal').modal({
                keyboard: false,
                backdrop: "static",
            });
            this.$('#upload_modal').modal('show');

        },

        //removes the view
        tear_down: function() {
            this.in_progress = false;
            var that = this;
            //modal takes time to hide. Needed to get the correct point of time when upload has finished.
            $('#upload_modal').modal('hide');
            $('.modal-backdrop').remove();
        },

        // starts the upload process      
        start_upload: function() {
            var dfd = new $.Deferred();
            console.log("UPLOAD: start the upload");
            var that = this;
            //run the inititalization logic - setup global vars , ui
            this.initialize_upload();
            //retrieve the collection of objects to be uploaded
            this.get_uploadq()
                .done(function(collection) {
                    //process each object serially in the upload collection
                    that.iterate_uploadq(collection)
                        .done(function() {
                            // upload successfully finished
                            that.tear_down();
                            dfd.resolve();
                        })
                        .fail(function(error) {
                            // upload failed
                            that.tear_down();
                            dfd.reject(error);
                        });
                })
                .fail(function(error) {
                    // failed to retrieve objects to be uploaded
                    that.tear_down();
                    dfd.reject(error);
                });
            return dfd;
        },

        //Reads the uploadQ table through the upload_collection backbone collection
        get_uploadq: function() {
            var dfd = new $.Deferred();
            // upload_collection is a pre-defined backbone collection attached to the uploadQ table in offline db
            upload_collection.fetch({
                success: function(collection) {
                    dfd.resolve(collection);
                },
                error: function(error) {
                    dfd.reject(error);
                }
            });
            return dfd;
        },

        // process each object serially in the uploadQ
        iterate_uploadq: function(uploadq) {
            var dfd = new $.Deferred();
            this.upload_collection = uploadq;
            console.log("UPLOAD: inside upload queue: " + this.upload_collection.length + " entries");
            $('#num_upload').html(this.upload_collection.length);

            //step for progress bar increments    
            progress_bar_step = 100 / this.upload_collection.length;
            //stores the current download status
            this.upload_status = {};
            this.upload_status["total"] = this.upload_collection.length;
            this.upload_status["uploaded"] = 0;
            this.pick_next(dfd);
            return dfd;
        },

        //returns the entity name of the object to be uploaded
        get_entity_name: function(upload_model) {
            return upload_model.get('entity_name')
        },

        //returns the action of the object to be uploaded
        get_action: function(upload_model) {
            return upload_model.get('action');
        },

        //returns the json of the object
        get_json: function(upload_model) {
            return upload_model.get('data');
        },

        //returns the foregn field desc of the object 
        get_foreign_field_desc: function(upload_model) {
            var entity_name = this.get_entity_name(upload_model);
            if (configs[entity_name].edit) {
                return configs[entity_name].edit.foreign_entities;
            } else
                return configs[entity_name].foreign_entities;
        },

        //returns the offline id of the object 
        get_offline_id: function(upload_model) {
            return parseInt(this.get_json(upload_model).id);
        },

        //returns the online id of the object 
        get_online_id: function(upload_model) {
            return parseInt(this.get_json(upload_model).online_id);
        },

        //recursively iterates over the uploadq list till its empty
        pick_next: function(whole_upload_dfd) {
            console.log("in pick_next");
            var that = this;
            this.update_status(this.upload_status["uploaded"] + "/" + this.upload_status["total"]);
            this.current_entry = this.upload_collection.shift();
            //all uploads processed
            if (!this.current_entry) {
                return whole_upload_dfd.resolve();
            }
            //user interrupt flag is set - user clicked on stop button
            else if (this.user_interrupt) {
                //put the upload object back
                this.upload_collection.unshift(this.current_entry);
                //stop the process
                return whole_upload_dfd.reject("User stopped Sync");
            }
            else if (this.server_connectivity_lost){
                 //put the upload object back
                this.upload_collection.unshift(this.current_entry);
                //stop the process
                return whole_upload_dfd.reject("Internet Lost during Upload");
            }
            // process the object
            else {
                this.process_upload_entry(this.current_entry)
                    .fail(function(error) {
                        console.log("FAILED TO UPLOAD AN OBJECT: ");
                        console.log(error);
                        //check for internet connectivity
                        if (that.server_connectivity_lost) {
                        //put the upload object back
                        that.upload_collection.unshift(this.current_entry);
                        //stop the process
                        return whole_upload_dfd.reject("Server connection lost during Upload");
                        }
                        //it would be reached in foll cases:
                        //object to be uploaded doesn't exists in offline anymore
                        //ConvertNamespace failed
                        //online_id couldn't be injected
                        //The object discarded in upload error form could not be deleted
                        //Internet connectivity lost during upload
                    })
                    .done(function() {
                        console.log("SUCESSFULLY UPLOADED AN OBJECT");
                    })
                    .always(function() {
                        // delete the object..finished processing it
                        //if internet connectivity exists
                        if (!that.server_connectivity_lost) {
                        that.current_entry.destroy();
                        // continue processing the objects even if this object failed
                        //  increment progress bar
                        that.increment_pb();
                        // increment upload status
                        that.upload_status["uploaded"]++;
                        //recursively process the rest of the objects
                        that.pick_next(whole_upload_dfd);}
                    });
            }

        },

        //starts processing of a single upload object             
        process_upload_entry: function(up_entry) {
            var dfd = new $.Deferred();
            //update action on the view
            this.update_action("Uploading " + this.get_entity_name(up_entry));

            switch (this.get_action(up_entry)) {
                case 'A':
                    //add case
                    this.upload_add_edit(up_entry, dfd);
                    break;
                case 'E':
                    //edit case
                    this.upload_add_edit(up_entry, dfd);
                    break;
                case 'D':
                    //delete case
                    this.upload_delete(up_entry, dfd);
                    break;
                default:
                    console.log("ambiguous case");
                    dfd.reject("UPLOAD:UNEXPECTED ERROR: Ambiguous case. None of add, edit , delete!");
            }
            return dfd.promise();

        },

        upload_add_edit: function(up_model, dfd) {
            var that = this;
            //check whether the object to be added/edited still exists, get the online_id for edit case
            Offline.fetch_object(this.get_entity_name(up_model), "id", this.get_offline_id(up_model))
                .done(function(off_model) {
                    console.log("Off model fetched - " + JSON.stringify(off_model.toJSON()));
                    // convert namespace from offline to online 
                    ConvertNamespace.convert(that.get_json(up_model), that.get_foreign_field_desc(up_model), "offlinetoonline")
                        .done(function(on_off_obj) {
                            //add case - remove the offline id - server will generate its own id
                            if (that.get_action(up_model) == "A") {
                                delete on_off_obj.on_json.id;
                            } else {
                                //edit case - put the online_id as id
                                on_off_obj.on_json.id = parseInt(off_model.get("online_id"));
                                delete on_off_obj.on_json.online_id;
                            }
                            // save the object on server
                            Online.save(null, that.get_entity_name(up_model), on_off_obj.on_json)
                                .done(function(on_model) {
                                    console.log("INCD:ADD: Successfully uploaded model. uploaded model - " + JSON.stringify(on_model.toJSON()));
                                    var off_json = off_model.toJSON();
                                    // inject the online id returned by server in offline object
                                    off_json.online_id = parseInt(on_model.get("id"));
                                    Offline.save(off_model, that.get_entity_name(up_model), off_json)
                                        .done(function(off_model) {
                                            // successfully uploaded
                                            console.log("OFF model after all upload - " , JSON.stringify(off_model.toJSON()));
                                            dfd.resolve();
                                        })
                                        .fail(function(error) {
                                            dfd.reject("UPLOAD: Error saving online_id in offline obj: ", error);
                                        });
                                })
                                .fail(function(error) {
                                    // server connection not established with server/ internet connection lost 
                                    if(error.status == 0) {
                                        var uploaded = that.upload_status["uploaded"];
                                        var total = that.upload_status["total"];
                                        var pending = total - uploaded;
                                        that.tear_down();  
                                        that.server_connectivity_lost = true;
                                        that.status_view(total, uploaded, pending);
                                        dfd.reject(error);
                                    }
                                    // unauthorised server connection i.e. when user is logged out from website( when django session expires)
                                    else if(error.status == 401){
                                        alert('Session time out. Login in to Digital Green website again!');
                                        that.tear_down();
                                        that.server_connectivity_lost = true;
                                        dfd.reject(error);
                                    }
                                    // server returned error when uploading object
                                    console.log("Error while saving oject on server");
                                    that.curr_entry_dfd = dfd;
                                    // show the object in its form with the error - to let user fix it and continue with upload
                                    that.show_form(that.get_entity_name(up_model), on_off_obj.off_json, error.responseText);
                                });
                        })
                        .fail(function(model, error) {
                            // namespace conversion failed
                            console.log("UPLOAD: Not uploading object coz ConvertNamespace failed");
                            dfd.reject(error);
                        });
                })
                .fail(function(error) {
                    // the object to be added/edited doesn't exist anymore....move on
                    if (error == "Not Found") {
                        return dfd.reject("The object to be uploaded doesn't exists anymore.")
                    } else
                        dfd.reject(error);
                });
        },
        // show the status of upladed/yet to uploaded data from upload queue
        status_view: function(total, uploaded, pending) {
            console.log("Upload Status View Initialised");
            this.UploadStatusView_v = new UploadStatusView();
            //append div-modal to body of dashboard.html
            $(this.UploadStatusView_v.el)
                .appendTo('body');
            this.UploadStatusView_v.render();
            //display the modal
            $('#upload_status_modal').modal('show');
            this.UploadStatusView_v.get_status(total, uploaded, pending);
                
        },

        // show the json in its form with the error returned by server - let user fix it
        show_form: function(entity_name, json, err_msg) {
            console.log("UPLOAD:ERROR: need to show this json -" + JSON.stringify(json));
            // create a form instance with that json
            var language = User.get('language');
            p = new Form({
                serialize: {
                    button1: configs['misc']['meta_'+language]['save_again'],
                    button2: configs['misc']['meta_'+language]['discard']
                },
                entity_name: entity_name,
                model_json: json
            });
            p.render();
            // show the error on form
            p.show_errors(err_msg);
            // listen to when the user clicks save on the form
            this.listenTo(p, 'save_clicked', this.after_upload_error_save_again);
            // listen to when the user clicks discard on the form
            this.listenTo(p, 'button2_clicked', this.after_upload_error_discard);
            this.$('#upload_form')
                .html(p.el);
        },

        // executed when user has corrected an object and retried upload after server returned error
        after_upload_error_save_again: function(e) {
            console.log("UPLOAD:ERROR: edit and retry");
            console.log("UPLOAD:ERROR: json from form - " + JSON.stringify(e.context.final_json));
            // corrected object
            var after_upload_error_json = e.context.final_json;
            var that = this;
            // save the corrected json in offline db
            Offline.save(null, this.get_entity_name(this.current_entry), after_upload_error_json)
                .done(function(off_model) {
                    // remove the form
                    that.$('#upload_form')
                        .empty();
                    // edit the current upload object to set the corrected json    
                    that.current_entry.set('data', after_upload_error_json);
                    // retry uploading the corrected object 
                    that.upload_add_edit(that.current_entry, that.curr_entry_dfd);
                })
                .fail(function(error) {
                    // the corrected json is not accepted by offline db - show the new error on form
                    e.context.show_errors(error);
                });
        },

        // executed when user discards the object after server returned error
        after_upload_error_discard: function(e) {
            console.log("DISCARD");
            var that = this;
            if (this.get_action(this.current_entry) == "A") {
                // delete the object from offline db if its add case
                Offline.delete_object(null, this.get_entity_name(this.current_entry), this.get_offline_id(this.current_entry))
                    .done(function() {
                        return that.curr_entry_dfd.resolve();
                    })
                    .fail(function(error) {
                        return that.curr_entry_dfd.reject("The object discarded in upload error form could not be deleted - " , error);
                    });
            } else {
                // edit case not handled - need to revert the edit in offline db!!
                this.curr_entry_dfd.resolve();
            }
            this.$('#upload_form')
                .html("");
        },

        upload_delete: function(up_model, dfd) {
            if (this.get_online_id(up_model)) {
                // delete the object from server
                Online.delete_object(null, this.get_entity_name(up_model), this.get_online_id(up_model))
                    .done(function() {
                        return dfd.resolve();
                    })
                    .fail(function(error) {
                        return dfd.reject("The object discarded in upload error form could not be deleted - " + error);
                    });
            } else {
                // No online_id was found on the model when deleted. Therefore it was never uploaded on server. Hence taking no action.
                return dfd.resolve();
            }
        },


    });



    // Our module now returns our view
    return UploadView;
});

// Retrieves updates on server since a timestamp, runs those updates on the offline DB thus keeping the offline db in sync with server db
// To use the module create an instance and call start_incremental_download on it 
define('views/incremental_download',[
    'jquery',
    'underscore',
    'layoutmanager',
    'indexeddb_backbone_config',
    'configs',
    'convert_namespace',
    'offline_utils',
    'models/user_model',
    'indexeddb-backbone',
    'bootstrapjs',
], function(jquery, underscore, layoutmanager, indexeddb, all_configs, ConvertNamespace, Offline, User) {

    var IncrementalDownloadView = Backbone.Layout.extend({

        initialize: function() {
            console.log("UPLOAD: initializing new incremental_download view");
            _.bindAll(this);
            this.start_timestamp = null;
            this.in_progress = false;
        },

        template: "#incremental_download_template",
        events: {
            "click #stop_inc_download": "stop_inc_download"
        },
        /* The incremental download modal code in HTML is commented for now, so is this one.
        //increment the progress bar
        increment_pb: function() {
            //get the current width of progress bar
            w = parseFloat(document.getElementById('inc_pbar').style.width);
            //increment the width with the step
            document.getElementById('inc_pbar').style.width = (w + this.progress_bar_step) + '%';
        },
        */

        serialize: function () {
            //send these to the list page template
            var language = User.get('language');
            return {
                language: language,
                all_configs: all_configs,
            };
        },

        //update the status on the view - # of downloaded/# of total objects
        update_status: function(status) {
            console.log(status);
            $('#inc_status').html(status);
        },

        //update the action on the view - for eg - "downloading person"
        update_action: function(action) {
            $('#inc_action').html(action);
        },

        //set the user_interrupt flag when user clicks on stop button - flag is checked before starting to process each update. So inc download would be stopped after the current object bieng downloaded is finished bieng processed
        stop_inc_download: function() {
            console.log("stopping inc download");
            this.user_interrupt = true;
        },

        //initializes the global vars used, ui
        initialize_inc_download: function(options) {
            var dfd = new $.Deferred();
            this.in_progress = true;
            this.user_interrupt = false;
            var that = this;

            //set ui for foreground inc download
            if (!(options.background)) {
                this.template = "#incremental_download_template";
                this.render()
                    .done(function() {
                        that.$('#incremental_download_modal').modal({
                            keyboard: false,
                            backdrop: "static",
                        });
                        that.$('#incremental_download_modal').modal('show');
                        dfd.resolve();
                    });
            }
            //set ui for background inc download
            else {
                this.template = "#incremental_download_background_template";
                this.render()
                    .done(function() {
                        dfd.resolve();
                    });
            }
            return dfd.promise();
        },

        //remove the view
        tear_down: function() {
            this.$('#incremental_download_modal').modal('hide');
            $('.modal-backdrop').remove();
            this.in_progress = false;
        },

        //starts the inc download process          
        start_incremental_download: function(options) {
            var dfd = new $.Deferred();
            var that = this;
            console.log("INCREMENTAL DOWNLOAD: start the incremental_download");
            var that = this;
            //initialization logic - like setting up ui, initializing global vars
            this.initialize_inc_download(options)
                .done(function() {
                    //query the endpoint to get the list of updates
                    that.getIncObjects()
                        .done(function(objects) {
                            //serially process each update
                            that.iterate_incd_objects(objects)
                                .done(function(last_object_timestamp) {
                                    //some finish logic -  save the timestamp
                                    that.finish_download(last_object_timestamp)
                                        .done(function() {
                                            //inc download successfuly finished
                                            //remove the view
                                            that.tear_down();
                                            //resolve the process
                                            dfd.resolve();
                                        })
                                        .fail(function(error) {
                                            //something failed in finish download
                                            that.tear_down();
                                            dfd.reject(error);
                                        });
                                })
                                .fail(function(error) {
                                    //error while saving some update
                                    if (error.last_object_timestamp) {
                                        //save the timestamp of last object successfully processed so that next inc download resumes from this point
                                        that.finish_download(error.last_object_timestamp)
                                            .always(function() {
                                                that.tear_down();
                                                dfd.reject(error.err_msg);
                                            });
                                    }
                                    dfd.reject(error.err_msg)
                                });
                        })
                        .fail(function(error) {
                            //something failed while getting the updates from server
                            that.tear_down();
                            dfd.reject(error);
                        });
                });
            return dfd;
        },

        //gets the list of updates from server
        getIncObjects: function() {
            var dfd = new $.Deferred();
            //Recording the time when the request for update was sent, to update last_inc_downloaded ts if required.
            this.start_timestamp = new Date().toJSON().replace("Z", "");
            //get the timestamp since when updates have to be fetched = timestamp when last inc download was run
            this.get_last_download_timestamp()
                .done(function(timestamp) {
                    console.log("Timestamp for inc download - " + timestamp);
                    //send the get request 
                    $.get(all_configs.misc.inc_download_url, {
                        timestamp: timestamp
                    }, function() {}, "json")
                        .fail(function() {
                            dfd.reject("Incremental download objects fetch failed!");
                        })
                        .done(function(objects) {
                            //resolve and return the objects
                            dfd.resolve(objects);
                        });
                })
                .fail(function(error) {
                    dfd.reject(error);
                });
            return dfd;
        },

        //the timestamp of the time when last inc download was run is returned or if no inc download has run till now, timestamp of full download is returned
        get_last_download_timestamp: function() {
            var dfd = new $.Deferred();
            //fetch last_inc_download timestamp from meta_data table
            Offline.fetch_object("meta_data", "key", "last_inc_download")
                .done(function(model) {
                    dfd.resolve(model.get('timestamp'));
                })
                .fail(function(model, error) {
                    //no last_inc_download timestamp found
                    //fetch and  return the timestamp of last full download
                    Offline.fetch_object("meta_data", "key", "last_full_download")
                        .done(function(model) {
                            dfd.resolve(model.get('timestamp'));
                        })
                        .fail(function(model, error) {
                            dfd.reject("Neither inc download has happened before nor full download.");
                        });
                });

            return dfd;
        },

        iterate_incd_objects: function(incd_objects) {
            var dfd = new $.Deferred();
            this.incd_objects = incd_objects;
            if (!this.incd_objects.length || this.incd_objects == 0)
                return dfd.resolve();

            //step for progress bar increments    
            this.progress_bar_step = 100 / incd_objects.length;
            //stores the current download status
            this.download_status = {};
            this.download_status["total"] = incd_objects.length;
            this.download_status["downloaded"] = 0;
            console.log("INCD objects received");
            console.log(incd_objects);
            this.pick_next(dfd);
            return dfd;
        },

        //recursively iterates over the incd_objects list till its empty
        pick_next: function(whole_download_dfd) {
            var that = this;
            this.prev_incd_o = this.cur_incd_o;
            this.update_status(this.download_status["downloaded"] + "/" + this.download_status["total"]);
            this.cur_incd_o = this.incd_objects.shift();
            //all updates processed
            if (!this.cur_incd_o) {
                var update_timestamp;
                //get the timestamp of last object processed 
                if (this.prev_incd_o)
                    update_timestamp = this.get_timestamp(this.prev_incd_o)
                    //if no object was processed use the start time of inc download    
                else
                    update_timestamp = this.start_timestamp;
                return whole_download_dfd.resolve(update_timestamp);
            }
            //user interrupt flag is set - user clicked on stop button
            else if (this.user_interrupt) {
                var update_timestamp;
                //get the timestamp of last object processed 
                if (this.prev_incd_o)
                    update_timestamp = this.get_timestamp(this.prev_incd_o)
                else
                    update_timestamp = null;
                return whole_download_dfd.reject({
                    err_msg: "User stopped Sync",
                    last_object_timestamp: update_timestamp
                });
            }
            // process the object
            else {
                this.process_incd_object(this.cur_incd_o)
                    .fail(function(error) {
                        console.log("FAILED TO INC DOWNLOAD AN OBJECT: ");
                        console.log(error);
                    })
                    .done(function() {
                        console.log("SUCESSFULLY DOWNLOADED AN OBJECT");
                    })
                    .always(function() {
                        // continue processing the objects even if this object failed
                        //  increment progress bar
                        //that.increment_pb();
                        // increment download status
                        that.download_status["downloaded"]++;
                        //recursively process the rest of the objects
                        that.pick_next(whole_download_dfd);
                    });
            }
        },

        //format of each object: {"pk":9372,"model":"dashboard.serverlog","fields":{"action":1,"timestamp":"2013-04-15T06:47:35","entry_table":"Screening","model_id":10000000132086}}
        // get the timestamp from object
        get_timestamp: function(obj) {
            return obj.fields.timestamp;
        },
        //get entity_name from object
        get_entity_name: function(obj) {
            for (var member in all_configs) {
                if (member == obj.fields.entry_table.toLowerCase()) {
                    return all_configs[member].entity_name;
                } else if ((all_configs[member].inc_table_name) && (all_configs[member].inc_table_name == obj.fields.entry_table.toLowerCase())) {
                    return all_configs[member].entity_name;
                }
            }
            return -1;
        },
        //get action from object
        get_action: function(obj) {
            return obj.fields.action;
        },
        //get online_id from object
        get_online_id: function(obj) {
            return parseInt(obj.fields.model_id);
        },
        //get foreign field desc object for this object
        get_foreign_field_desc: function(obj) {
            var entity_name = this.get_entity_name(obj);
            if (all_configs[entity_name].edit) {
                return all_configs[entity_name].edit.foreign_entities;
            } else
                return all_configs[entity_name].foreign_entities;
        },

        //runs an update object on the offline db             
        process_incd_object: function(incd_o) {
            var dfd = new $.Deferred();
            var that = this;
            // create online and offline backbone models for this entity
            // should be using the offline_utils and online_utils instead
            var generic_model_offline = Backbone.Model.extend({
                database: indexeddb,
                storeName: this.get_entity_name(incd_o),
            });
            var generic_model_online = Backbone.Model.extend({
                sync: Backbone.ajaxSync,
                url: function() {
                    return this.id ? all_configs[that.get_entity_name(incd_o)].rest_api_url + this.id + "/" : all_configs[that.get_entity_name(incd_o)].rest_api_url;
                },
            });
            this.offline_model = new generic_model_offline();
            this.online_model = new generic_model_online();
            
            //update action on the view
            this.update_action("Downloading " + this.get_entity_name(incd_o));
            
            switch (this.get_action(incd_o)) {
                // add case
                case 1:
                    this.incd_add(incd_o, dfd);
                    break;
                // edit case
                case 0:
                    this.incd_edit(incd_o, dfd);
                    break;
                // delete case    
                case -1:
                    this.incd_delete(incd_o, dfd);
                    break;
                default:
                    console.log("ambiguous case");
                    dfd.reject("ambiguous case. None of add, edit , delete!");
            }
            return dfd.promise();
        },
        
        // runs an add-update on offline db
        incd_add: function(incd_o, dfd) {
            var that = this;
            //fetch object from offline db - check whether it already exists
            this.fetch_from_offline(this.get_online_id(incd_o))
                .fail(function(error) {
                    if (error == "Not Found") {
                        fetch_and_add();
                    }
                })
                .done(function(off_model) {
                    // console.log("INCD: The model supposed to be added already exists. Moving on...");
                    fetch_and_add(off_model);
                });

            function fetch_and_add(existing_model) {
                //fetch update object from server
                that.fetch_from_online(that.get_online_id(incd_o))
                    .done(function(on_model) {
                        //convert namespace from online to offline
                        ConvertNamespace.convert(on_model.toJSON(), that.get_foreign_field_desc(incd_o), "onlinetooffline")
                            .done(function(on_off_obj) {
                                var off_json = on_off_obj.off_json;
                                //inject online id and remove server id so that offline DB generate its own id for this object
                                if (off_json.id) {
                                    off_json.online_id = parseInt(off_json.id);
                                    delete off_json.id;
                                }
                                //if the object with this online id already existed in offline DB it wud be over-written otherwise new one wud be created
                                Offline.save(existing_model, that.get_entity_name(incd_o), off_json)
                                    .done(function(off_model) {
                                        dfd.resolve();
                                    })
                                    .fail(function(error) {
                                        dfd.reject(error);
                                    });
                            })
                            .fail(function(error) {
                            	console.log("INCD: Failed convertnamespace..not saving ");
                            	dfd.reject(error);
                            });
                    })
                    .fail(function(response) {
                        // console.log("INCD: Error fetching model from server - "+response.statusText);
                        dfd.reject(response);
                    });
            }
        },

        // runs an edit-update on offline db
        incd_edit: function(incd_o, dfd) {
            var that = this;
            //fetch this object from offline db
            this.fetch_from_offline(this.get_online_id(incd_o))
                .done(function(off_model) {
                    //fetch the object from server
                    that.fetch_from_online(that.get_online_id(incd_o))
                        .done(function(on_model) {
                            //convert namespace of foreign elements in server object from online to offline
                            ConvertNamespace.convert(on_model.toJSON(), that.get_foreign_field_desc(incd_o), "onlinetooffline")
                                .done(function(on_off_obj) {
                                    //save the edit on offline db - remove this and use offline_utils instead
                                    that.edit_offline(off_model, on_off_obj.off_json)
                                        .done(function(off_model) {
                                            //  successfully edited in offline db
                                            dfd.resolve();
                                        })
                                        .fail(function(error) {
                                            //edit save failed
                                            dfd.reject(error);
                                        });
                                })
                                .fail(function(error) {
                                    //namespace conversion failed
                                    dfd.reject(error);
                                });
                        })
                        .fail(function(response) {
                            //server fetch failed
                            dfd.reject(response);
                        });
                })
                .fail(function(error) {
                    // object which was edited on server does not exist in offline DB...doing nothing...
                    dfd.reject("Error fetching model(to be edited) from offline db. Moving on..." + error);
                });
        },

        // runs a delete-update on offline db
        incd_delete: function(incd_o, dfd) {
            console.log("processing delete - " + JSON.stringify(incd_o));
            var that = this;
            //fetch object from offline db
            this.fetch_from_offline(this.get_online_id(incd_o))
                .done(function(off_model) {
                    //delete the object 
                    off_model.destroy({
                        success: function() {
                            dfd.resolve();
                        },
                        error: function(error) {
                            dfd.reject();
                        }
                    })
                })
                .fail(function(error) {
                    // object to be deleted already doesn't exists in offline db 
                    dfd.resolve(error);
                });
        },

        //executed at end of the inc download process
        finish_download: function(last_object_timestamp) {
            var dfd = new $.Deferred();
            var that = this;
            //possible if timestamp of last object in incd was not present or no objects were returned
            if (!last_object_timestamp)
                last_object_timestamp = this.start_timestamp;

            //update timestamp of last inc download in meta_data table    
            Offline.fetch_object("meta_data", "key", "last_inc_download")
                .done(function(model) {
                    set_timestamp(model);
                })
                .fail(function(model, error) {
                    set_timestamp(model);
                });

            function set_timestamp(model) {
                model.set('timestamp', last_object_timestamp);
                model.save(null, {
                    success: function() {
                        dfd.resolve();
                    },
                    error: function(model, error) {
                        dfd.reject("error updating last_full_download in meta_data objectStore");
                    }
                });
            };

            return dfd;
        },

        // all of the following functions should be removed and offline_utils and online_utils should be used instead - the dependence on global offline_model and online_model would also have to be removed
        
        //fetch object with online_id=online_id from offline db
        fetch_from_offline: function(online_id) {
            var dfd = new $.Deferred();
            this.offline_model.clear();
            this.offline_model.set({
                online_id: parseInt(online_id)
            });
            this.offline_model.fetch({
                success: function(off_model) {
                    dfd.resolve(off_model);
                },
                error: function(model, error) {
                    dfd.reject(error);
                }
            });
            return dfd.promise();
        },

        // fetch object with id=online_id from server 
        fetch_from_online: function(online_id) {
            var dfd = new $.Deferred();
            this.online_model.clear();
            this.online_model.set('id', parseInt(online_id));
            this.online_model.fetch({
                success: function(on_model, response) {
                    dfd.resolve(on_model);
                },
                error: function(model, response, options) {
                    dfd.reject(response);
                }
            });
            return dfd.promise();
        },

        // adds json object in offline db using offline_model
        add_offline: function(json) {
            var dfd = new $.Deferred();
            this.offline_model.clear();
            this.offline_model.set(json);
            this.offline_model.set('online_id', parseInt(json.id));
            this.offline_model.unset('id'); //new id would be generated, not saving by server id
            this.offline_model.save(null, {
                success: function(off_model) {
                    dfd.resolve(off_model);
                },
                error: function(model, error) {
                    dfd.reject(error);
                }
            });
            return dfd.promise();
        },

        // edits the object in off_model to json
        edit_offline: function(off_model, json) {
            var dfd = new $.Deferred();
            var offline_id = off_model.get("id");
            var online_id = json.id;
            off_model.set(json);
            off_model.set('id', parseInt(offline_id));
            off_model.set('online_id', parseInt(online_id));
            off_model.save(null, {
                success: function(off_model) {
                    dfd.resolve(off_model);
                },
                error: function(model, error) {
                    dfd.reject("ERRO EDITING model in IDB: ");
                }
            });
            return dfd.promise();
        },

    });

    return IncrementalDownloadView;
});

// Performs the full database download. For each entity defined in configs, creates chunked requests to fetch data 
// from server and saves it in offline db. To make it resumable, it does not clear the database before starting downloading. 
// For each chunk request created, it checks if that chunk request was already downloaded by looking into the full_download_info store in offline DB. 
// Since it continues from the present state of database found - In order to do a fresh download, there needs to be some 
// external code which flushes the database before calling this module.
// 
// To use the module, initialize a new object and call start_full_download on it.

define('views/full_download',[
    'jquery',
    'underscore',
    'layoutmanager',
    'indexeddb_backbone_config',
    'configs',
    'offline_utils',
    'models/user_model',
    'bootstrapjs'
], function(jquery, underscore, layoutmanager, indexeddb, all_configs, Offline, User) {


    var FullDownloadView = Backbone.Layout.extend({

        initialize: function() {
            _.bindAll(this);
        },

        template: "#download_template",

        internet_connected: function() {
            return navigator.onLine;
        },

        //send the list of entities to the template 
        serialize: function() {
            var language = User.get("language");
            return {
                language: language,
                all_configs: all_configs
            }
        },

        events: {
            'click #stop_full_download': 'stop_download'
        },

        //executed when user clicks stop donwload button 
        stop_download: function() {
            console.log("stopping download");
            //remove the view
            this.remove_ui();
            //abort all the network requests made by this module
            $.each(this.network_requests, function(index, xhr) {
                xhr.abort();
            });

            this.full_download_dfd.reject("User stopped download");

        },

        remove_ui: function() {
            // calling remove without hiding modal causes modal's backdrop to remain
            this.$('#full_download_modal').modal('hide');
            $('.modal-backdrop').remove();
            
        },

        // Checks internet connectivity
        // Initializes UI and objects used to update status. 
        // Fetches the full_download_info objectStore to resume download, if that's the case
        // Stores the start time for download
        initialize_download: function() {
            //Django complains when Z is present in timestamp bcoz timezone capab is off
            this.start_time = new Date().toJSON().replace("Z", "");

            //check whether internet is accessible - if not, abort full download
            if (!this.internet_connected()) {
                // this function is expected to return a dfd, so create a new dfd, reject it and return it
                var dfd = new $.Deferred();
                dfd.reject("Can't download database. Internet is not connected");
                return dfd;
            }
            //intialize UI objects
            this.$('#full_download_modal').modal({
                keyboard: false,
                backdrop: "static",
            });
            this.$('#full_download_modal').modal('show');
            
            //used to store the current download-status of each entity  
            this.download_status = {};

            //every request made to server will be stored in this, - to abort them if user chooses to stop download
            this.network_requests = [];

            //get the list of chunks that exists already downloaded - to resume download 
            var already_downloaded_chunks_dfd = this.get_already_downloaded_chunks();
            
            //get the original start time if download is resumed or else set th current time as the start time
            var start_time_dfd = this.fetch_or_set_download_start_time();
            
            //return combined dfd 
            return $.when.apply($, [already_downloaded_chunks_dfd, start_time_dfd]);
        },

        // fetching the full_download_info table to get all already downloaded chunks - to be used for resuming download
        get_already_downloaded_chunks: function() {
            var dfd = new $.Deferred();
            var that = this;
            Offline.fetch_collection("full_download_info")
                .done(function(coll) {
                    that.full_download_info_coll = coll;
                    dfd.resolve();
                })
                .fail(function(error) {
                    dfd.reject(error);
                });
            return dfd;

        },

        //if download is resuming then get the original start time other wise record current time as start time
        fetch_or_set_download_start_time: function() {
            var dfd = new $.Deferred();
            var that = this;
            Offline.fetch_object("meta_data", "key", "last_full_download_start")
                .fail(function(model, error) {
                    that.set_timestamp(model, that.start_time)
                        .done(function() {
                            dfd.resolve();
                        })
                        .fail(function(error) {
                            dfd.reject(error);
                        });
                })
                .done(function(model) {
                    that.start_time = model.get("timestamp");
                    dfd.resolve();
                });
            return dfd;
        },

        set_timestamp: function(model, timestamp) {
            model.set('timestamp', timestamp);
            //returns a promise object
            return model.save(); 
        },

        // this starts the full download process 
        start_full_download: function() {
            this.full_download_dfd = new $.Deferred();
            var that = this;
            //run some intitialization logic - check internt, setup ui etc
            this.initialize_download()
                .done(function() {
                    //iterate over entities and start their download
                    that.iterate_object_stores()
                        .done(function() {
                            //run some finish logic - save the timsetamp 
                            that.finish_download()
                                .done(function() {
                                    //run any after download logic defined by user
                                    that.call_after_download()
                                        .done(function() {
                                            // full download finised successfully
                                            that.remove_ui();
                                            that.full_download_dfd.resolve();
                                        })
                                        .fail(function(error) {
                                            //user defined after download failed
                                            that.remove_ui();
                                            that.full_download_dfd.reject(error);
                                        });
                                })
                                .fail(function(error) {
                                    //something in finish download failed
                                    that.remove_ui();
                                    that.full_download_dfd.reject(error);
                                });
                        })
                        .fail(function(error) {
                            //soemthing failed while iterating entities and their download
                            that.remove_ui();
                            that.full_download_dfd.reject(error);
                        })
                })
                .fail(function(error) {
                    //something failed in intialization
                    that.remove_ui();
                    that.full_download_dfd.reject(error);
                });

            return this.full_download_dfd;
        },

        //executed at the end of full download
        call_after_download: function() {
            //if user has defined afterFullDownload in configs, then execute it
            //must return a promise
            if (all_configs.misc.afterFullDownload)
                return all_configs.misc.afterFullDownload(this.start_time, this.download_status) 
            else
                return new $.Deferred().resolve();
        },

        // Starts download for all tables defined in config object. Rejects when any of them fails, Resolves when all are 
//         successfully downloaded
        iterate_object_stores: function() {
            var dfd = new $.Deferred();
            this.$('#stop_full_download').prop("disabled", false);
            //stores the dfds for each entity's download process
            var entity_dfds = [];
            
            //iterate over the entities
            for (var member in all_configs) {
                if (member == "misc")
                    continue;
                //initialize the current download-status for entity    
                this.download_status[member] = {
                    total: null,
                    downloaded: 0
                };
                //start full download for entity
                var entity_dfd = this.start_full_download_for_entity(all_configs[member]["entity_name"]);
                entity_dfds.push(entity_dfd);
            }
            
            //resolve when all entities have been downloaded, reject if any fails
            $.when.apply($, entity_dfds)
                .done(function() {
                    dfd.resolve();
                })
                .fail(function(error) {
                    dfd.reject(error);
                });
            return dfd;
        },

        //updates the progress bar
        update_pb_ui: function() {
            //can't fill progress bar untill total num of objects is known
            var ready_to_show = true;
            var total = 0;
            var downloaded = 0;
            //calculate the current status of download by looking at status of each entity
            _.each(this.download_status, function(status, entity) {
                //if total objects for any entity are not yet known, then can't show the progress
                if (status.total == null) {
                    ready_to_show = false;
                    return;
                } else {
                    //calculate the total num of objects bieng downloaded
                    total += status.total;
                    //calculate the total num of objects that have been downloaded
                    downloaded += status.downloaded;
                }
            });

            if (!ready_to_show)
                return;
            //set the progress bar with current progress    
            var percent_complete = (downloaded / total) * 100 + "%";
            $('#pbar').css("width", percent_complete);
        },
        
        //updates download-status display for an entity - entity_name | status(In Progress/Done) | #downloaded/#total
        update_status_ui: function(entity_name) {
            //get the # of downloaded objects for thi entity
            var downloaded = this.download_status[entity_name].downloaded;
            //get the # of total objects for thi entity
            var total = this.download_status[entity_name].total;
            //get the language chosen by user
            var language = User.get('language');
            //set the text
            var s_text = all_configs['misc']['meta_'+language]['inprogress'];
            if (downloaded >= total)
                s_text = all_configs['misc']['meta_'+language]['done'];
            //set the num
            var s_num = String(downloaded) + "/" + String(total);
            
            //update the view
            this.$('#' + entity_name).find('.status_text').html(s_text);
            this.$('#' + entity_name).find('.status_numbers').html(s_num);
        },

        //starts download for an entity 
        start_full_download_for_entity: function(entity_name) {
            var dfd = new $.Deferred();
            var that = this;
            //get the num of objects to be downloaded for this entity 
            that.get_num_of_objects_to_download(entity_name)
                .done(function(total_num_objects) {
                    //do the chunked download
                    that.chunk_it_fetch_it_save_it(entity_name, total_num_objects)
                        .done(function() {
                            //entity successfully downloaded
                            console.log("FINISHED DOWNLOADING - " + entity_name);
                            return dfd.resolve();
                        })
                        .fail(function(error) {
                            //error while downloading entity
                            return dfd.reject(error);
                        });
                })
                .fail(function() {
                    //error while retrieving total # of objects
                    console.log("DASHBOARD:DOWNLOAD:UnexpectedError: Error fetching num of objects to download for - " + entity_name);
                    return dfd.reject("Failed to fetch num of objects for - " + entity_name);
                });
            return dfd;
        },

        //does a small GET request to retrieve total # of objects to be downloaded for an entity
        get_num_of_objects_to_download: function(entity_name) {
            var dfd = new $.Deferred();
            console.log("DASHBOARD:DOWNLOAD: Fetching num of objects to download for - " + entity_name);
            //send GET request to download 1 object of entity type - the api must return the total # of objects info too
            var xhr = $.get(all_configs[entity_name].rest_api_url, {
                limit: 1,
                offset: 0
            }, function(data) {
                //return the total_count param
                if (data && data.meta)
                    return dfd.resolve(data.meta.total_count);
                else
                    return dfd.reject();
            });
            this.network_requests.push(xhr);
            return dfd;
        },
        
        //update the downlaod status of an entity - key= total/downloaded
        update_download_status: function(entity_name, key, increment) {
            var s_obj = this.download_status[entity_name];
            if (!s_obj[key])
                s_obj[key] = increment;
            else
                s_obj[key] += increment;
            
            //update the view     
            this.update_status_ui(entity_name);
            this.update_pb_ui();

        },

        chunk_it_fetch_it_save_it: function(entity_name, total_num_objects) {
            var dfd = new $.Deferred();
            this.update_download_status(entity_name, "total", total_num_objects);
            //default chunk size
            var limit = 1500; 
            //get entity specific config if defined by user
            if (all_configs[entity_name].download_chunk_size) 
                limit = all_configs[entity_name].download_chunk_size;
            // else get global option if defined by user   
            else if (all_configs.misc.download_chunk_size) 
                limit = all_configs.misc.download_chunk_size;
            
            //calc num of chunks    
            var num_chunks = Math.ceil(total_num_objects / limit);
            console.log("Num of chunks for - " + entity_name + " = " + num_chunks);
            var offset = 0;
            var chunk_dfds = [];
            var that = this;
            //process each chunk
            for (var i = 0; i < num_chunks; i++) {
                var chunk_dfd = this.process_chunk(entity_name, offset, limit);
                chunk_dfd.done(function(num_objects_saved) {
                    //update download-status of this entity with the num of objects that were downloaded in this chunk
                    that.update_download_status(entity_name, "downloaded", num_objects_saved);
                });
                chunk_dfds.push(chunk_dfd);
                offset += limit;
            }

            // resolve when all chunks of this entity are processed...
            $.when.apply($, chunk_dfds)
                .done(function() {
                    return dfd.resolve();
                })
                .fail(function(error) {
                    return dfd.reject(error);
                });
            return dfd;
        },

        process_chunk: function(entity_name, offset, limit) {
            var dfd = new $.Deferred();
            var that = this;
            //check whether chunks is already downloaded
            var num_downloaded = this.is_already_downloaded(entity_name, offset, limit);
            //return if chunk already downloaded
            if (num_downloaded != -1)
                dfd.resolve(num_downloaded);
            else {
                //fetach and save the chunk
                this.fetch_save(entity_name, offset, limit)
                    .done(function(num_downloaded) {
                        //record the chunk as downloaded when successfully downloaded
                        that.save_as_downloaded(entity_name, offset, limit, num_downloaded);
                        //return the num of objects that were downloaded in this chunk
                        dfd.resolve(num_downloaded);
                    })
                    .fail(function(error) {
                        //chunk download failed
                        dfd.reject(error);
                    });
            }

            return dfd;
        },

        //checks if (entity_name, offset, limit) chunk exists in full_download_info
        is_already_downloaded: function(entity_name, offset, limit) {
            var exists = this.full_download_info_coll.where({
                entity_name: entity_name,
                offset: offset,
                limit: limit
            });
            // return num of objects that were downloaded if it exists, -1 otherwise
            if (exists.length) {
                console.log("CHUNK ALREADY EXISTS DOWNLOADED");
                return exists[0].get("num_objects_downloaded");
            }
            return -1
        },

        // creates (entity_name, offset, limit, num_downloaded) object in full_download_info 
        save_as_downloaded: function(entity_name, offset, limit, num_downloaded) {
            this.full_download_info_coll.create({
                entity_name: entity_name,
                offset: offset,
                limit: limit,
                num_objects_downloaded: num_downloaded
            }, {
                success: function(model) {
                    console.log("CHUNK SAVED AS DOWNLOADED-" + JSON.stringify(model));
                }
            });
        },
        
        //fetch and save the chunk
        fetch_save: function(entity_name, offset, limit) {
            var dfd = new $.Deferred();
            var that = this;
            //fetches the chunk from server 
            this.fetch_collection(entity_name, offset, limit)
                .done(function(collection) {
                    //saves the fetched chunk 
                    that.save_collection(entity_name, collection)
                        .done(function() {
                            //successfully fetched and saved
                            //return the number of objects downloaded in this chunk
                            return dfd.resolve(collection.length);
                        })
                        .fail(function(error) {
                            //error while saving chunk
                            return dfd.reject("DOWNLOAD: Failed to save an object of " + entity_name + " - " + error);
                        });
                })
                .fail(function() {
                    //error while fetching chunk
                    console.log("DASHBOARD:DOWNLOAD: error fetching collection from server");
                    return dfd.reject("DOWNLOAD: Failed to fetch collection for " + entity_name);
                });
            return dfd;
        },
        
        //shd be removed and online_utils shd be used instead
        //fetches the chunk from server and returns as a backbone collection
        fetch_collection: function(entity_name, offset, limit) {
            var dfd = new $.Deferred();
            var generic_collection_online = Backbone.Collection.extend({
                url: all_configs[entity_name].rest_api_url,
                sync: Backbone.ajaxSync,
                parse: function(data) {
                    return data.objects;
                }
            });
            var collection_online = new generic_collection_online();
            var xhr = collection_online.fetch({
                data: {
                    limit: limit,
                    offset: offset
                },
                success: function(collection) {
                    return dfd.resolve(collection);
                },
                error: function() {
                    return dfd.reject();
                }
            });
            this.network_requests.push(xhr);
            return dfd;
        },

        save_collection: function(entity_name, collection) {
            var dfd = new $.Deferred();
            var objects = collection.toJSON();
            var dfds = [];
            for (var i = 0; i < objects.length; i++) {
                objects[i]['id'] = parseInt(objects[i]['id']);
                //in each object, inject 'online_id' 
                objects[i]['online_id'] = parseInt(objects[i]['id']);
                //save the object
                var s_dfd = this.save_object(entity_name, objects[i]);
                dfds.push(s_dfd);
            }
            //resolve when all objects are successfully saved, reject if any save fails
            $.when.apply($, dfds)
                .done(function() {
                    return dfd.resolve();
                })
                .fail(function(error) {
                    console.log(error);
                    return dfd.reject();
                });
            return dfd;
        },

        // custom save to allow constraint error fails - can't use the offline_utils save
        save_object: function(entity_name, json) {
            var dfd = new $.Deferred();
            var model = Offline.create_b_model(entity_name);
            model.save(json, {
                success: function() {
                    return dfd.resolve();
                },
                error: function(model, error) {
                    //pass the save as successful if it is a constraint/unique_together error
                    if (error.srcElement.error.name == "ConstraintError") {
                        return dfd.resolve();
                    }
                    return dfd.reject();
                }
            });
            return dfd;
        },

        finish_download: function() {
            var dfd = new $.Deferred();
            console.log("DASHBOARD:DOWNLOAD: In finish download");
            var that = this;
            that.db_downloaded();

            //save the start time of download in meta_data table - used later as an indicator that database has been fully downloaded and also as a timestamp for first inc download
            Offline.fetch_object("meta_data", "key", "last_full_download")
                .done(function(model) {
                    that.set_timestamp(model, that.start_time)
                        .done(function() {
                            dfd.resolve();
                        })
                        .fail(function(error) {
                            dfd.reject(error);
                        });
                })
                .fail(function(model, error) {
                    that.set_timestamp(model, that.start_time)
                        .done(function() {
                            dfd.resolve();
                        })
                        .fail(function(error) {
                            dfd.reject(error);
                        });
                });

            return dfd;
        },
        
        //enable links in dashboard
        db_downloaded: function() {
            $('.list_items').unbind('click', false);
            $('.list_items').removeClass("disabled");
            console.log("Dashboard links enabled");
            $("#helptext").hide();
        }




    });

    return FullDownloadView;
});

//This view contains the links to add and list pages of entities, the sync button, logout link, online-offline indicator
define('views/dashboard',['jquery', 'underscore', 'configs', 'indexeddb_backbone_config', 'collections/upload_collection', 'views/upload', 'views/incremental_download', 'views/notification', 'layoutmanager', 'models/user_model', 'auth', 'offline_utils', 'views/full_download' ],

function(jquery, pass, configs, indexeddb, upload_collection, UploadView, IncDownloadView, notifs_view, layoutmanager, User, Auth, Offline, FullDownloadView) {

    var DashboardView = Backbone.Layout.extend({
        template: "#dashboard",
        events: {
            "click #sync": "sync",
            "click #inc_download": "inc_download",
        },
        item_template: _.template($("#dashboard_item_template")
            .html()),

        initialize: function() {
            this.upload_v = null;
            this.inc_download_v = null;
            //start the background inc download process
            this.background_download();
            _(this)
                .bindAll('render');                                                             
            //re-render the view when User model changes - to keep username updated
            User.on('change', this.render);
            this.upload_entries = upload_collection.length;
        },

        serialize: function() {
            // send username and # of uploadQ items to the template 
            var username = User.get("username");
            var language = User.get("language");
            if(language === undefined) {
                    language = configs.misc.meta_default;
            }
            return {
                username: username,
                language: language,
                configs: configs,
                upload_entries: this.upload_entries
            }
        },

        afterRender: function() { 
            console.log("rendering dashboard");
            //iterate over entities defined in config and create their "list" and "add" rows 
            for (var member in configs) {
                var language = User.get("language");
                if(language === undefined) {
                    language = configs.misc.meta_default;
                }
                if (member == "misc") continue;
                var listing = true;
                var add = true;
                var enable_months;
                // check entity's config for whether to show list/add links for this entity
                if (configs[member].dashboard_display) {
                    listing = configs[member].dashboard_display.listing;
                    add = configs[member].dashboard_display.add;
                    enable_months = configs[member].dashboard_display.enable_months;
                }
                if(typeof enable_months != 'undefined'){
                	var d = new Date();
                    n = d.getMonth() + 1;
                    res = $.inArray(n, enable_months);
                    if(res === -1){
                    	add = false;
                    }
                }
                if (listing || add) {
                    if (listing) $('#dashboard_items')
                        .append(this.item_template({
                        name: member + "/list",
                        title: configs[member]['config_'+language]
                    }));

                    if (add) $('#dashboard_items_add')
                        .append(this.item_template({
                        name: member + "/add",
                        title: '<i class="glyphicon glyphicon-plus-sign"></i>'
                    }));
                    else $('#dashboard_items_add')
                        .append("<li class='disabled'><a><i class='glyphicon glyphicon-plus-sign' title='You are not allowed to add this currently'></a></li>");
                }
            }
            this.upload_entries = upload_collection.length;
            //keep the # uploadq entries shown on view up-to-date
            upload_collection.on('all', function() {
                $("#upload_num")
                    .html(function() {
                    return upload_collection.length;
                });
            });
            
            var that = this;
            
            //disable all links of db not yet downloaded
            Offline.fetch_object("meta_data", "key", "last_full_download")
                .done(function(model) {
                that.db_downloaded();
            })
                .fail(function(model, error) {
                //that.db_not_downloaded();
                console.log("DB not downloaded");
            });
            
            // $("#main-navbar").on('click',function(){
            //     $(".collapse").collapse('hide');
            // });
            $("#main-navbar").on('click',function(){
                    if($(window).width()<768)
                        $(".collapse").collapse('hide');
            });
            if(User.isOnline()){
                $('#sync').removeAttr("disabled");
            }
            else{
                $('#sync').attr('disabled', true);
            }
        },
        
        //enable add, list links
        db_downloaded: function() {
            $('.list_items')
                .unbind('click', false);
            $('.list_items')
                .removeClass("disabled");
            console.log("Dashboard links enabled");
            $("#helptext")
                .hide();
        },

        //disable add, list links
        /*db_not_downloaded: function() {
            $('.list_items')
                .bind('click', false);
            $('.list_items')
                .addClass("disabled");
            console.log("Dashboard links disabled");
            $("#helptext")
                .show();
        },*/

        //if DB exists initiate upload and then inc download otherwise start full download
        sync: function() {
            var that = this;
            if (this.inc_download_v && this.inc_download_v.in_progress) {
                alert("Please wait till background download is finished.");
                return;
            }
            Offline.fetch_object("meta_data", "key", "last_full_download")
                .done(function(model) {
                console.log("In Sync: db completely downloaded");
                that.sync_in_progress = true;
                //start upload
                that.upload()
                    .done(function() {
                    console.log("UPLOAD FINISHED");
                    notifs_view.add_alert({
                        notif_type: "success",
                        message: "Sync successfully finished"
                    });
                })
                    .fail(function(error) {
                    console.log("ERROR IN UPLOAD :" + error);
                    notifs_view.add_alert({
                        notif_type: "error",
                        message: "Sync Incomplete. Failed to finish upload : " + error
                    });
                })
                    .always(function() {
                    //upload finished
                    //start inc download - even if upload failed and internet connectivity is available 
                    if(!UploadView.server_connectivity_lost)  {
                        that.inc_download({
                            background: false
                        })
                            .done(function() {
                            console.log("INC DOWNLOAD FINISHED");
                            that.sync_in_progress = false;
                            notifs_view.add_alert({
                                notif_type: "success",
                                message: "Incremental download successfully finished"
                            });
                        })
                            .fail(function(error) {
                            console.log("ERROR IN INC DOWNLOAD");
                            console.log(error);
                            that.sync_in_progress = false;
                            notifs_view.add_alert({
                                notif_type: "error",
                                message: "Sync Incomplete. Failed to do Incremental Download: " + error
                            });
                        });
                    }
                });
            })
                .fail(function(model, error) {
                // if DB is not downloaded, start the full download    
                if (error == "Not Found") {
                    that.render()
                        .done(function() {
                        console.log("In Sync: db not completely downloaded");
                        that.download();
                    });
                }
            });
        },
        
        //method to initiate full download
        download: function() {
            var dfd = new $.Deferred();
            //create full download view
            if (!this.full_download_v) {
                this.full_download_v = new FullDownloadView();
            }
            //this view has a modal interface therefore appending to body
            $(this.full_download_v.el)
                .appendTo('body');
            this.full_download_v.render();
            var that = this;
            //start full download
            this.full_download_v.start_full_download()
                .done(function() {
                notifs_view.add_alert({
                    notif_type: "success",
                    message: "Successfully downloaded the database"
                });
                dfd.resolve();
            })
                .fail(function(error) {
                notifs_view.add_alert({
                    notif_type: "error",
                    message: "Failed to download the database : " + error
                });
                dfd.reject();
            });
            return dfd;
        },

        //method to initiate upload
        upload: function() {
            var dfd = $.Deferred();
            if (!this.upload_v) {
                this.upload_v = new UploadView();
            }
            $(this.upload_v.el)
                .appendTo('body');
            this.upload_v.render();
            this.upload_v.start_upload()
                .done(function() {
                return dfd.resolve();
            })
                .fail(function(error) {
                return dfd.reject(error);
            });
            return dfd;
        },

        //method to initiate inc download
        inc_download: function(options) {
            var dfd = $.Deferred();
            var that = this;
            if (!this.inc_download_v) {
                this.inc_download_v = new IncDownloadView();
            }
            if (this.inc_download_v.in_progress) {
                return dfd.resolve();
            }
            $(this.inc_download_v.el)
                .appendTo('body');
            //options contains whether to show modal or do it in background    
            this.inc_download_v.start_incremental_download(options)
                .done(function() {
                return dfd.resolve();
            })
                .fail(function(error) {
                return dfd.reject();
            });
            return dfd;
        },
        
        //starts the background inc download process
        background_download: function() {
            var that = this;
            console.log("Going for background inc download");
            
            //function to set timer to start inc download after time interval defined in config file
            var call_again = function() {
                setTimeout(function() {
                    that.background_download();
                }, configs.misc.background_download_interval);
            };

            //check if uploadqueue is empty and internet is connected - if both true do the background download
            if (this.is_uploadqueue_empty() && this.is_internet_connected() && !this.sync_in_progress) this.inc_download({
                background: true
            })
            //when the inc download is finished set the timer to start it again later
                .always(call_again);
            //if cant do inc download right now, just set the timer to start it again later    
            else call_again();
        },

        // check emptiness of uploadQ
        is_uploadqueue_empty: function() {
            //return false if the check is made before uploadQ collection could be fetched from DB
            return upload_collection.fetched && upload_collection.length <= 0;
        },

        // check internet connection
        is_internet_connected: function() {
            return navigator.onLine;
        }
    });

    // Our module now returns our view
    return DashboardView;
});

//This view the page header containt the branding, and the user profile - along with the username and logout action.
define('views/app_header',['jquery', 'underscore', 'configs', 'layoutmanager', 'models/user_model', 'auth'],

function(jquery, pass, configs, layoutmanager, User, Auth) {

    var HeaderView = Backbone.Layout.extend({
        template: "#page_header",
        events: {
            "click #logout": "logout",
            "click .js_language": "language",
        },
        
        initialize: function() {
            _(this)
                .bindAll('render');
            // Re-render the view when User model changes - to keep username updated    
            User.on('change', this.render);
        },

        serialize: function() {
            // Send username 
            var username = User.get("username");
            var language = User.get("language");
            return {
                username: username,
                language: language,
                configs: configs
            }
        },

        afterRender: function() { 
            console.log("rendering page_header");
            $( ".img-user" ).click(function(event) {
                // Stops the event from traveling up the hierarchy div-> container-> html.
                event.stopPropagation();
                $( ".user-dropdown" ).toggle();
            });
            
            // Hide dropdown if clicked anywhere outside the dropdown.
            $( "html" ).click(function() {
                $( ".user-dropdown" ).hide();
            });
            
            //keep the online-offline indicator up-to-date
            window.addEventListener("offline", this.user_offline);
            //keep the online-offline indicator up-to-date
            window.addEventListener("online", this.user_online);

            //set the online-offline indicator
            if (User.isOnline()) {
                this.user_online();
            } else {
                this.user_offline();
            }
        },
        
        //enable sync button, show online indicator
        user_online: function() {
            $('#sync')
                .removeAttr("disabled");
            $('#offline')
                .hide();
            $('#online')
                .show();
        },

        //disable sync button, show offline indicator
        user_offline: function() {
            $('#sync')
                .attr('disabled', true);
            $('#online')
                .hide();
            $('#offline')
                .show();
        },
        
        // logout and navigate to login url
        logout: function() {
            Auth.logout()
                .always(function() {
                window.location.href = window.location.origin + window.location.pathname;
            });
        },

        //this function is called when user clicks on language change options
        language: function(e) {
            e.preventDefault();
            var language_chosen = $(e.currentTarget).text();
            var language_current = User.get("language");
            if(language_chosen!=language_current){
                User.save({"language":language_chosen});
            }
        }
    });
    // Our module now returns our view
    return HeaderView;
});

/*! DataTables 1.10.2
 * ©2008-2014 SpryMedia Ltd - datatables.net/license
 */
(function(za,O,l){var N=function(h){function T(a){var b,c,d={};h.each(a,function(e){if((b=e.match(/^([^A-Z]+?)([A-Z])/))&&-1!=="a aa ai ao as b fn i m o s ".indexOf(b[1]+" "))c=e.replace(b[0],b[2].toLowerCase()),d[c]=e,"o"===b[1]&&T(a[e])});a._hungarianMap=d}function G(a,b,c){a._hungarianMap||T(a);var d;h.each(b,function(e){d=a._hungarianMap[e];if(d!==l&&(c||b[d]===l))"o"===d.charAt(0)?(b[d]||(b[d]={}),h.extend(!0,b[d],b[e]),G(a[d],b[d],c)):b[d]=b[e]})}function N(a){var b=p.defaults.oLanguage,c=a.sZeroRecords;
!a.sEmptyTable&&(c&&"No data available in table"===b.sEmptyTable)&&D(a,a,"sZeroRecords","sEmptyTable");!a.sLoadingRecords&&(c&&"Loading..."===b.sLoadingRecords)&&D(a,a,"sZeroRecords","sLoadingRecords");a.sInfoThousands&&(a.sThousands=a.sInfoThousands);(a=a.sDecimal)&&cb(a)}function db(a){w(a,"ordering","bSort");w(a,"orderMulti","bSortMulti");w(a,"orderClasses","bSortClasses");w(a,"orderCellsTop","bSortCellsTop");w(a,"order","aaSorting");w(a,"orderFixed","aaSortingFixed");w(a,"paging","bPaginate");
w(a,"pagingType","sPaginationType");w(a,"pageLength","iDisplayLength");w(a,"searching","bFilter");if(a=a.aoSearchCols)for(var b=0,c=a.length;b<c;b++)a[b]&&G(p.models.oSearch,a[b])}function eb(a){w(a,"orderable","bSortable");w(a,"orderData","aDataSort");w(a,"orderSequence","asSorting");w(a,"orderDataType","sortDataType")}function fb(a){var a=a.oBrowser,b=h("<div/>").css({position:"absolute",top:0,left:0,height:1,width:1,overflow:"hidden"}).append(h("<div/>").css({position:"absolute",top:1,left:1,width:100,
overflow:"scroll"}).append(h('<div class="test"/>').css({width:"100%",height:10}))).appendTo("body"),c=b.find(".test");a.bScrollOversize=100===c[0].offsetWidth;a.bScrollbarLeft=1!==c.offset().left;b.remove()}function gb(a,b,c,d,e,f){var g,j=!1;c!==l&&(g=c,j=!0);for(;d!==e;)a.hasOwnProperty(d)&&(g=j?b(g,a[d],d,a):a[d],j=!0,d+=f);return g}function Aa(a,b){var c=p.defaults.column,d=a.aoColumns.length,c=h.extend({},p.models.oColumn,c,{nTh:b?b:O.createElement("th"),sTitle:c.sTitle?c.sTitle:b?b.innerHTML:
"",aDataSort:c.aDataSort?c.aDataSort:[d],mData:c.mData?c.mData:d,idx:d});a.aoColumns.push(c);c=a.aoPreSearchCols;c[d]=h.extend({},p.models.oSearch,c[d]);fa(a,d,null)}function fa(a,b,c){var b=a.aoColumns[b],d=a.oClasses,e=h(b.nTh);if(!b.sWidthOrig){b.sWidthOrig=e.attr("width")||null;var f=(e.attr("style")||"").match(/width:\s*(\d+[pxem%]+)/);f&&(b.sWidthOrig=f[1])}c!==l&&null!==c&&(eb(c),G(p.defaults.column,c),c.mDataProp!==l&&!c.mData&&(c.mData=c.mDataProp),c.sType&&(b._sManualType=c.sType),c.className&&
!c.sClass&&(c.sClass=c.className),h.extend(b,c),D(b,c,"sWidth","sWidthOrig"),"number"===typeof c.iDataSort&&(b.aDataSort=[c.iDataSort]),D(b,c,"aDataSort"));var g=b.mData,j=U(g),i=b.mRender?U(b.mRender):null,c=function(a){return"string"===typeof a&&-1!==a.indexOf("@")};b._bAttrSrc=h.isPlainObject(g)&&(c(g.sort)||c(g.type)||c(g.filter));b.fnGetData=function(a,b,c){var d=j(a,b,l,c);return i&&b?i(d,b,a,c):d};b.fnSetData=function(a,b,c){return Ba(g)(a,b,c)};a.oFeatures.bSort||(b.bSortable=!1,e.addClass(d.sSortableNone));
a=-1!==h.inArray("asc",b.asSorting);c=-1!==h.inArray("desc",b.asSorting);!b.bSortable||!a&&!c?(b.sSortingClass=d.sSortableNone,b.sSortingClassJUI=""):a&&!c?(b.sSortingClass=d.sSortableAsc,b.sSortingClassJUI=d.sSortJUIAscAllowed):!a&&c?(b.sSortingClass=d.sSortableDesc,b.sSortingClassJUI=d.sSortJUIDescAllowed):(b.sSortingClass=d.sSortable,b.sSortingClassJUI=d.sSortJUI)}function V(a){if(!1!==a.oFeatures.bAutoWidth){var b=a.aoColumns;Ca(a);for(var c=0,d=b.length;c<d;c++)b[c].nTh.style.width=b[c].sWidth}b=
a.oScroll;(""!==b.sY||""!==b.sX)&&W(a);u(a,null,"column-sizing",[a])}function ga(a,b){var c=X(a,"bVisible");return"number"===typeof c[b]?c[b]:null}function Y(a,b){var c=X(a,"bVisible"),c=h.inArray(b,c);return-1!==c?c:null}function Z(a){return X(a,"bVisible").length}function X(a,b){var c=[];h.map(a.aoColumns,function(a,e){a[b]&&c.push(e)});return c}function Da(a){var b=a.aoColumns,c=a.aoData,d=p.ext.type.detect,e,f,g,j,i,h,m,o,k;e=0;for(f=b.length;e<f;e++)if(m=b[e],k=[],!m.sType&&m._sManualType)m.sType=
m._sManualType;else if(!m.sType){g=0;for(j=d.length;g<j;g++){i=0;for(h=c.length;i<h&&!(k[i]===l&&(k[i]=A(a,i,e,"type")),o=d[g](k[i],a),!o||"html"===o);i++);if(o){m.sType=o;break}}m.sType||(m.sType="string")}}function hb(a,b,c,d){var e,f,g,j,i,n,m=a.aoColumns;if(b)for(e=b.length-1;0<=e;e--){n=b[e];var o=n.targets!==l?n.targets:n.aTargets;h.isArray(o)||(o=[o]);f=0;for(g=o.length;f<g;f++)if("number"===typeof o[f]&&0<=o[f]){for(;m.length<=o[f];)Aa(a);d(o[f],n)}else if("number"===typeof o[f]&&0>o[f])d(m.length+
o[f],n);else if("string"===typeof o[f]){j=0;for(i=m.length;j<i;j++)("_all"==o[f]||h(m[j].nTh).hasClass(o[f]))&&d(j,n)}}if(c){e=0;for(a=c.length;e<a;e++)d(e,c[e])}}function I(a,b,c,d){var e=a.aoData.length,f=h.extend(!0,{},p.models.oRow,{src:c?"dom":"data"});f._aData=b;a.aoData.push(f);for(var b=a.aoColumns,f=0,g=b.length;f<g;f++)c&&Ea(a,e,f,A(a,e,f)),b[f].sType=null;a.aiDisplayMaster.push(e);(c||!a.oFeatures.bDeferRender)&&Fa(a,e,c,d);return e}function ha(a,b){var c;b instanceof h||(b=h(b));return b.map(function(b,
e){c=ia(a,e);return I(a,c.data,e,c.cells)})}function A(a,b,c,d){var e=a.iDraw,f=a.aoColumns[c],g=a.aoData[b]._aData,j=f.sDefaultContent,c=f.fnGetData(g,d,{settings:a,row:b,col:c});if(c===l)return a.iDrawError!=e&&null===j&&(P(a,0,"Requested unknown parameter "+("function"==typeof f.mData?"{function}":"'"+f.mData+"'")+" for row "+b,4),a.iDrawError=e),j;if((c===g||null===c)&&null!==j)c=j;else if("function"===typeof c)return c.call(g);return null===c&&"display"==d?"":c}function Ea(a,b,c,d){a.aoColumns[c].fnSetData(a.aoData[b]._aData,
d,{settings:a,row:b,col:c})}function Ga(a){return h.map(a.match(/(\\.|[^\.])+/g),function(a){return a.replace(/\\./g,".")})}function U(a){if(h.isPlainObject(a)){var b={};h.each(a,function(a,c){c&&(b[a]=U(c))});return function(a,c,f,g){var j=b[c]||b._;return j!==l?j(a,c,f,g):a}}if(null===a)return function(a){return a};if("function"===typeof a)return function(b,c,f,g){return a(b,c,f,g)};if("string"===typeof a&&(-1!==a.indexOf(".")||-1!==a.indexOf("[")||-1!==a.indexOf("("))){var c=function(a,b,f){var g,
j;if(""!==f){j=Ga(f);for(var i=0,h=j.length;i<h;i++){f=j[i].match($);g=j[i].match(Q);if(f){j[i]=j[i].replace($,"");""!==j[i]&&(a=a[j[i]]);g=[];j.splice(0,i+1);j=j.join(".");i=0;for(h=a.length;i<h;i++)g.push(c(a[i],b,j));a=f[0].substring(1,f[0].length-1);a=""===a?g:g.join(a);break}else if(g){j[i]=j[i].replace(Q,"");a=a[j[i]]();continue}if(null===a||a[j[i]]===l)return l;a=a[j[i]]}}return a};return function(b,e){return c(b,e,a)}}return function(b){return b[a]}}function Ba(a){if(h.isPlainObject(a))return Ba(a._);
if(null===a)return function(){};if("function"===typeof a)return function(b,d,e){a(b,"set",d,e)};if("string"===typeof a&&(-1!==a.indexOf(".")||-1!==a.indexOf("[")||-1!==a.indexOf("("))){var b=function(a,d,e){var e=Ga(e),f;f=e[e.length-1];for(var g,j,i=0,h=e.length-1;i<h;i++){g=e[i].match($);j=e[i].match(Q);if(g){e[i]=e[i].replace($,"");a[e[i]]=[];f=e.slice();f.splice(0,i+1);g=f.join(".");j=0;for(h=d.length;j<h;j++)f={},b(f,d[j],g),a[e[i]].push(f);return}j&&(e[i]=e[i].replace(Q,""),a=a[e[i]](d));if(null===
a[e[i]]||a[e[i]]===l)a[e[i]]={};a=a[e[i]]}if(f.match(Q))a[f.replace(Q,"")](d);else a[f.replace($,"")]=d};return function(c,d){return b(c,d,a)}}return function(b,d){b[a]=d}}function Ha(a){return C(a.aoData,"_aData")}function ja(a){a.aoData.length=0;a.aiDisplayMaster.length=0;a.aiDisplay.length=0}function ka(a,b,c){for(var d=-1,e=0,f=a.length;e<f;e++)a[e]==b?d=e:a[e]>b&&a[e]--; -1!=d&&c===l&&a.splice(d,1)}function la(a,b,c,d){var e=a.aoData[b],f;if("dom"===c||(!c||"auto"===c)&&"dom"===e.src)e._aData=
ia(a,e).data;else{var g=e.anCells,j;if(g){c=0;for(f=g.length;c<f;c++){for(j=g[c];j.childNodes.length;)j.removeChild(j.firstChild);g[c].innerHTML=A(a,b,c,"display")}}}e._aSortData=null;e._aFilterData=null;a=a.aoColumns;if(d!==l)a[d].sType=null;else{c=0;for(f=a.length;c<f;c++)a[c].sType=null}Ia(e)}function ia(a,b){var c=[],d=[],e=b.firstChild,f,g,j,i=0,n,m=a.aoColumns,o=function(a,b,c){"string"===typeof a&&(b=a.indexOf("@"),-1!==b&&(a=a.substring(b+1),j["@"+a]=c.getAttribute(a)))},k=function(a){g=m[i];
n=h.trim(a.innerHTML);g&&g._bAttrSrc?(j={display:n},o(g.mData.sort,j,a),o(g.mData.type,j,a),o(g.mData.filter,j,a),c.push(j)):c.push(n);i++};if(e)for(;e;){f=e.nodeName.toUpperCase();if("TD"==f||"TH"==f)k(e),d.push(e);e=e.nextSibling}else{d=b.anCells;e=0;for(f=d.length;e<f;e++)k(d[e])}return{data:c,cells:d}}function Fa(a,b,c,d){var e=a.aoData[b],f=e._aData,g=[],j,i,h,m,o;if(null===e.nTr){j=c||O.createElement("tr");e.nTr=j;e.anCells=g;j._DT_RowIndex=b;Ia(e);m=0;for(o=a.aoColumns.length;m<o;m++){h=a.aoColumns[m];
i=c?d[m]:O.createElement(h.sCellType);g.push(i);if(!c||h.mRender||h.mData!==m)i.innerHTML=A(a,b,m,"display");h.sClass&&(i.className+=" "+h.sClass);h.bVisible&&!c?j.appendChild(i):!h.bVisible&&c&&i.parentNode.removeChild(i);h.fnCreatedCell&&h.fnCreatedCell.call(a.oInstance,i,A(a,b,m),f,b,m)}u(a,"aoRowCreatedCallback",null,[j,f,b])}e.nTr.setAttribute("role","row")}function Ia(a){var b=a.nTr,c=a._aData;if(b){c.DT_RowId&&(b.id=c.DT_RowId);if(c.DT_RowClass){var d=c.DT_RowClass.split(" ");a.__rowc=a.__rowc?
Ja(a.__rowc.concat(d)):d;h(b).removeClass(a.__rowc.join(" ")).addClass(c.DT_RowClass)}c.DT_RowData&&h(b).data(c.DT_RowData)}}function ib(a){var b,c,d,e,f,g=a.nTHead,j=a.nTFoot,i=0===h("th, td",g).length,n=a.oClasses,m=a.aoColumns;i&&(e=h("<tr/>").appendTo(g));b=0;for(c=m.length;b<c;b++)f=m[b],d=h(f.nTh).addClass(f.sClass),i&&d.appendTo(e),a.oFeatures.bSort&&(d.addClass(f.sSortingClass),!1!==f.bSortable&&(d.attr("tabindex",a.iTabIndex).attr("aria-controls",a.sTableId),Ka(a,f.nTh,b))),f.sTitle!=d.html()&&
d.html(f.sTitle),La(a,"header")(a,d,f,n);i&&aa(a.aoHeader,g);h(g).find(">tr").attr("role","row");h(g).find(">tr>th, >tr>td").addClass(n.sHeaderTH);h(j).find(">tr>th, >tr>td").addClass(n.sFooterTH);if(null!==j){a=a.aoFooter[0];b=0;for(c=a.length;b<c;b++)f=m[b],f.nTf=a[b].cell,f.sClass&&h(f.nTf).addClass(f.sClass)}}function ba(a,b,c){var d,e,f,g=[],j=[],i=a.aoColumns.length,n;if(b){c===l&&(c=!1);d=0;for(e=b.length;d<e;d++){g[d]=b[d].slice();g[d].nTr=b[d].nTr;for(f=i-1;0<=f;f--)!a.aoColumns[f].bVisible&&
!c&&g[d].splice(f,1);j.push([])}d=0;for(e=g.length;d<e;d++){if(a=g[d].nTr)for(;f=a.firstChild;)a.removeChild(f);f=0;for(b=g[d].length;f<b;f++)if(n=i=1,j[d][f]===l){a.appendChild(g[d][f].cell);for(j[d][f]=1;g[d+i]!==l&&g[d][f].cell==g[d+i][f].cell;)j[d+i][f]=1,i++;for(;g[d][f+n]!==l&&g[d][f].cell==g[d][f+n].cell;){for(c=0;c<i;c++)j[d+c][f+n]=1;n++}h(g[d][f].cell).attr("rowspan",i).attr("colspan",n)}}}}function K(a){var b=u(a,"aoPreDrawCallback","preDraw",[a]);if(-1!==h.inArray(!1,b))B(a,!1);else{var b=
[],c=0,d=a.asStripeClasses,e=d.length,f=a.oLanguage,g=a.iInitDisplayStart,j="ssp"==z(a),i=a.aiDisplay;a.bDrawing=!0;g!==l&&-1!==g&&(a._iDisplayStart=j?g:g>=a.fnRecordsDisplay()?0:g,a.iInitDisplayStart=-1);var g=a._iDisplayStart,n=a.fnDisplayEnd();if(a.bDeferLoading)a.bDeferLoading=!1,a.iDraw++,B(a,!1);else if(j){if(!a.bDestroying&&!jb(a))return}else a.iDraw++;if(0!==i.length){f=j?a.aoData.length:n;for(j=j?0:g;j<f;j++){var m=i[j],o=a.aoData[m];null===o.nTr&&Fa(a,m);m=o.nTr;if(0!==e){var k=d[c%e];o._sRowStripe!=
k&&(h(m).removeClass(o._sRowStripe).addClass(k),o._sRowStripe=k)}u(a,"aoRowCallback",null,[m,o._aData,c,j]);b.push(m);c++}}else c=f.sZeroRecords,1==a.iDraw&&"ajax"==z(a)?c=f.sLoadingRecords:f.sEmptyTable&&0===a.fnRecordsTotal()&&(c=f.sEmptyTable),b[0]=h("<tr/>",{"class":e?d[0]:""}).append(h("<td />",{valign:"top",colSpan:Z(a),"class":a.oClasses.sRowEmpty}).html(c))[0];u(a,"aoHeaderCallback","header",[h(a.nTHead).children("tr")[0],Ha(a),g,n,i]);u(a,"aoFooterCallback","footer",[h(a.nTFoot).children("tr")[0],
Ha(a),g,n,i]);d=h(a.nTBody);d.children().detach();d.append(h(b));u(a,"aoDrawCallback","draw",[a]);a.bSorted=!1;a.bFiltered=!1;a.bDrawing=!1}}function L(a,b){var c=a.oFeatures,d=c.bFilter;c.bSort&&kb(a);d?ca(a,a.oPreviousSearch):a.aiDisplay=a.aiDisplayMaster.slice();!0!==b&&(a._iDisplayStart=0);a._drawHold=b;K(a);a._drawHold=!1}function lb(a){var b=a.oClasses,c=h(a.nTable),c=h("<div/>").insertBefore(c),d=a.oFeatures,e=h("<div/>",{id:a.sTableId+"_wrapper","class":b.sWrapper+(a.nTFoot?"":" "+b.sNoFooter)});
a.nHolding=c[0];a.nTableWrapper=e[0];a.nTableReinsertBefore=a.nTable.nextSibling;for(var f=a.sDom.split(""),g,j,i,n,m,o,k=0;k<f.length;k++){g=null;j=f[k];if("<"==j){i=h("<div/>")[0];n=f[k+1];if("'"==n||'"'==n){m="";for(o=2;f[k+o]!=n;)m+=f[k+o],o++;"H"==m?m=b.sJUIHeader:"F"==m&&(m=b.sJUIFooter);-1!=m.indexOf(".")?(n=m.split("."),i.id=n[0].substr(1,n[0].length-1),i.className=n[1]):"#"==m.charAt(0)?i.id=m.substr(1,m.length-1):i.className=m;k+=o}e.append(i);e=h(i)}else if(">"==j)e=e.parent();else if("l"==
j&&d.bPaginate&&d.bLengthChange)g=mb(a);else if("f"==j&&d.bFilter)g=nb(a);else if("r"==j&&d.bProcessing)g=ob(a);else if("t"==j)g=pb(a);else if("i"==j&&d.bInfo)g=qb(a);else if("p"==j&&d.bPaginate)g=rb(a);else if(0!==p.ext.feature.length){i=p.ext.feature;o=0;for(n=i.length;o<n;o++)if(j==i[o].cFeature){g=i[o].fnInit(a);break}}g&&(i=a.aanFeatures,i[j]||(i[j]=[]),i[j].push(g),e.append(g))}c.replaceWith(e)}function aa(a,b){var c=h(b).children("tr"),d,e,f,g,j,i,n,m,o,k;a.splice(0,a.length);f=0;for(i=c.length;f<
i;f++)a.push([]);f=0;for(i=c.length;f<i;f++){d=c[f];for(e=d.firstChild;e;){if("TD"==e.nodeName.toUpperCase()||"TH"==e.nodeName.toUpperCase()){m=1*e.getAttribute("colspan");o=1*e.getAttribute("rowspan");m=!m||0===m||1===m?1:m;o=!o||0===o||1===o?1:o;g=0;for(j=a[f];j[g];)g++;n=g;k=1===m?!0:!1;for(j=0;j<m;j++)for(g=0;g<o;g++)a[f+g][n+j]={cell:e,unique:k},a[f+g].nTr=d}e=e.nextSibling}}}function ma(a,b,c){var d=[];c||(c=a.aoHeader,b&&(c=[],aa(c,b)));for(var b=0,e=c.length;b<e;b++)for(var f=0,g=c[b].length;f<
g;f++)if(c[b][f].unique&&(!d[f]||!a.bSortCellsTop))d[f]=c[b][f].cell;return d}function na(a,b,c){u(a,"aoServerParams","serverParams",[b]);if(b&&h.isArray(b)){var d={},e=/(.*?)\[\]$/;h.each(b,function(a,b){var c=b.name.match(e);c?(c=c[0],d[c]||(d[c]=[]),d[c].push(b.value)):d[b.name]=b.value});b=d}var f,g=a.ajax,j=a.oInstance;if(h.isPlainObject(g)&&g.data){f=g.data;var i=h.isFunction(f)?f(b):f,b=h.isFunction(f)&&i?i:h.extend(!0,b,i);delete g.data}i={data:b,success:function(b){var d=b.error||b.sError;
d&&a.oApi._fnLog(a,0,d);a.json=b;u(a,null,"xhr",[a,b]);c(b)},dataType:"json",cache:!1,type:a.sServerMethod,error:function(b,c){var d=a.oApi._fnLog;"parsererror"==c?d(a,0,"Invalid JSON response",1):4===b.readyState&&d(a,0,"Ajax error",7);B(a,!1)}};a.oAjaxData=b;u(a,null,"preXhr",[a,b]);a.fnServerData?a.fnServerData.call(j,a.sAjaxSource,h.map(b,function(a,b){return{name:b,value:a}}),c,a):a.sAjaxSource||"string"===typeof g?a.jqXHR=h.ajax(h.extend(i,{url:g||a.sAjaxSource})):h.isFunction(g)?a.jqXHR=g.call(j,
b,c,a):(a.jqXHR=h.ajax(h.extend(i,g)),g.data=f)}function jb(a){return a.bAjaxDataGet?(a.iDraw++,B(a,!0),na(a,sb(a),function(b){tb(a,b)}),!1):!0}function sb(a){var b=a.aoColumns,c=b.length,d=a.oFeatures,e=a.oPreviousSearch,f=a.aoPreSearchCols,g,j=[],i,n,m,o=R(a);g=a._iDisplayStart;i=!1!==d.bPaginate?a._iDisplayLength:-1;var k=function(a,b){j.push({name:a,value:b})};k("sEcho",a.iDraw);k("iColumns",c);k("sColumns",C(b,"sName").join(","));k("iDisplayStart",g);k("iDisplayLength",i);var l={draw:a.iDraw,
columns:[],order:[],start:g,length:i,search:{value:e.sSearch,regex:e.bRegex}};for(g=0;g<c;g++)n=b[g],m=f[g],i="function"==typeof n.mData?"function":n.mData,l.columns.push({data:i,name:n.sName,searchable:n.bSearchable,orderable:n.bSortable,search:{value:m.sSearch,regex:m.bRegex}}),k("mDataProp_"+g,i),d.bFilter&&(k("sSearch_"+g,m.sSearch),k("bRegex_"+g,m.bRegex),k("bSearchable_"+g,n.bSearchable)),d.bSort&&k("bSortable_"+g,n.bSortable);d.bFilter&&(k("sSearch",e.sSearch),k("bRegex",e.bRegex));d.bSort&&
(h.each(o,function(a,b){l.order.push({column:b.col,dir:b.dir});k("iSortCol_"+a,b.col);k("sSortDir_"+a,b.dir)}),k("iSortingCols",o.length));b=p.ext.legacy.ajax;return null===b?a.sAjaxSource?j:l:b?j:l}function tb(a,b){var c=b.sEcho!==l?b.sEcho:b.draw,d=b.iTotalRecords!==l?b.iTotalRecords:b.recordsTotal,e=b.iTotalDisplayRecords!==l?b.iTotalDisplayRecords:b.recordsFiltered;if(c){if(1*c<a.iDraw)return;a.iDraw=1*c}ja(a);a._iRecordsTotal=parseInt(d,10);a._iRecordsDisplay=parseInt(e,10);c=oa(a,b);d=0;for(e=
c.length;d<e;d++)I(a,c[d]);a.aiDisplay=a.aiDisplayMaster.slice();a.bAjaxDataGet=!1;K(a);a._bInitComplete||pa(a,b);a.bAjaxDataGet=!0;B(a,!1)}function oa(a,b){var c=h.isPlainObject(a.ajax)&&a.ajax.dataSrc!==l?a.ajax.dataSrc:a.sAjaxDataProp;return"data"===c?b.aaData||b[c]:""!==c?U(c)(b):b}function nb(a){var b=a.oClasses,c=a.sTableId,d=a.oLanguage,e=a.oPreviousSearch,f=a.aanFeatures,g='<input type="search" class="'+b.sFilterInput+'"/>',j=d.sSearch,j=j.match(/_INPUT_/)?j.replace("_INPUT_",g):j+g,b=h("<div/>",
{id:!f.f?c+"_filter":null,"class":b.sFilter}).append(h("<label/>").append(j)),f=function(){var b=!this.value?"":this.value;b!=e.sSearch&&(ca(a,{sSearch:b,bRegex:e.bRegex,bSmart:e.bSmart,bCaseInsensitive:e.bCaseInsensitive}),a._iDisplayStart=0,K(a))},i=h("input",b).val(e.sSearch).attr("placeholder",d.sSearchPlaceholder).bind("keyup.DT search.DT input.DT paste.DT cut.DT","ssp"===z(a)?Ma(f,400):f).bind("keypress.DT",function(a){if(13==a.keyCode)return!1}).attr("aria-controls",c);h(a.nTable).on("search.dt.DT",
function(b,c){if(a===c)try{i[0]!==O.activeElement&&i.val(e.sSearch)}catch(d){}});return b[0]}function ca(a,b,c){var d=a.oPreviousSearch,e=a.aoPreSearchCols,f=function(a){d.sSearch=a.sSearch;d.bRegex=a.bRegex;d.bSmart=a.bSmart;d.bCaseInsensitive=a.bCaseInsensitive};Da(a);if("ssp"!=z(a)){ub(a,b.sSearch,c,b.bEscapeRegex!==l?!b.bEscapeRegex:b.bRegex,b.bSmart,b.bCaseInsensitive);f(b);for(b=0;b<e.length;b++)vb(a,e[b].sSearch,b,e[b].bEscapeRegex!==l?!e[b].bEscapeRegex:e[b].bRegex,e[b].bSmart,e[b].bCaseInsensitive);
wb(a)}else f(b);a.bFiltered=!0;u(a,null,"search",[a])}function wb(a){for(var b=p.ext.search,c=a.aiDisplay,d,e,f=0,g=b.length;f<g;f++){for(var j=[],i=0,h=c.length;i<h;i++)e=c[i],d=a.aoData[e],b[f](a,d._aFilterData,e,d._aData,i)&&j.push(e);c.length=0;c.push.apply(c,j)}}function vb(a,b,c,d,e,f){if(""!==b)for(var g=a.aiDisplay,d=Na(b,d,e,f),e=g.length-1;0<=e;e--)b=a.aoData[g[e]]._aFilterData[c],d.test(b)||g.splice(e,1)}function ub(a,b,c,d,e,f){var d=Na(b,d,e,f),e=a.oPreviousSearch.sSearch,f=a.aiDisplayMaster,
g;0!==p.ext.search.length&&(c=!0);g=xb(a);if(0>=b.length)a.aiDisplay=f.slice();else{if(g||c||e.length>b.length||0!==b.indexOf(e)||a.bSorted)a.aiDisplay=f.slice();b=a.aiDisplay;for(c=b.length-1;0<=c;c--)d.test(a.aoData[b[c]]._sFilterRow)||b.splice(c,1)}}function Na(a,b,c,d){a=b?a:Oa(a);c&&(a="^(?=.*?"+h.map(a.match(/"[^"]+"|[^ ]+/g)||"",function(a){return'"'===a.charAt(0)?a.match(/^"(.*)"$/)[1]:a}).join(")(?=.*?")+").*$");return RegExp(a,d?"i":"")}function Oa(a){return a.replace(Vb,"\\$1")}function xb(a){var b=
a.aoColumns,c,d,e,f,g,j,i,h,m=p.ext.type.search;c=!1;d=0;for(f=a.aoData.length;d<f;d++)if(h=a.aoData[d],!h._aFilterData){j=[];e=0;for(g=b.length;e<g;e++)c=b[e],c.bSearchable?(i=A(a,d,e,"filter"),m[c.sType]&&(i=m[c.sType](i)),null===i&&(i=""),"string"!==typeof i&&i.toString&&(i=i.toString())):i="",i.indexOf&&-1!==i.indexOf("&")&&(qa.innerHTML=i,i=Wb?qa.textContent:qa.innerText),i.replace&&(i=i.replace(/[\r\n]/g,"")),j.push(i);h._aFilterData=j;h._sFilterRow=j.join("  ");c=!0}return c}function yb(a){return{search:a.sSearch,
smart:a.bSmart,regex:a.bRegex,caseInsensitive:a.bCaseInsensitive}}function zb(a){return{sSearch:a.search,bSmart:a.smart,bRegex:a.regex,bCaseInsensitive:a.caseInsensitive}}function qb(a){var b=a.sTableId,c=a.aanFeatures.i,d=h("<div/>",{"class":a.oClasses.sInfo,id:!c?b+"_info":null});c||(a.aoDrawCallback.push({fn:Ab,sName:"information"}),d.attr("role","status").attr("aria-live","polite"),h(a.nTable).attr("aria-describedby",b+"_info"));return d[0]}function Ab(a){var b=a.aanFeatures.i;if(0!==b.length){var c=
a.oLanguage,d=a._iDisplayStart+1,e=a.fnDisplayEnd(),f=a.fnRecordsTotal(),g=a.fnRecordsDisplay(),j=g?c.sInfo:c.sInfoEmpty;g!==f&&(j+=" "+c.sInfoFiltered);j+=c.sInfoPostFix;j=Bb(a,j);c=c.fnInfoCallback;null!==c&&(j=c.call(a.oInstance,a,d,e,f,g,j));h(b).html(j)}}function Bb(a,b){var c=a.fnFormatNumber,d=a._iDisplayStart+1,e=a._iDisplayLength,f=a.fnRecordsDisplay(),g=-1===e;return b.replace(/_START_/g,c.call(a,d)).replace(/_END_/g,c.call(a,a.fnDisplayEnd())).replace(/_MAX_/g,c.call(a,a.fnRecordsTotal())).replace(/_TOTAL_/g,
c.call(a,f)).replace(/_PAGE_/g,c.call(a,g?1:Math.ceil(d/e))).replace(/_PAGES_/g,c.call(a,g?1:Math.ceil(f/e)))}function ra(a){var b,c,d=a.iInitDisplayStart,e=a.aoColumns,f;c=a.oFeatures;if(a.bInitialised){lb(a);ib(a);ba(a,a.aoHeader);ba(a,a.aoFooter);B(a,!0);c.bAutoWidth&&Ca(a);b=0;for(c=e.length;b<c;b++)f=e[b],f.sWidth&&(f.nTh.style.width=s(f.sWidth));L(a);e=z(a);"ssp"!=e&&("ajax"==e?na(a,[],function(c){var f=oa(a,c);for(b=0;b<f.length;b++)I(a,f[b]);a.iInitDisplayStart=d;L(a);B(a,!1);pa(a,c)},a):
(B(a,!1),pa(a)))}else setTimeout(function(){ra(a)},200)}function pa(a,b){a._bInitComplete=!0;b&&V(a);u(a,"aoInitComplete","init",[a,b])}function Pa(a,b){var c=parseInt(b,10);a._iDisplayLength=c;Qa(a);u(a,null,"length",[a,c])}function mb(a){for(var b=a.oClasses,c=a.sTableId,d=a.aLengthMenu,e=h.isArray(d[0]),f=e?d[0]:d,d=e?d[1]:d,e=h("<select/>",{name:c+"_length","aria-controls":c,"class":b.sLengthSelect}),g=0,j=f.length;g<j;g++)e[0][g]=new Option(d[g],f[g]);var i=h("<div><label/></div>").addClass(b.sLength);
a.aanFeatures.l||(i[0].id=c+"_length");i.children().append(a.oLanguage.sLengthMenu.replace("_MENU_",e[0].outerHTML));h("select",i).val(a._iDisplayLength).bind("change.DT",function(){Pa(a,h(this).val());K(a)});h(a.nTable).bind("length.dt.DT",function(b,c,d){a===c&&h("select",i).val(d)});return i[0]}function rb(a){var b=a.sPaginationType,c=p.ext.pager[b],d="function"===typeof c,e=function(a){K(a)},b=h("<div/>").addClass(a.oClasses.sPaging+b)[0],f=a.aanFeatures;d||c.fnInit(a,b,e);f.p||(b.id=a.sTableId+
"_paginate",a.aoDrawCallback.push({fn:function(a){if(d){var b=a._iDisplayStart,i=a._iDisplayLength,h=a.fnRecordsDisplay(),m=-1===i,b=m?0:Math.ceil(b/i),i=m?1:Math.ceil(h/i),h=c(b,i),o,m=0;for(o=f.p.length;m<o;m++)La(a,"pageButton")(a,f.p[m],m,h,b,i)}else c.fnUpdate(a,e)},sName:"pagination"}));return b}function Ra(a,b,c){var d=a._iDisplayStart,e=a._iDisplayLength,f=a.fnRecordsDisplay();0===f||-1===e?d=0:"number"===typeof b?(d=b*e,d>f&&(d=0)):"first"==b?d=0:"previous"==b?(d=0<=e?d-e:0,0>d&&(d=0)):"next"==
b?d+e<f&&(d+=e):"last"==b?d=Math.floor((f-1)/e)*e:P(a,0,"Unknown paging action: "+b,5);b=a._iDisplayStart!==d;a._iDisplayStart=d;b&&(u(a,null,"page",[a]),c&&K(a));return b}function ob(a){return h("<div/>",{id:!a.aanFeatures.r?a.sTableId+"_processing":null,"class":a.oClasses.sProcessing}).html(a.oLanguage.sProcessing).insertBefore(a.nTable)[0]}function B(a,b){a.oFeatures.bProcessing&&h(a.aanFeatures.r).css("display",b?"block":"none");u(a,null,"processing",[a,b])}function pb(a){var b=h(a.nTable);b.attr("role",
"grid");var c=a.oScroll;if(""===c.sX&&""===c.sY)return a.nTable;var d=c.sX,e=c.sY,f=a.oClasses,g=b.children("caption"),j=g.length?g[0]._captionSide:null,i=h(b[0].cloneNode(!1)),n=h(b[0].cloneNode(!1)),m=b.children("tfoot");c.sX&&"100%"===b.attr("width")&&b.removeAttr("width");m.length||(m=null);c=h("<div/>",{"class":f.sScrollWrapper}).append(h("<div/>",{"class":f.sScrollHead}).css({overflow:"hidden",position:"relative",border:0,width:d?!d?null:s(d):"100%"}).append(h("<div/>",{"class":f.sScrollHeadInner}).css({"box-sizing":"content-box",
width:c.sXInner||"100%"}).append(i.removeAttr("id").css("margin-left",0).append(b.children("thead")))).append("top"===j?g:null)).append(h("<div/>",{"class":f.sScrollBody}).css({overflow:"auto",height:!e?null:s(e),width:!d?null:s(d)}).append(b));m&&c.append(h("<div/>",{"class":f.sScrollFoot}).css({overflow:"hidden",border:0,width:d?!d?null:s(d):"100%"}).append(h("<div/>",{"class":f.sScrollFootInner}).append(n.removeAttr("id").css("margin-left",0).append(b.children("tfoot")))).append("bottom"===j?g:
null));var b=c.children(),o=b[0],f=b[1],k=m?b[2]:null;d&&h(f).scroll(function(){var a=this.scrollLeft;o.scrollLeft=a;m&&(k.scrollLeft=a)});a.nScrollHead=o;a.nScrollBody=f;a.nScrollFoot=k;a.aoDrawCallback.push({fn:W,sName:"scrolling"});return c[0]}function W(a){var b=a.oScroll,c=b.sX,d=b.sXInner,e=b.sY,f=b.iBarWidth,g=h(a.nScrollHead),j=g[0].style,i=g.children("div"),n=i[0].style,m=i.children("table"),i=a.nScrollBody,o=h(i),k=i.style,l=h(a.nScrollFoot).children("div"),p=l.children("table"),r=h(a.nTHead),
q=h(a.nTable),da=q[0],M=da.style,J=a.nTFoot?h(a.nTFoot):null,u=a.oBrowser,v=u.bScrollOversize,y,t,x,w,z,A=[],B=[],C=[],D,E=function(a){a=a.style;a.paddingTop="0";a.paddingBottom="0";a.borderTopWidth="0";a.borderBottomWidth="0";a.height=0};q.children("thead, tfoot").remove();z=r.clone().prependTo(q);y=r.find("tr");x=z.find("tr");z.find("th, td").removeAttr("tabindex");J&&(w=J.clone().prependTo(q),t=J.find("tr"),w=w.find("tr"));c||(k.width="100%",g[0].style.width="100%");h.each(ma(a,z),function(b,c){D=
ga(a,b);c.style.width=a.aoColumns[D].sWidth});J&&F(function(a){a.style.width=""},w);b.bCollapse&&""!==e&&(k.height=o[0].offsetHeight+r[0].offsetHeight+"px");g=q.outerWidth();if(""===c){if(M.width="100%",v&&(q.find("tbody").height()>i.offsetHeight||"scroll"==o.css("overflow-y")))M.width=s(q.outerWidth()-f)}else""!==d?M.width=s(d):g==o.width()&&o.height()<q.height()?(M.width=s(g-f),q.outerWidth()>g-f&&(M.width=s(g))):M.width=s(g);g=q.outerWidth();F(E,x);F(function(a){C.push(a.innerHTML);A.push(s(h(a).css("width")))},
x);F(function(a,b){a.style.width=A[b]},y);h(x).height(0);J&&(F(E,w),F(function(a){B.push(s(h(a).css("width")))},w),F(function(a,b){a.style.width=B[b]},t),h(w).height(0));F(function(a,b){a.innerHTML='<div class="dataTables_sizing" style="height:0;overflow:hidden;">'+C[b]+"</div>";a.style.width=A[b]},x);J&&F(function(a,b){a.innerHTML="";a.style.width=B[b]},w);if(q.outerWidth()<g){t=i.scrollHeight>i.offsetHeight||"scroll"==o.css("overflow-y")?g+f:g;if(v&&(i.scrollHeight>i.offsetHeight||"scroll"==o.css("overflow-y")))M.width=
s(t-f);(""===c||""!==d)&&P(a,1,"Possible column misalignment",6)}else t="100%";k.width=s(t);j.width=s(t);J&&(a.nScrollFoot.style.width=s(t));!e&&v&&(k.height=s(da.offsetHeight+f));e&&b.bCollapse&&(k.height=s(e),b=c&&da.offsetWidth>i.offsetWidth?f:0,da.offsetHeight<i.offsetHeight&&(k.height=s(da.offsetHeight+b)));b=q.outerWidth();m[0].style.width=s(b);n.width=s(b);m=q.height()>i.clientHeight||"scroll"==o.css("overflow-y");u="padding"+(u.bScrollbarLeft?"Left":"Right");n[u]=m?f+"px":"0px";J&&(p[0].style.width=
s(b),l[0].style.width=s(b),l[0].style[u]=m?f+"px":"0px");o.scroll();if((a.bSorted||a.bFiltered)&&!a._drawHold)i.scrollTop=0}function F(a,b,c){for(var d=0,e=0,f=b.length,g,j;e<f;){g=b[e].firstChild;for(j=c?c[e].firstChild:null;g;)1===g.nodeType&&(c?a(g,j,d):a(g,d),d++),g=g.nextSibling,j=c?j.nextSibling:null;e++}}function Ca(a){var b=a.nTable,c=a.aoColumns,d=a.oScroll,e=d.sY,f=d.sX,g=d.sXInner,j=c.length,d=X(a,"bVisible"),i=h("th",a.nTHead),n=b.getAttribute("width"),m=b.parentNode,o=!1,k,l;for(k=0;k<
d.length;k++)l=c[d[k]],null!==l.sWidth&&(l.sWidth=Cb(l.sWidthOrig,m),o=!0);if(!o&&!f&&!e&&j==Z(a)&&j==i.length)for(k=0;k<j;k++)c[k].sWidth=s(i.eq(k).width());else{j=h(b).clone().empty().css("visibility","hidden").removeAttr("id").append(h(a.nTHead).clone(!1)).append(h(a.nTFoot).clone(!1)).append(h("<tbody><tr/></tbody>"));j.find("tfoot th, tfoot td").css("width","");var p=j.find("tbody tr"),i=ma(a,j.find("thead")[0]);for(k=0;k<d.length;k++)l=c[d[k]],i[k].style.width=null!==l.sWidthOrig&&""!==l.sWidthOrig?
s(l.sWidthOrig):"";if(a.aoData.length)for(k=0;k<d.length;k++)o=d[k],l=c[o],h(Db(a,o)).clone(!1).append(l.sContentPadding).appendTo(p);j.appendTo(m);f&&g?j.width(g):f?(j.css("width","auto"),j.width()<m.offsetWidth&&j.width(m.offsetWidth)):e?j.width(m.offsetWidth):n&&j.width(n);Eb(a,j[0]);if(f){for(k=g=0;k<d.length;k++)l=c[d[k]],e=h(i[k]).outerWidth(),g+=null===l.sWidthOrig?e:parseInt(l.sWidth,10)+e-h(i[k]).width();j.width(s(g));b.style.width=s(g)}for(k=0;k<d.length;k++)if(l=c[d[k]],e=h(i[k]).width())l.sWidth=
s(e);b.style.width=s(j.css("width"));j.remove()}n&&(b.style.width=s(n));if((n||f)&&!a._reszEvt)h(za).bind("resize.DT-"+a.sInstance,Ma(function(){V(a)})),a._reszEvt=!0}function Ma(a,b){var c=b||200,d,e;return function(){var b=this,g=+new Date,j=arguments;d&&g<d+c?(clearTimeout(e),e=setTimeout(function(){d=l;a.apply(b,j)},c)):d?(d=g,a.apply(b,j)):d=g}}function Cb(a,b){if(!a)return 0;var c=h("<div/>").css("width",s(a)).appendTo(b||O.body),d=c[0].offsetWidth;c.remove();return d}function Eb(a,b){var c=
a.oScroll;if(c.sX||c.sY)c=!c.sX?c.iBarWidth:0,b.style.width=s(h(b).outerWidth()-c)}function Db(a,b){var c=Fb(a,b);if(0>c)return null;var d=a.aoData[c];return!d.nTr?h("<td/>").html(A(a,c,b,"display"))[0]:d.anCells[b]}function Fb(a,b){for(var c,d=-1,e=-1,f=0,g=a.aoData.length;f<g;f++)c=A(a,f,b,"display")+"",c=c.replace(Xb,""),c.length>d&&(d=c.length,e=f);return e}function s(a){return null===a?"0px":"number"==typeof a?0>a?"0px":a+"px":a.match(/\d$/)?a+"px":a}function Gb(){if(!p.__scrollbarWidth){var a=
h("<p/>").css({width:"100%",height:200,padding:0})[0],b=h("<div/>").css({position:"absolute",top:0,left:0,width:200,height:150,padding:0,overflow:"hidden",visibility:"hidden"}).append(a).appendTo("body"),c=a.offsetWidth;b.css("overflow","scroll");a=a.offsetWidth;c===a&&(a=b[0].clientWidth);b.remove();p.__scrollbarWidth=c-a}return p.__scrollbarWidth}function R(a){var b,c,d=[],e=a.aoColumns,f,g,j,i;b=a.aaSortingFixed;c=h.isPlainObject(b);var n=[];f=function(a){a.length&&!h.isArray(a[0])?n.push(a):n.push.apply(n,
a)};h.isArray(b)&&f(b);c&&b.pre&&f(b.pre);f(a.aaSorting);c&&b.post&&f(b.post);for(a=0;a<n.length;a++){i=n[a][0];f=e[i].aDataSort;b=0;for(c=f.length;b<c;b++)g=f[b],j=e[g].sType||"string",d.push({src:i,col:g,dir:n[a][1],index:n[a][2],type:j,formatter:p.ext.type.order[j+"-pre"]})}return d}function kb(a){var b,c,d=[],e=p.ext.type.order,f=a.aoData,g=0,j,i=a.aiDisplayMaster,h;Da(a);h=R(a);b=0;for(c=h.length;b<c;b++)j=h[b],j.formatter&&g++,Hb(a,j.col);if("ssp"!=z(a)&&0!==h.length){b=0;for(c=i.length;b<c;b++)d[i[b]]=
b;g===h.length?i.sort(function(a,b){var c,e,g,j,i=h.length,l=f[a]._aSortData,p=f[b]._aSortData;for(g=0;g<i;g++)if(j=h[g],c=l[j.col],e=p[j.col],c=c<e?-1:c>e?1:0,0!==c)return"asc"===j.dir?c:-c;c=d[a];e=d[b];return c<e?-1:c>e?1:0}):i.sort(function(a,b){var c,g,j,i,l=h.length,p=f[a]._aSortData,r=f[b]._aSortData;for(j=0;j<l;j++)if(i=h[j],c=p[i.col],g=r[i.col],i=e[i.type+"-"+i.dir]||e["string-"+i.dir],c=i(c,g),0!==c)return c;c=d[a];g=d[b];return c<g?-1:c>g?1:0})}a.bSorted=!0}function Ib(a){for(var b,c,
d=a.aoColumns,e=R(a),a=a.oLanguage.oAria,f=0,g=d.length;f<g;f++){c=d[f];var j=c.asSorting;b=c.sTitle.replace(/<.*?>/g,"");var i=c.nTh;i.removeAttribute("aria-sort");c.bSortable&&(0<e.length&&e[0].col==f?(i.setAttribute("aria-sort","asc"==e[0].dir?"ascending":"descending"),c=j[e[0].index+1]||j[0]):c=j[0],b+="asc"===c?a.sSortAscending:a.sSortDescending);i.setAttribute("aria-label",b)}}function Sa(a,b,c,d){var e=a.aaSorting,f=a.aoColumns[b].asSorting,g=function(a){var b=a._idx;b===l&&(b=h.inArray(a[1],
f));return b+1>=f.length?0:b+1};"number"===typeof e[0]&&(e=a.aaSorting=[e]);c&&a.oFeatures.bSortMulti?(c=h.inArray(b,C(e,"0")),-1!==c?(b=g(e[c]),e[c][1]=f[b],e[c]._idx=b):(e.push([b,f[0],0]),e[e.length-1]._idx=0)):e.length&&e[0][0]==b?(b=g(e[0]),e.length=1,e[0][1]=f[b],e[0]._idx=b):(e.length=0,e.push([b,f[0]]),e[0]._idx=0);L(a);"function"==typeof d&&d(a)}function Ka(a,b,c,d){var e=a.aoColumns[c];Ta(b,{},function(b){!1!==e.bSortable&&(a.oFeatures.bProcessing?(B(a,!0),setTimeout(function(){Sa(a,c,b.shiftKey,
d);"ssp"!==z(a)&&B(a,!1)},0)):Sa(a,c,b.shiftKey,d))})}function sa(a){var b=a.aLastSort,c=a.oClasses.sSortColumn,d=R(a),e=a.oFeatures,f,g;if(e.bSort&&e.bSortClasses){e=0;for(f=b.length;e<f;e++)g=b[e].src,h(C(a.aoData,"anCells",g)).removeClass(c+(2>e?e+1:3));e=0;for(f=d.length;e<f;e++)g=d[e].src,h(C(a.aoData,"anCells",g)).addClass(c+(2>e?e+1:3))}a.aLastSort=d}function Hb(a,b){var c=a.aoColumns[b],d=p.ext.order[c.sSortDataType],e;d&&(e=d.call(a.oInstance,a,b,Y(a,b)));for(var f,g=p.ext.type.order[c.sType+
"-pre"],j=0,i=a.aoData.length;j<i;j++)if(c=a.aoData[j],c._aSortData||(c._aSortData=[]),!c._aSortData[b]||d)f=d?e[j]:A(a,j,b,"sort"),c._aSortData[b]=g?g(f):f}function ta(a){if(a.oFeatures.bStateSave&&!a.bDestroying){var b={time:+new Date,start:a._iDisplayStart,length:a._iDisplayLength,order:h.extend(!0,[],a.aaSorting),search:yb(a.oPreviousSearch),columns:h.map(a.aoColumns,function(b,d){return{visible:b.bVisible,search:yb(a.aoPreSearchCols[d])}})};u(a,"aoStateSaveParams","stateSaveParams",[a,b]);a.oSavedState=
b;a.fnStateSaveCallback.call(a.oInstance,a,b)}}function Jb(a){var b,c,d=a.aoColumns;if(a.oFeatures.bStateSave){var e=a.fnStateLoadCallback.call(a.oInstance,a);if(e&&e.time&&(b=u(a,"aoStateLoadParams","stateLoadParams",[a,e]),-1===h.inArray(!1,b)&&(b=a.iStateDuration,!(0<b&&e.time<+new Date-1E3*b)&&d.length===e.columns.length))){a.oLoadedState=h.extend(!0,{},e);a._iDisplayStart=e.start;a.iInitDisplayStart=e.start;a._iDisplayLength=e.length;a.aaSorting=[];h.each(e.order,function(b,c){a.aaSorting.push(c[0]>=
d.length?[0,c[1]]:c)});h.extend(a.oPreviousSearch,zb(e.search));b=0;for(c=e.columns.length;b<c;b++){var f=e.columns[b];d[b].bVisible=f.visible;h.extend(a.aoPreSearchCols[b],zb(f.search))}u(a,"aoStateLoaded","stateLoaded",[a,e])}}}function ua(a){var b=p.settings,a=h.inArray(a,C(b,"nTable"));return-1!==a?b[a]:null}function P(a,b,c,d){c="DataTables warning: "+(null!==a?"table id="+a.sTableId+" - ":"")+c;d&&(c+=". For more information about this error, please see http://datatables.net/tn/"+d);if(b)za.console&&
console.log&&console.log(c);else if(a=p.ext,"alert"==(a.sErrMode||a.errMode))alert(c);else throw Error(c);}function D(a,b,c,d){h.isArray(c)?h.each(c,function(c,d){h.isArray(d)?D(a,b,d[0],d[1]):D(a,b,d)}):(d===l&&(d=c),b[c]!==l&&(a[d]=b[c]))}function Kb(a,b,c){var d,e;for(e in b)b.hasOwnProperty(e)&&(d=b[e],h.isPlainObject(d)?(h.isPlainObject(a[e])||(a[e]={}),h.extend(!0,a[e],d)):a[e]=c&&"data"!==e&&"aaData"!==e&&h.isArray(d)?d.slice():d);return a}function Ta(a,b,c){h(a).bind("click.DT",b,function(b){a.blur();
c(b)}).bind("keypress.DT",b,function(a){13===a.which&&(a.preventDefault(),c(a))}).bind("selectstart.DT",function(){return!1})}function x(a,b,c,d){c&&a[b].push({fn:c,sName:d})}function u(a,b,c,d){var e=[];b&&(e=h.map(a[b].slice().reverse(),function(b){return b.fn.apply(a.oInstance,d)}));null!==c&&h(a.nTable).trigger(c+".dt",d);return e}function Qa(a){var b=a._iDisplayStart,c=a.fnDisplayEnd(),d=a._iDisplayLength;c===a.fnRecordsDisplay()&&(b=c-d);if(-1===d||0>b)b=0;a._iDisplayStart=b}function La(a,b){var c=
a.renderer,d=p.ext.renderer[b];return h.isPlainObject(c)&&c[b]?d[c[b]]||d._:"string"===typeof c?d[c]||d._:d._}function z(a){return a.oFeatures.bServerSide?"ssp":a.ajax||a.sAjaxSource?"ajax":"dom"}function Ua(a,b){var c=[],c=Lb.numbers_length,d=Math.floor(c/2);b<=c?c=S(0,b):a<=d?(c=S(0,c-2),c.push("ellipsis"),c.push(b-1)):(a>=b-1-d?c=S(b-(c-2),b):(c=S(a-1,a+2),c.push("ellipsis"),c.push(b-1)),c.splice(0,0,"ellipsis"),c.splice(0,0,0));c.DT_el="span";return c}function cb(a){h.each({num:function(b){return va(b,
a)},"num-fmt":function(b){return va(b,a,Va)},"html-num":function(b){return va(b,a,wa)},"html-num-fmt":function(b){return va(b,a,wa,Va)}},function(b,c){t.type.order[b+a+"-pre"]=c})}function Mb(a){return function(){var b=[ua(this[p.ext.iApiIndex])].concat(Array.prototype.slice.call(arguments));return p.ext.internal[a].apply(this,b)}}var p,t,q,r,v,Wa={},Nb=/[\r\n]/g,wa=/<.*?>/g,Yb=/^[\w\+\-]/,Zb=/[\w\+\-]$/,Vb=RegExp("(\\/|\\.|\\*|\\+|\\?|\\||\\(|\\)|\\[|\\]|\\{|\\}|\\\\|\\$|\\^|\\-)","g"),Va=/[',$\u00a3\u20ac\u00a5%\u2009\u202F]/g,
H=function(a){return!a||!0===a||"-"===a?!0:!1},Ob=function(a){var b=parseInt(a,10);return!isNaN(b)&&isFinite(a)?b:null},Pb=function(a,b){Wa[b]||(Wa[b]=RegExp(Oa(b),"g"));return"string"===typeof a?a.replace(/\./g,"").replace(Wa[b],"."):a},Xa=function(a,b,c){var d="string"===typeof a;b&&d&&(a=Pb(a,b));c&&d&&(a=a.replace(Va,""));return H(a)||!isNaN(parseFloat(a))&&isFinite(a)},Qb=function(a,b,c){return H(a)?!0:!(H(a)||"string"===typeof a)?null:Xa(a.replace(wa,""),b,c)?!0:null},C=function(a,b,c){var d=
[],e=0,f=a.length;if(c!==l)for(;e<f;e++)a[e]&&a[e][b]&&d.push(a[e][b][c]);else for(;e<f;e++)a[e]&&d.push(a[e][b]);return d},xa=function(a,b,c,d){var e=[],f=0,g=b.length;if(d!==l)for(;f<g;f++)e.push(a[b[f]][c][d]);else for(;f<g;f++)e.push(a[b[f]][c]);return e},S=function(a,b){var c=[],d;b===l?(b=0,d=a):(d=b,b=a);for(var e=b;e<d;e++)c.push(e);return c},Ja=function(a){var b=[],c,d,e=a.length,f,g=0;d=0;a:for(;d<e;d++){c=a[d];for(f=0;f<g;f++)if(b[f]===c)continue a;b.push(c);g++}return b},w=function(a,
b,c){a[b]!==l&&(a[c]=a[b])},$=/\[.*?\]$/,Q=/\(\)$/,qa=h("<div>")[0],Wb=qa.textContent!==l,Xb=/<.*?>/g;p=function(a){this.$=function(a,b){return this.api(!0).$(a,b)};this._=function(a,b){return this.api(!0).rows(a,b).data()};this.api=function(a){return a?new q(ua(this[t.iApiIndex])):new q(this)};this.fnAddData=function(a,b){var c=this.api(!0),d=h.isArray(a)&&(h.isArray(a[0])||h.isPlainObject(a[0]))?c.rows.add(a):c.row.add(a);(b===l||b)&&c.draw();return d.flatten().toArray()};this.fnAdjustColumnSizing=
function(a){var b=this.api(!0).columns.adjust(),c=b.settings()[0],d=c.oScroll;a===l||a?b.draw(!1):(""!==d.sX||""!==d.sY)&&W(c)};this.fnClearTable=function(a){var b=this.api(!0).clear();(a===l||a)&&b.draw()};this.fnClose=function(a){this.api(!0).row(a).child.hide()};this.fnDeleteRow=function(a,b,c){var d=this.api(!0),a=d.rows(a),e=a.settings()[0],h=e.aoData[a[0][0]];a.remove();b&&b.call(this,e,h);(c===l||c)&&d.draw();return h};this.fnDestroy=function(a){this.api(!0).destroy(a)};this.fnDraw=function(a){this.api(!0).draw(!a)};
this.fnFilter=function(a,b,c,d,e,h){e=this.api(!0);null===b||b===l?e.search(a,c,d,h):e.column(b).search(a,c,d,h);e.draw()};this.fnGetData=function(a,b){var c=this.api(!0);if(a!==l){var d=a.nodeName?a.nodeName.toLowerCase():"";return b!==l||"td"==d||"th"==d?c.cell(a,b).data():c.row(a).data()||null}return c.data().toArray()};this.fnGetNodes=function(a){var b=this.api(!0);return a!==l?b.row(a).node():b.rows().nodes().flatten().toArray()};this.fnGetPosition=function(a){var b=this.api(!0),c=a.nodeName.toUpperCase();
return"TR"==c?b.row(a).index():"TD"==c||"TH"==c?(a=b.cell(a).index(),[a.row,a.columnVisible,a.column]):null};this.fnIsOpen=function(a){return this.api(!0).row(a).child.isShown()};this.fnOpen=function(a,b,c){return this.api(!0).row(a).child(b,c).show().child()[0]};this.fnPageChange=function(a,b){var c=this.api(!0).page(a);(b===l||b)&&c.draw(!1)};this.fnSetColumnVis=function(a,b,c){a=this.api(!0).column(a).visible(b);(c===l||c)&&a.columns.adjust().draw()};this.fnSettings=function(){return ua(this[t.iApiIndex])};
this.fnSort=function(a){this.api(!0).order(a).draw()};this.fnSortListener=function(a,b,c){this.api(!0).order.listener(a,b,c)};this.fnUpdate=function(a,b,c,d,e){var h=this.api(!0);c===l||null===c?h.row(b).data(a):h.cell(b,c).data(a);(e===l||e)&&h.columns.adjust();(d===l||d)&&h.draw();return 0};this.fnVersionCheck=t.fnVersionCheck;var b=this,c=a===l,d=this.length;c&&(a={});this.oApi=this.internal=t.internal;for(var e in p.ext.internal)e&&(this[e]=Mb(e));this.each(function(){var e={},g=1<d?Kb(e,a,!0):
a,j=0,i,n=this.getAttribute("id"),e=!1,m=p.defaults;if("table"!=this.nodeName.toLowerCase())P(null,0,"Non-table node initialisation ("+this.nodeName+")",2);else{db(m);eb(m.column);G(m,m,!0);G(m.column,m.column,!0);G(m,g);var o=p.settings,j=0;for(i=o.length;j<i;j++){if(o[j].nTable==this){i=g.bRetrieve!==l?g.bRetrieve:m.bRetrieve;if(c||i)return o[j].oInstance;if(g.bDestroy!==l?g.bDestroy:m.bDestroy){o[j].oInstance.fnDestroy();break}else{P(o[j],0,"Cannot reinitialise DataTable",3);return}}if(o[j].sTableId==
this.id){o.splice(j,1);break}}if(null===n||""===n)this.id=n="DataTables_Table_"+p.ext._unique++;var k=h.extend(!0,{},p.models.oSettings,{nTable:this,oApi:b.internal,oInit:g,sDestroyWidth:h(this)[0].style.width,sInstance:n,sTableId:n});o.push(k);k.oInstance=1===b.length?b:h(this).dataTable();db(g);g.oLanguage&&N(g.oLanguage);g.aLengthMenu&&!g.iDisplayLength&&(g.iDisplayLength=h.isArray(g.aLengthMenu[0])?g.aLengthMenu[0][0]:g.aLengthMenu[0]);g=Kb(h.extend(!0,{},m),g);D(k.oFeatures,g,"bPaginate bLengthChange bFilter bSort bSortMulti bInfo bProcessing bAutoWidth bSortClasses bServerSide bDeferRender".split(" "));
D(k,g,["asStripeClasses","ajax","fnServerData","fnFormatNumber","sServerMethod","aaSorting","aaSortingFixed","aLengthMenu","sPaginationType","sAjaxSource","sAjaxDataProp","iStateDuration","sDom","bSortCellsTop","iTabIndex","fnStateLoadCallback","fnStateSaveCallback","renderer",["iCookieDuration","iStateDuration"],["oSearch","oPreviousSearch"],["aoSearchCols","aoPreSearchCols"],["iDisplayLength","_iDisplayLength"],["bJQueryUI","bJUI"]]);D(k.oScroll,g,[["sScrollX","sX"],["sScrollXInner","sXInner"],
["sScrollY","sY"],["bScrollCollapse","bCollapse"]]);D(k.oLanguage,g,"fnInfoCallback");x(k,"aoDrawCallback",g.fnDrawCallback,"user");x(k,"aoServerParams",g.fnServerParams,"user");x(k,"aoStateSaveParams",g.fnStateSaveParams,"user");x(k,"aoStateLoadParams",g.fnStateLoadParams,"user");x(k,"aoStateLoaded",g.fnStateLoaded,"user");x(k,"aoRowCallback",g.fnRowCallback,"user");x(k,"aoRowCreatedCallback",g.fnCreatedRow,"user");x(k,"aoHeaderCallback",g.fnHeaderCallback,"user");x(k,"aoFooterCallback",g.fnFooterCallback,
"user");x(k,"aoInitComplete",g.fnInitComplete,"user");x(k,"aoPreDrawCallback",g.fnPreDrawCallback,"user");n=k.oClasses;g.bJQueryUI?(h.extend(n,p.ext.oJUIClasses,g.oClasses),g.sDom===m.sDom&&"lfrtip"===m.sDom&&(k.sDom='<"H"lfr>t<"F"ip>'),k.renderer)?h.isPlainObject(k.renderer)&&!k.renderer.header&&(k.renderer.header="jqueryui"):k.renderer="jqueryui":h.extend(n,p.ext.classes,g.oClasses);h(this).addClass(n.sTable);if(""!==k.oScroll.sX||""!==k.oScroll.sY)k.oScroll.iBarWidth=Gb();!0===k.oScroll.sX&&(k.oScroll.sX=
"100%");k.iInitDisplayStart===l&&(k.iInitDisplayStart=g.iDisplayStart,k._iDisplayStart=g.iDisplayStart);null!==g.iDeferLoading&&(k.bDeferLoading=!0,j=h.isArray(g.iDeferLoading),k._iRecordsDisplay=j?g.iDeferLoading[0]:g.iDeferLoading,k._iRecordsTotal=j?g.iDeferLoading[1]:g.iDeferLoading);""!==g.oLanguage.sUrl?(k.oLanguage.sUrl=g.oLanguage.sUrl,h.getJSON(k.oLanguage.sUrl,null,function(a){N(a);G(m.oLanguage,a);h.extend(true,k.oLanguage,g.oLanguage,a);ra(k)}),e=!0):h.extend(!0,k.oLanguage,g.oLanguage);
null===g.asStripeClasses&&(k.asStripeClasses=[n.sStripeOdd,n.sStripeEven]);var j=k.asStripeClasses,r=h("tbody tr:eq(0)",this);-1!==h.inArray(!0,h.map(j,function(a){return r.hasClass(a)}))&&(h("tbody tr",this).removeClass(j.join(" ")),k.asDestroyStripes=j.slice());var o=[],q,j=this.getElementsByTagName("thead");0!==j.length&&(aa(k.aoHeader,j[0]),o=ma(k));if(null===g.aoColumns){q=[];j=0;for(i=o.length;j<i;j++)q.push(null)}else q=g.aoColumns;j=0;for(i=q.length;j<i;j++)Aa(k,o?o[j]:null);hb(k,g.aoColumnDefs,
q,function(a,b){fa(k,a,b)});if(r.length){var s=function(a,b){return a.getAttribute("data-"+b)?b:null};h.each(ia(k,r[0]).cells,function(a,b){var c=k.aoColumns[a];if(c.mData===a){var d=s(b,"sort")||s(b,"order"),e=s(b,"filter")||s(b,"search");if(d!==null||e!==null){c.mData={_:a+".display",sort:d!==null?a+".@data-"+d:l,type:d!==null?a+".@data-"+d:l,filter:e!==null?a+".@data-"+e:l};fa(k,a)}}})}var t=k.oFeatures;g.bStateSave&&(t.bStateSave=!0,Jb(k,g),x(k,"aoDrawCallback",ta,"state_save"));if(g.aaSorting===
l){o=k.aaSorting;j=0;for(i=o.length;j<i;j++)o[j][1]=k.aoColumns[j].asSorting[0]}sa(k);t.bSort&&x(k,"aoDrawCallback",function(){if(k.bSorted){var a=R(k),b={};h.each(a,function(a,c){b[c.src]=c.dir});u(k,null,"order",[k,a,b]);Ib(k)}});x(k,"aoDrawCallback",function(){(k.bSorted||z(k)==="ssp"||t.bDeferRender)&&sa(k)},"sc");fb(k);j=h(this).children("caption").each(function(){this._captionSide=h(this).css("caption-side")});i=h(this).children("thead");0===i.length&&(i=h("<thead/>").appendTo(this));k.nTHead=
i[0];i=h(this).children("tbody");0===i.length&&(i=h("<tbody/>").appendTo(this));k.nTBody=i[0];i=h(this).children("tfoot");if(0===i.length&&0<j.length&&(""!==k.oScroll.sX||""!==k.oScroll.sY))i=h("<tfoot/>").appendTo(this);0===i.length||0===i.children().length?h(this).addClass(n.sNoFooter):0<i.length&&(k.nTFoot=i[0],aa(k.aoFooter,k.nTFoot));if(g.aaData)for(j=0;j<g.aaData.length;j++)I(k,g.aaData[j]);else(k.bDeferLoading||"dom"==z(k))&&ha(k,h(k.nTBody).children("tr"));k.aiDisplay=k.aiDisplayMaster.slice();
k.bInitialised=!0;!1===e&&ra(k)}});b=null;return this};var Rb=[],y=Array.prototype,$b=function(a){var b,c,d=p.settings,e=h.map(d,function(a){return a.nTable});if(a){if(a.nTable&&a.oApi)return[a];if(a.nodeName&&"table"===a.nodeName.toLowerCase())return b=h.inArray(a,e),-1!==b?[d[b]]:null;if(a&&"function"===typeof a.settings)return a.settings().toArray();"string"===typeof a?c=h(a):a instanceof h&&(c=a)}else return[];if(c)return c.map(function(){b=h.inArray(this,e);return-1!==b?d[b]:null}).toArray()};
q=function(a,b){if(!this instanceof q)throw"DT API must be constructed as a new object";var c=[],d=function(a){(a=$b(a))&&c.push.apply(c,a)};if(h.isArray(a))for(var e=0,f=a.length;e<f;e++)d(a[e]);else d(a);this.context=Ja(c);b&&this.push.apply(this,b.toArray?b.toArray():b);this.selector={rows:null,cols:null,opts:null};q.extend(this,this,Rb)};p.Api=q;q.prototype={concat:y.concat,context:[],each:function(a){for(var b=0,c=this.length;b<c;b++)a.call(this,this[b],b,this);return this},eq:function(a){var b=
this.context;return b.length>a?new q(b[a],this[a]):null},filter:function(a){var b=[];if(y.filter)b=y.filter.call(this,a,this);else for(var c=0,d=this.length;c<d;c++)a.call(this,this[c],c,this)&&b.push(this[c]);return new q(this.context,b)},flatten:function(){var a=[];return new q(this.context,a.concat.apply(a,this.toArray()))},join:y.join,indexOf:y.indexOf||function(a,b){for(var c=b||0,d=this.length;c<d;c++)if(this[c]===a)return c;return-1},iterator:function(a,b,c){var d=[],e,f,g,h,i,n=this.context,
m,o,k=this.selector;"string"===typeof a&&(c=b,b=a,a=!1);f=0;for(g=n.length;f<g;f++)if("table"===b)e=c(n[f],f),e!==l&&d.push(e);else if("columns"===b||"rows"===b)e=c(n[f],this[f],f),e!==l&&d.push(e);else if("column"===b||"column-rows"===b||"row"===b||"cell"===b){o=this[f];"column-rows"===b&&(m=Ya(n[f],k.opts));h=0;for(i=o.length;h<i;h++)e=o[h],e="cell"===b?c(n[f],e.row,e.column,f,h):c(n[f],e,f,h,m),e!==l&&d.push(e)}return d.length?(a=new q(n,a?d.concat.apply([],d):d),b=a.selector,b.rows=k.rows,b.cols=
k.cols,b.opts=k.opts,a):this},lastIndexOf:y.lastIndexOf||function(a,b){return this.indexOf.apply(this.toArray.reverse(),arguments)},length:0,map:function(a){var b=[];if(y.map)b=y.map.call(this,a,this);else for(var c=0,d=this.length;c<d;c++)b.push(a.call(this,this[c],c));return new q(this.context,b)},pluck:function(a){return this.map(function(b){return b[a]})},pop:y.pop,push:y.push,reduce:y.reduce||function(a,b){return gb(this,a,b,0,this.length,1)},reduceRight:y.reduceRight||function(a,b){return gb(this,
a,b,this.length-1,-1,-1)},reverse:y.reverse,selector:null,shift:y.shift,sort:y.sort,splice:y.splice,toArray:function(){return y.slice.call(this)},to$:function(){return h(this)},toJQuery:function(){return h(this)},unique:function(){return new q(this.context,Ja(this))},unshift:y.unshift};q.extend=function(a,b,c){if(b&&(b instanceof q||b.__dt_wrapper)){var d,e,f,g=function(a,b,c){return function(){var d=b.apply(a,arguments);q.extend(d,d,c.methodExt);return d}};d=0;for(e=c.length;d<e;d++)f=c[d],b[f.name]=
"function"===typeof f.val?g(a,f.val,f):h.isPlainObject(f.val)?{}:f.val,b[f.name].__dt_wrapper=!0,q.extend(a,b[f.name],f.propExt)}};q.register=r=function(a,b){if(h.isArray(a))for(var c=0,d=a.length;c<d;c++)q.register(a[c],b);else for(var e=a.split("."),f=Rb,g,j,c=0,d=e.length;c<d;c++){g=(j=-1!==e[c].indexOf("()"))?e[c].replace("()",""):e[c];var i;a:{i=0;for(var n=f.length;i<n;i++)if(f[i].name===g){i=f[i];break a}i=null}i||(i={name:g,val:{},methodExt:[],propExt:[]},f.push(i));c===d-1?i.val=b:f=j?i.methodExt:
i.propExt}};q.registerPlural=v=function(a,b,c){q.register(a,c);q.register(b,function(){var a=c.apply(this,arguments);return a===this?this:a instanceof q?a.length?h.isArray(a[0])?new q(a.context,a[0]):a[0]:l:a})};r("tables()",function(a){var b;if(a){b=q;var c=this.context;if("number"===typeof a)a=[c[a]];else var d=h.map(c,function(a){return a.nTable}),a=h(d).filter(a).map(function(){var a=h.inArray(this,d);return c[a]}).toArray();b=new b(a)}else b=this;return b});r("table()",function(a){var a=this.tables(a),
b=a.context;return b.length?new q(b[0]):a});v("tables().nodes()","table().node()",function(){return this.iterator("table",function(a){return a.nTable})});v("tables().body()","table().body()",function(){return this.iterator("table",function(a){return a.nTBody})});v("tables().header()","table().header()",function(){return this.iterator("table",function(a){return a.nTHead})});v("tables().footer()","table().footer()",function(){return this.iterator("table",function(a){return a.nTFoot})});v("tables().containers()",
"table().container()",function(){return this.iterator("table",function(a){return a.nTableWrapper})});r("draw()",function(a){return this.iterator("table",function(b){L(b,!1===a)})});r("page()",function(a){return a===l?this.page.info().page:this.iterator("table",function(b){Ra(b,a)})});r("page.info()",function(){if(0===this.context.length)return l;var a=this.context[0],b=a._iDisplayStart,c=a._iDisplayLength,d=a.fnRecordsDisplay(),e=-1===c;return{page:e?0:Math.floor(b/c),pages:e?1:Math.ceil(d/c),start:b,
end:a.fnDisplayEnd(),length:c,recordsTotal:a.fnRecordsTotal(),recordsDisplay:d}});r("page.len()",function(a){return a===l?0!==this.context.length?this.context[0]._iDisplayLength:l:this.iterator("table",function(b){Pa(b,a)})});var Sb=function(a,b,c){"ssp"==z(a)?L(a,b):(B(a,!0),na(a,[],function(c){ja(a);for(var c=oa(a,c),d=0,g=c.length;d<g;d++)I(a,c[d]);L(a,b);B(a,!1)}));if(c){var d=new q(a);d.one("draw",function(){c(d.ajax.json())})}};r("ajax.json()",function(){var a=this.context;if(0<a.length)return a[0].json});
r("ajax.params()",function(){var a=this.context;if(0<a.length)return a[0].oAjaxData});r("ajax.reload()",function(a,b){return this.iterator("table",function(c){Sb(c,!1===b,a)})});r("ajax.url()",function(a){var b=this.context;if(a===l){if(0===b.length)return l;b=b[0];return b.ajax?h.isPlainObject(b.ajax)?b.ajax.url:b.ajax:b.sAjaxSource}return this.iterator("table",function(b){h.isPlainObject(b.ajax)?b.ajax.url=a:b.ajax=a})});r("ajax.url().load()",function(a,b){return this.iterator("table",function(c){Sb(c,
!1===b,a)})});var Za=function(a,b){var c=[],d,e,f,g,j,i;if(!a||"string"===typeof a||a.length===l)a=[a];f=0;for(g=a.length;f<g;f++){e=a[f]&&a[f].split?a[f].split(","):[a[f]];j=0;for(i=e.length;j<i;j++)(d=b("string"===typeof e[j]?h.trim(e[j]):e[j]))&&d.length&&c.push.apply(c,d)}return c},$a=function(a){a||(a={});a.filter&&!a.search&&(a.search=a.filter);return{search:a.search||"none",order:a.order||"current",page:a.page||"all"}},ab=function(a){for(var b=0,c=a.length;b<c;b++)if(0<a[b].length)return a[0]=
a[b],a.length=1,a.context=[a.context[b]],a;a.length=0;return a},Ya=function(a,b){var c,d,e,f=[],g=a.aiDisplay;c=a.aiDisplayMaster;var j=b.search;d=b.order;e=b.page;if("ssp"==z(a))return"removed"===j?[]:S(0,c.length);if("current"==e){c=a._iDisplayStart;for(d=a.fnDisplayEnd();c<d;c++)f.push(g[c])}else if("current"==d||"applied"==d)f="none"==j?c.slice():"applied"==j?g.slice():h.map(c,function(a){return-1===h.inArray(a,g)?a:null});else if("index"==d||"original"==d){c=0;for(d=a.aoData.length;c<d;c++)"none"==
j?f.push(c):(e=h.inArray(c,g),(-1===e&&"removed"==j||0<=e&&"applied"==j)&&f.push(c))}return f};r("rows()",function(a,b){a===l?a="":h.isPlainObject(a)&&(b=a,a="");var b=$a(b),c=this.iterator("table",function(c){var e=b;return Za(a,function(a){var b=Ob(a);if(b!==null&&!e)return[b];var j=Ya(c,e);if(b!==null&&h.inArray(b,j)!==-1)return[b];if(!a)return j;for(var b=[],i=0,n=j.length;i<n;i++)b.push(c.aoData[j[i]].nTr);return a.nodeName&&h.inArray(a,b)!==-1?[a._DT_RowIndex]:h(b).filter(a).map(function(){return this._DT_RowIndex}).toArray()})});
c.selector.rows=a;c.selector.opts=b;return c});r("rows().nodes()",function(){return this.iterator("row",function(a,b){return a.aoData[b].nTr||l})});r("rows().data()",function(){return this.iterator(!0,"rows",function(a,b){return xa(a.aoData,b,"_aData")})});v("rows().cache()","row().cache()",function(a){return this.iterator("row",function(b,c){var d=b.aoData[c];return"search"===a?d._aFilterData:d._aSortData})});v("rows().invalidate()","row().invalidate()",function(a){return this.iterator("row",function(b,
c){la(b,c,a)})});v("rows().indexes()","row().index()",function(){return this.iterator("row",function(a,b){return b})});v("rows().remove()","row().remove()",function(){var a=this;return this.iterator("row",function(b,c,d){var e=b.aoData;e.splice(c,1);for(var f=0,g=e.length;f<g;f++)null!==e[f].nTr&&(e[f].nTr._DT_RowIndex=f);h.inArray(c,b.aiDisplay);ka(b.aiDisplayMaster,c);ka(b.aiDisplay,c);ka(a[d],c,!1);Qa(b)})});r("rows.add()",function(a){var b=this.iterator("table",function(b){var c,f,g,h=[];f=0;
for(g=a.length;f<g;f++)c=a[f],c.nodeName&&"TR"===c.nodeName.toUpperCase()?h.push(ha(b,c)[0]):h.push(I(b,c));return h}),c=this.rows(-1);c.pop();c.push.apply(c,b.toArray());return c});r("row()",function(a,b){return ab(this.rows(a,b))});r("row().data()",function(a){var b=this.context;if(a===l)return b.length&&this.length?b[0].aoData[this[0]]._aData:l;b[0].aoData[this[0]]._aData=a;la(b[0],this[0],"data");return this});r("row().node()",function(){var a=this.context;return a.length&&this.length?a[0].aoData[this[0]].nTr||
null:null});r("row.add()",function(a){a instanceof h&&a.length&&(a=a[0]);var b=this.iterator("table",function(b){return a.nodeName&&"TR"===a.nodeName.toUpperCase()?ha(b,a)[0]:I(b,a)});return this.row(b[0])});var bb=function(a){var b=a.context;b.length&&a.length&&(a=b[0].aoData[a[0]],a._details&&(a._details.remove(),a._detailsShow=l,a._details=l))},Tb=function(a,b){var c=a.context;if(c.length&&a.length){var d=c[0].aoData[a[0]];if(d._details){(d._detailsShow=b)?d._details.insertAfter(d.nTr):d._details.detach();
var e=c[0],f=new q(e),g=e.aoData;f.off("draw.dt.DT_details column-visibility.dt.DT_details destroy.dt.DT_details");0<C(g,"_details").length&&(f.on("draw.dt.DT_details",function(a,b){e===b&&f.rows({page:"current"}).eq(0).each(function(a){a=g[a];a._detailsShow&&a._details.insertAfter(a.nTr)})}),f.on("column-visibility.dt.DT_details",function(a,b){if(e===b)for(var c,d=Z(b),f=0,h=g.length;f<h;f++)c=g[f],c._details&&c._details.children("td[colspan]").attr("colspan",d)}),f.on("destroy.dt.DT_details",function(a,
b){if(e===b)for(var c=0,d=g.length;c<d;c++)g[c]._details&&bb(g[c])}))}}};r("row().child()",function(a,b){var c=this.context;if(a===l)return c.length&&this.length?c[0].aoData[this[0]]._details:l;if(!0===a)this.child.show();else if(!1===a)bb(this);else if(c.length&&this.length){var d=c[0],c=c[0].aoData[this[0]],e=[],f=function(a,b){if(a.nodeName&&"tr"===a.nodeName.toLowerCase())e.push(a);else{var c=h("<tr><td/></tr>").addClass(b);h("td",c).addClass(b).html(a)[0].colSpan=Z(d);e.push(c[0])}};if(h.isArray(a)||
a instanceof h)for(var g=0,j=a.length;g<j;g++)f(a[g],b);else f(a,b);c._details&&c._details.remove();c._details=h(e);c._detailsShow&&c._details.insertAfter(c.nTr)}return this});r(["row().child.show()","row().child().show()"],function(){Tb(this,!0);return this});r(["row().child.hide()","row().child().hide()"],function(){Tb(this,!1);return this});r(["row().child.remove()","row().child().remove()"],function(){bb(this);return this});r("row().child.isShown()",function(){var a=this.context;return a.length&&
this.length?a[0].aoData[this[0]]._detailsShow||!1:!1});var ac=/^(.+):(name|visIdx|visible)$/;r("columns()",function(a,b){a===l?a="":h.isPlainObject(a)&&(b=a,a="");var b=$a(b),c=this.iterator("table",function(b){var c=a,f=b.aoColumns,g=C(f,"sName"),j=C(f,"nTh");return Za(c,function(a){var c=Ob(a);if(a==="")return S(f.length);if(c!==null)return[c>=0?c:f.length+c];var e=typeof a==="string"?a.match(ac):"";if(e)switch(e[2]){case "visIdx":case "visible":a=parseInt(e[1],10);if(a<0){c=h.map(f,function(a,
b){return a.bVisible?b:null});return[c[c.length+a]]}return[ga(b,a)];case "name":return h.map(g,function(a,b){return a===e[1]?b:null})}else return h(j).filter(a).map(function(){return h.inArray(this,j)}).toArray()})});c.selector.cols=a;c.selector.opts=b;return c});v("columns().header()","column().header()",function(){return this.iterator("column",function(a,b){return a.aoColumns[b].nTh})});v("columns().footer()","column().footer()",function(){return this.iterator("column",function(a,b){return a.aoColumns[b].nTf})});
v("columns().data()","column().data()",function(){return this.iterator("column-rows",function(a,b,c,d,e){for(var c=[],d=0,f=e.length;d<f;d++)c.push(A(a,e[d],b,""));return c})});v("columns().cache()","column().cache()",function(a){return this.iterator("column-rows",function(b,c,d,e,f){return xa(b.aoData,f,"search"===a?"_aFilterData":"_aSortData",c)})});v("columns().nodes()","column().nodes()",function(){return this.iterator("column-rows",function(a,b,c,d,e){return xa(a.aoData,e,"anCells",b)})});v("columns().visible()",
"column().visible()",function(a,b){return this.iterator("column",function(c,d){var e;if(a===l)e=c.aoColumns[d].bVisible;else{var f=c.aoColumns;e=f[d];var g=c.aoData,j,i,n;if(a===l)e=e.bVisible;else{if(e.bVisible!==a){if(a){var m=h.inArray(!0,C(f,"bVisible"),d+1);j=0;for(i=g.length;j<i;j++)n=g[j].nTr,f=g[j].anCells,n&&n.insertBefore(f[d],f[m]||null)}else h(C(c.aoData,"anCells",d)).detach();e.bVisible=a;ba(c,c.aoHeader);ba(c,c.aoFooter);if(b===l||b)V(c),(c.oScroll.sX||c.oScroll.sY)&&W(c);u(c,null,"column-visibility",
[c,d,a]);ta(c)}e=void 0}}return e})});v("columns().indexes()","column().index()",function(a){return this.iterator("column",function(b,c){return"visible"===a?Y(b,c):c})});r("columns.adjust()",function(){return this.iterator("table",function(a){V(a)})});r("column.index()",function(a,b){if(0!==this.context.length){var c=this.context[0];if("fromVisible"===a||"toData"===a)return ga(c,b);if("fromData"===a||"toVisible"===a)return Y(c,b)}});r("column()",function(a,b){return ab(this.columns(a,b))});r("cells()",
function(a,b,c){h.isPlainObject(a)&&(typeof a.row!==l?(c=b,b=null):(c=a,a=null));h.isPlainObject(b)&&(c=b,b=null);if(null===b||b===l)return this.iterator("table",function(b){var d=a,e=$a(c),f=b.aoData,g=Ya(b,e),e=xa(f,g,"anCells"),j=h([].concat.apply([],e)),i,m=b.aoColumns.length,n,p,r,q;return Za(d,function(a){if(a===null||a===l){n=[];p=0;for(r=g.length;p<r;p++){i=g[p];for(q=0;q<m;q++)n.push({row:i,column:q})}return n}return h.isPlainObject(a)?[a]:j.filter(a).map(function(a,b){i=b.parentNode._DT_RowIndex;
return{row:i,column:h.inArray(b,f[i].anCells)}}).toArray()})});var d=this.columns(b,c),e=this.rows(a,c),f,g,j,i,n,m=this.iterator("table",function(a,b){f=[];g=0;for(j=e[b].length;g<j;g++){i=0;for(n=d[b].length;i<n;i++)f.push({row:e[b][g],column:d[b][i]})}return f});h.extend(m.selector,{cols:b,rows:a,opts:c});return m});v("cells().nodes()","cell().node()",function(){return this.iterator("cell",function(a,b,c){return a.aoData[b].anCells[c]})});r("cells().data()",function(){return this.iterator("cell",
function(a,b,c){return A(a,b,c)})});v("cells().cache()","cell().cache()",function(a){a="search"===a?"_aFilterData":"_aSortData";return this.iterator("cell",function(b,c,d){return b.aoData[c][a][d]})});v("cells().indexes()","cell().index()",function(){return this.iterator("cell",function(a,b,c){return{row:b,column:c,columnVisible:Y(a,c)}})});r(["cells().invalidate()","cell().invalidate()"],function(a){var b=this.selector;this.rows(b.rows,b.opts).invalidate(a);return this});r("cell()",function(a,b,
c){return ab(this.cells(a,b,c))});r("cell().data()",function(a){var b=this.context,c=this[0];if(a===l)return b.length&&c.length?A(b[0],c[0].row,c[0].column):l;Ea(b[0],c[0].row,c[0].column,a);la(b[0],c[0].row,"data",c[0].column);return this});r("order()",function(a,b){var c=this.context;if(a===l)return 0!==c.length?c[0].aaSorting:l;"number"===typeof a?a=[[a,b]]:h.isArray(a[0])||(a=Array.prototype.slice.call(arguments));return this.iterator("table",function(b){b.aaSorting=a.slice()})});r("order.listener()",
function(a,b,c){return this.iterator("table",function(d){Ka(d,a,b,c)})});r(["columns().order()","column().order()"],function(a){var b=this;return this.iterator("table",function(c,d){var e=[];h.each(b[d],function(b,c){e.push([c,a])});c.aaSorting=e})});r("search()",function(a,b,c,d){var e=this.context;return a===l?0!==e.length?e[0].oPreviousSearch.sSearch:l:this.iterator("table",function(e){e.oFeatures.bFilter&&ca(e,h.extend({},e.oPreviousSearch,{sSearch:a+"",bRegex:null===b?!1:b,bSmart:null===c?!0:
c,bCaseInsensitive:null===d?!0:d}),1)})});v("columns().search()","column().search()",function(a,b,c,d){return this.iterator("column",function(e,f){var g=e.aoPreSearchCols;if(a===l)return g[f].sSearch;e.oFeatures.bFilter&&(h.extend(g[f],{sSearch:a+"",bRegex:null===b?!1:b,bSmart:null===c?!0:c,bCaseInsensitive:null===d?!0:d}),ca(e,e.oPreviousSearch,1))})});r("state()",function(){return this.context.length?this.context[0].oSavedState:null});r("state.clear()",function(){return this.iterator("table",function(a){a.fnStateSaveCallback.call(a.oInstance,
a,{})})});r("state.loaded()",function(){return this.context.length?this.context[0].oLoadedState:null});r("state.save()",function(){return this.iterator("table",function(a){ta(a)})});p.versionCheck=p.fnVersionCheck=function(a){for(var b=p.version.split("."),a=a.split("."),c,d,e=0,f=a.length;e<f;e++)if(c=parseInt(b[e],10)||0,d=parseInt(a[e],10)||0,c!==d)return c>d;return!0};p.isDataTable=p.fnIsDataTable=function(a){var b=h(a).get(0),c=!1;h.each(p.settings,function(a,e){if(e.nTable===b||e.nScrollHead===
b||e.nScrollFoot===b)c=!0});return c};p.tables=p.fnTables=function(a){return jQuery.map(p.settings,function(b){if(!a||a&&h(b.nTable).is(":visible"))return b.nTable})};p.camelToHungarian=G;r("$()",function(a,b){var c=this.rows(b).nodes(),c=h(c);return h([].concat(c.filter(a).toArray(),c.find(a).toArray()))});h.each(["on","one","off"],function(a,b){r(b+"()",function(){var a=Array.prototype.slice.call(arguments);a[0].match(/\.dt\b/)||(a[0]+=".dt");var d=h(this.tables().nodes());d[b].apply(d,a);return this})});
r("clear()",function(){return this.iterator("table",function(a){ja(a)})});r("settings()",function(){return new q(this.context,this.context)});r("data()",function(){return this.iterator("table",function(a){return C(a.aoData,"_aData")}).flatten()});r("destroy()",function(a){a=a||!1;return this.iterator("table",function(b){var c=b.nTableWrapper.parentNode,d=b.oClasses,e=b.nTable,f=b.nTBody,g=b.nTHead,j=b.nTFoot,i=h(e),f=h(f),l=h(b.nTableWrapper),m=h.map(b.aoData,function(a){return a.nTr}),o;b.bDestroying=
!0;u(b,"aoDestroyCallback","destroy",[b]);a||(new q(b)).columns().visible(!0);l.unbind(".DT").find(":not(tbody *)").unbind(".DT");h(za).unbind(".DT-"+b.sInstance);e!=g.parentNode&&(i.children("thead").detach(),i.append(g));j&&e!=j.parentNode&&(i.children("tfoot").detach(),i.append(j));i.detach();l.detach();b.aaSorting=[];b.aaSortingFixed=[];sa(b);h(m).removeClass(b.asStripeClasses.join(" "));h("th, td",g).removeClass(d.sSortable+" "+d.sSortableAsc+" "+d.sSortableDesc+" "+d.sSortableNone);b.bJUI&&
(h("th span."+d.sSortIcon+", td span."+d.sSortIcon,g).detach(),h("th, td",g).each(function(){var a=h("div."+d.sSortJUIWrapper,this);h(this).append(a.contents());a.detach()}));!a&&c&&c.insertBefore(e,b.nTableReinsertBefore);f.children().detach();f.append(m);i.css("width",b.sDestroyWidth).removeClass(d.sTable);(o=b.asDestroyStripes.length)&&f.children().each(function(a){h(this).addClass(b.asDestroyStripes[a%o])});c=h.inArray(b,p.settings);-1!==c&&p.settings.splice(c,1)})});p.version="1.10.2";p.settings=
[];p.models={};p.models.oSearch={bCaseInsensitive:!0,sSearch:"",bRegex:!1,bSmart:!0};p.models.oRow={nTr:null,anCells:null,_aData:[],_aSortData:null,_aFilterData:null,_sFilterRow:null,_sRowStripe:"",src:null};p.models.oColumn={idx:null,aDataSort:null,asSorting:null,bSearchable:null,bSortable:null,bVisible:null,_sManualType:null,_bAttrSrc:!1,fnCreatedCell:null,fnGetData:null,fnSetData:null,mData:null,mRender:null,nTh:null,nTf:null,sClass:null,sContentPadding:null,sDefaultContent:null,sName:null,sSortDataType:"std",
sSortingClass:null,sSortingClassJUI:null,sTitle:null,sType:null,sWidth:null,sWidthOrig:null};p.defaults={aaData:null,aaSorting:[[0,"asc"]],aaSortingFixed:[],ajax:null,aLengthMenu:[10,25,50,100],aoColumns:null,aoColumnDefs:null,aoSearchCols:[],asStripeClasses:null,bAutoWidth:!0,bDeferRender:!1,bDestroy:!1,bFilter:!0,bInfo:!0,bJQueryUI:!1,bLengthChange:!0,bPaginate:!0,bProcessing:!1,bRetrieve:!1,bScrollCollapse:!1,bServerSide:!1,bSort:!0,bSortMulti:!0,bSortCellsTop:!1,bSortClasses:!0,bStateSave:!1,
fnCreatedRow:null,fnDrawCallback:null,fnFooterCallback:null,fnFormatNumber:function(a){return a.toString().replace(/\B(?=(\d{3})+(?!\d))/g,this.oLanguage.sThousands)},fnHeaderCallback:null,fnInfoCallback:null,fnInitComplete:null,fnPreDrawCallback:null,fnRowCallback:null,fnServerData:null,fnServerParams:null,fnStateLoadCallback:function(a){try{return JSON.parse((-1===a.iStateDuration?sessionStorage:localStorage).getItem("DataTables_"+a.sInstance+"_"+location.pathname))}catch(b){}},fnStateLoadParams:null,
fnStateLoaded:null,fnStateSaveCallback:function(a,b){try{(-1===a.iStateDuration?sessionStorage:localStorage).setItem("DataTables_"+a.sInstance+"_"+location.pathname,JSON.stringify(b))}catch(c){}},fnStateSaveParams:null,iStateDuration:7200,iDeferLoading:null,iDisplayLength:10,iDisplayStart:0,iTabIndex:0,oClasses:{},oLanguage:{oAria:{sSortAscending:": activate to sort column ascending",sSortDescending:": activate to sort column descending"},oPaginate:{sFirst:"First",sLast:"Last",sNext:"Next",sPrevious:"Previous"},
sEmptyTable:"No data available in table",sInfo:"Showing _START_ to _END_ of _TOTAL_ entries",sInfoEmpty:"Showing 0 to 0 of 0 entries",sInfoFiltered:"(filtered from _MAX_ total entries)",sInfoPostFix:"",sDecimal:"",sThousands:",",sLengthMenu:"Show _MENU_ entries",sLoadingRecords:"Loading...",sProcessing:"Processing...",sSearch:"Search:",sSearchPlaceholder:"",sUrl:"",sZeroRecords:"No matching records found"},oSearch:h.extend({},p.models.oSearch),sAjaxDataProp:"data",sAjaxSource:null,sDom:"lfrtip",sPaginationType:"simple_numbers",
sScrollX:"",sScrollXInner:"",sScrollY:"",sServerMethod:"GET",renderer:null};T(p.defaults);p.defaults.column={aDataSort:null,iDataSort:-1,asSorting:["asc","desc"],bSearchable:!0,bSortable:!0,bVisible:!0,fnCreatedCell:null,mData:null,mRender:null,sCellType:"td",sClass:"",sContentPadding:"",sDefaultContent:null,sName:"",sSortDataType:"std",sTitle:null,sType:null,sWidth:null};T(p.defaults.column);p.models.oSettings={oFeatures:{bAutoWidth:null,bDeferRender:null,bFilter:null,bInfo:null,bLengthChange:null,
bPaginate:null,bProcessing:null,bServerSide:null,bSort:null,bSortMulti:null,bSortClasses:null,bStateSave:null},oScroll:{bCollapse:null,iBarWidth:0,sX:null,sXInner:null,sY:null},oLanguage:{fnInfoCallback:null},oBrowser:{bScrollOversize:!1,bScrollbarLeft:!1},ajax:null,aanFeatures:[],aoData:[],aiDisplay:[],aiDisplayMaster:[],aoColumns:[],aoHeader:[],aoFooter:[],oPreviousSearch:{},aoPreSearchCols:[],aaSorting:null,aaSortingFixed:[],asStripeClasses:null,asDestroyStripes:[],sDestroyWidth:0,aoRowCallback:[],
aoHeaderCallback:[],aoFooterCallback:[],aoDrawCallback:[],aoRowCreatedCallback:[],aoPreDrawCallback:[],aoInitComplete:[],aoStateSaveParams:[],aoStateLoadParams:[],aoStateLoaded:[],sTableId:"",nTable:null,nTHead:null,nTFoot:null,nTBody:null,nTableWrapper:null,bDeferLoading:!1,bInitialised:!1,aoOpenRows:[],sDom:null,sPaginationType:"two_button",iStateDuration:0,aoStateSave:[],aoStateLoad:[],oSavedState:null,oLoadedState:null,sAjaxSource:null,sAjaxDataProp:null,bAjaxDataGet:!0,jqXHR:null,json:l,oAjaxData:l,
fnServerData:null,aoServerParams:[],sServerMethod:null,fnFormatNumber:null,aLengthMenu:null,iDraw:0,bDrawing:!1,iDrawError:-1,_iDisplayLength:10,_iDisplayStart:0,_iRecordsTotal:0,_iRecordsDisplay:0,bJUI:null,oClasses:{},bFiltered:!1,bSorted:!1,bSortCellsTop:null,oInit:null,aoDestroyCallback:[],fnRecordsTotal:function(){return"ssp"==z(this)?1*this._iRecordsTotal:this.aiDisplayMaster.length},fnRecordsDisplay:function(){return"ssp"==z(this)?1*this._iRecordsDisplay:this.aiDisplay.length},fnDisplayEnd:function(){var a=
this._iDisplayLength,b=this._iDisplayStart,c=b+a,d=this.aiDisplay.length,e=this.oFeatures,f=e.bPaginate;return e.bServerSide?!1===f||-1===a?b+d:Math.min(b+a,this._iRecordsDisplay):!f||c>d||-1===a?d:c},oInstance:null,sInstance:null,iTabIndex:0,nScrollHead:null,nScrollFoot:null,aLastSort:[],oPlugins:{}};p.ext=t={classes:{},errMode:"alert",feature:[],search:[],internal:{},legacy:{ajax:null},pager:{},renderer:{pageButton:{},header:{}},order:{},type:{detect:[],search:{},order:{}},_unique:0,fnVersionCheck:p.fnVersionCheck,
iApiIndex:0,oJUIClasses:{},sVersion:p.version};h.extend(t,{afnFiltering:t.search,aTypes:t.type.detect,ofnSearch:t.type.search,oSort:t.type.order,afnSortData:t.order,aoFeatures:t.feature,oApi:t.internal,oStdClasses:t.classes,oPagination:t.pager});h.extend(p.ext.classes,{sTable:"dataTable",sNoFooter:"no-footer",sPageButton:"paginate_button",sPageButtonActive:"current",sPageButtonDisabled:"disabled",sStripeOdd:"odd",sStripeEven:"even",sRowEmpty:"dataTables_empty",sWrapper:"dataTables_wrapper",sFilter:"dataTables_filter",
sInfo:"dataTables_info",sPaging:"dataTables_paginate paging_",sLength:"dataTables_length",sProcessing:"dataTables_processing",sSortAsc:"sorting_asc",sSortDesc:"sorting_desc",sSortable:"sorting",sSortableAsc:"sorting_asc_disabled",sSortableDesc:"sorting_desc_disabled",sSortableNone:"sorting_disabled",sSortColumn:"sorting_",sFilterInput:"",sLengthSelect:"",sScrollWrapper:"dataTables_scroll",sScrollHead:"dataTables_scrollHead",sScrollHeadInner:"dataTables_scrollHeadInner",sScrollBody:"dataTables_scrollBody",
sScrollFoot:"dataTables_scrollFoot",sScrollFootInner:"dataTables_scrollFootInner",sHeaderTH:"",sFooterTH:"",sSortJUIAsc:"",sSortJUIDesc:"",sSortJUI:"",sSortJUIAscAllowed:"",sSortJUIDescAllowed:"",sSortJUIWrapper:"",sSortIcon:"",sJUIHeader:"",sJUIFooter:""});var ya="",ya="",E=ya+"ui-state-default",ea=ya+"css_right ui-icon ui-icon-",Ub=ya+"fg-toolbar ui-toolbar ui-widget-header ui-helper-clearfix";h.extend(p.ext.oJUIClasses,p.ext.classes,{sPageButton:"fg-button ui-button "+E,sPageButtonActive:"ui-state-disabled",
sPageButtonDisabled:"ui-state-disabled",sPaging:"dataTables_paginate fg-buttonset ui-buttonset fg-buttonset-multi ui-buttonset-multi paging_",sSortAsc:E+" sorting_asc",sSortDesc:E+" sorting_desc",sSortable:E+" sorting",sSortableAsc:E+" sorting_asc_disabled",sSortableDesc:E+" sorting_desc_disabled",sSortableNone:E+" sorting_disabled",sSortJUIAsc:ea+"triangle-1-n",sSortJUIDesc:ea+"triangle-1-s",sSortJUI:ea+"carat-2-n-s",sSortJUIAscAllowed:ea+"carat-1-n",sSortJUIDescAllowed:ea+"carat-1-s",sSortJUIWrapper:"DataTables_sort_wrapper",
sSortIcon:"DataTables_sort_icon",sScrollHead:"dataTables_scrollHead "+E,sScrollFoot:"dataTables_scrollFoot "+E,sHeaderTH:E,sFooterTH:E,sJUIHeader:Ub+" ui-corner-tl ui-corner-tr",sJUIFooter:Ub+" ui-corner-bl ui-corner-br"});var Lb=p.ext.pager;h.extend(Lb,{simple:function(){return["previous","next"]},full:function(){return["first","previous","next","last"]},simple_numbers:function(a,b){return["previous",Ua(a,b),"next"]},full_numbers:function(a,b){return["first","previous",Ua(a,b),"next","last"]},_numbers:Ua,
numbers_length:7});h.extend(!0,p.ext.renderer,{pageButton:{_:function(a,b,c,d,e,f){var g=a.oClasses,j=a.oLanguage.oPaginate,i,l,m=0,o=function(b,d){var k,p,r,q,s=function(b){Ra(a,b.data.action,true)};k=0;for(p=d.length;k<p;k++){q=d[k];if(h.isArray(q)){r=h("<"+(q.DT_el||"div")+"/>").appendTo(b);o(r,q)}else{l=i="";switch(q){case "ellipsis":b.append("<span>&hellip;</span>");break;case "first":i=j.sFirst;l=q+(e>0?"":" "+g.sPageButtonDisabled);break;case "previous":i=j.sPrevious;l=q+(e>0?"":" "+g.sPageButtonDisabled);
break;case "next":i=j.sNext;l=q+(e<f-1?"":" "+g.sPageButtonDisabled);break;case "last":i=j.sLast;l=q+(e<f-1?"":" "+g.sPageButtonDisabled);break;default:i=q+1;l=e===q?g.sPageButtonActive:""}if(i){r=h("<a>",{"class":g.sPageButton+" "+l,"aria-controls":a.sTableId,"data-dt-idx":m,tabindex:a.iTabIndex,id:c===0&&typeof q==="string"?a.sTableId+"_"+q:null}).html(i).appendTo(b);Ta(r,{action:q},s);m++}}}};try{var k=h(O.activeElement).data("dt-idx");o(h(b).empty(),d);k!==null&&h(b).find("[data-dt-idx="+k+"]").focus()}catch(p){}}}});
var va=function(a,b,c,d){if(!a||"-"===a)return-Infinity;b&&(a=Pb(a,b));a.replace&&(c&&(a=a.replace(c,"")),d&&(a=a.replace(d,"")));return 1*a};h.extend(t.type.order,{"date-pre":function(a){return Date.parse(a)||0},"html-pre":function(a){return H(a)?"":a.replace?a.replace(/<.*?>/g,"").toLowerCase():a+""},"string-pre":function(a){return H(a)?"":"string"===typeof a?a.toLowerCase():!a.toString?"":a.toString()},"string-asc":function(a,b){return a<b?-1:a>b?1:0},"string-desc":function(a,b){return a<b?1:a>
b?-1:0}});cb("");h.extend(p.ext.type.detect,[function(a,b){var c=b.oLanguage.sDecimal;return Xa(a,c)?"num"+c:null},function(a){if(a&&(!Yb.test(a)||!Zb.test(a)))return null;var b=Date.parse(a);return null!==b&&!isNaN(b)||H(a)?"date":null},function(a,b){var c=b.oLanguage.sDecimal;return Xa(a,c,!0)?"num-fmt"+c:null},function(a,b){var c=b.oLanguage.sDecimal;return Qb(a,c)?"html-num"+c:null},function(a,b){var c=b.oLanguage.sDecimal;return Qb(a,c,!0)?"html-num-fmt"+c:null},function(a){return H(a)||"string"===
typeof a&&-1!==a.indexOf("<")?"html":null}]);h.extend(p.ext.type.search,{html:function(a){return H(a)?a:"string"===typeof a?a.replace(Nb," ").replace(wa,""):""},string:function(a){return H(a)?a:"string"===typeof a?a.replace(Nb," "):a}});h.extend(!0,p.ext.renderer,{header:{_:function(a,b,c,d){h(a.nTable).on("order.dt.DT",function(e,f,g,h){if(a===f){e=c.idx;b.removeClass(c.sSortingClass+" "+d.sSortAsc+" "+d.sSortDesc).addClass(h[e]=="asc"?d.sSortAsc:h[e]=="desc"?d.sSortDesc:c.sSortingClass)}})},jqueryui:function(a,
b,c,d){var e=c.idx;h("<div/>").addClass(d.sSortJUIWrapper).append(b.contents()).append(h("<span/>").addClass(d.sSortIcon+" "+c.sSortingClassJUI)).appendTo(b);h(a.nTable).on("order.dt.DT",function(f,g,h,i){if(a===g){b.removeClass(d.sSortAsc+" "+d.sSortDesc).addClass(i[e]=="asc"?d.sSortAsc:i[e]=="desc"?d.sSortDesc:c.sSortingClass);b.find("span."+d.sSortIcon).removeClass(d.sSortJUIAsc+" "+d.sSortJUIDesc+" "+d.sSortJUI+" "+d.sSortJUIAscAllowed+" "+d.sSortJUIDescAllowed).addClass(i[e]=="asc"?d.sSortJUIAsc:
i[e]=="desc"?d.sSortJUIDesc:c.sSortingClassJUI)}})}}});p.render={number:function(a,b,c,d){return{display:function(e){var f=0>e?"-":"",e=Math.abs(parseFloat(e)),g=parseInt(e,10),e=c?b+(e-g).toFixed(c).substring(2):"";return f+(d||"")+g.toString().replace(/\B(?=(\d{3})+(?!\d))/g,a)+e}}}};h.extend(p.ext.internal,{_fnExternApiFunc:Mb,_fnBuildAjax:na,_fnAjaxUpdate:jb,_fnAjaxParameters:sb,_fnAjaxUpdateDraw:tb,_fnAjaxDataSrc:oa,_fnAddColumn:Aa,_fnColumnOptions:fa,_fnAdjustColumnSizing:V,_fnVisibleToColumnIndex:ga,
_fnColumnIndexToVisible:Y,_fnVisbleColumns:Z,_fnGetColumns:X,_fnColumnTypes:Da,_fnApplyColumnDefs:hb,_fnHungarianMap:T,_fnCamelToHungarian:G,_fnLanguageCompat:N,_fnBrowserDetect:fb,_fnAddData:I,_fnAddTr:ha,_fnNodeToDataIndex:function(a,b){return b._DT_RowIndex!==l?b._DT_RowIndex:null},_fnNodeToColumnIndex:function(a,b,c){return h.inArray(c,a.aoData[b].anCells)},_fnGetCellData:A,_fnSetCellData:Ea,_fnSplitObjNotation:Ga,_fnGetObjectDataFn:U,_fnSetObjectDataFn:Ba,_fnGetDataMaster:Ha,_fnClearTable:ja,
_fnDeleteIndex:ka,_fnInvalidateRow:la,_fnGetRowElements:ia,_fnCreateTr:Fa,_fnBuildHead:ib,_fnDrawHead:ba,_fnDraw:K,_fnReDraw:L,_fnAddOptionsHtml:lb,_fnDetectHeader:aa,_fnGetUniqueThs:ma,_fnFeatureHtmlFilter:nb,_fnFilterComplete:ca,_fnFilterCustom:wb,_fnFilterColumn:vb,_fnFilter:ub,_fnFilterCreateSearch:Na,_fnEscapeRegex:Oa,_fnFilterData:xb,_fnFeatureHtmlInfo:qb,_fnUpdateInfo:Ab,_fnInfoMacros:Bb,_fnInitialise:ra,_fnInitComplete:pa,_fnLengthChange:Pa,_fnFeatureHtmlLength:mb,_fnFeatureHtmlPaginate:rb,
_fnPageChange:Ra,_fnFeatureHtmlProcessing:ob,_fnProcessingDisplay:B,_fnFeatureHtmlTable:pb,_fnScrollDraw:W,_fnApplyToChildren:F,_fnCalculateColumnWidths:Ca,_fnThrottle:Ma,_fnConvertToWidth:Cb,_fnScrollingWidthAdjust:Eb,_fnGetWidestNode:Db,_fnGetMaxLenString:Fb,_fnStringToCss:s,_fnScrollBarWidth:Gb,_fnSortFlatten:R,_fnSort:kb,_fnSortAria:Ib,_fnSortListener:Sa,_fnSortAttachListener:Ka,_fnSortingClasses:sa,_fnSortData:Hb,_fnSaveState:ta,_fnLoadState:Jb,_fnSettingsFromNode:ua,_fnLog:P,_fnMap:D,_fnBindAction:Ta,
_fnCallbackReg:x,_fnCallbackFire:u,_fnLengthOverflow:Qa,_fnRenderer:La,_fnDataSource:z,_fnRowAttributes:Ia,_fnCalculateEnd:function(){}});h.fn.dataTable=p;h.fn.dataTableSettings=p.settings;h.fn.dataTableExt=p.ext;h.fn.DataTable=function(a){return h(this).dataTable(a).api()};h.each(p,function(a,b){h.fn.DataTable[a]=b});return h.fn.dataTable};"function"===typeof define&&define.amd?define("datatables",["jquery"],N):"object"===typeof exports?N(require("jquery")):jQuery&&!jQuery.fn.dataTable&&N(jQuery)})(window,
document);

/*! TableTools 2.2.2
 * 2009-2014 SpryMedia Ltd - datatables.net/license
 *
 * ZeroClipboard 1.0.4
 * Author: Joseph Huckaby - MIT licensed
 */

/**
 * @summary     TableTools
 * @description Tools and buttons for DataTables
 * @version     2.2.2
 * @file        dataTables.tableTools.js
 * @author      SpryMedia Ltd (www.sprymedia.co.uk)
 * @contact     www.sprymedia.co.uk/contact
 * @copyright   Copyright 2009-2014 SpryMedia Ltd.
 *
 * This source file is free software, available under the following license:
 *   MIT license - http://datatables.net/license/mit
 *
 * This source file is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
 * or FITNESS FOR A PARTICULAR PURPOSE. See the license files for details.
 *
 * For details please refer to: http://www.datatables.net
 */


/* Global scope for TableTools for backwards compatibility.
 * Will be removed in 2.3
 */
var TableTools;

(function(window, document, undefined) {


var factory = function( $, DataTable ) {



//include ZeroClipboard.js
/* ZeroClipboard 1.0.4
 * Author: Joseph Huckaby
 */

var ZeroClipboard_TableTools = {

	version: "1.0.4-TableTools2",
	clients: {}, // registered upload clients on page, indexed by id
	moviePath: '', // URL to movie
	nextId: 1, // ID of next movie

	$: function(thingy) {
		// simple DOM lookup utility function
		if (typeof(thingy) == 'string') {
			thingy = document.getElementById(thingy);
		}
		if (!thingy.addClass) {
			// extend element with a few useful methods
			thingy.hide = function() { this.style.display = 'none'; };
			thingy.show = function() { this.style.display = ''; };
			thingy.addClass = function(name) { this.removeClass(name); this.className += ' ' + name; };
			thingy.removeClass = function(name) {
				this.className = this.className.replace( new RegExp("\\s*" + name + "\\s*"), " ").replace(/^\s+/, '').replace(/\s+$/, '');
			};
			thingy.hasClass = function(name) {
				return !!this.className.match( new RegExp("\\s*" + name + "\\s*") );
			};
		}
		return thingy;
	},

	setMoviePath: function(path) {
		// set path to ZeroClipboard.swf
		this.moviePath = path;
	},

	dispatch: function(id, eventName, args) {
		// receive event from flash movie, send to client
		var client = this.clients[id];
		if (client) {
			client.receiveEvent(eventName, args);
		}
	},

	register: function(id, client) {
		// register new client to receive events
		this.clients[id] = client;
	},

	getDOMObjectPosition: function(obj) {
		// get absolute coordinates for dom element
		var info = {
			left: 0,
			top: 0,
			width: obj.width ? obj.width : obj.offsetWidth,
			height: obj.height ? obj.height : obj.offsetHeight
		};

		if ( obj.style.width !== "" ) {
			info.width = obj.style.width.replace("px","");
		}

		if ( obj.style.height !== "" ) {
			info.height = obj.style.height.replace("px","");
		}

		while (obj) {
			info.left += obj.offsetLeft;
			info.top += obj.offsetTop;
			obj = obj.offsetParent;
		}

		return info;
	},

	Client: function(elem) {
		// constructor for new simple upload client
		this.handlers = {};

		// unique ID
		this.id = ZeroClipboard_TableTools.nextId++;
		this.movieId = 'ZeroClipboard_TableToolsMovie_' + this.id;

		// register client with singleton to receive flash events
		ZeroClipboard_TableTools.register(this.id, this);

		// create movie
		if (elem) {
			this.glue(elem);
		}
	}
};

ZeroClipboard_TableTools.Client.prototype = {

	id: 0, // unique ID for us
	ready: false, // whether movie is ready to receive events or not
	movie: null, // reference to movie object
	clipText: '', // text to copy to clipboard
	fileName: '', // default file save name
	action: 'copy', // action to perform
	handCursorEnabled: true, // whether to show hand cursor, or default pointer cursor
	cssEffects: true, // enable CSS mouse effects on dom container
	handlers: null, // user event handlers
	sized: false,

	glue: function(elem, title) {
		// glue to DOM element
		// elem can be ID or actual DOM element object
		this.domElement = ZeroClipboard_TableTools.$(elem);

		// float just above object, or zIndex 99 if dom element isn't set
		var zIndex = 99;
		if (this.domElement.style.zIndex) {
			zIndex = parseInt(this.domElement.style.zIndex, 10) + 1;
		}

		// find X/Y position of domElement
		var box = ZeroClipboard_TableTools.getDOMObjectPosition(this.domElement);

		// create floating DIV above element
		this.div = document.createElement('div');
		var style = this.div.style;
		style.position = 'absolute';
		style.left = '0px';
		style.top = '0px';
		style.width = (box.width) + 'px';
		style.height = box.height + 'px';
		style.zIndex = zIndex;

		if ( typeof title != "undefined" && title !== "" ) {
			this.div.title = title;
		}
		if ( box.width !== 0 && box.height !== 0 ) {
			this.sized = true;
		}

		// style.backgroundColor = '#f00'; // debug
		if ( this.domElement ) {
			this.domElement.appendChild(this.div);
			this.div.innerHTML = this.getHTML( box.width, box.height ).replace(/&/g, '&amp;');
		}
	},

	positionElement: function() {
		var box = ZeroClipboard_TableTools.getDOMObjectPosition(this.domElement);
		var style = this.div.style;

		style.position = 'absolute';
		//style.left = (this.domElement.offsetLeft)+'px';
		//style.top = this.domElement.offsetTop+'px';
		style.width = box.width + 'px';
		style.height = box.height + 'px';

		if ( box.width !== 0 && box.height !== 0 ) {
			this.sized = true;
		} else {
			return;
		}

		var flash = this.div.childNodes[0];
		flash.width = box.width;
		flash.height = box.height;
	},

	getHTML: function(width, height) {
		// return HTML for movie
		var html = '';
		var flashvars = 'id=' + this.id +
			'&width=' + width +
			'&height=' + height;

		if (navigator.userAgent.match(/MSIE/)) {
			// IE gets an OBJECT tag
			var protocol = location.href.match(/^https/i) ? 'https://' : 'http://';
			html += '<object classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" codebase="'+protocol+'download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=10,0,0,0" width="'+width+'" height="'+height+'" id="'+this.movieId+'" align="middle"><param name="allowScriptAccess" value="always" /><param name="allowFullScreen" value="false" /><param name="movie" value="'+ZeroClipboard_TableTools.moviePath+'" /><param name="loop" value="false" /><param name="menu" value="false" /><param name="quality" value="best" /><param name="bgcolor" value="#ffffff" /><param name="flashvars" value="'+flashvars+'"/><param name="wmode" value="transparent"/></object>';
		}
		else {
			// all other browsers get an EMBED tag
			html += '<embed id="'+this.movieId+'" src="'+ZeroClipboard_TableTools.moviePath+'" loop="false" menu="false" quality="best" bgcolor="#ffffff" width="'+width+'" height="'+height+'" name="'+this.movieId+'" align="middle" allowScriptAccess="always" allowFullScreen="false" type="application/x-shockwave-flash" pluginspage="http://www.macromedia.com/go/getflashplayer" flashvars="'+flashvars+'" wmode="transparent" />';
		}
		return html;
	},

	hide: function() {
		// temporarily hide floater offscreen
		if (this.div) {
			this.div.style.left = '-2000px';
		}
	},

	show: function() {
		// show ourselves after a call to hide()
		this.reposition();
	},

	destroy: function() {
		// destroy control and floater
		if (this.domElement && this.div) {
			this.hide();
			this.div.innerHTML = '';

			var body = document.getElementsByTagName('body')[0];
			try { body.removeChild( this.div ); } catch(e) {}

			this.domElement = null;
			this.div = null;
		}
	},

	reposition: function(elem) {
		// reposition our floating div, optionally to new container
		// warning: container CANNOT change size, only position
		if (elem) {
			this.domElement = ZeroClipboard_TableTools.$(elem);
			if (!this.domElement) {
				this.hide();
			}
		}

		if (this.domElement && this.div) {
			var box = ZeroClipboard_TableTools.getDOMObjectPosition(this.domElement);
			var style = this.div.style;
			style.left = '' + box.left + 'px';
			style.top = '' + box.top + 'px';
		}
	},

	clearText: function() {
		// clear the text to be copy / saved
		this.clipText = '';
		if (this.ready) {
			this.movie.clearText();
		}
	},

	appendText: function(newText) {
		// append text to that which is to be copied / saved
		this.clipText += newText;
		if (this.ready) { this.movie.appendText(newText) ;}
	},

	setText: function(newText) {
		// set text to be copied to be copied / saved
		this.clipText = newText;
		if (this.ready) { this.movie.setText(newText) ;}
	},

	setCharSet: function(charSet) {
		// set the character set (UTF16LE or UTF8)
		this.charSet = charSet;
		if (this.ready) { this.movie.setCharSet(charSet) ;}
	},

	setBomInc: function(bomInc) {
		// set if the BOM should be included or not
		this.incBom = bomInc;
		if (this.ready) { this.movie.setBomInc(bomInc) ;}
	},

	setFileName: function(newText) {
		// set the file name
		this.fileName = newText;
		if (this.ready) {
			this.movie.setFileName(newText);
		}
	},

	setAction: function(newText) {
		// set action (save or copy)
		this.action = newText;
		if (this.ready) {
			this.movie.setAction(newText);
		}
	},

	addEventListener: function(eventName, func) {
		// add user event listener for event
		// event types: load, queueStart, fileStart, fileComplete, queueComplete, progress, error, cancel
		eventName = eventName.toString().toLowerCase().replace(/^on/, '');
		if (!this.handlers[eventName]) {
			this.handlers[eventName] = [];
		}
		this.handlers[eventName].push(func);
	},

	setHandCursor: function(enabled) {
		// enable hand cursor (true), or default arrow cursor (false)
		this.handCursorEnabled = enabled;
		if (this.ready) {
			this.movie.setHandCursor(enabled);
		}
	},

	setCSSEffects: function(enabled) {
		// enable or disable CSS effects on DOM container
		this.cssEffects = !!enabled;
	},

	receiveEvent: function(eventName, args) {
		var self;

		// receive event from flash
		eventName = eventName.toString().toLowerCase().replace(/^on/, '');

		// special behavior for certain events
		switch (eventName) {
			case 'load':
				// movie claims it is ready, but in IE this isn't always the case...
				// bug fix: Cannot extend EMBED DOM elements in Firefox, must use traditional function
				this.movie = document.getElementById(this.movieId);
				if (!this.movie) {
					self = this;
					setTimeout( function() { self.receiveEvent('load', null); }, 1 );
					return;
				}

				// firefox on pc needs a "kick" in order to set these in certain cases
				if (!this.ready && navigator.userAgent.match(/Firefox/) && navigator.userAgent.match(/Windows/)) {
					self = this;
					setTimeout( function() { self.receiveEvent('load', null); }, 100 );
					this.ready = true;
					return;
				}

				this.ready = true;
				this.movie.clearText();
				this.movie.appendText( this.clipText );
				this.movie.setFileName( this.fileName );
				this.movie.setAction( this.action );
				this.movie.setCharSet( this.charSet );
				this.movie.setBomInc( this.incBom );
				this.movie.setHandCursor( this.handCursorEnabled );
				break;

			case 'mouseover':
				if (this.domElement && this.cssEffects) {
					//this.domElement.addClass('hover');
					if (this.recoverActive) {
						this.domElement.addClass('active');
					}
				}
				break;

			case 'mouseout':
				if (this.domElement && this.cssEffects) {
					this.recoverActive = false;
					if (this.domElement.hasClass('active')) {
						this.domElement.removeClass('active');
						this.recoverActive = true;
					}
					//this.domElement.removeClass('hover');
				}
				break;

			case 'mousedown':
				if (this.domElement && this.cssEffects) {
					this.domElement.addClass('active');
				}
				break;

			case 'mouseup':
				if (this.domElement && this.cssEffects) {
					this.domElement.removeClass('active');
					this.recoverActive = false;
				}
				break;
		} // switch eventName

		if (this.handlers[eventName]) {
			for (var idx = 0, len = this.handlers[eventName].length; idx < len; idx++) {
				var func = this.handlers[eventName][idx];

				if (typeof(func) == 'function') {
					// actual function reference
					func(this, args);
				}
				else if ((typeof(func) == 'object') && (func.length == 2)) {
					// PHP style object + method, i.e. [myObject, 'myMethod']
					func[0][ func[1] ](this, args);
				}
				else if (typeof(func) == 'string') {
					// name of function
					window[func](this, args);
				}
			} // foreach event handler defined
		} // user defined handler for event
	}

};

// For the Flash binding to work, ZeroClipboard_TableTools must be on the global
// object list
window.ZeroClipboard_TableTools = ZeroClipboard_TableTools;
//include TableTools.js
/* TableTools
 * 2009-2014 SpryMedia Ltd - datatables.net/license
 */

/*globals TableTools,ZeroClipboard_TableTools*/


(function($, window, document) {

/** 
 * TableTools provides flexible buttons and other tools for a DataTables enhanced table
 * @class TableTools
 * @constructor
 * @param {Object} oDT DataTables instance. When using DataTables 1.10 this can
 *   also be a jQuery collection, jQuery selector, table node, DataTables API
 *   instance or DataTables settings object.
 * @param {Object} oOpts TableTools options
 * @param {String} oOpts.sSwfPath ZeroClipboard SWF path
 * @param {String} oOpts.sRowSelect Row selection options - 'none', 'single', 'multi' or 'os'
 * @param {Function} oOpts.fnPreRowSelect Callback function just prior to row selection
 * @param {Function} oOpts.fnRowSelected Callback function just after row selection
 * @param {Function} oOpts.fnRowDeselected Callback function when row is deselected
 * @param {Array} oOpts.aButtons List of buttons to be used
 */
TableTools = function( oDT, oOpts )
{
	/* Santiy check that we are a new instance */
	if ( ! this instanceof TableTools )
	{
		alert( "Warning: TableTools must be initialised with the keyword 'new'" );
	}

	// In 1.10 we can use the API to get the settings object from a number of
	// sources
	var dtSettings = $.fn.dataTable.Api ?
		new $.fn.dataTable.Api( oDT ).settings()[0] :
		oDT.fnSettings();


	/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
	 * Public class variables
	 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

	/**
	 * @namespace Settings object which contains customisable information for TableTools instance
	 */
	this.s = {
		/**
		 * Store 'this' so the instance can be retrieved from the settings object
		 * @property that
		 * @type	 object
		 * @default  this
		 */
		"that": this,

		/** 
		 * DataTables settings objects
		 * @property dt
		 * @type	 object
		 * @default  <i>From the oDT init option</i>
		 */
		"dt": dtSettings,

		/**
		 * @namespace Print specific information
		 */
		"print": {
			/** 
			 * DataTables draw 'start' point before the printing display was shown
			 *  @property saveStart
			 *  @type	 int
			 *  @default  -1
			 */
			"saveStart": -1,

			/** 
			 * DataTables draw 'length' point before the printing display was shown
			 *  @property saveLength
			 *  @type	 int
			 *  @default  -1
			 */
			"saveLength": -1,

			/** 
			 * Page scrolling point before the printing display was shown so it can be restored
			 *  @property saveScroll
			 *  @type	 int
			 *  @default  -1
			 */
			"saveScroll": -1,

			/** 
			 * Wrapped function to end the print display (to maintain scope)
			 *  @property funcEnd
			 *  @type	 Function
			 *  @default  function () {}
			 */
			"funcEnd": function () {}
		},

		/**
		 * A unique ID is assigned to each button in each instance
		 * @property buttonCounter
		 *  @type	 int
		 * @default  0
		 */
		"buttonCounter": 0,

		/**
		 * @namespace Select rows specific information
		 */
		"select": {
			/**
			 * Select type - can be 'none', 'single' or 'multi'
			 * @property type
			 *  @type	 string
			 * @default  ""
			 */
			"type": "",

			/**
			 * Array of nodes which are currently selected
			 *  @property selected
			 *  @type	 array
			 *  @default  []
			 */
			"selected": [],

			/**
			 * Function to run before the selection can take place. Will cancel the select if the
			 * function returns false
			 *  @property preRowSelect
			 *  @type	 Function
			 *  @default  null
			 */
			"preRowSelect": null,

			/**
			 * Function to run when a row is selected
			 *  @property postSelected
			 *  @type	 Function
			 *  @default  null
			 */
			"postSelected": null,

			/**
			 * Function to run when a row is deselected
			 *  @property postDeselected
			 *  @type	 Function
			 *  @default  null
			 */
			"postDeselected": null,

			/**
			 * Indicate if all rows are selected (needed for server-side processing)
			 *  @property all
			 *  @type	 boolean
			 *  @default  false
			 */
			"all": false,

			/**
			 * Class name to add to selected TR nodes
			 *  @property selectedClass
			 *  @type	 String
			 *  @default  ""
			 */
			"selectedClass": ""
		},

		/**
		 * Store of the user input customisation object
		 *  @property custom
		 *  @type	 object
		 *  @default  {}
		 */
		"custom": {},

		/**
		 * SWF movie path
		 *  @property swfPath
		 *  @type	 string
		 *  @default  ""
		 */
		"swfPath": "",

		/**
		 * Default button set
		 *  @property buttonSet
		 *  @type	 array
		 *  @default  []
		 */
		"buttonSet": [],

		/**
		 * When there is more than one TableTools instance for a DataTable, there must be a 
		 * master which controls events (row selection etc)
		 *  @property master
		 *  @type	 boolean
		 *  @default  false
		 */
		"master": false,

		/**
		 * Tag names that are used for creating collections and buttons
		 *  @namesapce
		 */
		"tags": {}
	};


	/**
	 * @namespace Common and useful DOM elements for the class instance
	 */
	this.dom = {
		/**
		 * DIV element that is create and all TableTools buttons (and their children) put into
		 *  @property container
		 *  @type	 node
		 *  @default  null
		 */
		"container": null,

		/**
		 * The table node to which TableTools will be applied
		 *  @property table
		 *  @type	 node
		 *  @default  null
		 */
		"table": null,

		/**
		 * @namespace Nodes used for the print display
		 */
		"print": {
			/**
			 * Nodes which have been removed from the display by setting them to display none
			 *  @property hidden
			 *  @type	 array
			 *  @default  []
			 */
			"hidden": [],

			/**
			 * The information display saying telling the user about the print display
			 *  @property message
			 *  @type	 node
			 *  @default  null
			 */
			"message": null
	  },

		/**
		 * @namespace Nodes used for a collection display. This contains the currently used collection
		 */
		"collection": {
			/**
			 * The div wrapper containing the buttons in the collection (i.e. the menu)
			 *  @property collection
			 *  @type	 node
			 *  @default  null
			 */
			"collection": null,

			/**
			 * Background display to provide focus and capture events
			 *  @property background
			 *  @type	 node
			 *  @default  null
			 */
			"background": null
		}
	};

	/**
	 * @namespace Name space for the classes that this TableTools instance will use
	 * @extends TableTools.classes
	 */
	this.classes = $.extend( true, {}, TableTools.classes );
	if ( this.s.dt.bJUI )
	{
		$.extend( true, this.classes, TableTools.classes_themeroller );
	}


	/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
	 * Public class methods
	 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

	/**
	 * Retreieve the settings object from an instance
	 *  @method fnSettings
	 *  @returns {object} TableTools settings object
	 */
	this.fnSettings = function () {
		return this.s;
	};


	/* Constructor logic */
	if ( typeof oOpts == 'undefined' )
	{
		oOpts = {};
	}


	TableTools._aInstances.push( this );
	this._fnConstruct( oOpts );

	return this;
};



TableTools.prototype = {
	/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
	 * Public methods
	 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

	/**
	 * Retreieve the settings object from an instance
	 *  @returns {array} List of TR nodes which are currently selected
	 *  @param {boolean} [filtered=false] Get only selected rows which are  
	 *    available given the filtering applied to the table. By default
	 *    this is false -  i.e. all rows, regardless of filtering are 
	      selected.
	 */
	"fnGetSelected": function ( filtered )
	{
		var
			out = [],
			data = this.s.dt.aoData,
			displayed = this.s.dt.aiDisplay,
			i, iLen;

		if ( filtered )
		{
			// Only consider filtered rows
			for ( i=0, iLen=displayed.length ; i<iLen ; i++ )
			{
				if ( data[ displayed[i] ]._DTTT_selected )
				{
					out.push( data[ displayed[i] ].nTr );
				}
			}
		}
		else
		{
			// Use all rows
			for ( i=0, iLen=data.length ; i<iLen ; i++ )
			{
				if ( data[i]._DTTT_selected )
				{
					out.push( data[i].nTr );
				}
			}
		}

		return out;
	},


	/**
	 * Get the data source objects/arrays from DataTables for the selected rows (same as
	 * fnGetSelected followed by fnGetData on each row from the table)
	 *  @returns {array} Data from the TR nodes which are currently selected
	 */
	"fnGetSelectedData": function ()
	{
		var out = [];
		var data=this.s.dt.aoData;
		var i, iLen;

		for ( i=0, iLen=data.length ; i<iLen ; i++ )
		{
			if ( data[i]._DTTT_selected )
			{
				out.push( this.s.dt.oInstance.fnGetData(i) );
			}
		}

		return out;
	},


	/**
	 * Get the indexes of the selected rows
	 *  @returns {array} List of row indexes
	 *  @param {boolean} [filtered=false] Get only selected rows which are  
	 *    available given the filtering applied to the table. By default
	 *    this is false -  i.e. all rows, regardless of filtering are 
	      selected.
	 */
	"fnGetSelectedIndexes": function ( filtered )
	{
		var
			out = [],
			data = this.s.dt.aoData,
			displayed = this.s.dt.aiDisplay,
			i, iLen;

		if ( filtered )
		{
			// Only consider filtered rows
			for ( i=0, iLen=displayed.length ; i<iLen ; i++ )
			{
				if ( data[ displayed[i] ]._DTTT_selected )
				{
					out.push( displayed[i] );
				}
			}
		}
		else
		{
			// Use all rows
			for ( i=0, iLen=data.length ; i<iLen ; i++ )
			{
				if ( data[i]._DTTT_selected )
				{
					out.push( i );
				}
			}
		}

		return out;
	},


	/**
	 * Check to see if a current row is selected or not
	 *  @param {Node} n TR node to check if it is currently selected or not
	 *  @returns {Boolean} true if select, false otherwise
	 */
	"fnIsSelected": function ( n )
	{
		var pos = this.s.dt.oInstance.fnGetPosition( n );
		return (this.s.dt.aoData[pos]._DTTT_selected===true) ? true : false;
	},


	/**
	 * Select all rows in the table
	 *  @param {boolean} [filtered=false] Select only rows which are available 
	 *    given the filtering applied to the table. By default this is false - 
	 *    i.e. all rows, regardless of filtering are selected.
	 */
	"fnSelectAll": function ( filtered )
	{
		this._fnRowSelect( filtered ?
			this.s.dt.aiDisplay :
			this.s.dt.aoData
		);
	},


	/**
	 * Deselect all rows in the table
	 *  @param {boolean} [filtered=false] Deselect only rows which are available 
	 *    given the filtering applied to the table. By default this is false - 
	 *    i.e. all rows, regardless of filtering are deselected.
	 */
	"fnSelectNone": function ( filtered )
	{
		this._fnRowDeselect( this.fnGetSelectedIndexes(filtered) );
	},


	/**
	 * Select row(s)
	 *  @param {node|object|array} n The row(s) to select. Can be a single DOM
	 *    TR node, an array of TR nodes or a jQuery object.
	 */
	"fnSelect": function ( n )
	{
		if ( this.s.select.type == "single" )
		{
			this.fnSelectNone();
			this._fnRowSelect( n );
		}
		else
		{
			this._fnRowSelect( n );
		}
	},


	/**
	 * Deselect row(s)
	 *  @param {node|object|array} n The row(s) to deselect. Can be a single DOM
	 *    TR node, an array of TR nodes or a jQuery object.
	 */
	"fnDeselect": function ( n )
	{
		this._fnRowDeselect( n );
	},


	/**
	 * Get the title of the document - useful for file names. The title is retrieved from either
	 * the configuration object's 'title' parameter, or the HTML document title
	 *  @param   {Object} oConfig Button configuration object
	 *  @returns {String} Button title
	 */
	"fnGetTitle": function( oConfig )
	{
		var sTitle = "";
		if ( typeof oConfig.sTitle != 'undefined' && oConfig.sTitle !== "" ) {
			sTitle = oConfig.sTitle;
		} else {
			var anTitle = document.getElementsByTagName('title');
			if ( anTitle.length > 0 )
			{
				sTitle = anTitle[0].innerHTML;
			}
		}

		/* Strip characters which the OS will object to - checking for UTF8 support in the scripting
		 * engine
		 */
		if ( "\u00A1".toString().length < 4 ) {
			return sTitle.replace(/[^a-zA-Z0-9_\u00A1-\uFFFF\.,\-_ !\(\)]/g, "");
		} else {
			return sTitle.replace(/[^a-zA-Z0-9_\.,\-_ !\(\)]/g, "");
		}
	},


	/**
	 * Calculate a unity array with the column width by proportion for a set of columns to be
	 * included for a button. This is particularly useful for PDF creation, where we can use the
	 * column widths calculated by the browser to size the columns in the PDF.
	 *  @param   {Object} oConfig Button configuration object
	 *  @returns {Array} Unity array of column ratios
	 */
	"fnCalcColRatios": function ( oConfig )
	{
		var
			aoCols = this.s.dt.aoColumns,
			aColumnsInc = this._fnColumnTargets( oConfig.mColumns ),
			aColWidths = [],
			iWidth = 0, iTotal = 0, i, iLen;

		for ( i=0, iLen=aColumnsInc.length ; i<iLen ; i++ )
		{
			if ( aColumnsInc[i] )
			{
				iWidth = aoCols[i].nTh.offsetWidth;
				iTotal += iWidth;
				aColWidths.push( iWidth );
			}
		}

		for ( i=0, iLen=aColWidths.length ; i<iLen ; i++ )
		{
			aColWidths[i] = aColWidths[i] / iTotal;
		}

		return aColWidths.join('\t');
	},


	/**
	 * Get the information contained in a table as a string
	 *  @param   {Object} oConfig Button configuration object
	 *  @returns {String} Table data as a string
	 */
	"fnGetTableData": function ( oConfig )
	{
		/* In future this could be used to get data from a plain HTML source as well as DataTables */
		if ( this.s.dt )
		{
			return this._fnGetDataTablesData( oConfig );
		}
	},


	/**
	 * Pass text to a flash button instance, which will be used on the button's click handler
	 *  @param   {Object} clip Flash button object
	 *  @param   {String} text Text to set
	 */
	"fnSetText": function ( clip, text )
	{
		this._fnFlashSetText( clip, text );
	},


	/**
	 * Resize the flash elements of the buttons attached to this TableTools instance - this is
	 * useful for when initialising TableTools when it is hidden (display:none) since sizes can't
	 * be calculated at that time.
	 */
	"fnResizeButtons": function ()
	{
		for ( var cli in ZeroClipboard_TableTools.clients )
		{
			if ( cli )
			{
				var client = ZeroClipboard_TableTools.clients[cli];
				if ( typeof client.domElement != 'undefined' &&
					 client.domElement.parentNode )
				{
					client.positionElement();
				}
			}
		}
	},


	/**
	 * Check to see if any of the ZeroClipboard client's attached need to be resized
	 */
	"fnResizeRequired": function ()
	{
		for ( var cli in ZeroClipboard_TableTools.clients )
		{
			if ( cli )
			{
				var client = ZeroClipboard_TableTools.clients[cli];
				if ( typeof client.domElement != 'undefined' &&
					 client.domElement.parentNode == this.dom.container &&
					 client.sized === false )
				{
					return true;
				}
			}
		}
		return false;
	},


	/**
	 * Programmatically enable or disable the print view
	 *  @param {boolean} [bView=true] Show the print view if true or not given. If false, then
	 *    terminate the print view and return to normal.
	 *  @param {object} [oConfig={}] Configuration for the print view
	 *  @param {boolean} [oConfig.bShowAll=false] Show all rows in the table if true
	 *  @param {string} [oConfig.sInfo] Information message, displayed as an overlay to the
	 *    user to let them know what the print view is.
	 *  @param {string} [oConfig.sMessage] HTML string to show at the top of the document - will
	 *    be included in the printed document.
	 */
	"fnPrint": function ( bView, oConfig )
	{
		if ( oConfig === undefined )
		{
			oConfig = {};
		}

		if ( bView === undefined || bView )
		{
			this._fnPrintStart( oConfig );
		}
		else
		{
			this._fnPrintEnd();
		}
	},


	/**
	 * Show a message to the end user which is nicely styled
	 *  @param {string} message The HTML string to show to the user
	 *  @param {int} time The duration the message is to be shown on screen for (mS)
	 */
	"fnInfo": function ( message, time ) {
		var info = $('<div/>')
			.addClass( this.classes.print.info )
			.html( message )
			.appendTo( 'body' );

		setTimeout( function() {
			info.fadeOut( "normal", function() {
				info.remove();
			} );
		}, time );
	},



	/**
	 * Get the container element of the instance for attaching to the DOM
	 *   @returns {node} DOM node
	 */
	"fnContainer": function () {
		return this.dom.container;
	},



	/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
	 * Private methods (they are of course public in JS, but recommended as private)
	 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

	/**
	 * Constructor logic
	 *  @method  _fnConstruct
	 *  @param   {Object} oOpts Same as TableTools constructor
	 *  @returns void
	 *  @private 
	 */
	"_fnConstruct": function ( oOpts )
	{
		var that = this;

		this._fnCustomiseSettings( oOpts );

		/* Container element */
		this.dom.container = document.createElement( this.s.tags.container );
		this.dom.container.className = this.classes.container;

		/* Row selection config */
		if ( this.s.select.type != 'none' )
		{
			this._fnRowSelectConfig();
		}

		/* Buttons */
		this._fnButtonDefinations( this.s.buttonSet, this.dom.container );

		/* Destructor */
		this.s.dt.aoDestroyCallback.push( {
			"sName": "TableTools",
			"fn": function () {
				$(that.s.dt.nTBody).off( 'click.DTTT_Select', 'tr' );
				$(that.dom.container).empty();

				// Remove the instance
				var idx = $.inArray( that, TableTools._aInstances );
				if ( idx !== -1 ) {
					TableTools._aInstances.splice( idx, 1 );
				}
			}
		} );
	},


	/**
	 * Take the user defined settings and the default settings and combine them.
	 *  @method  _fnCustomiseSettings
	 *  @param   {Object} oOpts Same as TableTools constructor
	 *  @returns void
	 *  @private 
	 */
	"_fnCustomiseSettings": function ( oOpts )
	{
		/* Is this the master control instance or not? */
		if ( typeof this.s.dt._TableToolsInit == 'undefined' )
		{
			this.s.master = true;
			this.s.dt._TableToolsInit = true;
		}

		/* We can use the table node from comparisons to group controls */
		this.dom.table = this.s.dt.nTable;

		/* Clone the defaults and then the user options */
		this.s.custom = $.extend( {}, TableTools.DEFAULTS, oOpts );

		/* Flash file location */
		this.s.swfPath = this.s.custom.sSwfPath;
		if ( typeof ZeroClipboard_TableTools != 'undefined' )
		{
			ZeroClipboard_TableTools.moviePath = this.s.swfPath;
		}

		/* Table row selecting */
		this.s.select.type = this.s.custom.sRowSelect;
		this.s.select.preRowSelect = this.s.custom.fnPreRowSelect;
		this.s.select.postSelected = this.s.custom.fnRowSelected;
		this.s.select.postDeselected = this.s.custom.fnRowDeselected;

		// Backwards compatibility - allow the user to specify a custom class in the initialiser
		if ( this.s.custom.sSelectedClass )
		{
			this.classes.select.row = this.s.custom.sSelectedClass;
		}

		this.s.tags = this.s.custom.oTags;

		/* Button set */
		this.s.buttonSet = this.s.custom.aButtons;
	},


	/**
	 * Take the user input arrays and expand them to be fully defined, and then add them to a given
	 * DOM element
	 *  @method  _fnButtonDefinations
	 *  @param {array} buttonSet Set of user defined buttons
	 *  @param {node} wrapper Node to add the created buttons to
	 *  @returns void
	 *  @private 
	 */
	"_fnButtonDefinations": function ( buttonSet, wrapper )
	{
		var buttonDef;

		for ( var i=0, iLen=buttonSet.length ; i<iLen ; i++ )
		{
			if ( typeof buttonSet[i] == "string" )
			{
				if ( typeof TableTools.BUTTONS[ buttonSet[i] ] == 'undefined' )
				{
					alert( "TableTools: Warning - unknown button type: "+buttonSet[i] );
					continue;
				}
				buttonDef = $.extend( {}, TableTools.BUTTONS[ buttonSet[i] ], true );
			}
			else
			{
				if ( typeof TableTools.BUTTONS[ buttonSet[i].sExtends ] == 'undefined' )
				{
					alert( "TableTools: Warning - unknown button type: "+buttonSet[i].sExtends );
					continue;
				}
				var o = $.extend( {}, TableTools.BUTTONS[ buttonSet[i].sExtends ], true );
				buttonDef = $.extend( o, buttonSet[i], true );
			}

			var button = this._fnCreateButton(
				buttonDef,
				$(wrapper).hasClass(this.classes.collection.container)
			);

			if ( button ) {
				wrapper.appendChild( button );
			}
		}
	},


	/**
	 * Create and configure a TableTools button
	 *  @method  _fnCreateButton
	 *  @param   {Object} oConfig Button configuration object
	 *  @returns {Node} Button element
	 *  @private 
	 */
	"_fnCreateButton": function ( oConfig, bCollectionButton )
	{
	  var nButton = this._fnButtonBase( oConfig, bCollectionButton );

		if ( oConfig.sAction.match(/flash/) )
		{
			if ( ! this._fnHasFlash() ) {
				return false;
			}

			this._fnFlashConfig( nButton, oConfig );
		}
		else if ( oConfig.sAction == "text" )
		{
			this._fnTextConfig( nButton, oConfig );
		}
		else if ( oConfig.sAction == "div" )
		{
			this._fnTextConfig( nButton, oConfig );
		}
		else if ( oConfig.sAction == "collection" )
		{
			this._fnTextConfig( nButton, oConfig );
			this._fnCollectionConfig( nButton, oConfig );
		}

		return nButton;
	},


	/**
	 * Create the DOM needed for the button and apply some base properties. All buttons start here
	 *  @method  _fnButtonBase
	 *  @param   {o} oConfig Button configuration object
	 *  @returns {Node} DIV element for the button
	 *  @private
	 */
	"_fnButtonBase": function ( o, bCollectionButton )
	{
		var sTag, sLiner, sClass;

		if ( bCollectionButton )
		{
			sTag = o.sTag && o.sTag !== "default" ? o.sTag : this.s.tags.collection.button;
			sLiner = o.sLinerTag && o.sLinerTag !== "default" ? o.sLiner : this.s.tags.collection.liner;
			sClass = this.classes.collection.buttons.normal;
		}
		else
		{
			sTag = o.sTag && o.sTag !== "default" ? o.sTag : this.s.tags.button;
			sLiner = o.sLinerTag && o.sLinerTag !== "default" ? o.sLiner : this.s.tags.liner;
			sClass = this.classes.buttons.normal;
		}

		var
		  nButton = document.createElement( sTag ),
		  nSpan = document.createElement( sLiner ),
		  masterS = this._fnGetMasterSettings();

		nButton.className = sClass+" "+o.sButtonClass;
		nButton.setAttribute('id', "ToolTables_"+this.s.dt.sInstance+"_"+masterS.buttonCounter );
		nButton.appendChild( nSpan );
		nSpan.innerHTML = o.sButtonText;

		masterS.buttonCounter++;

		return nButton;
	},


	/**
	 * Get the settings object for the master instance. When more than one TableTools instance is
	 * assigned to a DataTable, only one of them can be the 'master' (for the select rows). As such,
	 * we will typically want to interact with that master for global properties.
	 *  @method  _fnGetMasterSettings
	 *  @returns {Object} TableTools settings object
	 *  @private 
	 */
	"_fnGetMasterSettings": function ()
	{
		if ( this.s.master )
		{
			return this.s;
		}
		else
		{
			/* Look for the master which has the same DT as this one */
			var instances = TableTools._aInstances;
			for ( var i=0, iLen=instances.length ; i<iLen ; i++ )
			{
				if ( this.dom.table == instances[i].s.dt.nTable )
				{
					return instances[i].s;
				}
			}
		}
	},



	/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
	 * Button collection functions
	 */

	/**
	 * Create a collection button, when activated will present a drop down list of other buttons
	 *  @param   {Node} nButton Button to use for the collection activation
	 *  @param   {Object} oConfig Button configuration object
	 *  @returns void
	 *  @private
	 */
	"_fnCollectionConfig": function ( nButton, oConfig )
	{
		var nHidden = document.createElement( this.s.tags.collection.container );
		nHidden.style.display = "none";
		nHidden.className = this.classes.collection.container;
		oConfig._collection = nHidden;
		document.body.appendChild( nHidden );

		this._fnButtonDefinations( oConfig.aButtons, nHidden );
	},


	/**
	 * Show a button collection
	 *  @param   {Node} nButton Button to use for the collection
	 *  @param   {Object} oConfig Button configuration object
	 *  @returns void
	 *  @private
	 */
	"_fnCollectionShow": function ( nButton, oConfig )
	{
		var
			that = this,
			oPos = $(nButton).offset(),
			nHidden = oConfig._collection,
			iDivX = oPos.left,
			iDivY = oPos.top + $(nButton).outerHeight(),
			iWinHeight = $(window).height(), iDocHeight = $(document).height(),
			iWinWidth = $(window).width(), iDocWidth = $(document).width();

		nHidden.style.position = "absolute";
		nHidden.style.left = iDivX+"px";
		nHidden.style.top = iDivY+"px";
		nHidden.style.display = "block";
		$(nHidden).css('opacity',0);

		var nBackground = document.createElement('div');
		nBackground.style.position = "absolute";
		nBackground.style.left = "0px";
		nBackground.style.top = "0px";
		nBackground.style.height = ((iWinHeight>iDocHeight)? iWinHeight : iDocHeight) +"px";
		nBackground.style.width = ((iWinWidth>iDocWidth)? iWinWidth : iDocWidth) +"px";
		nBackground.className = this.classes.collection.background;
		$(nBackground).css('opacity',0);

		document.body.appendChild( nBackground );
		document.body.appendChild( nHidden );

		/* Visual corrections to try and keep the collection visible */
		var iDivWidth = $(nHidden).outerWidth();
		var iDivHeight = $(nHidden).outerHeight();

		if ( iDivX + iDivWidth > iDocWidth )
		{
			nHidden.style.left = (iDocWidth-iDivWidth)+"px";
		}

		if ( iDivY + iDivHeight > iDocHeight )
		{
			nHidden.style.top = (iDivY-iDivHeight-$(nButton).outerHeight())+"px";
		}

		this.dom.collection.collection = nHidden;
		this.dom.collection.background = nBackground;

		/* This results in a very small delay for the end user but it allows the animation to be
		 * much smoother. If you don't want the animation, then the setTimeout can be removed
		 */
		setTimeout( function () {
			$(nHidden).animate({"opacity": 1}, 500);
			$(nBackground).animate({"opacity": 0.25}, 500);
		}, 10 );

		/* Resize the buttons to the Flash contents fit */
		this.fnResizeButtons();

		/* Event handler to remove the collection display */
		$(nBackground).click( function () {
			that._fnCollectionHide.call( that, null, null );
		} );
	},


	/**
	 * Hide a button collection
	 *  @param   {Node} nButton Button to use for the collection
	 *  @param   {Object} oConfig Button configuration object
	 *  @returns void
	 *  @private
	 */
	"_fnCollectionHide": function ( nButton, oConfig )
	{
		if ( oConfig !== null && oConfig.sExtends == 'collection' )
		{
			return;
		}

		if ( this.dom.collection.collection !== null )
		{
			$(this.dom.collection.collection).animate({"opacity": 0}, 500, function (e) {
				this.style.display = "none";
			} );

			$(this.dom.collection.background).animate({"opacity": 0}, 500, function (e) {
				this.parentNode.removeChild( this );
			} );

			this.dom.collection.collection = null;
			this.dom.collection.background = null;
		}
	},



	/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
	 * Row selection functions
	 */

	/**
	 * Add event handlers to a table to allow for row selection
	 *  @method  _fnRowSelectConfig
	 *  @returns void
	 *  @private 
	 */
	"_fnRowSelectConfig": function ()
	{
		if ( this.s.master )
		{
			var
				that = this,
				i, iLen,
				dt = this.s.dt,
				aoOpenRows = this.s.dt.aoOpenRows;

			$(dt.nTable).addClass( this.classes.select.table );

			// When using OS style selection, we want to cancel the shift text
			// selection, but only when the shift key is used (so you can
			// actually still select text in the table)
			if ( this.s.select.type === 'os' ) {
				$(dt.nTBody).on( 'mousedown.DTTT_Select', 'tr', function(e) {
					if ( e.shiftKey ) {

						$(dt.nTBody)
							.css( '-moz-user-select', 'none' )
							.one('selectstart.DTTT_Select', 'tr', function () {
								return false;
							} );
					}
				} );

				$(dt.nTBody).on( 'mouseup.DTTT_Select', 'tr', function(e) {
					$(dt.nTBody).css( '-moz-user-select', '' );
				} );
			}

			// Row selection
			$(dt.nTBody).on( 'click.DTTT_Select', this.s.custom.sRowSelector, function(e) {
				var row = this.nodeName.toLowerCase() === 'tr' ?
					this :
					$(this).parents('tr')[0];

				var select = that.s.select;
				var pos = that.s.dt.oInstance.fnGetPosition( row );

				/* Sub-table must be ignored (odd that the selector won't do this with >) */
				if ( row.parentNode != dt.nTBody ) {
					return;
				}

				/* Check that we are actually working with a DataTables controlled row */
				if ( dt.oInstance.fnGetData(row) === null ) {
				    return;
				}

				// Shift click, ctrl click and simple click handling to make
				// row selection a lot like a file system in desktop OSs
				if ( select.type == 'os' ) {
					if ( e.ctrlKey || e.metaKey ) {
						// Add or remove from the selection
						if ( that.fnIsSelected( row ) ) {
							that._fnRowDeselect( row, e );
						}
						else {
							that._fnRowSelect( row, e );
						}
					}
					else if ( e.shiftKey ) {
						// Add a range of rows, from the last selected row to
						// this one
						var rowIdxs = that.s.dt.aiDisplay.slice(); // visible rows
						var idx1 = $.inArray( select.lastRow, rowIdxs );
						var idx2 = $.inArray( pos, rowIdxs );

						if ( that.fnGetSelected().length === 0 || idx1 === -1 ) {
							// select from top to here - slightly odd, but both
							// Windows and Mac OS do this
							rowIdxs.splice( $.inArray( pos, rowIdxs )+1, rowIdxs.length );
						}
						else {
							// reverse so we can shift click 'up' as well as down
							if ( idx1 > idx2 ) {
								var tmp = idx2;
								idx2 = idx1;
								idx1 = tmp;
							}

							rowIdxs.splice( idx2+1, rowIdxs.length );
							rowIdxs.splice( 0, idx1 );
						}

						if ( ! that.fnIsSelected( row ) ) {
							// Select range
							that._fnRowSelect( rowIdxs, e );
						}
						else {
							// Deselect range - need to keep the clicked on row selected
							rowIdxs.splice( $.inArray( pos, rowIdxs ), 1 );
							that._fnRowDeselect( rowIdxs, e );
						}
					}
					else {
						// No cmd or shift click. Deselect current if selected,
						// or select this row only
						if ( that.fnIsSelected( row ) && that.fnGetSelected().length === 1 ) {
							that._fnRowDeselect( row, e );
						}
						else {
							that.fnSelectNone();
							that._fnRowSelect( row, e );
						}
					}
				}
				else if ( that.fnIsSelected( row ) ) {
					that._fnRowDeselect( row, e );
				}
				else if ( select.type == "single" ) {
					that.fnSelectNone();
					that._fnRowSelect( row, e );
				}
				else if ( select.type == "multi" ) {
					that._fnRowSelect( row, e );
				}

				select.lastRow = pos;
			} );//.on('selectstart', function () { return false; } );

			// Bind a listener to the DataTable for when new rows are created.
			// This allows rows to be visually selected when they should be and
			// deferred rendering is used.
			dt.oApi._fnCallbackReg( dt, 'aoRowCreatedCallback', function (tr, data, index) {
				if ( dt.aoData[index]._DTTT_selected ) {
					$(tr).addClass( that.classes.select.row );
				}
			}, 'TableTools-SelectAll' );
		}
	},

	/**
	 * Select rows
	 *  @param   {*} src Rows to select - see _fnSelectData for a description of valid inputs
	 *  @private 
	 */
	"_fnRowSelect": function ( src, e )
	{
		var
			that = this,
			data = this._fnSelectData( src ),
			firstTr = data.length===0 ? null : data[0].nTr,
			anSelected = [],
			i, len;

		// Get all the rows that will be selected
		for ( i=0, len=data.length ; i<len ; i++ )
		{
			if ( data[i].nTr )
			{
				anSelected.push( data[i].nTr );
			}
		}

		// User defined pre-selection function
		if ( this.s.select.preRowSelect !== null && !this.s.select.preRowSelect.call(this, e, anSelected, true) )
		{
			return;
		}

		// Mark them as selected
		for ( i=0, len=data.length ; i<len ; i++ )
		{
			data[i]._DTTT_selected = true;

			if ( data[i].nTr )
			{
				$(data[i].nTr).addClass( that.classes.select.row );
			}
		}

		// Post-selection function
		if ( this.s.select.postSelected !== null )
		{
			this.s.select.postSelected.call( this, anSelected );
		}

		TableTools._fnEventDispatch( this, 'select', anSelected, true );
	},

	/**
	 * Deselect rows
	 *  @param   {*} src Rows to deselect - see _fnSelectData for a description of valid inputs
	 *  @private 
	 */
	"_fnRowDeselect": function ( src, e )
	{
		var
			that = this,
			data = this._fnSelectData( src ),
			firstTr = data.length===0 ? null : data[0].nTr,
			anDeselectedTrs = [],
			i, len;

		// Get all the rows that will be deselected
		for ( i=0, len=data.length ; i<len ; i++ )
		{
			if ( data[i].nTr )
			{
				anDeselectedTrs.push( data[i].nTr );
			}
		}

		// User defined pre-selection function
		if ( this.s.select.preRowSelect !== null && !this.s.select.preRowSelect.call(this, e, anDeselectedTrs, false) )
		{
			return;
		}

		// Mark them as deselected
		for ( i=0, len=data.length ; i<len ; i++ )
		{
			data[i]._DTTT_selected = false;

			if ( data[i].nTr )
			{
				$(data[i].nTr).removeClass( that.classes.select.row );
			}
		}

		// Post-deselection function
		if ( this.s.select.postDeselected !== null )
		{
			this.s.select.postDeselected.call( this, anDeselectedTrs );
		}

		TableTools._fnEventDispatch( this, 'select', anDeselectedTrs, false );
	},

	/**
	 * Take a data source for row selection and convert it into aoData points for the DT
	 *   @param {*} src Can be a single DOM TR node, an array of TR nodes (including a
	 *     a jQuery object), a single aoData point from DataTables, an array of aoData
	 *     points or an array of aoData indexes
	 *   @returns {array} An array of aoData points
	 */
	"_fnSelectData": function ( src )
	{
		var out = [], pos, i, iLen;

		if ( src.nodeName )
		{
			// Single node
			pos = this.s.dt.oInstance.fnGetPosition( src );
			out.push( this.s.dt.aoData[pos] );
		}
		else if ( typeof src.length !== 'undefined' )
		{
			// jQuery object or an array of nodes, or aoData points
			for ( i=0, iLen=src.length ; i<iLen ; i++ )
			{
				if ( src[i].nodeName )
				{
					pos = this.s.dt.oInstance.fnGetPosition( src[i] );
					out.push( this.s.dt.aoData[pos] );
				}
				else if ( typeof src[i] === 'number' )
				{
					out.push( this.s.dt.aoData[ src[i] ] );
				}
				else
				{
					out.push( src[i] );
				}
			}

			return out;
		}
		else
		{
			// A single aoData point
			out.push( src );
		}

		return out;
	},


	/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
	 * Text button functions
	 */

	/**
	 * Configure a text based button for interaction events
	 *  @method  _fnTextConfig
	 *  @param   {Node} nButton Button element which is being considered
	 *  @param   {Object} oConfig Button configuration object
	 *  @returns void
	 *  @private 
	 */
	"_fnTextConfig": function ( nButton, oConfig )
	{
		var that = this;

		if ( oConfig.fnInit !== null )
		{
			oConfig.fnInit.call( this, nButton, oConfig );
		}

		if ( oConfig.sToolTip !== "" )
		{
			nButton.title = oConfig.sToolTip;
		}

		$(nButton).hover( function () {
			if ( oConfig.fnMouseover !== null )
			{
				oConfig.fnMouseover.call( this, nButton, oConfig, null );
			}
		}, function () {
			if ( oConfig.fnMouseout !== null )
			{
				oConfig.fnMouseout.call( this, nButton, oConfig, null );
			}
		} );

		if ( oConfig.fnSelect !== null )
		{
			TableTools._fnEventListen( this, 'select', function (n) {
				oConfig.fnSelect.call( that, nButton, oConfig, n );
			} );
		}

		$(nButton).click( function (e) {
			//e.preventDefault();

			if ( oConfig.fnClick !== null )
			{
				oConfig.fnClick.call( that, nButton, oConfig, null, e );
			}

			/* Provide a complete function to match the behaviour of the flash elements */
			if ( oConfig.fnComplete !== null )
			{
				oConfig.fnComplete.call( that, nButton, oConfig, null, null );
			}

			that._fnCollectionHide( nButton, oConfig );
		} );
	},



	/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
	 * Flash button functions
	 */
	
	/**
	 * Check if the Flash plug-in is available
	 *  @method  _fnHasFlash
	 *  @returns {boolean} `true` if Flash available, `false` otherwise
	 *  @private 
	 */
	"_fnHasFlash": function ()
	{
		try {
			var fo = new ActiveXObject('ShockwaveFlash.ShockwaveFlash');
			if (fo) {
				return true;
			}
		}
		catch (e) {
			if (
				navigator.mimeTypes &&
				navigator.mimeTypes['application/x-shockwave-flash'] !== undefined &&
				navigator.mimeTypes['application/x-shockwave-flash'].enabledPlugin
			) {
				return true;
			}
		}

		return false;
	},


	/**
	 * Configure a flash based button for interaction events
	 *  @method  _fnFlashConfig
	 *  @param   {Node} nButton Button element which is being considered
	 *  @param   {o} oConfig Button configuration object
	 *  @returns void
	 *  @private 
	 */
	"_fnFlashConfig": function ( nButton, oConfig )
	{
		var that = this;
		var flash = new ZeroClipboard_TableTools.Client();

		if ( oConfig.fnInit !== null )
		{
			oConfig.fnInit.call( this, nButton, oConfig );
		}

		flash.setHandCursor( true );

		if ( oConfig.sAction == "flash_save" )
		{
			flash.setAction( 'save' );
			flash.setCharSet( (oConfig.sCharSet=="utf16le") ? 'UTF16LE' : 'UTF8' );
			flash.setBomInc( oConfig.bBomInc );
			flash.setFileName( oConfig.sFileName.replace('*', this.fnGetTitle(oConfig)) );
		}
		else if ( oConfig.sAction == "flash_pdf" )
		{
			flash.setAction( 'pdf' );
			flash.setFileName( oConfig.sFileName.replace('*', this.fnGetTitle(oConfig)) );
		}
		else
		{
			flash.setAction( 'copy' );
		}

		flash.addEventListener('mouseOver', function(client) {
			if ( oConfig.fnMouseover !== null )
			{
				oConfig.fnMouseover.call( that, nButton, oConfig, flash );
			}
		} );

		flash.addEventListener('mouseOut', function(client) {
			if ( oConfig.fnMouseout !== null )
			{
				oConfig.fnMouseout.call( that, nButton, oConfig, flash );
			}
		} );

		flash.addEventListener('mouseDown', function(client) {
			if ( oConfig.fnClick !== null )
			{
				oConfig.fnClick.call( that, nButton, oConfig, flash );
			}
		} );

		flash.addEventListener('complete', function (client, text) {
			if ( oConfig.fnComplete !== null )
			{
				oConfig.fnComplete.call( that, nButton, oConfig, flash, text );
			}
			that._fnCollectionHide( nButton, oConfig );
		} );

		this._fnFlashGlue( flash, nButton, oConfig.sToolTip );
	},


	/**
	 * Wait until the id is in the DOM before we "glue" the swf. Note that this function will call
	 * itself (using setTimeout) until it completes successfully
	 *  @method  _fnFlashGlue
	 *  @param   {Object} clip Zero clipboard object
	 *  @param   {Node} node node to glue swf to
	 *  @param   {String} text title of the flash movie
	 *  @returns void
	 *  @private 
	 */
	"_fnFlashGlue": function ( flash, node, text )
	{
		var that = this;
		var id = node.getAttribute('id');

		if ( document.getElementById(id) )
		{
			flash.glue( node, text );
		}
		else
		{
			setTimeout( function () {
				that._fnFlashGlue( flash, node, text );
			}, 100 );
		}
	},


	/**
	 * Set the text for the flash clip to deal with
	 * 
	 * This function is required for large information sets. There is a limit on the 
	 * amount of data that can be transferred between Javascript and Flash in a single call, so
	 * we use this method to build up the text in Flash by sending over chunks. It is estimated
	 * that the data limit is around 64k, although it is undocumented, and appears to be different
	 * between different flash versions. We chunk at 8KiB.
	 *  @method  _fnFlashSetText
	 *  @param   {Object} clip the ZeroClipboard object
	 *  @param   {String} sData the data to be set
	 *  @returns void
	 *  @private 
	 */
	"_fnFlashSetText": function ( clip, sData )
	{
		var asData = this._fnChunkData( sData, 8192 );

		clip.clearText();
		for ( var i=0, iLen=asData.length ; i<iLen ; i++ )
		{
			clip.appendText( asData[i] );
		}
	},



	/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
	 * Data retrieval functions
	 */

	/**
	 * Convert the mixed columns variable into a boolean array the same size as the columns, which
	 * indicates which columns we want to include
	 *  @method  _fnColumnTargets
	 *  @param   {String|Array} mColumns The columns to be included in data retrieval. If a string
	 *			 then it can take the value of "visible" or "hidden" (to include all visible or
	 *			 hidden columns respectively). Or an array of column indexes
	 *  @returns {Array} A boolean array the length of the columns of the table, which each value
	 *			 indicating if the column is to be included or not
	 *  @private 
	 */
	"_fnColumnTargets": function ( mColumns )
	{
		var aColumns = [];
		var dt = this.s.dt;
		var i, iLen;

		if ( typeof mColumns == "object" )
		{
			for ( i=0, iLen=dt.aoColumns.length ; i<iLen ; i++ )
			{
				aColumns.push( false );
			}

			for ( i=0, iLen=mColumns.length ; i<iLen ; i++ )
			{
				aColumns[ mColumns[i] ] = true;
			}
		}
		else if ( mColumns == "visible" )
		{
			for ( i=0, iLen=dt.aoColumns.length ; i<iLen ; i++ )
			{
				aColumns.push( dt.aoColumns[i].bVisible ? true : false );
			}
		}
		else if ( mColumns == "hidden" )
		{
			for ( i=0, iLen=dt.aoColumns.length ; i<iLen ; i++ )
			{
				aColumns.push( dt.aoColumns[i].bVisible ? false : true );
			}
		}
		else if ( mColumns == "sortable" )
		{
			for ( i=0, iLen=dt.aoColumns.length ; i<iLen ; i++ )
			{
				aColumns.push( dt.aoColumns[i].bSortable ? true : false );
			}
		}
		else /* all */
		{
			for ( i=0, iLen=dt.aoColumns.length ; i<iLen ; i++ )
			{
				aColumns.push( true );
			}
		}

		return aColumns;
	},


	/**
	 * New line character(s) depend on the platforms
	 *  @method  method
	 *  @param   {Object} oConfig Button configuration object - only interested in oConfig.sNewLine
	 *  @returns {String} Newline character
	 */
	"_fnNewline": function ( oConfig )
	{
		if ( oConfig.sNewLine == "auto" )
		{
			return navigator.userAgent.match(/Windows/) ? "\r\n" : "\n";
		}
		else
		{
			return oConfig.sNewLine;
		}
	},


	/**
	 * Get data from DataTables' internals and format it for output
	 *  @method  _fnGetDataTablesData
	 *  @param   {Object} oConfig Button configuration object
	 *  @param   {String} oConfig.sFieldBoundary Field boundary for the data cells in the string
	 *  @param   {String} oConfig.sFieldSeperator Field separator for the data cells
	 *  @param   {String} oConfig.sNewline New line options
	 *  @param   {Mixed} oConfig.mColumns Which columns should be included in the output
	 *  @param   {Boolean} oConfig.bHeader Include the header
	 *  @param   {Boolean} oConfig.bFooter Include the footer
	 *  @param   {Boolean} oConfig.bSelectedOnly Include only the selected rows in the output
	 *  @returns {String} Concatenated string of data
	 *  @private 
	 */
	"_fnGetDataTablesData": function ( oConfig )
	{
		var i, iLen, j, jLen;
		var aRow, aData=[], sLoopData='', arr;
		var dt = this.s.dt, tr, child;
		var regex = new RegExp(oConfig.sFieldBoundary, "g"); /* Do it here for speed */
		var aColumnsInc = this._fnColumnTargets( oConfig.mColumns );
		var bSelectedOnly = (typeof oConfig.bSelectedOnly != 'undefined') ? oConfig.bSelectedOnly : false;

		/*
		 * Header
		 */
		if ( oConfig.bHeader )
		{
			aRow = [];

			for ( i=0, iLen=dt.aoColumns.length ; i<iLen ; i++ )
			{
				if ( aColumnsInc[i] )
				{
					sLoopData = dt.aoColumns[i].sTitle.replace(/\n/g," ").replace( /<.*?>/g, "" ).replace(/^\s+|\s+$/g,"");
					sLoopData = this._fnHtmlDecode( sLoopData );

					aRow.push( this._fnBoundData( sLoopData, oConfig.sFieldBoundary, regex ) );
				}
			}

			aData.push( aRow.join(oConfig.sFieldSeperator) );
		}

		/*
		 * Body
		 */
		var aSelected = this.fnGetSelected();
		bSelectedOnly = this.s.select.type !== "none" && bSelectedOnly && aSelected.length !== 0;

		var api = $.fn.dataTable.Api;
		var aDataIndex = api ?
			new api( dt ).rows( oConfig.oSelectorOpts ).indexes().flatten().toArray() :
			dt.oInstance
				.$('tr', oConfig.oSelectorOpts)
				.map( function (id, row) {
					// If "selected only", then ensure that the row is in the selected list
					return bSelectedOnly && $.inArray( row, aSelected ) === -1 ?
						null :
						dt.oInstance.fnGetPosition( row );
				} )
				.get();

		for ( j=0, jLen=aDataIndex.length ; j<jLen ; j++ )
		{
			tr = dt.aoData[ aDataIndex[j] ].nTr;
			aRow = [];

			/* Columns */
			for ( i=0, iLen=dt.aoColumns.length ; i<iLen ; i++ )
			{
				if ( aColumnsInc[i] )
				{
					/* Convert to strings (with small optimisation) */
					var mTypeData = dt.oApi._fnGetCellData( dt, aDataIndex[j], i, 'display' );
					if ( oConfig.fnCellRender )
					{
						sLoopData = oConfig.fnCellRender( mTypeData, i, tr, aDataIndex[j] )+"";
					}
					else if ( typeof mTypeData == "string" )
					{
						/* Strip newlines, replace img tags with alt attr. and finally strip html... */
						sLoopData = mTypeData.replace(/\n/g," ");
						sLoopData =
						    sLoopData.replace(/<img.*?\s+alt\s*=\s*(?:"([^"]+)"|'([^']+)'|([^\s>]+)).*?>/gi,
						        '$1$2$3');
						sLoopData = sLoopData.replace( /<.*?>/g, "" );
					}
					else
					{
						sLoopData = mTypeData+"";
					}

					/* Trim and clean the data */
					sLoopData = sLoopData.replace(/^\s+/, '').replace(/\s+$/, '');
					sLoopData = this._fnHtmlDecode( sLoopData );

					/* Bound it and add it to the total data */
					aRow.push( this._fnBoundData( sLoopData, oConfig.sFieldBoundary, regex ) );
				}
			}

			aData.push( aRow.join(oConfig.sFieldSeperator) );

			/* Details rows from fnOpen */
			if ( oConfig.bOpenRows )
			{
				arr = $.grep(dt.aoOpenRows, function(o) { return o.nParent === tr; });

				if ( arr.length === 1 )
				{
					sLoopData = this._fnBoundData( $('td', arr[0].nTr).html(), oConfig.sFieldBoundary, regex );
					aData.push( sLoopData );
				}
			}
		}

		/*
		 * Footer
		 */
		if ( oConfig.bFooter && dt.nTFoot !== null )
		{
			aRow = [];

			for ( i=0, iLen=dt.aoColumns.length ; i<iLen ; i++ )
			{
				if ( aColumnsInc[i] && dt.aoColumns[i].nTf !== null )
				{
					sLoopData = dt.aoColumns[i].nTf.innerHTML.replace(/\n/g," ").replace( /<.*?>/g, "" );
					sLoopData = this._fnHtmlDecode( sLoopData );

					aRow.push( this._fnBoundData( sLoopData, oConfig.sFieldBoundary, regex ) );
				}
			}

			aData.push( aRow.join(oConfig.sFieldSeperator) );
		}

		var _sLastData = aData.join( this._fnNewline(oConfig) );
		return _sLastData;
	},


	/**
	 * Wrap data up with a boundary string
	 *  @method  _fnBoundData
	 *  @param   {String} sData data to bound
	 *  @param   {String} sBoundary bounding char(s)
	 *  @param   {RegExp} regex search for the bounding chars - constructed outside for efficiency
	 *			 in the loop
	 *  @returns {String} bound data
	 *  @private 
	 */
	"_fnBoundData": function ( sData, sBoundary, regex )
	{
		if ( sBoundary === "" )
		{
			return sData;
		}
		else
		{
			return sBoundary + sData.replace(regex, sBoundary+sBoundary) + sBoundary;
		}
	},


	/**
	 * Break a string up into an array of smaller strings
	 *  @method  _fnChunkData
	 *  @param   {String} sData data to be broken up
	 *  @param   {Int} iSize chunk size
	 *  @returns {Array} String array of broken up text
	 *  @private 
	 */
	"_fnChunkData": function ( sData, iSize )
	{
		var asReturn = [];
		var iStrlen = sData.length;

		for ( var i=0 ; i<iStrlen ; i+=iSize )
		{
			if ( i+iSize < iStrlen )
			{
				asReturn.push( sData.substring( i, i+iSize ) );
			}
			else
			{
				asReturn.push( sData.substring( i, iStrlen ) );
			}
		}

		return asReturn;
	},


	/**
	 * Decode HTML entities
	 *  @method  _fnHtmlDecode
	 *  @param   {String} sData encoded string
	 *  @returns {String} decoded string
	 *  @private 
	 */
	"_fnHtmlDecode": function ( sData )
	{
		if ( sData.indexOf('&') === -1 )
		{
			return sData;
		}

		var n = document.createElement('div');

		return sData.replace( /&([^\s]*?);/g, function( match, match2 ) {
			if ( match.substr(1, 1) === '#' )
			{
				return String.fromCharCode( Number(match2.substr(1)) );
			}
			else
			{
				n.innerHTML = match;
				return n.childNodes[0].nodeValue;
			}
		} );
	},



	/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
	 * Printing functions
	 */

	/**
	 * Show print display
	 *  @method  _fnPrintStart
	 *  @param   {Event} e Event object
	 *  @param   {Object} oConfig Button configuration object
	 *  @returns void
	 *  @private 
	 */
	"_fnPrintStart": function ( oConfig )
	{
	  var that = this;
	  var oSetDT = this.s.dt;

		/* Parse through the DOM hiding everything that isn't needed for the table */
		this._fnPrintHideNodes( oSetDT.nTable );

		/* Show the whole table */
		this.s.print.saveStart = oSetDT._iDisplayStart;
		this.s.print.saveLength = oSetDT._iDisplayLength;

		if ( oConfig.bShowAll )
		{
			oSetDT._iDisplayStart = 0;
			oSetDT._iDisplayLength = -1;
			if ( oSetDT.oApi._fnCalculateEnd ) {
				oSetDT.oApi._fnCalculateEnd( oSetDT );
			}
			oSetDT.oApi._fnDraw( oSetDT );
		}

		/* Adjust the display for scrolling which might be done by DataTables */
		if ( oSetDT.oScroll.sX !== "" || oSetDT.oScroll.sY !== "" )
		{
			this._fnPrintScrollStart( oSetDT );

			// If the table redraws while in print view, the DataTables scrolling
			// setup would hide the header, so we need to readd it on draw
			$(this.s.dt.nTable).bind('draw.DTTT_Print', function () {
				that._fnPrintScrollStart( oSetDT );
			} );
		}

		/* Remove the other DataTables feature nodes - but leave the table! and info div */
		var anFeature = oSetDT.aanFeatures;
		for ( var cFeature in anFeature )
		{
			if ( cFeature != 'i' && cFeature != 't' && cFeature.length == 1 )
			{
				for ( var i=0, iLen=anFeature[cFeature].length ; i<iLen ; i++ )
				{
					this.dom.print.hidden.push( {
						"node": anFeature[cFeature][i],
						"display": "block"
					} );
					anFeature[cFeature][i].style.display = "none";
				}
			}
		}

		/* Print class can be used for styling */
		$(document.body).addClass( this.classes.print.body );

		/* Show information message to let the user know what is happening */
		if ( oConfig.sInfo !== "" )
		{
			this.fnInfo( oConfig.sInfo, 3000 );
		}

		/* Add a message at the top of the page */
		if ( oConfig.sMessage )
		{
			$('<div/>')
				.addClass( this.classes.print.message )
				.html( oConfig.sMessage )
				.prependTo( 'body' );
		}

		/* Cache the scrolling and the jump to the top of the page */
		this.s.print.saveScroll = $(window).scrollTop();
		window.scrollTo( 0, 0 );

		/* Bind a key event listener to the document for the escape key -
		 * it is removed in the callback
		 */
		$(document).bind( "keydown.DTTT", function(e) {
			/* Only interested in the escape key */
			if ( e.keyCode == 27 )
			{
				e.preventDefault();
				that._fnPrintEnd.call( that, e );
			}
		} );
	},


	/**
	 * Printing is finished, resume normal display
	 *  @method  _fnPrintEnd
	 *  @param   {Event} e Event object
	 *  @returns void
	 *  @private 
	 */
	"_fnPrintEnd": function ( e )
	{
		var that = this;
		var oSetDT = this.s.dt;
		var oSetPrint = this.s.print;
		var oDomPrint = this.dom.print;

		/* Show all hidden nodes */
		this._fnPrintShowNodes();

		/* Restore DataTables' scrolling */
		if ( oSetDT.oScroll.sX !== "" || oSetDT.oScroll.sY !== "" )
		{
			$(this.s.dt.nTable).unbind('draw.DTTT_Print');

			this._fnPrintScrollEnd();
		}

		/* Restore the scroll */
		window.scrollTo( 0, oSetPrint.saveScroll );

		/* Drop the print message */
		$('div.'+this.classes.print.message).remove();

		/* Styling class */
		$(document.body).removeClass( 'DTTT_Print' );

		/* Restore the table length */
		oSetDT._iDisplayStart = oSetPrint.saveStart;
		oSetDT._iDisplayLength = oSetPrint.saveLength;
		if ( oSetDT.oApi._fnCalculateEnd ) {
			oSetDT.oApi._fnCalculateEnd( oSetDT );
		}
		oSetDT.oApi._fnDraw( oSetDT );

		$(document).unbind( "keydown.DTTT" );
	},


	/**
	 * Take account of scrolling in DataTables by showing the full table
	 *  @returns void
	 *  @private 
	 */
	"_fnPrintScrollStart": function ()
	{
		var
			oSetDT = this.s.dt,
			nScrollHeadInner = oSetDT.nScrollHead.getElementsByTagName('div')[0],
			nScrollHeadTable = nScrollHeadInner.getElementsByTagName('table')[0],
			nScrollBody = oSetDT.nTable.parentNode,
			nTheadSize, nTfootSize;

		/* Copy the header in the thead in the body table, this way we show one single table when
		 * in print view. Note that this section of code is more or less verbatim from DT 1.7.0
		 */
		nTheadSize = oSetDT.nTable.getElementsByTagName('thead');
		if ( nTheadSize.length > 0 )
		{
			oSetDT.nTable.removeChild( nTheadSize[0] );
		}

		if ( oSetDT.nTFoot !== null )
		{
			nTfootSize = oSetDT.nTable.getElementsByTagName('tfoot');
			if ( nTfootSize.length > 0 )
			{
				oSetDT.nTable.removeChild( nTfootSize[0] );
			}
		}

		nTheadSize = oSetDT.nTHead.cloneNode(true);
		oSetDT.nTable.insertBefore( nTheadSize, oSetDT.nTable.childNodes[0] );

		if ( oSetDT.nTFoot !== null )
		{
			nTfootSize = oSetDT.nTFoot.cloneNode(true);
			oSetDT.nTable.insertBefore( nTfootSize, oSetDT.nTable.childNodes[1] );
		}

		/* Now adjust the table's viewport so we can actually see it */
		if ( oSetDT.oScroll.sX !== "" )
		{
			oSetDT.nTable.style.width = $(oSetDT.nTable).outerWidth()+"px";
			nScrollBody.style.width = $(oSetDT.nTable).outerWidth()+"px";
			nScrollBody.style.overflow = "visible";
		}

		if ( oSetDT.oScroll.sY !== "" )
		{
			nScrollBody.style.height = $(oSetDT.nTable).outerHeight()+"px";
			nScrollBody.style.overflow = "visible";
		}
	},


	/**
	 * Take account of scrolling in DataTables by showing the full table. Note that the redraw of
	 * the DataTable that we do will actually deal with the majority of the hard work here
	 *  @returns void
	 *  @private 
	 */
	"_fnPrintScrollEnd": function ()
	{
		var
			oSetDT = this.s.dt,
			nScrollBody = oSetDT.nTable.parentNode;

		if ( oSetDT.oScroll.sX !== "" )
		{
			nScrollBody.style.width = oSetDT.oApi._fnStringToCss( oSetDT.oScroll.sX );
			nScrollBody.style.overflow = "auto";
		}

		if ( oSetDT.oScroll.sY !== "" )
		{
			nScrollBody.style.height = oSetDT.oApi._fnStringToCss( oSetDT.oScroll.sY );
			nScrollBody.style.overflow = "auto";
		}
	},


	/**
	 * Resume the display of all TableTools hidden nodes
	 *  @method  _fnPrintShowNodes
	 *  @returns void
	 *  @private 
	 */
	"_fnPrintShowNodes": function ( )
	{
	  var anHidden = this.dom.print.hidden;

		for ( var i=0, iLen=anHidden.length ; i<iLen ; i++ )
		{
			anHidden[i].node.style.display = anHidden[i].display;
		}
		anHidden.splice( 0, anHidden.length );
	},


	/**
	 * Hide nodes which are not needed in order to display the table. Note that this function is
	 * recursive
	 *  @method  _fnPrintHideNodes
	 *  @param   {Node} nNode Element which should be showing in a 'print' display
	 *  @returns void
	 *  @private 
	 */
	"_fnPrintHideNodes": function ( nNode )
	{
		var anHidden = this.dom.print.hidden;

		var nParent = nNode.parentNode;
		var nChildren = nParent.childNodes;
		for ( var i=0, iLen=nChildren.length ; i<iLen ; i++ )
		{
			if ( nChildren[i] != nNode && nChildren[i].nodeType == 1 )
			{
				/* If our node is shown (don't want to show nodes which were previously hidden) */
				var sDisplay = $(nChildren[i]).css("display");
				if ( sDisplay != "none" )
				{
					/* Cache the node and it's previous state so we can restore it */
					anHidden.push( {
						"node": nChildren[i],
						"display": sDisplay
					} );
					nChildren[i].style.display = "none";
				}
			}
		}

		if ( nParent.nodeName.toUpperCase() != "BODY" )
		{
			this._fnPrintHideNodes( nParent );
		}
	}
};



/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
 * Static variables
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

/**
 * Store of all instances that have been created of TableTools, so one can look up other (when
 * there is need of a master)
 *  @property _aInstances
 *  @type	 Array
 *  @default  []
 *  @private
 */
TableTools._aInstances = [];


/**
 * Store of all listeners and their callback functions
 *  @property _aListeners
 *  @type	 Array
 *  @default  []
 */
TableTools._aListeners = [];



/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
 * Static methods
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

/**
 * Get an array of all the master instances
 *  @method  fnGetMasters
 *  @returns {Array} List of master TableTools instances
 *  @static
 */
TableTools.fnGetMasters = function ()
{
	var a = [];
	for ( var i=0, iLen=TableTools._aInstances.length ; i<iLen ; i++ )
	{
		if ( TableTools._aInstances[i].s.master )
		{
			a.push( TableTools._aInstances[i] );
		}
	}
	return a;
};

/**
 * Get the master instance for a table node (or id if a string is given)
 *  @method  fnGetInstance
 *  @returns {Object} ID of table OR table node, for which we want the TableTools instance
 *  @static
 */
TableTools.fnGetInstance = function ( node )
{
	if ( typeof node != 'object' )
	{
		node = document.getElementById(node);
	}

	for ( var i=0, iLen=TableTools._aInstances.length ; i<iLen ; i++ )
	{
		if ( TableTools._aInstances[i].s.master && TableTools._aInstances[i].dom.table == node )
		{
			return TableTools._aInstances[i];
		}
	}
	return null;
};


/**
 * Add a listener for a specific event
 *  @method  _fnEventListen
 *  @param   {Object} that Scope of the listening function (i.e. 'this' in the caller)
 *  @param   {String} type Event type
 *  @param   {Function} fn Function
 *  @returns void
 *  @private
 *  @static
 */
TableTools._fnEventListen = function ( that, type, fn )
{
	TableTools._aListeners.push( {
		"that": that,
		"type": type,
		"fn": fn
	} );
};


/**
 * An event has occurred - look up every listener and fire it off. We check that the event we are
 * going to fire is attached to the same table (using the table node as reference) before firing
 *  @method  _fnEventDispatch
 *  @param   {Object} that Scope of the listening function (i.e. 'this' in the caller)
 *  @param   {String} type Event type
 *  @param   {Node} node Element that the event occurred on (may be null)
 *  @param   {boolean} [selected] Indicate if the node was selected (true) or deselected (false)
 *  @returns void
 *  @private
 *  @static
 */
TableTools._fnEventDispatch = function ( that, type, node, selected )
{
	var listeners = TableTools._aListeners;
	for ( var i=0, iLen=listeners.length ; i<iLen ; i++ )
	{
		if ( that.dom.table == listeners[i].that.dom.table && listeners[i].type == type )
		{
			listeners[i].fn( node, selected );
		}
	}
};






/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
 * Constants
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */



TableTools.buttonBase = {
	// Button base
	"sAction": "text",
	"sTag": "default",
	"sLinerTag": "default",
	"sButtonClass": "DTTT_button_text",
	"sButtonText": "Button text",
	"sTitle": "",
	"sToolTip": "",

	// Common button specific options
	"sCharSet": "utf8",
	"bBomInc": false,
	"sFileName": "*.csv",
	"sFieldBoundary": "",
	"sFieldSeperator": "\t",
	"sNewLine": "auto",
	"mColumns": "all", /* "all", "visible", "hidden" or array of column integers */
	"bHeader": true,
	"bFooter": true,
	"bOpenRows": false,
	"bSelectedOnly": false,
	"oSelectorOpts": undefined, // See http://datatables.net/docs/DataTables/1.9.4/#$ for full options

	// Callbacks
	"fnMouseover": null,
	"fnMouseout": null,
	"fnClick": null,
	"fnSelect": null,
	"fnComplete": null,
	"fnInit": null,
	"fnCellRender": null
};


/**
 * @namespace Default button configurations
 */
TableTools.BUTTONS = {
	"csv": $.extend( {}, TableTools.buttonBase, {
		"sAction": "flash_save",
		"sButtonClass": "DTTT_button_csv",
		"sButtonText": "CSV",
		"sFieldBoundary": '"',
		"sFieldSeperator": ",",
		"fnClick": function( nButton, oConfig, flash ) {
			this.fnSetText( flash, this.fnGetTableData(oConfig) );
		}
	} ),

	"xls": $.extend( {}, TableTools.buttonBase, {
		"sAction": "flash_save",
		"sCharSet": "utf16le",
		"bBomInc": true,
		"sButtonClass": "DTTT_button_xls",
		"sButtonText": "Excel",
		"fnClick": function( nButton, oConfig, flash ) {
			this.fnSetText( flash, this.fnGetTableData(oConfig) );
		}
	} ),

	"copy": $.extend( {}, TableTools.buttonBase, {
		"sAction": "flash_copy",
		"sButtonClass": "DTTT_button_copy",
		"sButtonText": "Copy",
		"fnClick": function( nButton, oConfig, flash ) {
			this.fnSetText( flash, this.fnGetTableData(oConfig) );
		},
		"fnComplete": function(nButton, oConfig, flash, text) {
			var lines = text.split('\n').length;
            if (oConfig.bHeader) lines--;
            if (this.s.dt.nTFoot !== null && oConfig.bFooter) lines--;
			var plural = (lines==1) ? "" : "s";
			this.fnInfo( '<h6>Table copied</h6>'+
				'<p>Copied '+lines+' row'+plural+' to the clipboard.</p>',
				1500
			);
		}
	} ),

	"pdf": $.extend( {}, TableTools.buttonBase, {
		"sAction": "flash_pdf",
		"sNewLine": "\n",
		"sFileName": "*.pdf",
		"sButtonClass": "DTTT_button_pdf",
		"sButtonText": "PDF",
		"sPdfOrientation": "portrait",
		"sPdfSize": "A4",
		"sPdfMessage": "",
		"fnClick": function( nButton, oConfig, flash ) {
			this.fnSetText( flash,
				"title:"+ this.fnGetTitle(oConfig) +"\n"+
				"message:"+ oConfig.sPdfMessage +"\n"+
				"colWidth:"+ this.fnCalcColRatios(oConfig) +"\n"+
				"orientation:"+ oConfig.sPdfOrientation +"\n"+
				"size:"+ oConfig.sPdfSize +"\n"+
				"--/TableToolsOpts--\n" +
				this.fnGetTableData(oConfig)
			);
		}
	} ),

	"print": $.extend( {}, TableTools.buttonBase, {
		"sInfo": "<h6>Print view</h6><p>Please use your browser's print function to "+
		  "print this table. Press escape when finished.</p>",
		"sMessage": null,
		"bShowAll": true,
		"sToolTip": "View print view",
		"sButtonClass": "DTTT_button_print",
		"sButtonText": "Print",
		"fnClick": function ( nButton, oConfig ) {
			this.fnPrint( true, oConfig );
		}
	} ),

	"text": $.extend( {}, TableTools.buttonBase ),

	"select": $.extend( {}, TableTools.buttonBase, {
		"sButtonText": "Select button",
		"fnSelect": function( nButton, oConfig ) {
			if ( this.fnGetSelected().length !== 0 ) {
				$(nButton).removeClass( this.classes.buttons.disabled );
			} else {
				$(nButton).addClass( this.classes.buttons.disabled );
			}
		},
		"fnInit": function( nButton, oConfig ) {
			$(nButton).addClass( this.classes.buttons.disabled );
		}
	} ),

	"select_single": $.extend( {}, TableTools.buttonBase, {
		"sButtonText": "Select button",
		"fnSelect": function( nButton, oConfig ) {
			var iSelected = this.fnGetSelected().length;
			if ( iSelected == 1 ) {
				$(nButton).removeClass( this.classes.buttons.disabled );
			} else {
				$(nButton).addClass( this.classes.buttons.disabled );
			}
		},
		"fnInit": function( nButton, oConfig ) {
			$(nButton).addClass( this.classes.buttons.disabled );
		}
	} ),

	"select_all": $.extend( {}, TableTools.buttonBase, {
		"sButtonText": "Select all",
		"fnClick": function( nButton, oConfig ) {
			this.fnSelectAll();
		},
		"fnSelect": function( nButton, oConfig ) {
			if ( this.fnGetSelected().length == this.s.dt.fnRecordsDisplay() ) {
				$(nButton).addClass( this.classes.buttons.disabled );
			} else {
				$(nButton).removeClass( this.classes.buttons.disabled );
			}
		}
	} ),

	"select_none": $.extend( {}, TableTools.buttonBase, {
		"sButtonText": "Deselect all",
		"fnClick": function( nButton, oConfig ) {
			this.fnSelectNone();
		},
		"fnSelect": function( nButton, oConfig ) {
			if ( this.fnGetSelected().length !== 0 ) {
				$(nButton).removeClass( this.classes.buttons.disabled );
			} else {
				$(nButton).addClass( this.classes.buttons.disabled );
			}
		},
		"fnInit": function( nButton, oConfig ) {
			$(nButton).addClass( this.classes.buttons.disabled );
		}
	} ),

	"ajax": $.extend( {}, TableTools.buttonBase, {
		"sAjaxUrl": "/xhr.php",
		"sButtonText": "Ajax button",
		"fnClick": function( nButton, oConfig ) {
			var sData = this.fnGetTableData(oConfig);
			$.ajax( {
				"url": oConfig.sAjaxUrl,
				"data": [
					{ "name": "tableData", "value": sData }
				],
				"success": oConfig.fnAjaxComplete,
				"dataType": "json",
				"type": "POST",
				"cache": false,
				"error": function () {
					alert( "Error detected when sending table data to server" );
				}
			} );
		},
		"fnAjaxComplete": function( json ) {
			alert( 'Ajax complete' );
		}
	} ),

	"div": $.extend( {}, TableTools.buttonBase, {
		"sAction": "div",
		"sTag": "div",
		"sButtonClass": "DTTT_nonbutton",
		"sButtonText": "Text button"
	} ),

	"collection": $.extend( {}, TableTools.buttonBase, {
		"sAction": "collection",
		"sButtonClass": "DTTT_button_collection",
		"sButtonText": "Collection",
		"fnClick": function( nButton, oConfig ) {
			this._fnCollectionShow(nButton, oConfig);
		}
	} )
};
/*
 *  on* callback parameters:
 *     1. node - button element
 *     2. object - configuration object for this button
 *     3. object - ZeroClipboard reference (flash button only)
 *     4. string - Returned string from Flash (flash button only - and only on 'complete')
 */

// Alias to match the other plug-ins styling
TableTools.buttons = TableTools.BUTTONS;


/**
 * @namespace Classes used by TableTools - allows the styles to be override easily.
 *   Note that when TableTools initialises it will take a copy of the classes object
 *   and will use its internal copy for the remainder of its run time.
 */
TableTools.classes = {
	"container": "DTTT_container",
	"buttons": {
		"normal": "DTTT_button",
		"disabled": "DTTT_disabled"
	},
	"collection": {
		"container": "DTTT_collection",
		"background": "DTTT_collection_background",
		"buttons": {
			"normal": "DTTT_button",
			"disabled": "DTTT_disabled"
		}
	},
	"select": {
		"table": "DTTT_selectable",
		"row": "DTTT_selected selected"
	},
	"print": {
		"body": "DTTT_Print",
		"info": "DTTT_print_info",
		"message": "DTTT_PrintMessage"
	}
};


/**
 * @namespace ThemeRoller classes - built in for compatibility with DataTables' 
 *   bJQueryUI option.
 */
TableTools.classes_themeroller = {
	"container": "DTTT_container ui-buttonset ui-buttonset-multi",
	"buttons": {
		"normal": "DTTT_button ui-button ui-state-default"
	},
	"collection": {
		"container": "DTTT_collection ui-buttonset ui-buttonset-multi"
	}
};


/**
 * @namespace TableTools default settings for initialisation
 */
TableTools.DEFAULTS = {
	"sSwfPath":        "../swf/copy_csv_xls_pdf.swf",
	"sRowSelect":      "none",
	"sRowSelector":    "tr",
	"sSelectedClass":  null,
	"fnPreRowSelect":  null,
	"fnRowSelected":   null,
	"fnRowDeselected": null,
	"aButtons":        [ "copy", "csv", "xls", "pdf", "print" ],
	"oTags": {
		"container": "div",
		"button": "a", // We really want to use buttons here, but Firefox and IE ignore the
		                 // click on the Flash element in the button (but not mouse[in|out]).
		"liner": "span",
		"collection": {
			"container": "div",
			"button": "a",
			"liner": "span"
		}
	}
};

// Alias to match the other plug-ins
TableTools.defaults = TableTools.DEFAULTS;


/**
 * Name of this class
 *  @constant CLASS
 *  @type	 String
 *  @default  TableTools
 */
TableTools.prototype.CLASS = "TableTools";


/**
 * TableTools version
 *  @constant  VERSION
 *  @type	  String
 *  @default   See code
 */
TableTools.version = "2.2.2";



// DataTables 1.10 API
// 
// This will be extended in a big way in in TableTools 3 to provide API methods
// such as rows().select() and rows.selected() etc, but for the moment the
// tabletools() method simply returns the instance.

if ( $.fn.dataTable.Api ) {
	$.fn.dataTable.Api.register( 'tabletools()', function () {
		var tt = null;

		if ( this.context.length > 0 ) {
			tt = TableTools.fnGetInstance( this.context[0].nTable );
		}

		return tt;
	} );
}




/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
 * Initialisation
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

/*
 * Register a new feature with DataTables
 */
if ( typeof $.fn.dataTable == "function" &&
	 typeof $.fn.dataTableExt.fnVersionCheck == "function" &&
	 $.fn.dataTableExt.fnVersionCheck('1.9.0') )
{
	$.fn.dataTableExt.aoFeatures.push( {
		"fnInit": function( oDTSettings ) {
			var init = oDTSettings.oInit;
			var opts = init ?
				init.tableTools || init.oTableTools || {} :
				{};

			return new TableTools( oDTSettings.oInstance, opts ).dom.container;
		},
		"cFeature": "T",
		"sFeature": "TableTools"
	} );
}
else
{
	alert( "Warning: TableTools requires DataTables 1.9.0 or newer - www.datatables.net/download");
}

$.fn.DataTable.TableTools = TableTools;

})(jQuery, window, document);

/*
 * Register a new feature with DataTables
 */
if ( typeof $.fn.dataTable == "function" &&
	 typeof $.fn.dataTableExt.fnVersionCheck == "function" &&
	 $.fn.dataTableExt.fnVersionCheck('1.9.0') )
{
	$.fn.dataTableExt.aoFeatures.push( {
		"fnInit": function( oDTSettings ) {
			var oOpts = typeof oDTSettings.oInit.oTableTools != 'undefined' ?
				oDTSettings.oInit.oTableTools : {};

			var oTT = new TableTools( oDTSettings.oInstance, oOpts );
			TableTools._aInstances.push( oTT );

			return oTT.dom.container;
		},
		"cFeature": "T",
		"sFeature": "TableTools"
	} );
}
else
{
	alert( "Warning: TableTools 2 requires DataTables 1.9.0 or newer - www.datatables.net/download");
}


$.fn.dataTable.TableTools = TableTools;
$.fn.DataTable.TableTools = TableTools;


return TableTools;
}; // /factory


// Define as an AMD module if possible
if ( typeof define === 'function' && define.amd ) {
	define( 'TableTools',['jquery', 'datatables'], factory );
}
else if ( typeof exports === 'object' ) {
    // Node/CommonJS
    factory( require('jquery'), require('datatables') );
}
else if ( jQuery && !jQuery.fn.dataTable.TableTools ) {
	// Otherwise simply initialise as normal, stopping multiple evaluation
	factory( jQuery, jQuery.fn.dataTable );
}


})(window, document);


// generic list view - reads entity's objectstore and prepares table using templates declared in entity's config
define('views/list',['jquery', 'underscore', 'datatables', 'indexeddb_backbone_config', 'layoutmanager', 'views/notification', 'configs', 'offline_utils', 'models/user_model', 'indexeddb-backbone', 'TableTools'], function ($, pass, pass, indexeddb, layoutmanager, notifs_view, all_configs, Offline, User) {


    var ListView = Backbone.Layout.extend({

        template: "#list_view_template",

        //params passed contains the name of the entity whose listing is to be shown
        initialize: function (params) {
            this.entity_config = all_configs[params.entity_name];
            //TODO: if !entity_config, handle error etc
            //now context of all fuctions in this view would always be the view object
            _.bindAll(this);
            this.render();
            User.on('change', this.render);
        },

        serialize: function () {
            //send these to the list page template
            var language = User.get('language');
            return {
                page_header: this.entity_config['config_'+language],
                list_page_help: all_configs['misc']['meta_'+language]['list_page_help']
            };
        },

        afterRender: function () {
            //Fetch entity's full data from offline DB and call render_data when fetched
            Offline.fetch_collection(this.entity_config.entity_name)
                .done(this.render_data)
                .fail(function () {
                    notifs_view.add_alert({
                        notif_type: "error",
                        message: "Error reading data for listing."
                    });
                });
        },
        
        get_row_header: function () {
            var language = User.get('language');
            var list_elements = this.entity_config['list_elements_'+language];
            var header_row = $.map(list_elements, function (column_definition) {
                var header = "";
                if ('header' in column_definition) {
                    header = column_definition["header"];
                }
                else if ('element' in column_definition) {
                    // Split column_definition to get the very last field.
                    // For instance, extract block_name from village.block.block_name
                    element = column_definition["element"].split(".").pop().replace(/_/g, " ");
                    header = element[0].toUpperCase() + element.slice(1);
                }
                return {sTitle: header};
            });
            if (!('dashboard_display' in this.entity_config) || (!('add' in this.entity_config.dashboard_display)) || this.entity_config['dashboard_display']['add'] != false) {
                header_row.push({sTitle: all_configs['misc']['meta_'+language]['edit']});
            }
            return header_row;
        },
        
        get_row: function (model_object) {
            var language = User.get('language');
            var list_elements = this.entity_config['list_elements_'+language];
            var row = $.map(list_elements, function (column_definition) {
                var cell = '';
                if ('element' in column_definition) {
                    if ('subelement' in column_definition) {
                        var subelement_definition = column_definition['subelement'];
                        cell = $.map(model_object[column_definition['element']],function (val) {
                            return val[subelement_definition];
                        }).join("; ");
                    }
                    else {
                        var element_definition = column_definition['element'];
                        var element_parts = element_definition.split(".");
                        var object = model_object;
                        for (var i = 0; i < element_parts.length; i++) {
                            // To check if the entry is made online or offline. Display "Not uploaded in place of id in case of offline entry"
                            if(element_parts.length == 1 && element_parts[i] == "online_id" && object.online_id == undefined){
                                object = "Not Uploaded"
                            }
                            else{
                                    object = object[element_parts[i]];
                            }
                        }
                    }
                    if (object != null) {
                        cell = object;
                    }
                }
                else {
                    // Developer needs to be told that 'element' is compulsory.
                    alert('Error: Add element in list_elements parameter in configs.js');
                }
                return cell;
            });
            if (!('dashboard_display' in this.entity_config) || (!('add' in this.entity_config.dashboard_display)) || this.entity_config['dashboard_display']['add'] != false) {
                row.push('<a href="#' + this.entity_config.entity_name + '/edit/' + model_object['id'] + '" class="edit" title="Edit this entry"><i class="glyphicon glyphicon-pencil"></i></a>');

            }
            return row;
        },

        render_data: function (entity_collection) {
            // render data and call function get_row() to make array_table_values which is assigned to aaData later to
            // fill the table with the relevant values.
            var self = this;
            var language = User.get('language');
            console.log("in render_data...change in collection...rendering list view");
            var array_table_values = $.map(entity_collection.toJSON(), function (model) {
                return [self.get_row(model)];
            });
            aoColumns = this.get_row_header();
            this.$('#list_table')
                .DataTable({
                    "sDom": 'T<"clear">lfrtip',
                    "bDeferRender": true,
                    "aoColumns": aoColumns,
                    "bAutoWidth":false,
                    "aaData": array_table_values,       //aaData takes array_table_values and push data in the table.
                    "bAutoWidth":false,
                    "bDestroy": true,
                    "oLanguage": {
                        "sSearch": all_configs['misc']['meta_'+language]['search'],
                        "sLengthMenu": all_configs['misc']['meta_'+language]['enteries']+"_MENU_",
                        "sInfo": all_configs['misc']['meta_'+language]['total_enteries']+"_TOTAL_",
                        "oPaginate": {
                            "sNext": all_configs['misc']['meta_'+language]['next'],
                            "sPrevious": all_configs['misc']['meta_'+language]['previous']
                        },
                    },
                    "oTableTools": {
                        "sSwfPath": "/media/coco/app/scripts/libs/tabletools_media/swf/copy_csv_xls.swf",
                        "aButtons": [
                            {
                                "sExtends": "copy",
                                "sButtonText": all_configs['misc']['meta_'+language]['copy_clipboard']
                            },
                            {
                                "sExtends": "xls",
                                "sButtonText": all_configs['misc']['meta_'+language]['excel_download']
                            }
                        ]

                    }
                });
            $("#loaderimg")
                .hide();
            $("#sort-helptext").show();
        }
    });
    return ListView;
});

// This module is responsible for supporting Add/Edit functionalities. This is the container view of Form view for ADD/EDIT. Uses Form view to show the form. When Form has to be saved - gets the json from Form view and processes it to save the object depending upon the internet connectivity of the user.
define('views/form_controller',[
    'jquery',
    'underscore',
    'layoutmanager',
    'views/notification',
    'indexeddb_backbone_config',
    'configs',
    'views/form',
    'collections/upload_collection',
    'convert_namespace',
    'offline_utils',
    'online_utils',
    'models/user_model',
    'indexeddb-backbone'
], function(jquery, underscore, layoutmanager, notifs_view, indexeddb, configs, Form, upload_collection, ConvertNamespace, Offline, Online, User) {

    // FormController: Brings up the Add/Edit form

    /*
    If we are saving offline - we set the json from the form, (we denormalize it), save it in the model and save the model in the upload queue.
    If we are saving online - we set the json from the form, (we denormalize it), we convert foreign keys ids to the online namespace, save the offline model, and then save it on server.
    If server save succeeds, then we set the online_id in the offline model.
    */


var message_combined_success = "";
var message_combined_failure = "";

    var FormControllerView = Backbone.Layout.extend({

        initialize: function(params) {
            console.log("FORMCONTROLLER: initializing a new FormControllerView");
            this.params = params;
            _.bindAll(this);
            User.on('change', this.render);
        },
        template: "<div><div id = 'form'></div></div>",

        //setting up the form view
        beforeRender: function() {
            console.log(this.params);
            var language = User.get("language");
            var button = configs['misc']['meta_'+language]['save'];
            // pass on the params to the form view - also add desired names of the buttons on form - null hides the button
            this.params = $.extend(this.params, {
                serialize: {
                    button1: button,
                    button2: null
                }
            });
            // initialize the form view
            var form_v = new Form(this.params);
            // #form is the id of the element inside template where the form view will be inserted.
            this.setView("#form", form_v);
            // listen to when form view sends these events 
            // this view now does nothing till these events are triggered by the form view
            this.listenTo(form_v, 'save_clicked', this.on_save);
            this.listenTo(form_v, 'button2_clicked', this.on_button2);
        },

        // Called when form view triggers save_clicked event(triggered after form has been converted to json, json has been cleaned and denormalised). 
        // Identifies type of final_json and saves it
        // After Save is finished calls an after_form_save function
        on_save: function(e) {
            //event contains the form view object itself
            // Set the count of successful and failed saves. These are later used to give notifications
            counts_success = new Object();
            counts_failure = new Object();
            
            // Reset the notification messages because if the person is adding multiple persons, the message does not get duplicated
            message_combined_failure=""
            message_combined_success=""
            this.form = e.context; 
            console.log("FORMCONTROLLER: cleaned, denormalised json from form.js-" + JSON.stringify(this.form.final_json));
            var that = this;
            //stores dfds of all objects bieng saved in this form - form is completely saved when all dfd in this list are resolved
            var save_complete_dfds = []; 

            if (this.form.bulk) {
                // Save each object in bulk form individually
                $.each(this.form.final_json.bulk, function(ind, obj) {
                    // index is maintained in each object to find its location on the form
                    var bulk_index = obj.index;
                    delete obj.index;
                    // save the object
                    var save_object_dfd = that.save_object(obj, that.form.bulk.foreign_fields, that.form.entity_name);
                    save_object_dfd
                        .fail(function(error) {
                            // error while saving object
                            // show the error on the form right above the object
                            that.form.show_errors(that.convert_to_row_error(error, that.form.entity_name, bulk_index));
                        });
                    // put dfd for this object-save in the save_complete_dfds list
                    save_complete_dfds.push(save_object_dfd);
                });
            } 
            else 
            {
                //normal or inlines
                
                if (this.form.inline) {
                    // its an inline form
                    console.log("FORMCONTROLLER: separating inlines from final json");
                    // list of all inlines
                    this.inline_models = this.form.final_json.inlines;
                    //separate inlines from final json - since they would be saved separately
                    delete this.form.final_json.inlines;
                    // add a dummy dfd for inlines - resolve it when inlines have been saved
                    if((!this.form.edit_case) && (this.form.inline.req_nonnegotiable))
                    {
                        if ( this.form.inline.req_nonnegotiable > this.inline_models.length){
                            var err = {};
                            err[that.form.entity_name] = {
                                    __all__: ['Error: ' + this.form.inline.error_message]
                            };
                            this.form.show_errors(err);
                            var add_validation = this.form.inline.validation_chk;
                            $(add_validation).removeClass("donotvalidate");
                            $(add_validation).valid();
                            $(add_validation).addClass("donotvalidate");
                            return ;
                        }
                    }
                    var inlines_dfd = new $.Deferred();
                    save_complete_dfds.push(inlines_dfd);
                }
                // save the normal form object or the inline parent form
                var save_object_dfd = this.save_object(this.form.final_json, this.form.foreign_entities, this.form.entity_name);
                save_object_dfd
                    .done(function(off_json) {
                        // parent form saved
                        if (that.form.inline)
                            //If inline form - save inlines now
                            that.save_inlines(that.inline_models, off_json, that.form.inline)
                                .done(function(all_inlines) {
                                    console.log("ALL INLINES SAVED");
                                    inlines_dfd.resolve(all_inlines);
                                    
                                })
                                .fail(function() {
                                    console.log("FAILED AT INLINES SAVE");
                                    show_inline_error();
                                    inlines_dfd.reject();
                                });
                    })
                    .fail(function(error) {
                        that.form.show_errors(error);
                    });
                save_complete_dfds.push(save_object_dfd);
            }

            //When all objects in form are saved...
            $.when.apply(null, save_complete_dfds)
                .done(function() {
                    console.log("Everything saved");
                    that.after_form_save(that.form.entity_name);
                    if (message_combined_success!="")
                    {
                        notifs_view.add_alert({
                            notif_type: "success",
                            message: message_combined_success});
                    }
                })
                .fail(function() {
                    if (that.form.bulk)
                        show_bulk_error();
                    if (message_combined_success!="")
                        notifs_view.add_alert({
                            notif_type: "success",
                            message: message_combined_success});

                    notifs_view.add_alert({
                        notif_type: "error",
                        message: message_combined_failure
                    });
                });

            //shown if any inline could not be saved
            function show_inline_error() {
                var err = {};
                err[that.form.entity_name] = {
                    __all__: ["Some " + that.form.inline.entity + " (in red below) could not be saved. To correct errors and try saving them again - go to list page and edit this " + that.form.entity_name]
                };
                that.form.show_errors(err, true);
            };

            //shown if any bulk could not be saved
            function show_bulk_error() {
                var err = {};
                err[that.form.entity_name] = {
                    __all__: ["Some " + that.form.entity_name + " (in red below) could not be saved. To correct errors and try saving them again - open a new add form"]
                };
                that.form.show_errors(err, true);
            };
        },

        //converts the error for an inline/bulk into a format which makes it show up at its own row
        convert_to_row_error: function(error, row_entity_name, row_index) {
            error = $.parseJSON(error);
            error["row" + row_index] = error[row_entity_name];
            delete error[row_entity_name];
            return error;
        },
        
        // iterates over the inlines list and saves them serially
        save_inlines: function(inlines, parent_off_json, inline_config) {
            var dfd = new $.Deferred();
            var that = this;
            this.complete_inlines(inlines, parent_off_json, inline_config);
            iterate_inlines();
            return dfd;

            //saves inlines serially    
            function iterate_inlines() {
                if (!inlines.length)
                    return dfd.resolve();
                save_inline(inlines.shift())
                    .done(function() {
                        iterate_inlines();
                    })
                    .fail(function() {
                        dfd.reject();
                    });
            };
            // saves an inline
            function save_inline(inl) {
                var inl_dfd = $.Deferred();
                // index maintained to find its location on the form
                var inl_index = inl.index;
                delete inl.index;
                that.save_object(inl, inline_config.foreign_entities, inline_config.entity)
                    .fail(function(error) {
                        that.form.show_errors(that.convert_to_row_error(error, inline_config.entity, inl_index));
                        return inl_dfd.reject();
                    })
                    .done(function() {
                        return inl_dfd.resolve();
                    });
                return inl_dfd.promise();
            };
        },

        //put in the borrowed attributes and the joining attribute in inlines from the parent form
        complete_inlines: function(inlines, parent_off_json, inline_config) {
            var host_attr_json = {};
            // get the host attr from parent object
            host_attr_json[inline_config.joining_attribute.inline_attribute] = {}
            _.each(inline_config.joining_attribute.host_attribute, function(attr, index) {
                host_attr_json[inline_config.joining_attribute.inline_attribute][attr] = parent_off_json[attr];
            }, this);

            // get the borrowed attrs from parent object
            var borr_json = {}
            $.each(inline_config.borrow_attributes, function(index, b_attr) {
                borr_json[b_attr.inline_attribute] = parent_off_json[b_attr.host_attribute];
            });
            
            // substitute the host and borrowed attributes in each inline
            _.each(inlines, function(inl, index) {
                console.log("inl before extension - " + JSON.stringify(inl));
                $.extend(true, inl, host_attr_json);
                $.extend(true, inl, borr_json);
                console.log("inl after extension - " + JSON.stringify(inl));
            });
        },
        
        // save an object depending upon the internet connectivity of user
        save_object: function(json, foreign_entities, entity_name) {
            var dfd = new $.Deferred();
            var that = this;
            if (this.is_uploadqueue_empty() && this.is_internet_connected()) {
                //Online mode
                // convert namespace of object from offline to online
                ConvertNamespace.convert(json, foreign_entities, "offlinetoonline")
                    .done(function(on_off_jsons) {
                        // save in online mode
                        that.save_when_online(entity_name, on_off_jsons)
                            .done(function(off_json) {
                                // call any user defined after-save
                                call_after_save(off_json)
                                    .done(function() {
                                        // successfully saved
                                        show_suc_notif();
                                        dfd.resolve(off_json);
                                    })
                                    .fail(function(error) {
                                        // user defined after-save failed
                                        alert("afterSave failed for entity - " + entity_name + " - " + error);
                                    });
                            })
                            .fail(function(error) {
                                // error saving the object
                                // show error on form
                                show_err_notif();
                                dfd.reject(error);
                            });
                    })
                    .fail(function(error) {
                        // namespace conversion failed
                        show_err_notif();
                        return dfd.reject(error);
                    });
            } else {
                //Offline mode
                // save in offline mode
                this.save_when_offline(entity_name, json)
                    .done(function(off_json) {
                        // call any user defined after-save
                        call_after_save(off_json)
                            .done(function() {
                                // successfully saved
                                show_suc_notif();
                                dfd.resolve(off_json);
                            })
                            .fail(function(error) {
                                // user defined after-save failed
                                alert("afterSave failed for entity - " + entity_name + " - " + error);
                            });
                    })
                    .fail(function(error) {
                        // error saving the object
                        // show error on form
                        show_err_notif();
                        return dfd.reject(error);
                    });
            }
            
            function call_after_save(saved_off_json) {
                var dfd = new $.Deferred();
                // get the user defined after-save for this entity
                var afterSave = configs[entity_name].afterSave;
                if (afterSave)
                    afterSave(saved_off_json, Offline)
                        .done(function() {
                            dfd.resolve();
                        })
                        .fail(function(error) {
                            dfd.reject(error);
                        });
                else dfd.resolve();
                return dfd.promise();
            };

            function show_suc_notif() {
               
               // function counts the successful operations and creates the notification message. Has to be done BEFORE the notification is added, hence here.
                console.log(message_combined_success);
                if (counts_success.hasOwnProperty(entity_name)){
                    counts_success[entity_name] +=1;
                }
                else
                {
                    counts_success[entity_name] = 1;
                }
                message_combined_success="";
                for (var title in counts_success)
                {
                    if (counts_success[title]>0)
                        message_combined_success = message_combined_success + "<br>" + "Saved " + counts_success[title] + " " +title;
                }       
            };

            function show_err_notif() {
            // function counts the errors and creates the notification message
               if (counts_failure.hasOwnProperty(entity_name)){
                    counts_failure[entity_name] +=1;
                }
                else{
                    counts_failure[entity_name] = 1;
                }
                message_combined_failure="";
                for (var title in counts_failure)
                {
                    if (counts_failure[title]>0)
                        message_combined_failure = message_combined_failure + "<br>" + "Error saving " + counts_failure[title] + " " +title;

                }
            };
            return dfd.promise();
        },

        // saves the object in offline mode - in offline db and uploadQ
        save_when_offline: function(entity_name, off_json) {
            var dfd = new $.Deferred();
            var action, that = this;
            if (off_json.id)
                action = "E"
            else
                action = "A"

            // save in offline db and then the uploadQ
            Offline.save(null, entity_name, off_json)
                .done(function(off_m) {
                    // succesfully saved in offline db
                    console.log("SAVED IN OFFLINE - " + JSON.stringify(off_m.toJSON()));
                    upload_collection.create({
                        data: off_m.toJSON(),
                        action: action,
                        entity_name: entity_name
                    }, {
                        success: function(u_model) {
                            // successfully saved in uploadQ
                            console.log("FORMCNTROLLER: model added to uploadqueue - " + JSON.stringify(u_model.toJSON()));
                            return dfd.resolve(off_m.toJSON());
                        },
                        error: function(error) {
                            // failed to save in uploadQ
                            alert("Unexepected Error- error adding model to uploadqueue");
                            //TODO: Unexpected but should delete the model from offline db as well?
                            return dfd.reject(error);
                        }
                    });
                })
                .fail(function(error) {
                    // failed to save in offline db - return the error
                    return dfd.reject(error);
                });

            return dfd.promise();
        },

        // saves the object in online mode - on the server and then the offline db
        save_when_online: function(entity_name, on_off_jsons) {
            var dfd = new $.Deferred();
            var on_json = on_off_jsons.on_json;
            var off_json = on_off_jsons.off_json
            console.log("FORMCONTROLLER: Got this json to save online - " + JSON.stringify(on_json));
            var that = this;
            //if edit case, substitute id with online id TODO: move it to convertnamespace?
            if (off_json.id) {
                on_json.id = parseInt(off_json.online_id);
                delete on_json.online_id;
            }
            // save on server
            Online.save(null, entity_name, on_json)
                .done(function(on_m) {
                    // successfully saved on server
                    console.log("SAVED IN ONLINE - " + JSON.stringify(on_m.toJSON()));
                    // inject the online id returned by server in the offline object
                    off_json.online_id = parseInt(on_m.get("id"));
                    // save offline object in offline db
                    Offline.save(null, entity_name, off_json)
                        .done(function(off_m) {
                            // successfully saved in offline and online
                            console.log("SAVED IN OFFLINE - " + JSON.stringify(off_m.toJSON()));
                            return dfd.resolve(off_m.toJSON());
                        })
                        .fail(function(error) {
                            //TODO: what to do abt the model just saved on server? 
                            return dfd.reject(error);
                        });
                })
                .fail(function(xhr) {
                    // failed to save on server - return the error
                    return dfd.reject(xhr.responseText);
                });
            return dfd.promise();
        },
        
        // checks whether the uploadQ is empty or not
        is_uploadqueue_empty: function() {
            console.log("FORMCONTROLLER: length of upload_collection - " + upload_collection.length);
            console.log(upload_collection);

            return upload_collection.length <= 0;
        },

        // checks whther internet is available
        is_internet_connected: function() {
            return navigator.onLine;
        },
        
        // button2 is made null - so this is nevr used 
        on_button2: function(e) {
            console.log("FORMCONTROLLER: Button 2 clicked on form");
        },
        
        // route to a fresh add form for this entity
        after_form_save: function(entity_name) {
            window.Router.navigate(entity_name + '/add');
            //since may already be on the add page, therefore have to call this explicitly
            window.Router.add(entity_name); 
        }




    });

    // Our module now returns our view
    return FormControllerView;
});

// This is the home/status view shown at root url. It contains the welcome message, usage instructions and some offline db stats.
// It checks whether offline db exists or not, if not initiates the full download module.

define('views/status',[
    'jquery',
    'underscore',
    'layoutmanager',
    'indexeddb_backbone_config',
    'views/full_download',
    'configs',
    'collections/upload_collection',
    'views/notification',
    'models/user_model',
    'offline_utils',
    'indexeddb-backbone'
], function(jquery, underscore, layoutmanager, indexeddb, FullDownloadView, configs, upload_collection, notifs_view, User, Offline) {

    var StatusView = Backbone.Layout.extend({
        template: "#status",
        timestamp: null,
        upload_entries: null,
        events: {
            "click button#download": "download",
            "click button#reset_database": "reset"
        },

        initialize: function() {
            _(this).bindAll('render');
            this.fill_status();
            User.on('change', this.render);
        },

        serialize: function() {
            // send the following to the template
            var language = User.get('language');
            return {
                language: language,
                configs: configs,
                full_d_timestamp: this.full_download_timestamp,
                inc_d_timestamp: this.inc_download_timestamp,
                num_upload_entries: this.upload_entries,
                db_version: this.db_version,
                upload_collection: upload_collection.toJSON()
            }
        },

        // fills the stats on the view
        fill_status: function() {
            var that = this;
            // # of unsynced entries
            that.upload_entries = upload_collection.length;
            // current version of IndexedDB - its wrong - shd take the last migration instead of first
            that.db_version = indexeddb.migrations[0].version;

            // fetch last full download's timestamp
            Offline.fetch_object("meta_data", "key", "last_full_download")
                .done(function(model) {
                    that.full_download_timestamp = new Date(model.get('timestamp'));
                    // fetch last inc download's timestamp
                    Offline.fetch_object("meta_data", "key", "last_inc_download")
                        .done(function(model) {
                            that.inc_download_timestamp = new Date(model.get('timestamp'));
                            // all stats fetched....render the view
                            that.render();
                        })
                        .fail(function(model, error) {
                            // all stats fetched....render the view
                            that.inc_download_timestamp = "Never";
                            that.render();
                        });
                    that.render();
                })
                .fail(function(model, error) {
                    console.log("STATUS: error while fetching last_downloaded from meta_data objectStore");
                    console.log(error);
                    if (error == "Not Found") {
                        // offline db not populated...full donwload never finished
                        that.full_download_timestamp = "Never";
                        that.render()
                            .done(function() {
                                //Start full download automatically
                                that.download();
                            });
                    }
                });


        },

        //method to initiate full download
        download: function() {
            var dfd = new $.Deferred();
            //create full download view
            if (!this.full_download_v) {
                this.full_download_v = new FullDownloadView();
            }
            // set full download as subview
            this.setView("#modal", this.full_download_v).render();
            var that = this;
            //start full download
            this.full_download_v.start_full_download()
                .done(function() {
                    // render status view once full download finishes
                    that.fill_status();
                    notifs_view.add_alert({
                        notif_type: "success",
                        message: "Successfully downloaded the database"
                    });
                    dfd.resolve();
                })
                .fail(function(error) {
                    notifs_view.add_alert({
                        notif_type: "error",
                        message: "Failed to download the database : " + error
                    });
                    dfd.reject();
                });
            return dfd;
        },

        // Resets the offline db
        reset: function() {
            // check if user has unsynced data in upload queue
            if(upload_collection.length > 0){
                var val = confirm("You will lose unsynced data. Click 'Ok' to proceed and 'Cancel' to abort")
                if (val == true) {
                    Offline.reset_database();
                }    
            }
            else {
                var val = confirm("Your database will be deleted and downloaded again. Are you sure you want to continue?")
                if (val == true) {
                    Offline.reset_database();
                }
            }
        }
    });

    // Our module now returns our view
    return StatusView;
});

// The view for login. Its responsibiltiy is to show the login form to user and uses auth.js module to do the actual authentication.
define('views/login',[
    'jquery',
    'underscore',
    'backbone',
    'layoutmanager',
    'models/user_model',
    'auth',
	  'offline_utils', 
	  'configs',
    'collections/upload_collection'

], function(jquery, underscore, backbone, layoutmanager, User, Auth, Offline, all_configs, upload_collection){

    var LoginView = Backbone.Layout.extend({
      template: "#login",
      events:{
          'click #login_button': 'attempt_login',
		  'click #change_user' : 'change_user'		  
      },
      
      initialize: function(){
          console.log("Initializing login view");
          _(this).bindAll('render');
          var that = this;
          that.render();
      },
      
      serialize: function(){
          var s_passed = {};
          
          // name of the entity bieng added/edited
          
          // send the user info to the template
          s_passed["user"] = User.toJSON();
          s_passed["configs"] = all_configs;
          return s_passed;
      },
      
      scrap_view: function(){
           this.$('#login_modal').modal('hide');
           $('.modal-backdrop').remove();
      },
      
      afterRender: function(){
          console.log("rendered login view");
          //render the modal
          User.fetch({
              success: function(model){
                  console.log("USERMODEL : successfully fetched");
                  this.$('#login_modal').modal({
                       keyboard: false,
                       backdrop: "static",
                  });
              },
              error: function(){
                  console.log("USERMODEL :  fetch failed") 
                  this.$('#login_modal').modal({
                      keyboard: false,
                      backdrop: "static",
                  });           
              }
          });
      },
      
      //fetches u,p from dom  and asks auth module to login
      attempt_login: function(e){
		  e.preventDefault();
          console.log("login attempted");
          this.set_login_button_state('loading');
          var username = this.$('#username').val();
          var password = this.$('#password').val();
          var language = this.$('#language').val();
          var that = this;
          // use the auth module to authenticate
          if (language != ''){
              Auth.login(username, password, language)
                  .done(function(){
                      //login successfull - route to the home view
                      that.scrap_view();
                      window.Router.navigate("", {
                          trigger:true
                      });
                  })
                  .fail(function(error){
                      // authentication failed
                      // clear the password
    			      $("#password").val('');
                      // show the error
    				  that.$('#error_msg').html(error);
                      that.set_login_button_state('reset');
                  });
          }
          else{
              that.$('#error_msg').html("Language not Selected");
              that.set_login_button_state('reset');
          }
      },
      
      // set state of login button - disable while authentication request is under process
      set_login_button_state: function(state){
          if(state=="disabled")
              this.$("#login_button").attr("disabled",true);    
          else
              this.$("#login_button").button(state);    
      },
	  
      // to login with different user - clear the offline db of existing user
	  change_user: function(){
      // check if user has unsynced data in upload queue
      if(upload_collection.length > 0){
        var val = confirm("You will lose unsynced data. Click 'Ok' to proceed and 'Cancel' to abort")
        if (val == true) {
            Offline.reset_database();
        }    
      }
      else{
    		var val = confirm("Your current database will be deleted and a new database will be downloaded");
    		if (val==true){
    			Offline.reset_database();
    		}
  	  }
    }
      
  });
    
  // Our module now returns our view
  return LoginView;
});
//The parent view containing the side panel and the content panel. It will hold all other views as subviews - dashboard view goes into the side panel and the status/list/add_edit view goes into contant panel based on current url.
define('views/app_layout',['views/dashboard', 'views/app_header', 'views/list', 'views/form_controller', 'views/status', 'layoutmanager', 'views/login', 'models/user_model', 'auth'], function(DashboardView, HeaderView, ListView, FormControllerView, StatusView, layoutmanager, LoginView, User, Auth) {

    var AppLayout = Backbone.Layout.extend({
        template: "#page_layout",
        
        initialize: function() {
            console.log("initializing app layout");
        },
        
        serialize: function() {
            // send username to the template 
            var username = User.get("username");
            console.log(User);
            return {
                username: username,
            }
                
        },
        
        //when layout is rendered, create and put the dashboard view in the side panel - constant across all routes
        afterRender: function() {
            console.log("app layout rendered");
            var header_view = new HeaderView();
            this.setView("#header", header_view);
            header_view.render();
            var dashboard_view = new DashboardView();
            this.setView("#side_panel", dashboard_view);
            dashboard_view.render();
        },

        //content panel will be filled with a subview by one of the following functions based on the current url
        render_login: function() {
            var login_view = new LoginView();
            this.setView("#content", login_view);
        },

        render_home_view: function() {
            var s_view = new StatusView();
            this.setView("#content", s_view);
        },

        render_list_view: function(entity_name) {
            var l_view = new ListView({
                entity_name: entity_name
            });
            this.setView("#content", l_view);
        },

        render_add_edit_view: function(entity_name, id) {
            var formcontroller_view = new FormControllerView({
                entity_name: entity_name,
                model_id: id,
            });
            this.setView("#content", formcontroller_view);
            formcontroller_view.render(); //bcoz Its afterRender assumes its elements are in DOM
        }
    });
    return new AppLayout;
});

// Backbone router
define('router',['jquery', 'underscore', 'backbone', 'views/app_layout', 'configs', 'auth'], function(jquery, underscore, backbone, AppLayout, configs, Auth) {

    var initialize = function() {
        console.log("Initializing router");
        //create a router
        var app_router = new AppRouter();
        //set it on global object to make it easily accessible
        window.Router = app_router;
        //begin monitoring hash change events
        Backbone.history.start();
    };

    var AppRouter = Backbone.Router.extend({
        //define the routes and the function callbacks
        routes: {
            "": "home",
            ":entity/list": "list",
            ":entity/add": "add",
            ":entity/edit/:id": "edit",
            "login": "login"
        },
        home: function() {
            this.check_login_wrapper()
                .done(function() {
                AppLayout.render_home_view();
            });
        },
        list: function(entity_name) {
        	//Check if entity present in url is valid or not and if list view of that entity is enable in case it is valid
        	if(this.entity_valid(entity_name) && this.entity_list_enabled(entity_name)){
        		this.check_login_wrapper()
                .done(function(){
                    AppLayout.render_list_view(entity_name);
                });
        	}
        	else{
        		alert("You are not authorized to view this page. Please contact your administrator.");
        	}
        },
        add: function(entity_name) {
        	//Check if entity present in url is valid or not and if add view of that entity is enable in case it is valid
        	if(this.entity_valid(entity_name) && this.entity_add_enabled(entity_name)){
        		this.check_login_wrapper()
                .done(function(){
                    AppLayout.render_add_edit_view(entity_name, null);
                });
        	}
        	else{
        		alert("You are not authorized to view this page. Please contact your administrator.");
        	}
            
        },
        edit: function(entity_name, id) {
        	//Check if entity present in url is valid or not and if edit view of that entity is enable in case it is valid
        	if(this.entity_valid(entity_name) && this.entity_add_enabled(entity_name)){
        		this.check_login_wrapper()
                .done(function(){
                    AppLayout.render_add_edit_view(entity_name, parseInt(id));
                });
        	}
        	else{
        		alert("You are not authorized to view this page. Please contact your administrator.");
        	}
        },
        login: function() {
            AppLayout.render_login();
        },
        //Check if user entered wrong entity name in url.
        entity_valid: function(entity_name){
        	if(typeof configs[entity_name] == 'undefined'){
        		return false;
        	}
        	else{
        		return true;
        	}
        },
        //Check if list view was allowed in configs so that user may not directly enter the url and access table
        entity_list_enabled: function(entity_name){
            var listing = true;
            if(configs[entity_name].dashboard_display)
            {
            	listing = configs[entity_name].dashboard_display.listing;
            }
            return listing;
        },
      //Check if add view was allowed in configs so that user may not directly enter the url and access form
        entity_add_enabled: function(entity_name){
            var add = true;
            var enable_months;
            if(configs[entity_name].dashboard_display)
            {
                add = configs[entity_name].dashboard_display.add;
                enable_months = configs[entity_name].dashboard_display.enable_months;
            }
            if(typeof enable_months != 'undefined'){
            	var d = new Date();
                n = d.getMonth();
                n=n+1;
                res=$.inArray(n, enable_months);
                if(res === -1){
                	add=false;
                }
            }
            return add;
        },
        //check_login wrapper for checking whether user is logged in before routing to any of the above defined routes 
        check_login_wrapper: function() {
            var dfd = new $.Deferred();
            console.log("Authenticating before routing");
            Auth.check_login()
                .fail(function(err) {
                console.log("Unauthenticated");
                dfd.reject();
                //navigate to login url if user is not logged in
                window.Router.navigate("login", {
                    trigger: true
                });
            })
                .done(function() {
                console.log("Authenticated");
                dfd.resolve();
            });
            return dfd;
        }

    });

    return {
        initialize: initialize
    };
});

//The user of the COCO v2 framework shall write any app initialization logic here
define('user_initialize',['auth', 'offline_utils', 'configs', 'jquery', 'form_field_validator', ], function(Auth, Offline, all_configs) {

    var run = function() {
        // adding custom validation checks to jquery.Validation plugin
        $.validator.addMethod('allowedChar',
        validateUniCodeChars, 'Enter a string.');
        $.validator.addMethod('validateDate',
        validateDate, 'Enter the date in the form of YYYY-MM-DD.');
        $.validator.addMethod('validateTime',
        validateTime, 'Enter the time in the form of HH:MM. Use 24 hour format');
        $.validator.addMethod('dateOrder',
        dateOrder, 'End date should be later than start date');

        //onLogin callback ... used to check for reset database trigger
        //this thing belongs somewhere else...in app initialize probably...its a framework's thing
        reset_database_check();
    }

        function reset_database_check() {
            if (!all_configs.misc.onLogin) return;
            //if the user is logged in call the callback here else call it after login    
            Auth.check_login()
                .done(function() {
                if (!navigator.onLine) return;
                all_configs.misc.onLogin(Offline, Auth);
            });
        }

        function validateUniCodeChars(value) {
            if (value) {
                var alphabetCharset = /^[a-zA-Z ]+$/;
                var strictUniCodeChars = /.*[^\\x20-\\x7E].*/;
                if (alphabetCharset.test(value)) {
                    return true;
                }
                if (strictUniCodeChars.test(value)) {
                    return true;
                } else {
                    return false;
                }
            } else {
                return true;
            }
        }

        function validateDate(value) {
            var check = false;
            var re = /^\d{4}\-\d{1,2}\-\d{1,2}$/;
            if (re.test(value)) {
                var adata = value.split('-');
                var year = parseInt(adata[0], 10);
                var month = parseInt(adata[1], 10);
                var day = parseInt(adata[2], 10);
                var xdata = new Date(year, month - 1, day);
                if ((xdata.getFullYear() === year) && (xdata.getMonth() === month - 1) && (xdata.getDate() === day)) {
                    check = true;
                } else {
                    check = false;
                }
            } else {
                check = false;
            }
            return check;
        }

        function validateTime(value) {
            var check = false;
            var adata = value.split(':');
            var hours = parseInt(adata[0], 10);
            var minutes = parseInt(adata[1], 10);
            if ((hours > 24) && (minutes > 60)) {
                check = false;
            } else {
                check = true;
            }
            return check;
        }

        function dateOrder(value, element, options) {
            var check = false;
            var start = $('#' + options.production_date)
                .val();
            //console.log("START DATE = " + start + ' END = ' + value);

            startDate = start.split('-');
            endDate = value.split('-');

            if (endDate[0] > startDate[0] || String(endDate)
                .length === 0) {
                check = true;
            } else if (endDate[0] === startDate[0]) {
                if (endDate[1] > startDate[1]) {
                    check = true;
                } else if (endDate[1] === startDate[1]) {
                    if (endDate[2] >= startDate[2]) {
                        check = true;
                    }
                }
            }
            return check;
        }

        function timeOrder(value, element, options) {
            var check = false;
            var start = $('#' + options.start_time)
                .val();
            var end = value;
            if (start < end) {
                check = true;
            } else {
                check = false;
            }
            return check;
        }
    return {
        run: run
    };
});

//  Initializes application. 
// - updates appcache
// - runs framework intitialize:
//     * configures all ajax POST /PUT requests to set csrf token
//     * configures ajax requests to navigate to login url in case 401 error is recvd
//     * puts in the parent view of application - app_layout
// - runs initialization specified by user in user_initialize.js
// - starts router - Router takes over from here.

define('app',['router', 'user_initialize', 'views/app_layout', ], function(Router, UserInitialize, AppLayout) {

    var initialize = function() {
        //check for appcache update
        update_appcache(); 
        //wait till dom is ready
        $(function() {
            //initialize framework
            framework_initialize();
            //run any initialization logic defined by framework user in user_initialize.js 
            UserInitialize.run();
            //start the router - the router takes over from here 
            Router.initialize(); 
        });
    };


    var framework_initialize = function() {
        //globally configure ajax requests to set csrf token header for authentication
        $.ajaxSetup({
            // obviates need for sameOrigin test
            crossDomain: false, 
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type)) {
                    xhr.setRequestHeader("X-CSRFToken", get_csrf());
                }
            },
        });

        //globally configure ajax requests to redirect to login url when server returns unauthorized error
        $(document)
            .ajaxError(function(event, jqxhr, settings, exception) {
            if (jqxhr.status == 401) window.Router.navigate("login", {
                trigger: true
            });
        });

        //set the parent view - Applayout - containing the empty side and content panel
        $("#app")
            .empty()
            .append(AppLayout.el);
        AppLayout.render();
    };

    var get_csrf = function() {
        return $.cookie('csrftoken');
    };

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    };

    var update_appcache = function() {
        $(window)
            .load(function() {
            window.applicationCache.addEventListener('updateready', function(e) {
                if (window.applicationCache.status == window.applicationCache.UPDATEREADY) {
                    // Browser downloaded a new app cache.
                    // Swap it in and reload the page to get the new hotness.
                    window.applicationCache.swapCache();
                    if (confirm('A new version of this site is available. Load it?')) {
                        window.location.reload();
                    }
                }
            }, false);
        });
    };

    return {
        initialize: initialize
    };
});

//The entry point of application. Configures requirejs, loads "app" module
require.config({
    paths: {
        'hm': 'libs/hm',
        'jquery': 'libs/jquery.min',
        'underscore': 'libs/backbone/underscore-min',
        'backbone': 'libs/backbone/backbone-min',
        'indexeddb-backbone': 'libs/indexeddb-backbonejs-adapter/backbone-indexeddb',
        'datatables': 'libs/datatablejs_media/js/jquery.dataTables.min',
        'form_field_validator': 'libs/jquery.validate',
        'layoutmanager': 'libs/layoutmanager/backbone.layoutmanager',
        'syphon': 'libs/backbone.syphon',
        'bootstrapjs': 'libs/bootstrap/js/bootstrap.min',
        'chosen': 'libs/chosen-select/chosen.jquery.min',
        'date_picker': 'libs/bootstrap/js/bootstrap-datepicker',
        'time_picker': 'libs/bootstrap/js/bootstrap-timepicker.min',
        'jquery_cookie': 'libs/jquery.cookie',
        'TableTools': 'libs/tabletools_media/js/dataTables.tableTools'
    },

    //specifying dependencies of non-amd libraries
    shim: {
        'backbone': {
            //These script dependencies should be loaded before loading backbone.js
            deps: ['underscore', 'jquery'],
            exports: 'Backbone'
        },
        'indexeddb-backbone': {
            deps: ['backbone'],
        },
        'layoutmanager': {
            deps: ['backbone'],
        },
        'bootstrapjs': {
            deps: ['jquery'],
        },
        'underscore': {
            deps: ['jquery'],
            exports: "_"
        },
        'datatable': {
            deps: ["jquery"]
        },
        'zeroclipboard': {
    		deps:['jquery']
        },
        'tabletools': {
    		deps:['jquery', 'datatables']
        },
        'form_field_validator': {
            deps: ["jquery"]
        },

        'syphon': {
            deps: ["jquery", "backbone"]
        },

        'bootstrapjs': {
            deps: ["jquery"]
        },
        'chosen': {
            deps: ["jquery"]
        },
        'date_picker': {
            deps: ["jquery"]
        },
        'time_picker': {
            deps: ["jquery"]
        }
    }
});

require(['app'], function(app) {
    // Show alert if COCO is opened in Internet Explorer and redirect to FAQ page to install Chrome or Firefox 
    
    var ua = window.navigator.userAgent;
    var msie = ua.indexOf('MSIE ');
    var trident = ua.indexOf('Trident/');

    // Check for IE Version <= 10
    if (msie > 0) {
        alert("Currently COCO is not supported on IE Browser. Please use Chrome or Firefox.");
        window.location = "/coco/faq/#setup";
    }
    // Check for IE Version >= 11
    else if (trident > 0) {
        alert("Currently COCO is not supported on IE Browser. Please use Chrome or Firefox.");
        window.location = "/coco/faq/#setup";
    }
    else{
        //load and initialize app module
        app.initialize();
    }
});

define("main", function(){});

