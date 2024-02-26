import React, { useEffect } from 'react';

const EmployeeProfile = ({ socket }) => {
  useEffect(() => {
    // Establish WebSocket connection when the component mounts
    if (socket && socket.readyState === WebSocket.OPEN) {
      console.log('WebSocket connection is already open.');
    } else {
      console.log('Establishing WebSocket connection...');
      const newSocket = new WebSocket('ws://localhost:8080');

      // Event listener for WebSocket errors
      newSocket.onerror = (error) => {
        console.error('WebSocket error:', error);
      };

      // Event listener for WebSocket open
      newSocket.onopen = () => {
        console.log('WebSocket connection established successfully.');
      };

      // Cleanup function
      return () => {
        newSocket.close();
      };
    }
  }, [socket]); // Dependencies array to ensure this effect runs only once

  const getEmployeesShiftsRequest = () => {
    // Implement logic to send request for employee shifts using the existing socket
    if (socket && socket.readyState === WebSocket.OPEN) {
      // Example request
      const request = {
        request_id: 50,
      };
      socket.send(JSON.stringify(request));
    } else {
      console.error('Socket connection is not available.');
    }
  };

  const createNewShifts = () => {
    // Implement logic to create new week shifts using the existing socket
    if (socket && socket.readyState === WebSocket.OPEN) {
      // Example request
      const request = {
        request_id: 80,
      };
      socket.send(JSON.stringify(request));
    } else {
      console.error('Socket connection is not available.');
    }
  };

  const getProfileRequest = () => {
    // Implement logic to send request to view employee profile using the existing socket
    if (socket && socket.readyState === WebSocket.OPEN) {
      // Example request
      const request = {
        request_id: 70,
      };
      socket.send(JSON.stringify(request));
    } else {
      console.error('Socket connection is not available.');
    }
  };

  const getEmployeesList = () => {
    // Implement logic to get list of employees using the existing socket
    if (socket && socket.readyState === WebSocket.OPEN) {
      // Example request
      const request = {
        request_id: 60,
      };
      socket.send(JSON.stringify(request));
    } else {
      console.error('Socket connection is not available.');
    }
  };

  return (
    <div>
      <h1>Welcome!</h1>
      <h2>What would you like to do?</h2>
      <button onClick={getEmployeesShiftsRequest}>Schedule shifts</button>
      <button onClick={createNewShifts}>Create new week shifts</button>
      <button onClick={getProfileRequest}>View my profile</button>
      <button onClick={getEmployeesList}>View my employees</button>
      <div id="log"></div>
      {/* Example HTML structure with a container for displaying profile information */}
      <div id="profileContainer"></div>
    </div>
  );
};

export default EmployeeProfile;
