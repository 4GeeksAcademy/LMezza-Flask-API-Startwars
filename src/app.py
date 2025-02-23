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
from models import db, User, People, Planets, Favs_planets, Favs_people
#from models import Person
from sqlalchemy.exc import NoResultFound

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

#Listar todos los user LISTO
@app.route('/user', methods=['GET'])
def get_all_users():

    data = db.session.scalars(db.select(User)).all()
    result = list(map(lambda item: item.serialize(),data))
    # print(result)

    if result == []:
        return jsonify({"msg":"user does not exists"}), 404

    response_body = {
        "results": result
    }

    return jsonify(response_body), 200


#Listar todos los favs de cada user LISTO
@app.route('/user_favs/<int:id>', methods=['GET'])
def favs_user(id):
    try:
        planets = list(db.session.execute(db.select(Favs_planets).filter_by(users_id=id)).scalars())
        people = list(db.session.execute(db.select(Favs_people).filter_by(users_id=id)).scalars())
        # print(planets)
        # print(people)
        result_planets = list(map(lambda item: item.serialize(), planets))
        #print (result_planets)
        result_people = list(map(lambda item: item.serialize(), people))
        #print (result_people)

        result = {
            "result_planets": result_planets, 
            "result_people": result_people
        }
        #print(results)

        return jsonify({"result": result}), 200
    except NoResultFound:
        return jsonify({"msg": "User does not exist"}), 404

#Listar todo de People LISTO
@app.route('/people', methods=['GET'])
def get_people():

    data = db.session.scalars(db.select(People)).all()
    result = list(map(lambda item: item.serialize(),data))
    # print(result)

    if result == []:
        return jsonify({"msg":"user does not exists"}), 404

    response_body = {
        "results": result
    }

    return jsonify(response_body), 200

#Listar a PEOPLE por ID LISTO
@app.route('/people/<int:id>', methods=['GET'])
def get_one_character(id):
    try:
        #print(id)
        people = db.session.execute(db.select(People).filter_by(id=id)).scalar_one()
    
        return jsonify({"result":people.serialize()}), 200
    except:
        return jsonify({"msg":"user do not exist"}), 404

#Listar todos los PLANETS LISTO
@app.route('/planets', methods=['GET'])
def get_planets():

    data = db.session.scalars(db.select(Planets)).all()
    result = list(map(lambda item: item.serialize(),data))
    #print(result)

    if result == []:
        return jsonify({"msg":"user does not exists"}), 404

    response_body = {
        "msg": "Hello, this is your GET /user response ",
        "results": result
    }

    return jsonify(response_body), 200

#Listar PLANETS por ID_USER LISTO
@app.route('/planets/<int:id>', methods=['GET'])
def get_one_planet(id):
    try:
        #print(id)
        planet = db.session.execute(db.select(Planets).filter_by(id=id)).scalar_one()
    
        return jsonify({"result":planet.serialize()}), 200
    except:
        return jsonify({"msg":"user do not exist"}), 404

#Crear un FAV_PLANET LISTO
@app.route('/favsplanets/<int:id>', methods=['POST'])
def post_fav_planet(id):
    body_data = request.json
    # print(body_data)
    # print(body_data["planet_id"])
    # print(id)
    try:
        favs_planets = db.session.execute(db.select(Favs_planets).filter_by(users_id=body_data["user_id"]).filter_by(planets_id=body_data["planet_id"])).scalar_one()

        return jsonify({"result":"Fav does not exit"}), 400
    except:
        favs_planets = Favs_planets(users_id=body_data["user_id"], planets_id=body_data["planet_id"])
        db.session.add(favs_planets)
        db.session.commit()
        #print(favs_planets.serialize())

        response_body = {
            "favs_planets": favs_planets.serialize()
        }

        return jsonify(response_body), 200

#Crear un FAV_PEOPLE LISTO
@app.route('/favspeople/<int:id>', methods=['POST'])
def post_fav_people(id):
    body_data = request.json
    print(body_data)
    print(body_data["people_id"])
    # print(id)
    try:
        favs_people = db.session.execute(db.select(Favs_people).filter_by(users_id=body_data["user_id"]).filter_by(people_id=body_data["people_id"])).scalar_one()

        return jsonify({"result":"ok"}), 400
    except:
        favs_people = Favs_people(users_id=body_data["user_id"], people_id=body_data["people_id"])
        db.session.add(favs_people)
        db.session.commit()
        print(favs_people.serialize())

        response_body = {
            "favs_people": favs_people.serialize()
        }

        return jsonify(response_body), 200

#Borrar PLANET usando ID_PLANET LISTO
@app.route('/favsplanets/<int:id>', methods=['DELETE'])
def delete_fav_planet(id):
    #print(id)
    try:
        user_query = db.session.execute(db.select(Favs_planets).filter_by(id=id)).scalar_one()
        db.session.delete(user_query)
        db.session.commit()
    

        return jsonify({"msg":"Planet fav delete"}), 200
    except:
       
        return jsonify({"msg":"user not exist"}), 404

#Borrar PEOPLE usando ID_PLEOPLE LISTO
@app.route('/favspeople/<int:id>', methods=['DELETE'])
def delete_fav_people(id):
    #print(id)
    try:
        user_query = db.session.execute(db.select(Favs_people).filter_by(id=id)).scalar_one()
        #print(user_query.serialize())
        db.session.delete(user_query)
        db.session.commit()
    

        return jsonify({"msg":"People fav delete"}), 200
    except:
       
        return jsonify({"msg":"user not exist"}), 404
    
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
