"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, Company, User, Facility, Separator, SeparatorInputDataFluid, SeparatorInputDataSeparator, SeparatorInputDataReliefValve, SeparatorOutputGasAndLiquidAreas, SeparatorOutputInletNozzleParameters, SeparatorInputDataLevelControlValve
from api.utils import generate_sitemap, APIException
from api.calculations.separators.gasAndLiquidAreas import gas_and_liquid_areas_calc
from api.calculations.separators.inletNozzleParameters import inlet_nozzle_parameters_calc
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

api = Blueprint('api', __name__)

# Creación de token
@api.route("/signIn", methods=["POST"])
def sign_in():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(email=email).one_or_none()
    if not user or not user.check_password(password):
        return jsonify("Wrong email or password"), 401

    # Notice that we are passing in the actual sqlalchemy user object here
    access_token = create_access_token(identity=user.serialize())
    return jsonify(access_token=access_token)

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

# Actualizar datos en tabla datafluids
@api.route('/datafluids', methods=['PUT'])
def handle_update_data_fluids():
    datafluids = request.get_json()
    datafluid = SeparatorInputDataFluid.query.get(datafluids["id"])

    datafluid.id = datafluids["id"]
    datafluid.separator_id = datafluids["separator_id"]
    datafluid.operatingpressure = datafluids["operatingpressure"]
    datafluid.operatingtemperature = datafluids["operatingtemperature"]
    datafluid.oildensity = datafluids["oildensity"]
    datafluid.gasdensity = datafluids["gasdensity"]
    datafluid.mixturedensity = datafluids["mixturedensity"]
    datafluid.waterdensity = datafluids["waterdensity"]
    datafluid.feedbsw = datafluids["feedbsw"]
    datafluid.liquidviscosity = datafluids["liquidviscosity"]
    datafluid.gasviscosity = datafluids["gasviscosity"]
    datafluid.gasmw = datafluids["gasmw"]
    datafluid.liqmw = datafluids["liqmw"]
    datafluid.gascomprz = datafluids["gascomprz"]
    datafluid.especificheatratio = datafluids["especificheatratio"]
    datafluid.liquidsurfacetension = datafluids["liquidsurfacetension"]
    datafluid.liquidvaporpressure = datafluids["liquidvaporpressure"]
    datafluid.liquidcriticalpressure = datafluids["liquidcriticalpressure"]
    datafluid.standardgasflow = datafluids["standardgasflow"]
    datafluid.standardliquidflow = datafluids["standardliquidflow"]
    datafluid.actualgasflow = datafluids["actualgasflow"]
    datafluid.actualliquidflow = datafluids["actualliquidflow"]

    # separatorDataFluid = SeparatorInputDataFluid(id=id, separator_id=separator_id, operatingpressure=operatingpressure, operatingtemperature=operatingtemperature, 
    #                                                 oildensity=oildensity, gasdensity=gasdensity, mixturedensity=mixturedensity, waterdensity=waterdensity, feedbsw=feedbsw, 
    #                                                 liquidviscosity=liquidviscosity, gasviscosity=gasviscosity, gasmw=gasmw, liqmw=liqmw, gascomprz=gascomprz, especificheatratio=especificheatratio, 
    #                                                 liquidsurfacetension=liquidsurfacetension, liquidvaporpressure=liquidvaporpressure, liquidcriticalpressure=liquidcriticalpressure, standardgasflow=standardgasflow, 
    #                                                 standardliquidflow=standardliquidflow, actualgasflow=actualgasflow, actualliquidflow=actualliquidflow)

    # db.session.add(separatorDataFluid)
    db.session.commit()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200

# Seleccionar inputs data fluids
@api.route('/dataseparators', methods=['GET'])
def handle_get_data_separators():

    data_separators_query = SeparatorInputDataSeparator.query.all()
    all_data_separators = list(map(lambda x: x.serialize(), data_separators_query))
    return jsonify(all_data_separators), 200

# Insertar datos en  tabla data separators
@api.route('/dataseparators', methods=['POST'])
def handle_insert_data_separators():
    dataseparators = request.get_json()

    id = dataseparators["id"]
    separator_id = dataseparators["separator_id"]
    internaldiameter = dataseparators["internaldiameter"]
    ttlength = dataseparators["ttlength"]
    highleveltrip = dataseparators["highleveltrip"]
    highlevelalarm = dataseparators["highlevelalarm"]
    normalliquidlevel = dataseparators["normalliquidlevel"]
    lowlevelalarm = dataseparators["lowlevelalarm"]
    inletnozzle = dataseparators["inletnozzle"]
    gasoutletnozzle = dataseparators["gasoutletnozzle"]
    liquidoutletnozzle = dataseparators["liquidoutletnozzle"]
    inletdevicetype = dataseparators["inletdevicetype"]
    demistertype = dataseparators["demistertype"]


    separatorInputSeparators = SeparatorInputDataSeparator(id=id, separator_id=separator_id, internaldiameter=internaldiameter, ttlength=ttlength, 
                                                    highleveltrip=highleveltrip, highlevelalarm=highlevelalarm, normalliquidlevel=normalliquidlevel, lowlevelalarm=lowlevelalarm, inletnozzle=inletnozzle, 
                                                    gasoutletnozzle=gasoutletnozzle, liquidoutletnozzle=liquidoutletnozzle, inletdevicetype=inletdevicetype, demistertype=demistertype)

    db.session.add(separatorInputSeparators)
    db.session.commit()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200

