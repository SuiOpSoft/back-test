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
    facility1 = Facility(id="1", name="PDO Camp", location="Oman", company_id="1", user_id="1")
    separator1 = Separator(tag="v-3108", description="Separator V", facility_id="1")
    separatorDataFluid1 = SeparatorInputDataFluid(separator_tag="v-3108", operatingpressure="5536.33", operatingtemperature="37", oildensity="794.08", gasdensity="52.18", mixturedensity="197.76", waterdensity="1001", feedbsw="0.1", 
                                                    liquidviscosity="2.1065", gasviscosity="0.013385", gasmw="20.80", liqmw="155.53", gascomprz="0.8558", especificheatratio="1.4913", liquidsurfacetension="15.49", liquidvaporpressure="5536.3",
                                                    liquidcriticalpressure="12541.9", standardgasflow="25835.9", standardliquidflow="103.9", actualgasflow="435.5", actualliquidflow="106.33", kcp="1.49")
    
    separatorLevelControlValve1 = SeparatorInputDataLevelControlValve(separator_tag="v-3108", lcvtag="lcv-2021", lcvcv="47", 
                                                    lcvdiameter="5536.33", inletlcvpipingdiameter="5536.33", outletlcvpipingdiameter="5536.33", lcvfactorfl="0.9", lcvfactorfi="5536.33", 
                                                    lcvfactorfp="0.92", lcvinletpressure="5336.325", lcvoutletpressure="2286.325")

    separatorDataReliefValve1 = SeparatorInputDataReliefValve(separator_tag="v-3108", rvtag="rv-450", rvsetpressure="7900", 
                                                    rvorificearea="0.785")

    separatorInputSeparators1 = SeparatorInputDataSeparator(separator_tag="v-3108", internaldiameter="1800", ttlength="6300", 
                                                    highleveltrip="1080", highlevelalarm="900", normalliquidlevel="650", lowlevelalarm="390", inletnozzle="203.2", 
                                                    gasoutletnozzle="152.4", liquidoutletnozzle="203.2", inletdevicetype="SP", demistertype="VD")

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
@api.route('/companies/<string:company_name>', methods=['GET'])
def handle_get_company(company_name):

    #  user1 = Company.query.get(company_id)
    company_query = Company.query.filter_by(name=company_name)
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
    separatorDataFluid = SeparatorInputDataFluid(separator_tag=separator_tag, operatingpressure="-", operatingtemperature="-", 
                                                    oildensity="-", gasdensity="-", mixturedensity="-", waterdensity="-", feedbsw="-", 
                                                    liquidviscosity="-", gasviscosity="-", gasmw="-", liqmw="-", gascomprz="-", especificheatratio="-", 
                                                    liquidsurfacetension="-", liquidvaporpressure="-", liquidcriticalpressure="-", standardgasflow="-", 
                                                    standardliquidflow="-", actualgasflow="-", actualliquidflow="-", kcp="-")

    separatorLevelControlValve = SeparatorInputDataLevelControlValve(separator_tag=separator_tag, lcvtag="-", lcvcv="-", 
                                                    lcvdiameter="-", inletlcvpipingdiameter="-", outletlcvpipingdiameter="-", lcvfactorfl="-", lcvfactorfi="-", 
                                                    lcvfactorfp="-", lcvinletpressure="-", lcvoutletpressure="-")

    separatorDataReliefValve = SeparatorInputDataReliefValve(separator_tag=separator_tag, rvtag="-", rvsetpressure="-", 
                                                    rvorificearea="-")
    
    separatorInputSeparators = SeparatorInputDataSeparator(separator_tag=separator_tag, internaldiameter="-", ttlength="-", 
                                                    highleveltrip="-", highlevelalarm="-", normalliquidlevel="-", lowlevelalarm="-", inletnozzle="-", 
                                                    gasoutletnozzle="-", liquidoutletnozzle="-", inletdevicetype="-", demistertype="-")


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
# Seleccionar inputs data fluids
# @api.route('/datafluids', methods=['GET'])
# def handle_get_data_fluids():

#     data_fluids_query = SeparatorInputDataFluid.query.all()
#     all_data_fluids = list(map(lambda x: x.serialize(), data_fluids_query))
#     return jsonify(all_data_fluids), 200

