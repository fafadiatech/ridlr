import React, { useState } from 'react';
import {Alert, Navbar, NavbarBrand, NavbarToggler, Collapse, Nav, NavbarText, Button, Progress, Container, Row, Col, Label, Input} from 'reactstrap';
import Markdown from 'react-markdown';
import Countdown from "react-countdown";
import {getRequest} from './utils';

const Completionist = () => <span>Done!</span>;

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isOpen: false,
      questions: [],
      timer: 0,
    }
  }

  toggle = () => {
    var current = this.state.isOpen;
    this.setState({isOpen: !current});
  }

  doneFetchingQuestions = (data) => {
    console.log("done fetching questions");
    this.setState({timer: data.time_limit})
    console.log(data.time_limit);
  }

  fetchQuestions = () => {
    console.log("cool nice!");
    getRequest("http://localhost:8001/api/v1/questions/?invitation_code=12345", this.doneFetchingQuestions);
  }

  componentDidMount(){
    this.fetchQuestions()
  }

  render() {
    return (
      <div className="App">
        <Progress striped value="75" />
        <Navbar color="light" light expand="md">
                <NavbarBrand href="/">Ridlr</NavbarBrand>
                <NavbarToggler onClick={this.toggle} />
                <Collapse isOpen={this.state.isOpen} navbar>
                  <Nav className="mr-auto" navbar>
                  </Nav>
                  <NavbarText>
                    Time Left:{' '}
                    <Countdown date={Date.now() + (1000 * this.state.timer * 60)}>
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
}

export default App;
