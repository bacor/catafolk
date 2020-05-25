import React from "react"
import { useStaticQuery, graphql } from "gatsby"
import _ from 'lodash'
import Cite from 'citation-js';

import Markdown from 'react-markdown'
import {IoIosArrowForward} from "react-icons/io";

import Button from 'react-bootstrap/Button';
import Jumbotron from 'react-bootstrap/Jumbotron';
import CardDeck from 'react-bootstrap/CardDeck';
import Card from 'react-bootstrap/Card';

import Layout from "../components/layout"
import TagList from "../components/tag-list";
import People from "../components/people";
import { PropsCard, Prop } from "../components/properties";

import { 
  ChecksumCell,
  OptionsCell,
  TruncatedCell,
  RowHeaderCell,
  ExpanderCell,
  Index,
} from "../components/index";

import Row from 'react-bootstrap/Row';
import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col';

import Bibliography from "../components/bibliography"

const DatasetHeader = ({ dataset }) => {
  return (
    <Jumbotron className="w-100" key={`${dataset.dataset_id}-header`}>
      <div>
        <h1 className="display-4">{dataset.title || _.startCase(dataset.dataset_id)}</h1>
        <div className="lead" style={{maxWidth: 700 }}>
          {dataset.description 
            ? <Markdown source={dataset.description} />
            : <span className="text-muted">This dataset has no description yet...</span>}
        </div>
        <TagList tags={dataset.tags} variant="dark" className="mb-4" />
        <Button variant="dark" href={dataset.dataset_url} className="mr-2">
           Go to dataset <IoIosArrowForward />
         </Button>
         <Button variant="outline-secondary" href={`${dataset.github_directory}/index.csv`}>
           View full index <IoIosArrowForward />
         </Button>
      </div>
    </Jumbotron>
  )
}

function License({ abbreviation, name, url, text, unknown }) {
  console.log('ASDFASDFAS', abbreviation, name, url, unknown, text)
  if(unknown) {
    return <span className="text-danger">Unknown</span>;
  } else {
    return (
      <>
        <a href={url} target="_blank" className="bold" title={name}>{name}</a>.
        {text ? <><br /><span>{_.truncate(text, {length: 200})}</span></> : null}
      </>
    )
  }

  return (
    <a href={url} target="_blank" title={name}>{abbreviation}</a>
  )
}

function DatasetPropsCard({dataset, bibliography}) {
  return (
    <PropsCard title="Properties">
      <Prop title="Dataset ID" ><code className="text-muted">{dataset.dataset_id}</code></Prop>
      {dataset.version && (
        <Prop title="Version"><code className="text-muted">{dataset.version}</code></Prop>)}
      {dataset.authors && (
        <Prop title="Authors"><People people={dataset.authors} /></Prop>)}

      {dataset.contributors && (
        <Prop title="Contributors"><People people={dataset.contributors} /></Prop>)}
      
      <Prop title="Citation">
        {dataset.dataset_citation_keys.map(key => {
          const citation = bibliography.format('citation', {entry: key})
          return citation.slice(1, -1)
        }).join('; ')}
      </Prop>

      <Prop title="Sources">
        {dataset.publication_citation_keys.map(key => {
          const citation = bibliography.format('citation', {entry: key})
          return citation.slice(1, -1)
        }).join('; ')}
      </Prop>
      
      {dataset.copyright && (
        <Prop title="Copyright">
          <Markdown source={dataset.copyright} />
        </Prop>)}

      {dataset.license && (
        <Prop title="License"><License {...dataset.license} /></Prop>)}
      
      {dataset.formats && (
        <Prop title="Formats"><TagList tags={dataset.formats} variant="secondary" /></Prop>)}
    </PropsCard>
  );
}

function Technicalities({ dataset }) {
  return (
    <PropsCard title="Technicalities">
      <Prop title="Dataset ID" ><code className="text-muted">{dataset.dataset_id}</code></Prop>
      {dataset.version && (
        <Prop title="Version"><code className="text-muted">{dataset.version}</code></Prop>)}
      <Prop title="Checksum">
        {dataset.checksum 
          ? <code className="text-muted">{dataset.checksum}</code> 
          : 'Not available'}
      </Prop>
      {dataset.formats && (
        <Prop title="Format"><TagList tags={dataset.formats} variant="secondary" /></Prop>)}
      <Prop title="Songs">{dataset.files}</Prop>
    </PropsCard>
  );
}

