"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Usuario,Planeta,Personajes,Favoritos
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
jwt = JWTManager(app)
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people', methods=['GET'])
def get_all_people():
    query = Personajes.query.all()

    # map the results and your list of people  inside of the all_people variable
    results = list(map(lambda personaje: personaje.serialize(), query))
    response_body = {
        "message": results
    }

    return jsonify(response_body), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_one_single_people(people_id):
    
    query = Personajes.query.get(people_id)

    # map the results and your list of people  inside of the all_people variable
    results = query.serialize()
    
    response_body = {
        "message": results
    }

    return jsonify(response_body), 200

@app.route('/planets', methods=['GET'])
def get_all_planets():
    query = Planeta.query.all()

    # map the results and your list of people  inside of the all_people variable
    results = list(map(lambda Planeta: Planeta.serialize(), query))
    response_body = {
        "message": results
    }

    return jsonify(response_body), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_one_single_planet(planet_id):
    
    query = Planeta.query.get(planet_id)

    # map the results and your list of people  inside of the all_people variable
    results = query.serialize()
    
    response_body = {
        "message": results
    }

    return jsonify(response_body), 200

@app.route('/users', methods=['GET'])
def get_all_users():
    query = Usuario.query.all()

    # map the results and your list of people  inside of the all_people variable
    results = list(map(lambda usuario: usuario.serialize(), query))
    response_body = {
        "message": results
    }

    return jsonify(response_body), 200

@app.route('/users/favorites', methods=['GET'])
@jwt_required()
def get_all_favoritos_id():
    
    user_id = get_jwt_identity()

    favoritos_ID = Favoritos.query.filter_by(usuario_id=user_id)
    # map the results and your list of people  inside of the all_people variable
    results = list(map(lambda fab_id: fab_id.serialize(), favoritos_ID))
    print (results)
    for result in results:
        if result.get("planeta_id") == None:
            query_personajes = Personajes.query.get(result.get("personajes_id"))
            print (query_personajes,"querypersonajes")
            print (result,"resultados")
            result["nombre"] = query_personajes.serialize().get("nombre")
        else:
            query_planetas = Planeta.query.get(result.get("planeta_id"))
            result["nombre"] = query_planetas.serialize().get("nombre")
    response_body = {
        "message": results
    }

    return jsonify(response_body), 200


@app.route('/users/favorites', methods=['POST'])
@jwt_required()
def agrega_favorito():
    user_id = get_jwt_identity()
    # recibir info del request
    request_favorito = request.get_json()
    print(request_favorito)
    nuevo_favorito = Favoritos(usuario_id=user_id,planeta_id=request_favorito.get("planeta_id"),personajes_id=request_favorito.get("personajes_id"))
    
    db.session.add(nuevo_favorito)
    db.session.commit()

    return jsonify("favorito agregado satisfactoriamente"), 200

@app.route('/favorite/<int:favorite_id>', methods=['DELETE'])
@jwt_required()
def borra_favorito(favorite_id):
    
    user_id = get_jwt_identity()

    borra_favorito = Favoritos.query.get(favorite_id)
    
         
    if borra_favorito is None:
        raise APIException('Favorite not found', status_code=404)
    
    if  borra_favorito.serialize().get("usuario_id")!=user_id:
        raise APIException('Usuario no autorizado', status_code=404)

    db.session.delete(borra_favorito)

    db.session.commit()

    return jsonify("Favorito borrado satisfactoriamente"), 200

@app.route('/register', methods=["POST"])
def register():
    if request.method == 'POST':
       
        email = request.json.get("email", None)
        password = request.json.get("password", None)
        nombre= request.json.get("nombre", None)
        primer_apellido = request.json.get("primer_apellido", None)
        segundo_apellido = request.json.get("segundo_apellido", None)

        if not email:
            return jsonify({"msg": "email requerido"}), 400
        if not password:
            return jsonify({"msg": "Password requerido"}), 400

        if not nombre:
            return jsonify({"msg": "Nombre requerido"}), 400

        if not primer_apellido:
            return jsonify({"msg": "Primer Apellido requerido"}), 400

        if not segundo_apellido:
            return jsonify({"msg": "Segundo Apellido requerido"}), 400


        user = Usuario.query.filter_by(email=email).first()
        if user:
            return jsonify({"msg": "Username  already exists"}), 400

        user = Usuario()
        user.email = email
        user.nombre = nombre
        user.primer_apellido = primer_apellido
        user.segundo_apellido = segundo_apellido



        hashed_password = generate_password_hash(password)
       
        user.password = hashed_password

        db.session.add(user)
        db.session.commit()

        return jsonify({"success": "Thanks. your register was successfully", "status": "true"}), 200

@app.route('/login', methods=['POST'])
def login():

    if request.method == 'POST':
        email = request.json.get("email", None)
        password = request.json.get("password", None)

        if not email:
            return jsonify({"msg": "Username is required"}), 400
        if not password:
            return jsonify({"msg": "Password is required"}), 400

        user = Usuario.query.filter_by(email=email).first()
        if not user:
            return jsonify({"msg": "Username/Password are incorrect"}), 401

        if not check_password_hash(user.password, password):
            return jsonify({"msg": "Username/Password are incorrect"}), 401

        # crear el token
        expiracion = datetime.timedelta(days=3)
        access_token = create_access_token(identity=user.id, expires_delta=expiracion)

        data = {
            "user": user.serialize(),
            "token": access_token,
            "expires": expiracion.total_seconds()*1000
        }
        return jsonify(data), 200

# @app.route("/logout", methods=["DELETE"])
# @jwt_required()
# def logout():
#     jti = get_jwt()["jti"]
#     jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
#     return jsonify(msg="Access token revoked")

# A blocklisted access token will not be able to access this any more
# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
