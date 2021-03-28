"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, Company, User, Facility, Separator, SeparatorInputDataFluid, SeparatorInputDataSeparator, SeparatorInputDataReliefValve,SeparatorInputDataLevelControlValve, SeparatorOutputGasAndLiquidAreas, SeparatorOutputInletNozzleParameters, SeparatorOutputGasNozzleParameters, SeparatorOutputLiquidNozzleParameters, SeparatorOutputVesselGasCapacityParameters, SeparatorOutputVesselLiquidCapacityParameters, SeparatorOutputReliefValveParameters, SeparatorOutputLevelControlValveParameters
from api.utils import generate_sitemap, APIException
from api.calculations.separators.gasAndLiquidAreas import gas_and_liquid_areas_calc
from api.calculations.separators.inletNozzleParameters import inlet_nozzle_parameters_calc
from api.calculations.separators.gasNozzle import gas_nozzle_calc
from api.calculations.separators.liquidNozzle import liquid_nozzle_calc
from api.calculations.separators.vesselGasCapacity import vessel_gas_capacity_calc
from api.calculations.separators.vesselLiquidCapacity import vessel_liquid_capacity_calc
from api.calculations.separators.reliefValve import relief_valve_calc
from api.calculations.separators.levelControlValve import level_control_calc
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

api = Blueprint('api', __name__)

# Creación de token User
@api.route("/signInUser", methods=["POST"])
def sign_in():
    email = request.json.get("email", None)
    passwordUser = request.json.get("passwordUser", None)

    user = User.query.filter_by(email=email).one_or_none()
    if not user or not user.check_password(passwordUser):
        return jsonify("Wrong email or password"), 401

    # Notice that we are passing in the actual sqlalchemy user object here
    access_token = create_access_token(identity=user.serialize())
    return jsonify(access_token=access_token)

# Creación de token Company
@api.route("/signInCompany", methods=["POST"])
def sign_in_company():
    companyUser = request.json.get("companyUser", None)
    passwordCompany = request.json.get("passwordCompany", None)

    company = Company.query.filter_by(companyuser=companyUser).one_or_none()
    if not company or not company.check_password(passwordCompany):
        return jsonify("Wrong company user or password"), 401

    # Notice that we are passing in the actual sqlalchemy user object here
    access_token = create_access_token(identity=company.serialize())
    return jsonify(access_token_company=access_token)


# Rellenar tabla de companies
@api.route('/seedData', methods=['GET'])
def handle_data():

    company1 = Company(id="1", name="Shell", dateofstablish="1968", description="Petroleum Company", address="Holland", companyuser="ShellUx", password="123456")
    user1 = User(id="1", firstname="SuiOp", lastname="Soft", email="fran@gmail.com", password="suiop12345", company_id="1")
    facility1 = Facility(id="1", name="PDO Camp", location="Oman", company_id="1", facilitycode="ShellLagoon")
    separator1 = Separator(tag="v-3108", description="Separator V", facility_id="1")
    separatorDataFluid1 = SeparatorInputDataFluid(separator_tag="v-3108", operatingpressure=5536.33, operatingtemperature=37, oildensity=794.08, gasdensity=52.18, mixturedensity=197.76, waterdensity=1001, feedbsw=0.1, 
                                                    liquidviscosity=2.1065, gasviscosity=0.013385, gasmw=20.80, liqmw=155.53, gascomprz=0.8558, especificheatratio=1.4913, liquidsurfacetension=15.49, liquidvaporpressure=5536.3,
                                                    liquidcriticalpressure=12541.9, standardgasflow=25835.9, standardliquidflow=103.9, actualgasflow=435.5, actualliquidflow=106.33, kcp=1.49)
    
    separatorLevelControlValve1 = SeparatorInputDataLevelControlValve(separator_tag="v-3108", lcvtag="lcv-2021", lcvcv=47, 
                                                    lcvdiameter=5536.33, inletlcvpipingdiameter=5536.33, outletlcvpipingdiameter=5536.33, lcvfactorfl=0.9, 
                                                    lcvfactorfp=0.92, lcvinletpressure=5336.325, lcvoutletpressure=2286.325)

    separatorDataReliefValve1 = SeparatorInputDataReliefValve(separator_tag="v-3108", rvtag="rv-450", rvsetpressure=7900, 
                                                    rvorificearea=0.785)

    separatorInputSeparators1 = SeparatorInputDataSeparator(separator_tag="v-3108", internaldiameter=1800, ttlength=6300, 
                                                    highleveltrip=1080, highlevelalarm=900, normalliquidlevel=650, lowlevelalarm=390, inletnozzle=203.2, 
                                                    gasoutletnozzle=152.4, liquidoutletnozzle=203.2, inletdevicetype="SP", demistertype="VD")

    db.session.add(company1)
    db.session.add(user1)
    db.session.add(facility1)
    db.session.add(separator1)
    db.session.add(separatorDataFluid1)          
    db.session.add(separatorLevelControlValve1)
    db.session.add(separatorDataReliefValve1)
    db.session.add(separatorInputSeparators1)
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
@api.route('/companies/<string:company_user>', methods=['GET'])
def handle_get_company(company_user):

    #  user1 = Company.query.get(company_id)
    company_query = Company.query.filter_by(companyuser=company_user)
    company = list(map(lambda x: x.serialize(), company_query))
    return jsonify(company), 200

