import "../../css/Shift.css";
import {useState} from "react";
import Tooltip from "./Tooltip";
import WorkerList from "./WorkerList";
import {InfoIcon} from "../Icons/Info";
import {EditIcon} from "../Icons/Edit";
import {SaveIcon} from "../Icons/Save";
import {useSocket} from "../../utils";

function Shift({date, part, workers, allWorkers, workersShifts}) {
    console.log("date:", date)
    console.log("part:", part)
    console.log("workerss:", workers)
    console.log("allWorkers:", allWorkers)
    console.log("workersShifts:", workersShifts)

    const [showTooltip, setShowTooltip] = useState(false);
    const [editing, setEditing] = useState(false);
    const [selectedWorkers, setSelectedWorkers] = useState(workers);
    const socket = useSocket();

    function handleEditClick() {
        return !editing
    }

    function handleRemoveWorker(name) {
        setSelectedWorkers(prev =>
            prev.filter(worker => worker !== name)
        );

        // Find worker
        const worker = workersShifts.find(w => w.name === name);

        // Remove shift from worker
        worker.shifts = worker.shifts.filter(shift => shift.date !== date || shift.part !== part);

        console.log("Lets remove ", worker, " from the shift ", date, " ", part, "socket", socket) // TODO: Remove
        // Send to the server those details to remove the shift from the worker

        if (socket && socket.readyState === WebSocket.OPEN) {
            const request = {
                request_id: 99,
                data: {
                    type: "removeShift",
                    worker_name: worker,
                    day: date,
                    part: part,
                },
            };

            socket.send(JSON.stringify(request));
            console.log("Sent to server: ", request);
        }

    }

    function handleAddWorker(name) {
        if (name !== null) {
            if (!selectedWorkers.includes(name)) {
                setSelectedWorkers(prev => [...prev, name]);

                // Find worker
                const worker = workersShifts.find(w => w.name === name);

                // Add shift to worker
                worker.shifts.push({
                    date: date,
                    part: part
                });

                console.log("Lets add ", worker, " to the shift ", date, " ", part, "socket", socket) // TODO: Remove
                // Send to the server those details to add the shift to the worker

                if (socket && socket.readyState === WebSocket.OPEN) {
                    const request = {
                        request_id: 99,
                        data: {
                            type: "addShift",
                            worker_name: worker,
                            day: date,
                            part: part,
                        },
                    };

                    socket.send(JSON.stringify(request));
                    console.log("Sent to server: ", request);
                }
            }
        }
    }

    return (
        <div className="shift">

            <div className="shift-header">

                <InfoIcon
                    className="info-icon"
                    onMouseEnter={() => setShowTooltip(true)}
                    onMouseLeave={() => setShowTooltip(false)}
                >
                </InfoIcon>

                <Tooltip show={showTooltip}>
                    <div className="shift-info">
                        <p>Date: {date}</p>
                        <p>Part: {part}</p>
                    </div>
                </Tooltip>

                <div className="edit-workers" onClick={() => setEditing(handleEditClick)}>
                    {editing ? <SaveIcon/> : <EditIcon/>}
                </div>
            </div>

            <div className="shift-workers">
                {editing ? (
                    <div className="edit-workers-panel">
                        {/* Add worker dropdown */}
                        <WorkerList
                            allWorkers={allWorkers}
                            selectedWorkers={selectedWorkers}
                            onSelect={handleAddWorker}
                        />

                        {/* Display current workers */}
                        {selectedWorkers.map(name => (
                            <div key={name}>
                                <span>{name}</span>
                                <button onClick={() => handleRemoveWorker(name)}>
                                    x
                                </button>
                            </div>
                        ))}
                    </div>
                ) : (
                    <div className="shift-workers">
                        {selectedWorkers.map(worker => (
                            <p key={worker}>{worker}</p>))}
                    </div>
                )}

            </div>

        </div>
    );

}

export default Shift;