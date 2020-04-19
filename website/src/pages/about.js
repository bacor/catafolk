import React from "react"
import { graphql, Link } from "gatsby"
import Layout from "../components/layout"
import _ from 'lodash';
import Markdown from 'react-markdown'
import { IoIosArrowForward } from "react-icons/io";

import Card from 'react-bootstrap/Card';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Jumbotron from 'react-bootstrap/Jumbotron';

import { Index } from "../components/index";

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
              Below you find a table with all fields used by Catafolk (its ontology).
            </p>
          </Jumbotron>
        </Row>
        <Row>
          <Index columns={indexColumns} data={indexData} />
        </Row>
        <Row className="mt-5">
          <Card className="w-100">
            <Card.Header>Technical</Card.Header>
            <Card.Body>
              Please refer to the <a href="https://catafolk.readthedocs.io/en/latest/">online documentation</a>.
            </Card.Body>
          </Card>
        </Row>
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