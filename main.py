from flask import Flask, request, jsonify
from filter import filterSpreadsheet
from flask_api import status

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_data():
    return jsonify({'message': 'Hello world'}), status.HTTP_200_OK


@app.route('/', methods=['POST'])
def post_data():
    data = request.get_json()

    # check if data is empty
    if not data:
        return (jsonify({'message': 'No data received'}), status.HTTP_400_BAD_REQUEST)

    # check if data has the correct keys
    if not all(key in data for key in ('uf', 'idade', 'parcela', 'soma_parcela', 'esp', 'banco_emp', 'banco_pgto')):
        return (jsonify({'message': 'Data has missing keys'}), status.HTTP_400_BAD_REQUEST)

    # Do something with the data
    result = filterSpreadsheet(data)
    
    if not result:
        return (jsonify({'message': 'No data found'}), status.HTTP_404_NOT_FOUND)
    
    return (jsonify(result), status.HTTP_200_OK)


if __name__ == '__main__':
    app.run()
