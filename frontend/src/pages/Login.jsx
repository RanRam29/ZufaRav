import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

export default function Signup() {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
    rank: "",
    role: "",
    id_number: "",
    phone_number: "",
  });
  const [errors, setErrors] = useState({});
  const [serverError, setServerError] = useState("");
  const navigate = useNavigate();

  const validate = () => {
    const newErrors = {};
    const phoneRegex = /^(\+972[-\s]?)?0?5[0-9]-?[0-9]{7}$/;
    const idRegex = /^[0-9]{5,10}$/;

    if (!formData.username.trim()) newErrors.username = "יש להזין שם משתמש";
    if (formData.password.length < 4) newErrors.password = "הסיסמה חייבת להכיל לפחות 4 תווים";
    if (!formData.rank.trim()) newErrors.rank = "יש להזין דרגה";
    if (!formData.role.trim()) newErrors.role = "יש להזין תפקיד";
    if (!idRegex.test(formData.id_number)) newErrors.id_number = "מספר אישי לא תקין";
    if (!phoneRegex.test(formData.phone_number)) newErrors.phone_number = "מספר טלפון לא תקין";

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
    setErrors((prev) => ({ ...prev, [e.target.name]: "" }));
    setServerError("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;

    try {
      await axios.post(`${import.meta.env.VITE_API_BASE_URL}/auth/register`, formData);
      navigate("/");
    } catch (err) {
      setServerError(err?.response?.data?.detail || "שגיאה בהרשמה");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-blue-900 flex items-center justify-center px-4">
      <div className="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-md text-right">
        <h2 className="text-3xl font-bold mb-6 text-gray-800">הרשמה למערכת ZufaRav</h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          {["username", "password", "rank", "role", "id_number", "phone_number"].map((field) => (
            <div key={field}>
              <label className="block text-sm font-medium text-gray-600">
                {field === "username" && "שם משתמש"}
                {field === "password" && "סיסמה"}
                {field === "rank" && "דרגה"}
                {field === "role" && "תפקיד"}
                {field === "id_number" && "מספר אישי"}
                {field === "phone_number" && "מספר טלפון"}
              </label>
              <input
                type={field === "password" ? "password" : "text"}
                name={field}
                value={formData[field]}
                onChange={handleChange}
                className={`w-full border rounded-xl px-4 py-2 mt-1 text-right ${
                  errors[field] ? "border-red-500" : "border-gray-300"
                }`}
                required
              />
              {errors[field] && (
                <p className="text-xs text-red-600 mt-1">{errors[field]}</p>
              )}
            </div>
          ))}

          {serverError && (
            <div className="text-red-600 text-sm bg-red-100 px-3 py-2 rounded-xl text-center">
              {serverError}
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
