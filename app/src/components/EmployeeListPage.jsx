import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

const EmployeeListPage = ({ socket }) => {
  const [employeesList, setEmployeesList] = useState('');

  useEffect(() => {
    const getEmployeesList = () => {
      if (socket && socket.readyState === WebSocket.OPEN) {
        const request = {
          request_id: 60,
        };
        socket.send(JSON.stringify(request));
      } else {
        console.log('Socket not available or not open');
      }
    };

    // Define a function to handle messages from the server
    const handleMessage = (event) => {
      const response = JSON.parse(event.data);
      if (response.success) {
        setEmployeesList(response.data);
      } else {
        console.log('Error retrieving employee list');
      }
    };

    // Add event listener for incoming messages
    socket.addEventListener('message', handleMessage);

    // Clean up function to remove event listener when component unmounts
    return () => {
      socket.removeEventListener('message', handleMessage);
    };
  }, [socket]);

  return (
    <div>
      <h1>Manager Workers List</h1>
      <div id="employeesListContainer">
        <p>{employeesList}</p>
      </div>
      {/* Link back to home page */}
      <Link to="/">Go back to home page</Link>
    </div>
  );
};

export default EmployeeListPage;
