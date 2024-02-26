import React, { useState } from 'react';
import { Link } from 'react-router-dom';

function SignUpManager() {
    const [formData, setFormData] = useState({
        username: '',
        password: '',
        name: ''
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prevState => ({
            ...prevState,
            [name]: value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('/api/signup/manager', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });
            const data = await response.json();
            if (data.success) {
                alert('Manager sign-up successful');
                // Optionally, you can redirect to ManagerProfile or any other page here
            } else {
                alert('Error during manager sign-up: ' + data.message);
            }
        } catch (error) {
            console.error('Error during sign-up:', error);
            alert('Error during sign-up. Please try again later.');
        }
    };

    return (
        <div>
            <h2>Manager Sign Up</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Username:</label>
                    <input type="text" name="username" value={formData.username} onChange={handleChange} required />
                </div>
                <div>
                    <label>Password:</label>
                    <input type="password" name="password" value={formData.password} onChange={handleChange} required />
                </div>
                <div>
                    <label>Name:</label>
                    <input type="text" name="name" value={formData.name} onChange={handleChange} required />
                </div>
                <button type="submit">Sign Up</button>
            </form>
            <p>Already have an account? <Link to="/sign-in">Sign In</Link></p>
        </div>
    );
}

export default SignUpManager;
