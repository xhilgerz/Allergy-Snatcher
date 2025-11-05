// src/components/FoodList.js
import React, { useState, useEffect } from "react";
import Card from "./card";
import { getFoods } from "../api/api";


function FoodList() {
  const [foods, setFoods] = useState([]);
  const API_BASE = process.env.REACT_APP_API_BASE_URL || "http://localhost:5001";

  useEffect(() => {

    getFoods(10, 0, true).then(setFoods);
    
  
  }, []);

  return (
    <div>
      <h2>Foods</h2>
      <div className="food-grid">
        {Array.isArray(foods) && foods.length > 0 ? (
          foods.map((food) => (
            <Card
              key={food.id}
              picture={food.picture}
              name={food.name}
              //cuisine={food.cuisine}
              dietaryRestriction={food.dietaryRestriction}
            />
          ))
        ) : (
          <p>No foods found.</p>
        )}
      </div>
    </div>
  );
}

export default FoodList;
