from flask import Flask
import os
from allergy_snatcher.models.database import db
from allergy_snatcher.routes.auth import init_app as auth_init_app

def main() -> None:
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://myuser:mypassword@db:3306/mydatabase'
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

    with app.app_context():
        db.create_all()

    app.run(debug=True, host="0.0.0.0", port=5000)

if __name__ == "__main__":
    main()