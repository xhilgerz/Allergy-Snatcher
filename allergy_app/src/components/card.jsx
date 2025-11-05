import React from "react";

const Card = (props) => {

    return (
      <div className={'Card'}>
        <img className="Card-img" src= {props.picture}/>
        <h4>{props.name}</h4>
        <h5>{props.cuisine}</h5>
        <h5>{props.dietaryRestriction}</h5>
        
      </div>
    )
  }
  
  export default Card