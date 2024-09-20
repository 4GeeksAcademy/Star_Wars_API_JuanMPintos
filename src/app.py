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
from models import db, User, Personajes, Planetas, Personajes_favoritos, Planetas_favoritos
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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


#OBTENGO TODOS LOS PERSONAJES
@app.route("/personajes", methods=['GET'])
def personajes_list():
    personajes= Personajes.query.all()
    all_personajes=list(map(lambda x: x.serialize(), personajes))
    return jsonify(all_personajes), 200

#OBTENGO 1 PERSONAJE
@app.route("/personajes/<int:id>", methods=['GET'])
def personaje(id):
    personaje = Personajes.query.get(id)
    if not personaje:
        return jsonify({"error": "Personaje no encontrado"}), 400
    return jsonify(personaje.serialize()), 200

#OBTENER PLANETAS
@app.route("/planetas", methods=['GET'])
def planetas_list():
    planetas= Planetas.query.all()
    all_planetas=list(map(lambda x: x.serialize(), planetas))
    return jsonify(all_planetas), 200

#OBTENGO 1 PLANETA
@app.route("/planetas/<int:id>", methods=['GET'])
def planeta(id):
    planeta = Planetas.query.get(id)
    if not planeta:
        return jsonify({"error": "Planeta no encontrado"}), 400
    return jsonify(planeta.serialize()), 200

#OBTENGO TODOS LOS USERS
@app.route("/users", methods=['GET'])
def users_list():
    users= User.query.all()
    all_users=list(map(lambda x: x.serialize(), users))
    return jsonify(all_users), 200

#OBTENGO 1 USER
@app.route("/users/<int:id>", methods=['GET'])
def user_list(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 400
    return jsonify(user.serialize()), 200

#OBTENGO PLANETAS FAVORITOS

@app.route("/users/planetas_favoritos", methods=['GET'])
def obtener_planetas_favoritos():
    planetas_favoritos= Planetas_favoritos.query.all()
    all_planetas=list(map(lambda x: x.serialize(), planetas_favoritos))
    return jsonify(all_planetas), 200

#OBTENER PERSONAJES FAVORITOS

@app.route("/users/personajes_favoritos", methods=['GET'])
def obtener_personajes_favoritos():
    personajes_favoritos= Personajes_favoritos.query.all()
    all_personajes=list(map(lambda x: x.serialize(), personajes_favoritos))
    return jsonify(all_personajes), 200


#AGREGAR UN PLANETA A FAVORITOS

@app.route("/user/<int:user_id>/favoritos/planetas/<int:id>", methods=['POST'])
def agregar_planeta(user_id, id):
    planeta = Planetas.query.get(id)
    if not planeta:
        return jsonify({"error": "Planeta no encontrado"}), 404
    
    favorito_existente = Planetas_favoritos.query.filter_by(planeta_id=id, user_id=user_id).first()
    if favorito_existente:
        return jsonify({"error": "El planeta ya está en la lista de favoritos"}), 400
    
    nuevo_favorito = Planetas_favoritos(planeta_id=id, user_id=user_id)
    db.session.add(nuevo_favorito)
    db.session.commit()
    
    return jsonify({"message": f"El planeta {planeta.name} ha sido añadido a tus favoritos."}), 200

# AGREGAR 1 PERSONAJE A FAVORITOS
@app.route("/users/<int:user_id>/favoritos/personajes/<int:id>", methods=['POST'])
def agregar_personaje(user_id, id):
    personaje = Personajes.query.get(id)
    if not personaje:
        return jsonify({"error": "Personaje no encontrado"}), 404
    
    favorito_existente = Personajes_favoritos.query.filter_by(personaje_id=id, user_id=user_id).first()
    if favorito_existente:
        return jsonify({"error": "El personaje ya está en la lista de favoritos"}), 400
    
    nuevo_favorito = Personajes_favoritos(personaje_id=id, user_id=user_id)
    db.session.add(nuevo_favorito)
    db.session.commit()
    
    return jsonify({"message": f"El personaje {personaje.name} ha sido añadido a tus favoritos."}), 200


#ELIMINAR 1 PLANETA DE FAVORITOS

@app.route("/users/<int:user_id>/favoritos/planetas/<int:id>", methods=['DELETE'])
def eliminar_planeta(id):
    favorito = Planetas_favoritos.query.filter_by(planet_id=id).first()
    if not favorito:
        return jsonify({"error": "El favorito no existe"}), 404
    
    db.session.delete(favorito)
    db.session.commit()
    return jsonify({"message": "El planeta ha sido eliminado de favoritos."}), 200


 #ELIMINAR 1 PERSONAJE DE FAVORITOS

@app.route("/users/<int:user_id>/favoritos/personajes/<int:id>", methods=['DELETE'])
def eliminar_personaje(id):
    favorito = Personajes_favoritos.query.filter_by(personaje_id=id).first()
    if not favorito:
        return jsonify({"error": "El favorito no existe"}), 404
    
    db.session.delete(favorito)
    db.session.commit()
    return jsonify({"message": "El personaje ha sido eliminado de favoritos."}), 200





# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
