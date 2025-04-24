import React, { useEffect, useState } from "react";
import axios from "../axiosInstance";

export default function UserManagement() {
  const [users, setUsers] = useState([]);
  const [filter, setFilter] = useState("");
  const [editingUser, setEditingUser] = useState(null);
  const [editData, setEditData] = useState({});

  const fetchUsers = async () => {
    try {
      const res = await axios.get("/admin/users");
      setUsers(res.data);
    } catch (err) {
      alert("שגיאה בטעינת המשתמשים");
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleDelete = async (id) => {
    if (!confirm("למחוק את המשתמש?")) return;
    try {
      await axios.delete(`/admin/delete_user/${id}`);
      fetchUsers();
    } catch {
      alert("שגיאה במחיקת המשתמש");
    }
  };

  const startEdit = (user) => {
    setEditingUser(user.id);
    setEditData({ ...user });
  };

  const cancelEdit = () => {
    setEditingUser(null);
    setEditData({});
  };

  const saveEdit = async () => {
    try {
      await axios.put(`/admin/update_user/${editingUser}`, editData);
      setEditingUser(null);
      fetchUsers();
    } catch {
      alert("שגיאה בשמירת השינויים");
    }
  };

  const filteredUsers = users.filter(u =>
    u.username.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div className="p-6 text-right">
      <h2 className="text-2xl font-bold mb-4">ניהול משתמשים</h2>

      <input
        type="text"
        placeholder="חפש לפי שם משתמש..."
        className="input mb-4"
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
      />

      <table className="min-w-full bg-white border border-gray-300 rounded-xl text-sm">
        <thead className="bg-gray-200">
          <tr>
            <th className="px-4 py-2">שם משתמש</th>
            <th className="px-4 py-2">שם מלא</th>
            <th className="px-4 py-2">תפקיד</th>
            <th className="px-4 py-2">דירוג</th>
            <th className="px-4 py-2">מס' אישי</th>
            <th className="px-4 py-2">טלפון</th>
            <th className="px-4 py-2">אימייל</th>
            <th className="px-4 py-2">פעולות</th>
          </tr>
        </thead>
        <tbody>
          {filteredUsers.map((u) => (
            <tr key={u.id} className="text-center">
              <td className="border-t px-2 py-1">{editingUser === u.id ? (
                <input value={editData.username} onChange={(e) => setEditData({ ...editData, username: e.target.value })} />
              ) : u.username}</td>
              <td className="border-t px-2 py-1">{editingUser === u.id ? (
                <input value={editData.full_name} onChange={(e) => setEditData({ ...editData, full_name: e.target.value })} />
              ) : u.full_name}</td>
              <td className="border-t px-2 py-1">{editingUser === u.id ? (
                <select value={editData.role} onChange={(e) => setEditData({ ...editData, role: e.target.value })}>
                  <option value="admin">admin</option>
                  <option value="hamal">hamal</option>
                  <option value="driver">driver</option>
                </select>
              ) : u.role}</td>
              <td className="border-t px-2 py-1">{editingUser === u.id ? (
                <input value={editData.rank} onChange={(e) => setEditData({ ...editData, rank: e.target.value })} />
              ) : u.rank}</td>
              <td className="border-t px-2 py-1">{editingUser === u.id ? (
                <input value={editData.id_number} onChange={(e) => setEditData({ ...editData, id_number: e.target.value })} />
              ) : u.id_number}</td>
              <td className="border-t px-2 py-1">{editingUser === u.id ? (
                <input value={editData.phone_number} onChange={(e) => setEditData({ ...editData, phone_number: e.target.value })} />
              ) : u.phone_number}</td>
              <td className="border-t px-2 py-1">{editingUser === u.id ? (
                <input value={editData.email} onChange={(e) => setEditData({ ...editData, email: e.target.value })} />
              ) : u.email}</td>
              <td className="border-t px-2 py-1 space-x-1 space-y-1">
                {editingUser === u.id ? (
                  <>
                    <button onClick={saveEdit} className="bg-green-500 text-white px-2 rounded">שמור</button>
                    <button onClick={cancelEdit} className="bg-gray-400 text-white px-2 rounded">בטל</button>
                  </>
                ) : (
                  <>
                    <button onClick={() => startEdit(u)} className="bg-yellow-500 text-white px-2 rounded">ערוך</button>
                    <button onClick={() => handleDelete(u.id)} className="bg-red-600 text-white px-2 rounded">מחק</button>
                  </>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}