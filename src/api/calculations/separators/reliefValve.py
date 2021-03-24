from api.models import db, SeparatorInputDataFluid, SeparatorInputDataReliefValve, SeparatorOutputReliefValveParameters
import math

def relief_valve_calc():
    datafluids = SeparatorInputDataFluid.query.all()
    datavalves = SeparatorInputDataReliefValve.query.all()

    for datafluid in datafluids:
        for datavalve in datavalves:
            SeparatorOutputReliefValveParameters.query.filter(SeparatorOutputReliefValveParameters.separator_tag == datafluid.separator_tag).delete()

            #RELIEF VALVE DATA - PARAMETERS
            RVOrifice = datavalve.rvorificearea
            if RVOrifice == '' or RVOrifice == 0:
                return "Empty Relief Valve param."
            RVPress = datavalve.rvsetpressure
            if RVPress == '' or RVPress == 0:
                return "Empty Relief Valve param."
            
            #REQUIRED DATA FROM FLUID DATA PARAMETERS
            Tr = datafluid.operatingtemperature
            if Tr == '' or Tr == 0:
                return "Empty Fluids param."
            Zg = datafluid.gascomprz
            if Zg == '' or Zg == 0:
                return "Empty Fluids param."
            GMw = datafluid.gasmw
            if GMw == '' or GMw == 0:
                return "Empty Fluids param."
            SGf = datafluid.standardgasflow
            if SGf == '' or SGf == 0:
                return "Empty Fluids param."
            AGf = datafluid.actualgasflow
            if AGf == '' or AGf == 0:
                return "Empty Fluids param."
            kg = datafluid.liquidsurfacetension
            if kg == '' or kg == 0:
                return "Empty Fluids param."
            
            Cf = 520 * (kg * (2 / (kg + 1)) ** ((kg + 1) / (kg - 1))) ** 0.5
            RvCap = (2502.69264 * RVOrifice * Cf * ((RVPress * 1.1) / 100 + 1)) / math.sqrt((Tr + 273.15) * Zg * GMw)
            RvCap = (RvCap * AGf) / (SGf * 24)
            if (AGf > RvCap):
              RV_Status = "Exceeded"
            else:
              RV_Status = "OK"
    
            separatoroutputreliefvalve = SeparatorOutputReliefValveParameters(separator_tag=datafluid.separator_tag, reliefvalvecapacity=format(RvCap, ".2f"), 
                                                                                                  reliefvalvecapacitystatus=RV_Status)
    
            db.session.add(separatoroutputreliefvalve)
            db.session.commit()
        