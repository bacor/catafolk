(window.webpackJsonp=window.webpackJsonp||[]).push([[19],{GVxD:function(e,a,t){"use strict";t.r(a),t.d(a,"query",(function(){return T}));var r=t("KQm4"),n=t("zLVn"),l=t("q1tI"),c=t.n(l),s=(t("Wbzz"),t("LvDl")),i=t.n(s),o=t("ajLg"),u=t.n(o),m=t("IujW"),d=t.n(m),E=t("IdFE"),h=t("cWnB"),p=t("xXt2"),f=t("YdCC"),g=Object(f.a)("card-deck"),b=t("6xyR"),v=t("Bl7J"),y=t("whKl");function w(e){var a=e.url,t=e.children,r=void 0!==a&null!==a;return c.a.createElement(c.a.Fragment,null,r?c.a.createElement("a",{href:a},t):c.a.createElement("span",null,t))}function x(e){var a=e.name,t=e.url,r=e.role,l=Object(n.a)(e,["name","url","role"]),s=void 0!==r&null!==r;return c.a.createElement("span",l,c.a.createElement(w,{url:t},a),s?c.a.createElement("span",{className:"text-muted"}," (",r,")"):null)}function _(e){var a=e.persons,t=Object(n.a)(e,["persons"]);return c.a.createElement("div",t,a.map((function(e,t){return c.a.createElement("span",{key:e.name},c.a.createElement(x,{name:e.name,url:e.url,role:e.role}),t<a.length-1?", ":null)})))}var N=function(e){var a=e.people,t=e.textProps,r=Object(n.a)(e,["people","textProps"]);return"string"==typeof a?c.a.createElement("span",Object.assign({},t,r),a):c.a.createElement(_,Object.assign({persons:a},r))},k=t("wSTC"),C=t("Kvkj"),H=t("3Z9Z"),j=t("7vrA"),L=t("pTLS"),O=function(e){var a=e.dataset;return c.a.createElement(p.a,{className:"w-100",key:a.dataset_id+"-header"},c.a.createElement("div",null,c.a.createElement("h1",{className:"display-4"},a.title||i.a.startCase(a.dataset_id)),c.a.createElement("div",{className:"lead",style:{maxWidth:700}},a.description?c.a.createElement(d.a,{source:a.description}):c.a.createElement("span",{className:"text-muted"},"This dataset has no description yet...")),c.a.createElement(y.a,{tags:a.tags,variant:"dark",className:"mb-4"}),c.a.createElement(h.a,{variant:"dark",href:a.dataset_url,className:"mr-2"},"Go to dataset ",c.a.createElement(E.b,null)),c.a.createElement(h.a,{variant:"outline-secondary",href:a.github_directory+"/index.csv"},"View full index ",c.a.createElement(E.b,null))))};function F(e){e.abbreviation;var a=e.name,t=e.url,r=e.text;return e.unknown?c.a.createElement("span",{className:"text-danger"},"Unknown"):c.a.createElement(c.a.Fragment,null,c.a.createElement("a",{href:t,target:"_blank",className:"bold",title:a},a),".",r?c.a.createElement(c.a.Fragment,null,c.a.createElement("br",null),c.a.createElement("span",null,i.a.truncate(r,{length:200}))):null)}function B(e){var a=e.dataset,t=e.bibliography;return c.a.createElement(k.b,{title:"Properties"},c.a.createElement(k.a,{title:"Dataset ID"},c.a.createElement("code",{className:"text-muted"},a.dataset_id)),a.version&&c.a.createElement(k.a,{title:"Version"},c.a.createElement("code",{className:"text-muted"},a.version)),a.authors&&c.a.createElement(k.a,{title:"Authors"},c.a.createElement(N,{people:a.authors})),a.contributors&&c.a.createElement(k.a,{title:"Contributors"},c.a.createElement(N,{people:a.contributors})),c.a.createElement(k.a,{title:"Citation"},a.dataset_citation_keys.map((function(e){return t.format("citation",{entry:e}).slice(1,-1)})).join("; ")),c.a.createElement(k.a,{title:"Sources"},a.publication_citation_keys.map((function(e){return t.format("citation",{entry:e}).slice(1,-1)})).join("; ")),a.copyright&&c.a.createElement(k.a,{title:"Copyright"},c.a.createElement(d.a,{source:a.copyright})),a.license&&c.a.createElement(k.a,{title:"License"},c.a.createElement(F,a.license)),a.formats&&c.a.createElement(k.a,{title:"Formats"},c.a.createElement(y.a,{tags:a.formats,variant:"secondary"})))}var I=function(e){var a=e.dataset,t=null!==a.readme;return t&&(t=a.readme.file.wordCount.words>0),t?c.a.createElement(b.a,{className:"w-100"},c.a.createElement(b.a.Header,null,"Read me"),c.a.createElement(b.a.Body,null,c.a.createElement(d.a,{source:a.readme.file.rawMarkdownBody}))):c.a.createElement(b.a,{bg:"secondary",text:"light",className:"w-100 text-center"},c.a.createElement(b.a.Header,null,"No readme yet..."),c.a.createElement(b.a.Body,null,c.a.createElement(b.a.Title,null,"Contribute!"),c.a.createElement("p",null,"This dataset has no readme yet, describing how to download or use the dataset. ",c.a.createElement("br",null),"Are you familiar with this dataset? Please consider ",c.a.createElement("a",{className:"text-dark"},"contributing"),"."),c.a.createElement(h.a,{variant:"light",href:a.github_directory+"/README.md"},"Edit me on GitHub!")))};function A(e){var a=e.issue;return c.a.createElement(c.a.Fragment,null,c.a.createElement("dt",null,a.title),c.a.createElement("dd",null,c.a.createElement(d.a,{source:a.description})))}function D(e){var a=e.issues;return c.a.createElement(b.a,{className:"border-danger",bg:"light"},c.a.createElement(b.a.Header,null,"Issues"),c.a.createElement(b.a.Body,null,c.a.createElement("dl",{className:"small"},a.map((function(e){return c.a.createElement(A,{issue:e,key:e.title})})))))}function M(e){var a=e.bibliography,t=Object(n.a)(e,["bibliography"]);return c.a.createElement(b.a,null,c.a.createElement(b.a.Header,null,"References"),c.a.createElement(b.a.Body,null,c.a.createElement(L.a,Object.assign({bibliography:a},t))))}a.default=function(e){var a,t,n=e.data,l=n.metadata;l.github_directory=n.site.siteMetadata.github+"/tree/master/datasets/"+l.dataset_id,l.raw_index_url="#",l.index=n.index,l.readme=n.readme;var s=n.sources.nodes.map((function(e){return e.content})).join("\n"),o=new u.a(s),m=n.index.source_keys;(a=m).push.apply(a,Object(r.a)(l.dataset_citation_keys)),(t=m).push.apply(t,Object(r.a)(l.publication_citation_keys));var d=(m=i.a.uniq(m)).length>0&&m!==[""],E={};m.forEach((function(e){var a;try{a=o.format("citation",{entry:e})}catch(t){console.warn("An error occured while formatting citation "+e,t),a=e}E[e]=a}));var h=o.data.filter((function(e){return e.id in E}));o.data=h;var p=l.show_columns||[],f=c.a.useMemo((function(){return[{Header:function(){return null},id:"expander",Cell:C.b,Filter:!1,Sort:!1},{Header:"ID",accessor:"id",Cell:C.e,width:50},{Header:"Options",accessor:function(e){return""+(void 0!==e.preview_url)+(void 0!==e.url)+(void 0!==e.source_url)},id:"options",Cell:C.d,Filter:!1,width:50},{Header:"Num",accessor:"source_song_num",width:20},{Header:"Title",accessor:"title",Cell:function(e){var a=e.cell;return c.a.createElement(C.f,{cell:a,maxLength:80})}},{Header:"Source",id:"source",accessor:function(e){if(!e.source_key)return null;var a=E[e.source_key],t=e.source_page_num;return a?a.slice(1,-1)+(t?", p. "+t:""):e.source_key+(t?", p. "+t:"")},Cell:function(e){var a=e.cell;return c.a.createElement(C.f,{cell:a,maxLength:25})}},{Header:"Location",accessor:"location",Cell:function(e){var a=e.cell;return c.a.createElement(C.f,{cell:a,maxLength:30})}},{Header:"Collectors",accessor:"collector",Cell:function(e){var a=e.cell;return c.a.createElement(C.f,{cell:a,maxLength:30})}},{Header:"Culture",accessor:"culture",Cell:function(e){var a=e.cell;return c.a.createElement(C.f,{cell:a,maxLength:30})}},{Header:"Language",accessor:"language",Cell:function(e){var a=e.cell;return c.a.createElement(C.f,{cell:a,maxLength:30})}},{Header:"Genre",accessor:"genres",Cell:function(e){var a=e.cell;return c.a.createElement(C.f,{cell:a,maxLength:30})}},{Header:"Meters",accessor:"meters",Cell:function(e){var a=e.cell;return c.a.createElement(C.f,{cell:a,maxLength:30})}},{Header:"Key",accessor:"key",width:30},{Header:"Ambitus",accessor:"ambitus",width:30},{Header:"md5",accessor:"checksum",Cell:C.a,width:20}]}),[]),b=c.a.useMemo((function(){return l.index.songs})),y=null!==l.issues;return c.a.createElement(v.a,{pageName:l.dataset_id},c.a.createElement(j.a,null,c.a.createElement(H.a,{className:"mt-5"},c.a.createElement(O,{dataset:l})),c.a.createElement(H.a,null,c.a.createElement(g,null,c.a.createElement(B,{dataset:l,bibliography:o}),y&&c.a.createElement(D,{issues:l.issues})))),c.a.createElement(j.a,{className:"mt-5"},c.a.createElement(H.a,null,l.index?c.a.createElement(C.c,{columns:f,data:b,showColumns:p,bibliography:o}):"None")),c.a.createElement(j.a,{className:"mt-5"},c.a.createElement(H.a,{className:"mt-5"},c.a.createElement(I,{dataset:l})),c.a.createElement(H.a,{className:"mt-5"},c.a.createElement(g,{className:"w-100"},d&&c.a.createElement(M,{bibliography:o,twoColumns:!0})))))};var T="611018628"},whKl:function(e,a,t){"use strict";var r=t("zLVn"),n=t("q1tI"),l=t.n(n),c=t("65eO");function s(e){var a=e.children,t=Object(r.a)(e,["children"]);return l.a.createElement(c.a,Object.assign({pill:!0},t),a)}a.a=function(e){var a=e.tags,t=e.variant,n=Object(r.a)(e,["tags","variant"]);return l.a.createElement("div",n,a.map((function(e){return l.a.createElement(s,{variant:t||"light",className:"mr-2",key:e},e)})))}}}]);
//# sourceMappingURL=component---src-templates-dataset-js-48b4689d622b91b8b05c.js.map