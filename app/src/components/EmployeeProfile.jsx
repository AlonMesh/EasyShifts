import React, { useState, useEffect } from 'react';
import * as socket_object from '../utils';
import { useSocket } from '../utils';

function EmployeeProfile() {
  const socket = socket_object.useSocket(); // Call useSocket hook directly

  const [profileData, setProfileData] = useState(null);

  useEffect(() => {
    if (socket && socket.readyState === WebSocket.OPEN) {
      // Fetch employee profile data when the component mounts
      const getProfileRequest = {
        request_id: 70
      };

      socket.send(JSON.stringify(getProfileRequest));

      // Event listener for messages received on the WebSocket
      const handleSocketMessage = (event) => {
        const response = JSON.parse(event.data);
        if (response && response.request_id === 70) { // Check if response is not null
          handleProfileResponse(response);
        }
      };

      // Attach event listener for WebSocket messages
      socket.addEventListener('message', handleSocketMessage);

      // Cleanup function
      return () => {
        socket.removeEventListener('message', handleSocketMessage);
      };
    }
  }, [socket]);

  // Function to handle profile response
  const handleProfileResponse = (response) => {
    if (response.success) {
      setProfileData(response.data);
    } else {
      console.error('Failed to retrieve profile data');
    }
  };

  return (
    <div>
      <h2>Employee Profile</h2>
      {profileData ? (
        <div>
          <p>Username: {profileData.username}</p>
          {/* Display other profile data here */}
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}

export default EmployeeProfile;
