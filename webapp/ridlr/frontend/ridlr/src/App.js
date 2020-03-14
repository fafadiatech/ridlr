import React from 'react';
import {BrowserRouter, Route, Switch} from 'react-router-dom';

// Import all components that needs to be rendered
import Home from './Home';
import Summary from './Summary';
import Quiz from './Quiz';
import Error from './Error';

class App extends React.Component {
  render() {
    return (
      <BrowserRouter>
        <Switch>
          <Route path="/" component={Home} exact/>
          <Route path="/quiz" component={Quiz}/>
          <Route path="/summary" component={Summary}/>
          <Route component={Error}/>
        </Switch>
      </BrowserRouter>
    );
  }
}

export default App;
