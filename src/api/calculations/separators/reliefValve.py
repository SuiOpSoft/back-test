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
            if RVOrifice == '' or RVOrifice == '-':
                return "Empty Relief Valve param."
            RVPress = datavalve.rvsetpressure
            if RVPress == '' or RVPress == '-':
                return "Empty Relief Valve param."
            
            #REQUIRED DATA FROM FLUID DATA PARAMETERS
            Tr = datafluid.operatingtemperature
            if Tr == '' or Tr == '-':
                return "Empty Fluids param."
            Zg = datafluid.gascomprz
            if Zg == '' or Zg == '-':
                return "Empty Fluids param."
            GMw = datafluid.gasmw
            if GMw == '' or GMw == '-':
                return "Empty Fluids param."
            SGf = datafluid.standardgasflow
            if SGf == '' or SGf == '-':
                return "Empty Fluids param."
            AGf = datafluid.actualgasflow
            if AGf == '' or AGf == '-':
                return "Empty Fluids param."
            kg = datafluid.liquidsurfacetension
            if kg == '' or kg == '-':
                return "Empty Fluids param."
            
            Cf = 520 * (float(kg) * (2 / (float(kg) + 1)) ** ((float(kg) + 1) / (float(kg) - 1))) ** 0.5
            RvCap = (2502.69264 * float(RVOrifice) * Cf * ((float(RVPress) * 1.1) / 100 + 1)) / math.sqrt((float(Tr) + 273.15) * float(Zg) * float(GMw))
            RvCap = (RvCap * float(AGf)) / (float(SGf) * 24)
            if (float(AGf) > RvCap):
              RV_Status = "Exceeded"
            else:
              RV_Status = "OK"
    
            separatoroutputreliefvalve = SeparatorOutputReliefValveParameters(separator_tag=datafluid.separator_tag, reliefvalvecapacity=str(format(RvCap, ".2f")), 
                                                                                                  reliefvalvecapacitystatus=RV_Status)
    
            db.session.add(separatoroutputreliefvalve)
            db.session.commit()
        