import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { useEffect, useState } from "react";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Dashboard from "./pages/Dashboard";
import UserMovementDashboard from "./pages/UserMovementDashboard";
import CreateEvent from "./pages/CreateEvent";
import EventAuditDashboard from "./pages/EventAuditDashboard";
import ArchivedEvents from "./pages/ArchivedEvents"; // ✅ חדש

export default function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));

  useEffect(() => {
    const handleStorageChange = () => {
      setToken(localStorage.getItem("token"));
    };
    window.addEventListener("storage", handleStorageChange);
    return () => window.removeEventListener("storage", handleStorageChange);
  }, []);

  return (
    <div dir="rtl" className="font-sans">
      <Router>
        <Routes>
          <Route path="/" element={token ? <Navigate to="/dashboard" /> : <Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route
            path="/dashboard"
            element={token ? <Dashboard /> : <Navigate to="/" replace />}
          />
          <Route
            path="/create-event"
            element={token ? <CreateEvent /> : <Navigate to="/" replace />}
          />
          <Route
            path="/movement"
            element={token ? <UserMovementDashboard /> : <Navigate to="/" replace />}
          />
          <Route
            path="/audit"
            element={token ? <EventAuditDashboard /> : <Navigate to="/" replace />}
          />
          <Route
            path="/reports"
            element={token ? <ArchivedEvents /> : <Navigate to="/" replace />} // ✅ חדש
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Router>
    </div>
  );
}
