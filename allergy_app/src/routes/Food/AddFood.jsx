// Page where users can insert a new food to the database
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import FoodForm from "../../components/FoodForm.jsx";
import { addFood } from "../../api/api.js";

export default function AddFood() {
  const navigate = useNavigate();
  const [errors, setErrors] = useState({});

  const handleCreate = async (payload) => {
    setErrors({}); // Clear previous errors
    try {
      await addFood(payload);
      alert("Food added successfully!");
      navigate("/");
    } catch (error) {
      if (error.response && (error.response.status === 422 || error.response.status === 411)) {
        const errorDetails = error.response.data.details;
        const newErrors = {};
        errorDetails.forEach(detail => {
          const fieldName = detail.loc[0];
          if (fieldName === 'sat_fats') {
            newErrors['saturated_fats'] = detail.msg;
          } else if (fieldName === 'cal') {
            newErrors['calories'] = detail.msg;
          } else {
            newErrors[fieldName] = detail.msg;
          }
        });
        setErrors(newErrors);
      } else {
        // Handle other types of errors (e.g., network error, server 500)
        // The generic error is already emitted by api.js, so you might not need to do anything extra
        console.error("Failed to add food:", error);
      }
    }
  };

  return (
    <div className="add-food-container">
      <h1>This is where you can add a new food item</h1>
      <p>Fill out the form below to add a new food to the database.</p>
      <FoodForm submitLabel="Add Food" onSubmit={handleCreate} errors={errors} />
    </div>
  );
}
