import React, { useState } from 'react';
import {Alert, Navbar, NavbarBrand, NavbarToggler, Collapse, Nav, NavbarText, Button, Progress, Container, Row, Col, Label, Input} from 'reactstrap';
import Markdown from 'react-markdown';
import Countdown from "react-countdown";
import {getRequest} from './utils';

function doneFetchingQuestions(data){
  console.log("done fetching questions");
  console.log(data);
}

function fetchQuestions(){
  console.log("cool nice!");
  getRequest("http://localhost:8001/api/v1/questions/?invitation_code=12345", doneFetchingQuestions);
}

function App() {
  const [isOpen, setIsOpen] = useState(false);
  const toggle = () => setIsOpen(!isOpen);
  const Completionist = () => <span>Done!</span>;

  fetchQuestions()
  return (
    <div className="App">
      <Progress striped value="75" />
      <Navbar color="light" light expand="md">
              <NavbarBrand href="/">Ridlr</NavbarBrand>
              <NavbarToggler onClick={toggle} />
              <Collapse isOpen={isOpen} navbar>
                <Nav className="mr-auto" navbar>
                </Nav>
                <NavbarText>
                  Time Left:{' '}
                  <Countdown date={Date.now() + (1000 * 60 * 75)}>
                    <Completionist />
                  </Countdown>
                </NavbarText>&nbsp;&nbsp;
                <Button color="primary"> Prev </Button>&nbsp;
                <Button color="primary"> Next </Button>
              </Collapse>
        </Navbar>
        <Alert color="primary">This is cool!</Alert>
        <Container>
          <Row>
            <Markdown source="## Ut non tempor dolore sunt do cillum esse culpa dolor aute incididunt irure." /><br/><br/><br/>
          </Row>
          <Row>
            <Col xs="6">
              <Label check>
                <Input type="radio" name="radio1" />{' '}Option one is this and that—be sure to include why it's great
              </Label>
            </Col>
            <Col xs="6">
              <Label check>
                <Input type="radio" name="radio1" />{' '}Option one is this and that—be sure to include why it's great
              </Label>
            </Col>
          </Row>
          <Row>
            <Col xs="6">
              <Label check>
                <Input type="radio" name="radio1" />{' '}Option one is this and that—be sure to include why it's great
              </Label>
            </Col>
            <Col xs="6">
              <Label check>
                <Input type="radio" name="radio1" />{' '}Option one is this and that—be sure to include why it's great
              </Label>
            </Col>
          </Row>
        </Container>
    </div>
  );
}

export default App;
