import React from "react"
import { graphql, Link } from "gatsby"
import Layout from "../components/layout"
import _ from 'lodash';
import Markdown from 'react-markdown'
import { IoIosArrowForward } from "react-icons/io";
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Jumbotron from 'react-bootstrap/Jumbotron';
import Badge from 'react-bootstrap/Badge';

function StatusBadge({ value, ...props }) {
  const colors = {
    beta: 'success',
    alpha: 'info',
    draft: 'secondary'
  }
  let color;
  if(value in colors) {
    color = colors[value]
  } else {
    color = 'muted'
  }
  return <Badge pill variant={color} {...props}>{value}</Badge>
}

const DatasetRow = ({ dataset }) => {
  console.log(dataset)
  return (<tr>
    <th scope="row">
      {dataset.title || _.startCase(dataset.dataset_id)}
    </th>
    <td><StatusBadge value={dataset.status} /></td>
    <td>{dataset.group_ids ? dataset.group_ids.join(', ') : ''}</td>
    <td><Markdown source={dataset.description} /></td>
    <td>{dataset.num_entries}</td>
    <td>
      <Link to={`/${dataset.fields.slug}`} className="btn btn-secondary btn-sm">
        <span style={{whiteSpace: 'nowrap'}}>View <IoIosArrowForward /></span>
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
                  <th scope="col">Status</th>
                  <th scope="col">Groups</th>
                  <th scope="col" className="w-50">Description</th>
                  <th scope="col">Songs</th>
                  <th scope="col"></th>
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
          title
          status
          dataset_id
          group_ids
          num_entries
          description
          fields {
            slug
          }
        }
      }
    }
  }`