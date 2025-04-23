import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "../axiosInstance";

export default function Signup() {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
    rank: "",
    role: "",
    id_number: "",
    phone_number: "",
    full_name: "",
    email: "",
  });

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
      await axios.post(`${import.meta.env.VITE_API_BASE_URL}/auth/register`, formData);
      navigate("/");
    } catch (err) {
      setError(err?.response?.data?.detail || "שגיאה בהרשמה");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-blue-900 flex items-center justify-center px-4">
      <div className="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-md text-right">
        <h2 className="text-3xl font-bold mb-6 text-gray-800">הרשמה למערכת ZufaRav</h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          <Input label="שם משתמש" name="username" value={formData.username} onChange={handleChange} required />
          <Input label="סיסמה" name="password" type="password" value={formData.password} onChange={handleChange} required />
          <Input label="דרגה" name="rank" value={formData.rank} onChange={handleChange} required />
          <Input label="תפקיד" name="role" value={formData.role} onChange={handleChange} required />
          <Input label="מספר אישי" name="id_number" value={formData.id_number} onChange={handleChange} required />
          <Input label="מספר טלפון" name="phone_number" value={formData.phone_number} onChange={handleChange} required />
          <Input label="שם מלא" name="full_name" value={formData.full_name} onChange={handleChange} />
          <Input label="אימייל" name="email" type="email" value={formData.email} onChange={handleChange} />

          {error && (
            <div className="text-red-600 text-sm bg-red-100 px-3 py-2 rounded-xl text-center">
              {error}
            </div>
          )}

          <button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 rounded-xl transition duration-200"
          >
            הרשם
          </button>

          <div className="text-center text-sm mt-4">
            כבר רשום?{" "}
            <a href="/" className="text-blue-600 hover:underline">
              חזור להתחברות
            </a>
          </div>
        </form>
      </div>
    </div>
  );
}

function Input({ label, name, type = "text", value, onChange, required = false }) {
  return (
    <div>
      <label htmlFor={name} className="block text-sm font-medium text-gray-600">
        {label}
      </label>
      <input
        id={name}
        name={name}
        type={type}
        autoComplete={name}
        value={value}
        onChange={onChange}
        required={required}
        className="w-full border rounded-xl px-4 py-2 mt-1 text-right"
      />
    </div>
  );
}
