/**
 * Configure your Gatsby site with this file.
 *
 * See: https://www.gatsbyjs.org/docs/gatsby-config/
 */
const path = require(`path`)
// const { typeNameFromDir, typeNameFromFile } = require("gatsby-transformer-csv")

const excludedDatasets = [
  'bronson-child-ballads',
  'densmore-ojibway',
  'densmore-pawnee',
  // 'densmore-teton-sioux',
  // 'creighton-nova-scotia',
  // 'deutscher-liederhort',
  // 'essen-china-han',
  // 'essen-china-natmin',
  // 'essen-china-shanxi',
  // 'essen-china-xinhua',
  // 'natural-history-of-song',
  // 'sagrillo-ireland',
  // 'sagrillo-luxembourg',
  // 'sagrillo-scotland',
  // 'densmore-pueblo',
  // 'densmore-nootka',
  // 'finnish-folk-tunes'
];

// Filenames that should be included
allowedDatasetFiles = [
  'index.csv',
  'dataset.yml',
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
    {
      resolve: `gatsby-source-filesystem`,
      options: {
        // name: `index`,
        path: `${__dirname}/../datasets/`,
        // You can use anymatch https://github.com/micromatch/anymatch
        ignore: [
          '**/data/*', 
          '**/*.zip',
          '**/template.yml',
          
          // Ignore all files that are not in allowedDatasetFiles
          string => {
            const isFile = path.extname(string) !== ''
            const isAllowed = allowedDatasetFiles.includes(path.basename(string))
            return isFile && !isAllowed
          },
          
          // Excluded datasets
          ...excludedDatasets.map(id => `**/${id}/*`)
        ]
      }
    },
    // Load schema
    {
      resolve: `gatsby-source-filesystem`,
      options: {
        name: `schema`,
        path: `${__dirname}/../schemas`,
        ignore: [`${__dirname}/../schemas/!(index-schema.csv)`]
      }
    },
    // Load all bibtex files 
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
