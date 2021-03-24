from api.models import db, SeparatorInputDataSeparator, SeparatorInputDataFluid, SeparatorOutputInletNozzleParameters
import math
from flask import Flask,jsonify

def inlet_nozzle_parameters_calc():
    datafluids = SeparatorInputDataFluid.query.all()
    dataseparators = SeparatorInputDataSeparator.query.all()


    for datafluid in datafluids:
        for dataseparator in dataseparators:
            SeparatorOutputInletNozzleParameters.query.filter(SeparatorOutputInletNozzleParameters.separator_tag == datafluid.separator_tag).delete()

            AGf = datafluid.actualgasflow
            if AGf == '' or AGf == 0:
                return "Empty Fluids param."
            ALf = datafluid.actualliquidflow
            if ALf == '' or ALf == 0:
                return "Empty Fluids param."
            Md = datafluid.mixturedensity
            if Md == '' or Md == 0:
                return "Empty Fluids param."
        
            ##REQUIRED DATA FROM SEPARATOR DATA PARAMETERS
            INd=dataseparator.inletnozzle
            if INd == '' or INd == 0:
                return "Empty Separator param."
            InletDevice = dataseparator.inletdevicetype
            if InletDevice == '' or InletDevice == 0:
                return "Empty Separator param."
        
            MaxIm=0
            INCap=""
            INAr = 3.14159265358979/4*(INd/1000)**2
            MIv = (AGf + ALf)/(3600*INAr)
            Im = Md * MIv**2
        
            if (InletDevice == "NID"):
                MaxIm=1500
            if (InletDevice == "HOP"):
                MaxIm=2100
            if (InletDevice == "SP"):
                MaxIm=8000
        
            MaxMIv = math.sqrt(MaxIm/Md)
            MaxALf = MaxMIv/MIv*ALf
            MaxAGf = MaxMIv/MIv*AGf
            if(Im > MaxIm): 
                INCap = "Exceeded" 
            else: INCap = "OK"
        
        
            separatorgasandliquidareas = SeparatorOutputInletNozzleParameters(separator_tag=datafluid.separator_tag, mixtureinletnozzlevelocity = format(MIv, ".2f"), inletnozzlemomentum = format(Im, ".2f"), maximummixtureinletnozzlevelocity = format(MaxMIv, ".2f"),
                                                                            maximuminletnozzlemomentum = MaxIm, maximumliquidflowinletnozzle = format(MaxALf, ".2f"), maximumgasflowinletnozzle = format(MaxAGf, ".2f"), statusinletnozzle = INCap)
        
            db.session.add(separatorgasandliquidareas)
            db.session.commit()