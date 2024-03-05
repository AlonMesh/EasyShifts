import React, { useState, useEffect } from 'react';
import { useSocket } from '../utils';

const EmployeeListPage = () => {
  const [employees, setEmployees] = useState([]);
  const socket = useSocket();

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

const handleApprove = (userName) => {
  if (socket.readyState === WebSocket.OPEN) {
    const request = {
      request_id: 62,
      data: { userName },
    };
    socket.send(JSON.stringify(request));
    fetchEmployees(); // Fetch updated employee list after approval
  } else {
    console.error('WebSocket connection not open.');
  }
};

const handleReject = (userName) => {
  if (socket.readyState === WebSocket.OPEN) {
    const request = {
      request_id: 64,
      data: { userName },
    };
    socket.send(JSON.stringify(request));
    fetchEmployees(); // Fetch updated employee list after rejection
  } else {
    console.error('WebSocket connection not open.');
  }
};


  useEffect(() => {
    fetchEmployees();

    const handleMessage = (event) => {
      const data = JSON.parse(event.data);
      if (Array.isArray(data)) { // Check if data is an array (list of employees)
        setEmployees(data); // Update state with the list of employees
      } else {
        console.error('Error fetching employees:', data.error);
      }
    };

    if (socket) {
      socket.addEventListener('message', handleMessage);
    }

    return () => {
      if (socket) {
        socket.removeEventListener('message', handleMessage);
      }
    };
  }, [socket]);

  return (
    <div>
      <h1>Employee List</h1>
      <ul>
        {employees.map(employee => (
          <li key={employee.userName}>
            {employee.name}
            {!employee.approved && (
              <>
                <button onClick={() => handleApprove(employee.userName)}>Approve</button>
                <button onClick={() => handleReject(employee.userName)}>Reject</button>
              </>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default EmployeeListPage;
