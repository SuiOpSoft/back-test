  
import os
from flask_admin import Admin
from .models import db, Company, User, Facility, Separator, SeparatorInputDataFluid, SeparatorInputDataSeparator, SeparatorOutputGasAndLiquidAreas, SeparatorOutputInletNozzleParameters, SeparatorInputDataReliefValve, SeparatorInputDataLevelControlValve, SeparatorOutputGasNozzleParameters, SeparatorOutputLiquidNozzleParameters, SeparatorOutputVesselGasCapacityParameters, SeparatorOutputVesselLiquidCapacityParameters, SeparatorOutputReliefValveParameters, SeparatorOutputLevelControlValveParameters
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(Company, db.session))
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Facility, db.session))
    admin.add_view(ModelView(Separator, db.session))
    admin.add_view(ModelView(SeparatorInputDataFluid, db.session))
    admin.add_view(ModelView(SeparatorInputDataSeparator, db.session))
    admin.add_view(ModelView(SeparatorInputDataReliefValve, db.session))
    admin.add_view(ModelView(SeparatorInputDataLevelControlValve, db.session))
    admin.add_view(ModelView(SeparatorOutputGasAndLiquidAreas, db.session))
    admin.add_view(ModelView(SeparatorOutputInletNozzleParameters, db.session))
    admin.add_view(ModelView(SeparatorOutputGasNozzleParameters, db.session))
    admin.add_view(ModelView(SeparatorOutputLiquidNozzleParameters, db.session))
    admin.add_view(ModelView(SeparatorOutputVesselGasCapacityParameters, db.session))
    admin.add_view(ModelView(SeparatorOutputVesselLiquidCapacityParameters, db.session))
    admin.add_view(ModelView(SeparatorOutputReliefValveParameters, db.session))
    admin.add_view(ModelView(SeparatorOutputLevelControlValveParameters, db.session))
    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))