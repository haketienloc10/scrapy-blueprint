from flask import Blueprint, request, jsonify, send_file
from flask_apispec import MethodResource

api_json = Blueprint('api_json', __name__)


class OpenAPIJSON(MethodResource):
    def get(self):
        try:
            return send_file('../v2-petstore.json', attachment_filename='../v2-petstore.json')
        except Exception as e:
            return str(e)


api_json.add_url_rule('/json', view_func=OpenAPIJSON.as_view('json'))
