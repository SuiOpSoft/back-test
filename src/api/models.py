from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import safe_str_cmp

db = SQLAlchemy()

## Company table
class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    companyuser = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
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

    def check_password(self, password_param):
        return safe_str_cmp(self.password.encode('utf-8'), password_param.encode('utf-8'))

## Many to Many association between User and Facilities
association_table = db.Table('user_facilities', db.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('facility_id', db.Integer, db.ForeignKey('facilities.id'))
)

## User tables
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)
    facilities = db.relationship(
        "Facility",
        secondary=association_table,
        back_populates="users")


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

    def check_password(self, password_param):
        return safe_str_cmp(self.password.encode('utf-8'), password_param.encode('utf-8'))

# ## Facilities table
class Facility(db.Model):
    __tablename__ = 'facilities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)##Es necesario?????
    separators = db.relationship('Separator') ## One to many to separators table
    users = db.relationship(
        "User",
        secondary=association_table,
        back_populates="facilities")

    def __repr__(self):
        return '<Facility {self.name}>'
        
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "company_id": self.company_id,
            "user_id" : self.user_id      
        }

# ## Separators table
class Separator(db.Model):
    __tablename__ = 'separators'
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(120), nullable=True)
    facility_id = db.Column(db.Integer, db.ForeignKey("facilities.id"), nullable=True)
    separators_inputs_data_fluids = db.relationship('SeparatorInputDataFluid') ## separators_inputs_data_fluids
    separators_inputs_data_separators = db.relationship('SeparatorInputDataSeparator') ## separators_inputs_data_separators
    separators_inputs_data_relief_valves = db.relationship('SeparatorInputDataReliefValve') ## separators_inputs_data_relief_valves
    separators_inputs_data_level_control_valves = db.relationship('SeparatorInputDataLevelControlValve') ## separators_inputs_data_level_control_valves
    separators_outputs_gas_and_liquid_areas = db.relationship('SeparatorOutputGasAndLiquidAreas') ## separators_outputs_gas_and_liquid_areas
    separators_outputs_inlet_nozzle_parameters = db.relationship('SeparatorOutputInletNozzleParameters') ## separators_outputs_inlet_nozzle_parameters
    separators_outputs_gas_nozzle_parameters = db.relationship('SeparatorOutputGasNozzleParameters') ## separators_outputs_gas_nozzle_parameters
    separators_outputs_liquid_nozzle_parameters = db.relationship('SeparatorOutputLiquidNozzleParameters') ## separators_outputs_liquid_nozzle_parameters
    separators_outputs_vessel_gas_capacity_parameters = db.relationship('SeparatorOutputVesselGasCapacityParameters') ## separators_outputs_vessel_gas_capacity_parameters
    separators_outputs_vessel_liquid_capacity_parameters = db.relationship('SeparatorOutputVesselLiquidCapacityParameters') ## separators_outputs_vessel_liquid_capacity_parameters
    separators_outputs_relief_valve_parameters = db.relationship('SeparatorOutputReliefValveParameters') ## separators_outputs_relief_valve_parameters
    separators_outputs_level_control_valve_parameters = db.relationship('SeparatorOutputLevelControlValveParameters') ## separators_outputs_level_control_valve_parameters

    def __repr__(self):
        return '<Separator {self.tag}>'
        
    def serialize(self):
        return {
            "id": self.id,
            "tag": self.tag,
            "description": self.description,
            "facility_id": self.facility_id
        }

