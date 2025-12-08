import { useEffect, useState } from "react";
import { subscribeToErrors } from "../utils/errorBus";

export default function ErrorToast() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    const unsubscribe = subscribeToErrors((event) => {
      setMessage(event.detail || "Something went wrong");
    });
    return unsubscribe;
  }, []);

  if (!message) return null;

  return (
    <div
      style={{
        position: "fixed",
        bottom: "1rem",
        right: "1rem",
        background: "#b00020",
        color: "white",
        padding: "0.75rem 1rem",
        borderRadius: "6px",
        boxShadow: "0 8px 16px rgba(0,0,0,0.2)",
        zIndex: 2000,
        display: "flex",
        gap: "0.5rem",
        alignItems: "center",
      }}
    >
      <span>{message}</span>
      <button
        onClick={() => setMessage("")}
        style={{
          border: "none",
          background: "transparent",
          color: "white",
          fontWeight: "bold",
          cursor: "pointer",
          fontSize: "1rem",
        }}
        aria-label="Dismiss error"
      >
        ×
      </button>
    </div>
  );
}
