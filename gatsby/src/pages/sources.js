import React from "react";
import { useStaticQuery, graphql } from "gatsby";

import Card from 'react-bootstrap/Card';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Jumbotron from 'react-bootstrap/Jumbotron';
import Cite from 'citation-js';

import Layout from "../components/layout";
import Bibliography from "../components/bibliography"

export default () => {
  const bibtexFile = useStaticQuery(graphql`{
    file: rawCode(name: {eq: "sources"}) {
      content
    }
  }`);
  const bibliography = new Cite(bibtexFile.file.content)

  return   (
    <Layout pageName="datasets">
      <Container>
        <Row className="mt-5">
          <Jumbotron className="col-12">
            <h1 className="display-4">Sources</h1>
            <p className="lead w-75">
            </p>
          </Jumbotron>
        </Row>
        <Row>
          <Card className="w-100">
            <Card.Header>Sources</Card.Header>
            <Card.Body>
              <Bibliography bibliography={bibliography} twoColumns={true} />
            </Card.Body>
          </Card>
        </Row>
      </Container>
    </Layout>
  )
}

// export const query = graphql`
//   query {
//     allDataset {
//       edges {
//         node {
//           dataset_id
//           num_files
//         }
//       }
//     }
//   }`