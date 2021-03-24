from api.models import db, SeparatorInputDataSeparator, SeparatorInputDataFluid, SeparatorOutputGasAndLiquidAreas, SeparatorOutputVesselLiquidCapacityParameters
import math
  
def vessel_liquid_capacity_calc():
    datafluids = SeparatorInputDataFluid.query.all()
    dataseparators = SeparatorInputDataSeparator.query.all()
    gasliquids = SeparatorOutputGasAndLiquidAreas.query.all()

    for datafluid in datafluids:
        for dataseparator in dataseparators:
            for gasliquid in gasliquids:
                SeparatorOutputVesselLiquidCapacityParameters.query.filter(SeparatorOutputVesselLiquidCapacityParameters.separator_tag == datafluid.separator_tag).delete()

                #REQUIRED DATA FROM FLUID DATA PARAMETERS
                ALf = datafluid.actualliquidflow
                if ALf == '' or ALf == 0:
                    return "Empty Fluids param."

                #REQUIRED DATA FROM SEPARATOR DATA PARAMETERS
                Lenght = dataseparator.ttlength
                if Lenght == '' or Lenght == 0:
                    return "Empty Separator param."

                #REQUIRED DATA FROM OUTPUT SEPARATOR GAS AND LIQUID AREAS INCLUDING NOZZLE AREAS
                LA_Nl = gasliquid.normalleveltriparea
                LA_Ll = gasliquid.lowleveltripliquidarea

                Rt = 2
                SLv = ((LA_Nl - LA_Ll) * Lenght) / 1000
                MLf = (SLv / Rt) * 60

                if (ALf > MLf):
                  VLiqCap = "Exceeded"
                else:
                  VLiqCap = "OK"

                separatoroutputvesselliquid = SeparatorOutputVesselLiquidCapacityParameters(separator_tag=datafluid.separator_tag, maximumvesselliquidflowcapacityatnormallevel=format(MLf, ".2f"), 
                                                                                              statusvesselliquidcapacity=VLiqCap)

                db.session.add(separatoroutputvesselliquid)
                db.session.commit()
