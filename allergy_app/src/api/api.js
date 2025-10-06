// src/api/api.js

const BASE_URL =
  process.env.NODE_ENV === "production"
    ? "http://backend:5000" // inside Docker Compose network
    : "http://localhost:5000"; // when testing locally

export async function getFoods() {
  try {
    const response = await fetch(`${BASE_URL}/api/foods`);
    if (!response.ok) {
      throw new Error("Failed to fetch foods");
    }
    const data = await response.json();
    console.log("✅ Data fetched from Flask:", data); 
    return data;
  } catch (error) {
    console.error("Error fetching foods:", error);
    throw error;
  }
}
