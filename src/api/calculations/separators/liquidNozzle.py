from api.models import db, SeparatorInputDataFluid, SeparatorOutputGasAndLiquidAreas, SeparatorOutputLiquidNozzleParameters
import math
  
def liquid_nozzle_calc():
    datafluids = SeparatorInputDataFluid.query.all()
    gasliquids = SeparatorOutputGasAndLiquidAreas.query.all()

    for datafluid in datafluids:
        for gasliquid in gasliquids:
            SeparatorOutputLiquidNozzleParameters.query.filter(SeparatorOutputLiquidNozzleParameters.separator_tag == datafluid.separator_tag).delete()

            #REQUIRED DATA FROM FLUID DATA PARAMETERS
            ALf = datafluid.actualliquidflow
            if ALf == '' or ALf == '-':
                return "Empty Fluids param."

            #REQUIRED DATA FROM OUTPUT SEPARATOR GAS AND LIQUID AREAS INCLUDING NOZZLE AREAS
            LONArea = gasliquid.liquidnozzlearea
            if LONArea == '' or LONArea == '-':
                return "Empty Liquid Nozzle param."

            MaxLOv = 1
            LOv = float(ALf) / (3600 * float(LONArea))
            MaxALf_LO = MaxLOv * float(LONArea) * 3600
            if (LOv > MaxLOv):
              LOCap = "Exceeded"
            else:
              LOCap = "OK"

            separatoroutputliquidnozzle = SeparatorOutputLiquidNozzleParameters(separator_tag=datafluid.separator_tag, liquidnozzlevelocity=str(format(LOv, ".2f")), 
                                                                                maximumliquidnozzlevelocity=str(format(MaxLOv, ".2f")), maximumliquidnozzleflow=str(format(MaxALf_LO, ".2f")), statusliquidnozzle=LOCap)

            db.session.add(separatoroutputliquidnozzle)
            db.session.commit()