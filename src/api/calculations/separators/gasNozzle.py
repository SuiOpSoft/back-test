from api.models import db, SeparatorInputDataFluid, SeparatorOutputGasAndLiquidAreas, SeparatorOutputGasNozzleParameters
import math
  
def gas_nozzle_calc():
    datafluids = SeparatorInputDataFluid.query.all()
    gasliquids = SeparatorOutputGasAndLiquidAreas.query.all()

    for datafluid in datafluids:
        for gasliquid in gasliquids:
            SeparatorOutputGasNozzleParameters.query.filter(SeparatorOutputGasNozzleParameters.separator_tag == datafluid.separator_tag).delete()
            
            #REQUIRED DATA FROM FLUID DATA PARAMETERS
            AGf = datafluid.actualgasflow
            if AGf == '' or AGf == 0:
                return "Empty Fluids param."
            Gd = datafluid.gasdensity
            if Gd == '' or Gd == 0:
                return "Empty Fluids param."

            #REQUIRED DATA FROM OUTPUT SEPARATOR GAS AND LIQUID AREAS INCLUDING NOZZLE AREAS
            GONArea = gasliquid.gasnozzlearea
            if GONArea == '' or GONArea == 0:
                return "Empty Gas Nozzle param."

            GOv = AGf / (3600 * GONArea)
            Gm = Gd * GOv ** 2
            MaxGm = 4500
            MaxGOv = math.sqrt(MaxGm / Gd)
            MaxAGf_GO = (MaxGOv / GOv * AGf)
            if (Gm > MaxGm):
              GOCap = "Exceeded"
            else:
              GOCap = "OK"

            separatoroutputgasnozzle = SeparatorOutputGasNozzleParameters(separator_tag=datafluid.separator_tag, gasnozzlevelocity=format(GOv, ".2f"), gasnozzlemomentum=format(Gm, ".2f"), 
                                                                            maximumgasnozzlevelocity=format(MaxGOv, ".2f"), maximumgasnozzlemomentum=format(MaxGm, ".2f"), maximumgasnozzleflow=format(MaxAGf_GO, ".2f"), 
                                                                            statusgasnozzle=GOCap)

            db.session.add(separatoroutputgasnozzle)
            db.session.commit()
