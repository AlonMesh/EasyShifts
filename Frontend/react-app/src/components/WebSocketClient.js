// WebSocketClient.js

import React from 'react';
import './WebSocketClient.css'; // Import your CSS file if you have one

class WebSocketClient extends React.Component {
  redirectToLogin = () => {
    // login component
  };

  redirectToSignUp = () => {
    // sign up component
  };

  render() {
    return (
      <div>
        <h1>Welcome to Easy Shifts!</h1>
        <button onClick={this.redirectToLogin}>Login</button>
        <button onClick={this.redirectToSignUp}>Sign Up</button>
        <div id="log"></div>
      </div>
    );
  }
}

export default WebSocketClient;
