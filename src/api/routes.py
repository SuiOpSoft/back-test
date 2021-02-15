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
    db.session.add(company1)
    db.session.commit()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200

# Seleccionar todas las compañias
@api.route('/companies', methods=['GET'])
def handle_getCompanies():

    companies_query = Company.query.all()
    all_companies = list(map(lambda x: x.serialize(), companies_query))
    return jsonify(all_companies), 200

# Seleccionar una compañia por id
@api.route('/companies/<int:company_name>', methods=['GET'])
def handle_getCompany(company_id):

    #  user1 = Company.query.get(company_id)
    company_query = Company.query.filter_by(name=company_id)
    all_companies = list(map(lambda x: x.serialize(), companies_query))
    return jsonify(all_companies), 200


    # companies_query = Company.query.all()
    # all_companies = list(map(lambda x: x.serialize(), companies_query))
    # return jsonify(all_companies), 200
# Seleccionar usuarios
# Seleccionar un usuario por id