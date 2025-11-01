import { use } from "react";
import { getFoods } from "../api/api";

function FoodList(){

    const [foods, setFoods] = useState([]);

  useEffect(() => {
    // fetch data from backend
    getFoods().then(data => setFoods(data));
  }, []); // empty array → run once on mount

  return (
    <ul>
      {foods.map((food) => (
        <li key={food.id}>{food.name}</li>
      ))}
    </ul>
  );
}
