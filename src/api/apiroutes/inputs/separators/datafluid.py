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
       return jsonify("Error. Empty Operating Pressure param"), 401
    datafluid.operatingtemperature = datafluids["operatingtemperature"]
    if datafluid.operatingtemperature == '' or datafluid.operatingtemperature =='-':
        return jsonify("Error. Empty Operating Temperature param"), 401
    datafluid.oildensity = datafluids["oildensity"]
    if datafluid.oildensity == '' or datafluid.oildensity == '-':
        return jsonify("Error. Empty Oil Density param"), 401
    datafluid.gasdensity = datafluids["gasdensity"]
    if datafluid.gasdensity == '' or datafluid.gasdensity == '-':
        return jsonify("Error. Empty Gas Density param"), 401
    datafluid.mixturedensity = datafluids["mixturedensity"]
    if datafluid.mixturedensity == '' or '-':
        return jsonify("Error. Empty Mixture Density param"), 401
    datafluid.waterdensity = datafluids["waterdensity"]
    if datafluid.waterdensity == '' or '-':
        return jsonify("Error. Empty Water Density params"), 401
    datafluid.feedbsw = datafluids["feedbsw"]
    if datafluid.feedbsw == '' or '-':
        return jsonify("Error. Empty Feed BSW params"), 401
    datafluid.liquidviscosity = datafluids["liquidviscosity"]
    if datafluid.liquidviscosity == '' or '-':
        return jsonify("Error. Empty Liquid Viscosity params"), 401
    datafluid.gasviscosity = datafluids["gasviscosity"]
    if datafluid.gasviscosity == '' or '-':
        return jsonify("Error. Empty Gas Viscosity params"), 401
    datafluid.gasmw = datafluids["gasmw"]
    if datafluid.gasmw == '' or '-':
        return jsonify("Error. Empty Gas Mw params"), 401
    datafluid.liqmw = datafluids["liqmw"]
    if datafluid.liqmw == '' or '-':
        return jsonify("Error. Empty Liq MW params"), 401
    datafluid.gascomprz = datafluids["gascomprz"]
    if datafluid.gascomprz == '' or '-':
        return jsonify("Error. Empty Gas Compressor (Z) params"), 401
    datafluid.especificheatratio = datafluids["especificheatratio"]
    if datafluid.especificheatratio == '' or '-':
        return jsonify("Error. Empty Specific Heat Ratio params"), 401
    datafluid.liquidsurfacetension = datafluids["liquidsurfacetension"]
    if datafluid.liquidsurfacetension == '' or '-':
        return jsonify("Error. Empty Liquid Surface Tension params"), 401
    datafluid.liquidvaporpressure = datafluids["liquidvaporpressure"]
    if datafluid.liquidvaporpressure == '' or '-':
        return jsonify("Error. Empty Liquid Vapor Pressure params"), 401
    datafluid.liquidcriticalpressure = datafluids["liquidcriticalpressure"]
    if datafluid.liquidcriticalpressure == '' or '-':
        return jsonify("Error. Empty Liquid Critical Pressure params"), 401
    datafluid.standardgasflow = datafluids["standardgasflow"]
    if datafluid.standardgasflow == '' or '-':
        return jsonify("Error. Empty Standard Gas Flow params"), 401
    datafluid.standardliquidflow = datafluids["standardliquidflow"]
    if datafluid.standardliquidflow == '' or '-':
        return jsonify("Error. Empty Standard Liquid Flow params"), 401
    datafluid.actualgasflow = datafluids["actualgasflow"]
    if datafluid.actualgasflow == '' or '-':
        return jsonify("Error. Empty Actual Gas Flow params"), 401
    datafluid.actualliquidflow = datafluids["actualliquidflow"]
    if datafluid.actualliquidflow == '' or '-':
        return jsonify("Error. Empty Actual Liquid Flow params"), 401

    db.session.add(datafluid)
    db.session.commit()

    response_body = {
        "message": "Success"
    }

    return jsonify(response_body), 200