# ## separators_inputs_data_fluids
class SeparatorInputDataFluid(db.Model):
    __tablename__ = 'separators_inputs_data_fluids'
    id = db.Column(db.Integer, primary_key=True)
    separator_tag = db.Column(db.String, db.ForeignKey("separators.tag"), nullable=False)
    operatingpressure = db.Column(db.Float, nullable=False)
    operatingtemperature = db.Column(db.Float, nullable=False)
    oildensity = db.Column(db.Float, nullable=False)
    gasdensity = db.Column(db.Float, nullable=False)
    mixturedensity = db.Column(db.Float, nullable=False)
    waterdensity = db.Column(db.Float, nullable=False)
    feedbsw = db.Column(db.Float, nullable=False)
    liquidviscosity = db.Column(db.Float, nullable=False)
    gasviscosity = db.Column(db.Float, nullable=False)
    gasmw = db.Column(db.Float, nullable=False)
    liqmw = db.Column(db.Float, nullable=False)
    gascomprz = db.Column(db.Float, nullable=False)
    kcp = db.Column(db.Float, nullable=False)
    especificheatratio = db.Column(db.Float, nullable=False)
    liquidsurfacetension = db.Column(db.Float, nullable=False)
    liquidvaporpressure = db.Column(db.Float, nullable=False)
    liquidcriticalpressure = db.Column(db.Float, nullable=False)
    standardgasflow = db.Column(db.Float, nullable=False)
    standardliquidflow = db.Column(db.Float, nullable=False)
    actualgasflow = db.Column(db.Float, nullable=False)
    actualliquidflow = db.Column(db.Float, nullable=False)
    

    def __repr__(self):
        return '<SeparatorInputDataFluid {self.separator_tag}>'
        
    def serialize(self):
        return {
            "id": self.id,
            "separator_tag": self.separator_tag,
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
            "especificheatratio": self.especificheatratio,
            "liquidsurfacetension": self.liquidsurfacetension,
            "liquidvaporpressure": self.liquidvaporpressure,
            "liquidcriticalpressure": self.liquidcriticalpressure,
            "standardgasflow": self.standardgasflow,
            "standardliquidflow": self.standardliquidflow,
            "actualgasflow": self.actualgasflow,
            "actualliquidflow": self.actualliquidflow,
            "kcp": self.kcp
        }

