from flask import Flask, Response, jsonify, request
from flask_api import status
from flask_cors import CORS

from filter import filterSpreadsheet

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def get_data():
    return jsonify({"message": "Hello world"}), status.HTTP_200_OK


@app.route("/", methods=["POST"])
def post_data():
    data = request.get_json()

    if not data:
        return (jsonify({"message": "No data received"}), status.HTTP_400_BAD_REQUEST)

    # insert 0 in empty integer fields
    for key in (
        "idadeMin",
        "idadeMax",
        "parcelaMin",
        "parcelaMax",
        "parcelasPagasMin",
        "parcelasPagasMax",
        "jurosMin",
        "jurosMax",
    ):
        if key not in data:
            data[key] = 0

    # check if all fields are not null
    if not all(
        key in data
        for key in (
            "uf",
            "idadeMin",
            "idadeMax",
            "parcelaMin",
            "parcelaMax",
            "parcelasPagasMin",
            "parcelasPagasMax",
            "jurosMin",
            "jurosMax",
            "esp",
            "banco_emp",
            "banco_pgto",
        )
    ):
        return (
            jsonify({"message": "Data has missing keys"}),
            status.HTTP_400_BAD_REQUEST,
        )

    # check if list fields are lists
    if not all(
        isinstance(uf, list)
        for uf in (data["uf"], data["esp"], data["banco_emp"], data["banco_pgto"])
    ):
        return (
            jsonify({"message": "Data has invalid values", "data": data}),
            status.HTTP_400_BAD_REQUEST,
        )

    # check if all integer fields are integers
    if not all(
        isinstance(data[key], int)
        for key in (
            "idadeMin",
            "idadeMax",
            "parcelaMin",
            "parcelaMax",
            "parcelasPagasMin",
            "parcelasPagasMax",
            "jurosMin",
            "jurosMax",
        )
    ):
        return (
            jsonify({"message": "Data has invalid values", "data": data}),
            status.HTTP_400_BAD_REQUEST,
        )

    # check if all values in uf are strings
    if not all(isinstance(uf, str) for uf in data["uf"]):
        return (
            jsonify({"message": "UF array has invalid values", "data": data}),
            status.HTTP_400_BAD_REQUEST,
        )

    special_strings_for_arrays = ["ALL"]
    for key in ("esp", "banco_emp", "banco_pgto"):
        for field in data[key]:
            if field in special_strings_for_arrays:
                break
            if not isinstance(field, int):
                return (
                    jsonify({"message": "Data has invalid values", "data": data}),
                    status.HTTP_400_BAD_REQUEST,
                )

    result = filterSpreadsheet(data)

    if not result:
        return (jsonify({"message": "No data found"}), status.HTTP_404_NOT_FOUND)

    if not isinstance(result, str):
        return (
            jsonify({"message": "Internal server error"}),
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    if len(result.splitlines()) == 1:
        return (jsonify({"message": "No data found"}), status.HTTP_404_NOT_FOUND)

    return (
        Response(
            result,
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment; filename=data.csv"},
        ),
        status.HTTP_200_OK,
    )


if __name__ == "__main__":
    app.run()
