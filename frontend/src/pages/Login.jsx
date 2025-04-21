import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");

    if (!username.trim()) return setError("יש להזין שם משתמש");
    if (password.length < 3) return setError("סיסמה חייבת להכיל לפחות 3 תווים");

    try {
      const res = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/auth/login`, {
        username,
        password,
      });

      if (res.data.access_token) {
        localStorage.setItem("token", res.data.access_token);
        navigate("/dashboard");
      } else {
        setError("התחברות נכשלה: טוקן לא התקבל");
      }
    } catch (err) {
      setError(err?.response?.data?.detail || "שגיאה בהתחברות");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-blue-900 flex items-center justify-center px-4">
      <div className="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-md text-right">
        <h2 className="text-3xl font-bold mb-6 text-gray-800">התחברות למערכת ZufaRav</h2>

        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-600">שם משתמש</label>
            <input
              type="text"
              className="w-full border rounded-xl px-4 py-2 mt-1 text-right"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-600">סיסמה</label>
            <input
              type="password"
              className="w-full border rounded-xl px-4 py-2 mt-1 text-right"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {error && (
            <div className="text-red-600 text-sm bg-red-100 px-3 py-2 rounded-xl text-center">
              {error}
            </div>
          )}

          <button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 rounded-xl transition duration-200"
          >
            התחבר
          </button>

          <div className="text-center text-sm mt-4">
            אין לך חשבון?{" "}
            <a href="/signup" className="text-blue-600 hover:underline">
              לעמוד הרשמה
            </a>
          </div>
        </form>
      </div>
    </div>
  );
}
