import React, { useState } from "react";
import Select from "react-select";
import { addFood } from "../api/api.js";

export default function AddFoodForm() {
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
    publication_status: "private", // ✅ backend expects "private" not false
  });

  const allowedRestrictions = [
    "Dairy", "Nuts", "Gluten", "Kosher", "Vegan", "Red meat",
    "Pork", "Keto", "Shellfish", "Eggs", "Soy", "Lactose",
  ];

  // ✅ handles all input updates
  const handleChange = (e) => {
    const { name, value, type } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]:
        type === "number"
          ? value === "" ? "" : parseFloat(value)
          : value,
    }));
  };

  // ✅ react-select multi handler
  const handleRestrictionsChange = (selectedOptions) => {
    const values = selectedOptions ? selectedOptions.map(opt => opt.value) : [];
    setFormData((prev) => ({ ...prev, restrictions: values }));
  };

  // ✅ builds backend-safe payload
  const handleSubmit = async (e) => {
    e.preventDefault();

    const formattedData = {
      name: formData.name,
      brand: formData.brand,
      publication_status: formData.publication_status,
      carbs: formData.carbs === "" ? null : parseFloat(formData.carbs),
      protein: formData.protein === "" ? null : parseFloat(formData.protein),
      total_fats: formData.total_fats === "" ? null : parseFloat(formData.total_fats),
      sat_fats: formData.saturated_fats === "" ? null : parseFloat(formData.saturated_fats),
      trans_fats: formData.trans_fats === "" ? null : parseFloat(formData.trans_fats),
      cholesterol: formData.cholesterol === "" ? null : parseFloat(formData.cholesterol),
      sodium: formData.sodium === "" ? null : parseFloat(formData.sodium),
      dietary_fiber: formData.dietary_fiber === "" ? null : parseFloat(formData.dietary_fiber),
      sugars: formData.total_sugars === "" ? null : parseFloat(formData.total_sugars),
      cal: formData.calories === "" ? null : parseFloat(formData.calories),

      // required by backend
      category_id: 1, // temporary default
      cuisine_id: 1,

      // convert string → list of ingredient objects
      ingredients: formData.ingredients
        ? formData.ingredients
            .split(",")
            .map((i) => ({ ingredient_name: i.trim() }))
        : [],

      // placeholder IDs until you map real restriction IDs
      dietary_restriction_ids: formData.restrictions.map((_, idx) => idx + 1),
    };

    console.log("Submitting formatted data:", formattedData);

    try {
      const res = await addFood(formattedData);
      console.log("Backend success:", res);
      alert("Food added successfully!");
    } catch (err) {
      console.error("Backend failed:", err);
      alert("Failed to add food — check console for details.");
    }
  };

  const restrictionOptions = allowedRestrictions.map(r => ({
    value: r,
    label: r,
  }));

  return (
    <form onSubmit={handleSubmit} className="add-food-form">
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
        Dietary Restrictions:
        <Select
          isMulti
          name="restrictions"
          options={restrictionOptions}
          onChange={handleRestrictionsChange}
          value={restrictionOptions.filter(opt =>
            formData.restrictions.includes(opt.value)
          )}
          placeholder="Select dietary restrictions..."
        />
      </label>

      <button type="submit">Add Food</button>
    </form>
  );
}
