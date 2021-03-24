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
            if ALf == '' or ALf == 0:
                return "Empty Fluids param."
            LVp = datafluid.liquidvaporpressure
            if LVp == '' or LVp == 0:
                return "Empty Fluids param."
            LCp = datafluid.liquidcriticalpressure
            if LCp == '' or LCp == 0:
                return "Empty Fluids param."
            Ld = datafluid.oildensity
            if Ld == '' or Ld == 0:
                return "Empty Fluids param."
            #LEVEL CONTROL VALVE DATA - PARAMETERS
            LCV_Cv = datalevel.lcvcv
            if LCV_Cv == '' or LCV_Cv == 0:
                return "Empty Level Control Valve param."
            LCV_Pi = datalevel.lcvinletpressure
            if LCV_Pi == '' or LCV_Pi == 0:
                return "Empty Level Control Valve param."
            LCV_Po = datalevel.lcvoutletpressure
            if LCV_Po == '' or LCV_Po == 0:
                return "Empty Level Control Valve param."    
            LCV_Fl = datalevel.lcvfactorfl
            if LCV_Fl == '' or LCV_Fl == 0:
                return "Empty Level Control Valve param."
            LCV_Fp = datalevel.lcvfactorfp
            if LCV_Fp == '' or LCV_Fp == 0:
                return "Empty Level Control Valve param."
            #LEVEL CONTROL VALVE CAPACITY CALCULATIONS
            Alf1 = (ALf * 264.172) / 60.0
            P1p = LCV_Pi * 0.145033
            P2p = LCV_Po * 0.145033
            Pvp = LVp * 0.145033
            Pcp = LCp * 0.145033
            Ff = 0.96 - 0.28 * math.sqrt(Pvp / Pcp) 
            # DPchoke=LCV_Fl^2*(P1p-Ff*Pvp)
            DPchoke = (LCV_Fl ** 2) * (P1p - Ff * Pvp)
            DPv = P1p - P2p
            if DPv <= DPchoke:
                # LCV_Cvreq=Alf1/LCV_Fp*Math.sqrt((Ld/1000)/DPv)
                LCV_Cvreq = (Alf1 / LCV_Fp) * math.sqrt((Ld / 1000) / DPv)
            else:
                # {LCV_Cvreq=Alf1/LCV_Fp*Math.sqrt((Ld/1000)/DPchoke)}
                LCV_Cvreq = (Alf1 / LCV_Fp) * math.sqrt((Ld / 1000) / DPchoke)
            LCV_MaxAlf = (ALf * LCV_Cv) / LCV_Cvreq
            if (LCV_Cvreq > LCV_Cv):
                LCV_Status = "Exceeded"
            else:
                LCV_Status = "OK"
            separatoroutputlevelcontrolvalve = SeparatorOutputLevelControlValveParameters(separator_tag=datafluid.separator_tag, lcvliquidflowcapacity=format(LCV_MaxAlf, ".2f"), 
                                                                                                  levelvalverequiredcv=format(LCV_Cvreq, ".2f"), levelcontrolvalvestatus=LCV_Status)
            db.session.add(separatoroutputlevelcontrolvalve)
            db.session.commit()
