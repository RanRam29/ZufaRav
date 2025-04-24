import { useEffect, useState } from "react";
import axios from "../axiosInstance";
import { useNavigate } from "react-router-dom";

export default function UsersDashboard() {
  const [users, setUsers] = useState([]);
  const [log, setLog] = useState([]);
  const [search, setSearch] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    fetchUsers();
    fetchAuditLog();
  }, []);

  const fetchUsers = async () => {
    try {
      const res = await axios.get("/admin/users");
      setUsers(res.data);
    } catch (err) {
      alert("שגיאה בטעינת המשתמשים");
    }
  };

  const fetchAuditLog = async () => {
    try {
      const res = await axios.get("/admin/audit-log");
      setLog(res.data);
    } catch (err) {
      console.error("שגיאה ביומן פעולות", err);
    }
  };

  const handleDelete = async (username) => {
    if (!confirm(`למחוק את המשתמש ${username}?`)) return;
    try {
      await axios.delete(`/admin/delete-user/${username}`);
      setUsers((prev) => prev.filter((u) => u.username !== username));
      fetchAuditLog();
    } catch (err) {
      alert("❌ שגיאה במחיקת המשתמש");
    }
  };

  const filtered = users.filter((u) =>
    u.username.toLowerCase().includes(search.toLowerCase()) ||
    u.full_name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="p-6 text-right max-w-7xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">ניהול משתמשים</h2>

      <input
        type="text"
        placeholder="חיפוש לפי שם משתמש או שם מלא"
        className="border px-4 py-2 rounded-xl mb-4 w-full md:w-1/3"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />

      <div className="overflow-x-auto">
        <table className="min-w-full bg-white border rounded-xl">
          <thead className="bg-gray-200">
            <tr>
              <th className="px-3 py-2">שם משתמש</th>
              <th className="px-3 py-2">שם מלא</th>
              <th className="px-3 py-2">תפקיד</th>
              <th className="px-3 py-2">דרגה</th>
              <th className="px-3 py-2">טלפון</th>
              <th className="px-3 py-2">אימייל</th>
              <th className="px-3 py-2">פעולות</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((u, i) => (
              <tr key={i} className="text-center border-t">
                <td className="px-2 py-1">{u.username}</td>
                <td className="px-2 py-1">{u.full_name}</td>
                <td className="px-2 py-1">{u.role}</td>
                <td className="px-2 py-1">{u.rank}</td>
                <td className="px-2 py-1">{u.phone_number}</td>
                <td className="px-2 py-1">{u.email}</td>
                <td className="px-2 py-1 space-x-1 rtl:space-x-reverse">
                  <button
                    onClick={() => navigate(`/profile?username=${u.username}`)}
                    className="bg-blue-600 text-white px-2 rounded"
                  >
                    ערוך
                  </button>
                  <button
                    onClick={() => handleDelete(u.username)}
                    className="bg-red-500 text-white px-2 rounded"
                  >
                    מחק
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <h3 className="text-xl font-bold mt-10 mb-2">יומן פעולות אחרונות</h3>
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white border rounded-xl">
          <thead className="bg-gray-100">
            <tr>
              <th className="px-3 py-2">משתמש</th>
              <th className="px-3 py-2">פעולה</th>
              <th className="px-3 py-2">פירוט</th>
              <th className="px-3 py-2">תאריך</th>
            </tr>
          </thead>
          <tbody>
            {log.map((item, i) => (
              <tr key={i} className="text-center border-t">
                <td className="px-2 py-1">{item.username}</td>
                <td className="px-2 py-1">{item.action}</td>
                <td className="px-2 py-1">{item.details}</td>
                <td className="px-2 py-1">{new Date(item.timestamp).toLocaleString("he-IL")}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
