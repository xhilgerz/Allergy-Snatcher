import React, { useState } from "react";

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
    restriction: "",
    approved: false,
  });

  const allowedRestrictions = [
  "Dairy",
  "Nuts",
  "Gluten",
  "Kosher",
  "Vegan",
  "Red meat",
  "Pork",
  "Keto",
  "Shellfish",
  "Eggs",
  "Soy",
  "Lactose",
];

  // single handler for ALL inputs
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value, // update the matching key
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Submitted food:", formData);
    //addFood(formData)
  };

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
        Ingredients:
        <textarea
          name="ingredients"
          value={formData.ingredients}
          onChange={handleChange}
        />
      </label>

      <label>
        Nutritional Information:
        <textarea
          name="nutritional_info"
          value={formData.nutritional_info}
          onChange={handleChange}
        />
      </label>

      <label>
        Total Fats (g):
        <input
          type="number"
          name="total_fats"
          value={formData.total_fats}
          onChange={handleChange}
        />
      </label>

      <label>
        Saturated Fats (g):
        <input
          type="number"
          name="saturated_fats"
          value={formData.saturated_fats}
          onChange={handleChange}
        />
      </label>

      <label>
        Trans Fats (g):
        <input
          type="number"
          name="trans_fats"
          value={formData.trans_fats}
          onChange={handleChange}
        />
      </label>

      <label>
        Cholesterol (mg):
        <input
          type="number"
          name="cholesterol"
          value={formData.cholesterol}
          onChange={handleChange}
        />
      </label>

      <label>
        Sodium (mg):
        <input
          type="number"
          name="sodium"
          value={formData.sodium}
          onChange={handleChange}
        />
      </label>

      <label>
        Total Carbohydrates (g):
        <input
          type="number"
          name="total_carbohydrates"
          value={formData.total_carbohydrates}
          onChange={handleChange}
        />
      </label>

      <label>
        Dietary Fiber (g):
        <input
          type="number"
          name="dietary_fiber"
          value={formData.dietary_fiber}
          onChange={handleChange}
        />
      </label>

      <label>
        Total Sugars (g):
        <input
          type="number"
          name="total_sugars"
          value={formData.total_sugars}
          onChange={handleChange}
        />
      </label>

      <label>
        Added Sugars (g):
        <input
          type="number"
          name="added_sugars"
          value={formData.added_sugars}
          onChange={handleChange}
        />
      </label>


      <label>
        Calories:
        <input
          type="number"
          name="calories"
          value={formData.calories}
          onChange={handleChange}
        />
      </label>

      <label>
        Protein (g):
        <input
          type="number"
          name="protein"
          value={formData.protein}
          onChange={handleChange}
        />
      </label>

      <label>
        Cuisine:
        <input name="cuisine" value={formData.cuisine} onChange={handleChange} />
      </label>

      <label>
        Dietary Restriction:
        <select
          name="restriction"
          value={formData.restriction}
          onChange={handleChange}
        >
          <option value="">-- Select a restriction --</option>
          {allowedRestrictions.map((r) => (
            <option key={r} value={r}>
              {r}
            </option>
          ))}
        </select>
      </label>

      <button type="submit">Add Food</button>
    </form>

  );
}
