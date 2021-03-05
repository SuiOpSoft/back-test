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
            Gd = datafluid.gasdensity

            #REQUIRED DATA FROM OUTPUT SEPARATOR GAS AND LIQUID AREAS INCLUDING NOZZLE AREAS
            GONArea = gasliquid.gasnozzlearea

            GOv = float(AGf) / (3600 * float(GONArea))
            Gm = float(Gd) * GOv ** 2
            MaxGm = 4500
            MaxGOv = math.sqrt(MaxGm / float(Gd))
            MaxAGf_GO = (MaxGOv / GOv) * float(AGf)
            if (Gm > MaxGm):
              GOCap = "Exceeded"
            else:
              GOCap = "OK"

            separatoroutputgasnozzle = SeparatorOutputGasNozzleParameters(separator_tag=datafluid.separator_tag, gasnozzlevelocity=str(format(GOv, ".2f")), gasnozzlemomentum=str(format(Gm, ".2f")), 
                                                                            maximumgasnozzlevelocity=str(format(MaxGOv, ".2f")), maximumgasnozzlemomentum=str(format(MaxGm, ".2f")), maximumgasnozzleflow=str(format(MaxAGf_GO, ".2f")), 
                                                                            statusgasnozzle=GOCap)

            db.session.add(separatoroutputgasnozzle)
            db.session.commit()
