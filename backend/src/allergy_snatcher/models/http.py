from pydantic import BaseModel, Field
from typing import List, Optional, Literal

# --- Category Schemas ---

class CategorySchema(BaseModel):
    """
    Schema for representing a food category.
    """
    id: int
    category: str

    model_config = {"from_attributes": True}

class CategoryListSchema(BaseModel):
    """
    Schema for a list of categories.
    """
    categories: List[CategorySchema]

class CreateCategorySchema(BaseModel):
    """
    Schema for creating a new category.
    """
    category: str


# --- Cuisine Schemas ---

class CuisineSchema(BaseModel):
    """
    Schema for representing a food cuisine.
    """
    id: int
    cuisine: str

    model_config = {"from_attributes": True}

class CuisineListSchema(BaseModel):
    """
    Schema for a list of cuisines.
    """
    cuisines: List[CuisineSchema]

class CreateCuisineSchema(BaseModel):
    """
    Schema for creating a new cuisine.
    """
    cuisine: str


# --- Dietary Restriction Schemas ---

class DietaryRestrictionSchema(BaseModel):
    """
    Schema for representing a dietary restriction.
    """
    id: int
    restriction: str

    model_config = {"from_attributes": True}

class DietaryRestrictionListSchema(BaseModel):
    """
    Schema for a list of dietary restrictions.
    """
    restrictions: List[DietaryRestrictionSchema]

class CreateDietaryRestrictionSchema(BaseModel):
    """
    Schema for creating a new dietary restriction.
    """
    restriction: str

# --- Food Schemas ---

class IngredientSchema(BaseModel):
    """
    Schema for representing an ingredient.
    """
    id: int
    ingredient_name: str

    model_config = {"from_attributes": True}

class FoodSchema(BaseModel):
    """
    Schema for representing a food item.
    """
    id: int
    name: str
    brand: Optional[str] = None
    publication_status: Literal["public", "private", "unlisting"]
    dietary_fiber: Optional[float] = None
    sugars: Optional[float] = None
    protein: Optional[float] = None
    carbs: Optional[float] = None
    cal: Optional[float] = None
    cholesterol: Optional[float] = None
    sodium: Optional[float] = None
    trans_fats: Optional[float] = None
    total_fats: Optional[float] = None
    sat_fats: Optional[float] = None
    serving_amt: Optional[float] = None
    serving_unit: Optional[str] = None
    category: CategorySchema
    cuisine: Optional[CuisineSchema] = None
    dietary_restrictions: List[DietaryRestrictionSchema] = []
    model_config = {"from_attributes": True}

class FoodListSchema(BaseModel):
    """
    Schema for a list of food items.
    """
    foods: List[FoodSchema]


class CreateIngredientSchema(BaseModel):
    """
    Schema for creating a new ingredient.
    """
    ingredient_name: str

class CreateFoodSchema(BaseModel):
    """
    Schema for creating a new food item.
    """
    name: str
    brand: Optional[str] = None
    publication_status: Literal["public", "private", "unlisting"] = "private"
    dietary_fiber: Optional[float] = None
    sugars: Optional[float] = None
    protein: Optional[float] = None
    carbs: Optional[float] = None
    cal: Optional[float] = None
    cholesterol: Optional[float] = None
    sodium: Optional[float] = None
    trans_fats: Optional[float] = None
    total_fats: Optional[float] = None
    sat_fats: Optional[float] = None
    serving_amt: Optional[float] = None
    serving_unit: Optional[str] = None
    category_id: int
    cuisine_id: Optional[int] = None
    ingredients: List[CreateIngredientSchema] = []
    dietary_restriction_ids: List[int] = []

class UpdateFoodSchema(BaseModel):
    """
    Schema for updating a food item.
    """
    name: Optional[str] = None
    brand: Optional[str] = None
    publication_status: Optional[Literal["public", "private", "unlisting"]] = None
    dietary_fiber: Optional[float] = None
    sugars: Optional[float] = None
    protein: Optional[float] = None
    carbs: Optional[float] = None
    cal: Optional[float] = None
    cholesterol: Optional[float] = None
    sodium: Optional[float] = None
    trans_fats: Optional[float] = None
    total_fats: Optional[float] = None
    sat_fats: Optional[float] = None
    serving_amt: Optional[float] = None
    serving_unit: Optional[str] = None
    category_id: Optional[int] = None
    cuisine_id: Optional[int] = None
    ingredients: Optional[List[CreateIngredientSchema]] = None
    dietary_restriction_ids: Optional[List[int]] = None