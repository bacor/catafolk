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
                A catalogue of folk music datasets for computational ethnomusicology
              </p>
              <hr className="my-4" />
              <p>
                The project hopes to make datasets of folk music more easily accessible. 
                It provides a reference of datasets, but also aims to include some basic automatic analyses.
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
