import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import FoodForm from "./FoodForm.jsx";
import { deleteFood, getFoodById, updateFood } from "../api/api.js";

export default function EditFoodDetails() {
  const { foodId } = useParams();
  const navigate = useNavigate();
  const [initialValues, setInitialValues] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;
    (async () => {
      try {
        const food = await getFoodById(foodId);
        if (!isMounted) return;
        setInitialValues({
          ...food,
          ingredients: food.ingredients ?? [],
          restrictions: food.dietary_restrictions?.map((r) => r.id) ?? [],
          cuisine: food.cuisine?.id ?? null,
          category_id: food.category?.id ?? 1,
        });
      } catch (err) {
        console.error("Failed to load food", err);
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    })();

    return () => {
      isMounted = false;
    };
  }, [foodId]);

  const handleSubmit = async (payload) => {
    await updateFood(foodId, payload);
    alert("Food updated successfully!");
    navigate("/edit-food");
  };

  const handleDelete = async () => {
    if (!window.confirm("Are you sure you want to delete this food item?")) {
      return;
    }
    await deleteFood(foodId,true);
    alert("Food deleted successfully!");
    navigate("/edit-food");
  };

  if (loading) {
    return <p>Loading...</p>;
  }

  if (!initialValues) {
    return <p>Food not found.</p>;
  }

  return (
    <FoodForm
      initialValues={initialValues}
      onSubmit={handleSubmit}
      submitLabel="Save Changes"
      showDelete
      onDelete={handleDelete}
      isEditing
    />
  );
}
