// src/components/FoodList.js
import React, { useState, useEffect } from "react";
import Card from "./card";
import { getFoods } from "../api/api";
import RestrictionsPage from "../routes/Food/RestrictionsPage.jsx";
import { useNavigate } from "react-router-dom";



export default function FoodList({ data }) {
  // If nothing has loaded yet
  const navigate = useNavigate();
  if (!data || Object.keys(data).length === 0) {
    return <p>Loading...</p>;
  }

  const onNameClick = (restrictionName) => {
  console.log("Food name clicked:", restrictionName);
  navigate(`/restrictions/${restrictionName}`);
};


  return (
    <div className="food-list">
      {/* Loop through each restriction group */}
      {Object.entries(data).map(([restrictionName, foods]) => (
        <div key={restrictionName} className="food-group">
          <h2 onClick={() => onNameClick(restrictionName)}>{restrictionName}</h2>

          <div className="food-scroll-container">
            {foods.map((food) => (
              <Card
                key={food.id}
                food={{
                  ...food,
                  dietaryRestriction: food.dietary_restrictions?.map(r => r.restriction),
                }}
              />
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
export { FoodList };