import React, { useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Login from '../components/Login';
import SignUp from '../components/SignUp';
import Home from '../components/Home';
import SignUpManager from '../components/SignUpManager';
import SignUpEmployee from '../components/SignUpEmployee';
import './App.css';

function App() {
  useEffect(() => {
    // Establish WebSocket connection when the component mounts
    const socket = new WebSocket('ws://localhost:8080');

    // Event listener for WebSocket errors
    socket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    // Cleanup function
    return () => {
      socket.close();
    };
  }, []);

  return (
    <Router>
      <div className="App">
        <h1>Welcome to Easy Shifts!</h1>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path="/signupManager" element={<SignUpManager />} />
          <Route path="/signupEmployee" element={<SignUpEmployee />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
