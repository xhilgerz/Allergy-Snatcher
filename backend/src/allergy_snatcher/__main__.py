from flask import Flask
from authlib.integrations.flask_client import OAuth



def main() -> None:
    app = Flask(__name__)
    oauth = OAuth(app)
    
     #app.config.from_object('allergy_snatcher.config.Config') 

    app.run(debug=True)

if __name__ == "__main__":
    main()