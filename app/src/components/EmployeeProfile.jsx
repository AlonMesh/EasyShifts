// EmployeeProfile.js

import React, { useState, useEffect } from 'react';
import * as socket_object from '../utils';
import { useSocket } from '../utils';
import { Link } from 'react-router-dom';
import '../css/EmployeeProfile.css'; // Import the CSS file

function EmployeeProfile() {
  const socket = socket_object.useSocket();
  const [profileData, setProfileData] = useState(null);

  useEffect(() => {
    if (socket && socket.readyState === WebSocket.OPEN) {
      const getProfileRequest = {
        request_id: 70,
      };

      socket.send(JSON.stringify(getProfileRequest));

      const handleSocketMessage = (event) => {
        const response = JSON.parse(event.data);
        if (response && response.request_id === 70) {
          handleProfileResponse(response);
        }
      };

      socket.addEventListener('message', handleSocketMessage);

      return () => {
        socket.removeEventListener('message', handleSocketMessage);
      };
    }
  }, [socket]);

  const handleProfileResponse = (response) => {
    if (response.success) {
      setProfileData(response.data);
    } else {
      console.error('Failed to retrieve profile data');
    }
  };

  return (
    <div className="EmployeeProfileContainer">
      <div className="ProfileHeader">
        <h2>Employee Profile</h2>
      </div>
      {profileData ? (
        <div>
          <p className="ProfileInfo">Username: {profileData.username}</p>

          <div className="ButtonContainer">
            <button className="SignInShiftsButton">
              <Link to="/SignInShifts" aria-label="Sign In Shifts">
                <span className="ButtonIcon" role="img" aria-label="Note Icon"></span>
                <span className="ButtonText">Sign in shifts</span>
              </Link>
            </button>
            <button className="ViewShiftsButton">
              <Link to="/ShiftsPage" aria-label="View My Shifts">
                <span className="ButtonIcon" role="img" aria-label="Calendar Icon"></span>
                <span className="ButtonText">View my shifts</span>
              </Link>
            </button>
          </div>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}

export default EmployeeProfile;
