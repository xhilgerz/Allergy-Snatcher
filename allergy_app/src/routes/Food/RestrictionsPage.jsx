import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getFoods } from "../../api/api"; // or wherever your getFoods() lives

export default function RestrictionsPage() {
  
  const { restrictionName } = useParams();       // ex: "Vegan"
  const [foods, setFoods] = useState([]);        // holds foods from the API

  useEffect(() => {
    // Call getFoods and then filter by restriction
    getFoods().then((data) => {
      // assuming each food has a dietary_restrictions array
      const filtered = data.filter((food) =>
        food.dietary_restrictions?.some(
          (r) => r.restriction === restrictionName
        )
      );
      setFoods(filtered);
    });
  }, [restrictionName]);

  return (
  <div className="FoodContainer">
    <h1>{restrictionName} Foods</h1>
    <p>Showing results for: {restrictionName}</p>

    {foods.length === 0 ? (
      <p>No foods found for this restriction.</p>
    ) : (
      // ✅ horizontal scroll container
      <div className="food-scroll-container">
        {foods.map((food) => (
          <div key={food.id} className="Card">
            <h4>{food.name}</h4>
            <h5>{food.cuisine?.cuisine}</h5>
            <h6>
              {food.dietary_restrictions
                ?.map((r) => r.restriction)
                .join(", ")}
            </h6>
          </div>
        ))}
      </div>
    )}
  </div>
);
}
