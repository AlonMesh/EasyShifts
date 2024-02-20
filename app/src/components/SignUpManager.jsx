import React from 'react';

const ManagerSignUp = () => {
  const sendManagerSignUpRequest = () => {
    // Implement the function to send sign-up request
    // This function will be handled differently in React
  };

  return (
    <div>
      <h1>Manager Sign Up</h1>

      <label htmlFor="managerUsername">Username:</label>
      <input type="text" id="managerUsername" name="managerUsername" required />

      <br />

      <label htmlFor="managerPassword">Password:</label>
      <input type="password" id="managerPassword" name="managerPassword" required />

      <br />

      <label htmlFor="name">Business Name:</label>
      <input type="text" id="name" name="name" required />

      <br />

      <button type="submit" onClick={sendManagerSignUpRequest}>Sign Up</button>
      <div id="log"></div>
    </div>
  );
};

export default ManagerSignUp;