# Seleccionar una compañia por id
@api.route('/companies/<int:company_id>', methods=['GET'])
def handle_get_company_by_id(company_id):

    #  user1 = Company.query.get(company_id)
    company_query = Company.query.filter_by(id=company_id)
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

# Insertar usuario
@api.route('/users', methods=['POST'])
def handle_insert_user():
    user = request.get_json()
    print(user)

    ## User params
    company_id = user["company_id"]
    email = user["email"]

    ## Cración del usario en la tabla users
    user = User(firstname="-", lastname="-", email=email, password="-", company_id=company_id)

    db.session.add(user)
    db.session.commit()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200

# Actualizar usuario
@api.route('/users', methods=['PUT'])
def handle_update_data_users():
    users = request.get_json()
    user = User.query.filter_by(email = users["email"]).first()

    user.email = users["email"]
    user.firstname = users["firstname"]
    user.lastname = users["lastname"]
    user.password = users["password"]

    db.session.add(user)
    db.session.commit()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200


# Eliminar Usuarios
@api.route('/users', methods=['DELETE'])
def handle_delete_data_users():
    users = request.get_json()
    user = User.query.filter_by(email = users["email"]).first()
    
    db.session.delete(user)
    db.session.commit()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200

## Facilities resources ##
# Seleccionar separadores
@api.route('/facilities/<int:company_id>', methods=['GET'])
def handle_get_facilities_by_company_id(company_id):

    facility_query = Facility.query.filter_by(company_id=company_id)
    facility = list(map(lambda x: x.serialize(), facility_query))
    return jsonify(facility), 200

# Insertar facility
@api.route('/facilities', methods=['POST'])
def handle_insert_facility():
    facility = request.get_json()
    print(facility)

    ## Facility params
    company_id = facility["company_id"]
    facilitycode = facility["facilitycode"]

    ## Cración del usario en la tabla facilities
    facility = Facility(facilitycode=facilitycode, name="-", location="-", company_id=company_id)

    db.session.add(facility)
    db.session.commit()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200

#Delete facility
@api.route('/facilities', methods=['DELETE'])
def handle_delete_data_facilities():
    facilities = request.get_json()
    facility = Facility.query.filter_by(facilitycode = facilities ["facilitycode"]).first()
    
    db.session.delete(facility)
    db.session.commit()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200

# Actualizar facility
@api.route('/facilities', methods=['PUT'])
def handle_update_data_facilities():
    facilities = request.get_json()
    facility = Facility.query.filter_by(facilitycode = facilities["facilitycode"]).first()

    facility.facilitycode = facilities["facilitycode"]
    facility.name = facilities["name"]
    facility.location = facilities["location"]

    db.session.add(facility)
    db.session.commit()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200

## Separators resources ##
# Seleccionar separadores
@api.route('/separators', methods=['GET'])
def handle_get_separators():

    separator_query = Separator.query.all()
    all_separators = list(map(lambda x: x.serialize(), separator_query))
    return jsonify(all_separators), 200

