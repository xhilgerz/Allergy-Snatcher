from pydantic import BaseModel, Field, field_validator, model_validator, ValidationInfo
from typing import List, Optional, Literal
from .database import DietaryRestriction, Category, Cuisine

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
    food_id: int
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

class FoodValidatorModel(BaseModel):
    @field_validator('dietary_restriction_ids', mode='before', check_fields=False)
    @classmethod
    def validate_dietary_restriction_ids(cls, v):
        if not v or v == '[]':
            return v
        
        restrictions = DietaryRestriction.query.all()
        valid_ids = {r.id for r in restrictions}
        valid_names = {r.restriction for r in restrictions}

        for sel in v:
            if isinstance(sel, str):
                if sel not in valid_names:
                    raise ValueError(f"Invalid dietary restriction: {sel}")
            elif isinstance(sel, int):
                if sel not in valid_ids:
                    raise ValueError(f"Invalid dietary restriction ID: {sel}")
            else:
                raise ValueError(f"Invalid dietary restriction ID: {sel}")
            
        return v
    
    @model_validator(mode='before')
    @classmethod
    def validate_fats(cls, data):
        total_fats = data.get('total_fats')
        sat_fats = data.get('sat_fats')
        trans_fats = data.get('trans_fats')

        if total_fats is not None:
            if sat_fats is not None and trans_fats is not None:
                if total_fats < sat_fats + trans_fats:
                    raise ValueError("total_fats cannot be less than the sum of sat_fats and trans_fats")
            elif sat_fats is not None and total_fats < sat_fats:
                raise ValueError("total_fats cannot be less than sat_fats")
            elif trans_fats is not None and total_fats < trans_fats:
                raise ValueError("total_fats cannot be less than trans_fats")
        
        return data

    @field_validator('category_id', mode='before', check_fields=False)
    @classmethod
    def validate_category_id(cls, v):
        if v is None:
            return v
        if not Category.query.get(v):
            raise ValueError(f"Invalid category ID: {v}")
        return v

    @field_validator('cuisine_id', mode='before', check_fields=False)
    @classmethod
    def validate_cuisine_id(cls, v):
        if v is None:
            return v
        if not Cuisine.query.get(v):
            raise ValueError(f"Invalid cuisine ID: {v}")
        return v
    
    @field_validator(
        'dietary_fiber', 'sugars', 'protein', 'carbs', 'cal', 
        'cholesterol', 'sodium', 'trans_fats', 'total_fats', 
        'sat_fats', 'serving_amt',
        check_fields=False
    )
    @classmethod
    def validate_non_negative(cls, v: float, info: ValidationInfo):
        if v is not None and v < 0:
            raise ValueError(f"{info.field_name} cannot be negative")
        return v

class CreateFoodSchema(FoodValidatorModel):
    """
    Schema for creating a new food item.
    """
    name: str
    brand: Optional[str] = None
    publication_status: Optional[Literal["private"]] = "private"
    dietary_fiber: float
    sugars: float
    protein: float
    carbs: float
    cal: float
    cholesterol: float
    sodium: float
    trans_fats: float
    total_fats: float
    sat_fats: float
    serving_amt: float
    serving_unit: Literal['g','mg', 'oz','lb', 'tsp', 'tbsp', 'cup', 'item']
    category_id: int
    cuisine_id: Optional[int] = None
    ingredients: List[CreateIngredientSchema] = Field(default_factory=list, min_length=1)
    dietary_restriction_ids: List[int|str] = [] # accepts name of dietary restriction or restriction id

class UpdateFoodSchema(FoodValidatorModel):
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
    dietary_restriction_ids: Optional[List[int|str]] = None
