// Page where users can insert a new food to the database
import AddFoodForm from "../../components/addFoodForm.jsx";
export default function About() {

  return (
    <div className="add-food-container">
      <h1>This is where you can add a new food item</h1>
        <p>Fill out the form below to add a new food to the database.</p>
        <AddFoodForm />
    </div>
  );
}