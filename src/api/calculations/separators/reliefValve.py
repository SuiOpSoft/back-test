from api.models import db, SeparatorInputDataFluid, SeparatorInputDataReliefValve, SeparatorOutputReliefValveParameters
import math

def relief_valve_calc():
    datafluids = SeparatorInputDataFluid.query.all()
    datavalves = SeparatorInputDataReliefValve.query.all()

    for datafluid in datafluids:
        for datavalve in datavalves:

            #RELIEF VALVE DATA - PARAMETERS
            RVOrifice = datavalve.rvorificearea
            RVPress = datavalve.rvsetpressure
            
            #REQUIRED DATA FROM FLUID DATA PARAMETERS
            Tr = datafluid.operatingtemperature
            Zg = datafluid.gascomprz
            GMw = datafluid.gasmw
            SGf = datafluid.standardgasflow
            AGf = datafluid.actualgasflow
            kg = datafluid.liquidsurfacetension #Revisión!!!!!!
            
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
        