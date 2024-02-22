import React from 'react';
import { Link } from 'react-router-dom';

const EmployeePage = () => {
  // This component represents the employee page
  return (
    <div>
      <h1>Welcome to the Employee Page!</h1>
      <p>This is the page where employees can perform various tasks.</p>
      <Link to="/manager">Go to Manager Page</Link>
    </div>
  );
};

export default EmployeePage;
