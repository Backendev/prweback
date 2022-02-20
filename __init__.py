from flask import Flask, request
from flask import render_template
import os,json



app = Flask(__name__)

_port = os.environ.get('PORT', 5000)

@app.route('/')
def index():
    data = {"a":"1234"}
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=_port)