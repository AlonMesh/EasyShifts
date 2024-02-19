
function EmployeeLogin() {
  const sendLoginRequest = () => {
    // Implement your login logic here
  };

  return (
    <div>
      <h1>Employee Log In</h1>

      <label htmlFor="username">Username:</label>
      <input type="text" id="username" name="username" required />

      <br />

      <label htmlFor="password">Password:</label>
      <input type="password" id="password" name="password" required />

      <button type="submit" onClick={sendLoginRequest}>
        Log In
      </button>
      <div id="log"></div>
    </div>
  );
}

export default EmployeeLogin;