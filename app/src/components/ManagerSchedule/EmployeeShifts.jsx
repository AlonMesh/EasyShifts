import EmployeeShiftItem from "./EmployeeShiftItem";
import '../../css/EmployeeShifts.css';

function EmployeeShifts({employees}) {
  return (
    <div className="employee-shifts">
      <h2>Employee Shifts</h2>

      <div className="shift-list">
        {employees.map(emp => (
          <EmployeeShiftItem
            name={emp.name}
            request={emp.request}
          />
        ))}
      </div>
    </div>
  );
}

export default EmployeeShifts;