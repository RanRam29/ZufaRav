export default function FilterBar({ setFilterConfirmed }) {
  return (
    <div className="flex gap-2 mb-4 justify-end">
      <button onClick={() => setFilterConfirmed("all")} className="bg-gray-300 px-3 py-1 rounded">הצג הכל</button>
      <button onClick={() => setFilterConfirmed("confirmed")} className="bg-green-300 px-3 py-1 rounded">מאושרים</button>
      <button onClick={() => setFilterConfirmed("pending")} className="bg-yellow-300 px-3 py-1 rounded">בהמתנה</button>
    </div>
  );
}