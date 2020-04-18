const path = require(`path`)
const { createFilePath } = require(`gatsby-source-filesystem`)

exports.onCreateNode = ({ node, getNode, actions }) => {
  const { createNodeField } = actions
  if (node.internal.type === 'dataset') {
    const slug = `datasets/${node.dataset_id}/`
    createNodeField({node, name: 'slug', value: slug})
  } 
//   else if (node.internal.type == 'Song') {
//     // console.log(node)
// //       if (node.name.endsWith('-index')) {
// //         createNodeField({
// //             node,
// //             name: `dataset_id`,
// //             value: node.name.replace('-index', ''),
// //         })
// //       }
      
//   }
}

exports.createPages = async ({ graphql, actions }) => {
  const { createPage } = actions
  const result = await graphql(`
    query {
      allDataset {
        nodes {
          dataset_id
          fields {
            slug
          }
        }
      } 
    }
  `)
  result.data.allDataset.nodes.forEach((node) => {
    createPage({
      path: node.fields.slug,
      component: path.resolve(`./src/templates/dataset.js`),
      context: {
        // Data passed to context is available
        // in page queries as GraphQL variables.
        dataset_id: node.dataset_id
      },
    })
  })
}