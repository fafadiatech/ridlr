import React from 'react';
import {Input, Container, Row, Col, Button} from 'reactstrap';

class Home extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      invitationCode: "",
      canRedirect: false,
    };
  }

  handleInvitationCode = (e) => {
    this.setState({invitationCode: e.target.value});
  }

  handleConfirmClick = () => {
    this.setState({canRedirect: true});
  }

  render() {
    // Check if we need to redirect?
    if(this.state.canRedirect){
      this.props.history.push(`/quiz/${this.state.invitationCode}`);
    }

    // Render current view
    return (
      <div className="Home">
        <Container>
          <Row>
            <Col sm="12" md={{ size: 6, offset: 3 }}>
              <h2>Welcome!</h2>
              <h3>Please enter invitation code to proceed</h3>
              <Input type="text" name="invitation-code" id="invitation-code" placeholder="Invitation Code" onChange={(e) => {this.handleInvitationCode(e)}}/><br/>
            </Col>
            <Col sm="12" md={{ size: 6, offset: 3 }}>
              <Button color="primary" size="lg" disabled={this.state.invitationCode === ""} onClick={this.handleConfirmClick}>Confirm</Button>{' '}
            </Col>
          </Row>
        </Container>
      </div>
    );
  }
}

export default Home;
