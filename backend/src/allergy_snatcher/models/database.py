"""
SQLAlchemy models for a user authentication and food tracking system, 
designed for MySQL 8.
"""

# Allows for forward-referencing type hints in relationships (e.g., Mapped["User"])
from __future__ import annotations
import datetime
from typing import List, Literal
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, DateTime, ForeignKey, UniqueConstraint, func, Float, Text
from sqlalchemy.dialects.mysql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class Base(db.Model):
    __abstract__ = True

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
    
    role: Mapped[Literal["admin","user"]] = mapped_column(ENUM("admin","user"), nullable=False, default="user")
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
    foods: Mapped[List[Food]] = relationship(
        back_populates="user"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id!r}, username={self.username!r})>"

# --- Password Model ---
class Password(Base):
    """
    Stores the user's hashed password in a separate table.
    """
    __tablename__ = "passwords"
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    user: Mapped[User] = relationship(back_populates="password")

    
    
    def __repr__(self) -> str:
        return f"<Password(user_id={self.user_id!r})>"

# --- OAuth Account Model ---
class OAuthAccount(Base):
    """
    Represents a link to an external OAuth provider (e.g., Google, GitHub).
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
    
    # UPDATED: Increased length for safety. Some tokens can be very long.
    # Alternatively, use `Text` if tokens exceed this.
    access_token: Mapped[str] = mapped_column(String(2048), nullable=True)
    refresh_token: Mapped[str] = mapped_column(String(2048), nullable=True)
    
    expires_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    
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
    
    session_token: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    expires_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False,
                                                           default=lambda: datetime.datetime.now() + 
                                                           datetime.timedelta(hours=1)) # default 1 hour from now
    
    refresh_token: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    refresh_token_expires_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False,
        default=lambda: datetime.datetime.now() + datetime.timedelta(days=30) # default 30 days from now
    )
    
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
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
    # Defines the publication status of the food item:
    # - 'public': Approved by an admin and publicly visible.
    # - 'private': Contributor is not ready to share; visible only to admins and the contributor.
    # - 'unlisting': Contributor has requested publication; pending admin review.
    publication_status: Mapped[Literal["public", "private", "unlisting"]] = mapped_column(
        ENUM("public", "private", "unlisting"), default="private", nullable=False
    )
    
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
    
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    user: Mapped[User | None] = relationship(back_populates="foods")
    
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
    category: Mapped[Category] = relationship(back_populates="foods")
    
    cuisine_id: Mapped[int | None] = mapped_column(ForeignKey("cuisines.id"), nullable=True)
    cuisine: Mapped[Cuisine | None] = relationship(back_populates="foods")

    ingredients: Mapped[List[Ingredient]] = relationship(
        back_populates="food", cascade="all, delete-orphan"
    )
    
    restriction_associations: Mapped[List[DietRestrictAssoc]] = relationship(
        back_populates="food", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Food(id={self.id!r}, name={self.name!r})>"

class Ingredient(Base):
    """
    Represents an ingredient for a food item.
    """
    __tablename__ = "ingredients"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    food_id: Mapped[int] = mapped_column(ForeignKey("foods.id"), nullable=False)
    food: Mapped[Food] = relationship(back_populates="ingredients")
    
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

    food: Mapped[Food] = relationship(back_populates="restriction_associations")
    restriction: Mapped[DietaryRestriction] = relationship(back_populates="food_associations")

    def __repr__(self) -> str:
        return f"<DietRestrictAssoc(food_id={self.food_id!r}, restriction_id={self.restriction_id!r})>"
