import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../api/axios';

export default function Dashboard() {
  const [stats, setStats] = useState({ total_employees: 0, present_today: 0, absent_today: 0 });
  const [recent, setRecent] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError('');
    Promise.all([
      api.get('/dashboard/stats'),
      api.get('/dashboard/recent-attendance', { params: { limit: 10 } }),
    ])
      .then(([statsRes, recentRes]) => {
        if (!cancelled) {
          setStats(statsRes.data);
          setRecent(recentRes.data);
        }
      })
      .catch((err) => {
        if (!cancelled) {
          const d = err.response?.data?.detail;
          setError(Array.isArray(d) ? d.map((x) => x.msg || JSON.stringify(x)).join(', ') : d || err.message || 'Failed to load dashboard');
        }
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => { cancelled = true; };
  }, []);

  if (loading) return <p className="state-msg">Loading dashboard...</p>;
  if (error) return <p className="error-msg">{error}</p>;

  return (
    <div className="dashboard">
      <div className="dashboard__cards">
        <div className="stat-card stat-card--blue">
          <div className="stat-card__icon">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
              <circle cx="9" cy="7" r="4" />
              <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
              <path d="M16 3.13a4 4 0 0 1 0 7.75" />
            </svg>
          </div>
          <div className="stat-card__content">
            <span className="stat-card__label">Total Employees</span>
            <span className="stat-card__value">{stats.total_employees}</span>
          </div>
        </div>
        <div className="stat-card stat-card--green">
          <div className="stat-card__icon">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
              <polyline points="22 4 12 14.01 9 11.01" />
            </svg>
          </div>
          <div className="stat-card__content">
            <span className="stat-card__label">Present Today</span>
            <span className="stat-card__value">{stats.present_today}</span>
          </div>
        </div>
        <div className="stat-card stat-card--red">
          <div className="stat-card__icon">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
          </div>
          <div className="stat-card__content">
            <span className="stat-card__label">Absent Today</span>
            <span className="stat-card__value">{stats.absent_today}</span>
          </div>
        </div>
      </div>
      <div className="dashboard__section table-wrap">
        <h2>Recent Attendance</h2>
        {recent.length === 0 ? (
          <p className="state-msg">No recent attendance records</p>
        ) : (
          <>
            <table>
              <thead>
                <tr>
                  <th>Employee</th>
                  <th>Date</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {recent.map((row) => (
                  <tr key={row.id}>
                    <td>{row.employee_name}</td>
                    <td>{row.date}</td>
                    <td>
                      <span className={`status-badge status-badge--${row.status === 'Present' ? 'present' : 'absent'}`}>
                        {row.status}
                      </span>
                    </td>
                    <td>
                      <Link to={`/employees?highlight=${row.employee_id}`} className="link-detail">
                        View Details
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            <div className="dashboard__actions">
              <Link to="/attendance" className="btn btn-primary">
                View All Attendance
              </Link>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
