import React from "react"
import { graphql, Link } from "gatsby"
import Layout from "../components/layout"
import _ from 'lodash';
import Markdown from 'react-markdown'
import { IoIosArrowForward } from "react-icons/io";

import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Jumbotron from 'react-bootstrap/Jumbotron';

import { Index } from "../components/index";

import architectureImg from "../assets/architecture.png";
import pythonPackageImg from "../assets/python-package.png";
import registryImg from "../assets/registry.png";

export default ({ data }) => {
  const indexColumns = React.useMemo(
    () => [
      {
        Header: 'Field',
        accessor: 'field',
      },
      {
        Header: 'Group',
        accessor: 'group',
      },
      {
        Header: 'Required',
        accessor: 'required',
      },
      {
        Header: 'Description',
        accessor: 'description',
      },
      {
        Header: 'Data type',
        accessor: 'dtype',
      },
      {
        Header: 'Details',
        accessor: 'details',
      },
    ],
    []
  );
  const indexData = React.useMemo(() => data.fields.nodes)
  
  return   (
    <Layout pageName="datasets">
      <Container>
        <Row className="mt-5">
          <Jumbotron className="col-12">
            <h1 className="display-4">About</h1>
            <p className="lead w-75">
              Catafolk is a project that indexes cross-cultural music datasets 
              and serves metadata about these collections in a consistent, 
              easy-to-use format.
              We hope this project will help diversifying computational music 
              research and contribute to the creation of large, cross-cultural musical datasets.
            </p>
            <p>The project is still in an early stage.</p>
          </Jumbotron>
        </Row>
        <Row>
          <Col>
            <Card className="w-100 mb-5">
              <Card.Header>Architecture</Card.Header>
              <Card.Body>
                <img src={architectureImg} style={{ maxWidth: "500px", width: "100%"}} />
                <p>
                  Catafolk consists of three components.
                  First, there is the <a href="https://github.com/bacor/catafolk-registry">registry</a>, a repository that contains all the
                  metadata about all corpora and the songs therein. Second, 
                  the indices in the registry are generated using 
                  {` `}<a href="github.com/bacor/catafolk-python">the Python package</a>.
                  Third, there is the <a href="github.com/bacor/catafolk">website</a> (which you're looking at), that serves 
                  the registry via a graphical interface.
                  Central to all these three components is the Catafolk schema:
                  the list of metadata fields used by Catafolk. You can find
                  the index below.
                </p>
              </Card.Body>
            </Card>
          </Col>
          <Col>
            <Card className="w-100 mb-5">
              <Card.Header>Registry</Card.Header>
              <Card.Body>
                <img src={registryImg} style={{ maxWidth: "500px", width: "100%"}} />
                <p>
                  The registry is a Github repository that contains all metadata about
                  all corpora. For every corpus it contains at least two files:
                  a <code>corpus.yml</code> file with metadata about the entire corpus,
                  a <code>index.csv</code> file that contains metadata about every
                  song in the corpus using the Catafolk schema. Moreover, it can
                  incluce a <code>README.md</code> file, and a <code>src</code> 
                  directory containing Python code and whatever else is needed 
                  to generate the index. All corpora are versioned.
                </p>
                <Button variant="outline-secondary" href={`https://github.com/bacor/catafolk-registry`}>
                  Registry GitHub repository <IoIosArrowForward />
                </Button>
              </Card.Body>
            </Card>
          </Col>
        </Row>

        <Row>
          <Col>
            <Card className="w-100 mb-5">
              <Card.Header>Python package</Card.Header>
              <Card.Body>
                <img src={pythonPackageImg} style={{ maxWidth: "500px", width: "100%"}} />
                <p>
                  The Python package is primarily used to generate indices of 
                  corpora, and ensure it respects the schema. Indices are generated
                  by combining metadata from various sources: the source files,
                  perhaps some additional metadata source, some constants,
                  and automatically determined fields (checksums, filepaths, etc.).
                  These are then combined for every song in the corpus 
                  and the result is exported to a csv filed.
                </p>
                <Button variant="outline-secondary" href={`https://github.com/bacor/catafolk-python`}>
                  Python package repository <IoIosArrowForward />
                </Button>
              </Card.Body>
            </Card>
          </Col>
          
          <Col>
            <Card className="w-100 mb-5">
              <Card.Header>Contributing</Card.Header>
              <Card.Body>
                {/* <img src={architectureImg} style={{ maxWidth: "500px", width: "100%"}} /> */}
                <p>
                  To contribute corpora, you can submit a pull-request to the
                  {' '}<a href="https://github.com/bacor/catafolk-registry">registry</a>.
                  As a bare minimum, it needs to include a <code>corpus.yml</code>{' '}
                  and a <code>index.csv</code> file. But including a <code>README.md</code>
                  and a <code>src</code> directory with code used to generate
                  the index.
                </p>
                <p>
                  You can also contribute code, or simply play around with the website
                  and let us know what you think. Editing readme's or reporting
                  issues is also very valuable.
                </p>
                <p>
                  If you want to contribute in whatever way, feel free to get
                  in touch!
                </p>
                <Button variant="outline-secondary" href={`mailto:b.j.m.cornelissen@uva.nl`}>
                  Get in touch <IoIosArrowForward />
                </Button>
              </Card.Body>
            </Card>
          </Col>
        </Row>


        <Row>
          <Index columns={indexColumns} data={indexData} />
        </Row>
        {/* <Row className="mt-5">
          <Card className="w-100">
            <Card.Header>Technical</Card.Header>
            <Card.Body>
              Please refer to the <a href="https://catafolk.readthedocs.io/en/latest/">online documentation</a>.
            </Card.Body>
          </Card>
        </Row> */}
      </Container>
    </Layout>
  )
}

export const query = graphql`{
  fields: allIndexSchemaCsv {
    nodes {
      details
      description
      dtype
      field
      group
      required
    }
  }
}`