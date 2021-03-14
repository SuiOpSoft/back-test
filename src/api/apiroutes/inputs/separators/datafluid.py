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
    if datafluid.operatingpressure == '' or datafluid.operatingpressure == '-':
       return jsonify("Empty Operating Pressure param"), 401
    datafluid.operatingtemperature = datafluids["operatingtemperature"]
    if datafluid.operatingtemperature == '' or datafluid.operatingtemperature =='-':
        return jsonify("Empty Operating Temperature param"), 401
    datafluid.oildensity = datafluids["oildensity"]
    if datafluid.oildensity == '' or datafluid.oildensity == '-':
        return jsonify("Empty Oil Density param"), 401
    datafluid.gasdensity = datafluids["gasdensity"]
    if datafluid.gasdensity == '' or datafluid.gasdensity == '-':
        return jsonify("Empty Gas Density param"), 401
    datafluid.mixturedensity = datafluids["mixturedensity"]
    if datafluid.mixturedensity == '' or datafluid.mixturedensity == '-':
        return jsonify("Empty Mixture Density param"), 401
    datafluid.waterdensity = datafluids["waterdensity"]
    if datafluid.waterdensity == '' or datafluid.waterdensity == '-':
        return jsonify("Empty Water Density params"), 401
    datafluid.feedbsw = datafluids["feedbsw"]
    if datafluid.feedbsw == '' or datafluid.feedbsw == '-':
        return jsonify("Empty Feed BSW params"), 401
    datafluid.liquidviscosity = datafluids["liquidviscosity"]
    if datafluid.liquidviscosity == '' or datafluid.liquidviscosity == '-':
        return jsonify("Empty Liquid Viscosity params"), 401
    datafluid.gasviscosity = datafluids["gasviscosity"]
    if datafluid.gasviscosity == '' or datafluid.gasviscosity == '-':
        return jsonify("Empty Gas Viscosity params"), 401
    datafluid.gasmw = datafluids["gasmw"]
    if datafluid.gasmw == '' or datafluid.gasmw == '-':
        return jsonify("Empty Gas Mw params"), 401
    datafluid.liqmw = datafluids["liqmw"]
    if datafluid.liqmw == '' or datafluid.liqmw == '-':
        return jsonify("Empty Liq MW params"), 401
    datafluid.gascomprz = datafluids["gascomprz"]
    if datafluid.gascomprz == '' or datafluid.gascomprz == '-':
        return jsonify("Empty Gas Compressor (Z) params"), 401
    datafluid.especificheatratio = datafluids["especificheatratio"]
    if datafluid.especificheatratio == '' or datafluid.especificheatratio == '-':
        return jsonify("Empty Specific Heat Ratio params"), 401
    datafluid.liquidsurfacetension = datafluids["liquidsurfacetension"]
    if datafluid.liquidsurfacetension == '' or datafluid.liquidsurfacetension == '-':
        return jsonify("Empty Liquid Surface Tension params"), 401
    datafluid.liquidvaporpressure = datafluids["liquidvaporpressure"]
    if datafluid.liquidvaporpressure == '' or datafluid.liquidvaporpressure == '-':
        return jsonify("Empty Liquid Vapor Pressure params"), 401
    datafluid.liquidcriticalpressure = datafluids["liquidcriticalpressure"]
    if datafluid.liquidcriticalpressure == '' or datafluid.liquidcriticalpressure == '-':
        return jsonify("Empty Liquid Critical Pressure params"), 401
    datafluid.standardgasflow = datafluids["standardgasflow"]
    if datafluid.standardgasflow == '' or datafluid.standardgasflow == '-':
        return jsonify("Empty Standard Gas Flow params"), 401
    datafluid.standardliquidflow = datafluids["standardliquidflow"]
    if datafluid.standardliquidflow == '' or datafluid.standardliquidflow == '-':
        return jsonify("Empty Standard Liquid Flow params"), 401
    datafluid.actualgasflow = datafluids["actualgasflow"]
    if datafluid.actualgasflow == '' or datafluid.actualgasflow == '-':
        return jsonify("Empty Actual Gas Flow params"), 401
    datafluid.actualliquidflow = datafluids["actualliquidflow"]
    if datafluid.actualliquidflow == '' or datafluid.actualliquidflow == '-':
        return jsonify("Empty Actual Liquid Flow params"), 401

    db.session.add(datafluid)
    db.session.commit()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200