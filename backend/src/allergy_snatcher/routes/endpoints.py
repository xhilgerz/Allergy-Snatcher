from flask import Flask, Blueprint, jsonify


routes = Blueprint('routes', __name__)


@routes.route("/api/categories/", methods=['GET'])
def get_categories():

    # Todo: Get categories from database

    return jsonify(["Sample", "Glutten-free"])