from flask import Flask, jsonify, request
from flask_cors import CORS

from pet.pet_dataset import PetDataset

app = Flask(__name__)
CORS(app)

pet = PetDataset()


@app.route("/document", methods=["GET"])
def get_document():
    document_name = request.args.get("document_name")
    document = pet.get_document_by_name(document_name)
    if document:
        return jsonify(document.to_json())
    else:
        return (
            jsonify({"error": "Document not found"}),
            404,
        )


def start_server():
    app.run(host="127.0.0.1", port=8000, debug=True)


if __name__ == "__main__":
    start_server()
