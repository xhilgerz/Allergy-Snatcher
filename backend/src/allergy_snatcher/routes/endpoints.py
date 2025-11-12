from flask import Blueprint, jsonify, request, g
from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from ..models.auth import require_session, require_role, require_force, optional_session
from ..models.database import Category, Cuisine, db, Food, Ingredient, DietaryRestriction, DietRestrictAssoc
from ..models.http import (
    CategorySchema, CuisineSchema, CreateCategorySchema, CreateCuisineSchema, 
    DietaryRestrictionSchema, CreateDietaryRestrictionSchema, FoodSchema, CreateFoodSchema, CreateIngredientSchema, UpdateFoodSchema
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

@routes.route("/api/diet-restrictions/", methods=['GET'])
def get_diet_restrictions():
    '''
    HTTP GET
        Returns a list of diet restrictions of food and their ID's from the database.
        Doesn't require authentication.
    '''
    
    diet_rest = DietaryRestriction.query.all()
    diet_rest_schemas = [DietaryRestrictionSchema.model_validate(dr).model_dump() for dr in diet_rest]
    return jsonify(diet_rest_schemas)



@routes.route("/api/foods/<int:limit>/<int:offset>/<string:showhidden>", methods=['GET'])
@optional_session
def get_foods(showhidden: str|bool, limit: int, offset: int):
    """
    HTTP GET
        Returns a list of food objects from the database. Gets list of all public foods, includes
        unlisting foods (if admin) and private foods (if owned by contributor). With admins, showprivate
        will show all private foods. Unauthenticated users will only receive public foods, regardless
        of the showhidden parameter.
        Doesn't require authentication.
    """
    try:
        showhidden = str(showhidden).lower() == 'true'
        query = Food.query.options(
            joinedload(Food.category),
            joinedload(Food.cuisine),
            joinedload(Food.restriction_associations).joinedload(DietRestrictAssoc.restriction)
        )

        ## had to comment out to test if foods are entering database correctly
        # if g.user and g.user.role == 'admin':
        #     if not showhidden:
        #         query = query.filter(Food.publication_status != 'private')
        # elif g.user:
        #     query = query.filter(
        #         or_(
        #             Food.publication_status == 'public',
        #             Food.user_id == g.user.id
        #         )
        #     )
        # else:
        #     query = query.filter(Food.publication_status == 'public')

        foods = query.limit(limit).offset(offset).all()
        food_schemas = [FoodSchema.model_validate(f).model_dump() for f in foods]
        return jsonify(food_schemas)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
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
        food = Food.query.options(
            joinedload(Food.category),
            joinedload(Food.cuisine),
            joinedload(Food.restriction_associations).joinedload(DietRestrictAssoc.restriction)
        ).get(food_id)

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

@routes.route("/api/foods/category/<int:category_id>/<int:limit>/<int:offset>/<string:showhidden>", methods=['GET'])
@optional_session
def get_food_by_category(category_id: int, limit: int, offset: int, showhidden: str|bool):
    """
        HTTP GET
            Returns list of food objects by category. (admins see unlisting and public by default, private based on parameters)
            Doesn't require authentication. If unauthenticated, returns all public foods.
            If authenticated, returns all food if admin, returns all public and private if contributor.
            Additional parameters include length of results and offsets (so not all results are returned at once enabling paging)
    """
    try:
        showhidden = showhidden.lower() == 'true'
        query = Food.query.options(
            joinedload(Food.category),
            joinedload(Food.cuisine),
            joinedload(Food.restriction_associations).joinedload(DietRestrictAssoc.restriction)
        ).filter_by(category_id=category_id)

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

@routes.route("/api/foods/cuisine/<int:cuisine_id>/<int:limit>/<int:offset>/<string:showhidden>", methods=['GET'])
@optional_session
def get_food_by_cuisine(cuisine_id: int, limit: int, offset: int, showhidden: str|bool):
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
        showhidden = showhidden.lower() == 'true'
        query = Food.query.options(
            joinedload(Food.category),
            joinedload(Food.cuisine),
            joinedload(Food.restriction_associations).joinedload(DietRestrictAssoc.restriction)
        ).filter_by(cuisine_id=cuisine_id)

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

@routes.route("/api/foods/diet-restriction/<int:restriction_id>/<int:limit>/<int:offset>/<string:showhidden>", methods=['GET'])
@optional_session
def get_food_by_diet_restriction(restriction_id: int, limit: int, offset: int, showhidden: str|bool):
    """
        HTTP GET
            Returns list of food objects by dietary restriction. (admins see unlisting and public by default, private based on parameters)
            Doesn't require authentication. If unauthenticated, returns all public foods.
            If authenticated, returns all food if admin, returns all public and private if contributor.
            Admins may list private foods that are not theirs with the showhidden parameter, this options
            has no effect if the user is not an admin.
            Additional parameters include length of results and offsets (so not all results are returned at once enabling paging)
    """
    try:
        showhidden = str(showhidden).lower() == 'true'
        query = Food.query.options(
            joinedload(Food.category),
            joinedload(Food.cuisine),
            joinedload(Food.restriction_associations).joinedload(DietRestrictAssoc.restriction)
        ).join(DietRestrictAssoc).filter(DietRestrictAssoc.restriction_id == restriction_id)

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
#@require_session
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
        # if not food:
        #     return jsonify({"error": "Food not found"}), 404

        # if g.user.role == 'admin':
        #     if food.publication_status == 'public' or food.user_id != g.user.id:
        #         if request.headers.get('confirmation') != 'force':
        #             return jsonify({"error": "Confirmation required to modify public/other users' data"}), 400
        # elif food.publication_status == 'public':
        #     return jsonify({"error": "Forbidden"}), 403
        # elif food.user_id != g.user.id:
        #     return jsonify({"error": "Forbidden"}), 403

        data = request.get_json()
        validated_data = UpdateFoodSchema(**data)

        for field, value in validated_data.model_dump(exclude_unset=True).items():
            if field == 'ingredients':
                food.ingredients = []
                for ingredient_data in value:
                    new_ingredient = Ingredient(ingredient_name=ingredient_data['ingredient_name'])
                    food.ingredients.append(new_ingredient)
            elif field == 'dietary_restriction_ids':
                food.restriction_associations = []
                for restriction_id in value:
                    assoc = DietRestrictAssoc(food_id=food.id, restriction_id=restriction_id)
                    food.restriction_associations.append(assoc)
            else:
                setattr(food, field, value)

        db.session.commit()

        return jsonify(FoodSchema.model_validate(food).model_dump())
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@routes.route("/api/foods/<int:food_id>", methods=['DELETE'])
#@require_session
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

    #     # Admin access logic
    #     if g.user.role == 'admin':
    #         if request.headers.get('confirmation') != 'force':
    #             return jsonify({"error": "Confirmation required for admin deletion"}), 400
        
    #     # Contributor (non-admin) access logic
    #     else:
    #         if food.publication_status == 'public':
    #             return jsonify({"error": "Forbidden: Contributors cannot delete public items"}), 403
    #         if food.user_id != g.user.id:
    #             return jsonify({"error": "Forbidden: You are not the owner of this item"}), 403
            
    #         # Force check for contributor deleting their own item
    #         if request.headers.get('confirmation') != 'force':
    #             return jsonify({"error": "Confirmation required to delete your own item"}), 400
        
        db.session.delete(food)
        db.session.commit()
        
        return jsonify({"message": "Food item deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@routes.route("/api/foods/", methods=['PUT'])
#@require_session
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

        for restriction_id in validated_data.dietary_restriction_ids:
            assoc = DietRestrictAssoc(food_id=new_food.id, restriction_id=restriction_id)
            new_food.restriction_associations.append(assoc)

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

@routes.route("/api/diet-restrictions/", methods=['POST'])
@require_role('admin')
def create_diet_restriction():
    """
    HTTP POST
        Insert new diet restriction object. Session auth required (admin only).
    """
    try:
        data = request.get_json()
        validated_data = CreateDietaryRestrictionSchema(**data)
        
        new_restriction = DietaryRestriction(restriction=validated_data.restriction)
        db.session.add(new_restriction)
        db.session.commit()
        
        return jsonify(DietaryRestrictionSchema.model_validate(new_restriction).model_dump()), 201
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

@routes.route("/api/diet-restrictions/<int:restriction_id>", methods=['DELETE'])
@require_role('admin')
def delete_diet_restriction_by_id(restriction_id):
    """
    HTTP DELETE
        Deletes dietary restriction object. No DB references to the restriction must exist before deleting. Session auth required (admin only).
    """
    try:
        restriction = DietaryRestriction.query.get(restriction_id)
        if not restriction:
            return jsonify({"error": "Dietary restriction not found"}), 404
        
        db.session.delete(restriction)
        db.session.commit()
        
        return jsonify({"message": "Dietary restriction deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400



def init_app(app):
    app.register_blueprint(routes)