import React, { useState } from 'react';

const SignUpManager = ({ socket }) => {
  const [managerUsername, setManagerUsername] = useState('');
  const [managerPassword, setManagerPassword] = useState('');
  const [businessName, setBusinessName] = useState('');
  const [log, setLog] = useState('');

  const sendManagerSignUpRequest = () => {
    if (!socket) {
      console.error("Socket connection is not available.");
      return;
    }

    const requestData = {
      request_id: 30, // This should match the request ID expected by your server
      data: {
        username: managerUsername,
        password: managerPassword,
        name: businessName
      }
    };

    // Send sign-up request to the server using WebSocket
    socket.send(JSON.stringify(requestData));

    // Handle response from the server
    socket.onmessage = (event) => {
      const response = JSON.parse(event.data);
      if (response.success) {
        // Sign-up successful
        setLog(response.message);
        // Redirect or perform any other necessary action
        setTimeout(() => {
          window.location.replace("../pages/manager_page.html");
        }, 2000); // Redirect after 2 seconds (adjust as needed)
      } else {
        // Sign-up failed
        setLog(response.message);
      }
    };
  };

  return (
    <div>
      <h1>Manager Sign Up</h1>
      <label htmlFor="managerUsername">Username:</label>
      <input
        type="text"
        id="managerUsername"
        name="managerUsername"
        value={managerUsername}
        onChange={(e) => setManagerUsername(e.target.value)}
        required
      />
      <br />
      <label htmlFor="managerPassword">Password:</label>
      <input
        type="password"
        id="managerPassword"
        name="managerPassword"
        value={managerPassword}
        onChange={(e) => setManagerPassword(e.target.value)}
        required
      />
      <br />
      <label htmlFor="name">Business Name:</label>
      <input
        type="text"
        id="name"
        name="name"
        value={businessName}
        onChange={(e) => setBusinessName(e.target.value)}
        required
      />
      <br />
      <button type="button" onClick={sendManagerSignUpRequest}>Sign Up</button>
      <div id="log">{log}</div>
    </div>
  );
};

export default SignUpManager;
