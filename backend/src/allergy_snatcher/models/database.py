"""
SQLAlchemy models for a user authentication and food tracking system, 
based on the provided relational schema.
"""

# Allows for forward-referencing type hints in relationships (e.g., Mapped["User"])
from __future__ import annotations
import datetime
from typing import List
from sqlalchemy import create_engine, Integer, String, DateTime, ForeignKey, UniqueConstraint, func, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# --- Base Class ---
# All models will inherit from this class
class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""
    pass

# --- User Model ---
class User(Base):
    """
    Represents a user in the system.
    Matches the 'Users' table in the diagram.
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Unique username for login
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    
    # User's primary email address. Also unique.
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    
    role: Mapped[str] = mapped_column(String(50), nullable=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str] = mapped_column(String(100), nullable=True)

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # --- Relationships ---
    
    # One-to-one relationship with Password.
    # A user can exist without a password (e.g., OAuth-only)
    password: Mapped[Password | None] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    
    # One-to-many: A user can have multiple OAuth accounts linked
    oauth_accounts: Mapped[List[OAuthAccount]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    
    # One-to-many: A user can have multiple active sessions
    sessions: Mapped[List[UserSession]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    
    # One-to-many: A user can contribute many food items
    foods_contributed: Mapped[List[Food]] = relationship(
        back_populates="contributor"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id!r}, username={self.username!r})>"

# --- Password Model ---
class Password(Base):
    """
    Stores the user's hashed password in a separate table.
    This creates a one-to-one relationship with User and allows a
    User to exist without a password.
    """
    __tablename__ = "passwords"
    
    # The primary key is also the foreign key to users,
    # enforcing a one-to-one relationship.
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    
    # Stored hash of the user's local password.
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    # --- Relationship ---
    
    # One-to-one relationship back to the User
    user: Mapped[User] = relationship(back_populates="password")
    
    def __repr__(self) -> str:
        return f"<Password(user_id={self.user_id!r})>"

# --- OAuth Account Model ---
class OAuthAccount(Base):
    """
    Represents a link to an external OAuth provider (e.g., Google, GitHub).
    This links to the User, not the Session, to allow for persistent
    "Sign in with..." functionality.
    """
    __tablename__ = "oauth_accounts"
    
    __table_args__ = (
        UniqueConstraint("provider", "provider_user_id", name="uq_provider_user_id"),
        UniqueConstraint("provider", "user_id", name="uq_provider_user"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    provider: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    provider_user_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    access_token: Mapped[str] = mapped_column(String(1024), nullable=True)
    refresh_token: Mapped[str] = mapped_column(String(1024), nullable=True)
    expires_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    scopes: Mapped[str] = mapped_column(String(1024), nullable=True)
    
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    user: Mapped[User] = relationship(back_populates="oauth_accounts")

    def __repr__(self) -> str:
        return f"<OAuthAccount(id={self.id!r}, user_id={self.user_id!r}, provider={self.provider!r})>"

# --- User Session Model ---
class UserSession(Base):
    """
    Represents an active, authenticated user session (matches 'Sessions' table).
    """
    __tablename__ = "user_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    
    # This corresponds to 'Client Token' in the diagram
    session_token: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    
    # Corresponds to 'Expires' in the diagram
    expires_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    
    # Corresponds to 'Created' in the diagram
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user: Mapped[User] = relationship(back_populates="sessions")

    def __repr__(self) -> str:
        return f"<UserSession(id={self.id!r}, user_id={self.user_id!r}, expires_at={self.expires_at!r})>"


# ---
# --- Food Models
# ---

class Category(Base):
    """
    Lookup table for food categories (e.g., 'Dairy', 'Vegetable').
    """
    __tablename__ = "categories"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    
    # One-to-many: A category can have many foods
    foods: Mapped[List[Food]] = relationship(back_populates="category")

    def __repr__(self) -> str:
        return f"<Category(id={self.id!r}, category={self.category!r})>"

class Cuisine(Base):
    """
    Lookup table for food cuisines (e.g., 'Italian', 'Mexican').
    """
    __tablename__ = "cuisines"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    cuisine: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    # One-to-many: A cuisine can apply to many foods
    foods: Mapped[List[Food]] = relationship(back_populates="cuisine")

    def __repr__(self) -> str:
        return f"<Cuisine(id={self.id!r}, cuisine={self.cuisine!r})>"

class DietaryRestriction(Base):
    """
    Lookup table for dietary restrictions (e.g., 'Gluten-Free', 'Vegan').
    """
    __tablename__ = "dietary_restrictions"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    restriction: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    
    # Many-to-many relationship with Food, via DietRestrictAssoc
    food_associations: Mapped[List[DietRestrictAssoc]] = relationship(
        back_populates="restriction", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<DietaryRestriction(id={self.id!r}, restriction={self.restriction!r})>"


class Food(Base):
    """
    Main table for food items and their nutritional information.
    """
    __tablename__ = "foods"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    brand: Mapped[str] = mapped_column(String(100), nullable=True)
    
    # Nutritional info
    dietary_fiber: Mapped[float] = mapped_column(Float, nullable=True)
    sugars: Mapped[float] = mapped_column(Float, nullable=True)
    protein: Mapped[float] = mapped_column(Float, nullable=True)
    carbs: Mapped[float] = mapped_column(Float, nullable=True)
    cal: Mapped[float] = mapped_column(Float, nullable=True)
    cholesterol: Mapped[float] = mapped_column(Float, nullable=True)
    sodium: Mapped[float] = mapped_column(Float, nullable=True)
    trans_fats: Mapped[float] = mapped_column(Float, nullable=True)
    total_fats: Mapped[float] = mapped_column(Float, nullable=True)
    sat_fats: Mapped[float] = mapped_column(Float, nullable=True)
    serving_amt: Mapped[float] = mapped_column(Float, nullable=True)
    serving_unit: Mapped[str] = mapped_column(String(50), nullable=True)
    
    # --- Foreign Keys & Relationships ---
    
    # (Optional) link to the user who contributed this item
    contributor_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    contributor: Mapped[User | None] = relationship(back_populates="foods_contributed")
    
    # (Required) link to a category
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
    category: Mapped[Category] = relationship(back_populates="foods")
    
    # (Required) link to a cuisine
    cuisine_id: Mapped[int] = mapped_column(ForeignKey("cuisines.id"), nullable=False)
    cuisine: Mapped[Cuisine] = relationship(back_populates="foods")

    # One-to-many: A food is made of multiple ingredients
    ingredients: Mapped[List[Ingredient]] = relationship(
        back_populates="food", cascade="all, delete-orphan"
    )
    
    # Many-to-many relationship with DietaryRestriction, via DietRestrictAssoc
    restriction_associations: Mapped[List[DietRestrictAssoc]] = relationship(
        back_populates="food", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Food(id={self.id!r}, name={self.name!r})>"

class Ingredient(Base):
    """
    Represents an ingredient for a food item.
    In the diagram, 'Ingredient' is a text field.
    """
    __tablename__ = "ingredients"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # The food this ingredient belongs to
    food_id: Mapped[int] = mapped_column(ForeignKey("foods.id"), nullable=False)
    food: Mapped[Food] = relationship(back_populates="ingredients")
    
    # The name of the ingredient (e.g., 'Flour', 'Sugar')
    ingredient_name: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self) -> str:
        return f"<Ingredient(id={self.id!r}, name={self.ingredient_name!r})>"


class DietRestrictAssoc(Base):
    """
    Association table for the many-to-many relationship
    between Food and DietaryRestriction.
    """
    __tablename__ = "diet_restrict_assoc"
    
    # Composite primary key
    food_id: Mapped[int] = mapped_column(ForeignKey("foods.id"), primary_key=True)
    restriction_id: Mapped[int] = mapped_column(ForeignKey("dietary_restrictions.id"), primary_key=True)

    # --- Relationships ---
    food: Mapped[Food] = relationship(back_populates="restriction_associations")
    restriction: Mapped[DietaryRestriction] = relationship(back_populates="food_associations")

    def __repr__(self) -> str:
        return f"<DietRestrictAssoc(food_id={self.food_id!r}, restriction_id={self.restriction_id!r})>"

