// src/components/FoodList.js
import React, { useState, useEffect } from "react";
import Card from "./card";
import { getDietRestrictions } from "../api/api";
import { useNavigate } from "react-router-dom";

export default function FoodList({ data }) {
  const navigate = useNavigate();
  const [allowedRestrictions, setAllowedRestrictions] = useState([]);

  useEffect(() => {
    (async () => {
      try {
        const list = await getDietRestrictions();
        setAllowedRestrictions(
          list.map((r) => ({ value: r.id, label: r.restriction }))
        );
      } catch (err) {
        console.error("Failed to load restrictions", err);
      }
    })();
  }, []);

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
      {Object.entries(data)
        .filter(([restrictionName]) =>
          allowedRestrictions.some((r) => r.label === restrictionName)
        )
        .map(([restrictionName, foods]) => {
          const visibleFoods = foods.filter(
            (food) => food.publication_status === "public"
          );

          if (visibleFoods.length === 0) return null;

          return (
            <div key={restrictionName} className="food-group">
              <h2 onClick={() => onNameClick(restrictionName)}>
                {restrictionName}
              </h2>
              <div className="food-scroll-container">
                {visibleFoods.map((food) => (
                  <Card
                    key={food.id}
                    food={{
                      ...food,
                      dietaryRestriction: food.dietary_restrictions?.map(
                        (r) => r.restriction
                      ),
                    }}
                  />
                ))}
              </div>
            </div>
          );
        })}
    </div>
  );
}

export { FoodList };
