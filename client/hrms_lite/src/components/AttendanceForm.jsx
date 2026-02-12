import { useState, useEffect } from 'react';
import api from '../api/axios';

export default function AttendanceForm({ onSuccess, onSubmitSuccess }) {
  const [employees, setEmployees] = useState([]);
  const [employeeId, setEmployeeId] = useState('');
  const [date, setDate] = useState('');
  const [status, setStatus] = useState('Present');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [loadingEmployees, setLoadingEmployees] = useState(true);

  useEffect(() => {
    let cancelled = false;
    setLoadingEmployees(true);
    api
      .get('/employees')
      .then((res) => {
        if (!cancelled) setEmployees(res.data);
      })
      .catch(() => {
        if (!cancelled) setEmployees([]);
      })
      .finally(() => {
        if (!cancelled) setLoadingEmployees(false);
      });
    return () => { cancelled = true; };
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await api.post('/attendance', {
        employee_id: Number(employeeId),
        date,
        status,
      });
      setDate('');
      setStatus('Present');
      onSubmitSuccess?.();
    } catch (err) {
      const d = err.response?.data?.detail;
      setError(Array.isArray(d) ? d.map((x) => x.msg || JSON.stringify(x)).join(', ') : d || err.message || 'Failed to mark attendance');
    } finally {
      setLoading(false);
    }
  };

  if (loadingEmployees) return <p className="state-msg">Loading employees...</p>;

  return (
    <form onSubmit={handleSubmit} className="form-block">
      <h2>Mark Attendance</h2>
      <div className="form-row">
        <label>Employee</label>
        <select
          value={employeeId}
          onChange={(e) => {
            const val = e.target.value;
            setEmployeeId(val);
            onSuccess?.(val ? Number(val) : null);
          }}
          required
        >
          <option value="">Select employee</option>
          {employees.map((emp) => (
            <option key={emp.id} value={emp.id}>
              {emp.employee_id} – {emp.full_name}
            </option>
          ))}
        </select>
      </div>
      <div className="form-row">
        <label>Date</label>
        <input
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
          required
        />
      </div>
      <div className="form-row">
        <label>Status</label>
        <select value={status} onChange={(e) => setStatus(e.target.value)}>
          <option value="Present">Present</option>
          <option value="Absent">Absent</option>
        </select>
      </div>
      {error && <p className="error-msg">{error}</p>}
      <button type="submit" disabled={loading}>
        {loading ? 'Submitting...' : 'Submit'}
      </button>
    </form>
  );
}
