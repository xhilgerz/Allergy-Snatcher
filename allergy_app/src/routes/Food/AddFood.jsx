// Page where users can insert a new food to the database
import { useNavigate } from "react-router-dom";
import FoodForm from "../../components/FoodForm.jsx";
import { addFood } from "../../api/api.js";

export default function AddFood() {
  const navigate = useNavigate();

  const handleCreate = async (payload) => {
    try {
      await addFood(payload);
      alert("Food added successfully!");
      navigate("/");
    } catch (error) {
      console.error("Failed to add food:", error);
      // Error toast is emitted in api.js; just stop navigation on failure.
    }
  };

  return (
    <div className="add-food-container">
      <h1>This is where you can add a new food item</h1>
      <p>Fill out the form below to add a new food to the database.</p>
      <FoodForm submitLabel="Add Food" onSubmit={handleCreate} />
    </div>
  );
}