const Readme = ({ dataset }) => {
  let hasReadme = dataset.readme !== null
  if(hasReadme) hasReadme = dataset.readme.file.wordCount.words > 0;

  if(hasReadme) {
    return (
      <Card className="w-100">
        <Card.Header>Read me</Card.Header>
        <Card.Body>  
          <Markdown source={dataset.readme.file.rawMarkdownBody} />
        </Card.Body>
      </Card>
    )
  } else {
    return (
      <Card bg="secondary" text="light" className="w-100 text-center">
        <Card.Header>No readme yet...</Card.Header>
        <Card.Body>
          <Card.Title>Contribute!</Card.Title>
          <p>
            This dataset has no readme yet, describing how to download or use the dataset. <br/> 
            Are you familiar with this dataset? 
            Please consider <a className="text-dark">contributing</a>.
          </p>
          <Button variant="light" href={`${dataset.github_directory}/README.md`}>Edit me on GitHub!</Button>
        </Card.Body>
      </Card>
    );
  }
}

function Issue({ issue }) {
  return (
    <>
      <dt>{issue.title}</dt>
      <dd><Markdown source={issue.description} /></dd>
    </>
  )
}

function Issues({ issues }) {
  return (
    <Card className="border-danger" bg="light">
      <Card.Header>Issues</Card.Header>
      <Card.Body>
        <dl className="small">
          {issues.map(issue => <Issue issue={issue} key={issue.title} />)}
        </dl>
      </Card.Body>
    </Card>
  )
}

function Sources({ bibliography, ...opts }) {
  return (
    <Card>
      <Card.Header>References</Card.Header>
      <Card.Body>
        <Bibliography bibliography={bibliography} {...opts} />
      </Card.Body>
    </Card>
  )
}

export default ({ data }) => {
  const dataset = data.metadata

  dataset.github_directory = `${data.site.siteMetadata.github}/tree/master/datasets/${dataset.dataset_id}`
  dataset.raw_index_url = '#'
  dataset.index = data.index
  dataset.readme = data.readme

  // Generate citation keys for all items
  const bibtex = data.sources.nodes.map(node => node.content).join("\n")
  const bibliography = new Cite(bibtex)
  let sourceKeys = data.index.source_keys
  sourceKeys.push(...dataset.dataset_citation_keys)
  sourceKeys.push(...dataset.publication_citation_keys)
  sourceKeys = _.uniq(sourceKeys)
  const hasSources = (sourceKeys.length > 0 && sourceKeys !== [''])
  const citations = {}
  sourceKeys.forEach(key => {
    let citation
    try {
      citation = bibliography.format('citation', {entry: key})
    } catch (e) {
      console.warn(`An error occured while formatting citation ${key}`, e)
      citation = key
    }
    citations[key] = citation
  })
  const cited = bibliography.data.filter(entry => entry.id in citations)
  bibliography.data = cited
  
  const showColumns = dataset.show_columns || []
  
  const indexColumns = React.useMemo(
    () => [
      {
        // Make an expander cell
        Header: () => null, // No header
        id: 'expander', // It needs an ID
        Cell: ExpanderCell,
        Filter: false,
        Sort: false,
      },
      {
        Header: 'ID',
        accessor: 'id',
        Cell: RowHeaderCell,
        width: 50,
      },
      {
        Header: 'Options',
        accessor: row => {
          const hasPreview = row.preview_url !== undefined;
          const hasUrl = row.url !== undefined;
          const hasCode = row.source_url !== undefined;
          return `${hasPreview}${hasUrl}${hasCode}`
        },
        id: "options",
        Cell: OptionsCell,
        Filter: false,
        width: 50,
      },
      {
        Header: 'Num',
        accessor: 'source_song_num',
        width: 20,
      },
      {
        Header: 'Title',
        accessor: 'title',
        Cell: ({cell}) => <TruncatedCell cell={cell} maxLength={80} />,
      },
      {
        Header: 'Source',
        id: 'source',
        accessor: (row) => {
          if(!row.source_key) return null;
          const citation = citations[row.source_key]
          const pageNum = row.source_page_num
          if(citation) {
            return `${citation.slice(1, -1)}${ pageNum ? `, p. ${pageNum}` : ''}`
          } else {
            return `${row.source_key}${ pageNum ? `, p. ${pageNum}` : ''}`
          }
        },
        Cell: ({cell}) => <TruncatedCell cell={cell} maxLength={25} />
      },
      {
        Header: 'Location',
        accessor: 'location',
        Cell: ({cell}) => <TruncatedCell cell={cell} maxLength={30} />
      },
      {
        Header: 'Collectors',
        accessor: 'collector',
        Cell: ({cell}) => <TruncatedCell cell={cell} maxLength={30} />
      },
      {
        Header: 'Culture',
        accessor: 'culture',
        Cell: ({cell}) => <TruncatedCell cell={cell} maxLength={30} />
      },
      {
        Header: 'Language',
        accessor: 'language',
        Cell: ({cell}) => <TruncatedCell cell={cell} maxLength={30} />
      },
      {
        Header: 'Genre',
        accessor: 'genres',
        Cell: ({cell}) => <TruncatedCell cell={cell} maxLength={30} />
      },
      {
        Header: 'Meters',
        accessor: 'meters',
        Cell: ({cell}) => <TruncatedCell cell={cell} maxLength={30} />
      },
      {
        Header: 'Key',
        accessor: 'key',
        width: 30
      },
      {
        Header: 'Ambitus',
        accessor: 'ambitus',
        width: 30
      },
      {
        Header: 'md5',
        accessor: 'checksum',
        Cell: ChecksumCell,
        width: 20
      }
    ],
    []
  );
  const indexData = React.useMemo(() => dataset.index.songs)

  const hasIssues = dataset.issues !== null

  return (
    <Layout pageName={dataset.dataset_id}>
      <Container>
        <Row className="mt-5">
          <DatasetHeader dataset={dataset}/>
        </Row>
        <Row>
          <CardDeck>
            <DatasetPropsCard dataset={dataset} bibliography={bibliography} />
            {/* <Technicalities dataset={dataset} /> */}
            {hasIssues && <Issues issues={dataset.issues} />}
          </CardDeck>
        </Row>
      </Container>
      
      <Container className="mt-5">
        <Row>
        { dataset.index
          ? <Index columns={indexColumns} data={indexData} showColumns={showColumns} bibliography={bibliography} />
          : "None"
        }
        </Row>
      </Container>

      <Container className="mt-5">
        <Row className="mt-5">
          <Readme dataset={dataset} />
        </Row>
        <Row className="mt-5">
          <CardDeck className="w-100">
            {hasSources && <Sources bibliography={bibliography} twoColumns={true} />}
          </CardDeck>
        </Row>
      </Container>
    </Layout>
  );
}

