"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")
jackson_family.add_member(jackson_family.create_member("John", 33, [7, 13, 22]))
jackson_family.add_member(jackson_family.create_member("Jane", 35, [10, 14, 3]))
jackson_family.add_member(jackson_family.create_member("Jimmy", 5, [1]))

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():
    try:
        members = jackson_family.get_all_members()
        return jsonify(members), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500    



@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    try:
        member = jackson_family.get_member(member_id)
        if member is None:
            return jsonify({"error": "Member not found"}), 404
        return jsonify(member), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/member', methods=['POST'])
def add_new_member():
    body = request.get_json()

    if not body:
        return jsonify({"error": "El cuerpo del request está vacío"}), 400
    if "first_name" not in body or "age" not in body or "lucky_numbers" not in body:
        return jsonify({"error": "Faltan datos necesarios (first_name, age, lucky_numbers)"}), 400

    new_member = jackson_family.create_member(
        first_name=body["first_name"],
        age=body["age"],
        lucky_numbers=body["lucky_numbers"],
        id=body.get("id")  # ID es opcional, se genera automáticamente si no se pasa
    )

    jackson_family.add_member(new_member)

    return jsonify({"message": "Miembro agregado exitosamente", "member": new_member}), 200




@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    try:
        member = jackson_family.get_member(member_id)
        if member is None:
            return jsonify({"error": "Member not found"}), 404
        
        jackson_family.delete_member(member_id)
        return jsonify({"done": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500      








# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
