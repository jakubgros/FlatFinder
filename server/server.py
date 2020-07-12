from flask import Flask, request
from flask_api import status

from env_utils.base_dir import base_dir

app = Flask(__name__)

def get_flat_json(flat_id):
    try:
        with open(f"{base_dir}/temp/fetched_flats/{flat_id}.json", "r", encoding="UTF-8") as in_handle:
            flat = in_handle.readlines()
    except FileNotFoundError:
        return None
    else:
        return flat

@app.route('/api/flat', methods=['GET'])
def get_flat():
    args = request.args
    if 'flat_id' in args:
        flat_id=args['flat_id']
    else:
        raise Exception("flat_id parameter has to be provided")

    flat_json = get_flat_json(flat_id)
    return flat_json, status.HTTP_200_OK


def run_server():
    app.run(debug=True, port=5002)


if __name__ == '__main__':
    run_server()

