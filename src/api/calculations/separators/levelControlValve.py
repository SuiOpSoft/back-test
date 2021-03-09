from api.models import db, SeparatorInputDataFluid, SeparatorInputDataLevelControlValve, SeparatorOutputLevelControlValveParameters
import math
import sys
from decimal import Decimal

def level_control_calc():
    datafluids = SeparatorInputDataFluid.query.all()
    datalevels = SeparatorInputDataLevelControlValve.query.all()

    for datafluid in datafluids:
        for datalevel in datalevels:
            SeparatorOutputLevelControlValveParameters.query.filter(SeparatorOutputLevelControlValveParameters.separator_tag == datafluid.separator_tag).delete()
            
            #REQUIRED DATA FROM FLUID DATA PARAMETERS
            ALf = datafluid.actualliquidflow
            LVp = datafluid.liquidvaporpressure
            LCp = datafluid.liquidcriticalpressure
            Ld = datafluid.oildensity
            #LEVEL CONTROL VALVE DATA - PARAMETERS
            LCV_Cv = datalevel.lcvcv
            LCV_Pi = datalevel.lcvinletpressure
            LCV_Po = datalevel.lcvoutletpressure
            LCV_Fl = datalevel.lcvfactorfl
            LCV_Fp = datalevel.lcvfactorfp
            #LEVEL CONTROL VALVE CAPACITY CALCULATIONS
            Alf1 = (float(ALf) * 264.172) / 60.0
            P1p = float(LCV_Pi) * 0.145033
            P2p = float(LCV_Po) * 0.145033
            Pvp = float(LVp) * 0.145033
            Pcp = float(LCp) * 0.145033
            Ff = 0.96 - 0.28 * math.sqrt(Pvp / Pcp) 
            DPchoke = Decimal(LCV_Fl) ** Decimal(2 * (P1p - Ff * Pvp))
            DPv = P1p - P2p
            if DPv <= DPchoke:
                LCV_Cvreq = (Alf1 / float(LCV_Fp)) * math.sqrt(Decimal(Ld) / 1000 / DPv)
            else:
                LCV_Cvreq = (Alf1 / float(LCV_Fp)) * math.sqrt(Decimal(Ld) / 1000 / DPchoke)

            LCV_MaxAlf = (float(ALf) * float(LCV_Cv)) / LCV_Cvreq
            if (LCV_Cvreq > float(LCV_Cv)):
                LCV_Status = "Exceeded"
            else:
                LCV_Status = "OK"
            separatoroutputlevelcontrolvalve = SeparatorOutputLevelControlValveParameters(separator_tag=datafluid.separator_tag, lcvliquidflowcapacity=str(format(LCV_MaxAlf, ".2f")), 
                                                                                                  levelvalverequiredcv=str(format(LCV_Cvreq, ".2f")), levelcontrolvalvestatus=LCV_Status)
            db.session.add(separatoroutputlevelcontrolvalve)
            db.session.commit()
