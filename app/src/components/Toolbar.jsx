import React from 'react';
import './../css/Toolbar.css';
import {Link} from 'react-router-dom';

const Toolbar = () => {
    return (
        <div className="toolbar">
            <h3>EasyShifts</h3>
            <Link to="/home" className="but">Home</Link>
        </div>
    );
};

export default Toolbar;
