// src/api/api.js

const API_BASE = process.env.REACT_APP_API_BASE_URL || "http://localhost:5001";

export async function getFoods() {
  try {
    const response = await fetch(`${API_BASE}/api/foods/10/0/True`);
    if (!response.ok) {
      throw new Error("Failed to fetch foods");
    }
    const data = await response.json();
    console.log(" Data fetched from Flask:", data); 
    return data;
  } catch (error) {
    console.error("Error fetching foods:", error);
    throw error;
  }

}
