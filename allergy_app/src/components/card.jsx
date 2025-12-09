import React, { useState } from "react";
import { updateFood, deleteFood } from "../api/api.js";

const Card = ({
  food,
  showApproveButton = false,
  showEditButtons = false,
  onApprove,
  onReject,
  onDelete,
}) => {
  const [isModalOpen, setIsModalOpen] = useState(false); // detail modal
  const [confirmAction, setConfirmAction] = useState(null); // "approve" | "reject" | "delete"

  const handleEdit = (e) => {
    e.stopPropagation();
    console.log("Editing food with ID:", food.id);

    // Navigate to edit page
    window.location.href = `/edit-food/${food.id}`;
  };

  const requestApprove = (e) => {
    e.stopPropagation();
    setConfirmAction("approve");
  };

  const requestReject = (e) => {
    e.stopPropagation();
    setConfirmAction("reject");
  };

  const requestDelete = (e) => {
    e.stopPropagation();
    setConfirmAction("delete");
  };

  const runConfirmedAction = async () => {
    if (confirmAction === "approve") {
      const payload = { ...food, publication_status: "public" };
      await updateFood(food.id, payload, { force: true });
      onApprove?.();
    } else if (confirmAction === "reject" || confirmAction === "delete") {
      await deleteFood(food.id, true);
      onReject?.();
      onDelete?.();
    }
    setConfirmAction(null);
  };

  

  return (
    <>
    <div className="Card" onClick={() => setIsModalOpen(true)}>
      <h4>{food.name}</h4>
      <h5>{food.cuisine?.cuisine}</h5>
      <h6>{food.dietaryRestriction?.join(", ")}</h6>

      {showApproveButton && (
        <div className="button-group">
          <button onClick={requestApprove} className="approve-btn">
            Approve
          </button>
          <button onClick={requestReject} className="reject-btn">
            Reject
          </button>
        </div>
      )}
      {showEditButtons && (
        <div className="button-group">
          <button onClick={handleEdit} className="edit-btn">
            Edit
          </button>
          <button onClick={requestDelete} className="reject-btn">
            Delete
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
              ["Total Carbohydrates (g)", food.carbs],
              ["Total Fats (g)", food.total_fats],
              ["Saturated Fats (g)", food.sat_fats ?? food.saturated_fats],
              ["Trans Fats (g)", food.trans_fats],
              ["Cholesterol (mg)", food.cholesterol],
              ["Sodium (mg)", food.sodium],
              ["Dietary Fiber (g)", food.dietary_fiber],
              ["Total Sugars (g)", food.sugars ?? food.total_sugars],
              ,
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
    {confirmAction && (
      <div
        className="confirm-modal__backdrop"
        onClick={() => setConfirmAction(null)}
        style={{
          position: "fixed",
          inset: 0,
          background: "rgba(0,0,0,0.5)",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          zIndex: 1100,
        }}
      >
        <div
          className="confirm-modal__dialog"
          onClick={(e) => e.stopPropagation()}
          style={{
            background: "#fff",
            padding: "1.25rem",
            borderRadius: "8px",
            maxWidth: "360px",
            width: "90%",
            color: "#333",
          }}
        >
          <p style={{ marginBottom: "1rem" }}>
            {confirmAction === "approve" && "Approve this food and publish it?"}
            {confirmAction === "reject" && "Reject this food and delete it?"}
            {confirmAction === "delete" && "Delete this food?"}
          </p>
          <div
            className="button-group"
            style={{ display: "flex", gap: "0.75rem", justifyContent: "flex-end" }}
          >
            <button onClick={runConfirmedAction} className="approve-btn">
              Yes
            </button>
            <button onClick={() => setConfirmAction(null)} className="reject-btn">
              Cancel
            </button>
          </div>
        </div>
      </div>
    )}
    </>
  );
}
  
  export default Card