# Insertar datos en  tabla data fluids
# @api.route('/datafluids', methods=['POST'])
# def handle_insert_data_fluids():
#     datafluids = request.get_json()

#     id = datafluids["id"]
#     separator_id = datafluids["separator_id"]
#     operatingpressure = datafluids["operatingpressure"]
#     operatingtemperature = datafluids["operatingtemperature"]
#     oildensity = datafluids["oildensity"]
#     gasdensity = datafluids["gasdensity"]
#     mixturedensity = datafluids["mixturedensity"]
#     waterdensity = datafluids["waterdensity"]
#     feedbsw = datafluids["feedbsw"]
#     liquidviscosity = datafluids["liquidviscosity"]
#     gasviscosity = datafluids["gasviscosity"]
#     gasmw = datafluids["gasmw"]
#     liqmw = datafluids["liqmw"]
#     gascomprz = datafluids["gascomprz"]
#     especificheatratio = datafluids["especificheatratio"]
#     liquidsurfacetension = datafluids["liquidsurfacetension"]
#     liquidvaporpressure = datafluids["liquidvaporpressure"]
#     liquidcriticalpressure = datafluids["liquidcriticalpressure"]
#     standardgasflow = datafluids["standardgasflow"]
#     standardliquidflow = datafluids["standardliquidflow"]
#     actualgasflow = datafluids["actualgasflow"]
#     actualliquidflow = datafluids["actualliquidflow"]

    

#     separatorDataFluid = SeparatorInputDataFluid(id=id, separator_id=separator_id, operatingpressure=operatingpressure, operatingtemperature=operatingtemperature, 
#                                                     oildensity=oildensity, gasdensity=gasdensity, mixturedensity=mixturedensity, waterdensity=waterdensity, feedbsw=feedbsw, 
#                                                     liquidviscosity=liquidviscosity, gasviscosity=gasviscosity, gasmw=gasmw, liqmw=liqmw, gascomprz=gascomprz, especificheatratio=especificheatratio, 
#                                                     liquidsurfacetension=liquidsurfacetension, liquidvaporpressure=liquidvaporpressure, liquidcriticalpressure=liquidcriticalpressure, standardgasflow=standardgasflow, 
#                                                     standardliquidflow=standardliquidflow, actualgasflow=actualgasflow, actualliquidflow=actualliquidflow)

 
#     db.session.add(separatorDataFluid)
#     db.session.commit()

#     response_body = {
#         "message": "Success"
#     }

#     return jsonify(response_body), 200

# Actualizar datos en tabla datafluids
# @api.route('/datafluids', methods=['PUT'])
# def handle_update_data_fluids():
#     datafluids = request.get_json()
#     datafluid = SeparatorInputDataFluid.query.filter_by(separator_tag = datafluids["separator_tag"]).first()

