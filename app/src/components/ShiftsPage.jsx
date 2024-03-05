import React, { useEffect, useState } from 'react';
import { useSocket } from '../utils';

const getShiftParts = (shiftDetails, nextSunday) => {
  const currentWeekShifts = shiftDetails.filter(shift => {
    const shiftDate = new Date(shift.shiftDate);
    const nextSundayMidnight = new Date(nextSunday);
    nextSundayMidnight.setHours(0, 0, 0, 0);
    const endOfWeek = new Date(nextSundayMidnight.getTime() + 7 * 24 * 60 * 60 * 1000);

    return shiftDate >= nextSundayMidnight && shiftDate < endOfWeek;
  });

  const shiftPartsByDate = {};
  currentWeekShifts.forEach(shift => {
    const dateKey = new Date(shift.shiftDate).toLocaleDateString();
    if (!shiftPartsByDate[dateKey]) {
      shiftPartsByDate[dateKey] = [];
    }
    shiftPartsByDate[dateKey].push(shift.shiftPart);
  });

  // Sort shift parts within each day (morning, noon, evening)
  Object.keys(shiftPartsByDate).forEach(dateKey => {
    shiftPartsByDate[dateKey] = shiftPartsByDate[dateKey].sort((a, b) => {
      const order = { morning: 1, noon: 2, evening: 3 };
      return order[a] - order[b];
    });
  });

  return shiftPartsByDate;
};

const CalendarPage = () => {
  const socket = useSocket();
  const [shiftDetails, setShiftDetails] = useState([]);
  const [nextSunday, setNextSunday] = useState(new Date());

  useEffect(() => {
    const getNextSunday = () => {
      const today = new Date();
      const daysUntilSunday = 7 - today.getDay();
      return new Date(today.getTime() + daysUntilSunday * 24 * 60 * 60 * 1000);
    };

    if (socket && socket.readyState === WebSocket.OPEN) {
      const getShiftsRequest = {
        request_id: 90,
      };
      socket.send(JSON.stringify(getShiftsRequest));

      const handleSocketMessage = (event) => {
        const response = JSON.parse(event.data);
        if (response && response.request_id === 90) {
          setShiftDetails(response.data);
        }
      };

      socket.addEventListener('message', handleSocketMessage);

      setNextSunday(getNextSunday());

      return () => {
        socket.removeEventListener('message', handleSocketMessage);
      };
    }
  }, [socket]);

  const shiftPartsByDate = getShiftParts(shiftDetails, nextSunday);

  return (
    <div>
      <h2>My Shifts</h2>
      <div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'center', alignItems: 'center' }}>
        {Array.from({ length: 7 }, (_, index) => {
          const currentDate = new Date(nextSunday.getTime() + index * 24 * 60 * 60 * 1000);
          const dateKey = currentDate.toLocaleDateString();
          const shiftParts = shiftPartsByDate[dateKey];

          return (
            <div
              key={index}
              style={{
                position: 'relative',
                padding: '5px',
                textAlign: 'center',
                flex: 1,
                margin: '5px',
              }}
            >
              <div
                style={{
                  backgroundColor: 'blue',
                  color: 'white',
                  padding: '8px',
                  borderRadius: '5px',
                  position: 'absolute',
                  top: '0',
                  left: '0',
                  right: '0',
                }}
              >
                {currentDate.toLocaleDateString('en-US', { weekday: 'long' })}
                <p style={{ fontSize: '14px', fontWeight: 'bold', marginBottom: '5px', marginTop: '5px' }}>
                  {currentDate.toLocaleDateString()}
                </p>
              </div>
              <div
                style={{
                  backgroundColor: shiftParts ? '#D1EEFC' : '#EFEFF4',
                  border: '1px solid #ddd',
                  padding: '10px',
                  textAlign: 'center',
                  borderRadius: '8px',
                  height: '120px',
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  justifyContent: 'center',
                  marginTop: '55px',
                }}
              >
                {shiftParts &&
                  shiftParts.map((shiftPart, partIndex) => (
                    <div
                      key={partIndex}
                      style={{ backgroundColor: '#007AFF', color: 'white', padding: '8px', borderRadius: '5px', margin: '2px' }}
                    >
                      {shiftPart}
                    </div>
                  ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default CalendarPage;