# Actualizar datos en  tabla data separators
@api.route('/dataseparators', methods=['PUT'])
def handle_update_data_separators():
    dataseparators = request.get_json()
    dataseparator = SeparatorInputDataSeparator.query.get(dataseparators["id"])

    dataseparator.id = dataseparators["id"]
    dataseparator.separator_id = dataseparators["separator_id"]
    dataseparator.internaldiameter = dataseparators["internaldiameter"]
    dataseparator.ttlength = dataseparators["ttlength"]
    dataseparator.highleveltrip = dataseparators["highleveltrip"]
    dataseparator.highlevelalarm = dataseparators["highlevelalarm"]
    dataseparator.normalliquidlevel = dataseparators["normalliquidlevel"]
    dataseparator.lowlevelalarm = dataseparators["lowlevelalarm"]
    dataseparator.inletnozzle = dataseparators["inletnozzle"]
    dataseparator.gasoutletnozzle = dataseparators["gasoutletnozzle"]
    dataseparator.liquidoutletnozzle = dataseparators["liquidoutletnozzle"]
    dataseparator.inletdevicetype = dataseparators["inletdevicetype"]
    dataseparator.demistertype = dataseparators["demistertype"]


    # separatorInputSeparators = SeparatorInputDataSeparator(id=id, separator_id=separator_id, internaldiameter=internaldiameter, ttlength=ttlength, 
    #                                                 highleveltrip=highleveltrip, highlevelalarm=highlevelalarm, normalliquidlevel=normalliquidlevel, lowlevelalarm=lowlevelalarm, inletnozzle=inletnozzle, 
    #                                                 gasoutletnozzle=gasoutletnozzle, liquidoutletnozzle=liquidoutletnozzle, inletdevicetype=inletdevicetype, demistertype=demistertype)

    db.session.commit()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200

# Seleccionar inputs data fluids
@api.route('/datareliefvalve', methods=['GET'])
def handle_get_data_relief_valve():

    data_reliefvalve_query = SeparatorInputDataReliefValve.query.all()
    all_data_reliefvalve = list(map(lambda x: x.serialize(), data_reliefvalve_query))
    return jsonify(all_data_reliefvalve), 200

# Insertar datos en  tabla data relief valve
@api.route('/datareliefvalve', methods=['POST'])
def handle_insert_data_relief_valve():
    datareliefvalves = request.get_json()

    id = datareliefvalves["id"]
    separator_id = datareliefvalves["separator_id"]
    rvtag = datareliefvalves["rvtag"]
    rvsetpressure = datareliefvalves["rvsetpressure"]
    rvorificearea = datareliefvalves["rvorificearea"]


    separatorReliefValve = SeparatorInputDataReliefValve(id=id, separator_id=separator_id, rvtag=rvtag, rvsetpressure=rvsetpressure, 
                                                    rvorificearea=rvorificearea)

    db.session.add(separatorReliefValve)
    db.session.commit()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200

# Actualizar datos en  tabla data relief valve
@api.route('/datareliefvalve', methods=['PUT'])
def handle_update_data_relief_valve():
    datareliefvalves = request.get_json()
    datareliefvalve = SeparatorInputDataReliefValve.query.get(datareliefvalves["id"])

    datareliefvalve.id = datareliefvalves["id"]
    datareliefvalve.separator_id = datareliefvalves["separator_id"]
    datareliefvalve.rvtag = datareliefvalves["rvtag"]
    datareliefvalve.rvsetpressure = datareliefvalves["rvsetpressure"]
    datareliefvalve.rvorificearea = datareliefvalves["rvorificearea"]


    # separatorReliefValve = SeparatorInputDataReliefValve(id=id, separator_id=separator_id, rvtag=rvtag, rvsetpressure=rvsetpressure, 
    #                                                 rvorificearea=rvorificearea)

    db.session.commit()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200

# Seleccionar inputs data fluids
@api.route('/datalevelcontrolvalve', methods=['GET'])
def handle_get_data_level_control_valve():

    data_levelcontrolvalve_query = SeparatorInputDataLevelControlValve.query.all()
    all_data_levelcontrolvalve = list(map(lambda x: x.serialize(), data_levelcontrolvalve_query))
    return jsonify(all_data_levelcontrolvalve), 200

