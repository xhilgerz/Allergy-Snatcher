export async function getFoods() {
  try {
    const response = await fetch(`/api/foods/10/0/True`);
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


export async function addFood(foodData) {
  try {
    const response = await fetch(`/api/foods`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(foodData),
    });

    if (!response.ok) {
      throw new Error("Failed to add food");
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error adding food:", error);
    throw error;
  }
}