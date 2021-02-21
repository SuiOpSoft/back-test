from api.models import db, SeparatorInputDataSeparator, SeparatorOutputGasAndLiquidAreas
import math

def gas_and_liquid_areas_calc():
    dataseparator = db.session.query(SeparatorInputDataSeparator).one()
    print(dataseparator.ttlength)

    HHl=dataseparator.highleveltrip
    Nl=dataseparator.normalliquidlevel
    Ll=dataseparator.lowlevelalarm
    Diam=dataseparator.internaldiameter
    Length=dataseparator.ttlength
    INd=dataseparator.inletnozzle
    GOn=dataseparator.gasoutletnozzle
    LOn=dataseparator.liquidoutletnozzle

    Pi = 3.14159265358979
    print(Length)
    Area_Sep  = Pi * float(Diam)**2/(4*10**6)
    Radio = float(Diam)/2
    INArea = Pi * float(INd)**2/(4*10**6)
    GONArea  = Pi * float(GOn)**2/(4*10**6)
    LONArea  = Pi * float(LOn)**2/(4*10**6)
    ABS_R_Hh = abs(Radio-float(HHl))
    ABS_R_Nl = abs(Radio-float(Nl))
    ABS_R_Ll = abs(Radio-float(Ll))
    AHh=2.0*math.acos(ABS_R_Hh/Radio)
    ANl=2.0*math.acos(ABS_R_Nl/Radio)
    ALl=2.0*math.acos(ABS_R_Ll/Radio)
    TAHh=0.5*ABS_R_Hh*float(Diam)*math.sin(AHh/2.0)/1.0e+6
    TANl=0.5*ABS_R_Nl*float(Diam)*math.sin(ANl/2.0)/1.0e+6
    TALl=0.5*ABS_R_Ll*float(Diam)*math.sin(ALl/2.0)/1.0e+6
    if float(HHl)>Radio: 
        LA_Hh=Radio**2/2.0*(2*Pi-AHh)/1.0E+6+TAHh 
    else: 
        LA_Hh=Radio**2/2.0*AHh/1.0E+6-TAHh
    if float(Nl)>Radio: 
        LA_Nl=Radio**2/2.0*(2*Pi-ANl)/1.0E+6+TANl
    else:
        LA_Nl=Radio**2/2.0*ANl/1.0E+6-TANl
    if float(Ll)>Radio: 
        LA_Ll=Radio**2/2.0*(2*Pi-ALl)/1.0E+6+TALl
    else: 
        LA_Ll=Radio**2/2.0*ALl/1.0E+6-TALl

    GA_Hh=Area_Sep-LA_Hh
    GA_Nl=Area_Sep-LA_Nl
    GA_Ll=Area_Sep-LA_Ll

    separatorgasandliquidareas = SeparatorOutputGasAndLiquidAreas(id="1", separator_id="1", separatorcrosssectionalarearatio=str(format(Radio, ".2f")), separatorcrosssectionalarea=str(round(Area_Sep, 2)), inletnozzlearea=str(format(INArea, ".2f")),
                                                                    gasnozzlearea=str(GONArea), liquidnozzlearea=str(LONArea), highleveltripgasarea=str(GA_Hh), normallevelgasarea=str(GA_Nl), lowlevelgasarea=str(GA_Ll),
                                                                    highleveltripliquidarea=str(LA_Hh), normalleveltriparea=str(LA_Nl), lowleveltripliquidarea=str(LA_Ll))

    db.session.add(separatorgasandliquidareas)
    db.session.commit()