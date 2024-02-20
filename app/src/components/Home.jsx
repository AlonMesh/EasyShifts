// components/Home.js
import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div>
      <h2>Welcome to Easy Shifts!</h2>
      <button><Link to="/login">Login</Link></button>
      <button><Link to="/signup">Sign Up</Link></button>
    </div>
  );
}

export default Home;