# ## separators_inputs_data_separators
class SeparatorInputDataSeparator(db.Model):
    __tablename__ = 'separators_inputs_data_separators'
    id = db.Column(db.Integer, primary_key=True)
    separator_tag = db.Column(db.String, db.ForeignKey("separators.tag"), nullable=False)
    internaldiameter = db.Column(db.Float, nullable=False)
    ttlength = db.Column(db.Float, nullable=False)
    highleveltrip = db.Column(db.Float, nullable=False)
    highlevelalarm = db.Column(db.Float, nullable=False)
    normalliquidlevel = db.Column(db.Float, nullable=False)
    lowlevelalarm = db.Column(db.Float, nullable=False)
    inletnozzle = db.Column(db.Float, nullable=False)
    gasoutletnozzle = db.Column(db.Float, nullable=False)
    liquidoutletnozzle = db.Column(db.Float, nullable=False)
    inletdevicetype = db.Column(db.String(80), nullable=False)
    demistertype = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<SeparatorInputDataSeparator {self.separator_tag}>'
        
    def serialize(self):
        return {
            "id": self.id,
            "separator_tag": self.separator_tag,
            "internaldiameter": self.internaldiameter,
            "ttlength": self.ttlength,
            "highleveltrip": self.highleveltrip,
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
    separator_tag = db.Column(db.String, db.ForeignKey("separators.tag"), nullable=False)
    rvtag = db.Column(db.String(80), nullable=False)
    rvsetpressure = db.Column(db.Float, nullable=False)
    rvorificearea = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<SeparatorInputDataReliefValve {self.separator_tag}>'
        
    def serialize(self):
        return {
            "id": self.id,
            "separator_tag": self.separator_tag,
            "rvtag": self.rvtag,
            "rvsetpressure": self.rvsetpressure,
            "rvorificearea": self.rvorificearea
        }
        
### separators_inputs_data_level_control_valves
class SeparatorInputDataLevelControlValve(db.Model):
    __tablename__ = 'separators_inputs_data_level_control_valves'
    id = db.Column(db.Integer, primary_key=True)
    separator_tag = db.Column(db.String, db.ForeignKey("separators.tag"), nullable=False)
    lcvtag = db.Column(db.String(80), nullable=False)
    lcvcv = db.Column(db.Float, nullable=False)
    lcvdiameter = db.Column(db.Float, nullable=False)
    inletlcvpipingdiameter = db.Column(db.Float, nullable=False)
    outletlcvpipingdiameter = db.Column(db.Float, nullable=False)
    lcvfactorfl = db.Column(db.Float, nullable=False)
    #lcvfactorfi = db.Column(db.Float, nullable=False)
    lcvfactorfp = db.Column(db.Float, nullable=False)
    lcvinletpressure = db.Column(db.Float, nullable=False)
    lcvoutletpressure = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<SeparatorInputDataLevelControlValve {self.separator_tag}>'
        
    def serialize(self):
        return {
            "id": self.id,
            "separator_tag": self.separator_tag,
            "lcvtag": self.lcvtag,
            "lcvcv": self.lcvcv,
            "lcvdiameter": self.lcvdiameter,
            "inletlcvpipingdiameter": self.inletlcvpipingdiameter,
            "outletlcvpipingdiameter": self.outletlcvpipingdiameter,
            "lcvfactorfl": self.lcvfactorfl,
            #"lcvfactorfi": self.lcvfactorfi,
            "lcvfactorfp": self.lcvfactorfp,
            "lcvinletpressure": self.lcvinletpressure,
            "lcvoutletpressure": self.lcvoutletpressure
        }

# ## separators_outputs_gas_and_liquid_areas
class SeparatorOutputGasAndLiquidAreas(db.Model):
    __tablename__ = 'separators_outputs_gas_and_liquid_areas'
    id = db.Column(db.Integer, primary_key=True)
    separator_tag = db.Column(db.String, db.ForeignKey("separators.tag"), nullable=False)
    separatorcrosssectionalarearatio = db.Column(db.Float, nullable=False)
    separatorcrosssectionalarea = db.Column(db.Float, nullable=False)
    inletnozzlearea = db.Column(db.Float, nullable=False)
    gasnozzlearea = db.Column(db.Float, nullable=False)
    liquidnozzlearea = db.Column(db.Float, nullable=False)
    highleveltripgasarea = db.Column(db.Float, nullable=False)
    normallevelgasarea = db.Column(db.Float, nullable=False)
    lowlevelgasarea = db.Column(db.Float, nullable=False)
    highleveltripliquidarea = db.Column(db.Float, nullable=False)
    normalleveltriparea = db.Column(db.Float, nullable=False)
    lowleveltripliquidarea = db.Column(db.Float, nullable=False)
    

    def __repr__(self):
        return '<SeparatorOutputGasAndLiquidAreas {self.separator_tag}>'
        
    def serialize(self):
        return {
            "id": self.id,
            "separator_tag": self.separator_tag,
            "separatorcrosssectionalarearatio": self.separatorcrosssectionalarearatio,
            "separatorcrosssectionalarea": self.separatorcrosssectionalarea,
            "inletnozzlearea": self.inletnozzlearea,
            "gasnozzlearea": self.gasnozzlearea,
            "liquidnozzlearea": self.liquidnozzlearea,
            "highleveltripgasarea": self.highleveltripgasarea,
            "normallevelgasarea": self.normallevelgasarea,
            "lowlevelgasarea": self.lowlevelgasarea,
            "highleveltripliquidarea": self.highleveltripliquidarea,
            "normalleveltriparea": self.normalleveltriparea,
            "lowleveltripliquidarea": self.lowleveltripliquidarea
        }

## separators_outputs_inlet_nozzle_parameters
class SeparatorOutputInletNozzleParameters(db.Model):
    __tablename__ = 'separators_outputs_inlet_nozzle_parameters'
    id = db.Column(db.Integer, primary_key=True)
    separator_tag = db.Column(db.String, db.ForeignKey("separators.tag"), nullable=False)
    mixtureinletnozzlevelocity = db.Column(db.Float, nullable=False)
    inletnozzlemomentum = db.Column(db.Float, nullable=False)
    maximummixtureinletnozzlevelocity = db.Column(db.Float, nullable=False)
    maximuminletnozzlemomentum = db.Column(db.Float, nullable=False)
    maximumliquidflowinletnozzle = db.Column(db.Float, nullable=False)
    maximumgasflowinletnozzle = db.Column(db.Float, nullable=False)
    statusinletnozzle = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<SeparatorOutputInletNozzleParameters {self.separator_tag}>'
        
    def serialize(self):
        return {
            "id": self.id,
            "separator_tag": self.separator_tag,
            "mixtureinletnozzlevelocity": self.mixtureinletnozzlevelocity,
            "inletnozzlemomentum": self.inletnozzlemomentum,
            "maximummixtureinletnozzlevelocity": self.maximummixtureinletnozzlevelocity,
            "maximuminletnozzlemomentum": self.maximuminletnozzlemomentum,
            "maximumliquidflowinletnozzle": self.maximumliquidflowinletnozzle,
            "maximumgasflowinletnozzle": self.maximumgasflowinletnozzle,
            "statusinletnozzle": self.statusinletnozzle,
            
        }

# ## separators_outputs_gas_nozzle_parameters
class SeparatorOutputGasNozzleParameters(db.Model):
    __tablename__ = 'separators_outputs_gas_nozzle_parameters'
    id = db.Column(db.Integer, primary_key=True)
    separator_tag = db.Column(db.String, db.ForeignKey("separators.tag"), nullable=False)
    gasnozzlevelocity = db.Column(db.Float, nullable=False)
    gasnozzlemomentum = db.Column(db.Float, nullable=False)
    maximumgasnozzlevelocity = db.Column(db.Float, nullable=False)
    maximumgasnozzlemomentum = db.Column(db.Float, nullable=False)
    maximumgasnozzleflow = db.Column(db.Float, nullable=False) 
    statusgasnozzle = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<SeparatorOutputGasNozzleParameters {self.separator_tag}>'
        
    def serialize(self):
        return {
            "id": self.id,
            "separator_tag": self.separator_tag,
            "gasnozzlevelocity": self.gasnozzlevelocity,
            "gasnozzlemomentum": self.gasnozzlemomentum,
            "maximumgasnozzlevelocity": self.maximumgasnozzlevelocity,
            "maximumgasnozzlemomentum": self.maximumgasnozzlemomentum,
            "maximumgasnozzleflow": self.maximumgasnozzleflow,
            "statusgasnozzle": self.statusgasnozzle
            
        }

# ## separators_outputs_liquid_nozzle_parameters
class SeparatorOutputLiquidNozzleParameters(db.Model):
    __tablename__ = 'separators_outputs_liquid_nozzle_parameters'
    id = db.Column(db.Integer, primary_key=True)
    separator_tag = db.Column(db.String, db.ForeignKey("separators.tag"), nullable=False)
    liquidnozzlevelocity = db.Column(db.Float, nullable=False)   
    maximumliquidnozzlevelocity = db.Column(db.Float, nullable=False)   
    maximumliquidnozzleflow = db.Column(db.Float, nullable=False) 
    statusliquidnozzle = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<SeparatorOutputLiquidNozzleParameters {self.separator_tag}>'
        
    def serialize(self):
        return {
            "id": self.id,
            "separator_tag": self.separator_tag,
            "liquidnozzlevelocity": self.liquidnozzlevelocity,          
            "maximumliquidnozzlevelocity": self.maximumliquidnozzlevelocity,           
            "maximumliquidnozzleflow": self.maximumliquidnozzleflow,
            "statusliquidnozzle": self.statusliquidnozzle
            
        }

# ## separators_outputs_vessel_gas_capacity_parameters
class SeparatorOutputVesselGasCapacityParameters(db.Model):
    __tablename__ = 'separators_outputs_vessel_gas_capacity_parameters'
    id = db.Column(db.Integer, primary_key=True)
    separator_tag = db.Column(db.String, db.ForeignKey("separators.tag"), nullable=False)
    gasloadfactor = db.Column(db.Float, nullable=False)   
    maximumgasflowathhlevel = db.Column(db.Float, nullable=False)   
    maximumgasflowatnormallevel = db.Column(db.Float, nullable=False) 
    statusgascapacityathighlevel = db.Column(db.String(80), nullable=False)
    statusgascapacityatnormallevel = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<SeparatorOutputVesselGasCapacityParameters {self.separator_tag}>'
        
    def serialize(self):
        return {
            "id": self.id,
            "separator_tag": self.separator_tag,
            "gasloadfactor": self.gasloadfactor,          
            "maximumgasflowathhlevel": self.maximumgasflowathhlevel,           
            "maximumgasflowatnormallevel": self.maximumgasflowatnormallevel,
            "statusgascapacityathighlevel": self.statusgascapacityathighlevel,
            "statusgascapacityatnormallevel": self.statusgascapacityatnormallevel
            
        }

# ## separators_outputs_vessel_liquid_capacity_parameters
class SeparatorOutputVesselLiquidCapacityParameters(db.Model):
    __tablename__ = 'separators_outputs_vessel_liquid_capacity_parameters'
    id = db.Column(db.Integer, primary_key=True)
    separator_tag = db.Column(db.String, db.ForeignKey("separators.tag"), nullable=False)
    maximumvesselliquidflowcapacityatnormallevel = db.Column(db.Float, nullable=False)   
    statusvesselliquidcapacity = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<SeparatorOutputVesselLiquidCapacityParameters {self.separator_tag}>'
        
    def serialize(self):
        return {
            "id": self.id,
            "separator_tag": self.separator_tag,
            "maximumvesselliquidflowcapacityatnormallevel": self.maximumvesselliquidflowcapacityatnormallevel,          
            "statusvesselliquidcapacity": self.statusvesselliquidcapacity
            
        }

# ## separators_outputs_relief_valve_parameters
class SeparatorOutputReliefValveParameters(db.Model):
    __tablename__ = 'separators_outputs_relief_valve_parameters'
    id = db.Column(db.Integer, primary_key=True)
    separator_tag = db.Column(db.String, db.ForeignKey("separators.tag"), nullable=False)
    reliefvalvecapacity = db.Column(db.Float, nullable=False)   
    reliefvalvecapacitystatus = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<SeparatorOutputReliefValveParameters {self.separator_tag}>'
        
    def serialize(self):
        return {
            "id": self.id,
            "separator_tag": self.separator_tag,
            "reliefvalvecapacity": self.reliefvalvecapacity,          
            "reliefvalvecapacitystatus": self.reliefvalvecapacitystatus
            
        }

# ## separators_outputs_level_control_valve_parameters
class SeparatorOutputLevelControlValveParameters(db.Model):
    __tablename__ = 'separators_outputs_level_control_valve_parameters'
    id = db.Column(db.Integer, primary_key=True)
    separator_tag = db.Column(db.String, db.ForeignKey("separators.tag"), nullable=False)
    lcvliquidflowcapacity = db.Column(db.Float, nullable=False)   
    levelvalverequiredcv = db.Column(db.Float, nullable=False)
    levelcontrolvalvestatus = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<SeparatorOutputLevelControlValveParameters {self.separator_tag}>'
        
    def serialize(self):
        return {
            "id": self.id,
            "separator_tag": self.separator_tag,
            "lcvliquidflowcapacity": self.lcvliquidflowcapacity,          
            "levelvalverequiredcv": self.levelvalverequiredcv,
            "levelcontrolvalvestatus": self.levelcontrolvalvestatus
            
        }
