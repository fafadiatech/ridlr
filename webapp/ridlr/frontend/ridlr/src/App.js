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
      alertType: "",
      showAlert: false,
      isOpen: false,
      questions: [],
      questionIndex: -1,
      currentQuestion: "",
      currentChoiceId: -1,
      correctChoiceId: 0,
      currentChoiceA: "",
      currentChoiceB: "",
      currentChoiceC: "",
      currentChoiceD: "",
      currentChoiceAId: 0,
      currentChoiceBId: 0,
      currentChoiceCId: 0,
      currentChoiceDId: 0,
      alertCaption: "",
      timer: 0,
    }
  }

  toggle = () => {
    var current = this.state.isOpen;
    this.setState({isOpen: !current});
  }

  loadNextQuestion = () => {
    this.setState({showAlert: false});
    this.setState({currentChoiceId: -1});
    var i = this.state.questionIndex;

    if(i < this.state.questions.length-1){
      i += 1;
      this.setState({questionIndex: i});
      this.setState({currentQuestion: this.state.questions[this.state.questionIndex].question});
      this.setState({currentChoiceA: this.state.questions[this.state.questionIndex].choices[0].choice});
      this.setState({currentChoiceB: this.state.questions[this.state.questionIndex].choices[1].choice});
      this.setState({currentChoiceC: this.state.questions[this.state.questionIndex].choices[2].choice});
      this.setState({currentChoiceD: this.state.questions[this.state.questionIndex].choices[3].choice});
      this.setState({currentChoiceAId: this.state.questions[this.state.questionIndex].choices[0].id});
      this.setState({currentChoiceBId: this.state.questions[this.state.questionIndex].choices[1].id});
      this.setState({currentChoiceCId: this.state.questions[this.state.questionIndex].choices[2].id});
      this.setState({currentChoiceDId: this.state.questions[this.state.questionIndex].choices[3].id});

      for(var j in this.state.questions[this.state.questionIndex].choices){
        if(this.state.questions[this.state.questionIndex].choices[j].correct === true){
          this.setState({correctChoiceId: this.state.questions[this.state.questionIndex].choices[j].id});
        }
      }
    }

  }

  doneFetchingQuestions = (data) => {
    this.setState({quizName: data.quiz});
    this.setState({timer: data.time_limit});
    this.setState({questions: data.questions});
    this.loadNextQuestion();
  }

  handleChoiceChange = (choiceID) => {
    this.setState({currentChoiceId: choiceID});
  }

  handleEval = () => {
    if(this.state.currentChoiceId === this.state.correctChoiceId){
      this.setState({alertType: "success"});
      this.setState({alertCaption: "Correct: You've got it!"});
    }else{
      this.setState({alertType: "danger"});
      this.setState({alertCaption: "Wrong: Try Again!"});
    }
    this.setState({showAlert: true});

    setTimeout(function(){
      this.loadNextQuestion();
    }.bind(this), 2000);
  }
  fetchQuestions = () => {
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
                </Collapse>
          </Navbar>
    <Alert color={this.state.alertType} isOpen={this.state.showAlert}>{this.state.alertCaption}</Alert>
          <Container>
            <Row>
              <Markdown source={`## ${this.state.currentQuestion}`} /><br/><br/><br/>
            </Row>
            <Row>
              <Col xs="6">
                <Label check>
                  <Input type="radio" name="radio1" onClick={(event) => this.handleChoiceChange(this.state.currentChoiceAId)} checked={this.state.currentChoiceAId === this.state.currentChoiceId}/>
                    {' '}
                    <Markdown source={this.state.currentChoiceA} />
                </Label>
              </Col>
              <Col xs="6">
                <Label check>
                  <Input type="radio" name="radio1" onClick={(event) => this.handleChoiceChange(this.state.currentChoiceBId)} checked={this.state.currentChoiceBId === this.state.currentChoiceId}/>
                    {' '}
                    <Markdown source={this.state.currentChoiceB} />
                </Label>
              </Col>
            </Row>
            <Row>
              <Col xs="6">
                <Label check>
                  <Input type="radio" name="radio1" onClick={(event) => this.handleChoiceChange(this.state.currentChoiceCId)} checked={this.state.currentChoiceCId === this.state.currentChoiceId}/>
                    {' '}
                    <Markdown source={this.state.currentChoiceC} />
                </Label>
              </Col>
              <Col xs="6">
                <Label check>
                  <Input type="radio" name="radio1" onClick={(event) => this.handleChoiceChange(this.state.currentChoiceDId)} checked={this.state.currentChoiceDId === this.state.currentChoiceId}/>
                    {' '}
                    <Markdown source={this.state.currentChoiceD} />
                </Label>
              </Col>
            </Row>
            <Row>
              <Col sm="12" md={{ size: 6, offset: 3 }}>
                <Button color="primary" size="lg" disabled={this.state.currentChoiceId === -1} onClick={this.handleEval}>Confirm</Button>{' '}
              </Col>
            </Row>
          </Container>
      </div>
    );
  }
}

export default App;
