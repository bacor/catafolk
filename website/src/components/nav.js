import React from "react"
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import 'bootstrap/dist/css/bootstrap.min.css';

export default () => (
  <Navbar className="navbar navbar-expand-lg navbar-light bg-light sticky-top border-bottom">
    <Container>
      <div className="navbar-brand mr-1">
        <a className="navbar-brand mr-0" href="{{ site.baseurl }}/index.html">
          <strong>Catafolk</strong>
        </a>
      </div>
      <p className="small mt-3">
        <a className="badge badge-pill badge-danger text-light"
          data-toggle="tooltip" data-html="true" data-placement="right"
          title="Project in a very early stage">beta</a>
      </p>
      <Navbar.Toggle aria-controls="basic-navbar-nav" />
      <Navbar.Collapse id="basic-navbar-nav">
        <Nav className="ml-auto">
          <Nav.Link href="#home">Home</Nav.Link>
          <Nav.Link href="#link">Link</Nav.Link>
          <Nav.Link href="#link">Link</Nav.Link>
        </Nav>
      </Navbar.Collapse>
    </Container>
  </Navbar>
)