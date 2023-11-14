import os
import connexion
from flask_injector import FlaskInjector
from connexion.resolver import RestyResolver
from providers.MongoProvider import MongoProvider
from injector import Binder
from flask_cors import CORS

from connexion.exceptions import OAuthProblem

API_KEY = os.environ.get('API_KEY')
TOKEN_SERVICE = {API_KEY: {"uid": 100}}



def apikey_auth(token, required_scopes):
    info = TOKEN_SERVICE.get(token, None)

    if not info:
        raise OAuthProblem("Invalid token")

    return info

def configure(binder: Binder) -> Binder:
    binder.bind(
        MongoProvider
    )


if __name__ == '__main__':
    
    # Provide the app and the directory of the docs
    app = connexion.App(__name__, specification_dir='swagger/') 
    
    
    CORS(app.app)
    app.add_api('email-service-docs.yaml', resolver=RestyResolver('api'))
    FlaskInjector(app=app.app, modules=[configure])
    
    # Allow requests through port 20 20
    app.run(port=int(os.environ.get('PORT', 2020)))  