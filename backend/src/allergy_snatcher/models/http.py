"""
Pydantic models for validating and serializing HTTP request/response data.
"""
from pydantic import BaseModel, Field
from typing import List, Optional

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