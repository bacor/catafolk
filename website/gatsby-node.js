const path = require(`path`)
const fs = require('fs');
const _ = require('lodash');
const parse = require('csv-parse/lib/sync');
const { createFilePath } = require(`gatsby-source-filesystem`);

// Options
const indexSchemaFn = `${__dirname}/../index-schema.csv`;
const datasetSchemaFn = `${__dirname}/../dataset-schema.graphql`;

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


exports.createSchemaCustomization = ({ actions, schema }) => {
  const { createTypes } = actions
  // Load schema from file schema.graphql
  const datasetSchema = fs.readFileSync(datasetSchemaFn, {encoding: 'utf-8'})
  createTypes(datasetSchema)

  // Load index sch
  const indexSchemaCSV = fs.readFileSync(indexSchemaFn, {encoding: 'utf-8'})
  const indexSchema = parse(indexSchemaCSV, { columns: true })
  const fields = _.fromPairs(indexSchema.map(entry => [entry.field, entry.graphql_type]))
  const typeDefs = [
    schema.buildObjectType({
      name: "IndexCsv",
      fields: fields,
      interfaces: ["Node"],
      extensions: { infer: false }
    }),
  ]
  createTypes(typeDefs)
}