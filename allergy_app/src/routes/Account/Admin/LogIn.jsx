import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../../context/AuthContext.jsx";

export default function LogIn() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [isAdminRegister, setIsAdminRegister] = useState(false);
  const [adminKey, setAdminKey] = useState("");
  const [error, setError] = useState("");
  const [status, setStatus] = useState("");
  const [mode, setMode] = useState("login"); // "login" | "register"

  const { user, loading, login, register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setStatus("");
    try {
      if (mode === "login") {
        await login(username, password);
        setStatus("Logged in! Choose what you want to do next.");
      } else {
        await register({
          username,
          email,
          password,
          role: isAdminRegister ? "admin" : "user",
          admin_key: isAdminRegister ? adminKey : undefined,
        });
        setStatus(
          `Registered as ${isAdminRegister ? "admin" : "user"} and logged in! Choose what you want to do next.`
        );
      }
      setUsername("");
      setPassword("");
      setEmail("");
      setAdminKey("");
    } catch (err) {
      setError(
        err.message || (mode === "login" ? "Login failed" : "Registration failed")
      );
    }
  };

  if (loading) return <p>Checking login…</p>;

  return (
    <div className="admin-login">
      <h1>Register / Log In</h1>

      {user ? (
        <div className="admin-login__status">
          <p>
            {status ||
              `You are logged in as ${user.username} (${user.role}).`}
          </p>
          <p>Select an option to continue:</p>

          <div className="admin-login__actions">
            {user.role === "admin" ? (
              <>
                <button type="button" onClick={() => navigate("/approve-food")}>
                  Approve Foods
                </button>
                <button type="button" onClick={() => navigate("/edit-food")}>
                  Edit Foods
                </button>
                <button type="button" onClick={() => navigate("/manage-tags")}>
                  Manage Tags
                </button>
              </>
            ) : (
              <p>You are logged in as a standard user.</p>
            )}
          </div>
        </div>
      ) : (
        <form className="admin-login__form" onSubmit={handleSubmit}>
          <div style={{ display: "flex", gap: "0.5rem", marginBottom: "1rem" }}>
            <button
              type="button"
              onClick={() => {
                setMode("login");
                setIsAdminRegister(false);
                setError("");
                setStatus("");
              }}
              style={{ fontWeight: mode === "login" ? "bold" : "normal" }}
            >
              Log In
            </button>
            <button
              type="button"
              onClick={() => {
                setMode("register");
                setError("");
                setStatus("");
              }}
              style={{ fontWeight: mode === "register" ? "bold" : "normal" }}
            >
              Register
            </button>
          </div>

          <label htmlFor="username">Username</label>
          <input
            id="username"
            value={username}
            placeholder="Enter username"
            onChange={(e) => setUsername(e.target.value)}
          />

          <label htmlFor="adminPassword">Password</label>
          <input
            id="adminPassword"
            type="password"
            value={password}
            placeholder="Enter password"
            onChange={(e) => setPassword(e.target.value)}
          />

          {mode === "register" && (
            <>
              <label htmlFor="email">Email</label>
              <input
                id="email"
                type="email"
                value={email}
                placeholder="Enter email"
                onChange={(e) => setEmail(e.target.value)}
              />
              
            </>
          )}

          <button type="submit">{mode === "login" ? "Log In" : "Register"}</button>

          {error && <p className="admin-login__error">{error}</p>}
          {status && !error && (
            <p className="admin-login__status-text">{status}</p>
          )}
        </form>
      )}
    </div>
  );
}
