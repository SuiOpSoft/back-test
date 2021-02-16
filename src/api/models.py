from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

## Company table
class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    dateofstablish = db.Column(db.Integer, nullable=True)
    description = db.Column(db.String(120), nullable=True)
    address = db.Column(db.String(120), nullable=True)
    users = db.relationship('User') ## One to many to users table
    facilities = db.relationship('Facility') ## One to many to facilities table

    def __repr__(self):
        return f'<Company {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "dateofstablish": self.dateofstablish,
            "description": self.description,
            "address": self.address
        }

## User tables
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)
    facilities = db.relationship('Facility') ## One to many to facilities table

    def __repr__(self):
        return '<User {self.email}>'
        
    def serialize(self):
        return {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "company_id": self.company_id
        }

## Facilities table
class Facility(db.Model):
    __tablename__ = 'facilities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("facilities.id"), unique=True, nullable=False)
    separators = db.relationship('Separator') ## One to many to separators table

    def __repr__(self):
        return '<Facility {self.name}>'
        
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "company_id": self.company_id,
            "user_id": self.user_id
        }


## Separators table
class Separator(db.Model):
    __tablename__ = 'separators'
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(120), nullable=False)
    facility_id = db.Column(db.Integer, db.ForeignKey("facilities.id"), unique=True, nullable=False)
    separators_inputs = db.relationship('SeparatorInput') ## One to many to separators_inputs table
    separators_outputs = db.relationship('SeparatorOutputs') ## One to many to separators_outputs table

    def __repr__(self):
        return '<Separator {self.tag}>'
        
    def serialize(self):
        return {
            "id": self.id,
            "tag": self.tag,
            "description": self.description,
            "facility_id": self.facility_id
        }

## separators_inputs
class SeparatorInput(db.Model):
    __tablename__ = 'separators_inputs'
    id = db.Column(db.Integer, primary_key=True)
    separator_id = db.Column(db.Integer, db.ForeignKey("separators.id"), unique=True, nullable=False)
    separators_inputs_data_fluids = db.relationship('separators_inputs_data_fluids') ## One to one to separators_inputs_data_fluids table
    separators_inputs_data_separators = db.relationship('separators_inputs_data_separators') ## One to one to separators_inputs_data_separators table
    separators_inputs_data_relief_valves = db.relationship('separators_inputs_data_relief_valves') ## One to one to separators_inputs_data_relief_valves table
    separators_inputs_data_level_control_valves = db.relationship('separators_inputs_data_level_control_valves') ## One to one to separators_inputs_data_level_control_valves table

    def __repr__(self):
        return '<SeparatorInput {self.separator_id}>'
        
    def serialize(self):
        return {
            "id": self.id,
            "separator_id": self.separator_id
        }

## separators_inputs_data_fluids
class SeparatorInputDataFluid(db.Model):
    __tablename__ = 'separators_inputs_data_fluids'
    id = db.Column(db.Integer, primary_key=True)
    separator_id = db.Column(db.Integer, db.ForeignKey("separators_inputs.separator_id"), unique=True, nullable=False)
    operatingpressure = db.Column(db.String(80), nullabe=False)
    operatingtemperature = db.Column(db.String(80), nullabe=False)
    oildensity = db.Column(db.String(80), nullabe=False)
    gasdensity = db.Column(db.String(80), nullabe=False)
    mixturedensity = db.Column(db.String(80), nullabe=False)
    waterdensity = db.Column(db.String(80), nullabe=False)
    feedbsw = db.Column(db.String(80), nullabe=False)
    liquidviscosity = db.Column(db.String(80), nullabe=False)
    gasviscosity = db.Column(db.String(80), nullabe=False)
    gasmw = db.Column(db.String(80), nullabe=False)
    liqmw = db.Column(db.String(80), nullabe=False)
    gascomprz = db.Column(db.String(80), nullabe=False)
    kcpcv = db.Column(db.String(80), nullabe=False)
    liquidsurfacetension = db.Column(db.String(80), nullabe=False)
    liquidvaporpressure = db.Column(db.String(80), nullabe=False)
    liquidcriticalpressure = db.Column(db.String(80), nullabe=False)
    standardgasflow = db.Column(db.String(80), nullabe=False)
    standardliquidflow = db.Column(db.String(80), nullabe=False)
    actualgasflow = db.Column(db.String(80), nullabe=False)
    actualliquidflow = db.Column(db.String(80), nullabe=False)

    def __repr__(self):
        return '<SeparatorInputDataFluid {self.separator_id}>'
        
    def serialize(self):
        return {
            "id": self.id,
            "separator_id": self.separator_id,
            "operatingpressure": self.operatingpressure,
            "operatingtemperature": self.operatingtemperature,
            "oildensity": self.oildensity,
            "gasdensity": self.gasdensity,
            "mixturedensity": self.mixturedensity,
            "waterdensity": self.waterdensity,
            "feedbsw": self.feedbsw,
            "liquidviscosity": self.liquidviscosity,
            "gasviscosity": self.gasviscosity,
            "gasmw": self.gasmw,
            "liqmw": self.liqmw,
            "gascomprz": self.gascomprz,
            "kcpcv": self.kcpcv,
            "liquidsurfacetension": self.liquidsurfacetension,
            "liquidvaporpressure": self.liquidvaporpressure,
            "liquidcriticalpressure": self.liquidcriticalpressure,
            "standardgasflow": self.standardgasflow,
            "standardliquidflow": self.standardliquidflow,
            "actualgasflow": self.actualgasflow,
            "actualliquidflow": self.actualliquidflow
        }

