import React, { useEffect, useMemo, useState } from "react";
import Select from "react-select";
import { getCuisines, getDietRestrictions } from "../api/api.js";

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
  total_carbohydrates: "",
  dietary_fiber: "",
  total_sugars: "",
  added_sugars: "",
  calories: "",
  protein: "",
  carbs: "",
  cuisine: null,
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
}) {
  const [formData, setFormData] = useState(defaultValues);
  const [restrictionOptions, setRestrictionOptions] = useState([]);
  const [cuisineOptions, setCuisineOptions] = useState([]);
  const [isSubmitting, setIsSubmitting] = useState(false);

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
      cal: formData.calories === "" ? null : Number(formData.calories),
      category_id: formData.category_id,
      cuisine_id: formData.cuisine,
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

  return (
    <form className="food-form" onSubmit={handleSubmit}>
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
