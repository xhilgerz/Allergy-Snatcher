// src/api/api.js
import { emitError } from "../utils/errorBus";

const API_BASE = process.env.REACT_APP_API_BASE_URL || "";
const url = (path) => `${API_BASE}${path}`;

async function handleResponse(response, defaultMsg = "Request failed") {
  const text = await response.text();
  let message = defaultMsg;
  try {
    const parsed = text ? JSON.parse(text) : {};
    if (response.ok) return parsed;
    message = parsed.error || parsed.message || message;
  } catch {
    if (response.ok) return text || null;
    message = text || message;
  }
  const err = new Error(message);
  err._emitted = true; // mark so we don't emit twice downstream
  emitError(message);
  throw err;
}

function handleError(error, fallback = "Request failed") {
  if (!error?._emitted) {
    emitError(error?.message || fallback);
  }
  throw error;
}

export async function getAdminPassword() {
  const response = await fetch(url(`/admin/password`), { credentials: "include" });
  if (!response.ok) {
    const message = await response.text();
    throw new Error(`Failed to load admin password: ${message || response.status}`);
  }

  const data = await response.json();
  return data.password;
}


export async function registerUser({ username, email, password, role = "user", admin_key }) {
  const response = await fetch(url(`/auth/register`), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify({ username, email, password, role, admin_key }),
  });
  return handleResponse(response, "Registration failed");
}

export async function login(username, password) {
  const response = await fetch(url(`/auth/login`), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify({ username, password }),
  });
  return handleResponse(response, "Invalid credentials");
}

export async function logout() {
  await fetch(url(`/logout`), { method: "POST", credentials: "include" });
}

export async function getAuthStatus() {
  const response = await fetch(url(`/auth/status`), { credentials: "include" });
  if (!response.ok) {
    throw new Error("Failed to fetch auth status");
  }
  return response.json();
}

export async function getFoods() {
  console.log("API_BASE =", process.env.REACT_APP_API_BASE_URL);

  try {
    const response = await fetch(url(`/api/foods/100/0/True`), {
      credentials: "include",
    });
    const data = await handleResponse(response, "Failed to fetch foods");
    console.log(" Data fetched from Flask:", data); 
    return data;
  } catch (error) {
    console.error("Error fetching foods:", error);
    return handleError(error, "Failed to fetch foods");
  }

}

export async function getFoodById(foodId) {
  try {
    const response = await fetch(url(`/api/foods/${foodId}`), {
      credentials: "include",
    });
    return await handleResponse(response, `Failed to fetch food ${foodId}`);
  } catch (error) {
    console.error("Error fetching food:", error);
    return handleError(error, `Failed to fetch food ${foodId}`);
  }
}

export async function addFood(foodData) {
  try {
    const response = await fetch(url(`/api/foods/`), {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      credentials: "include", 
      body: JSON.stringify(foodData),
    });

    const data = await handleResponse(response, "Failed to add food");
    console.log("Backend response:", response.status, data);
    return data;
  } catch (error) {
    console.error("Error adding food:", error);
    return handleError(error, "Failed to add food");
  }
}

  export async function updateFood(food_id, foodData,{ force = false } = {}) {
  try {
  const headers = { "Content-Type": "application/json" };
    if (force) headers.confirmation = "force";

    const response = await fetch(url(`/api/foods/${food_id}`), {
      method: "PATCH",
      headers,
      credentials: "include", 
      body: JSON.stringify(foodData),
    });

    const updatedFood = await handleResponse(response, `Failed to update food (status ${response.status})`);
    console.log("Updated food:", updatedFood);
    return updatedFood;
  } catch (error) {
    console.error("Error updating food:", error);
    return handleError(error, "Failed to update food");
  }
}

export async function deleteFood(food_id, force = false) {
  try {
    const headers = { "Content-Type": "application/json" };
    if (force) headers.confirmation = "force";
    
    const response = await fetch(url(`/api/foods/${food_id}`), {
      method: "DELETE",
      headers,
      credentials: "include",
    });

    const deletedFood = await handleResponse(response, `Failed to delete food (status ${response.status})`);
    console.log("Deleted food:", deletedFood);
    return deletedFood;
  } catch (error) {
    console.error("Error deleting food:", error);
    return handleError(error, "Failed to delete food");
  }
}

