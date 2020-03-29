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
  },
  plugins: [
    {
      resolve: `gatsby-source-filesystem`,
      options: {
        name: `datasets`,
        path: `${__dirname}/../datasets/`,
        ignore: ['**/data/*', '**/config.json']
      }
    },
    {
      resolve: `gatsby-transformer-csv`,
      options: {
        typeName: 'Song'
      }
    },
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
    }
  ]
}
