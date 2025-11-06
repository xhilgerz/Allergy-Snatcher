from flask import Flask
import os
from allergy_snatcher.models.database import db
from allergy_snatcher.routes.auth import init_app as auth_init_app
from flask_cors import CORS

def create_app() -> Flask:
    """Creates and configures the Flask app."""
    app = Flask(__name__, static_folder='../static', static_url_path='/')

    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)


    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD')
    db_host = os.environ.get('DB_HOST')
    db_port = os.environ.get('DB_PORT')
    db_name = os.environ.get('DB_NAME')
    

    if not all([db_user, db_password, db_host, db_port, db_name]):
        raise ValueError('One or more database environment variables are not set')

    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', None) # Change this in production
    if not app.config['SECRET_KEY']:
        raise ValueError('SECRET_KEY is not set')


    oauth_providers = {}

    # Google
    if 'OAUTH_GOOGLE_CLIENT_ID' in os.environ:
        oauth_providers['google'] = {
            'client_id': os.environ.get('OAUTH_GOOGLE_CLIENT_ID'),
            'client_secret': os.environ.get('OAUTH_GOOGLE_CLIENT_SECRET'),
            'server_metadata_url': 'https://accounts.google.com/.well-known/openid-configuration',
            'client_kwargs': {
                'scope': 'openid email profile'
            }
        }

    # GitHub
    if 'OAUTH_GITHUB_CLIENT_ID' in os.environ:
        oauth_providers['github'] = {
            'client_id': os.environ.get('OAUTH_GITHUB_CLIENT_ID'),
            'client_secret': os.environ.get('OAUTH_GITHUB_CLIENT_SECRET'),
            'api_base_url': 'https://api.github.com/',
            'userinfo_endpoint': 'https://api.github.com/user',
            'authorize_url': 'https://github.com/login/oauth/authorize',
            'access_token_url': 'https://github.com/login/oauth/access_token',
            'client_kwargs': {
                'scope': 'user:email'
            }
        }


    # Authentik
    if 'OAUTH_AUTHENTIK_CLIENT_ID' in os.environ:
        oauth_providers['authentik'] = {
            'client_id': os.environ.get('OAUTH_AUTHENTIK_CLIENT_ID'),
            'client_secret': os.environ.get('OAUTH_AUTHENTIK_CLIENT_SECRET'),
            'server_metadata_url': os.environ.get('OAUTH_AUTHENTIK_SERVER_METADATA_URL'),
            'client_kwargs': {
                'scope': 'openid email profile'
            }
        }

    app.config['OAUTH_PROVIDERS'] = oauth_providers

    db.init_app(app)
    auth_init_app(app)

    from allergy_snatcher.routes.endpoints import routes
    from allergy_snatcher.routes.auth import auth_bp
    app.register_blueprint(routes)
    app.register_blueprint(auth_bp)

    #CORS(app, origins=["http://localhost:3000"])

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        return app.send_static_file('index.html')

    with app.app_context():
        db.create_all()

    return app

# Create the app instance for Gunicorn to find
app = create_app()

if __name__ == "__main__":
    # This block is now just for local development (e.g., `python -m src.allergy_snatcher`)
    is_debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(debug=is_debug, host="0.0.0.0", port=5001)