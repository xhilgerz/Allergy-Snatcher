// src/api/api.js

export async function getAdminPassword() {
  const response = await fetch(`/admin/password`);
  if (!response.ok) {
    const message = await response.text();
    throw new Error(`Failed to load admin password: ${message || response.status}`);
  }

  const data = await response.json();
  return data.password;
}


export async function getFoods() {
  console.log("API_BASE =", process.env.REACT_APP_API_BASE_URL);

  try {
    const response = await fetch(`/api/foods/100/0/True`);
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

export async function getFoodById(foodId) {
  try {
    const response = await fetch(`/api/foods/${foodId}`);
    if (!response.ok) {
      throw new Error(`Failed to fetch food ${foodId}`);
    }
    return await response.json();
  } catch (error) {
    console.error("Error fetching food:", error);
    throw error;
  }
}

export async function addFood(foodData) {
  try {
    const response = await fetch(`/api/foods/`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      credentials: "include", 
      body: JSON.stringify(foodData),
    });

    const text = await response.text();
    console.log("Backend response:", response.status, text);

    let data;

    try {
      data = JSON.parse(text);
    } catch {
      data = text;
    }

    if (!response.ok) {
      throw new Error("Failed to add food");
    }

    return data;
  } catch (error) {
    console.error("Error adding food:", error);
    throw error;
  }
}

  export async function updateFood(food_id, foodData) {
  try {

    const response = await fetch(`/api/foods/${food_id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      credentials: "include", 
      body: JSON.stringify(foodData),
    });

    // Handle response errors
    if (!response.ok) {
      const errText = await response.text();
      console.error("Backend error:", errText);
      throw new Error(`Failed to update food (status ${response.status})`);
    }

    const updatedFood = await response.json();
    console.log("Updated food:", updatedFood);
    return updatedFood;
  } catch (error) {
    console.error("Error updating food:", error);
    throw error;
  }
}

export async function deleteFood(food_id) {
  try {
    const response = await fetch(`/api/foods/${food_id}`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
    });

    // Handle response errors
    if (!response.ok) {
      const errText = await response.text();
      console.error("Backend error:", errText);
      throw new Error(`Failed to delete food (status ${response.status})`);
    }

    const deletedFood = await response.json();
    console.log("Deleted food:", deletedFood);
    return deletedFood;
  } catch (error) {
    console.error("Error deleting food:", error);
    throw error;
  }
}

export async function getDietRestrictions() {
  console.log("API_BASE =", process.env.REACT_APP_API_BASE_URL);

  try {
    const response = await fetch("/api/diet-restrictions/");
    if (!response.ok) {
      throw new Error("Failed to fetch diet restrictions");
    }
    const data = await response.json();
    console.log(" Data fetched from Flask:", data); 
    return data;
  } catch (error) {
    console.error("Error fetching foods:", error);
    throw error;
  }

}

export async function createDietRestriction(restrictionData) {
  try {
    const response = await fetch(`/api/diet-restrictions/`, {
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
    throw error;
  }
}

export async function deleteDietRestriction(restriction_id) {
  try {
    const response = await fetch(`/api/diet-restrictions/${restriction_id}`, {
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
    throw error;
  }
}



export async function getCuisines() {
  console.log("API_BASE =", process.env.REACT_APP_API_BASE_URL);

  try {
    const response = await fetch("/api/cuisines/");
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
    const response = await fetch(`/api/cuisines/`, {
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
    const response = await fetch(`/api/cuisines/${cuisine_id}`, {
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
    const response = await fetch(`/api/cuisines/`, {
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
    const response = await fetch(`/api/cuisines/${restriction_id}`, {
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
