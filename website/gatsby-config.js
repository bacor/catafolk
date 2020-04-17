/**
 * Configure your Gatsby site with this file.
 *
 * See: https://www.gatsbyjs.org/docs/gatsby-config/
 */
// const path = require(`path`)
// const { typeNameFromDir, typeNameFromFile } = require("gatsby-transformer-csv")

module.exports = {
  pathPrefix: "/catafolk",
  siteMetadata: {
    title: `Catafolk`,
    github: `https://github.com/bacor/catafolk`,
    website: `https://bacor.github.io/catafolk`,
  },
  plugins: [
    {
      resolve: `gatsby-source-filesystem`,
      options: {
        name: `index`,
        path: `${__dirname}/../datasets/`,
        // You can use anymatch https://github.com/micromatch/anymatch
        ignore: ['**/data/*', '**/config.json', '**/additional-metadata.csv']
      }
    },
    `gatsby-transformer-csv`,
    // {
    //   resolve: `gatsby-transformer-csv`,
    //   options: {
    //     name: 'index',
    //     typeName: 'Song'
    //   }
    // },
    {
      resolve: 'gatsby-transformer-yaml',
      options: {
        typeName: 'Dataset'
      }
    },
    'gatsby-transformer-remark',
    {
      resolve: `gatsby-source-filesystem`,
      options: {
        name: `bibliography`,
        path: `${__dirname}/../bibliography`
      }
    },
    {
      resolve: `gatsby-transformer-code`,
      options: {
        name: `bibliography`,
        extensions: ['bib']
      }
    },
    // Load schema
    {
      resolve: `gatsby-source-filesystem`,
      options: {
        name: `schema`,
        path: `${__dirname}/../catafolk/`,
        ignore: [`${__dirname}/../catafolk/!(schema.csv)`]
      }
    }
  ]
}
