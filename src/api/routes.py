"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, Company, User
from api.utils import generate_sitemap, APIException

api = Blueprint('api', __name__)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend"
    }

    return jsonify(response_body), 200

# Rellenar tabla de companies
@api.route('/seedData', methods=['GET'])
def handle_data():

    company1 = Company(id="1", name="Shell", dateofstablish="1968", description="Petroleum Company", address="Holland")
    user1 = User(id="1", firstname="SuiOp", lastname="Soft", email="suiopsoft@gmail.com", password="suiop12345", company_id="1")
    db.session.add(company1)
    db.session.add(user1)
    db.session.commit()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200
## Companies resources ##
# Seleccionar todas las compañias
@api.route('/companies', methods=['GET'])
def handle_getCompanies():

    companies_query = Company.query.all()
    all_companies = list(map(lambda x: x.serialize(), companies_query))
    return jsonify(all_companies), 200

# Seleccionar una compañia por id
@api.route('/companies/<string:company_name>', methods=['GET'])
def handle_getCompany(company_name):

    #  user1 = Company.query.get(company_id)
    company_query = Company.query.filter_by(name=company_name)
    company = list(map(lambda x: x.serialize(), company_query))
    return jsonify(company), 200

## Users resources ##
# Seleccionar usuarios
@api.route('/users', methods=['GET'])
def handle_getUsers():

    users_query = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users_query))
    return jsonify(all_users), 200

# Seleccionar un usuario por email
@api.route('/users/<string:user_email>', methods=['GET'])
def handle_getUser(user_email):

    #  user1 = Company.query.get(company_id)
    user_query = User.query.filter_by(email=user_email)
    user = list(map(lambda x: x.serialize(), user_query))
    return jsonify(user), 200
# Seleccionar separadores por usuario
# Seleccionar inputs de separadores por usuario
# Seleccionar outputs de separadores por usuario