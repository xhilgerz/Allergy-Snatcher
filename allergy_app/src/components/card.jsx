import React, { useState } from "react";
import { updateFood, deleteFood } from "../api/api.js";

const Card = ({
  food,
  showApproveButton = false,
  showEditButtons = false,
  onApprove,
  onReject,
}) => {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleEdit = (e) => {
    e.stopPropagation();
    console.log("Editing food with ID:", food.id);

    // Navigate to edit page
    window.location.href = `/edit-food/${food.id}`;
  };

  const handleApprove = async (e) => {
    e.stopPropagation();
    const payload = { ...food, publication_status: "public" };
    await updateFood(food.id, payload);
    onApprove?.();
  };

  const handleReject = async (e) => {
    e.stopPropagation();
    await deleteFood(food.id, food);
    onReject?.();
  };

  return (
    <>
    <div className="Card" onClick={() => setIsModalOpen(true)}>
      <h4>{food.name}</h4>
      <h5>{food.cuisine?.cuisine}</h5>
      <h6>{food.dietaryRestriction?.join(", ")}</h6>

      {showApproveButton && (
        <div className="button-group">
          <button onClick={handleApprove} className="approve-btn">
            Approve
          </button>
          <button onClick={handleReject} className="reject-btn">
            Reject
          </button>
        </div>
      )}
      {showEditButtons && (
        <div className="button-group">
          <button onClick={handleEdit} className="edit-btn">
            Edit
          </button>
        </div>
      )}

    </div>
    {isModalOpen && (
      <div
        className="food-modal__backdrop"
        onClick={() => setIsModalOpen(false)}
        style={{
          position: "fixed",
          inset: 0,
          background: "rgba(0,0,0,0.5)",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          zIndex: 1000,
        }}
      >
        <div
          className="food-modal__dialog"
          onClick={(e) => e.stopPropagation()}
          style={{
            background: "#fff",
            padding: "1.5rem",
            borderRadius: "8px",
            maxWidth: "480px",
            width: "90%",
            color: "#333",
            position: "relative",
          }}
        >
          <button
            className="food-modal__close"
            onClick={() => setIsModalOpen(false)}
            style={{
              border: "none",
              background: "transparent",
              fontSize: "1.5rem",
              position: "absolute",
              right: "1.5rem",
              top: "1rem",
              cursor: "pointer",
            }}
            aria-label="Close"
          >
            ×
          </button>
          <h2>{food.name}</h2>
          {food.brand && <p><strong>Brand:</strong> {food.brand}</p>}
          <p><strong>Cuisine:</strong> {food.cuisine?.cuisine ?? "N/A"}</p>
          {food.dietaryRestriction && food.dietaryRestriction.length > 0 && (
            <p>
              <strong>Restrictions:</strong> {food.dietaryRestriction.join(", ")}
            </p>
          )}
          {food.ingredients && food.ingredients.length > 0 && (
            <div>
              <strong>Ingredients:</strong>
              <ul>
                {food.ingredients.map((ingredient, idx) => (
                  <li key={idx}>
                    {ingredient.ingredient_name ?? ingredient}
                  </li>
                ))}
              </ul>
            </div>
          )}
          <div className="food-modal__nutrition">
            {[
              ["Calories", food.cal],
              ["Protein (g)", food.protein],
              ["Carbs (g)", food.carbs],
              ["Total Fats (g)", food.total_fats],
              ["Saturated Fats (g)", food.sat_fats ?? food.saturated_fats],
              ["Trans Fats (g)", food.trans_fats],
              ["Cholesterol (mg)", food.cholesterol],
              ["Sodium (mg)", food.sodium],
              ["Total Carbohydrates (g)", food.total_carbohydrates],
              ["Dietary Fiber (g)", food.dietary_fiber],
              ["Total Sugars (g)", food.sugars ?? food.total_sugars],
              ["Added Sugars (g)", food.added_sugars],
            ].map(([label, value]) => (
              <p key={label}>
                <strong>{label}:</strong> {value ?? "N/A"}
              </p>
            ))}
          </div>
          {food.nutritional_info && (
            <p style={{ marginTop: "0.75rem" }}>
              <strong>Notes:</strong> {food.nutritional_info}
            </p>
          )}
        </div>
      </div>
    )}
    </>
  );
}
  
  export default Card
