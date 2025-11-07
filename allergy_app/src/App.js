// src/App.js
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Home from "./routes/HomePage/Home";
import About from "./routes/HomePage/About";
import AddFood from "./routes/Food/AddFood"; // optional for example
import ApproveFood from "./routes/Account/Admin/ApproveFood";
import RestrictionsPage from "./routes/Food/RestrictionsPage";

function App() {
  return (
    <Router>
      <nav className="navbar">
        <Link to="/">Home</Link>
        <Link to="/about">About</Link>
        <Link to="/add-food">Add Food</Link>
        <Link to="/approve-food">Approve Food</Link> {/* New link for PendingFoods */}
      </nav>

      <Routes>
        <Route path="/" element={<Home />} />        {/* Home route */}
        <Route path="/about" element={<About />} />  {/* Example extra page */}
        <Route path="/add-food" element={<AddFood />} /> {/* Example extra page */}
        <Route path="/approve-food" element={<ApproveFood />} /> {/* New route for ApproveFoods */}
        <Route path="/restrictions/:restrictionName" element={<RestrictionsPage />} />

      </Routes>
    </Router>
  );
}

export default App;
