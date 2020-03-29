import React from "react"
import { graphql, Link } from "gatsby"
import _ from 'lodash';
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Jumbotron from 'react-bootstrap/Jumbotron'
import {IoIosArrowForward} from "react-icons/io";
import Layout from "../components/layout"

export default ({ data }) => {
  return   (
    <Layout>
      <Container>
        <Row className="mt-5">
          <Jumbotron className="col-12">
            <h1 className="display-4">Page not found...</h1>
            <p className="lead w-75">Something went wrong</p>
            <Link to='/' className="btn btn-dark">Go back to the homepage <IoIosArrowForward /></Link>
          </Jumbotron>
        </Row>
      </Container>
    </Layout>
  )
}