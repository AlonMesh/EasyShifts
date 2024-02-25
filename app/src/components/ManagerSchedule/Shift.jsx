import "../../css/Shift.css";
import {useState} from "react";
import Tooltip from "./Tooltip";
import WorkerList from "./WorkerList";

function Shift({workplaceId, date, part, workers, allWorkers}) {
    const [showTooltip, setShowTooltip] = useState(false);
    const [editing, setEditing] = useState(false);
    const [selectedWorkers, setSelectedWorkers] = useState(workers);

    function handleEditClick() {
        return !editing
    }

    function handleRemoveWorker(name) {
        setSelectedWorkers(prev =>
            prev.filter(worker => worker !== name)
        );
    }

    function handleAddWorker(name) {
        if (name !== null) {
            if (!selectedWorkers.includes(name))
                setSelectedWorkers(prev => [...prev, name]);
        }
    }

    return (
        <>
            <div className="shift">

                <div className="shift-header">

                    <div
                        className="info-icon"
                        onMouseEnter={() => setShowTooltip(true)}
                        onMouseLeave={() => setShowTooltip(false)}
                    >
                    </div>

                    <Tooltip show={showTooltip}>
                        <div className="shift-info">
                            <p>Workplace: {workplaceId}</p>
                            <p>Date: {date}</p>
                            <p>Part: {part}</p>
                        </div>
                    </Tooltip>

                    <div className="edit-workers" onClick={() => setEditing(handleEditClick)}>
                        {editing ? 'D' : 'E'}
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
        </>
    )
        ;

}

export default Shift;