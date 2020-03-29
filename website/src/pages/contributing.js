import React from "react"
import { graphql, Link } from "gatsby"
import Layout from "../components/layout"
import _ from 'lodash';
import Markdown from 'react-markdown'
import { IoIosArrowForward } from "react-icons/io";

export default ({ data }) => {
  return   (
    <Layout>
      <div className="jumbotron row">
        <div className="w-100">
          <h1 className="display-4">Contributing</h1>
          <p className="lead w-75">
          How to contribute to Catafolk
          </p>
        </div>
      </div>
      <div className="row mt-5">
        <div className="card w-100">
          <div className="card-body">
            To do
          </div>
        </div>
      </div>
    </Layout>
  )
}