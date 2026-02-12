import { useState } from 'react';
import EmployeeForm from '../components/EmployeeForm';
import EmployeeList from '../components/EmployeeList';

export default function Employees() {
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  return (
    <div className="page">
      <EmployeeForm onSuccess={() => setRefreshTrigger((c) => c + 1)} />
      <EmployeeList refreshTrigger={refreshTrigger} />
    </div>
  );
}