# Insertar separador
@api.route('/separators', methods=['POST'])
def handle_insert_separator():
    separator = request.get_json()
    print(separator)

    ## Separator params
    separator_tag = separator["tag"]
    facility_id = separator["facility_id"] ## Falta coger la facility del front (Escogerla en la pantalla del usuario)

    ## Cración del separador en la tabla separators
    separator = Separator(tag=separator_tag, facility_id=facility_id)

    ## Inputs 
    separatorDataFluid = SeparatorInputDataFluid(separator_tag=separator_tag, operatingpressure=0, operatingtemperature=0, 
                                                    oildensity=0, gasdensity=0, mixturedensity=0, waterdensity=0, feedbsw=0, 
                                                    liquidviscosity=0, gasviscosity=0, gasmw=0, liqmw=0, gascomprz=0, especificheatratio=0, 
                                                    liquidsurfacetension=0, liquidvaporpressure=0, liquidcriticalpressure=0, standardgasflow=0, 
                                                    standardliquidflow=0, actualgasflow=0, actualliquidflow=0, kcp=0)

    separatorLevelControlValve = SeparatorInputDataLevelControlValve(separator_tag=separator_tag, lcvtag='-', lcvcv=0, 
                                                    lcvdiameter=0, inletlcvpipingdiameter=0, outletlcvpipingdiameter=0, lcvfactorfl=0, 
                                                    lcvfactorfp=0, lcvinletpressure=0, lcvoutletpressure=0)

    separatorDataReliefValve = SeparatorInputDataReliefValve(separator_tag=separator_tag, rvtag=0, rvsetpressure=0, 
                                                    rvorificearea=0)
    
    separatorInputSeparators = SeparatorInputDataSeparator(separator_tag=separator_tag, internaldiameter=0, ttlength=0, 
                                                    highleveltrip=0, highlevelalarm=0, normalliquidlevel=0, lowlevelalarm=0, inletnozzle=0, 
                                                    gasoutletnozzle=0, liquidoutletnozzle=0, inletdevicetype='-', demistertype='-')


    db.session.add(separator)
    db.session.add(separatorDataFluid)
    db.session.add(separatorLevelControlValve)
    db.session.add(separatorDataReliefValve)
    db.session.add(separatorInputSeparators)
    db.session.commit()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200


