from flask import Flask
from authlib.integrations.flask_client import OAuth



def main() -> None:
    app = Flask(__name__)
    oauth = OAuth(app)
    
     #app.config.from_object('allergy_snatcher.config.Config') 
    
    from allergy_snatcher.endpoints import routes
    app.register_blueprint(routes)
    app.run(debug=True, host="0.0.0.0", port=5000)

if __name__ == "__main__":
    main()