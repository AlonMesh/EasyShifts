// components/Login.js
import React from 'react';

const Login = () => {
  return (
    <div>
      <h1>Employee Log In</h1>
      <label htmlFor="username">Username:</label>
      <input type="text" id="username" name="username" required />
      <br />
      <label htmlFor="password">Password:</label>
      <input type="password" id="password" name="password" required />
      <button type="submit">Log In</button>
    </div>
  );
}

export default Login;
