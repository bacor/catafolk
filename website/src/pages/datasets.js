import React from "react"
import { graphql, Link } from "gatsby"
import Layout from "../components/layout"
import _ from 'lodash';
import Markdown from 'react-markdown'
import { IoIosArrowForward } from "react-icons/io";
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Jumbotron from 'react-bootstrap/Jumbotron';

const DatasetRow = ({ dataset }) => {
  return (<tr>
    <th scope="row">
      {dataset.title || _.startCase(dataset.dataset_id)}
    </th>
    <td><Markdown source={dataset.description} /></td>
    <td>{dataset.files}</td>
    <td>
      <Link to={`/${dataset.fields.slug}`} className="btn btn-outline-secondary btn-sm">
        {dataset.dataset_id}  <IoIosArrowForward />
      </Link>
    </td>
  </tr>)
}

export default ({ data }) => {
  return   (
    <Layout pageName="datasets">
      <Container>
        <Row className="mt-5">
          <Jumbotron className="col-12">
            <h1 className="display-4">Datasets</h1>
            <p className="lead w-75">
            A list of all datasets in Catafolk
            </p>
          </Jumbotron>
        </Row>
        <Row>
          <div className="card w-100">
            <div className="card-header">
              Analyzed datasets
            </div>
            <div className="card-body">
              <table className="table table-responsive-md table-hover small">
              <thead>
                  <tr>
                  <th scope="col">Title</th>
                  <th scope="col" className="w-50">Description</th>
                  <th scope="col">Songs</th>
                  <th scope="col">ID</th>
                  </tr>
              </thead>
              <tbody>
                {
                  data.allDataset.edges.map(edge => (
                    <DatasetRow dataset={edge.node} key={edge.node.dataset_id} />
                  ))
                }
              </tbody>
              </table>
            </div>
          </div>
        </Row>
      </Container>
    </Layout>
  )
}

export const query = graphql`
  query {
    allDataset {
      edges {
        node {
          dataset_id
          files
          description
          fields {
            slug
          }
        }
      }
    }
  }`