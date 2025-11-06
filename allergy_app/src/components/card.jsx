import React from "react";

const Card = (props) => {
    console.log("Card props:", props.dietaryRestriction);
    return (
      <div className={'Card'}>
        <img className="Card-img" src= {props.picture}/>
        <h4>{props.name}</h4>
        <h5>{props.cuisine}</h5>
        <h5>{props.dietaryRestriction?.join(", ")}</h5>
        
      </div>
    )
  }
  
  export default Card