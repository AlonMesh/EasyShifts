// App.jsx
import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Login from '../components/Login';
import SignUp from '../components/SignUp';
import Home from '../components/Home';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <h1>Welcome to Easy Shifts!</h1>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;


