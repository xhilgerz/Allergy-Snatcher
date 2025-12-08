// src/App.js
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Home from "./routes/HomePage/Home.jsx";
import About from "./routes/HomePage/About.jsx";
import AddFood from "./routes/Food/AddFood.jsx"; // optional for example
import ApproveFood from "./routes/Account/Admin/ApproveFood.jsx";
import RestrictionsPage from "./routes/Food/RestrictionsPage.jsx";
import EditFood from "./routes/Account/Admin/EditFoods.jsx";
import EditFoodDetails from "./components/editFoodDetails.jsx";
import Admin from "./routes/Account/Admin/LogIn.jsx";
import ManageTags from "./routes/Account/Admin/ManageTags.jsx";
import { AuthProvider, useAuth } from "./context/AuthContext.jsx";
import ErrorToast from "./components/ErrorToast.jsx";

function Nav() {
  const { user, loading, logout } = useAuth();
  return (
    <nav className="navbar">
      <Link to="/">Home</Link>
      <Link to="/add-food">Add Food</Link>
      <Link to="/admin">Log In / Sign Up</Link>
      <Link to="/about">About</Link>
      <span style={{ marginLeft: "auto" }}>
        {loading ? "Checking login…" : user ? `Signed in as ${user.username}` : "Not signed in"}
      </span>
      {user && (
        <button className="btn" onClick={logout} style={{ marginLeft: "0.5rem" }}>
          Log out
        </button>
      )}
    </nav>
  );
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <ErrorToast />
        <Nav />

        <Routes>
          <Route path="/" element={<Home />} />        {/* Home route */}
          <Route path="/about" element={<About />} />  {/* Example extra page */}
          <Route path="/add-food" element={<AddFood />} /> {/* Example extra page */}
          <Route path="/approve-food" element={<ApproveFood />} /> {/* New route for ApproveFoods */}
          <Route path="/restrictions/:restrictionName" element={<RestrictionsPage />} />
          <Route path="/edit-food" element={<EditFood />} />
          <Route path="/edit-food/:foodId" element={<EditFoodDetails />} />
          <Route path="/admin" element={<Admin />} />
          <Route path="/manage-tags" element={<ManageTags />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
