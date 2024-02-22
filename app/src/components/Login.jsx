import React, { useState } from 'react';
import ManagerProfile from './managerProfile.jsx';
import EmployeeProfile from './employeeProfile.jsx';

const Login = ({ socket }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [log, setLog] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false); // New state variable
  const [isManager, setIsManager] = useState(false); // New state variable for user role

  const sendLoginRequest = () => {
    if (!socket) {
      console.error("Socket connection is not available.");
      return;
    }

    const requestData = {
      request_id: 10,
      data: {
        username: username,
        password: password
      }
    };

    // Send login request to the server using WebSocket
    socket.send(JSON.stringify(requestData));

    // Handle response from the server
    socket.onmessage = (event) => {
      const response = JSON.parse(event.data);
      if (response.userExists === 'f') {
        setLog('Invalid Username or Password');
      } else {
        setIsLoggedIn(true); // Set isLoggedIn to true upon successful login
        setIsManager(response.isManager === 't'); // Set isManager based on user role
        setLog(response.isManager === 't' ? 'Redirecting to manager profile...' : 'Redirecting to employee profile...');
      }
    };
  };

  return (
    <div>
      <h1>Employee Log In</h1>
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
      <div id="log">{log}</div>

      {/* Conditionally render the profile component only if user is logged in */}
      {isLoggedIn && (isManager ? <ManagerProfile /> : <EmployeeProfile />)}
    </div>
  );
};

export default Login;