export async function getDietRestrictions() {
  console.log("API_BASE =", process.env.REACT_APP_API_BASE_URL);

  try {
    const response = await fetch(url("/api/diet-restrictions/"), {
      credentials: "include",
    });
    const data = await handleResponse(response, "Failed to fetch diet restrictions");
    console.log(" Data fetched from Flask:", data); 
    return data;
  } catch (error) {
    console.error("Error fetching foods:", error);
    return handleError(error, "Failed to fetch diet restrictions");
  }

}

export async function createDietRestriction(restrictionData) {
  try {
    const response = await fetch(url(`/api/diet-restrictions/`), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify(restrictionData),
    });

    if (!response.ok) {
      const errText = await response.text();
      console.error("Backend error:", errText);
      throw new Error(
        `Failed to create diet restriction (status ${response.status})`
      );
    }

    const restriction = await response.json();
    console.log("Created restriction: ", restriction);
    return restriction;
  } catch (error) {
    console.error("Error creating restriction:", error);
    return handleError(error, "Failed to create diet restriction");
  }
}

export async function deleteDietRestriction(restriction_id) {
  try {
    const response = await fetch(url(`/api/diet-restrictions/${restriction_id}`), {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
    });

    if (!response.ok) {
      const errText = await response.text();
      console.error("Backend error:", errText);
      throw new Error(
        `Failed to delete diet restriction (status ${response.status})`
      );
    }

    const result = await response.json();
    console.log("Deleted restriction:", result);
    return result;
  } catch (error) {
    console.error("Error deleting restriction:", error);
    return handleError(error, "Failed to delete diet restriction");
  }
}

export async function getCategories() {
  try {
    const response = await fetch(url("/api/categories/"), {
      credentials: "include",
    });
    return await handleResponse(response, "Failed to fetch categories");
  } catch (error) {
    console.error("Error fetching categories:", error);
    return handleError(error, "Failed to fetch categories");
  }
}



export async function getCuisines() {
  console.log("API_BASE =", process.env.REACT_APP_API_BASE_URL);

  try {
    const response = await fetch(url("/api/cuisines/"), {
      credentials: "include",
    });
    if (!response.ok) {
      throw new Error("Failed to fetch cuisines");
    }
    const data = await response.json();
    console.log(" Data fetched from Flask:", data); 
    return data;
  } catch (error) {
    console.error("Error fetching cuisines:", error);
    throw error;
  }

}

export async function createCuisine(cuisineData){

  try {
    const response = await fetch(url(`/api/cuisines/`), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include", 
      body: JSON.stringify(cuisineData),
    });

    // Handle response errors
    if (!response.ok) {
      const errText = await response.text();
      console.error("Backend error:", errText);
      throw new Error(`Failed to create cuisine (status ${response.status})`);
    }

    const updatedFood = await response.json();
    console.log("Created food: ", updatedFood);
    return updatedFood;
  } catch (error) {
    console.error("Error creaiting cuisine:", error);
    throw error;
  }
}

export async function deleteCuisine(cuisine_id){
  try {
    const response = await fetch(url(`/api/cuisines/${cuisine_id}`), {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
    });

    // Handle response errors
    if (!response.ok) {
      const errText = await response.text();
      console.error("Backend error:", errText);
      throw new Error(`Failed to delete cuisine (status ${response.status})`);
    }

    const deletedFood = await response.json();
    console.log("Deleted food:", deletedFood);
    return deletedFood;
  } catch (error) {
    console.error("Error deleting cuisine:", error);
    throw error;
  }
}


export async function createRestriction(restrictionData){

  try {
    const response = await fetch(url(`/api/diet-restrictions/`), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include", 
      body: JSON.stringify(restrictionData),
    });

    // Handle response errors
    if (!response.ok) {
      const errText = await response.text();
      console.error("Backend error:", errText);
      throw new Error(`Failed to create cuisine (status ${response.status})`);
    }

    const updatedFood = await response.json();
    console.log("Created food: ", updatedFood);
    return updatedFood;
  } catch (error) {
    console.error("Error creaiting cuisine:", error);
    throw error;
  }
}

export async function deleteRestriction(restriction_id){
  try {
    const response = await fetch(url(`/api/diet-restrictions/${restriction_id}`), {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
    });

    // Handle response errors
    if (!response.ok) {
      const errText = await response.text();
      console.error("Backend error:", errText);
      throw new Error(`Failed to delete cuisine (status ${response.status})`);
    }

    const deletedFood = await response.json();
    console.log("Deleted food:", deletedFood);
    return deletedFood;
  } catch (error) {
    console.error("Error deleting cuisine:", error);
    throw error;
  }
}
