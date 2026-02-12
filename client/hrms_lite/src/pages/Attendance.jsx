import { useState } from 'react';
import AttendanceForm from '../components/AttendanceForm';
import AttendanceList from '../components/AttendanceList';

export default function Attendance() {
  const [selectedEmployeeId, setSelectedEmployeeId] = useState(null);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleEmployeeSelect = (employeeId) => {
    setSelectedEmployeeId(employeeId);
  };

  const handleSubmitSuccess = () => {
    setRefreshTrigger((c) => c + 1);
  };

  return (
    <div className="page">
      <AttendanceForm
        onSuccess={handleEmployeeSelect}
        onSubmitSuccess={handleSubmitSuccess}
      />
      <AttendanceList
        employeeId={selectedEmployeeId}
        refreshTrigger={refreshTrigger}
      />
    </div>
  );
}
