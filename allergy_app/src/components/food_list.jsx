// src/components/FoodList.js
import React, { useState, useEffect } from "react";
import Card from "./card";
import { getFoods } from "../api/api";


export default function FoodList({ data }) {
  // If nothing has loaded yet
  if (!data || Object.keys(data).length === 0) {
    return <p>Loading...</p>;
  }

  return (
    <div className="food-list">
      {/* Loop through each restriction group */}
      {Object.entries(data).map(([restrictionName, foods]) => (
        <div key={restrictionName} className="food-group">
          <h2>{restrictionName}</h2>

          <div className="food-scroll-container">
            {foods.map((food) => (
              <Card
                key={food.id}
                picture={food.picture}
                name={food.name}
                cuisine={food.cuisine?.cuisine}
                dietaryRestriction={food.dietary_restrictions?.map(r => r.restriction)}
              />
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
export { FoodList };