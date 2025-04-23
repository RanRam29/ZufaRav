import React, { useEffect, useState } from 'react';
import axios from '../axiosInstance';

export default function ArchivedEvents() {
  const [archived, setArchived] = useState([]);

  useEffect(() => {
    fetchArchived();
  }, []);

  const fetchArchived = async () => {
    try {
      const res = await axios.get('/events/archive');
      setArchived(res.data);
    } catch (err) {
      alert('שגיאה בטעינת הארכיון');
      console.error(err);
    }
  };

  return (
    <div className="p-6 text-right">
      <h2 className="text-2xl font-bold mb-4">📁 ארכיון אירועים שנמחקו</h2>
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white border rounded-xl">
          <thead className="bg-gray-200">
            <tr>
              <th className="px-4 py-2">כותרת</th>
              <th className="px-4 py-2">כתובת</th>
              <th className="px-4 py-2">מדווח</th>
              <th className="px-4 py-2">תאריך יצירה</th>
              <th className="px-4 py-2">מי אישר</th>
              <th className="px-4 py-2">מתי אישר</th>
              <th className="px-4 py-2">זמן הגעה</th>
              <th className="px-4 py-2">מי מחק</th>
              <th className="px-4 py-2">מתי נמחק</th>
            </tr>
          </thead>
          <tbody>
            {archived.map((event, i) => (
              <tr key={i} className="text-center border-t">
                <td className="px-2 py-1">{event.title}</td>
                <td className="px-2 py-1">{event.location}</td>
                <td className="px-2 py-1">{event.reporter}</td>
                <td className="px-2 py-1">{new Date(event.created_at).toLocaleString('he-IL')}</td>
                <td className="px-2 py-1">{event.confirmed_by || "—"}</td>
                <td className="px-2 py-1">{event.confirmed_at ? new Date(event.confirmed_at).toLocaleString('he-IL') : "—"}</td>
                <td className="px-2 py-1">{event.arrival_time ? new Date(event.arrival_time).toLocaleString('he-IL') : "—"}</td>
                <td className="px-2 py-1 font-bold text-red-600">{event.deleted_by}</td>
                <td className="px-2 py-1">{new Date(event.deleted_at).toLocaleString('he-IL')}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}