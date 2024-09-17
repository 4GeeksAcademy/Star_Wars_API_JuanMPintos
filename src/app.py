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
from models import db, User, Personajes, Planetas, Favoritos
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
    personaje= Personajes.query.get(id)
    return jsonify(personaje), 200

#OBTENER PLANETAS
@app.route("/planetas", methods=['GET'])
def planetas_list():
    planetas= Planetas.query.all()
    all_planetas=list(map(lambda x: x.serialize(), planetas))
    return jsonify(all_planetas), 200

#OBTENGO 1 PLANETA
@app.route("/planetas/<int:id>", methods=['GET'])
def planeta(id):
    planeta= Planetas.query.get(id)
    return jsonify(planeta), 200

#OBTENGO TODOS LOS USERS
@app.route("/users", methods=['GET'])
def users_list():
    users= User.query.all()
    all_users=list(map(lambda x: x.serialize(), users))
    return jsonify(all_users), 200

#OBTENGO 1 USER
@app.route("/users/<int:id>", method=['GET'])
def user_list(id):
    user= User.query.get(id)
    one_users=list(map(lambda x: x.serialize(), user))
    return jsonify(one_users), 200


# AGREGAR UN PLANETA A FAVORITOS

@app.route("/favoritos/planetas/<int:id>", methods=['POST'])
def agregar_planeta(id):
    planeta = Planetas.query.get(id)
    if not planeta:
        return jsonify({"error": "Planeta no encontrado"}), 400
    
    favorito_existente = Favoritos.query.filter_by(planet_id=id).first()
    if favorito_existente:
        return jsonify({"error": "El planeta ya está en la lista de favoritos"}), 400
    nuevo_favorito = Favoritos(planet_id=id)

    db.session.add(nuevo_favorito)
    db.session.commit()
    return jsonify({"message": f"El planeta {planeta.nombre} ha sido añadido a tus favoritos."}), 200

# AGREGAR 1 PERSONAJE A FAVORITOS

@app.route("/favoritos/personajes/<int:id>", methods=['POST'])
def agregar_personaje(id):




#ELIMINAR 1 PLANETA DE FAVORITOS

@app.route("/favoritos/planetas/<int:id>", methods=['DELETE'])
def eliminar_planeta(id):
    planeta = Planetas.query.get(id)
    db.session.delete(planeta)
    db.session.commit()


#ELIMINAR 1 PERSONAJE DE FAVORITOS

@app.route("/favoritos/personajes/<int:id>", methods=['DELETE'])
def eliminar_personaje(id):
    personaje = Personajes.query.get(id)
    db.session.delete(personaje)
    db.session.commit()

#OBTENER FAVORITOS
@app.route("/favoritos", method=['GET'])
def favoritos_list():
    favoritos= Favoritos.query.all()
    all_favoritos=list(map(lambda x: x.serialize(), favoritos))
    return jsonify(all_favoritos), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
