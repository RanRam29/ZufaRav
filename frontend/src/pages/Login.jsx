import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "../axiosInstance";

export default function Login() {
  const [formData, setFormData] = useState({ username: "", password: "" });
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const response = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/auth/login`, formData);
      localStorage.setItem("token", response.data.access_token);
      navigate("/dashboard");
    } catch (err) {
      setError("התחברות נכשלה: טוקן לא התקבל");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-blue-900 flex items-center justify-center px-4">
      <div className="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-md text-right">
        <h2 className="text-3xl font-bold mb-6 text-gray-800">התחברות למערכת ZufaRav</h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="username" className="block text-sm font-medium text-gray-600">
              שם משתמש
            </label>
            <input
              id="username"
              name="username"
              type="text"
              autoComplete="username"
              value={formData.username}
              onChange={handleChange}
              className="w-full border rounded-xl px-4 py-2 mt-1 text-right"
              required
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-600">
              סיסמה
            </label>
            <input
              id="password"
              name="password"
              type="password"
              autoComplete="current-password"
              value={formData.password}
              onChange={handleChange}
              className="w-full border rounded-xl px-4 py-2 mt-1 text-right"
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
