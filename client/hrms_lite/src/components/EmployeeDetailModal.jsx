import { useState, useEffect } from 'react';
import api from '../api/axios';

export default function EmployeeDetailModal({ employeeId, onClose }) {
  const [employee, setEmployee] = useState(null);
  const [attendance, setAttendance] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!employeeId) return;
    setLoading(true);
    setError('');
    Promise.all([
      api.get(`/employees/${employeeId}`),
      api.get('/attendance', { params: { employee_id: employeeId } }),
    ])
      .then(([empRes, attRes]) => {
        setEmployee(empRes.data);
        setAttendance(attRes.data);
      })
      .catch((err) => {
        const d = err.response?.data?.detail;
        setError(Array.isArray(d) ? d.map((x) => x.msg || JSON.stringify(x)).join(', ') : d || err.message || 'Failed to load');
      })
      .finally(() => setLoading(false));
  }, [employeeId]);

  if (!employeeId) return null;

  const formatDate = (d) => {
    if (!d) return '—';
    try {
      const dt = typeof d === 'string' ? new Date(d) : d;
      return dt.toLocaleDateString('en-CA', { year: 'numeric', month: 'short', day: 'numeric' });
    } catch {
      return d;
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose} role="dialog" aria-modal="true" aria-labelledby="employee-detail-title">
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal__header">
          <h2 id="employee-detail-title">Employee Details</h2>
          <button type="button" className="modal__close" onClick={onClose} aria-label="Close">
            ×
          </button>
        </div>
        <div className="modal__body">
          {loading && <p className="state-msg">Loading...</p>}
          {error && <p className="error-msg">{error}</p>}
          {!loading && !error && employee && (
            <>
              <div className="detail-grid">
                <div className="detail-item">
                  <span className="detail-item__label">ID</span>
                  <span className="detail-item__value">{employee.id}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-item__label">Employee ID</span>
                  <span className="detail-item__value">{employee.employee_id}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-item__label">Full Name</span>
                  <span className="detail-item__value">{employee.full_name}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-item__label">Email</span>
                  <span className="detail-item__value">{employee.email}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-item__label">Department</span>
                  <span className="detail-item__value">{employee.department}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-item__label">Joined</span>
                  <span className="detail-item__value">{formatDate(employee.created_at)}</span>
                </div>
              </div>
              <div className="detail-section">
                <h3>Attendance History</h3>
                {attendance.length === 0 ? (
                  <p className="state-msg">No attendance records</p>
                ) : (
                  <table className="detail-table">
                    <thead>
                      <tr>
                        <th>Date</th>
                        <th>Status</th>
                      </tr>
                    </thead>
                    <tbody>
                      {attendance.map((row) => (
                        <tr key={row.id}>
                          <td>{row.date}</td>
                          <td>
                            <span className={`status-badge status-badge--${row.status === 'Present' ? 'present' : 'absent'}`}>
                              {row.status}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                )}
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