export const query = graphql`
  query ($dataset_id: String!) {
    metadata: dataset(dataset_id: {eq: $dataset_id}) {
      title
      dataset_id
      status
      url
      tags
      description
      num_entries
      formats
      authors {
        name
        role
        url
      }
      contributors {
        name
        role
        url
      }
      credits
      dataset_citation_keys
      publication_citation_keys
      copyright
      license {
        unknown
        name
        text
        abbreviation
        url
      }
      show_columns
      hide_columns
      issues {
        title
        description
      }
    }
    index: allIndexCsv(filter: {dataset_id: {eq: $dataset_id}}) {
      songs: nodes {
        id
        title
        title_translation
        location
        latitude
        longitude
        auto_geocoded
        language
        glottolog_id
        culture
        culture_dplace_id
        culture_hraf_id
        genres
        performer: performers
        performer_genders
        instrumentation
        instrument_use
        percussion_use
        voice_use
        key: tonality
        modality: scale
        ambitus
        tempo
        meters
        metric_classification
        collector: collectors
        collection_date
        collection_date_earliest
        collection_date_latest
        source_key: publication_key
        publication_type
        publication_title
        publication_authors
        publication_date
        source_page_num: publication_page_num
        source_song_num: publication_song_num
        tune_family_id
        catalogue_num
        source_url: publication_preview_url
        encoder: encoders
        encoding_date
        contributors
        copyright
        license_id
        path: file_path
        file_format
        version
        checksum: file_checksum
        url: file_url
        preview_url: file_preview_url
        has_lyrics: file_has_lyrics
        has_music: file_has_music
        file_has_licence
        other_fields
        comments
        warnings
        description
        lyrics
        lyrics_translation
      }
      source_keys: distinct(field: publication_key)
    }
    readme: file(relativeDirectory: {eq: $dataset_id}, name: {eq: "README"}) {
      file: childMarkdownRemark{
        rawMarkdownBody
        wordCount {
          words
        }
      }
    }
    sources: allRawCode {
      nodes {
        content
      }
    }
    site {
      siteMetadata {
        github
      }
    }
  }`