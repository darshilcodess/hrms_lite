import { useState, useEffect } from 'react';
import api from '../api/axios';

export default function EmployeeList({ refreshTrigger }) {
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchEmployees = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await api.get('/employees');
      setEmployees(res.data);
    } catch (err) {
      const d = err.response?.data?.detail;
      setError(Array.isArray(d) ? d.map((x) => x.msg || JSON.stringify(x)).join(', ') : d || err.message || 'Failed to load employees');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEmployees();
  }, [refreshTrigger]);

  const handleDelete = async (id) => {
    try {
      await api.delete(`/employees/${id}`);
      setEmployees((prev) => prev.filter((e) => e.id !== id));
    } catch (err) {
      const d = err.response?.data?.detail;
      setError(Array.isArray(d) ? d.map((x) => x.msg || JSON.stringify(x)).join(', ') : d || err.message || 'Failed to delete');
    }
  };

  if (loading) return <p className="state-msg">Loading...</p>;
  if (error) return <p className="error-msg">{error}</p>;
  if (employees.length === 0) return <p className="state-msg">No employees found</p>;

  return (
    <div className="table-wrap">
      <h2>Employee List</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Employee ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Department</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {employees.map((emp) => (
            <tr key={emp.id}>
              <td>{emp.id}</td>
              <td>{emp.employee_id}</td>
              <td>{emp.full_name}</td>
              <td>{emp.email}</td>
              <td>{emp.department}</td>
              <td>
                <button type="button" onClick={() => handleDelete(emp.id)} className="btn-danger">
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
