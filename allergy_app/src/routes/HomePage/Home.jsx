// This page will include the page with each dietary restriction and their perspective food cards
// src/pages/Home.js
import React from "react";
import FoodList from "../../components/food_list.jsx"; // fixed relative path

export default function Home() {
  return (
    <div className="home-container">
      <h1>Welcome to the Allergy Snatcher</h1>
      <p>Welcome to our cool website</p>

      {/* FoodList component goes here */}
      <FoodList />

    </div>
  );
}