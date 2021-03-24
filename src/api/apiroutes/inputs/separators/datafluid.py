from flask import request, jsonify, Blueprint
from api.models import db, SeparatorInputDataFluid

api_datafluid = Blueprint('api_datafluid', __name__)

# Seleccionar inputs data fluids
@api_datafluid.route('/datafluids', methods=['GET'])
def handle_get_data_fluids():

    data_fluids_query = SeparatorInputDataFluid.query.all()
    all_data_fluids = list(map(lambda x: x.serialize(), data_fluids_query))
    return jsonify(all_data_fluids), 200

# Actualizar datos en tabla datafluids
@api_datafluid.route('/datafluids', methods=['PUT'])
def handle_update_data_fluids():
    datafluids = request.get_json()
    datafluid = SeparatorInputDataFluid.query.filter_by(separator_tag = datafluids["separator_tag"]).first()

    datafluid.separator_tag = datafluids["separator_tag"]
    datafluid.operatingpressure = datafluids["operatingpressure"]
    if datafluid.operatingpressure == '' or float(datafluid.operatingpressure) == 0:
       return jsonify("Empty Operating Pressure param"), 401
    if float(datafluid.operatingpressure) != 0 and float(datafluid.operatingpressure) < 100.00 or float(datafluid.operatingpressure) > 60000.00 :
       return jsonify("Invalid Operating Pressure param (Min. 100 - Max. 60000)"), 401

    datafluid.operatingtemperature = datafluids["operatingtemperature"]
    if datafluid.operatingtemperature == '' or float(datafluid.operatingtemperature) == 0:
        return jsonify("Empty Operating Temperature param"), 401
    if float(datafluid.operatingtemperature) != 0 and float(datafluid.operatingtemperature) < 15 or float(datafluid.operatingtemperature) > 80:
        return jsonify("Invalid Operating Temperature param (Min. 15 - Max. 80)"), 401
    
    datafluid.oildensity = datafluids["oildensity"]
    if datafluid.oildensity == '' or float(datafluid.oildensity) == 0:
        return jsonify("Empty Oil Density param"), 401
    if float(datafluid.oildensity) != 0 and float(datafluid.oildensity) < 300 or float(datafluid.oildensity) > 1300:
        return jsonify("Invalid Oil Density param (Min. 300 - Max. 1300)"), 401
    
    datafluid.gasdensity = datafluids["gasdensity"]
    if datafluid.gasdensity == '' or float(datafluid.gasdensity) == 0:
        return jsonify("Empty Gas Density param."), 401
    if float(datafluid.gasdensity) != 0 and float(datafluid.gasdensity) < 1 or float(datafluid.gasdensity) > 750:
        return jsonify("Invalid Gas Density param. (Min. 1 - Max. 750)"), 401
    
    datafluid.mixturedensity = datafluids["mixturedensity"]
    if datafluid.mixturedensity == '' or float(datafluid.mixturedensity) == 0:
        return jsonify("Empty Mixture Density param."), 401

    datafluid.waterdensity = datafluids["waterdensity"]
    if datafluid.waterdensity == '' or float(datafluid.waterdensity) == 0:
        return jsonify("Empty Water Density param."), 401
    if float(datafluid.waterdensity) != 0 and float(datafluid.waterdensity) < 900 or float(datafluid.waterdensity) > 1100:
        return jsonify("Invalid Water Density param. (Min. 900 - Max. 1100)"), 401
    
    datafluid.feedbsw = datafluids["feedbsw"]
    if datafluid.feedbsw == '' or float(datafluid.feedbsw) == 0:
        return jsonify("Empty Feed BSW param."), 401
    if float(datafluid.feedbsw) != 0 and float(datafluid.feedbsw) < 0.01 or float(datafluid.feedbsw) > 100:
        return jsonify("Invalid Feed BSW param. (Min. 0.01 - Max. 100)"), 401
    
    datafluid.liquidviscosity = datafluids["liquidviscosity"]
    if datafluid.liquidviscosity == '' or float(datafluid.liquidviscosity) == 0:
        return jsonify("Empty Liquid Viscosity param."), 401
    if float(datafluid.liquidviscosity) != 0 and float(datafluid.liquidviscosity) < 1 or float(datafluid.liquidviscosity) > 30:
        return jsonify("Invalid Liquid Viscosity param. (Min. 1 - Max. 30)"), 401
    
    datafluid.gasviscosity = datafluids["gasviscosity"]
    if datafluid.gasviscosity == '' or float(datafluid.gasviscosity) == 0:
        return jsonify("Empty Gas Viscosity param."), 401
    if float(datafluid.gasviscosity) != 0 and float(datafluid.gasviscosity) < 0.005 or float(datafluid.gasviscosity) > 0.2:
        return jsonify("Invalid Gas Viscosity param. (Min. 0.005 - Max. 0.2)"), 401

    datafluid.gasmw = datafluids["gasmw"]
    if datafluid.gasmw == '' or float(datafluid.gasmw) == 0:
        return jsonify("Empty Gas Mw param."), 401
    if float(datafluid.gasmw) != 0 and float(datafluid.gasmw) < 14 or float(datafluid.gasmw) > 50 :
        return jsonify("Invalid Gas Mw param. (Min. 14 - Max. 50)"), 401

    datafluid.liqmw = datafluids["liqmw"]
    if datafluid.liqmw == '' or float(datafluid.liqmw) == 0:
        return jsonify("Empty Liq MW param."), 401
    if float(datafluid.liqmw) != 0 and float(datafluid.liqmw) < 100 or float(datafluid.liqmw) > 900:
        return jsonify("Invalid Liq MW param. (Min. 100 - Max. 900)"), 401

    datafluid.gascomprz = datafluids["gascomprz"]
    if datafluid.gascomprz == '' or float(datafluid.gascomprz) == 0:
        return jsonify("Empty Gas Compressor (Z) param."), 401
    if float(datafluid.gascomprz) != 0 and float(datafluid.gascomprz) < 0.5 or float(datafluid.gascomprz) > 1.3:
        return jsonify("Invalid Gas Compressor (Z) param. (Min. 0.5 - Max. 1.3)"), 401

    datafluid.kcp = datafluids["kcp"]
    if datafluid.kcp == '' or float(datafluid.kcp) == 0:
        return jsonify("Empty kCpCv param."), 401
    if float(datafluid.kcp) != 0 and float(datafluid.kcp) < 1 or float(datafluid.kcp) > 3:
        return jsonify("Invalid kCpCv param. (Min. 1.0 - Max. 3.0)"), 401

    datafluid.especificheatratio = datafluids["especificheatratio"]
    if datafluid.especificheatratio == '' or float(datafluid.especificheatratio) == 0:
        return jsonify("Empty Specific Heat Ratio param."), 401
    # if float(datafluid.especificheatratio) != 0 and float(datafluid.especificheatratio) < ? float(datafluid.especificheatratio) > ?:
    #     return jsonify("Invalid Specific Heat Ratio param. (Min. ? - Max. ?)"), 401

    datafluid.liquidsurfacetension = datafluids["liquidsurfacetension"]
    if datafluid.liquidsurfacetension == '' or float(datafluid.liquidsurfacetension) == 0:
        return jsonify("Empty Liquid Surface Tension param."), 401
    if float(datafluid.liquidsurfacetension) != 0 and float(datafluid.liquidsurfacetension) < 5 or float(datafluid.liquidsurfacetension) > 40:
        return jsonify("Invalid Liquid Surface Tension param. (Min. 5 - Max. 40)"), 401

    datafluid.liquidvaporpressure = datafluids["liquidvaporpressure"]
    if datafluid.liquidvaporpressure == '' or float(datafluid.liquidvaporpressure) == 0:
        return jsonify("Empty Liquid Vapor Pressure param."), 401
    if float(datafluid.liquidvaporpressure) != 0 and float(datafluid.liquidvaporpressure) < 100 or float(datafluid.liquidvaporpressure) > 60000:
        return jsonify("Invalid Liquid Vapor Pressure param. (Min. 100 - Max. 60000)"), 401

    datafluid.liquidcriticalpressure = datafluids["liquidcriticalpressure"]
    if datafluid.liquidcriticalpressure == '' or float(datafluid.liquidcriticalpressure) == 0:
        return jsonify("Empty Liquid Critical Pressure param."), 401
    if float(datafluid.liquidcriticalpressure) != 0 and float(datafluid.liquidcriticalpressure) < 1000 or float(datafluid.liquidcriticalpressure) > 60000:
        return jsonify("Invalid Liquid Critical Pressure param. (Min. 1000 - Max. 60000)"), 401

    datafluid.standardgasflow = datafluids["standardgasflow"]
    if datafluid.standardgasflow == '' or float(datafluid.standardgasflow) == 0:
        return jsonify("Empty Standard Gas Flow param."), 401

    datafluid.standardliquidflow = datafluids["standardliquidflow"]
    if datafluid.standardliquidflow == '' or datafluid.standardliquidflow == '0':
        return jsonify("Empty Standard Liquid Flow param."), 401

    datafluid.actualgasflow = datafluids["actualgasflow"]
    if datafluid.actualgasflow == '' or datafluid.actualgasflow == '0':
        return jsonify("Empty Actual Gas Flow param."), 401

    datafluid.actualliquidflow = datafluids["actualliquidflow"]
    if datafluid.actualliquidflow == '' or datafluid.actualliquidflow == '0':
        return jsonify("Empty Actual Liquid Flow param."), 401

    db.session.add(datafluid)
    db.session.commit()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200