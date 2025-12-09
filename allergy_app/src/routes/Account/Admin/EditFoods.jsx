//This page shows the specific foods under a restriction including gluten free, non-dairy, etc. Can be filtered further using filter features. 
import React, { useEffect, useState } from "react";
import FoodCard from "../../../components/card.jsx";  // adjust path if needed
import { getFoods } from "../../../api/api.js";

export default function EditFood() {
  const [foods, setFoods] = useState([]);

  const fetchFoods = async () => {
    const data = await getFoods();
    setFoods(data);
  };

  // Fetch foods from backend
  useEffect(() => {
    fetchFoods();
  }, []);

  // Filter only published foods
  const publishedFoods = foods.filter(
    (food) => food.publication_status === "public"
  );

  const handleApprove = (foodId) => {
    console.log(`Edit button clicked for food ID ${foodId}`);
    // you can later call updateFood() here to change status or open a modal
  };

  return (
    <div className="edit-food-page">
      <div className="edit-food-container">
        <h1>Edit Foods</h1>
        
      </div>

      <div className="PendingFoodsContainer">
        {publishedFoods.length > 0 ? (
          publishedFoods.map((food) => (
            <FoodCard
              key={food.id}
              food={{
                ...food,
                dietaryRestriction: food.dietary_restrictions?.map(
                  (r) => r.restriction
                ),
              }}
              showEditButtons={true}
              onApprove={() => handleApprove(food.id)}
              onDelete={fetchFoods}
            />
          ))
        ) : (
          <p>No published foods to edit.</p>
        )}
      </div>
    </div>
  );
}