## separators_inputs_data_separators
class SeparatorInputDataSeparator(db.Model):
    __tablename__ = 'separators_inputs_data_separators'
    id = db.Column(db.Integer, primary_key=True)
    separator_id = db.Column(db.Integer, db.ForeignKey("separators_inputs.separator_id"), unique=True, nullable=False)
    internaldiameter = db.Column(db.String(80), nullabe=False)
    ttlength = db.Column(db.String(80), nullabe=False)
    highlevelTrip = db.Column(db.String(80), nullabe=False)
    highlevelalarm = db.Column(db.String(80), nullabe=False)
    normalliquidlevel = db.Column(db.String(80), nullabe=False)
    lowlevelalarm = db.Column(db.String(80), nullabe=False)
    inletnozzle = db.Column(db.String(80), nullabe=False)
    gasoutletnozzle = db.Column(db.String(80), nullabe=False)
    liquidoutletnozzle = db.Column(db.String(80), nullabe=False)
    inletdevicetype = db.Column(db.String(80), nullabe=False)
    demistertype = db.Column(db.String(80), nullabe=False)

    def __repr__(self):
        return '<SeparatorInputDataFluid {self.separator_id}>'
        
    def serialize(self):
        return {
            "id": self.id,
            "separator_id": self.separator_id,
            "internaldiameter": self.internaldiameter,
            "ttlength": self.ttlength,
            "highlevelTrip": self.highlevelTrip,
            "highlevelalarm": self.highlevelalarm,
            "normalliquidlevel": self.normalliquidlevel,
            "lowlevelalarm": self.lowlevelalarm,
            "inletnozzle": self.inletnozzle,
            "gasoutletnozzle": self.gasoutletnozzle,
            "liquidoutletnozzle": self.liquidoutletnozzle,
            "inletdevicetype": self.inletdevicetype,
            "demistertype": self.demistertype
        }

## separators_inputs_data_relief_valves
class SeparatorInputDataReliefValve(db.Model):
    __tablename__ = 'separators_inputs_data_relief_valves'
    id = db.Column(db.Integer, primary_key=True)
    separator_id = db.Column(db.Integer, db.ForeignKey("separators_inputs.separator_id"), unique=True, nullable=False)
    rvtag = db.Column(db.String(80), nullabe=False)
    rvsetpressure = db.Column(db.String(80), nullabe=False)
    rvorificearea = db.Column(db.String(80), nullabe=False)

    def __repr__(self):
        return '<SeparatorInputDataFluid {self.separator_id}>'
        
    def serialize(self):
        return {
            "id": self.id,
            "separator_id": self.separator_id,
            "rvtag": self.rvtag,
            "rvsetpressure": self.rvsetpressure,
            "rvorificearea": self.rvorificearea
        }
        
## separators_inputs_data_level_control_valves
class SeparatorInputDataLevelControlValve(db.Model):
    __tablename__ = 'separators_inputs_data_level_control_valves'
    id = db.Column(db.Integer, primary_key=True)
    separator_id = db.Column(db.Integer, db.ForeignKey("separators_inputs.separator_id"), unique=True, nullable=False)
    lcvtag = db.Column(db.String(80), nullabe=False)
    lcvcv = db.Column(db.String(80), nullabe=False)
    lcvdiameter = db.Column(db.String(80), nullabe=False)
    inletlcvpipingdiameter = db.Column(db.String(80), nullabe=False)
    outletlcvpipingdiameter = db.Column(db.String(80), nullabe=False)
    lcvfactorfl = db.Column(db.String(80), nullabe=False)
    lcvfactorfi = db.Column(db.String(80), nullabe=False)
    lcvfactorfp = db.Column(db.String(80), nullabe=False)
    lcvinletpressure = db.Column(db.String(80), nullabe=False)
    lcvoutletpressure = db.Column(db.String(80), nullabe=False)

    def __repr__(self):
        return '<SeparatorInputDataFluid {self.separator_id}>'
        
    def serialize(self):
        return {
            "id": self.id,
            "separator_id": self.separator_id,
            "lcvtag": self.lcvtag,
            "lcvcv": self.lcvcv,
            "lcvdiameter": self.lcvdiameter,
            "inletlcvpipingdiameter": self.inletlcvpipingdiameter,
            "outletlcvpipingdiameter": self.outletlcvpipingdiameter,
            "lcvfactorfl": self.lcvfactorfl,
            "lcvfactorfi": self.lcvfactorfi,
            "lcvfactorfp": self.lcvfactorfp,
            "lcvinletpressure": self.lcvinletpressure,
            "lcvoutletpressure": self.lcvoutletpressure
        }

## separators_outputs
## separators_outputs_gas_and_liquid_areas
## separators_outputs_inlet_nozzle_parameters
## separators_outputs_gas_nozzle_parameters
## separators_outputs_liquid_nozzle_parameters
## separators_outputs_vessel_gas_capacity_parameters
## separators_outputs_vessel_liquid_capacity_parameters
## separators_outputs_relief_valve_parameters
## separators_outputs_level_control_valve_parameters