#     datafluid.separator_tag = datafluids["separator_tag"]
#     datafluid.operatingpressure = datafluids["operatingpressure"]
#     if datafluid.operatingpressure == '' or datafluid.operatingpressure == '-':
#        return jsonify("Error. Empty Operating Pressure param"), 401
#     datafluid.operatingtemperature = datafluids["operatingtemperature"]
#     if datafluid.operatingtemperature == '' or datafluid.operatingtemperature =='-':
#         return jsonify("Error. Empty Operating Temperature param"), 401
#     datafluid.oildensity = datafluids["oildensity"]
#     if datafluid.oildensity == '' or '-':
#         return jsonify("Error. Empty Oil Density param"), 401
#     datafluid.gasdensity = datafluids["gasdensity"]
#     if datafluid.gasdensity == '' or '-':
#         return jsonify("Error. Empty Gas Density param"), 401
#     datafluid.mixturedensity = datafluids["mixturedensity"]
#     if datafluid.mixturedensity == '' or '-':
#         return jsonify("Error. Empty Mixture Density param"), 401
#     datafluid.waterdensity = datafluids["waterdensity"]
#     if datafluid.waterdensity == '' or '-':
#         return jsonify("Error. Empty Water Density params"), 401
#     datafluid.feedbsw = datafluids["feedbsw"]
#     if datafluid.feedbsw == '' or '-':
#         return jsonify("Error. Empty Feed BSW params"), 401
#     datafluid.liquidviscosity = datafluids["liquidviscosity"]
#     if datafluid.liquidviscosity == '' or '-':
#         return jsonify("Error. Empty Liquid Viscosity params"), 401
#     datafluid.gasviscosity = datafluids["gasviscosity"]
#     if datafluid.gasviscosity == '' or '-':
#         return jsonify("Error. Empty Gas Viscosity params"), 401
#     datafluid.gasmw = datafluids["gasmw"]
#     if datafluid.gasmw == '' or '-':
#         return jsonify("Error. Empty Gas Mw params"), 401
#     datafluid.liqmw = datafluids["liqmw"]
#     if datafluid.liqmw == '' or '-':
#         return jsonify("Error. Empty Liq MW params"), 401
#     datafluid.gascomprz = datafluids["gascomprz"]
#     if datafluid.gascomprz == '' or '-':
#         return jsonify("Error. Empty Gas Compressor (Z) params"), 401
#     datafluid.especificheatratio = datafluids["especificheatratio"]
#     if datafluid.especificheatratio == '' or '-':
#         return jsonify("Error. Empty Specific Heat Ratio params"), 401
#     datafluid.liquidsurfacetension = datafluids["liquidsurfacetension"]
#     if datafluid.liquidsurfacetension == '' or '-':
#         return jsonify("Error. Empty Liquid Surface Tension params"), 401
#     datafluid.liquidvaporpressure = datafluids["liquidvaporpressure"]
#     if datafluid.liquidvaporpressure == '' or '-':
#         return jsonify("Error. Empty Liquid Vapor Pressure params"), 401
#     datafluid.liquidcriticalpressure = datafluids["liquidcriticalpressure"]
#     if datafluid.liquidcriticalpressure == '' or '-':
#         return jsonify("Error. Empty Liquid Critical Pressure params"), 401
#     datafluid.standardgasflow = datafluids["standardgasflow"]
#     if datafluid.standardgasflow == '' or '-':
#         return jsonify("Error. Empty Standard Gas Flow params"), 401
#     datafluid.standardliquidflow = datafluids["standardliquidflow"]
#     if datafluid.standardliquidflow == '' or '-':
#         return jsonify("Error. Empty Standard Liquid Flow params"), 401
#     datafluid.actualgasflow = datafluids["actualgasflow"]
#     if datafluid.actualgasflow == '' or '-':
#         return jsonify("Error. Empty Actual Gas Flow params"), 401
#     datafluid.actualliquidflow = datafluids["actualliquidflow"]
#     if datafluid.actualliquidflow == '' or '-':
#         return jsonify("Error. Empty Actual Liquid Flow params"), 401

    
    


#     db.session.add(datafluid)
#     db.session.commit()

#     response_body = {
#         "message": "Success"
#     }

