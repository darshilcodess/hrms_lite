import { useState, useEffect } from 'react';
import api from '../api/axios';

export default function AttendanceList({ employeeId, refreshTrigger }) {
  const [list, setList] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!employeeId) {
      setList([]);
      setError('');
      return;
    }
    setLoading(true);
    setError('');
    api
      .get('/attendance', { params: { employee_id: employeeId } })
      .then((res) => setList(res.data))
      .catch((err) => {
        setList([]);
        const d = err.response?.data?.detail;
        setError(Array.isArray(d) ? d.map((x) => x.msg || JSON.stringify(x)).join(', ') : d || err.message || 'Failed to load attendance');
      })
      .finally(() => setLoading(false));
  }, [employeeId, refreshTrigger]);

  if (!employeeId) return <p className="state-msg">Select an employee to view attendance</p>;
  if (loading) return <p className="state-msg">Loading...</p>;
  if (error) return <p className="error-msg">{error}</p>;
  if (list.length === 0) return <p className="state-msg">No attendance records</p>;

  return (
    <div className="table-wrap">
      <h2>Attendance</h2>
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {list.map((row) => (
            <tr key={row.id}>
              <td>{row.date}</td>
              <td>{row.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
