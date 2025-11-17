import React, { useEffect, useState } from "react";
import {
  createCuisine,
  deleteCuisine,
  getCuisines,
  createDietRestriction,
  deleteDietRestriction,
  getDietRestrictions,
} from "../../../api/api.js";

export default function ManageTags() {
  const [cuisines, setCuisines] = useState([]);
  const [newCuisine, setNewCuisine] = useState("");
  const [dietRestrictions, setDietRestrictions] = useState([]);
  const [newRestriction, setNewRestriction] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const loadTags = async () => {
    setLoading(true);
    setError("");
    try {
      const [cuisineList, restrictionList] = await Promise.all([
        getCuisines(),
        getDietRestrictions(),
      ]);
      setCuisines(cuisineList);
      setDietRestrictions(restrictionList);
    } catch (err) {
      console.error("Failed to load tags", err);
      setError("Failed to load cuisines/restrictions");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTags();
  }, []);

  const handleCreateCuisine = async (event) => {
    event.preventDefault();
    if (!newCuisine.trim()) {
      setError("Cuisine name cannot be empty");
      return;
    }

    try {
      await createCuisine({ cuisine: newCuisine.trim() });
      setNewCuisine("");
      await loadTags();
    } catch (err) {
      console.error("Failed to create cuisine", err);
      setError("Failed to create cuisine");
    }
  };

  const handleDeleteCuisine = async (id) => {
    if (!window.confirm("Delete this cuisine?")) return;
    try {
      await deleteCuisine(id);
      await loadTags();
    } catch (err) {
      console.error("Failed to delete cuisine", err);
      setError("Failed to delete cuisine");
    }
  };

  const handleCreateRestriction = async (event) => {
    event.preventDefault();
    if (!newRestriction.trim()) {
      setError("Restriction name cannot be empty");
      return;
    }
    try {
      await createDietRestriction({ restriction: newRestriction.trim() });
      setNewRestriction("");
      await loadTags();
    } catch (err) {
      console.error("Failed to create restriction", err);
      setError("Failed to create restriction");
    }
  };

  const handleDeleteRestriction = async (id) => {
    if (!window.confirm("Delete this restriction?")) return;
    try {
      await deleteDietRestriction(id);
      await loadTags();
    } catch (err) {
      console.error("Failed to delete restriction", err);
      setError("Failed to delete restriction");
    }
  };

  return (
    <section className="manage-tags">
      <h1>Manage Cuisines</h1>

      <form className="manage-tags__form" onSubmit={handleCreateCuisine}>
        <input
          type="text"
          placeholder="New cuisine name"
          value={newCuisine}
          onChange={(e) => setNewCuisine(e.target.value)}
        />
        <button type="submit">Add Cuisine</button>
      </form>

      {error && <p className="manage-tags__error">{error}</p>}

      <div className="manage-tags__list">
        {loading ? (
          <p>Loading cuisines...</p>
        ) : cuisines.length === 0 ? (
          <p>No cuisines created yet.</p>
        ) : (
          cuisines.map((cuisine) => (
            <div key={cuisine.id} className="manage-tags__item">
              <span>{cuisine.cuisine}</span>
              <button onClick={() => handleDeleteCuisine(cuisine.id)}>
                Delete
              </button>
            </div>
          ))
        )}
      </div>

      <h1 style={{ marginTop: "2.5rem" }}>Manage Dietary Restrictions</h1>

      <form className="manage-tags__form" onSubmit={handleCreateRestriction}>
        <input
          type="text"
          placeholder="New restriction name"
          value={newRestriction}
          onChange={(e) => setNewRestriction(e.target.value)}
        />
        <button type="submit">Add Restriction</button>
      </form>

      <div className="manage-tags__list">
        {loading ? (
          <p>Loading dietary restrictions...</p>
        ) : dietRestrictions.length === 0 ? (
          <p>No restrictions created yet.</p>
        ) : (
          dietRestrictions.map((restriction) => (
            <div key={restriction.id} className="manage-tags__item">
              <span>{restriction.restriction}</span>
              <button onClick={() => handleDeleteRestriction(restriction.id)}>
                Delete
              </button>
            </div>
          ))
        )}
      </div>
    </section>
  );
}
