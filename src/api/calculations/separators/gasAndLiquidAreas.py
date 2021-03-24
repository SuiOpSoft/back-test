from api.models import db, SeparatorInputDataSeparator, SeparatorOutputGasAndLiquidAreas
from flask import Flask,jsonify
import math

def gas_and_liquid_areas_calc():
    dataseparators = SeparatorInputDataSeparator.query.all()

    for dataseparator in dataseparators:
        SeparatorOutputGasAndLiquidAreas.query.filter(SeparatorOutputGasAndLiquidAreas.separator_tag == dataseparator.separator_tag).delete()
        
        HHl=dataseparator.highleveltrip
        if HHl == '' or HHl == 0:
            return "Empty Separator param."
        Nl=dataseparator.normalliquidlevel
        if Nl == '' or Nl == 0:
            return "Empty Separator param."
        Ll=dataseparator.lowlevelalarm
        if Ll == '' or Ll == 0:
            return "Empty Separator param."
        Diam=dataseparator.internaldiameter
        if Diam == '' or Diam == 0:
            return "Empty Separator param."
        Length=dataseparator.ttlength
        if Length == '' or Length == 0:
            return "Empty Separator param."
        INd=dataseparator.inletnozzle
        if INd == '' or INd == 0:
            return "Empty Separator param."
        GOn=dataseparator.gasoutletnozzle
        if GOn == '' or GOn == 0:
            return "Empty Separator param."
        LOn=dataseparator.liquidoutletnozzle
        if LOn == '' or LOn == 0:
            return "Empty Separator param."

        Pi = 3.14159265358979
        Area_Sep  = Pi * Diam**2/(4*10**6)
        Radio = Diam/2
        INArea = Pi * INd**2/(4*10**6)
        GONArea  = Pi * GOn**2/(4*10**6)
        LONArea  = Pi * LOn**2/(4*10**6)
        ABS_R_Hh = abs(Radio-HHl)
        ABS_R_Nl = abs(Radio-Nl)
        ABS_R_Ll = abs(Radio-Ll)
        AHh=2.0*math.acos(ABS_R_Hh/Radio)
        ANl=2.0*math.acos(ABS_R_Nl/Radio)
        ALl=2.0*math.acos(ABS_R_Ll/Radio)
        TAHh=0.5*ABS_R_Hh*Diam*math.sin(AHh/2.0)/1.0e+6
        TANl=0.5*ABS_R_Nl*Diam*math.sin(ANl/2.0)/1.0e+6
        TALl=0.5*ABS_R_Ll*Diam*math.sin(ALl/2.0)/1.0e+6
        if HHl>Radio: 
            LA_Hh=Radio**2/2.0*(2*Pi-AHh)/1.0E+6+TAHh 
        else: 
            LA_Hh=Radio**2/2.0*AHh/1.0E+6-TAHh
        if Nl>Radio: 
            LA_Nl=Radio**2/2.0*(2*Pi-ANl)/1.0E+6+TANl
        else:
            LA_Nl=Radio**2/2.0*ANl/1.0E+6-TANl
        if Ll>Radio: 
            LA_Ll=Radio**2/2.0*(2*Pi-ALl)/1.0E+6+TALl
        else: 
            LA_Ll=Radio**2/2.0*ALl/1.0E+6-TALl

        GA_Hh=Area_Sep-LA_Hh
        GA_Nl=Area_Sep-LA_Nl
        GA_Ll=Area_Sep-LA_Ll

        separatorgasandliquidareas = SeparatorOutputGasAndLiquidAreas(separator_tag=dataseparator.separator_tag, separatorcrosssectionalarearatio=format(Radio, ".2f"), separatorcrosssectionalarea=format(Area_Sep, ".4f"), inletnozzlearea=format(INArea, ".4f"),
                                                                        gasnozzlearea=format(GONArea, ".4f"), liquidnozzlearea=format(LONArea, ".4f"), highleveltripgasarea=format(GA_Hh,".4f"), normallevelgasarea=format(GA_Nl, ".4f"), lowlevelgasarea=format(GA_Ll, ".4f"),
                                                                        highleveltripliquidarea=format(LA_Hh, ".4f"), normalleveltriparea=format(LA_Nl, ".4f"), lowleveltripliquidarea=format(LA_Ll, ".4f"))

        db.session.add(separatorgasandliquidareas)
        db.session.commit()
