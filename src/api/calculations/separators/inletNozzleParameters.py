from api.models import db, SeparatorInputDataSeparator, SeparatorInputDataFluid, SeparatorOutputInletNozzleParameters
import math

def inlet_nozzle_parameters_calc():
    datafluids = SeparatorInputDataFluid.query.all()
    dataseparators = SeparatorInputDataSeparator.query.all()


    for datafluid in datafluids:
        for dataseparator in dataseparators:
            SeparatorOutputInletNozzleParameters.query.filter(SeparatorOutputInletNozzleParameters.separator_tag == datafluid.separator_tag).delete()

    AGf = datafluid.actualgasflow
    ALf = datafluid.actualliquidflow
    Md = datafluid.mixturedensity

##REQUIRED DATA FROM SEPARATOR DATA PARAMETERS
    INd=dataseparator.inletnozzle
    InletDevice = "NID"

    MaxIm=0
    INCap=""
    INAr = 3.14159265358979/4*(float(INd)/1000)**2
    MIv = (float(AGf) + float(ALf))/(3600*INAr)
    Im = float(Md) * MIv**2

    if (InletDevice == "NID"): 
        MaxIm=1500
    if (InletDevice == "HOP"): 
        MaxIm=2100
    if (InletDevice == "SP"): 
        MaxIm=8000

    MaxMIv = math.sqrt(MaxIm/float(Md))
    MaxALf = MaxMIv/MIv*float(ALf)
    MaxAGf = MaxMIv/MIv*float(AGf)
    if(Im > MaxIm): 
        INCap = "Exceeded" 
    else: INCap = "OK"


    separatorgasandliquidareas = SeparatorOutputInletNozzleParameters(separator_tag=datafluid.separator_tag, mixtureinletnozzlevelocity = float(format(MIv, ".2f")), inletnozzlemomentum = float(format(Im, ".2f")), maximummixtureinletnozzlevelocity = float(format(MaxMIv, ".2f")),
                                                                    maximuminletnozzlemomentum = float(MaxIm), maximumliquidflowinletnozzle = float(format(MaxALf, ".2f")), maximumgasflowinletnozzle = float(format(MaxAGf, ".2f")), statusinletnozzle = INCap)

    db.session.add(separatorgasandliquidareas)
    db.session.commit()