import React, { useState } from 'react'
import axios from 'axios'

export default function Login() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  const handleLogin = async () => {
    try {
      const res = await axios.post('http://localhost:8000/auth/login', {
        username,
        password
      })
      // שמירת שם המשתמש בזיכרון הדפדפן
      localStorage.setItem("username", res.data.username)
      alert('התחברת בהצלחה!')
      window.location.href = '/dashboard'
    } catch (err) {
      alert('שגיאת התחברות')
    }
  }

  return (
    <div style={{ direction: 'rtl', textAlign: 'center', marginTop: 50 }}>
      <h2>התחברות</h2>
      <input placeholder="שם משתמש" onChange={e => setUsername(e.target.value)} />
      <br />
      <input placeholder="סיסמה" type="password" onChange={e => setPassword(e.target.value)} />
      <br />
      <button onClick={handleLogin}>התחבר</button>
    </div>
  )
}
