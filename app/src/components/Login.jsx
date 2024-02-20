import React, { useState } from 'react';

const Login = ({ socket }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const sendLoginRequest = () => {
    // Check if username and password are not empty
    if (username.trim() === '' || password.trim() === '') {
      setErrorMessage('Username and password are required');
      return;
    }

    // Assuming `socket` is defined and passed from the App component
    if (socket && socket.readyState === WebSocket.OPEN) {
      const request = {
        request_id: 10,
        data: { username, password },
      };

      socket.send(JSON.stringify(request));
    } else {
      setErrorMessage('Not connected to the server');
    }
  };

  // Event listener for receiving messages
  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.success) {
      const isManager = data.isManager;
      if (isManager) {
        // Navigate to the manager page
        window.location.replace("/manager");
      } else {
        // Navigate to the employee page
        window.location.replace("/employee");
      }
    } else {
      setErrorMessage('Invalid Username or Password');
    }
  };

  return (
    <div>
      <h1>Log In</h1>
      <label htmlFor="username">Username:</label>
      <input
        type="text"
        id="username"
        name="username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        required
      />
      <br />
      <label htmlFor="password">Password:</label>
      <input
        type="password"
        id="password"
        name="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />
      <button type="button" onClick={sendLoginRequest}>Log In</button>
      {errorMessage && <p>{errorMessage}</p>}
    </div>
  );
};

export default Login;
