"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, Company, User, Facility, Separator, SeparatorInputDataFluid
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
    user1 = User(id="1", firstname="SuiOp", lastname="Soft", email="fran@gmail.com", password="suiop12345", company_id="1")
    facility1 = Facility(id="1", name="PDO Camp", location="Oman", company_id="1", user_id="1")
    separator1 = Separator(id="1", tag="v-3108", description="Separator V", facility_id="1")
    separatorDataFluid1 = SeparatorInputDataFluid(id="1", separator_id="1", operatingpressure="5536.33", operatingtemperature="37", oildensity="794.08", gasdensity="52.18", mixturedensity="197.76", waterdensity="1001", feedbsw="0.1", 
                                                    liquidviscosity="2.1065", gasviscosity="0.013385", gasmw="20.80", liqmw="155.53", gascomprz="0.8558", especificheatratio="1.4913", liquidsurfacetension="15.49", liquidvaporpressure="5536.3",
                                                    liquidcriticalpressure="12541.9", standardgasflow="25835.9", standardliquidflow="103.9", actualgasflow="435.5", actualliquidflow="106.33")
    db.session.add(company1)
    db.session.add(user1)
    db.session.add(facility1)
    db.session.add(separator1)
    db.session.add(separatorDataFluid1)
    db.session.commit()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200
## Companies resources ##
# Seleccionar todas las compañias
@api.route('/companies', methods=['GET'])
def handle_get_companies():

    companies_query = Company.query.all()
    all_companies = list(map(lambda x: x.serialize(), companies_query))
    return jsonify(all_companies), 200

# Seleccionar una compañia por name
@api.route('/companies/<string:company_name>', methods=['GET'])
def handle_get_company(company_name):

    #  user1 = Company.query.get(company_id)
    company_query = Company.query.filter_by(name=company_name)
    company = list(map(lambda x: x.serialize(), company_query))
    return jsonify(company), 200

## Users resources ##
# Seleccionar usuarios
@api.route('/users', methods=['GET'])
def handle_get_users():

    users_query = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users_query))
    return jsonify(all_users), 200

# Seleccionar un usuario por email
@api.route('/users/<string:user_email>', methods=['GET'])
def handle_get_user_by_email(user_email):

    #  user1 = Company.query.get(company_id)
    user_query = User.query.filter_by(email=user_email)
    user = list(map(lambda x: x.serialize(), user_query))
    return jsonify(user), 200

# Seleccionar usuarios por compañia
@api.route('/users/<int:company_id>', methods=['GET'])
def handle_get_user_by_company_id(company_id):

    #  user1 = Company.query.get(company_id)
    user_query = User.query.filter_by(company_id=company_id)
    user = list(map(lambda x: x.serialize(), user_query))
    return jsonify(user), 200

## Separators resources ##
# Seleccionar separadores
@api.route('/separators', methods=['GET'])
def handle_get_separators():

    separator_query = Separator.query.all()
    all_separators = list(map(lambda x: x.serialize(), separator_query))
    return jsonify(all_separators), 200

## Inputs resources ##
# Seleccionar inputs data fluids
@api.route('/datafluids', methods=['GET'])
def handle_get_data_fluids():

    data_fluids_query = SeparatorInputDataFluid.query.all()
    all_data_fluids = list(map(lambda x: x.serialize(), data_fluids_query))
    return jsonify(all_data_fluids), 200

# Insertar datos en  tabla data fluids
@api.route('/datafluids', methods=['POST'])
def handle_insert_data_fluids():
    datafluids = request.get_json()

    id = datafluids["id"]
    separator_id = datafluids["separator_id"]
    operatingpressure = datafluids["operatingpressure"]
    operatingtemperature = datafluids["operatingtemperature"]
    oildensity = datafluids["oildensity"]
    gasdensity = datafluids["gasdensity"]
    mixturedensity = datafluids["mixturedensity"]
    waterdensity = datafluids["waterdensity"]
    feedbsw = datafluids["feedbsw"]
    liquidviscosity = datafluids["liquidviscosity"]
    gasviscosity = datafluids["gasviscosity"]
    gasmw = datafluids["gasmw"]
    liqmw = datafluids["liqmw"]
    gascomprz = datafluids["gascomprz"]
    especificheatratio = datafluids["especificheatratio"]
    liquidsurfacetension = datafluids["liquidsurfacetension"]
    liquidvaporpressure = datafluids["liquidvaporpressure"]
    liquidcriticalpressure = datafluids["liquidcriticalpressure"]
    standardgasflow = datafluids["standardgasflow"]
    standardliquidflow = datafluids["standardliquidflow"]
    actualgasflow = datafluids["actualgasflow"]
    actualliquidflow = datafluids["actualliquidflow"]

    separatorDataFluid = SeparatorInputDataFluid(id=id, separator_id=separator_id, operatingpressure=operatingpressure, operatingtemperature=operatingtemperature, 
                                                    oildensity=oildensity, gasdensity=gasdensity, mixturedensity=mixturedensity, waterdensity=waterdensity, feedbsw=feedbsw, 
                                                    liquidviscosity=liquidviscosity, gasviscosity=gasviscosity, gasmw=gasmw, liqmw=liqmw, gascomprz=gascomprz, especificheatratio=especificheatratio, 
                                                    liquidsurfacetension=liquidsurfacetension, liquidvaporpressure=liquidvaporpressure, liquidcriticalpressure=liquidcriticalpressure, standardgasflow=standardgasflow, 
                                                    standardliquidflow=standardliquidflow, actualgasflow=actualgasflow, actualliquidflow=actualliquidflow)

    db.session.add(separatorDataFluid)
    db.session.commit()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200

