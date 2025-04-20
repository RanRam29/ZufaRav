import React, { useState } from 'react';
import axios from 'axios';

axios.defaults.baseURL = import.meta.env.VITE_API_BASE_URL;

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async () => {
    try {
      const res = await axios.post('/auth/login', {
        username,
        password
      });
      localStorage.setItem('username', res.data.username);
      alert('התחברת בהצלחה!');
      window.location.href = '/dashboard';
    } catch (err) {
      console.error('Login failed:', err);
      alert('שגיאת התחברות');
    }
  };

  return (
    <div style={{ direction: 'rtl', textAlign: 'center', marginTop: 50 }}>
      <h2>התחברות</h2>
      <input
        placeholder="שם משתמש"
        onChange={e => setUsername(e.target.value)}
        value={username}
      />
      <br />
      <input
        placeholder="סיסמה"
        type="password"
        onChange={e => setPassword(e.target.value)}
        value={password}
      />
      <br />
      <button onClick={handleLogin}>התחבר</button>
    </div>
  );
}
