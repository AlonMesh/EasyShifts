import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import webSocket from 'ws'; // Import WebSocket library
import axios from 'axios'; // Make sure to install axios using npm or yarn
import { useSocket } from '../utils';

const EmployListPage = () => {
  const [employees, setEmployees] = useState([]);
  const [approvedEmployees, setApprovedEmployees] = useState([]);
  const [unapprovedEmployees, setUnapprovedEmployees] = useState([]);
  const socket = useSocket();

  useEffect(() => {
    if (socket) {
      fetchEmployees();
    }
  }, [socket]);

  const fetchEmployees = () => {
    if (socket.readyState === WebSocket.OPEN) {
      const request = {
        request_id: 60,
      };
      socket.send(JSON.stringify(request));
    } else {
      console.error('WebSocket connection not open.');
    }
  };

  const handleApprove = (employeeId) => {
    if (socket.readyState === WebSocket.OPEN) {
      const request = {
        request_id: 72,
        data: { employeeId },
      };
      socket.send(JSON.stringify(request));
    } else {
      console.error('WebSocket connection not open.');
    }
  };

 const handleReject = (employeeId) => {
  if (socket.readyState === WebSocket.OPEN) {
    const request = {
      request_id: 74, // Assuming 100 is the request ID for employee rejection
      data: { employeeId },
    };
    socket.send(JSON.stringify(request));
  } else {
    console.error('WebSocket connection not open.');
  }
};


  useEffect(() => {
    // Add event listener to handle messages from the server
    const handleMessage = (event) => {
      const data = JSON.parse(event.data);
      const { success, employees } = data;

      if (success) {
        setEmployees(employees);
        const approved = employees.filter(employee => employee.approved);
        const unapproved = employees.filter(employee => !employee.approved);
        setApprovedEmployees(approved);
        setUnapprovedEmployees(unapproved);
      } else {
        console.error('Error fetching employees:', data.error);
      }
    };

    if (socket) {
      socket.addEventListener('message', handleMessage);
    }

    // Cleanup function
    return () => {
      if (socket) {
        socket.removeEventListener('message', handleMessage);
      }
    };
  }, [socket]);

  return (
    <div>
      <h1>Employee List</h1>
      <h2>Approved Employees</h2>
      <ul>
        {approvedEmployees.map(employee => (
          <li key={employee.id}>
            {employee.name}
          </li>
        ))}
      </ul>
      <h2>Unapproved Employees</h2>
      <ul>
        {unapprovedEmployees.map(employee => (
          <li key={employee.id}>
            {employee.name} -
            <button onClick={() => handleApprove(employee.id)}>Approve</button>
            <button onClick={() => handleReject(employee.id)}>Reject</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default EmployListPage;