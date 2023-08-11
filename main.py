from flask import Flask, request, jsonify, Response
from filter import filterSpreadsheet
from flask_api import status
from flask_cors import CORS

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

    for key in ("uf", "esp", "banco_emp", "banco_pgto"):
        if key not in data or data[key] == []:
            return jsonify({"message": "Missing arrays"}), status.HTTP_400_BAD_REQUEST

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

    if not all(isinstance(uf, str) for uf in data["uf"]):
        return (
            jsonify({"message": "UF array has invalid values", "data": data}),
            status.HTTP_400_BAD_REQUEST,
        )

    for key in ("esp", "banco_emp", "banco_pgto"):
        if not isinstance(data[key], list) or not all(
            isinstance(uf, int) for uf in data[key]
        ):
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