## Inputs resources ##
# Eliminar datos en tabla datafluids
@api.route('/datafluids', methods=['DELETE'])
def handle_delete_data_fluids():
    datafluids = request.get_json()
    datafluid = SeparatorInputDataFluid.query.filter_by(separator_tag = datafluids["separator_tag"]).first()
    separator = Separator.query.filter_by(tag = datafluids["separator_tag"]).first()
    datalevelcontrolvalve = SeparatorInputDataLevelControlValve.query.filter_by(separator_tag = datafluids["separator_tag"]).first()
    datareliefvalve = SeparatorInputDataReliefValve.query.filter_by(separator_tag = datafluids["separator_tag"]).first()
    dataseparator = SeparatorInputDataSeparator.query.filter_by(separator_tag = datafluids["separator_tag"]).first()

    datafluid.separator_tag = datafluids["separator_tag"]
    dataseparator.separator_tag = datafluids["separator_tag"]
    datalevelcontrolvalve.separator_tag = datafluids["separator_tag"]
    datareliefvalve.separator_tag = datafluids["separator_tag"]
    separator.tag = datafluids["separator_tag"]

    db.session.delete(datafluid)
    db.session.delete(dataseparator)
    db.session.delete(datalevelcontrolvalve)
    db.session.delete(datareliefvalve)
    db.session.delete(separator)
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
    dataseparator = SeparatorInputDataSeparator.query.filter_by(separator_tag = dataseparators["separator_tag"]).first()

    dataseparator.separator_tag = dataseparators["separator_tag"]
    dataseparator.internaldiameter = dataseparators["internaldiameter"]
    if dataseparator.internaldiameter == '' or float(dataseparator.internaldiameter) == 0:
        return jsonify("Empty Internal Diameter param."), 401
    if float(dataseparator.internaldiameter) != 0 and float(dataseparator.internaldiameter) < 100 or float(dataseparator.internaldiameter) > 5000:
        return jsonify("Invalid Internal Diameter param. (Min. 100 - Max. 5000)"), 401

    dataseparator.ttlength = dataseparators["ttlength"]
    if dataseparator.ttlength == '' or float(dataseparator.ttlength) == 0:
        return jsonify("Empty T-T Length param."), 401
    if float(dataseparator.ttlength) != 0 and float(dataseparator.ttlength) < 100 or float(dataseparator.ttlength) > 10000:
        return jsonify("Invalid T-T Length param. (Min. 100 - Max. 10000)"), 401

    dataseparator.highleveltrip = dataseparators["highleveltrip"]
    if dataseparator.highleveltrip == '' or float(dataseparator.highleveltrip) == 0:
        return jsonify("Empty High Level Trip param."), 401
    if float(dataseparator.highleveltrip) != 0 and float(dataseparator.highleveltrip) < 100 or float(dataseparator.highleveltrip) > 5000:
        return jsonify("Invalid High Level Trip param. (Min. 100 - Max. 5000)"), 401

    dataseparator.highlevelalarm = dataseparators["highlevelalarm"]
    if dataseparator.highlevelalarm == '' or float(dataseparator.highlevelalarm) == 0:
        return jsonify("Empty High Level Alarm param."), 401
    if float(dataseparator.highlevelalarm) != 0 and float(dataseparator.highlevelalarm) < 100 or float(dataseparator.highlevelalarm) > 5000:
        return jsonify("Invalid High Level Alarm param. (Min. 100 - Max. 5000)"), 401

    dataseparator.normalliquidlevel = dataseparators["normalliquidlevel"]
    if dataseparator.normalliquidlevel == '' or float(dataseparator.normalliquidlevel) == 0:
        return jsonify("Empty Normal Liquid Level param."), 401
    if float(dataseparator.normalliquidlevel) != 0 and float(dataseparator.normalliquidlevel) < 100 or float(dataseparator.normalliquidlevel) > 5000:
        return jsonify("Invalid Normal Liquid Level param. (Min. 100 - Max. 5000)"), 401

    dataseparator.lowlevelalarm = dataseparators["lowlevelalarm"]
    if dataseparator.lowlevelalarm == '' or float(dataseparator.lowlevelalarm) == 0:
        return jsonify("Empty Low Level Alarm param."), 401
    if float(dataseparator.lowlevelalarm) != 0 and float(dataseparator.lowlevelalarm) < 100 or float(dataseparator.lowlevelalarm) > 5000:
        return jsonify("Invalid Low Level Alarm param. (Min. 100 - Max. 5000)"), 401

    dataseparator.inletnozzle = dataseparators["inletnozzle"]
    if dataseparator.inletnozzle == '' or float(dataseparator.inletnozzle) == 0:
        return jsonify("Empty Inlet Nozzle param."), 401
    if float(dataseparator.inletnozzle) != 0 and float(dataseparator.inletnozzle) < 50 or float(dataseparator.inletnozzle) > 1300:
        return jsonify("Invalid Inlet Nozzle param. (Min. 50 - Max. 1300)"), 401

    dataseparator.gasoutletnozzle = dataseparators["gasoutletnozzle"]
    if dataseparator.gasoutletnozzle == '' or float(dataseparator.gasoutletnozzle) == 0:
        return jsonify("Empty Gas Outlet Nozzle param."), 401
    if float(dataseparator.gasoutletnozzle) != 0 and float(dataseparator.gasoutletnozzle) < 50 or float(dataseparator.gasoutletnozzle) > 1300:
        return jsonify("Invalid Gas Outlet Nozzle param. (Min. 50 - Max. 1300)"), 401

    dataseparator.liquidoutletnozzle = dataseparators["liquidoutletnozzle"]
    if dataseparator.liquidoutletnozzle == '' or float(dataseparator.liquidoutletnozzle) == 0:
        return jsonify("Empty Liquid Outlet Nozzle param."), 401
    if float(dataseparator.liquidoutletnozzle) != 0 and float(dataseparator.liquidoutletnozzle) < 50 or float(dataseparator.liquidoutletnozzle) > 1300:
        return jsonify("invalid Liquid Outlet Nozzle param. (Min. 50 - Max. 1300)"), 401

    dataseparator.inletdevicetype = dataseparators["inletdevicetype"]
    if dataseparator.inletdevicetype == '' or dataseparator.inletdevicetype == '-':
        return jsonify("Empty Inlet Device Type param."), 401
    if dataseparator.inletdevicetype != 'SP' and dataseparator.inletdevicetype != 'NID' and dataseparator.inletdevicetype != 'HOP':
        return jsonify("Invalid Inlet Device Type param. (SP, NID or HOP)"), 401

    dataseparator.demistertype = dataseparators["demistertype"]
    if dataseparator.demistertype == '' or dataseparator.demistertype == '-':
        return jsonify("Empty Demister Type param."), 401
    if dataseparator.demistertype != 'KO' and dataseparator.demistertype != 'VD' and dataseparator.demistertype != 'HD' and dataseparator.demistertype != 'HVD':
        return jsonify("Invalid Demister Type param. (KO, VD, HD or HVD)"), 401


    db.session.add(dataseparator)
    db.session.commit()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200

