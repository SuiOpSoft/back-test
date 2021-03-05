from api.models import db, SeparatorInputDataSeparator, SeparatorOutputGasAndLiquidAreas
import math

def gas_and_liquid_areas_calc():
    dataseparators = SeparatorInputDataSeparator.query.all()

    for dataseparator in dataseparators:
        SeparatorOutputGasAndLiquidAreas.query.filter(SeparatorOutputGasAndLiquidAreas.separator_tag == dataseparator.separator_tag).delete()
        
        HHl=dataseparator.highleveltrip
        Nl=dataseparator.normalliquidlevel
        Ll=dataseparator.lowlevelalarm
        Diam=dataseparator.internaldiameter
        Length=dataseparator.ttlength
        INd=dataseparator.inletnozzle
        GOn=dataseparator.gasoutletnozzle
        LOn=dataseparator.liquidoutletnozzle

        Pi = 3.14159265358979
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

        separatorgasandliquidareas = SeparatorOutputGasAndLiquidAreas(separator_tag=dataseparator.separator_tag, separatorcrosssectionalarearatio=str(format(Radio, ".2f")), separatorcrosssectionalarea=str(format(Area_Sep, ".2f")), inletnozzlearea=str(format(INArea, ".2f")),
                                                                        gasnozzlearea=str(format(GONArea, ".2f")), liquidnozzlearea=str(format(LONArea, ".2f")), highleveltripgasarea=str(format(GA_Hh,".2f")), normallevelgasarea=str(format(GA_Nl, ".2f")), lowlevelgasarea=str(format(GA_Ll, ".2f")),
                                                                        highleveltripliquidarea=str(format(LA_Hh, ".2f")), normalleveltriparea=str(format(LA_Nl, ".2f")), lowleveltripliquidarea=str(format(LA_Ll, ".2f")))

        db.session.add(separatorgasandliquidareas)
        db.session.commit()