import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import * as socket_object from '../utils'

const EmployeeListPage = () => {
  const [employeesList, setEmployeesList] = useState('');

  useEffect(() => {
    const getEmployeesList = () => {
      if (socket_object.useSocket() && socket_object.useSocket().readyState === WebSocket.OPEN) {
        const request = {
          request_id: 60,
        };
        socket_object.useSocket().send(JSON.stringify(request));
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
    socket_object.useSocket().addEventListener('message', handleMessage);

    // Clean up function to remove event listener when component unmounts
    return () => {
      socket_object.useSocket().removeEventListener('message', handleMessage);
    };
  }, [socket_object.useSocket()]);

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
