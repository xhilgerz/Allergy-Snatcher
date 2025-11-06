// src/App.js
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Home from "./routes/HomePage/Home";
import About from "./routes/HomePage/About";
import AddFood from "./routes/Food/AddFood" // optional for example

function App() {
  return (
    <Router>
      <nav className="navbar">
        <Link to="/">Home</Link>
        <Link to="/about">About</Link>
        <Link to="/add-food">Add Food</Link>
      </nav>

      <Routes>
        <Route path="/" element={<Home />} />        {/* Home route */}
        <Route path="/about" element={<About />} />  {/* Example extra page */}
        <Route path="/add-food" element={<AddFood />} /> {/* Example extra page */}
      </Routes>
    </Router>
  );
}

export default App;
