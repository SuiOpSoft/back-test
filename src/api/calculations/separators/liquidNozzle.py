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
            if ALf == '' or ALf == 0:
                return "Empty Fluids param."

            #REQUIRED DATA FROM OUTPUT SEPARATOR GAS AND LIQUID AREAS INCLUDING NOZZLE AREAS
            LONArea = gasliquid.liquidnozzlearea
            if LONArea == '' or LONArea == 0:
                return "Empty Liquid Nozzle param."

            MaxLOv = 1
            LOv = ALf / (3600 * LONArea)
            MaxALf_LO = MaxLOv * LONArea * 3600
            if (LOv > MaxLOv):
              LOCap = "Exceeded"
            else:
              LOCap = "OK"

            separatoroutputliquidnozzle = SeparatorOutputLiquidNozzleParameters(separator_tag=datafluid.separator_tag, liquidnozzlevelocity=format(LOv, ".2f"), 
                                                                                maximumliquidnozzlevelocity=format(MaxLOv, ".2f"), maximumliquidnozzleflow=format(MaxALf_LO, ".2f"), statusliquidnozzle=LOCap)

            db.session.add(separatoroutputliquidnozzle)
            db.session.commit()