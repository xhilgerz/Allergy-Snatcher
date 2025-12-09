import React, { useEffect, useMemo, useState } from "react";
import Select from "react-select";
import { getCuisines, getDietRestrictions, getCategories } from "../api/api.js";

const defaultValues = {
  name: "",
  brand: "",
  ingredients: "",
  nutritional_info: "",
  total_fats: "",
  saturated_fats: "",
  trans_fats: "",
  cholesterol: "",
  sodium: "",
  dietary_fiber: "",
  total_sugars: "",
  calories: "",
  protein: "",
  carbs: "",
  cuisine: null,
  serving_amt: "",
  serving_unit: "",
  category_id: 1,
  restrictions: [],
  publication_status: "private",
};

export default function FoodForm({
  initialValues = null,
  onSubmit,
  submitLabel = "Save",
  onDelete,
  showDelete = false,
  isEditing = false,
  errors = {},
}) {
  const [formData, setFormData] = useState(defaultValues);
  const [restrictionOptions, setRestrictionOptions] = useState([]);
  const [cuisineOptions, setCuisineOptions] = useState([]);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [categoryOptions, setCategoryOptions] = useState([]);

  const normalizedInitialValues = useMemo(() => {
    const source = initialValues ?? {};
    const normalized = { ...defaultValues, ...source };
    if (Array.isArray(source.ingredients)) {
      normalized.ingredients = source.ingredients
        .map((i) => i.ingredient_name)
        .join(", ");
    } else if (typeof source.ingredients === "string") {
      normalized.ingredients = source.ingredients;
    }
    if (source.cuisine && typeof source.cuisine === "object") {
      normalized.cuisine = source.cuisine.id ?? null;
    } else if (typeof source.cuisine === "number") {
      normalized.cuisine = source.cuisine;
    }
    if (
      Array.isArray(source.restrictions) &&
      source.restrictions.length > 0
    ) {
      normalized.restrictions = source.restrictions;
    } else if (Array.isArray(source.dietary_restrictions)) {
      normalized.restrictions = source.dietary_restrictions.map(
        (r) => r.id
      );
    }
    if (source.category && source.category.id) {
      normalized.category_id = source.category.id;
    } else if (source.category_id) {
      normalized.category_id = source.category_id;
    }
    return normalized;
  }, [initialValues]);

  useEffect(() => {
    setFormData(normalizedInitialValues);
  }, [normalizedInitialValues]);

  useEffect(() => {
    (async () => {
      try {
        const list = await getDietRestrictions();
        setRestrictionOptions(
          list.map((r) => ({ value: r.id, label: r.restriction }))
        );
      } catch (err) {
        console.error("Failed to load restrictions", err);
      }
    })();
  }, []);

  useEffect(() => {
    (async () => {
      try {
        const list = await getCuisines();
        setCuisineOptions(list.map((c) => ({ value: c.id, label: c.cuisine })));
      } catch (err) {
        console.error("Failed to load cuisines", err);
      }
    })();
  }, []);

  useEffect(() => {
    (async () => {
      try {
        const list = await getCategories();
        setCategoryOptions(list.map((c) => ({ value: c.id, label: c.category })));
      } catch (err) {
        console.error("Failed to load categories", err);
      }
    })();
  }, []);

  const handleChange = (event) => {
    const { name, value, type } = event.target;
    setFormData((prev) => ({
      ...prev,
      [name]:
        type === "number"
          ? value === ""
            ? ""
            : parseFloat(value)
          : value,
    }));
  };

  const handleRestrictionsChange = (selected) => {
    const values = selected ? selected.map((opt) => opt.value) : [];
    setFormData((prev) => ({ ...prev, restrictions: values }));
  };

  const handleCuisineChange = (selected) => {
    setFormData((prev) => ({ ...prev, cuisine: selected ? selected.value : null }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!onSubmit) {
      return;
    }

    setIsSubmitting(true);
    // Resolve cuisine ID: if the form value is an id, use it; if it's a string label, match to options.
    let cuisineId = formData.cuisine;
    if (typeof cuisineId === "string" && cuisineId.trim().length > 0) {
      const match = cuisineOptions.find(
        (opt) => opt.label.toLowerCase() === cuisineId.trim().toLowerCase()
      );
      cuisineId = match ? match.value : null;
    }

    const payload = {
      name: formData.name,
      brand: formData.brand,
      publication_status: formData.publication_status,
      carbs: formData.carbs === "" ? null : Number(formData.carbs),
      protein: formData.protein === "" ? null : Number(formData.protein),
      total_fats:
        formData.total_fats === "" ? null : Number(formData.total_fats),
      sat_fats:
        formData.saturated_fats === "" ? null : Number(formData.saturated_fats),
      trans_fats:
        formData.trans_fats === "" ? null : Number(formData.trans_fats),
      cholesterol:
        formData.cholesterol === "" ? null : Number(formData.cholesterol),
      sodium: formData.sodium === "" ? null : Number(formData.sodium),
      dietary_fiber:
        formData.dietary_fiber === "" ? null : Number(formData.dietary_fiber),
      sugars: formData.total_sugars === "" ? null : Number(formData.total_sugars),
      added_sugars: formData.added_sugars === "" ? null : Number(formData.added_sugars),
      cal: formData.calories === "" ? null : Number(formData.calories),
      serving_amt: formData.serving_amt === "" ? null : Number(formData.serving_amt),
      serving_unit: formData.serving_unit || null,
      category_id: formData.category_id,
      cuisine_id: cuisineId,
      ingredients: formData.ingredients
        ? formData.ingredients
            .split(",")
            .map((ingredient) => ({ ingredient_name: ingredient.trim() }))
            .filter((ingredient) => ingredient.ingredient_name.length > 0)
        : [],
      dietary_restriction_ids: formData.restrictions,
    };

    try {
      await onSubmit(payload);
    } finally {
      setIsSubmitting(false);
    }
  };

  const ErrorMessage = ({ field }) => {
    // The form uses 'saturated_fats' and 'calories' but the backend might send 'sat_fats' or 'cal'
    const fieldName =
      field === "saturated_fats"
        ? "saturated_fats"
        : field === "calories"
        ? "calories"
        : field;
    const backendFieldName =
      field === "saturated_fats"
        ? "sat_fats"
        : field === "calories"
        ? "cal"
        : field;
    
    const message = errors[fieldName] || errors[backendFieldName];
    return message ? <span className="error-message">{message}</span> : null;
  };


  return (
    <form className="food-form" onSubmit={handleSubmit}>
      <label>
        Name:
        <input name="name" value={formData.name} onChange={handleChange} />
        <ErrorMessage field="name" />
      </label>

      <label>
        Brand:
        <input name="brand" value={formData.brand} onChange={handleChange} />
        <ErrorMessage field="brand" />
      </label>

      <label>
        Ingredients (comma-separated):
        <textarea
          name="ingredients"
          value={formData.ingredients}
          onChange={handleChange}
        />
        <ErrorMessage field="ingredients" />
      </label>

      {[
        ["total_fats", "Total Fats (g)"],
        ["saturated_fats", "Saturated Fats (g)"],
        ["trans_fats", "Trans Fats (g)"],
        ["cholesterol", "Cholesterol (mg)"],
        ["sodium", "Sodium (mg)"],
        ["carbs", "Total Carbohydrates (g)"],
        ["dietary_fiber", "Dietary Fiber (g)"],
        ["total_sugars", "Total Sugars (g)"],
        ["added_sugars", "Added Sugars (g)"],
        ["calories", "Calories"],
        ["protein", "Protein (g)"],
      ].map(([name, label]) => (
        <label key={name}>
          {label}
          <input
            type="number"
            name={name}
            value={formData[name]}
            onChange={handleChange}
            step="any"
          />
          <ErrorMessage field={name} />
        </label>
      ))}

      <label>
        Cuisine:
        <Select
          name="cuisine"
          options={cuisineOptions}
          value={
            cuisineOptions.find((option) => option.value === formData.cuisine) ||
            null
          }
          onChange={handleCuisineChange}
          placeholder="Select a cuisine..."
        />
        <ErrorMessage field="cuisine_id" />
      </label>

      <label>
        Category:
        <Select
          name="category"
          options={categoryOptions}
          value={
            categoryOptions.find((option) => option.value === formData.category_id) ||
            null
          }
          onChange={(selected) =>
            setFormData((prev) => ({ ...prev, category_id: selected ? selected.value : null }))
          }
          placeholder="Select a category..."
        />
        <ErrorMessage field="category_id" />
      </label>

      <label>
        Serving Amount:
        <input
          type="number"
          name="serving_amt"
          value={formData.serving_amt}
          onChange={handleChange}
          min="0"
          step="any"
        />
        <ErrorMessage field="serving_amt" />
      </label>
      <label>
        Serving Unit:
        <select
          name="serving_unit"
          value={formData.serving_unit}
          onChange={handleChange}
        >
          <option value="">Select unit</option>
          <option value="g">g</option>
          <option value="mg">mg</option>
          <option value="oz">oz</option>
          <option value="lb">lb</option>
          <option value="tsp">tsp</option>
          <option value="tbsp">tbsp</option>
          <option value="cup">cup</option>
          <option value="item">item</option>
        </select>
        <ErrorMessage field="serving_unit" />
      </label>

      <label>
        Dietary Restrictions:
        <Select
          isMulti
          name="restrictions"
          options={restrictionOptions}
          value={restrictionOptions.filter((option) =>
            formData.restrictions.includes(option.value)
          )}
          onChange={handleRestrictionsChange}
          placeholder="Select dietary restrictions..."
        />
        <ErrorMessage field="dietary_restriction_ids" />
      </label>

      {isEditing && (
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
      )}

      <div className="food-form__actions">
        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? "Saving..." : submitLabel}
        </button>
        {showDelete && onDelete && (
          <button
            type="button"
            className="delete-btn"
            onClick={onDelete}
            disabled={isSubmitting}
          >
            Delete
          </button>
        )}
      </div>
    </form>
  );
}
