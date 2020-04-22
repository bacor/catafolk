import React from "react"
import Card from "react-bootstrap/Card"
import Row from "react-bootstrap/Row"
import _ from 'lodash';

function Prop({ title, children, visible, defaultValue, inRow, titleOptions, hasContent, ...options }) {
  const content = (defaultValue && (!children || hasContent === false)) 
    ? defaultValue : children;
  if(visible === false) {
    return null
  } else if(inRow === false) {
    return (
      <>
        <dt {...titleOptions}>{title}</dt>
        <dd {...options}>{content}</dd>
      </>
    )
  } else {
    return (
      <>
        <dt className="col-lg-3">{title}</dt>
        <dd className="col-lg-9" {...options}>{content}</dd>
      </>
    );
  }
}

function PropsList({ properties, title, children, asRow, ...options }) {
  if(asRow === false) {
    return <dl {...options}>{children}</dl>
  } else {
    return <Row as="dl" {...options}>{children}</Row>
  }
}

function PropsCard({ properties, title, children, footer, ...options}) {
  return (
    <Card>
      <Card.Header>{title}</Card.Header>
      <Card.Body>
        <PropsList>
          {children}
        </PropsList>
      </Card.Body>
      { 
        footer 
          ? <Card.Footer className="text-muted small">{footer}</Card.Footer>
          : null 
      }
    </Card>
  );
}

export {
  PropsCard,
  PropsList,
  Prop
}