# Eliminar datos en tabla datafluids
@api.route('/dataseparators', methods=['DELETE'])
def handle_delete_data_separators():
    dataseparators = request.get_json()
    dataseparator = SeparatorInputDataSeparator.query.filter_by(separator_tag = dataseparators["separator_tag"]).first()
    separator = Separator.query.filter_by(tag = dataseparators["separator_tag"]).first()
    datafluid = SeparatorInputDataFluid.query.filter_by(separator_tag = dataseparators["separator_tag"]).first()
    datalevelcontrolvalve = SeparatorInputDataLevelControlValve.query.filter_by(separator_tag = dataseparators["separator_tag"]).first()
    datareliefvalve = SeparatorInputDataReliefValve.query.filter_by(separator_tag = dataseparators["separator_tag"]).first()

    dataseparator.separator_tag = dataseparators["separator_tag"]
    datafluid.separator_tag = dataseparators["separator_tag"]
    datalevelcontrolvalve.separator_tag = dataseparators["separator_tag"]
    datareliefvalve.separator_tag = dataseparators["separator_tag"]
    separator.tag = dataseparators["separator_tag"]

    db.session.delete(dataseparator)
    db.session.delete(datafluid)
    db.session.delete(datalevelcontrolvalve)
    db.session.delete(datareliefvalve)
    db.session.delete(separator)
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
    datareliefvalve = SeparatorInputDataReliefValve.query.filter_by(separator_tag = datareliefvalves["separator_tag"]).first()

    datareliefvalve.separator_tag = datareliefvalves["separator_tag"]
    datareliefvalve.rvtag = datareliefvalves["rvtag"]
    if datareliefvalve.rvtag == '' or datareliefvalve.rvtag == '-':
        return jsonify("Empty RV Tag param."), 401

    datareliefvalve.rvsetpressure = datareliefvalves["rvsetpressure"]
    if datareliefvalve.rvsetpressure == '' or float(datareliefvalve.rvsetpressure) == 0:
        return jsonify("Empty RV Set Pressure param."), 401
    if float(datareliefvalve.rvsetpressure) != 0 and float(datareliefvalve.rvsetpressure) < 300 or float(datareliefvalve.rvsetpressure) > 80000:
        return jsonify("Invalid RV Set Pressure param. (Min. 300 - Max. 80000)"), 401

    datareliefvalve.rvorificearea = datareliefvalves["rvorificearea"]
    if datareliefvalve.rvorificearea == '' or float(datareliefvalve.rvorificearea) == 0:
        return jsonify("Empty RV Orifice Area param."), 401
    if float(datareliefvalve.rvorificearea) != 0 and float(datareliefvalve.rvorificearea) < 0.1 or float(datareliefvalve.rvorificearea) > 30:
        return jsonify("Invalid RV Orifice Area param. (Min. 0.1 - Max. 30)"), 401


    db.session.add(datareliefvalve)
    db.session.commit()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200

