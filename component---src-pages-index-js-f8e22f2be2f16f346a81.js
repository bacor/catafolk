(window.webpackJsonp=window.webpackJsonp||[]).push([[7],{"65eO":function(e,a,t){"use strict";var l=t("wx14"),n=t("zLVn"),s=t("TSYQ"),r=t.n(s),c=t("q1tI"),i=t.n(c),m=t("vUet"),o=i.a.forwardRef((function(e,a){var t=e.bsPrefix,s=e.variant,c=e.pill,o=e.className,u=e.as,d=void 0===u?"span":u,f=Object(n.a)(e,["bsPrefix","variant","pill","className","as"]),E=Object(m.a)(t,"badge");return i.a.createElement(d,Object(l.a)({ref:a},f,{className:r()(o,E,c&&E+"-pill",s&&E+"-"+s)}))}));o.displayName="Badge",o.defaultProps={pill:!1},a.a=o},RXBc:function(e,a,t){"use strict";t.r(a);var l=t("q1tI"),n=t.n(l),s=t("Wbzz"),r=t("LvDl"),c=t.n(r),i=t("6xyR"),m=t("YdCC"),o=Object(m.a)("card-columns"),u=t("7vrA"),d=t("3Z9Z"),f=t("xXt2"),E=t("Bl7J"),p=t("IujW"),v=t.n(p),b=t("whKl");var g=function(e){var a=e.dataset;return n.a.createElement(i.a,{key:a.dataset_id},n.a.createElement(i.a.Body,null,n.a.createElement(i.a.Title,null,a.title||c.a.startCase(a.dataset_id)),n.a.createElement(v.a,{source:a.description,className:"card-text"}),a.tags.length>0?n.a.createElement(b.a,{tags:a.tags,className:"mb-3"}):null,n.a.createElement(s.a,{to:"/"+a.fields.slug,className:"btn btn-dark"},"View ",a.dataset_id)))};t.d(a,"query",(function(){return y}));a.default=function(e){var a=e.data;return n.a.createElement(E.a,null,n.a.createElement(u.a,{className:"mt-5"},n.a.createElement(d.a,null,n.a.createElement(f.a,{className:"w-100"},n.a.createElement("div",{style:{maxWidth:"700px"}},n.a.createElement("h1",{className:"display-4"},"Catafolk"),n.a.createElement("p",{className:"lead"},"A catalogue of folk music datasets for computational ethnomusicology"),n.a.createElement("hr",{className:"my-4"}),n.a.createElement("p",null,"The project hopes to make datasets of folk music more easily accessible. It provides a reference of datasets, but also aims to include some basic automatic analyses.")))),n.a.createElement(d.a,{className:"mt-4"},n.a.createElement(o,null,a.allDataset.edges.map((function(e){return n.a.createElement(g,{dataset:e.dataset,key:e.dataset.dataset_id})})),n.a.createElement(i.a,{bg:"dark",text:"light"},n.a.createElement(i.a.Body,null,n.a.createElement(i.a.Title,null,"And more..."),n.a.createElement(i.a.Text,null,"Catafolk currently contains ",a.total.totalCount," datasets.",n.a.createElement(s.a,{to:"/datasets/",className:"btn btn-light mt-3"},"View all datasets"))))))))};var y="2818987343"},whKl:function(e,a,t){"use strict";t("rGqo"),t("yt8O"),t("Btvt"),t("RW0V"),t("91GP");var l=t("q1tI"),n=t.n(l),s=t("65eO");function r(e,a){if(null==e)return{};var t,l,n={},s=Object.keys(e);for(l=0;l<s.length;l++)t=s[l],a.indexOf(t)>=0||(n[t]=e[t]);return n}function c(e){var a=e.children,t=r(e,["children"]);return n.a.createElement(s.a,Object.assign({pill:!0},t),a)}a.a=function(e){var a=e.tags,t=e.variant,l=r(e,["tags","variant"]);return n.a.createElement("div",l,a.map((function(e){return n.a.createElement(c,{variant:t||"light",className:"mr-2",key:e},e)})))}}}]);
//# sourceMappingURL=component---src-pages-index-js-f8e22f2be2f16f346a81.js.map