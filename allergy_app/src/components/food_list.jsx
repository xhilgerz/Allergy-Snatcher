// src/components/FoodList.js
import React, { useState, useEffect } from "react";
import Card from "./card.jsx";

function FoodList() {
  const [foods, setFoods] = useState([]);
  // Use CRA env var with fallback to local dev backend port used by docker-compose.dev.yml
  const API_BASE = process.env.REACT_APP_API_BASE_URL || "http://localhost:5001";

  //ask to get a api get call that returns a list of foods from the backend
  // ask to get a list of foods by their dietary restriction id
  useEffect(() => {
    const url = `${API_BASE}/api/foods/1`;
    // eslint-disable-next-line no-console
    console.log("Fetching foods from:", url);

    fetch(url)
      .then((response) => {
        if (!response.ok) throw new Error("Network response was not ok");
        return response.json();
      })
      .then((data) => setFoods([data]))
      .catch((error) => console.error("Error fetching data:", error));
  }, [API_BASE]);

  return (
    <div>
      <h2>Gluten Free</h2>
      <div className="food-grid">
    {foods.map((food) => (
      <Card
        picture={food.picture}
        key={food.id}
        name={food.name}
        cuisine={food.cuisine}
        dietaryRestriction={food.dietaryRestriction}
    />
  ))}
</div>
    </div>
  );
}

export default FoodList;