@api.route('/datareliefvalve', methods=['DELETE'])
def handle_delete_data_relief_valve():
    datareliefvalves = request.get_json()
    datareliefvalve = SeparatorInputDataReliefValve.query.filter_by(separator_tag = datareliefvalves["separator_tag"]).first()
    datalevelcontrolvalve = SeparatorInputDataLevelControlValve.query.filter_by(separator_tag = datareliefvalves["separator_tag"]).first()
    separator = Separator.query.filter_by(tag = datareliefvalves["separator_tag"]).first()
    datafluid = SeparatorInputDataFluid.query.filter_by(separator_tag = datareliefvalves["separator_tag"]).first()
    dataseparator = SeparatorInputDataSeparator.query.filter_by(separator_tag = datareliefvalves["separator_tag"]).first()

    separator.tag = datareliefvalves["separator_tag"]
    datareliefvalve.separator_tag = datareliefvalves["separator_tag"]
    datalevelcontrolvalve.separator_tag = datareliefvalves["separator_tag"]
    datafluid.separator_tag = datareliefvalves["separator_tag"]
    dataseparator.separator_tag = datareliefvalves["separator_tag"]
    

    db.session.delete(datareliefvalve)
    db.session.delete(datafluid)
    db.session.delete(datalevelcontrolvalve)
    db.session.delete(dataseparator)
    db.session.delete(separator)
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
    lcvtag = datalevelcontrolvalves["lcvtag"]
    lcvcv = datalevelcontrolvalves["lcvcv"]
    lcvdiameter = datalevelcontrolvalves["lcvdiameter"]
    inletlcvpipingdiameter = datalevelcontrolvalves["inletlcvpipingdiameter"]
    outletlcvpipingdiameter = datalevelcontrolvalves["outletlcvpipingdiameter"]
    lcvfactorfl = datalevelcontrolvalves["lcvfactorfl"]
    #lcvfactorfi = datalevelcontrolvalves["lcvfactorfi"]
    lcvfactorfp = datalevelcontrolvalves["lcvfactorfp"]
    lcvinletpressure = datalevelcontrolvalves["lcvinletpressure"]
    lcvoutletpressure = datalevelcontrolvalves["lcvoutletpressure"]


    separatorLevelControlValve = SeparatorInputDataLevelControlValve(id=id, separator_id=separator_id, lcvtag=lcvtag, lcvcv=lcvcv, 
                                                    lcvdiameter=lcvdiameter, inletlcvpipingdiameter=inletlcvpipingdiameter, outletlcvpipingdiameter=outletlcvpipingdiameter, lcvfactorfl=lcvfactorfl, 
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
    datalevelcontrolvalve = SeparatorInputDataLevelControlValve.query.filter_by(separator_tag = datalevelcontrolvalves["separator_tag"]).first()
    
    datalevelcontrolvalve.separator_tag = datalevelcontrolvalves["separator_tag"]
    datalevelcontrolvalve.lcvtag = datalevelcontrolvalves["lcvtag"]
    if datalevelcontrolvalve.lcvtag == '' or datalevelcontrolvalve.lcvtag == '-':
        return jsonify("Empty LCV Tag param."), 401

    datalevelcontrolvalve.lcvcv = datalevelcontrolvalves["lcvcv"]
    if datalevelcontrolvalve.lcvcv == '' or float(datalevelcontrolvalve.lcvcv) == 0:
        return jsonify("Empty LCV CV param."), 401
    if float(datalevelcontrolvalve.lcvcv) != 0 and float(datalevelcontrolvalve.lcvcv) < 3 or float(datalevelcontrolvalve.lcvcv) > 400:
        return jsonify("Invalid LCV CV param. (Min. 3 - Max. 400)"), 401

    #datalevelcontrolvalve.lcvdiameter = datalevelcontrolvalves["lcvdiameter"]
    #datalevelcontrolvalve.inletlcvpipingdiameter = datalevelcontrolvalves["inletlcvpipingdiameter"]
    #datalevelcontrolvalve.outletlcvpipingdiameter = datalevelcontrolvalves["outletlcvpipingdiameter"]
    datalevelcontrolvalve.lcvfactorfl = datalevelcontrolvalves["lcvfactorfl"]
    if datalevelcontrolvalve.lcvfactorfl == '' or float(datalevelcontrolvalve.lcvfactorfl) == 0:
        return jsonify("Empty LCV Factor Fl param."), 401
    if float(datalevelcontrolvalve.lcvfactorfl) != 0 and float(datalevelcontrolvalve.lcvfactorfl) < 0.75 or float(datalevelcontrolvalve.lcvfactorfl) > 1.1:
        return jsonify("Invalid LCV Factor Fl param. (Min. 0.75 - Max. 1.1)"), 401

    # datalevelcontrolvalve.lcvfactorfi = datalevelcontrolvalves["lcvfactorfi"]
    # if datalevelcontrolvalve.lcvfactorfi == '' or datalevelcontrolvalve.lcvfactorfi == 0:
    #     return jsonify("Empty LCV Factor Fi param."), 401
    datalevelcontrolvalve.lcvfactorfp = datalevelcontrolvalves["lcvfactorfp"]
    if datalevelcontrolvalve.lcvfactorfp == '' or float(datalevelcontrolvalve.lcvfactorfp) == 0:
        return jsonify("Empty LCV Factor Fp param."), 401
    if float(datalevelcontrolvalve.lcvfactorfp) != 0 and float(datalevelcontrolvalve.lcvfactorfp) < 0.75 or float(datalevelcontrolvalve.lcvfactorfp) > 1.1:
        return jsonify("Invalid LCV Factor Fp param. (Min. 0.75 - Max. 1.1)"), 401

    datalevelcontrolvalve.lcvinletpressure = datalevelcontrolvalves["lcvinletpressure"]
    if datalevelcontrolvalve.lcvinletpressure == '' or float(datalevelcontrolvalve.lcvinletpressure) == 0:
        return jsonify("Empty LCV Inlet Pressure param."), 401
    if float(datalevelcontrolvalve.lcvinletpressure) != 0 and float(datalevelcontrolvalve.lcvinletpressure) < 100 or float(datalevelcontrolvalve.lcvinletpressure) > 60000:
        return jsonify("Invalid LCV Inlet Pressure param. (Min. 100 - Max. 60000)"), 401

    datalevelcontrolvalve.lcvoutletpressure = datalevelcontrolvalves["lcvoutletpressure"]
    if datalevelcontrolvalve.lcvoutletpressure == '' or float(datalevelcontrolvalve.lcvoutletpressure) == 0:
        return jsonify("Empty LCV Outlet Pressure param."), 401
    if float(datalevelcontrolvalve.lcvoutletpressure) != 0 and float(datalevelcontrolvalve.lcvoutletpressure) < 50 or float(datalevelcontrolvalve.lcvoutletpressure) > 40000:
        return jsonify("Invalid LCV Outlet Pressure param. (Min. 50 - Max. 40000)"), 401

    db.session.add(datalevelcontrolvalve)
    db.session.commit()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200

# Eliminar datos en tabla datafluids
@api.route('/datalevelcontrolvalve', methods=['DELETE'])
def handle_delete_data_level_control_valve():
    datalevelcontrolvalves = request.get_json()
    datalevelcontrolvalve = SeparatorInputDataLevelControlValve.query.filter_by(separator_tag = datalevelcontrolvalves["separator_tag"]).first()
    separator = Separator.query.filter_by(tag = datalevelcontrolvalves["separator_tag"]).first()
    datafluid = SeparatorInputDataFluid.query.filter_by(separator_tag = datalevelcontrolvalves["separator_tag"]).first()
    datareliefvalve = SeparatorInputDataReliefValve.query.filter_by(separator_tag = datalevelcontrolvalves["separator_tag"]).first()
    dataseparator = SeparatorInputDataSeparator.query.filter_by(separator_tag = datalevelcontrolvalves["separator_tag"]).first()

    separator.tag = datalevelcontrolvalves["separator_tag"]
    datalevelcontrolvalve.separator_tag = datalevelcontrolvalves["separator_tag"]
    datafluid.separator_tag = datalevelcontrolvalves["separator_tag"]
    datareliefvalve.separator_tag = datalevelcontrolvalves["separator_tag"]
    dataseparator.separator_tag = datalevelcontrolvalves["separator_tag"]
    

    db.session.delete(datafluid)
    db.session.delete(dataseparator)
    db.session.delete(datalevelcontrolvalve)
    db.session.delete(datareliefvalve)
    db.session.delete(separator)
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


    res = gas_and_liquid_areas_calc()
    if res == None:
        response_body = {
            "message": "Success"
        }
        code = 200
    else:
        response_body = {
            "message": res
        }
        code = 401

    return jsonify(response_body), code


# Seleccionar SeparatorOutputGasAndLiquidAreas
@api.route('/gasandliquidareascalc', methods=['GET'])
def handle_get_gas_liquid_areas():

    gas_liquid_query = SeparatorOutputGasAndLiquidAreas.query.all()
    all_gas_liquid = list(map(lambda x: x.serialize(), gas_liquid_query))
    return jsonify(all_gas_liquid), 200


## Calcular SeparatorOutputInletNozzleParameters
@api.route('/inletnozzleparameterscalc', methods=['POST'])
def handle_calc_inlet_nozzle_parameters():

    res = inlet_nozzle_parameters_calc()
    if res == None:
        response_body = {
            "message": "Success"
        }
        code = 200
    else:
        response_body = {
            "message": res
        }
        code = 401

    return jsonify(response_body), code


# Seleccionar SeparatorOutputInletNozzleParameters
@api.route('/inletnozzleparameterscalc', methods=['GET'])
def handle_get_inlet_nozzle_parameters():

    inlet_nozzle_query = SeparatorOutputInletNozzleParameters.query.all()
    all_inlet_nozzle = list(map(lambda x: x.serialize(), inlet_nozzle_query))
    return jsonify(all_inlet_nozzle), 200

## Calcular SeparatorOutputGasNozzleParameters
@api.route('/gasnozzleparameterscalc', methods=['POST'])
def handle_calc_gas_nozzle_parameters():

    res = gas_nozzle_calc()
    if res == None:
        response_body = {
            "message": "Success"
        }
        code = 200
    else:
        response_body = {
            "message": res
        }
        code = 401

    return jsonify(response_body), code


# Seleccionar SeparatorOutputGasNozzleParameters
@api.route('/gasnozzleparameterscalc', methods=['GET'])
def handle_get_gas_nozzle_parameters():

    gas_nozzle_query = SeparatorOutputGasNozzleParameters.query.all()
    all_gas_nozzle = list(map(lambda x: x.serialize(), gas_nozzle_query))
    return jsonify(all_gas_nozzle), 200

## Calcular SeparatorOutputLiquidNozzleParameters
@api.route('/liquidnozzleparameterscalc', methods=['POST'])
def handle_calc_liquid_nozzle_parameters():

    res = liquid_nozzle_calc()
    if res == None:
        response_body = {
            "message": "Success"
        }
        code = 200
    else:
        response_body = {
            "message": res
        }
        code = 401

    return jsonify(response_body), code


# Seleccionar SeparatorOutputLiquidNozzleParameters
@api.route('/liquidnozzleparameterscalc', methods=['GET'])
def handle_get_liquid_nozzle_parameters():

    liquid_nozzle_query = SeparatorOutputLiquidNozzleParameters.query.all()
    all_liquid_nozzle = list(map(lambda x: x.serialize(), liquid_nozzle_query))
    return jsonify(all_liquid_nozzle), 200

## Calcular SeparatorOutputVesselGasCapacityParameters
@api.route('/vesselgascapacitycalc', methods=['POST'])
def handle_calc_vessel_gas_parameters():

    res = vessel_gas_capacity_calc()
    if res == None:
        response_body = {
            "message": "Success"
        }
        code = 200
    else:
        response_body = {
            "message": res
        }
        code = 401

    return jsonify(response_body), code
    

# Seleccionar SeparatorOutputVesselGasCapacityParameters
@api.route('/vesselgascapacitycalc', methods=['GET'])
def handle_get_vessel_gas_parameters():

    vessel_gas_query = SeparatorOutputVesselGasCapacityParameters.query.all()
    all_vessel_gas = list(map(lambda x: x.serialize(), vessel_gas_query))
    return jsonify(all_vessel_gas), 200

## Calcular SeparatorOutputVesselLiquidCapacityParameters
@api.route('/vesselliquidcapacitycalc', methods=['POST'])
def handle_calc_vessel_liquid_parameters():

    res = vessel_liquid_capacity_calc()
    if res == None:
        response_body = {
            "message": "Success"
        }
        code = 200
    else:
        response_body = {
            "message": res
        }
        code = 401

    return jsonify(response_body), code


# Seleccionar SeparatorOutputVesselLiquidCapacityParameters
@api.route('/vesselliquidcapacitycalc', methods=['GET'])
def handle_get_vessel_liquid_parameters():

    vessel_liquid_query = SeparatorOutputVesselLiquidCapacityParameters.query.all()
    all_vessel_liquid = list(map(lambda x: x.serialize(), vessel_liquid_query))
    return jsonify(all_vessel_liquid), 200

## Calcular SeparatorOutputReliefValveParameters
@api.route('/reliefvalvecalc', methods=['POST'])
def handle_calc_relief_valve_parameters():

    res = relief_valve_calc()
    if res == None:
        response_body = {
            "message": "Success"
        }
        code = 200
    else:
        response_body = {
            "message": res
        }
        code = 401

    return jsonify(response_body), code
    

# Seleccionar SeparatorOutputReliefValveParameters
@api.route('/reliefvalvecalc', methods=['GET'])
def handle_get_relief_valve_parameters():

    relief_valve_query = SeparatorOutputReliefValveParameters.query.all()
    all_relief_valves = list(map(lambda x: x.serialize(), relief_valve_query))
    return jsonify(all_relief_valves), 200

## Calcular SeparatorOutputReliefValveParameters
@api.route('/levelcontrolcalc', methods=['POST'])
def handle_calc_level_control_valve_parameters():

    res = level_control_calc()
    if res == None:
        response_body = {
            "message": "Success"
        }
        code = 200
    else:
        response_body = {
            "message": res
        }
        code = 401

    return jsonify(response_body), code
    

# Seleccionar SeparatorOutputReliefValveParameters
@api.route('/levelcontrolcalc', methods=['GET'])
def handle_get_level_control_valve_parameters():

    level_control_valve_query = SeparatorOutputLevelControlValveParameters.query.all()
    all_level_control_valves = list(map(lambda x: x.serialize(), level_control_valve_query))
    return jsonify(all_level_control_valves), 200


