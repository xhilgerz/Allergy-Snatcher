import React from "react";
import FoodCard from "./card.jsx";
export default function PendingFoods({ foods, onApprove }) {
  console.log("PendingFoods props:", { foods, onApprove });

   return (
    <div className="PendingFoodsContainer">
      {foods.map((food) => (
        <FoodCard
        key={food.id}
        food={{
          ...food,
          dietaryRestriction: food.dietary_restrictions?.map((r) => r.restriction),
        }}
          showApproveButton={true}
          onApprove={onApprove}
        />
      ))}
    </div>
  );
}
