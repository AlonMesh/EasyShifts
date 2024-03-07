import React, {useEffect, useState} from 'react';
import EmployeeShifts from './EmployeeShifts';
import ScheduleBoard from "./ScheduleBoard";
import '../../css/ManagerSchedule.css';

function ManagerSchedule({socket}) {
    // State
    const [loading, setLoading] = useState(true);
    const [employeesRequests, setEmployeesRequests] = useState([]);
    const [allWorkers, setAllWorkers] = useState([]);
    const [preferences, setPreferences] = useState({
        number_of_shifts_per_day: 2,
        closed_days: []
    });
    const [startDate, setStartDate] = useState(null);
    const [assignedShifts, setAssignedShifts] = useState([]);

    const getEmployeesRequestsData = () => {
        return new Promise((resolve, reject) => {
            try {
                if (!socket) {
                    console.error('Socket connection is not available - GERD.');
                    reject('Socket connection is not available - GERD.');
                    return;
                }

                const request = {
                    request_id: 91,
                };

                // Send the request to the server
                socket.send(JSON.stringify(request));

                // Create a separate function to handle the message event
                const handleMessage = (event) => {
                    // Check if the WebSocket connection is still open
                    if (socket.readyState === WebSocket.OPEN) {
                        const response = JSON.parse(event.data);
                        if (response.request_id === 91) {
                            resolve(response.data);
                        }
                    } else {
                        reject('WebSocket connection is closed');
                    }
                };
                if (socket) {
                    console.log("Action: addEventListener")
                    // Attach the message handler to the onmessage event
                    socket.addEventListener('message', handleMessage);
                }
            } catch (error) {
                console.error('Error occurred while getting employees requests data:', error);
                reject(error);
            }
        });
    };

    const getAllWorkers = () => {
        return new Promise((resolve, reject) => {
            try {
                if (!socket) {
                    console.error('Socket connection is not available - GAW.');
                    reject('Socket connection is not available - GAW.');
                    return;
                }

                const request = {
                    request_id: 93,
                };

                // Send the request to the server
                socket.send(JSON.stringify(request));

                // Create a separate function to handle the message event
                const handleMessage = (event) => {
                    // Check if the WebSocket connection is still open
                    if (socket.readyState === WebSocket.OPEN) {
                        const data = JSON.parse(event.data);
                        if (data.request_id === 93) {
                            resolve(data.data);
                        }
                    } else {
                        reject('WebSocket connection is closed');
                    }
                };

                // Attach the message handler to the onmessage event
                socket.addEventListener('message', handleMessage);
            } catch (error) {
                console.error('Error occurred while getting all employees names:', error);
                reject(error);
            }
        });
    };

    const getPreferences = () => {
        return new Promise((resolve, reject) => {
            try {
                if (!socket) {
                    console.error('Socket connection is not available - GP.');
                    reject('Socket connection is not available - GP.');
                    return;
                }

                const request = {
                    request_id: 95,
                };

                // Send the request to the server
                socket.send(JSON.stringify(request));

                // Create a separate function to handle the message event
                const handleMessage = (event) => {
                    // Check if the WebSocket connection is still open
                    if (socket.readyState === WebSocket.OPEN) {
                        const response = JSON.parse(event.data);
                        if (response.request_id === 95) {
                            resolve(response.data);
                        }
                    } else {
                        reject('WebSocket connection is closed');
                    }
                };

                // Attach the message handler to the onmessage event
                socket.addEventListener('message', handleMessage);
            } catch (error) {
                console.error('Error occurred while getting preferences:', error);
                reject(error);
            }
        });
    };

    const getStartDate = () => {
        return new Promise((resolve, reject) => {
            try {
                if (!socket) {
                    console.error('Socket connection is not available - GP.');
                    reject('Socket connection is not available - GP.');
                    return;
                }

                const request = {
                    request_id: 97,
                };

                // Send the request to the server
                socket.send(JSON.stringify(request));

                // Create a separate function to handle the message event
                const handleMessage = (event) => {
                    // Check if the WebSocket connection is still open
                    if (socket.readyState === WebSocket.OPEN) {
                        const data = JSON.parse(event.data);
                        if (data.request_id === 97) {
                            resolve(new Date(data.data));
                        }
                    } else {
                        reject('WebSocket connection is closed');
                    }
                };

                // Attach the message handler to the onmessage event
                socket.addEventListener('message', handleMessage);
            } catch (error) {
                console.error('Error occurred while getting preferences:', error);
                reject(error);
            }
        });
    };

    const getAssignedShifts = ({startDate}) => {
        return new Promise((resolve, reject) => {
            try {
                if (!socket) {
                    console.error('Socket connection is not available - GP.');
                    reject('Socket connection is not available - GP.');
                    return;
                }

                if (startDate === null || startDate === undefined) {
                    console.error('Start date is not available in getAssignedShifts.');
                    reject('Start date is not available in getAssignedShifts.');
                    return;
                }

                const request = {
                    request_id: 98,
                    data: {
                        start_date: startDate,
                    },
                };

                // Send the request to the server
                socket.send(JSON.stringify(request));

                // Create a separate function to handle the message event
                const handleMessage = (event) => {
                    // Check if the WebSocket connection is still open
                    if (socket.readyState === WebSocket.OPEN) {
                        const data = JSON.parse(event.data);
                        console.log('recived:: ', data);
                        if (data.request_id === 98) {
                            resolve(data.data);
                        }
                    } else {
                        reject('WebSocket connection is closed');
                    }
                };

                // Attach the message handler to the onmessage event
                socket.addEventListener('message', handleMessage);
            } catch (error) {
                console.error('Error occurred while getting preferences:', error);
                reject(error);
            }
        });
    };


    useEffect(() => {
        // Function to handle the message event
        const handleMessage = (event) => {
            try {
                const data = JSON.parse(event.data);

                switch (data.request_id) {
                    case 91:
                        setEmployeesRequests(data.data);
                        break;
                    case 93:
                        setAllWorkers(data.data);
                        break;
                    case 95:
                        setPreferences(data.data);
                        break;
                    case 97:
                        setStartDate(new Date(data.data));
                        break;
                    case 98:
                        setAssignedShifts(data.data);
                        console.log('DONE: assignedShifts:', data.data);
                        break;
                    default:
                        // Handle other cases if needed
                        break;
                }
            } catch (error) {
                console.error('Error parsing WebSocket message:', error);
            }
        };

        // Attach the message handler to the onmessage event
        if (socket) {
            console.log("Action: addEventListener")
            socket.addEventListener('message', handleMessage);
        }

        // Fetch initial data
        const fetchData = async () => {
            try {
                // Set loading to true
                setLoading(true);

                console.log('socket2: ' + socket);

                const employeesRequests = await getEmployeesRequestsData();
                setEmployeesRequests(employeesRequests);

                const allWorkers = await getAllWorkers();
                setAllWorkers(allWorkers);

                const preferences = await getPreferences();
                setPreferences(preferences);

                const startDate = await getStartDate();
                setStartDate(startDate);

                const assignedShifts = await getAssignedShifts({startDate});
                setAssignedShifts(assignedShifts);
                console.log('DONE: assignedShifts:', assignedShifts);
            } catch (error) {
                console.log(error);
            } finally {
                setLoading(false);
            }
        };

        fetchData(); // Fetch data when the component mounts

        // Clean up the event listener when the component is unmounted
        return () => {
            if (socket) {
                console.log("Action: removeEventListener");
                socket.removeEventListener('message', handleMessage);
            }
        };
    }, [socket]);
    // Render the ManagerSchedule component
    return (
        <div className="manager-schedule">
            {/* Display EmployeeShifts and ScheduleBoard components */}
            {loading ? (
                <div>Loading...</div>
            ) : (
                <div className="board-and-requests">
                    <EmployeeShifts employees={employeesRequests} className="EmployeeShifts" />
                    {preferences ? (
                        <ScheduleBoard
                            partsCount={preferences.number_of_shifts_per_day}
                            closedDays={preferences.closed_days}
                            startDate={startDate}
                            allWorkers={allWorkers}
                            assignedShifts={assignedShifts}
                            className="ScheduleBoard"
                        />
                    ) : (
                        <div>No preferences available</div>
                    )}
                </div>
            )}

            {/* Action Buttons */}
            {/*<div className="buttons">*/}
            {/*    <button>Save</button>*/}
            {/*    <button>Clean</button>*/}
            {/*    <button>Publish</button>*/}
            {/*</div>*/}
        </div>
    );
}

export default ManagerSchedule;