#     return jsonify(response_body), 200
    

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
    if dataseparator.internaldiameter == '' or dataseparator.internaldiameter == '-':
        return jsonify("Empty Internal Diameter param."), 401
    dataseparator.ttlength = dataseparators["ttlength"]
    if dataseparator.ttlength == '' or dataseparator.ttlength == '-':
        return jsonify("Empty T-T Length param."), 401
    dataseparator.highleveltrip = dataseparators["highleveltrip"]
    if dataseparator.highleveltrip == '' or dataseparator.highleveltrip == '-':
        return jsonify("Empty High Level Trip param."), 401
    dataseparator.highlevelalarm = dataseparators["highlevelalarm"]
    if dataseparator.highlevelalarm == '' or dataseparator.highlevelalarm == '-':
        return jsonify("Empty High Level Alarm param."), 401
    dataseparator.normalliquidlevel = dataseparators["normalliquidlevel"]
    if dataseparator.normalliquidlevel == '' or dataseparator.normalliquidlevel == '-':
        return jsonify("Empty Normal Liquid Level param."), 401
    dataseparator.lowlevelalarm = dataseparators["lowlevelalarm"]
    if dataseparator.lowlevelalarm == '' or dataseparator.lowlevelalarm == '-':
        return jsonify("Empty Low Level Alarm param."), 401
    dataseparator.inletnozzle = dataseparators["inletnozzle"]
    if dataseparator.inletnozzle == '' or dataseparator.inletnozzle == '-':
        return jsonify("Empty Inlet Nozzle param."), 401
    dataseparator.gasoutletnozzle = dataseparators["gasoutletnozzle"]
    if dataseparator.gasoutletnozzle == '' or dataseparator.gasoutletnozzle == '-':
        return jsonify("Empty Gas Outlet Nozzle param."), 401
    dataseparator.liquidoutletnozzle = dataseparators["liquidoutletnozzle"]
    if dataseparator.liquidoutletnozzle == '' or dataseparator.liquidoutletnozzle == '-':
        return jsonify("Empty Liquid Outlet Nozzle param."), 401
    dataseparator.inletdevicetype = dataseparators["inletdevicetype"]
    if dataseparator.inletdevicetype == '' or dataseparator.inletdevicetype == '-':
        return jsonify("Empty Inlet Device Type param."), 401
    dataseparator.demistertype = dataseparators["demistertype"]
    if dataseparator.demistertype == '' or dataseparator.demistertype == '-':
        return jsonify("Empty Demister Type param."), 401


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
    if dataseparator.rvtag == '' or dataseparator.rvtag == '-':
        return jsonify("Empty RV Tag param."), 401
    datareliefvalve.rvsetpressure = datareliefvalves["rvsetpressure"]
    if dataseparator.rvsetpressure == '' or dataseparator.rvsetpressure == '-':
        return jsonify("Empty RV Set Pressure param."), 401
    datareliefvalve.rvorificearea = datareliefvalves["rvorificearea"]
    if dataseparator.rvorificearea == '' or dataseparator.rvorificearea == '-':
        return jsonify("Empty RV Orifice Area param."), 401


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
    lcvfactorfi = datalevelcontrolvalves["lcvfactorfi"]
    lcvfactorfp = datalevelcontrolvalves["lcvfactorfp"]
    lcvinletpressure = datalevelcontrolvalves["lcvinletpressure"]
    lcvoutletpressure = datalevelcontrolvalves["lcvoutletpressure"]


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
    datalevelcontrolvalve = SeparatorInputDataLevelControlValve.query.filter_by(separator_tag = datalevelcontrolvalves["separator_tag"]).first()
    
    datalevelcontrolvalve.separator_tag = datalevelcontrolvalves["separator_tag"]
    datalevelcontrolvalve.lcvtag = datalevelcontrolvalves["lcvtag"]
    if dataseparator.lcvtag == '' or dataseparator.lcvtag == '-':
        return jsonify("Empty LCV Tag param."), 401
    datalevelcontrolvalve.lcvcv = datalevelcontrolvalves["lcvcv"]
    if dataseparator.lcvcv == '' or dataseparator.lcvcv == '-':
        return jsonify("Empty LCV CV param."), 401
    #datalevelcontrolvalve.lcvdiameter = datalevelcontrolvalves["lcvdiameter"]
    #datalevelcontrolvalve.inletlcvpipingdiameter = datalevelcontrolvalves["inletlcvpipingdiameter"]
    #datalevelcontrolvalve.outletlcvpipingdiameter = datalevelcontrolvalves["outletlcvpipingdiameter"]
    datalevelcontrolvalve.lcvfactorfl = datalevelcontrolvalves["lcvfactorfl"]
    if dataseparator.lcvfactorfl == '' or dataseparator.lcvfactorfl == '-':
        return jsonify("Empty LCV Factor Fl param."), 401
    datalevelcontrolvalve.lcvfactorfi = datalevelcontrolvalves["lcvfactorfi"]
    if dataseparator.lcvfactorfi == '' or dataseparator.lcvfactorfi == '-':
        return jsonify("Empty LCV Factor Fi param."), 401
    datalevelcontrolvalve.lcvfactorfp = datalevelcontrolvalves["lcvfactorfp"]
    if dataseparator.lcvfactorfp == '' or dataseparator.lcvfactorfp == '-':
        return jsonify("Empty LCV Factor Fp param."), 401
    datalevelcontrolvalve.lcvinletpressure = datalevelcontrolvalves["lcvinletpressure"]
    if dataseparator.lcvinletpressure == '' or dataseparator.lcvinletpressure == '-':
        return jsonify("Empty LCV Inlet Pressure param."), 401
    datalevelcontrolvalve.lcvoutletpressure = datalevelcontrolvalves["lcvoutletpressure"]
    if dataseparator.lcvoutletpressure == '' or dataseparator.lcvoutletpressure == '-':
        return jsonify("Empty LCV Outlet Pressure param."), 401

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

