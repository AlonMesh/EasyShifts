import '../../css/EmployeeShiftItem.css';

function EmployeeShiftItem({name, request}) {
    return (
                <div className="shift-item-frame">
                    <h3>{name}</h3>
                    <p>{request}</p>
                </div>
    );
}

export default EmployeeShiftItem;