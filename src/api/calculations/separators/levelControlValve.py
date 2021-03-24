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
            if ALf == '' or ALf == '-':
                return "Empty Fluids param."
            LVp = datafluid.liquidvaporpressure
            if LVp == '' or LVp == '-':
                return "Empty Fluids param."
            LCp = datafluid.liquidcriticalpressure
            if LCp == '' or LCp == '-':
                return "Empty Fluids param."
            Ld = datafluid.oildensity
            if Ld == '' or Ld == '-':
                return "Empty Fluids param."
            #LEVEL CONTROL VALVE DATA - PARAMETERS
            LCV_Cv = datalevel.lcvcv
            if LCV_Cv == '' or LCV_Cv == '-':
                return "Empty Level Control Valve param."
            LCV_Pi = datalevel.lcvinletpressure
            if LCV_Pi == '' or LCV_Pi == '-':
                return "Empty Level Control Valve param."
            LCV_Po = datalevel.lcvoutletpressure
            if LCV_Po == '' or LCV_Po == '-':
                return "Empty Level Control Valve param."    
            LCV_Fl = datalevel.lcvfactorfl
            if LCV_Fl == '' or LCV_Fl == '-':
                return "Empty Level Control Valve param."
            LCV_Fp = datalevel.lcvfactorfp
            if LCV_Fp == '' or LCV_Fp == '-':
                return "Empty Level Control Valve param."
            #LEVEL CONTROL VALVE CAPACITY CALCULATIONS
            Alf1 = (float(ALf) * 264.172) / 60.0
            P1p = float(LCV_Pi) * 0.145033
            P2p = float(LCV_Po) * 0.145033
            Pvp = float(LVp) * 0.145033
            Pcp = float(LCp) * 0.145033
            Ff = 0.96 - 0.28 * math.sqrt(Pvp / Pcp) 
            # DPchoke=LCV_Fl^2*(P1p-Ff*Pvp)
            DPchoke = (float(LCV_Fl) ** 2) * (P1p - Ff * Pvp)
            print("DPSHoke", DPchoke)
            DPv = P1p - P2p
            if DPv <= DPchoke:
                print("ENTRA 1")
                # LCV_Cvreq=Alf1/LCV_Fp*Math.sqrt((Ld/1000)/DPv)
                LCV_Cvreq = (Alf1 / float(LCV_Fp)) * math.sqrt((float(Ld) / 1000) / DPv)
                print(LCV_Cvreq)
            else:
                print("ENTRA 2")
                # {LCV_Cvreq=Alf1/LCV_Fp*Math.sqrt((Ld/1000)/DPchoke)}
                LCV_Cvreq = (Alf1 / float(LCV_Fp)) * math.sqrt((float(Ld) / 1000) / DPchoke)
                print(LCV_Cvreq)

            LCV_MaxAlf = (float(ALf) * float(LCV_Cv)) / LCV_Cvreq
            if (LCV_Cvreq > float(LCV_Cv)):
                LCV_Status = "Exceeded"
            else:
                LCV_Status = "OK"
            separatoroutputlevelcontrolvalve = SeparatorOutputLevelControlValveParameters(separator_tag=datafluid.separator_tag, lcvliquidflowcapacity=str(format(LCV_MaxAlf, ".2f")), 
                                                                                                  levelvalverequiredcv=str(format(LCV_Cvreq, ".2f")), levelcontrolvalvestatus=LCV_Status)
            db.session.add(separatoroutputlevelcontrolvalve)
            db.session.commit()
