import React from "react";

const Card = ({ food, showApproveButton = false, onApprove }) => {


    
  const handleApprove = (e) => {
    e.stopPropagation();
    //onApprove?.(food.id);
    console.log("Approved food with ID:", food.id);
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
    </div>
  );
}
  
  export default Card