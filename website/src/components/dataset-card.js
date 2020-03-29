import React from "react"
import { Link } from "gatsby"
import _ from 'lodash';
import Markdown from 'react-markdown'

import Card from 'react-bootstrap/Card';
import TagList from "../components/tag-list"

function DatasetCard({ dataset }) {
  return (
    <Card key={dataset.dataset_id}>
      <Card.Body>
        <Card.Title>{dataset.title || _.startCase(dataset.dataset_id)}</Card.Title>
        <Markdown source={dataset.description} className="card-text" />
        {
          dataset.tags.length > 0 
            ? <TagList tags={dataset.tags} className="mb-3" />
            : null
        }
        <Link to={`/${dataset.fields.slug}`} className="btn btn-dark">View {dataset.dataset_id}</Link>
      </Card.Body>
    </Card>
  )
}

export default DatasetCard;