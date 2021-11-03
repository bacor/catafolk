import React from "react"
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import { Link } from "gatsby"

import 'bootstrap/dist/css/bootstrap.min.css';

export default ({ children, pageName }) => {
  return (
    <div>
      <Navbar className="navbar navbar-expand-lg navbar-light bg-light border-bottom">
        <Container>
          <div className="navbar-brand mr-1">
            <Link to="/" className="navbar-brand mr-0">
              <strong>Catafolk</strong>
            </Link>
            { pageName && `://${pageName}` }
          </div>
          <p className="small mt-3">
            <a className="badge badge-pill badge-danger text-light"
              data-toggle="tooltip" data-html="true" data-placement="right"
              title="Project in a very early stage">beta</a>
          </p>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="ml-auto">
              <Link to="/datasets/" className="nav-link" activeClassName="active">Corpora</Link>
              <Link to="/sources/" className="nav-link" activeClassName="active">Sources</Link>
              <Link to="/about/" className="nav-link" activeClassName="active">About</Link>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>

      {children}

      <div className="bg-light mt-5 py-5 border-top small">
        <div className="container">
          <div className="row">
            <div className="col-lg-3 col-md-5 my-2">
              <p>
                <a href="" className="text-dark"><strong>Catafolk</strong></a><br />
                A catalogue of folk music datasets for computational ethnomusicology
              </p>
              <hr />
              <p>
                Copyright  Bas Cornelissen <br/>
                <a href="http://www.mcg.uva.nl/" className="text-muted">Music Cognition Group</a> &amp;{' '}
                <a href="http://illc.uva.nl/clclab" className="text-muted">clclab</a><br />
                <a href="http://illc.uva.nl/" className="text-muted">ILLC</a>,{' '}
                <a href="http://uva.nl/" className="text-muted">University of Amsterdam</a>
              </p>
            </div>
            <div className="col-lg-2 col-md-3">
              <ul className="nav flex-column d-table d-md-block">
                <li className="nav-item d-inline d-md-block">
                  <Link to="/datasets/" className="nav-link d-inline-block pl-0 pl-md-3">Datasets</Link>
                </li>
                <li className="nav-item d-inline d-md-block">
                  <Link to="/about/" className="nav-link d-inline-block pl-0 pl-md-3">About</Link>
                </li>
                <li className="nav-item d-inline d-md-block">
                  <Link to="/sources/" className="nav-link d-inline-block pl-0 pl-md-3">Sources</Link>
                </li>
                <li className="nav-item d-inline d-md-block">
                  <a className="nav-link d-inline-block pl-0 pl-md-3" href="https://github.com/">Github</a>
                </li>
              </ul>
            </div>
            <div className="col-lg-4 offset-lg-3 col-md-4 d-none d-md-block">
              <div className="card bg-dark text-light">
                <div className="card-header d-md-none d-lg-block">Project in infancy</div>
                <div className="card-body">
                  <p>
                  This project is in its infancy: many things are still likely to change.
                  If you are interested in the project, or want to contribute, please get in touch.
                  Your comments and suggestions are also very welcome.
                  </p>
                  <a className="btn btn-danger btn-sm">Get in touch</a>
                </div>
              </div>
            </div>
            
          </div>
        </div>
      </div>
    </div>
  )
}