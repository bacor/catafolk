/**
 * Configure your Gatsby site with this file.
 *
 * See: https://www.gatsbyjs.org/docs/gatsby-config/
 */
const { min } = require("lodash");
const path = require(`path`)
const yaml = require('js-yaml');
const fs   = require('fs');
// const { typeNameFromDir, typeNameFromFile } = require("gatsby-transformer-csv")

// Load configuration file
const configFn = './catafolk-config.yml';
const catafolkConfig = yaml.load(fs.readFileSync(configFn, 'utf8'));
const schemaDir = catafolkConfig['schemaDir'];
const registryDir = catafolkConfig['registryDir'];
const excludedCorpora = catafolkConfig['excludedCorpora']; 

// Filenames that should be included
allowedCorpusFiles = [
  'index.csv',
  'corpus.yml',
  'README.md',
  'readme.md',
  'groups.yml'
]

module.exports = {
  pathPrefix: "/catafolk",
  siteMetadata: {
    title: `Catafolk`,
    github: `https://github.com/bacor/catafolk`,
    website: `https://bacor.github.io/catafolk`,
  },
  plugins: [
    // Load all corpora from the registry
    {
      resolve: `gatsby-source-filesystem`,
      options: {
        path: `${registryDir}/corpora/`,
        ignore: [
          // Note: you can use anymatch https://github.com/micromatch/anymatch
          '**/data/*', 
          '**/src/*',

          // Excluded datasets
          ...excludedCorpora.map(id => `**/${id}/*`),
          
          // Ignore all files that are not in allowedCorpusFiles
          string => {
            const basename = path.basename(string)
            const isVersionDir = basename.match(/\d+\.\d+\.\d+/) !== null
            const isFile = path.extname(string) !== '' && !isVersionDir
            const isAllowed = allowedCorpusFiles.includes(basename)
            return isFile && !isAllowed
          }
        ]
      }
    },
    // Load schema
    {
      resolve: `gatsby-source-filesystem`,
      options: {
        name: `schema`,
        path: schemaDir,
        ignore: [`${schemaDir}/!(index-schema.csv)`]
      }
    },
    // Load all bibtex files 
    {
      resolve: `gatsby-source-filesystem`,
      options: {
        name: `bibliography`,
        path: `${registryDir}/bibliography`
      }
    },
    {
      resolve: `gatsby-transformer-code`,
      options: {
        name: `bibliography`,
        extensions: ['bib']
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
    // 'gatsby-transformer-yaml',
    {
      resolve: 'gatsby-transformer-yaml',
      options: {
        // Create one node type for every filename
        // So all dataset.yml files will have type Dataset
        typeName: ({ node }) => node.name
      }
    },
    'gatsby-transformer-remark'
  ]
}
