//This page allows the admin to approve foods that users have submitted
import { useEffect, useState } from "react"; // ✅ include useState
import PendingFoods from "../../../components/pendingFoods.jsx";
import { getFoods } from "../../../api/api.js"; // fixed relative path
import { useAuth } from "../../../context/AuthContext.jsx";


export default function ApproveFood() {
  const [foods, setFoods] = useState([]);
  const { user, loading } = useAuth();

  const fetchFoods = async () => {
    const data = await getFoods();
    setFoods(data);
  };

  useEffect(() => {
    if (user?.role === "admin") {
      fetchFoods();
    }
  }, [user]);

  if (loading) return <p>Checking login…</p>;
  if (!user || user.role !== "admin")
    return <p>Admins only. Please log in with an admin account.</p>;

  return (
    <div className="approve-food-container">
      <h1>Approve Pending Foods</h1>
      <PendingFoods foods={foods} onChange={fetchFoods} />
    </div>
  );
}
