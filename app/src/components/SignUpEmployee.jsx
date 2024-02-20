import React from 'react';

const EmployeeSignUp = () => {
  const sendEmployeeSignUpRequest = () => {
    // Implement the function to send sign-up request
    // This function will be handled differently in React
  };

  return (
    <div>
      <h1>Employee Sign Up</h1>

      <label htmlFor="employeeUsername">Username:</label>
      <input type="text" id="employeeUsername" name="employeeUsername" required />

      <br />

      <label htmlFor="employeePassword">Password:</label>
      <input type="password" id="employeePassword" name="employeePassword" required />

      <br />

      <label htmlFor="businessNumber">Business Number:</label>
      <input type="text" id="businessNumber" name="businessNumber" required />

      <br />

      <label htmlFor="employeeName">Name :</label>
      <input type="text" id="employeeName" name="employeeName" required />

      <br />

      <button type="submit" onClick={sendEmployeeSignUpRequest}>Sign Up</button>
      <div id="log"></div>
    </div>
  );
};

export default EmployeeSignUp;
