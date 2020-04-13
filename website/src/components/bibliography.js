import React from "react";
import Cite from 'citation-js';
import chicagoAuthorDate from 'raw-loader!../assets/chicago-author-date.cls'
import styles from './bibliography.module.css'

// Register Chicago format
let config = Cite.plugins.config.get('@csl')
config.templates.add('chicago', chicagoAuthorDate)

// Cite.plugins.dict.add('test', {
//     bibliographyContainer: ['', ''],
//     entry: ['Bla', 'Boe'],
//     list: ['<ul style="list-style-type:none">', '</ul>'],
//     listItem: ['<li>', '</li>']
//   }
// )
// console.log(Cite.plugins.dict.list())

// function BibliographyItem({ item }) {
//   const html = item.format('bibliography', {
//     format: 'html',
//     template: 'chicago'
//   })
//   console.log(html)
//   const output = (
//     <div dangerouslySetInnerHTML={{__html: html}}>
//     </div>
//   )
//   return output
// }

function getRawBibtexEntries(bibliography) {
  const ids = bibliography.getIds()
  if(bibliography.data.length === 0) return [];
  const graph = bibliography.data[0]._graph
  let rawEntries = {}
  graph.forEach(item => {
    if(item.type == '@bibtex/object') {
      const label = item.data.label
      if(ids.indexOf(label) >= 0) {
        rawEntries[label] = item.data
      }
    }
  })
  return rawEntries
}

function Bibliography({ children, twoColumns, ...options }) {
  let classNames = styles.bibliography
  if(twoColumns) classNames += ` ${styles.bibliographyCol2}`
  return (
    <div className={classNames} {...options}>
      {children}
    </div>
  ); 
}

export default ({ bibliography, ...options }) => {
  const rawEntries = getRawBibtexEntries(bibliography)
  
  // const bibTexButton = bibtex => (
  //   `<a class="badge badge-pill badge-light"
  //     data-toggle="popover" data-html="true" data-placement="bottom"
  //     title="BibTex entry"
  //     data-content="<pre class='text-muted small'>${bibtex}</pre>">
  //     BibTeX
  //   </a>`
  // )
  
  let output = bibliography.format('bibliography', {
    format: 'html',
    template: 'chicago',
    lang: 'en-US',
    append (entry) {
      // const item = new Cite(entry)
      // const bibtex = item.format('bibtex')
      const raw = rawEntries[entry.id]
      const elements = []
       
      if('catafolk-hathitrust' in raw.properties) {
        const href = raw.properties['catafolk-hathitrust']
        const btn = `<a class="badge badge-pill badge-light d-inline" href="${href}" target="_blank">Hathi Trust</a>`
        elements.push(btn)
      }
      
      if('catafolk-googlebooks' in raw.properties) {
        const href = raw.properties['catafolk-googlebooks']
        const btn = `<a class="badge badge-pill badge-light d-inline" href="${href}" target="_blank">Google</a>`
        elements.push(btn)
      }

      if('catafolk-worldcat' in raw.properties) {
        const href = raw.properties['catafolk-worldcat']
        const btn = `<a class="badge badge-pill badge-light d-inline" href="${href}" target="_blank">Worldcat</a>`
        elements.push(btn)
      }

      const output = ` ${elements.join(' ')}`
      return output
    },
  })

  return (
    <Bibliography dangerouslySetInnerHTML={{__html: output}} {...options} />
  )

  // return (
  //   <div className={`${styles.bibliography} ${styles.bibliographyCol2}`}>
  //     {bibliography.data.map(json => {
  //       const item = new Cite(json);
  //       return <BibliographyItem item={item} key={item.data.id} />
  //     })}
  //   </div>   
  // )
}