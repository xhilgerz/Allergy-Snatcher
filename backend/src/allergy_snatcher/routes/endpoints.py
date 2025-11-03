from flask import Blueprint, jsonify
from ..models.database import Category, Cuisine
from ..models.http import CategorySchema, CuisineSchema


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

def init_app(app):
    app.register_blueprint(routes)