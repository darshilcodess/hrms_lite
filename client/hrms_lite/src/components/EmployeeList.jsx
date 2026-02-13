import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import api from '../api/axios';
import EmployeeDetailModal from './EmployeeDetailModal';

export default function EmployeeList({ refreshTrigger }) {
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [detailId, setDetailId] = useState(null);
  const [searchParams] = useSearchParams();
  const highlightId = searchParams.get('highlight');

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

  useEffect(() => {
    const id = highlightId ? parseInt(highlightId, 10) : null;
    if (id && !isNaN(id)) setDetailId(id);
  }, [highlightId]);

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this employee? This will also remove their attendance records.')) return;
    try {
      await api.delete(`/employees/${id}`);
      setEmployees((prev) => prev.filter((e) => e.id !== id));
      if (detailId === id) setDetailId(null);
    } catch (err) {
      const d = err.response?.data?.detail;
      setError(Array.isArray(d) ? d.map((x) => x.msg || JSON.stringify(x)).join(', ') : d || err.message || 'Failed to delete');
    }
  };

  const formatDate = (d) => {
    if (!d) return '—';
    try {
      const dt = typeof d === 'string' ? new Date(d) : d;
      return dt.toLocaleDateString('en-CA', { year: 'numeric', month: 'short', day: 'numeric' });
    } catch {
      return d;
    }
  };

  if (loading) return <p className="state-msg">Loading...</p>;
  if (error) return <p className="error-msg">{error}</p>;
  if (employees.length === 0) return <p className="state-msg">No employees found</p>;

  return (
    <>
      <div className="table-wrap">
        <h2>Employee List</h2>
        <div className="table-scroll">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Employee ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Department</th>
                <th>Joined</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {employees.map((emp) => (
                <tr key={emp.id} className={detailId === emp.id ? 'row-highlight' : ''}>
                  <td>{emp.id}</td>
                  <td>{emp.employee_id}</td>
                  <td>{emp.full_name}</td>
                  <td>{emp.email}</td>
                  <td>{emp.department}</td>
                  <td>{formatDate(emp.created_at)}</td>
                  <td>
                    <div className="cell-actions">
                      <button type="button" className="btn btn-ghost" onClick={() => setDetailId(emp.id)}>
                        View Details
                      </button>
                      <button type="button" onClick={() => handleDelete(emp.id)} className="btn-danger">
                        Delete
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      {detailId != null && (
        <EmployeeDetailModal employeeId={detailId} onClose={() => setDetailId(null)} />
      )}
    </>
  );
}