# Insertar datos en  tabla data level control valve
@api.route('/datalevelcontrolvalve', methods=['POST'])
def handle_insert_data_level_control_valve():
    datalevelcontrolvalves = request.get_json()

    id = datalevelcontrolvalves["id"]
    separator_id = datalevelcontrolvalves["separator_id"]
    internaldiameter = datalevelcontrolvalves["lcvtag"]
    ttlength = datalevelcontrolvalves["lcvcv"]
    highleveltrip = datalevelcontrolvalves["lcvdiameter"]
    highlevelalarm = datalevelcontrolvalves["inletlcvpipingdiameter"]
    normalliquidlevel = datalevelcontrolvalves["outletlcvpipingdiameter"]
    lowlevelalarm = datalevelcontrolvalves["lcvfactorfl"]
    inletnozzle = datalevelcontrolvalves["lcvfactorfi"]
    gasoutletnozzle = datalevelcontrolvalves["lcvfactorfp"]
    liquidoutletnozzle = datalevelcontrolvalves["lcvinletpressure"]
    inletdevicetype = datalevelcontrolvalves["lcvoutletpressure"]


    separatorLevelControlValve = SeparatorInputDataLevelControlValve(id=id, separator_id=separator_id, lcvtag=lcvtag, lcvcv=lcvcv, 
                                                    lcvdiameter=lcvdiameter, inletlcvpipingdiameter=inletlcvpipingdiameter, outletlcvpipingdiameter=outletlcvpipingdiameter, lcvfactorfl=lcvfactorfl, lcvfactorfi=lcvfactorfi, 
                                                    lcvfactorfp=lcvfactorfp, lcvinletpressure=lcvinletpressure, lcvoutletpressure=lcvoutletpressure)

    db.session.add(separatorLevelControlValve)
    db.session.commit()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200

# Insertar datos en  tabla data level control valve
@api.route('/datalevelcontrolvalve', methods=['PUT'])
def handle_update_data_level_control_valve():
    datalevelcontrolvalves = request.get_json()
    datalevelcontrolvalve = SeparatorInputDataLevelControlValve.query.get(dataseparators["id"])

    datalevelcontrolvalve.id = datalevelcontrolvalves["id"]
    datalevelcontrolvalve.separator_id = datalevelcontrolvalves["separator_id"]
    datalevelcontrolvalve.internaldiameter = datalevelcontrolvalves["lcvtag"]
    datalevelcontrolvalve.ttlength = datalevelcontrolvalves["lcvcv"]
    datalevelcontrolvalve.highleveltrip = datalevelcontrolvalves["lcvdiameter"]
    datalevelcontrolvalve.highlevelalarm = datalevelcontrolvalves["inletlcvpipingdiameter"]
    datalevelcontrolvalve.normalliquidlevel = datalevelcontrolvalves["outletlcvpipingdiameter"]
    datalevelcontrolvalve.lowlevelalarm = datalevelcontrolvalves["lcvfactorfl"]
    datalevelcontrolvalve.inletnozzle = datalevelcontrolvalves["lcvfactorfi"]
    datalevelcontrolvalve.gasoutletnozzle = datalevelcontrolvalves["lcvfactorfp"]
    datalevelcontrolvalve.liquidoutletnozzle = datalevelcontrolvalves["lcvinletpressure"]
    datalevelcontrolvalve.inletdevicetype = datalevelcontrolvalves["lcvoutletpressure"]


    # separatorLevelControlValve = SeparatorInputDataLevelControlValve(id=id, separator_id=separator_id, lcvtag=lcvtag, lcvcv=lcvcv, 
    #                                                 lcvdiameter=lcvdiameter, inletlcvpipingdiameter=inletlcvpipingdiameter, outletlcvpipingdiameter=outletlcvpipingdiameter, lcvfactorfl=lcvfactorfl, lcvfactorfi=lcvfactorfi, 
    #                                                 lcvfactorfp=lcvfactorfp, lcvinletpressure=lcvinletpressure, lcvoutletpressure=lcvoutletpressure)

    db.session.commit()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200


# Seleccionar separadores por usuario
# Seleccionar inputs de separadores por usuario
# Seleccionar outputs de separadores por usuario

## Outputs resources ##
## Calcular SeparatorOutputGasAndLiquidAreas
@api.route('/gasandliquidareascalc', methods=['POST'])
def handle_calc_gas_liquid_areas():

    gas_and_liquid_areas_calc()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200


# Seleccionar SeparatorOutputGasAndLiquidAreas
@api.route('/gasandliquidareascalc', methods=['GET'])
def handle_get_gas_liquid_areas():

    gas_liquid_query = SeparatorOutputGasAndLiquidAreas.query.all()
    all_gas_liquid = list(map(lambda x: x.serialize(), gas_liquid_query))
    return jsonify(all_gas_liquid), 200


## Calcular SeparatorOutputInletNozzleParameters
@api.route('/inletnozzleparameterscalc', methods=['POST'])
def handle_calc_inlet_nozzle_parameters():

    inlet_nozzle_parameters_calc()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200

# Seleccionar SeparatorOutputInletNozzleParameters
@api.route('/inletnozzleparameterscalc', methods=['GET'])
def handle_get_inlet_nozzle_parameters():

    inlet_nozzle_query = SeparatorOutputInletNozzleParameters.query.all()
    all_inlet_nozzle = list(map(lambda x: x.serialize(), inlet_nozzle_query))
    return jsonify(all_inlet_nozzle), 200

