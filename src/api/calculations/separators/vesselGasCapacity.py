from api.models import db, SeparatorInputDataSeparator, SeparatorInputDataFluid, SeparatorOutputGasAndLiquidAreas, SeparatorOutputVesselGasCapacityParameters
import math
  
def vessel_gas_capacity_calc():
    datafluids = SeparatorInputDataFluid.query.all()
    dataseparators = SeparatorInputDataSeparator.query.all()
    gasliquids = SeparatorOutputGasAndLiquidAreas.query.all()

    for datafluid in datafluids:
        for dataseparator in dataseparators:
            for gasliquid in gasliquids:
                SeparatorOutputVesselGasCapacityParameters.query.filter(SeparatorOutputVesselGasCapacityParameters.separator_tag == datafluid.separator_tag).delete()

                Param1 = 0
                Param2 = 0
                #REQUIRED DATA FROM FLUID DATA PARAMETERS
                AGf = datafluid.actualgasflow
                if AGf == '' or AGf == 0:
                    return "Empty Fluids param."
                Ld = datafluid.oildensity
                if Ld == '' or Ld == 0:
                    return "Empty Fluids param."
                Gd = datafluid.gasdensity
                if Gd == '' or Gd == 0:
                    return "Empty Fluids param."

                #REQUIRED DATA FROM SEPARATOR DATA PARAMETERS
                InletDevice = dataseparator.inletdevicetype
                if InletDevice == '' or InletDevice == 0:
                    return "Empty Separator param."
                Demister = dataseparator.demistertype
                if Demister == '' or Demister == 0:
                    return "Empty Separator param."

                #REQUIRED DATA FROM OUTPUT SEPARATOR GAS AND LIQUID AREAS INCLUDING NOZZLE AREAS
                GA_Hh = gasliquid.highleveltripgasarea
                GA_Nl = gasliquid.normallevelgasarea

                if (InletDevice == "NID"):
                  Param1 = 0.96
                if (InletDevice == "HOP"):
                  Param1 = 0.97
                if (InletDevice == "SP"):
                  Param1 = 0.98
                if (Demister == "KO"):
                  Param2 = 0.06
                if (Demister == "VD"):
                  Param2 = 0.07
                if (Demister == "HD"):
                  Param2 = 0.08
                if (Demister == "HVD"):
                  Param2 = 0.1
                GasLoadFactor = Param1 * Param2
                AreaHh1 = GasLoadFactor * GA_Hh
                AreaNl2 = GasLoadFactor * GA_Nl
                MaxAGfV1 = (AreaHh1 / math.sqrt(Gd / (Ld - Gd))) * 3600
                MaxAGfV2 = (AreaNl2 / math.sqrt(Gd / (Ld - Gd))) * 3600
                if (AGf > MaxAGfV1):
                  VGasCap1 = "Criterio HH level Exceeded"
                else:
                  VGasCap1 = "Criterio HH level OK"
                if (AGf > MaxAGfV2):
                  VGasCap2 = "Criterio Normal level Exceeded"
                else:
                  VGasCap2 = "Criterio Normal level OK"


                separatoroutputvesselgas = SeparatorOutputVesselGasCapacityParameters(separator_tag=datafluid.separator_tag, gasloadfactor=format(GasLoadFactor, ".2f"), 
                                                                                              maximumgasflowathhlevel=format(MaxAGfV1, ".2f"), maximumgasflowatnormallevel=format(MaxAGfV2, ".2f"), 
                                                                                              statusgascapacityathighlevel=VGasCap1, statusgascapacityatnormallevel=VGasCap2)

                db.session.add(separatoroutputvesselgas)
                db.session.commit()
