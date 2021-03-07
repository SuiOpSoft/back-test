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

                #REQUIRED DATA FROM SEPARATOR DATA PARAMETERS
                Lenght = dataseparator.ttlength

                #REQUIRED DATA FROM OUTPUT SEPARATOR GAS AND LIQUID AREAS INCLUDING NOZZLE AREAS
                LA_Nl = gasliquid.normalleveltriparea
                LA_Ll = gasliquid.lowleveltripliquidarea

                Rt = 2
                SLv = ((float(LA_Nl) - float(LA_Ll)) * float(Lenght)) / 1000
                MLf = (SLv / Rt) * 60

                if (float(ALf) > MLf):
                  VLiqCap = "Exceeded"
                else:
                  VLiqCap = "OK"

                separatoroutputvesselliquid = SeparatorOutputVesselLiquidCapacityParameters(separator_tag=datafluid.separator_tag, maximumvesselliquidflowcapacityatnormallevel=str(format(MLf, ".2f")), 
                                                                                              statusvesselliquidcapacity=str(format(VLiqCap, ".2f")))

                db.session.add(separatoroutputvesselliquid)
                db.session.commit()
