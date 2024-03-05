// components/Home.js
import React from 'react';
import { Link } from 'react-router-dom';
import './../css/Home.css';

const Home = () => {
  return (
    <div className="home-container">
      <h1>Welcome to Easy Shifts!</h1>
      {/*
      <p> Welcome to Easy Shifts, your ultimate solution for streamlined shift management!
         Our innovative app empowers both managers and employees by simplifying the shift
          scheduling process. Say goodbye to tedious communication and manual coordination. 
          With Easy Shifts, employees can effortlessly send their shift requests directly to managers, 
          and managers can efficiently respond, making the entire process seamless. 
          Enjoy the convenience of requesting, managing, and receiving shift updates all in one place. 
          Revolutionize the way you handle scheduling and ensure a hassle-free experience for both 
          managers and employees. Easy Shifts is here to make work scheduling efficient, effective, 
          and, most importantly, easy for everyone involved. 
        </p>
        <img src="/path/to/easy_shifts_image.jpg" alt="Easy Shifts" className="easy-shifts-image" />
        */}
      
      <div className="button-container">
        <button className="login-button"><Link to="/login">Login</Link></button>
        <button className="signup-button"><Link to="/signup">Sign Up</Link></button>
      </div>
    </div>
  );
}

export default Home;
