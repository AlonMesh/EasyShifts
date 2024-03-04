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
    fetchEmployees();
  }, []);

  const fetchEmployees = async () => {
    try {
      const response = await axios.get('http://localhost:8080', {
        params: {
          request_id: 60
        }
      });
      setEmployees(response.data);
      const approved = response.data.filter(employee => employee.approved);
      const unapproved = response.data.filter(employee => !employee.approved);
      setApprovedEmployees(approved);
      setUnapprovedEmployees(unapproved);
    } catch (error) {
      console.error('Error fetching employees:', error);
    }
  };

  const handleApprove = async (employeeId) => {
    try {
      // Send request to approve employee
      await axios.post('http://localhost:8080/approve-employee', { employeeId });
      // Fetch updated list of employees
      fetchEmployees();
    } catch (error) {
      console.error('Error approving employee:', error);
    }
  };

  const handleReject = async (employeeId) => {
    try {
      // Send request to delete employee
      await axios.delete(`http://localhost:8080/delete-employee/${employeeId}`);
      // Fetch updated list of employees
      fetchEmployees();
    } catch (error) {
      console.error('Error rejecting employee:', error);
    }
  };

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