## Calcular SeparatorOutputGasNozzleParameters
@api.route('/gasnozzleparameterscalc', methods=['POST'])
def handle_calc_gas_nozzle_parameters():

    gas_nozzle_calc()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200

# Seleccionar SeparatorOutputGasNozzleParameters
@api.route('/gasnozzleparameterscalc', methods=['GET'])
def handle_get_gas_nozzle_parameters():

    gas_nozzle_query = SeparatorOutputGasNozzleParameters.query.all()
    all_gas_nozzle = list(map(lambda x: x.serialize(), gas_nozzle_query))
    return jsonify(all_gas_nozzle), 200

## Calcular SeparatorOutputLiquidNozzleParameters
@api.route('/liquidnozzleparameterscalc', methods=['POST'])
def handle_calc_liquid_nozzle_parameters():

    liquid_nozzle_calc()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200

# Seleccionar SeparatorOutputLiquidNozzleParameters
@api.route('/liquidnozzleparameterscalc', methods=['GET'])
def handle_get_liquid_nozzle_parameters():

    liquid_nozzle_query = SeparatorOutputLiquidNozzleParameters.query.all()
    all_liquid_nozzle = list(map(lambda x: x.serialize(), liquid_nozzle_query))
    return jsonify(all_liquid_nozzle), 200

## Calcular SeparatorOutputVesselGasCapacityParameters
@api.route('/vesselgascapacitycalc', methods=['POST'])
def handle_calc_vessel_gas_parameters():

    vessel_gas_capacity_calc()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200

# Seleccionar SeparatorOutputVesselGasCapacityParameters
@api.route('/vesselgascapacitycalc', methods=['GET'])
def handle_get_vessel_gas_parameters():

    vessel_gas_query = SeparatorOutputVesselGasCapacityParameters.query.all()
    all_vessel_gas = list(map(lambda x: x.serialize(), vessel_gas_query))
    return jsonify(all_vessel_gas), 200

## Calcular SeparatorOutputVesselLiquidCapacityParameters
@api.route('/vesselliquidcapacitycalc', methods=['POST'])
def handle_calc_vessel_liquid_parameters():

    vessel_liquid_capacity_calc()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200

# Seleccionar SeparatorOutputVesselLiquidCapacityParameters
@api.route('/vesselliquidcapacitycalc', methods=['GET'])
def handle_get_vessel_liquid_parameters():

    vessel_liquid_query = SeparatorOutputVesselLiquidCapacityParameters.query.all()
    all_vessel_liquid = list(map(lambda x: x.serialize(), vessel_liquid_query))
    return jsonify(all_vessel_liquid), 200

## Calcular SeparatorOutputReliefValveParameters
@api.route('/reliefvalvecalc', methods=['POST'])
def handle_calc_relief_valve_parameters():

    relief_valve_calc()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200

# Seleccionar SeparatorOutputReliefValveParameters
@api.route('/reliefvalvecalc', methods=['GET'])
def handle_get_relief_valve_parameters():

    relief_valve_query = SeparatorOutputReliefValveParameters.query.all()
    all_relief_valves = list(map(lambda x: x.serialize(), relief_valve_query))
    return jsonify(all_relief_valves), 200

## Calcular SeparatorOutputReliefValveParameters
@api.route('/levelcontrolcalc', methods=['POST'])
def handle_calc_level_control_valve_parameters():

    level_control_calc()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200

# Seleccionar SeparatorOutputReliefValveParameters
@api.route('/levelcontrolcalc', methods=['GET'])
def handle_get_level_control_valve_parameters():

    level_control_valve_query = SeparatorOutputLevelControlValveParameters.query.all()
    all_level_control_valves = list(map(lambda x: x.serialize(), level_control_valve_query))
    return jsonify(all_level_control_valves), 200


