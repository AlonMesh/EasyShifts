import React, {useState} from 'react';
import {Link} from 'react-router-dom';
import './../css/SignUp.css';

const SignUp = () => {
    const [role, setRole] = useState('');

    const handleRoleChange = (event) => {
        setRole(event.target.value);
    };

    return (
        <div className="signup-container">
            <div className="signup-form">
                <h1>Pick your role</h1>
                <form>
                    <div>
                        <div className="icons-container">
                            <img src="/businessman.png" alt="Manager Icon" className="icon"/>
                        </div>
                        <label>
                            <input
                                type="radio"
                                value="manager"
                                checked={role === 'manager'}
                                onChange={handleRoleChange}
                            />
                            Manager
                        </label>
                    </div>
                    <div>
                        <div className="icons-container">
                            <img src="/worker.png" alt="Employee Icon" className="icon"/>
                        </div>
                        <label>
                            <input
                                type="radio"
                                value="employee"
                                checked={role === 'employee'}
                                onChange={handleRoleChange}
                            />
                            Employee
                        </label>
                    </div>
                    <Link
                        to={role === 'manager' ? '/SignUpManager' : (role === 'employee' ? '/SignUpEmployee' : '/signup')}>
                        <button disabled={!role}>Continue</button>
                    </Link>
                </form>
            </div>
        </div>
    );
}

export default SignUp;
