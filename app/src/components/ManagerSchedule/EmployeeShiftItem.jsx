import '../../css/EmployeeShiftItem.css';

function EmployeeShiftItem({name, request}) {
    return (
        <div className="shift-item-frame">
            <div className="shift-item">
                <h3>{name}</h3>
                <p>{request}</p>
            </div>
        </div>
    );
}

export default EmployeeShiftItem;