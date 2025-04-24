export default function LogoutPopup({ show }) {
  if (!show) return null;
  return (
    <div className="fixed top-4 left-1/2 transform -translate-x-1/2 bg-white border px-6 py-2 rounded-xl z-50 shadow-lg animate-fade">
      ✅ נותקת מהמערכת
    </div>
  );
}