import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const ADMIN_PASSWORD = process.env.REACT_APP_ADMIN_PASSWORD;

export default function LogIn() {
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [status, setStatus] = useState("");
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const navigate = useNavigate();

  // Check localStorage on load
  useEffect(() => {
    const storedValue = localStorage.getItem("isAdminAuthenticated");
    if (storedValue === "true") {
      setIsAuthenticated(true);
      setStatus("You are already logged in.");
    }
  }, []);

  // Handle login
  const handleSubmit = (event) => {
    event.preventDefault();
    setError("");
    setStatus("");

    if (!ADMIN_PASSWORD) {
      setError("Admin password is not configured. Check your .env file.");
      return;
    }

    if (password === ADMIN_PASSWORD) {
      localStorage.setItem("isAdminAuthenticated", "true");
      setIsAuthenticated(true);
      setStatus("Success! Choose what you want to do next.");
      setPassword("");
    } else {
      setError("Incorrect password. Please try again.");
    }
  };

  // Handle logout
  const handleLogout = () => {
    localStorage.removeItem("isAdminAuthenticated");
    setIsAuthenticated(false);
    setStatus("You have been logged out.");
  };

  return (
    <div className="admin-login">
      <h1>Admin Log In</h1>
      <p>Enter the admin password to access moderation tools.</p>

      {isAuthenticated ? (
        <div className="admin-login__status">
          <p>{status || "You are logged in."}</p>
          <p>Select an option to continue:</p>

          <div className="admin-login__actions">
            <button type="button" onClick={() => navigate("/approve-food")}>
              Approve Foods
            </button>
            <button type="button" onClick={() => navigate("/edit-food")}>
              Edit Foods
            </button>
            <button type="button" onClick={handleLogout}>
              Log out
            </button>
          </div>
        </div>
      ) : (
        <form className="admin-login__form" onSubmit={handleSubmit}>
          <label htmlFor="adminPassword">Password</label>
          <input
            id="adminPassword"
            type="password"
            value={password}
            placeholder="Enter admin password"
            onChange={(e) => setPassword(e.target.value)}
          />

          <button type="submit">Log In</button>

          {error && <p className="admin-login__error">{error}</p>}
          {status && !error && (
            <p className="admin-login__status-text">{status}</p>
          )}
        </form>
      )}
    </div>
  );
}
