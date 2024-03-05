// components/Home.js
import React from 'react';
import {Link} from 'react-router-dom';
import './../css/Home.css';

const Home = () => {
    return (
        <div className="home-container">
            <img src="/easyshifts-logo.png" alt="Easy Shifts" className="easy-shifts-image"/>

            <div className="text-container">
                <div className="bullets">
                    <div className="bullet-item">Say goodbye to tedious communication and manual coordination</div>
                    <div className="bullet-item">Effortlessly send shift requests directly to managers with
                        EasyShifts
                    </div>
                    <div className="bullet-item">Revolutionize work scheduling for an efficient and hassle-free
                        experience
                    </div>
                </div>
            </div>

            <div className="button-container">
                <Link to="/login" className="login-button">Login</Link>
                <Link to="/signup" className="signup-button">Sign Up</Link>
            </div>
        </div>
    );
}

export default Home;
