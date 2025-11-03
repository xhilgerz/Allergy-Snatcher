from flask import Blueprint, jsonify, request, g
from sqlalchemy import or_
from ..models.auth import require_session, require_role, require_force, optional_session
from ..models.database import Category, Cuisine, db, Food, Ingredient
from ..models.http import (
    CategorySchema, CuisineSchema, CreateCategorySchema, CreateCuisineSchema, 
    FoodSchema, CreateFoodSchema, CreateIngredientSchema, UpdateFoodSchema
)


routes = Blueprint('routes', __name__)


@routes.route("/api/categories/", methods=['GET'])
def get_categories():
    '''
    HTTP GET
        Returns a list of categories of food  and their ID's from the database.
        Doesn't require authentication.
    '''
    
    categories = Category.query.all()
    category_schemas = [CategorySchema.model_validate(c).model_dump() for c in categories]
    return jsonify(category_schemas)

@routes.route("/api/cuisines/", methods=['GET'])
def get_cuisines():
    '''
    HTTP GET
        Returns a list of cuisines of food and their ID's from the database.
        Doesn't require authentication.
    '''
    
    cuisines = Cuisine.query.all()
    cuisine_schemas = [CuisineSchema.model_validate(c).model_dump() for c in cuisines]
    return jsonify(cuisine_schemas)

