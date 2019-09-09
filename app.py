import os
import traceback
from flask import Flask, jsonify, request, Response
from flask_swagger_ui import get_swaggerui_blueprint

application = Flask(__name__)

### swagger specific ###
SWAGGER_URL = '/documentation'
API_URL = '/static/openapi.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "CARAMLService"
    }
)
application.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

@application.route('/', methods=['GET', 'POST'])
def welcome():
    response_text = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
        <title>CARA ML Service</title>
        <h2>Welcome to  !</h2>
        <p></p>"""
    return response_text

@application.route('/do_stuff', methods=['POST'])
def do_stuff():
    content = request.get_json(silent=True)
    try:
        # do something
        return jsonify(content), 200
    except Exception as e:
        tb = traceback.format_exc().split('\n')
        error_response = {
            "Request Status": "Failed",
            "Error": e.__class__.__name__,
            "Error Message": str(e),
            "stack_trace": "\n".join(tb)
        }
        return jsonify(error_response), 500

if __name__ == "__main__":
    application.run(host='0.0.0.0')
