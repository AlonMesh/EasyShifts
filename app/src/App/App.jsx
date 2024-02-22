import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Login from '../components/Login';
import SignUp from '../components/SignUp';
import Home from '../components/Home';
import SignUpManager from '../components/SignUpManager';
import SignUpEmployee from '../components/SignUpEmployee';
import managerProfile from '../components/managerProfile';
import employeeProfile from '../components/employeeProfile';
import './App.css';

function App() {
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    // Establish WebSocket connection when the component mounts
    const newSocket = new WebSocket('ws://localhost:8080');

    // Event listener for WebSocket errors
    newSocket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    // Update the socket state
    setSocket(newSocket);

    // Cleanup function
    return () => {
      newSocket.close();
    };
  }, []);

  return (
    <Router>
      <div className="App">
        <h1>Welcome to Easy Shifts!</h1>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login socket={socket} />} />
          <Route path="/signup" element={<SignUp socket={socket} />} />
          <Route path="/signupManager" element={<SignUpManager socket={socket} />} />
          <Route path="/signupEmployee" element={<SignUpEmployee socket={socket} />} />
          <Route path="/managerProfile" element={<managerProfile socket={socket} />} />
          <Route path="/employeeProfile" element={<employeeProfile socket={socket} />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
