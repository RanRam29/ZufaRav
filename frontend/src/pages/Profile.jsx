import { useEffect, useState } from "react";
import axios from "../axiosInstance";
import { useNavigate, useLocation } from "react-router-dom";

export default function Profile() {
  const [user, setUser] = useState(null);
  const [editMode, setEditMode] = useState(false);
  const [formData, setFormData] = useState({});
  const navigate = useNavigate();
  const location = useLocation();
  const token = localStorage.getItem("token");
  const role = localStorage.getItem("role");

  const queryParams = new URLSearchParams(location.search);
  const queryUsername = queryParams.get("username");

  useEffect(() => {
    if (!token) navigate("/login");
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const res = queryUsername
        ? await axios.get(`/admin/users/${queryUsername}`)
        : await axios.get("/admin/me");
      setUser(res.data);
      setFormData(res.data);
    } catch (err) {
      console.error("שגיאה בטעינת פרופיל", err);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleUpdate = async () => {
    try {
      await axios.patch("/admin/update-user", formData);
      alert("✅ הפרופיל עודכן בהצלחה");
      setUser(formData);
      setEditMode(false);
    } catch (err) {
      alert("❌ שגיאה בעדכון המשתמש");
    }
  };

  if (!user) return <p className="text-center mt-10">טוען פרופיל...</p>;

  return (
    <div className="max-w-xl mx-auto p-6 bg-white shadow-xl rounded-xl mt-10 text-right">
      <h2 className="text-2xl font-bold mb-4">פרופיל משתמש</h2>

      <div className="space-y-4">
        <Field label="שם משתמש" name="username" value={formData.username} onChange={handleChange} disabled />
        <Field label="שם מלא" name="full_name" value={formData.full_name} onChange={handleChange} editable={editMode} />
        <Field label="דרגה" name="rank" value={formData.rank} onChange={handleChange} editable={editMode} />
        <Field label="תפקיד" name="role" value={formData.role} onChange={handleChange} editable={editMode} />
        <Field label="מספר אישי" name="id_number" value={formData.id_number} onChange={handleChange} editable={editMode} />
        <Field label="מספר טלפון" name="phone_number" value={formData.phone_number} onChange={handleChange} editable={editMode} />
        <Field label="אימייל" name="email" value={formData.email} onChange={handleChange} editable={editMode} />
      </div>

      {role === "admin" && (
        <div className="mt-6 text-center space-x-2 rtl:space-x-reverse">
          {editMode ? (
            <>
              <button onClick={handleUpdate} className="bg-green-600 text-white px-4 py-2 rounded-xl">שמור</button>
              <button onClick={() => setEditMode(false)} className="bg-gray-400 text-white px-4 py-2 rounded-xl">בטל</button>
            </>
          ) : (
            <button onClick={() => setEditMode(true)} className="bg-blue-600 text-white px-4 py-2 rounded-xl">ערוך</button>
          )}
        </div>
      )}
    </div>
  );
}

function Field({ label, name, value, onChange, editable = true, disabled = false }) {
  return (
    <div>
      <label htmlFor={name} className="block text-sm font-medium text-gray-700">{label}</label>
      <input
        id={name}
        name={name}
        type="text"
        value={value || ""}
        onChange={onChange}
        disabled={!editable || disabled}
        className="w-full border rounded-xl px-4 py-2 mt-1 bg-gray-50 text-right"
      />
    </div>
  );
}
