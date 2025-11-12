import React from "react";
import { updateFood } from "../api/api.js";
import EditFoodDetails from "./editFoodDetails.jsx";

const Card = ({ food, showApproveButton = false, showEditButtons = false, onApprove }) => {

  const handleEdit = (e) => {
    e.stopPropagation();
    console.log("Editing food with ID:", food.id);

    // Navigate to edit page
    window.location.href = `/edit-food/${food.id}`;
  };

  const handleApprove = (e) => {
    e.stopPropagation();
    //onApprove?.(food.id);
    console.log("Approved food with ID:", food.id);
    food.publication_status = "public";
    onApprove?.(food);
    console.log("Food approved:", food);
    updateFood(food.id, food);


  };

  const handleReject = (e) => {
    e.stopPropagation();
    console.log("Rejected food with ID:", food.id);
    
  }

  return (
    <div className="Card">
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
  );
}
  
  export default Card