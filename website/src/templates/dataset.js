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

function Licence({ abbreviation, name, url, unknown }) {
  if(unknown) return <span className="text-danger">Unknown</span>;
  return (
    <a href={url} target="_blank" title={name}>{abbreviation}</a>
  )
}

function DatasetPropsCard({dataset}) {
  let footer;
  if(!dataset.licence || !dataset.copyright) {
    footer = (
      <>
        Some info is missing... 
        Please consider <a href={`${dataset.github_directory}/dataset.yml`}>contributing</a> on GitHub.
      </>
    )
  }

  return (
    <PropsCard title="Properties" footer={footer}>
      {dataset.authors && (
        <Prop title="Authors"><People people={dataset.authors} /></Prop>)}
      {dataset.contributors && (
        <Prop title="Contributors"><People people={dataset.contributors} /></Prop>)}
      {dataset.copyright && (
        <Prop title="Copyright">{dataset.copyright}</Prop>)}
      {dataset.licence && (
        <Prop title="Licence"><Licence {...dataset.licence} /></Prop>)}
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
  let hasReadme = 'readme' in dataset;
  if(hasReadme) hasReadme = dataset.readme.file.wordCount.words > 0;
  console.log(dataset.readme)
  // const defaultContent = (
  //   <Card.Body>
  //     <Card.Title>Contribute!</Card.Title>
  //     <p>
  //       This dataset has no readme yet, describing how to download or use the dataset. <br/> 
  //       Are you familiar with this dataset? 
  //       Please consider <a className="text-dark">contributing</a>.
  //     </p>
  //     <Button variant="light" href={`${dataset.github_directory}/README.md`}>Edit me on GitHub!</Button>
  //   </Card.Body>
  // );
  // return (
  //   <div className="row mt-5">
  //     <Card bg="secondary" text="light" className="w-100 text-center">
  //       <Card.Header>Read me</Card.Header>
  //       {hasReadme ? <Card.Body>{dataset.readme.file.html}</Card.Body> : defaultContent}
  //       </Card>
  //     </div>
  // );

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

function Sources({ bibliography }) {
  return (
    <Card>
      <Card.Header>Sources</Card.Header>
      <Card.Body>
        <Bibliography bibliography={bibliography} />
      </Card.Body>
    </Card>
  )
}

export default ({ data }) => {
  const dataset = data.metadata
  dataset.github_directory = '#'
  dataset.raw_index_url = '#'
  dataset.index = data.index
  dataset.readme = data.readme

  // console.log('asdfasdf', data)

  // Generate citation keys for all items
  const bibtex = data.sources.content
  const bibliography = new Cite(bibtex)
  const sourceKeys = data.index.source_keys
  const hasSources = (sourceKeys.length > 0 && sourceKeys !== [''])

  const citations = {}
  sourceKeys.forEach(key => {
    const citation = bibliography.format('citation', {entry: key})
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
        Cell: ({cell}) => <TruncatedCell cell={cell} maxLength={40} />,
      },
      {
        Header: 'Source',
        id: 'source',
        accessor: (row) => {
          if(!row.source_key) return null;
          const citation = citations[row.source_key]
          const pageNum = row.source_page_num
          return `${citation.slice(1, -1)}${ pageNum && `, p. ${pageNum}`}`
        },
        Cell: ({cell}) => <TruncatedCell cell={cell} maxLength={25} />
      },
      {
        Header: 'Location',
        accessor: 'location',
        Cell: ({cell}) => <TruncatedCell cell={cell} maxLength={30} />
      },
      {
        Header: 'Genre',
        accessor: 'genre',
        Cell: ({cell}) => <TruncatedCell cell={cell} maxLength={30} />
      },
      {
        Header: 'Meter',
        accessor: 'meter',
        width: 30
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
            <DatasetPropsCard dataset={dataset} />
            <Technicalities dataset={dataset} />
          </CardDeck>
        </Row>
        <Row className="mt-5">
          <Readme dataset={dataset} />
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
        <Row>
          <CardDeck className="w-100">
            {hasSources && <Sources bibliography={bibliography} twoColumns={false} />}
            {hasIssues && <Issues issues={dataset.issues} />}
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
      dataset_url
      tags
      description
      files
      formats
      authors {
        name
        role
        url
      }
      contributors {
        name
      }
      copyright
      licence {
        unknown
        name
        abbreviation
        url
      }
      show_columns
      issues {
        title
        description
      }
    }
    index: allSong(filter: {dataset_id: {eq: $dataset_id}}) {
      songs: nodes {
        id
        checksum
        collection_date
        collector
        copyright
        culture
        encoding_date
        encoder
        format
        genre
        has_lyrics
        has_music
        ambitus
        catalogue_number
        encoder
        key
        language
        language_iso
        location
        latitude
        license_abbr
        longitude
        meter
        metric_classification
        modality
        path
        performer
        preview_url
        source
        source_author
        source_address
        source_key
        source_date
        source_page_num
        source_publisher
        source_song_num
        source_title
        source_url
        title_eng
        title
        url
        version
      }
      source_keys: distinct(field: source_key)
    }
    readme: file(relativeDirectory: {eq: $dataset_id}, name: {eq: "README"}) {
      file: childMarkdownRemark{
        rawMarkdownBody
        wordCount {
          words
        }
      }
    }
    sources: rawCode(name: {eq: "sources"}) {
      content
    }
  }`