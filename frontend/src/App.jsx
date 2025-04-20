import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Signup from './pages/Signup';
import Login from './pages/Login';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} /> {/* התחברות ראשית */}
        <Route path="/signup" element={<Signup />} /> {/* הרשמה */}
        <Route path="/dashboard" element={<Dashboard />} /> {/* דשבורד */}
      </Routes>
    </Router>
  );
}

export default App;
