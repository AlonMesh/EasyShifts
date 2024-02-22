import React, { useState } from 'react';

const SignUpEmployee = ({ socket }) => {
  const [employeeUsername, setEmployeeUsername] = useState('');
  const [employeePassword, setEmployeePassword] = useState('');
  const [businessNumber, setBusinessNumber] = useState('');
  const [employeeName, setEmployeeName] = useState('');
  const [log, setLog] = useState('');

  const sendEmployeeSignUpRequest = () => {
    if (!socket) {
      console.error("Socket connection is not available.");
      return;
    }

    const requestData = {
      request_id: 20,
      data: {
        username: employeeUsername,
        password: employeePassword,
        businessNumber: businessNumber,
        employeeName: employeeName
      }
    };

    // Send sign-up request to the server using WebSocket
    socket.send(JSON.stringify(requestData));

    // Handle response from the server
    socket.onmessage = (event) => {
      const response = JSON.parse(event.data);
      const { success, message } = response.data;
      if (success) {
        setLog(message);
        setTimeout(() => {
          window.location.replace("../pages/employee_page.html");
        }, 2000); // Redirect after 2 seconds (adjust as needed)
      } else {
        setLog('Sign up failed. Please try again.');
      }
    };
  };

  return (
    <div>
      <h1>Employee Sign Up</h1>
      <label htmlFor="employeeUsername">Username:</label>
      <input
        type="text"
        id="employeeUsername"
        name="employeeUsername"
        value={employeeUsername}
        onChange={(e) => setEmployeeUsername(e.target.value)}
        required
      />
      <br />
      <label htmlFor="employeePassword">Password:</label>
      <input
        type="password"
        id="employeePassword"
        name="employeePassword"
        value={employeePassword}
        onChange={(e) => setEmployeePassword(e.target.value)}
        required
      />
      <br />
      <label htmlFor="businessNumber">Business Number:</label>
      <input
        type="text"
        id="businessNumber"
        name="businessNumber"
        value={businessNumber}
        onChange={(e) => setBusinessNumber(e.target.value)}
        required
      />
      <br />
      <label htmlFor="employeeName">Name :</label>
      <input
        type="text"
        id="employeeName"
        name="employeeName"
        value={employeeName}
        onChange={(e) => setEmployeeName(e.target.value)}
        required
      />
      <br />
      <button type="button" onClick={sendEmployeeSignUpRequest}>Sign Up</button>
      <div id="log">{log}</div>
    </div>
  );
};

export default SignUpEmployee;
