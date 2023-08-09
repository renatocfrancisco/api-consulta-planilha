from flask import Flask, request, jsonify, Response
from filter import filterSpreadsheet
from flask_api import status
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def get_data():
    return jsonify({'message': 'Hello world'}), status.HTTP_200_OK


@app.route('/', methods=['POST'])
def post_data():
    data = request.get_json()

    if not data:
        return (jsonify({'message': 'No data received'}), status.HTTP_400_BAD_REQUEST)

    if not all(key in data for key in ('uf', 'idadeMin', 'idadeMax', 'parcelaMin', 'parcelaMax', 'parcelasPagasMin', 'parcelasPagasMax', 'jurosMin', 'jurosMax', 'esp', 'banco_emp', 'banco_pgto')):
        return (jsonify({'message': 'Data has missing keys'}), status.HTTP_400_BAD_REQUEST)

    if not all(isinstance(data[key], int) for key in ('idadeMin', 'idadeMax', 'parcelaMin', 'parcelaMax', 'parcelasPagasMin', 'parcelasPagasMax', 'jurosMin', 'jurosMax')):
        return (jsonify({'message': 'Data has invalid values', 'data': data}), status.HTTP_400_BAD_REQUEST)

    if not all(isinstance(data[key], list) for key in ('uf', 'esp', 'banco_emp', 'banco_pgto')):
        return (jsonify({'message': 'Data has invalid values', 'data': data}), status.HTTP_400_BAD_REQUEST)

    result = filterSpreadsheet(data)

    if not result:
        return (jsonify({'message': 'No data found'}), status.HTTP_404_NOT_FOUND)

    if not isinstance(result, str):
        return (jsonify({'message': 'Internal server error'}), status.HTTP_500_INTERNAL_SERVER_ERROR)

    return (Response(
        result,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=data.csv'}
    ), status.HTTP_200_OK)


if __name__ == '__main__':
    app.run()
