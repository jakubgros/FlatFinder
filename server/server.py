from flask import Flask, jsonify, request
from flask_api import status

from env_utils.base_dir import base_dir

app = Flask(__name__)

def get_flat_json(flat_id):
    with open(f"{base_dir}/temp/")


@app.route('/api/test', methods=['GET'])
def get_flat():
    args = request.args
    if 'flat_id' in args:
        flat_id=args['flat_id']
    else:
        raise Exception("flat_id parameter has to be provided")

    flat_json = get_flat_json(flat_id)

    return flat, status.HTTP_200_OK


def run_server():
    app.run(debug=True, port=5002)


if __name__ == '__main__':
    run_server()

