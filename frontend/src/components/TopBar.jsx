export default function TopBar({ username, role, navigate, handleLogout }) {
  return (
    <div className="flex justify-between items-center mb-4">
      <div>
        <h2 className="text-2xl font-bold">דשבורד אירועים</h2>
        <p>משתמש: <b>{username}</b> | תפקיד: <b>{role}</b></p>
      </div>
      <div className="flex gap-2">
        {(role === "admin" || role === "hamal") && (
          <button onClick={() => navigate("/create-event")} className="bg-green-600 text-white px-4 py-2 rounded-xl">צור אירוע חדש</button>
        )}
        <button onClick={() => navigate("/movement")} className="bg-blue-600 text-white px-4 py-2 rounded-xl">דשבורד תנועה</button>
        <button onClick={handleLogout} className="bg-gray-500 text-white px-4 py-2 rounded-xl">התנתק</button>
        <button onClick={() => navigate("/reports")} className="bg-gray-700 text-white px-4 py-2 rounded-xl">ארכיון</button>
      </div>
    </div>
  );
}
