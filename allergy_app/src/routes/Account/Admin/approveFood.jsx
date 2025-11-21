//This page allows the admin to approve foods that users have submitted
import { useEffect, useState } from "react"; // ✅ include useState
import PendingFoods from "../../../components/pendingFoods.jsx";
import { getFoods } from "../../../api/api.js"; // fixed relative path


export default function ApproveFood() {
  const [foods, setFoods] = useState([]);

  const fetchFoods = async () => {
    const data = await getFoods();
    setFoods(data);
  };

  useEffect(() => {
    fetchFoods();
  }, []);

  return (
    <div className="approve-food-container">
      <h1>Approve Pending Foods</h1>
      <PendingFoods foods={foods} onChange={fetchFoods} />
    </div>
  );
}
