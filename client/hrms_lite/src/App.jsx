import { Routes, Route, NavLink } from 'react-router-dom';
import Employees from './pages/Employees';
import Attendance from './pages/Attendance';
import './styles.css';

function App() {
  return (
    <div className="app">
      <nav className="nav">
        <span className="nav-brand">HRMS Lite</span>
        <NavLink to="/employees">Employees</NavLink>
        <NavLink to="/attendance">Attendance</NavLink>
      </nav>
      <Routes>
        <Route path="/" element={<Employees />} />
        <Route path="/employees" element={<Employees />} />
        <Route path="/attendance" element={<Attendance />} />
      </Routes>
    </div>
  );
}

export default App;
