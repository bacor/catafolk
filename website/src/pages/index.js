import React from "react"
import { graphql, Link } from "gatsby"
import _ from 'lodash';
import Card from 'react-bootstrap/Card';
import CardColumns from 'react-bootstrap/CardColumns';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Jumbotron from 'react-bootstrap/Jumbotron';
import Layout from "../components/layout"
import DatasetCard from "../components/dataset-card";

export default ({ data }) => {
  return (
    <Layout>
      <Container className="mt-5">
        <Row>
          <Jumbotron className="w-100">
            <div  style={{ maxWidth: '700px' }}>
              <h1 className="display-4">Catafolk</h1>
              <p className="lead">
                A catalogue of folk music corpora for computational ethnomusicology
              </p>
              <hr className="my-4" />
              <p>
                The project aims to make cross-cultural music corpora more easily accessible.
                It is a catalogue of music corpora, but also an index of songs in
                those corpora, providing metadata in a consistent format.
                We hope the project contributes to diversifying computational music research 
                and to the creation of large, cross-cultural musical corpora.              
              </p>
            </div> 
          </Jumbotron>
        </Row>
        <Row className="mt-4">
          <CardColumns>
            {data.allCorpus.edges.map(node => (
              <DatasetCard dataset={node.dataset} key={node.dataset.dataset_id} />
            ))}
            <Card bg="dark" text="light">
              <Card.Body>
                <Card.Title>And more...</Card.Title>
                <Card.Text>
                  Catafolk currently contains {data.total.totalCount} datasets.
                  <Link to="/datasets/" className="btn btn-light mt-3">View all datasets</Link>
                </Card.Text>
              </Card.Body>
            </Card>
          </CardColumns>
        </Row> 
      </Container>
    </Layout>
  )
}

export const query = graphql`{
  allCorpus(filter: {dataset_id: {in: [
    "finnish-folk-tunes",
    "essen-deutschl-erk",
    "densmore-teton-sioux",
    "densmore-ojibway",
    "sagrillo-lorraine",
    "sagrillo-luxembourg",
    "creighton-nova-scotia",
    "natural-history-of-song"
  ]}}) {
    edges {
      dataset: node {
        dataset_id
        description
        fields {
          slug
        }
        title
        tags
      }
    }
  }
  total: allCorpus {
    totalCount
  }
}`
