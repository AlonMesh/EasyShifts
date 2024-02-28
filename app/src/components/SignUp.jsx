import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const SignUp = () => {
  const [role, setRole] = useState('');

  const handleRoleChange = (event) => {
    setRole(event.target.value);
  };

  return (
    <div>
      <h1>Sign Up</h1>
      <form>
        <div>
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
        <Link to={role === 'manager' ? '/SignUpManager' : (role === 'employee' ? '/SignUpEmployee' : '/signup' )}>
          <button disabled={!role}>Continue</button>
        </Link>
      </form>
    </div>
  );
}

export default SignUp;
