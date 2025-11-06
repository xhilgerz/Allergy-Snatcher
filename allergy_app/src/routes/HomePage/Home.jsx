// This page will include the page with each dietary restriction and their perspective food cards
// src/pages/Home.js
import React, { useState,useEffect } from "react";
import FoodList from "../../components/food_list.jsx"; // fixed relative path
import { getFoods } from "../../api/api.js"; // fixed relative path

export default function Home() {

  const [foods, setFoods] = useState([]);

  useEffect(() => {
    getFoods().then((data) => {
  const bins = {};



      data.forEach((food) => {
        food.dietary_restrictions.forEach((restriction) => {
        const restrictionName = restriction.restriction; // extract the string name
        if (!bins[restrictionName]) bins[restrictionName] = [];
        bins[restrictionName].push(food);
      });

      });
      setFoods(bins);
    });
  }, []);

  return (
    <div className="home-container">
      <h1>Welcome to the Allergy Snatcher</h1>
      <p>Welcome to our cool website</p>

      {/* FoodList component goes here */}

      <FoodList data={foods}/>
      

    </div>
  );
}