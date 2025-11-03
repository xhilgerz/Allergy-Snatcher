from flask import Flask
from allergy_snatcher.models.database import db
from allergy_snatcher.routes.auth import init_app as auth_init_app

def main() -> None:
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://myuser:mypassword@db:3306/mydatabase'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'supersecretkey' # Change this in production

    db.init_app(app)
    auth_init_app(app)

    from allergy_snatcher.routes.endpoints import routes
    from allergy_snatcher.routes.auth import auth_bp
    app.register_blueprint(routes)
    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()

    app.run(debug=True, host="0.0.0.0", port=5000)

if __name__ == "__main__":
    main()