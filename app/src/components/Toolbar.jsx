import React from 'react';
import './../css/Toolbar.css';
import { Link } from 'react-router-dom';

const Toolbar = () => {
  return (
    <div className="toolbar">
      <h3>EasyShifts</h3>
      <button><Link to="/home">Home</Link></button>
    </div>
  );
};

export default Toolbar;
