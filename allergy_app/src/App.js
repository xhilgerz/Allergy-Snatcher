// src/App.js
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Home from "./routes/HomePage/Home.jsx";
import About from "./routes/HomePage/About.jsx";
import AddFood from "./routes/Food/AddFood.jsx"; // optional for example
import ApproveFood from "./routes/Account/Admin/ApproveFood.jsx";
import RestrictionsPage from "./routes/Food/RestrictionsPage.jsx";
import EditFood from "./routes/Account/Admin/EditFoods.jsx";
import EditFoodDetails from "./components/editFoodDetails.jsx";

function App() {
  return (
    <Router>
      <nav className="navbar">
        <Link to="/">Home</Link>
        <Link to="/about">About</Link>
        <Link to="/add-food">Add Food</Link>
        <Link to="/approve-food">Approve Food</Link> {/* New link for PendingFoods */}
        <Link to="/edit-food">Edit Food</Link>
      </nav>

      <Routes>
        <Route path="/" element={<Home />} />        {/* Home route */}
        <Route path="/about" element={<About />} />  {/* Example extra page */}
        <Route path="/add-food" element={<AddFood />} /> {/* Example extra page */}
        <Route path="/approve-food" element={<ApproveFood />} /> {/* New route for ApproveFoods */}
        <Route path="/restrictions/:restrictionName" element={<RestrictionsPage />} />
        <Route path="/edit-food" element={<EditFood />} />
        <Route path="/edit-food/:foodId" element={<EditFoodDetails />} />

      </Routes>
    </Router>
  );
}

export default App;
