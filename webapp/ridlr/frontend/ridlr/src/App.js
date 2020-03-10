import React from 'react';
import {Alert, Navbar, NavbarBrand, NavbarToggler, Collapse, Nav, NavbarText, Button, Progress, Container, Row, Col, Label, Input} from 'reactstrap';
import Markdown from 'react-markdown';
import Countdown from "react-countdown";
import {getRequest} from './utils';

const Completionist = () => <span>Done!</span>;

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      quizName: "",
      isOpen: false,
      questions: [],
      questionIndex: 0,
      currentQuestion: "",
      currentChoiceA: "",
      currentChoiceB: "",
      currentChoiceC: "",
      currentChoiceD: "",
      timer: 0,
    }
  }

  toggle = () => {
    var current = this.state.isOpen;
    this.setState({isOpen: !current});
  }

  doneFetchingQuestions = (data) => {
    console.log("done fetching questions");
    this.setState({quizName: data.quiz})
    this.setState({timer: data.time_limit})
    this.setState({questions: data.questions})
    this.setState({currentQuestion: data.questions[0].question})
    this.setState({currentChoiceA: data.questions[0].choices[0].choice})
    this.setState({currentChoiceB: data.questions[0].choices[1].choice})
    this.setState({currentChoiceC: data.questions[0].choices[2].choice})
    this.setState({currentChoiceD: data.questions[0].choices[3].choice})
    console.log(data);
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
                <NavbarBrand href="/">
                  Ridlr{' ' + this.state.quizName}
                </NavbarBrand>
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
              <Markdown source={`## ${this.state.currentQuestion}`} /><br/><br/><br/>
            </Row>
            <Row>
              <Col xs="6">
                <Label check>
                  <Input type="radio" name="radio1" />
                    {' '}
                    <Markdown source={this.state.currentChoiceA} />
                </Label>
              </Col>
              <Col xs="6">
                <Label check>
                  <Input type="radio" name="radio1" />
                    {' '}
                    <Markdown source={this.state.currentChoiceB} />
                </Label>
              </Col>
            </Row>
            <Row>
              <Col xs="6">
                <Label check>
                  <Input type="radio" name="radio1" />
                    {' '}
                    <Markdown source={this.state.currentChoiceC} />
                </Label>
              </Col>
              <Col xs="6">
                <Label check>
                  <Input type="radio" name="radio1" />
                    {' '}
                    <Markdown source={this.state.currentChoiceD} />
                </Label>
              </Col>
            </Row>
          </Container>
      </div>
    );
  }
}

export default App;
