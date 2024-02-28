// App.jsx
import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Home from '../components/Home';
import Login from '../components/Login';
import SignUp from '../components/SignUp';
import ManagerSchedule from '../components/ManagerSchedule/ManagerSchedule';
import ManagerProfile from '../components/ManagerProfile';
import ManagerSettings from '../components/ManagerSettings';
import SignUpManager from '../components/SignUpManager';
import SignUpEmployee from '../components/SignUpEmployee';
import EmployeeProfile from '../components/EmployeeProfile';
import SignInShifts from '../components/SignInShifts';
import ManagerViewShiftsRequests from '../components/ManagerViewShiftsRequests';
import ManagerWorkersList from '../components/ManagerWorkersList';
import ShiftsPage from '../components/ShiftsPage';
import EmployeeListPage from '../components/EmployeeListPage';
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

    // Event listener for WebSocket open
    newSocket.onopen = () => {
      console.log('WebSocket connection established successfully.');
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
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path={"/manager-schedule"} element={<ManagerSchedule />} />
          <Route path={"/manager-profile"} element={<ManagerProfile />} />
          <Route path={"/manager-settings"} element={<ManagerSettings />} />
          <Route path="/signupManager" element={<SignUpManager socket={socket} />} />
          <Route path="/signupEmployee" element={<SignUpEmployee socket={socket} />} />
          <Route path="/managerProfile" element={<ManagerProfile socket={socket} />} />
          <Route path="/employeeProfile" element={<EmployeeProfile socket={socket} />} />
          <Route path="/signInShifts" element={<SignInShifts socket={socket} />} />
          <Route path="/managerViewShiftsRequests" element={<ManagerViewShiftsRequests socket={socket} />} />
          <Route path="/managerWorkersList" element={<ManagerWorkersList socket={socket} />} />
          <Route path="/shiftsPage" element={<ShiftsPage socket={socket} />} />
          <Route path="/employeeListPage" element={<EmployeeListPage socket={socket} />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