# Insertar datos en  tabla data separators
@api.route('/dataseparators', methods=['POST'])
def handle_insert_data_separators():
    dataseparators = request.get_json()

    id = dataseparators["id"]
    separator_id = dataseparators["separator_id"]
    internaldiameter = dataseparators["internaldiameter"]
    ttlength = dataseparators["ttlength"]
    highlevelTrip = dataseparators["highlevelTrip"]
    highlevelalarm = dataseparators["highlevelalarm"]
    normalliquidlevel = dataseparators["normalliquidlevel"]
    lowlevelalarm = dataseparators["lowlevelalarm"]
    inletnozzle = dataseparators["inletnozzle"]
    gasoutletnozzle = dataseparators["gasoutletnozzle"]
    liquidoutletnozzle = dataseparators["liquidoutletnozzle"]
    inletdevicetype = dataseparators["inletdevicetype"]
    demistertype = dataseparators["demistertype"]


    separatorInputSeparators = SeparatorInputDataSeparator(id=id, separator_id=separator_id, internaldiameter=internaldiameter, ttlength=ttlength, 
                                                    highlevelTrip=highlevelTrip, highlevelalarm=highlevelalarm, normalliquidlevel=normalliquidlevel, lowlevelalarm=lowlevelalarm, inletnozzle=inletnozzle, 
                                                    gasoutletnozzle=gasoutletnozzle, liquidoutletnozzle=liquidoutletnozzle, inletdevicetype=inletdevicetype, demistertype=demistertype)

    db.session.add(separatorInputSeparators)
    db.session.commit()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200

# Insertar datos en  tabla data relief valve
@api.route('/datareliefvalve', methods=['POST'])
def handle_insert_data_relief_valve():
    datareliefvalve = request.get_json()

    id = datareliefvalve["id"]
    separator_id = datareliefvalve["separator_id"]
    rvtag = datareliefvalve["rvtag"]
    rvsetpressure = datareliefvalve["rvsetpressure"]
    rvorificearea = datareliefvalve["rvorificearea"]


    separatorReliefValve = SeparatorInputDataReliefValve(id=id, separator_id=separator_id, rvtag=rvtag, rvsetpressure=rvsetpressure, 
                                                    rvorificearea=rvorificearea)

    db.session.add(separatorReliefValve)
    db.session.commit()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200

# Insertar datos en  tabla data level control valve
@api.route('/datalevelcontrolvalve', methods=['POST'])
def handle_insert_data_level_control_valve():
    datalevelcontrolvalve = request.get_json()

    id = datalevelcontrolvalve["id"]
    separator_id = datalevelcontrolvalve["separator_id"]
    internaldiameter = datalevelcontrolvalve["lcvtag"]
    ttlength = datalevelcontrolvalve["lcvcv"]
    highlevelTrip = datalevelcontrolvalve["lcvdiameter"]
    highlevelalarm = datalevelcontrolvalve["inletlcvpipingdiameter"]
    normalliquidlevel = datalevelcontrolvalve["outletlcvpipingdiameter"]
    lowlevelalarm = datalevelcontrolvalve["lcvfactorfl"]
    inletnozzle = datalevelcontrolvalve["lcvfactorfi"]
    gasoutletnozzle = datalevelcontrolvalve["lcvfactorfp"]
    liquidoutletnozzle = datalevelcontrolvalve["lcvinletpressure"]
    inletdevicetype = datalevelcontrolvalve["lcvoutletpressure"]


    separatorLevelControlValve = SeparatorInputDataLevelControlValve(id=id, separator_id=separator_id, lcvtag=lcvtag, lcvcv=lcvcv, 
                                                    lcvdiameter=lcvdiameter, inletlcvpipingdiameter=inletlcvpipingdiameter, outletlcvpipingdiameter=outletlcvpipingdiameter, lcvfactorfl=lcvfactorfl, lcvfactorfi=lcvfactorfi, 
                                                    lcvfactorfp=lcvfactorfp, lcvinletpressure=lcvinletpressure, lcvoutletpressure=lcvoutletpressure)

    db.session.add(separatorLevelControlValve)
    db.session.commit()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200


# Seleccionar separadores por usuario
# Seleccionar inputs de separadores por usuario
# Seleccionar outputs de separadores por usuario

## Outputs resources ##