@routes.route("/api/foods/<int:food_id>", methods=['GET'])
@optional_session
def get_food_by_id(food_id):
    """
    HTTP GET
        Returns food object and its information from the database.
        Doesn't require authentication if food is public, otherwise, requires
        authentication from either contributor or admin.
    """
    try:
        food = Food.query.get(food_id)

        if not food:
            return jsonify({"error": "Food not found"}), 404

        is_public = food.publication_status == 'public'
        is_admin = g.user and g.user.role == 'admin'
        is_owner = g.user and food.user_id == g.user.id

        if is_public or is_admin or is_owner:
            return jsonify(FoodSchema.model_validate(food).model_dump())
        else:
            # Return 404 to conceal the existence of the resource from unauthorized users
            return jsonify({"error": "Food not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@routes.route("/api/foods/category/<int:category_id>/<int:limit>/<int:offset>/<bool:showhidden>", methods=['GET'])
@optional_session
def get_food_by_category(category_id: int, limit: int, offset: int, showhidden: bool):
    """
        HTTP GET
            Returns list of food objects by category. (admins see unlisting and public by default, private based on parameters)
            Doesn't require authentication. If unauthenticated, returns all public foods.
            If authenticated, returns all food if admin, returns all public and private if contributor.
            Additional parameters include length of results and offsets (so not all results are returned at once enabling paging)
    """
    try:
        query = Food.query.filter_by(category_id=category_id)

        if g.user and g.user.role == 'admin':
            if not showhidden:
                # Admin sees public, unlisting, and their own private foods by default
                query = query.filter(
                    or_(
                        Food.publication_status != 'private',
                        Food.user_id == g.user.id
                    )
                )
            # if showhidden is True, admin sees all, so no filter is applied
        elif g.user:
            # Authenticated user (contributor) sees public food and their own private/unlisting food
            query = query.filter(
                or_(
                    Food.publication_status == 'public',
                    Food.user_id == g.user.id
                )
            )
        else:
            # Unauthenticated user sees only public food
            query = query.filter(Food.publication_status == 'public')

        foods = query.limit(limit).offset(offset).all()
        food_schemas = [FoodSchema.model_validate(f).model_dump() for f in foods]
        return jsonify(food_schemas)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@routes.route("/api/foods/cuisine/<int:cuisine_id>/<int:limit>/<int:offset>/<bool:showhidden>", methods=['GET'])
@optional_session
def get_food_by_cuisine(cuisine_id: int, limit: int, offset: int, showhidden: bool):
    """
        HTTP GET
            Returns list of food objects by cuisine. (admins see unlisting and public by default, private based on parameters)
            Doesn't require authentication. If unauthenticated, returns all public foods.
            If authenticated, returns all food if admin, returns all public and private if contributor.
            Admins may list private foods that are not theirs with the showhidden parameter, this options
            has no effect if the user is not an admin.
            Additional parameters include length of results and offsets (so not all results are returned at once enabling paging)
    """
    try:
        query = Food.query.filter_by(cuisine_id=cuisine_id)

        if g.user and g.user.role == 'admin':
            if not showhidden:
                # Admin sees public, unlisting, and their own private foods by default
                query = query.filter(
                    or_(
                        Food.publication_status != 'private',
                        Food.user_id == g.user.id
                    )
                )
            # if showhidden is True, admin sees all, so no filter is applied
        elif g.user:
            # Authenticated user (contributor) sees public food and their own private/unlisting food
            query = query.filter(
                or_(
                    Food.publication_status == 'public',
                    Food.user_id == g.user.id
                )
            )
        else:
            # Unauthenticated user sees only public food
            query = query.filter(Food.publication_status == 'public')

        foods = query.limit(limit).offset(offset).all()
        food_schemas = [FoodSchema.model_validate(f).model_dump() for f in foods]
        return jsonify(food_schemas)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@routes.route("/api/foods/<int:food_id>", methods=['PATCH'])
@require_session
def update_food_by_id(food_id):
    """
        HTTP PATCH
            Update attributes of Food object with new information. Food object must already exist
            if the food object is public, then only an admin can update. If the food object is private, then
            only the contributor can update. If the food object is unlisting, then only an admin can update and publish, but
            the contributor can still update or mark as private. Authentication with sessions is required.
            When admin is updating food that is published or food that is not their own, then the admin must pass a force
            parameter to confirm their change.
    """
    try:
        food = Food.query.get(food_id)
        if not food:
            return jsonify({"error": "Food not found"}), 404

        if g.user.role == 'admin':
            if food.publication_status == 'public' or food.user_id != g.user.id:
                require_force()
        elif food.publication_status == 'public':
            return jsonify({"error": "Forbidden"}), 403
        elif food.user_id != g.user.id:
            return jsonify({"error": "Forbidden"}), 403

        data = request.get_json()
        validated_data = UpdateFoodSchema(**data)

        for field, value in validated_data.model_dump(exclude_unset=True).items():
            if field == 'ingredients':
                food.ingredients = []
                for ingredient_data in value:
                    new_ingredient = Ingredient(ingredient_name=ingredient_data['ingredient_name'])
                    food.ingredients.append(new_ingredient)
            else:
                setattr(food, field, value)

        db.session.commit()

        return jsonify(FoodSchema.model_validate(food).model_dump())
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@routes.route("/api/foods/<int:food_id>", methods=['DELETE'])
@require_session
def delete_food_by_id(food_id):
    """
        HTTP DELETE
            Deletes food object. If food is private or unlisting, then the contributer and admin can delete
            (use a force parameter to confirm). If food is public, only admin can delete. Session auth required.
    """
    try:
        food = Food.query.get(food_id)
        if not food:
            return jsonify({"error": "Food not found"}), 404

        if g.user.role == 'admin':
            require_force()
        elif food.publication_status == 'public':
            return jsonify({"error": "Forbidden"}), 403
        elif food.user_id != g.user.id:
            return jsonify({"error": "Forbidden"}), 403
        
        db.session.delete(food)
        db.session.commit()
        
        return jsonify({"message": "Food item deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@routes.route("/api/foods/", methods=['PUT'])
@require_session
def create_food():
    """
    HTTP PUT
        Insert new food object, food object is required to be private on first creation. Session auth required.
    """
    try:
        data = request.get_json()
        validated_data = CreateFoodSchema(**data)
        validated_data.publication_status = 'private'
        new_food = Food(
            name=validated_data.name,
            brand=validated_data.brand,
            publication_status=validated_data.publication_status,
            dietary_fiber=validated_data.dietary_fiber,
            sugars=validated_data.sugars,
            protein=validated_data.protein,
            carbs=validated_data.carbs,
            cal=validated_data.cal,
            cholesterol=validated_data.cholesterol,
            sodium=validated_data.sodium,
            trans_fats=validated_data.trans_fats,
            total_fats=validated_data.total_fats,
            sat_fats=validated_data.sat_fats,
            serving_amt=validated_data.serving_amt,
            serving_unit=validated_data.serving_unit,
            category_id=validated_data.category_id,
            cuisine_id=validated_data.cuisine_id
        )

        for ingredient_data in validated_data.ingredients:
            new_ingredient = Ingredient(ingredient_name=ingredient_data.ingredient_name)
            new_food.ingredients.append(new_ingredient)

        db.session.add(new_food)
        db.session.commit()
        
        return jsonify(FoodSchema.model_validate(new_food).model_dump()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@routes.route("/api/categories/", methods=['POST'])
@require_role('admin')
def create_category():
    """
    HTTP POST
        Insert new category object. Session auth required (admin only).
    """
    try:
        data = request.get_json()
        validated_data = CreateCategorySchema(**data)
        
        new_category = Category(category=validated_data.category)
        db.session.add(new_category)
        db.session.commit()
        
        return jsonify(CategorySchema.model_validate(new_category).model_dump()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@routes.route("/api/cuisines/", methods=['POST'])
@require_role('admin')
def create_cuisine():
    """
    HTTP POST
        Insert new cuisine object. Session auth required (admin only
    """
    try:
        data = request.get_json()
        validated_data = CreateCuisineSchema(**data)
        
        new_cuisine = Cuisine(cuisine=validated_data.cuisine)
        db.session.add(new_cuisine)
        db.session.commit()
        
        return jsonify(CuisineSchema.model_validate(new_cuisine).model_dump()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@routes.route("/api/categories/<int:category_id>", methods=['DELETE'])
@require_role('admin')
def delete_category_by_id(category_id):
    """
    HTTP DELETE
        Deletes category object. No DB references to category must exist before deleting. Session auth required (admin only).
    """
    try:
        category = Category.query.get(category_id)
        if not category:
            return jsonify({"error": "Category not found"}), 404
        
        db.session.delete(category)
        db.session.commit()
        
        return jsonify({"message": "Category deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@routes.route("/api/cuisines/<int:cuisine_id>", methods=['DELETE'])
@require_role('admin')
def delete_cuisine_by_id(cuisine_id):
    """
    HTTP DELETE
        Deletes cuisine object. NO DB references to cuisine must exist before deleting. Session auth required (admin only).
    """
    try:
        cuisine = Cuisine.query.get(cuisine_id)
        if not cuisine:
            return jsonify({"error": "Cuisine not found"}), 404
        
        db.session.delete(cuisine)
        db.session.commit()
        
        return jsonify({"message": "Cuisine deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400



def init_app(app):
    app.register_blueprint(routes)