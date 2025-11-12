import React, { useState, useEffect } from "react";
import Select from "react-select";
import { useParams, useNavigate } from "react-router-dom";
import { updateFood, getFoods, deleteFood } from "../api/api.js";

export default function EditFoodForm() {
  const { foodId } = useParams();
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    name: "",
    brand: "",
    ingredients: "",
    nutritional_info: "",
    total_fats: "",
    saturated_fats: "",
    trans_fats: "",
    cholesterol: "",
    sodium: "",
    total_carbohydrates: "",
    dietary_fiber: "",
    total_sugars: "",
    added_sugars: "",
    calories: "",
    protein: "",
    carbs: "",
    cuisine: "",
    restrictions: [],
    publication_status: "private",
  });

  const allowedRestrictions = [
    "Dairy", "Nuts", "Gluten", "Kosher", "Vegan", "Red meat",
    "Pork", "Keto", "Shellfish", "Eggs", "Soy", "Lactose",
  ];

  // ✅ Load existing food data when component mounts
  useEffect(() => {
    getFoods().then((foods) => {
      const food = foods.find((f) => f.id === parseInt(foodId));
      if (food) {
        setFormData({
          name: food.name || "",
          brand: food.brand || "",
          ingredients: food.ingredients
            ? food.ingredients.map((i) => i.ingredient_name).join(", ")
            : "",
          nutritional_info: food.nutritional_info || "",
          total_fats: food.total_fats || "",
          saturated_fats: food.sat_fats || "",
          trans_fats: food.trans_fats || "",
          cholesterol: food.cholesterol || "",
          sodium: food.sodium || "",
          total_carbohydrates: food.total_carbohydrates || "",
          dietary_fiber: food.dietary_fiber || "",
          total_sugars: food.sugars || "",
          added_sugars: food.added_sugars || "",
          calories: food.cal || "",
          protein: food.protein || "",
          carbs: food.carbs || "",
          cuisine: food.cuisine?.cuisine || "",
          restrictions: food.dietary_restrictions?.map((r) => r.restriction) || [],
          publication_status: food.publication_status || "private",
        });
      }
    });
  }, [foodId]);

  // ✅ Handle input changes
  const handleChange = (e) => {
    const { name, value, type } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]:
        type === "number" ? (value === "" ? "" : parseFloat(value)) : value,
    }));
  };

  // ✅ React-Select handler
  const handleRestrictionsChange = (selectedOptions) => {
    const values = selectedOptions ? selectedOptions.map((opt) => opt.value) : [];
    setFormData((prev) => ({ ...prev, restrictions: values }));
  };

  // ✅ Delete Food handler
  const handleDelete = async () => {
    if (window.confirm("Are you sure you want to delete this food item?")) {
      try {
        await deleteFood(foodId);
        alert("✅ Food deleted successfully!");
        navigate("/edit-food");
      } catch (err) {
        console.error("Backend delete failed:", err);
        alert("❌ Failed to delete food — check console for details.");
      }
    }
  };

  // ✅ Submit updated data
  const handleSubmit = async (e) => {
    e.preventDefault();

    const formattedData = {
      name: formData.name,
      brand: formData.brand,
      publication_status: formData.publication_status,
      carbs: formData.carbs === "" ? null : parseFloat(formData.carbs),
      protein: formData.protein === "" ? null : parseFloat(formData.protein),
      total_fats:
        formData.total_fats === "" ? null : parseFloat(formData.total_fats),
      sat_fats:
        formData.saturated_fats === "" ? null : parseFloat(formData.saturated_fats),
      trans_fats:
        formData.trans_fats === "" ? null : parseFloat(formData.trans_fats),
      cholesterol:
        formData.cholesterol === "" ? null : parseFloat(formData.cholesterol),
      sodium: formData.sodium === "" ? null : parseFloat(formData.sodium),
      dietary_fiber:
        formData.dietary_fiber === "" ? null : parseFloat(formData.dietary_fiber),
      sugars:
        formData.total_sugars === "" ? null : parseFloat(formData.total_sugars),
      cal: formData.calories === "" ? null : parseFloat(formData.calories),

      category_id: 1,
      cuisine_id: 1,

      ingredients: formData.ingredients
        ? formData.ingredients
            .split(",")
            .map((i) => ({ ingredient_name: i.trim() }))
        : [],

      dietary_restriction_ids: formData.restrictions.map((_, idx) => idx + 1),
    };

    console.log("Submitting edited food:", formattedData);

    try {
      const res = await updateFood(foodId, formattedData, true);
      console.log("Backend update success:", res);
      alert("✅ Food updated successfully!");
      navigate("/edit-food");
    } catch (err) {
      console.error("Backend update failed:", err);
      alert("❌ Failed to update food — check console for details.");
    }
  };

  const restrictionOptions = allowedRestrictions.map((r) => ({
    value: r,
    label: r,
  }));

  return (
    <form onSubmit={handleSubmit} className="edit-food-form">
      <h1>Edit Food #{foodId}</h1>

      <label>
        Name:
        <input name="name" value={formData.name} onChange={handleChange} />
      </label>

      <label>
        Brand:
        <input name="brand" value={formData.brand} onChange={handleChange} />
      </label>

      <label>
        Ingredients (comma-separated):
        <textarea
          name="ingredients"
          value={formData.ingredients}
          onChange={handleChange}
        />
      </label>

      <label>
        Nutritional Info:
        <textarea
          name="nutritional_info"
          value={formData.nutritional_info}
          onChange={handleChange}
        />
      </label>

      {/* numeric inputs */}
      {[
        ["total_fats", "Total Fats (g)"],
        ["saturated_fats", "Saturated Fats (g)"],
        ["trans_fats", "Trans Fats (g)"],
        ["cholesterol", "Cholesterol (mg)"],
        ["sodium", "Sodium (mg)"],
        ["total_carbohydrates", "Total Carbohydrates (g)"],
        ["dietary_fiber", "Dietary Fiber (g)"],
        ["total_sugars", "Total Sugars (g)"],
        ["added_sugars", "Added Sugars (g)"],
        ["calories", "Calories"],
        ["protein", "Protein (g)"],
        ["carbs", "Carbs (g)"],
      ].map(([name, label]) => (
        <label key={name}>
          {label}
          <input
            type="number"
            name={name}
            value={formData[name]}
            onChange={handleChange}
          />
        </label>
      ))}

      <label>
        Cuisine:
        <input name="cuisine" value={formData.cuisine} onChange={handleChange} />
      </label>

      <label>
        Publication Status:
        <select
          name="publication_status"
          value={formData.publication_status}
          onChange={handleChange}
        >
          <option value="private">Private</option>
          <option value="public">Public</option>
          <option value="unlisting">Unlisting</option>
        </select>
      </label>

      <label>
        Dietary Restrictions:
        <Select
          isMulti
          name="restrictions"
          options={restrictionOptions}
          onChange={handleRestrictionsChange}
          value={restrictionOptions.filter((opt) =>
            formData.restrictions.includes(opt.value)
          )}
          placeholder="Select dietary restrictions..."
        />
      </label>

      <div className="button-container">
        <button type="submit" className="save-btn">
          Save Changes
        </button>
        <button
          type="button"
          onClick={handleDelete}
          className="delete-btn"
          style={{ marginLeft: "1rem", backgroundColor: "red", color: "white" }}
        >
          Delete
        </button>
      </div>
    </form>
  );
}

