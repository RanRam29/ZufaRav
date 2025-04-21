export default function App() {
  const token = localStorage.getItem("token");

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
            path="/movement"
            element={token ? <UserMovementDashboard /> : <Navigate to="/" replace />}
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Router>
    </div>
  );
}
