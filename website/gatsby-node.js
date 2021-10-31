const path = require(`path`)
const fs = require('fs');
const _ = require('lodash');
const parse = require('csv-parse/lib/sync');
const { createFilePath } = require(`gatsby-source-filesystem`);

// Options
// Schemas probably have to move.
// const indexSchemaFn = `${__dirname}/../schemas/index-schema.csv`;
const indexSchemaFn = `./schemas/index-schema.csv`;
const corpusSchemaFn = `./schemas/corpus-schema.graphql`;

exports.onCreateNode = ({ node, getNode, actions }) => {
  const { createNodeField } = actions
  if (node.internal.type === 'corpus') {
    const slug = `datasets/${node.dataset_id}/${node.version}`
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
      allCorpus {
        nodes {
          dataset_id
          fields {
            slug
          }
        }
      } 
    }
  `)
  result.data.allCorpus.nodes.forEach((node) => {
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
  const corpusSchema = fs.readFileSync(corpusSchemaFn, {encoding: 'utf-8'})
  createTypes(corpusSchema)

  // Load index sch
  const indexSchemaCSV = fs.readFileSync(indexSchemaFn, {encoding: 'utf-8'})
  const indexSchema = parse(indexSchemaCSV, { columns: true })
  
  // Use custom types from the schema
  // TODO perhaps it is better to use custom extensions?
  // https://www.gatsbyjs.org/docs/schema-customization/#creating-custom-extensions
  // https://github.com/gatsbyjs/gatsby/issues/16174
  const fields = {}
  indexSchema.forEach(entry => {
    const fieldName = entry.field
    const fieldType = entry.dtype
    const fieldSpec = {}

    if(fieldType === 'boolean') {
      fieldSpec.type = 'Boolean'
      fieldSpec.resolve = source => {
        const value = source[fieldName]
        return value !== '' ? value === 'True' : null
      }

    } else if(fieldType == 'int') {
      fieldSpec.type = 'Int'
      fieldSpec.resolve = source => {
        const value = source[fieldName]
        return value === '' ? null : parseInt(value)
      }

    } else if(fieldType == 'string-list') {
      fieldSpec.type = '[String]'
      fieldSpec.resolve = source => {
        const value = source[fieldName]
        return (value === '' || value == undefined) ? [] : value.split('|');
      }

    } else if(fieldType === 'float') {
      fieldSpec.type = 'Float'
      fieldSpec.resolve = source => {
        const value = source[fieldName]
        return value === '' ? null : parseFloat(value)
      }

    // } else if(fieldType === 'date') {
    // TODO
    
    // Default: String
    } else {
      fieldSpec.type = 'String'
      fieldSpec.resolve = source => {
        const value = source[fieldName]
        return value === '' ? null : value
      }
    }

    fields[fieldName] = fieldSpec
  });
  
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