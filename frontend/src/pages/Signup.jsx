import React, { useState } from 'react';
import axios from 'axios';

export default function Signup() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [rank, setRank] = useState('');
  const [role, setRole] = useState('');
  const [idNumber, setIdNumber] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const response = await axios.post('/auth/register', {
        username,
        password,
        rank,
        role,
        id_number: idNumber,
        phone_number: phoneNumber
      });
      alert('המשתמש נרשם בהצלחה!');
      setUsername('');
      setPassword('');
      setRank('');
      setRole('');
      setIdNumber('');
      setPhoneNumber('');
    } catch (err) {
      setError('שגיאה בהרשמה');
    }
  };

  return (
    <div style={{ direction: 'rtl', textAlign: 'center', marginTop: '50px' }}>
      <h2>הרשמה למערכת</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <input
            type="text"
            placeholder="שם משתמש"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div>
          <input
            type="password"
            placeholder="סיסמה"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <div>
          <input
            type="text"
            placeholder="דרגה"
            value={rank}
            onChange={(e) => setRank(e.target.value)}
            required
          />
        </div>
        <div>
          <input
            type="text"
            placeholder="תפקיד"
            value={role}
            onChange={(e) => setRole(e.target.value)}
            required
          />
        </div>
        <div>
          <input
            type="text"
            placeholder="מספר אישי/ת.ז"
            value={idNumber}
            onChange={(e) => setIdNumber(e.target.value)}
            required
          />
        </div>
        <div>
          <input
            type="text"
            placeholder="מספר טלפון"
            value={phoneNumber}
            onChange={(e) => setPhoneNumber(e.target.value)}
            required
          />
        </div>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        <button type="submit">הירשם</button>
      </form>
    </div>
  );
}
