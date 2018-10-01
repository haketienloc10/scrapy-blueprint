import json, os
from flask import Flask
from app.database import mongo
# from app.pet.views import api_v1_bp, PetResource
from app.crawler.views import api_crawl, AllResource
from app.json.views import api_json
from flask_cors import CORS
from app.schemas import CrawlSchema

# add logo
kwargs = {
    'x-logo': dict(
            url="https://rebilly.github.io/ReDoc/petstore-logo.png",
            backgroundColor="#FFFFFF",
            altText="Petstore logo"
        )
}

app = Flask(__name__)
# app configuration
app_settings = os.getenv(
    'APP_SETTINGS',
    'app.config'
)
# mongo.init_app(app)
app.config.from_object(app_settings)
# init mongo
mongo.init_app(app)
# allow CORS
CORS(app)

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec


# register Blueprint
app.register_blueprint(api_crawl, url_prefix='/api')
app.register_blueprint(api_json, url_prefix='/api')

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='pets',
        version='v1',
        info=dict(
            description='A minimal user API',
            **kwargs
        ),
        tags=[
            {
                "name": "crawl",
                "description": "Operations about crawl"
            },
        ],
    # openapi_version='3.0.1',
    plugins=[MarshmallowPlugin()],
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',
    'APISPEC_SWAGGER_UI_URL' : None
})
docs = FlaskApiSpec(app)

# app.add_url_rule('/pet/<name>', view_func=PetResource.as_view('PetResource'))
print(app.url_map._rules_by_endpoint)
'''
endpoint must equal as_view name 
e.g: PetResource.as_view('pet') => as_view name: pet == endpoint="pet"
'''
docs.spec.definition('User', schema=CrawlSchema)
docs.register(AllResource, blueprint="api_crawl", endpoint="crawl")
# docs.register(get_pets, blueprint="api_v1")