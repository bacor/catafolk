(window.webpackJsonp=window.webpackJsonp||[]).push([[18],{"8oxB":function(e,t){var n,r,a=e.exports={};function o(){throw new Error("setTimeout has not been defined")}function c(){throw new Error("clearTimeout has not been defined")}function i(e){if(n===setTimeout)return setTimeout(e,0);if((n===o||!n)&&setTimeout)return n=setTimeout,setTimeout(e,0);try{return n(e,0)}catch(t){try{return n.call(null,e,0)}catch(t){return n.call(this,e,0)}}}!function(){try{n="function"==typeof setTimeout?setTimeout:o}catch(e){n=o}try{r="function"==typeof clearTimeout?clearTimeout:c}catch(e){r=c}}();var l,u=[],s=!1,f=-1;function m(){s&&l&&(s=!1,l.length?u=l.concat(u):f=-1,u.length&&h())}function h(){if(!s){var e=i(m);s=!0;for(var t=u.length;t;){for(l=u,u=[];++f<t;)l&&l[f].run();f=-1,t=u.length}l=null,s=!1,function(e){if(r===clearTimeout)return clearTimeout(e);if((r===c||!r)&&clearTimeout)return r=clearTimeout,clearTimeout(e);try{r(e)}catch(t){try{return r.call(null,e)}catch(t){return r.call(this,e)}}}(e)}}function p(e,t){this.fun=e,this.array=t}function d(){}a.nextTick=function(e){var t=new Array(arguments.length-1);if(arguments.length>1)for(var n=1;n<arguments.length;n++)t[n-1]=arguments[n];u.push(new p(e,t)),1!==u.length||s||i(h)},p.prototype.run=function(){this.fun.apply(null,this.array)},a.title="browser",a.browser=!0,a.env={},a.argv=[],a.version="",a.versions={},a.on=d,a.addListener=d,a.once=d,a.off=d,a.removeListener=d,a.removeAllListeners=d,a.emit=d,a.prependListener=d,a.prependOnceListener=d,a.listeners=function(e){return[]},a.binding=function(e){throw new Error("process.binding is not supported")},a.cwd=function(){return"/"},a.chdir=function(e){throw new Error("process.chdir is not supported")},a.umask=function(){return 0}},dyTM:function(e,t,n){"use strict";n.r(t);var r=n("q1tI"),a=n.n(r),o=n("Wbzz"),c=n("6xyR"),i=n("7vrA"),l=n("3Z9Z"),u=n("xXt2"),s=n("ajLg"),f=n.n(s),m=n("Bl7J"),h=n("pTLS");t.default=function(){var e=Object(o.c)("1073422028"),t=new f.a(e.file.content);return a.a.createElement(m.a,{pageName:"datasets"},a.a.createElement(i.a,null,a.a.createElement(l.a,{className:"mt-5"},a.a.createElement(u.a,{className:"col-12"},a.a.createElement("h1",{className:"display-4"},"Sources"),a.a.createElement("p",{className:"lead w-75"},"The project pays special attention to bibliography, to ensure the origins of all the songs are clearly documented. All sources currently included in Catafolk are listed below."))),a.a.createElement(l.a,null,a.a.createElement(c.a,{className:"w-100"},a.a.createElement(c.a.Header,null,"Sources"),a.a.createElement(c.a.Body,null,a.a.createElement(h.a,{bibliography:t,twoColumns:!0}))))))}}}]);
//# sourceMappingURL=component---src-pages-sources-js-c6c7081640afad0931ca.js.map