include("MadGraphControl/SUSY_SimplifiedModel_PreInclude.py")
# from GeneratorFilters.GeneratorFiltersConf import xAODPhotonFilter
# from GeneratorFilters.GeneratorFiltersConf import xAODMultiElecMuTauFilter
from MadGraphControl.MadGraphUtilsHelpers import get_physics_short


include("GeneratorFilters//xAODPhotonFilter_Common.py")
include("GeneratorFilters//xAODMultiElecMuTauFilter_Common.py")
include("GeneratorFilters//xAODMETFilter_Common.py")

JOName = get_physics_short()

# get the file name and split it on _ to extract relevant information
jobConfigParts = JOName.split("_")
print("jobConfigParts: ", jobConfigParts)

METCut = jobConfigParts[3]

mN2 = float(jobConfigParts[5])
mN1 = float(jobConfigParts[7])


jobOptProcess = jobConfigParts[8]


print("mN2: ", mN2, "\nmN1: ", mN1, "\nProcess: ", jobOptProcess, "\nMETCut: ", METCut)


higgsino = False
winobino = False
if jobOptProcess == "HH":
    higgsino = True
    jobOptProcess_evt_desc = "Higgsino"

    process = """
    generate p p > n2 n1         @1
    add process p p > n2 n1 j    @2
    add process p p > n2 n1 j j  @3
    add process p p > n2 x1+     @4
    add process p p > n2 x1+ j   @5
    add process p p > n2 x1+ j j @6
    add process p p > n2 x1-     @7
    add process p p > n2 x1- j   @8
    add process p p > n2 x1- j j @9
    """

elif jobOptProcess == "WB":
    winobino = True
    jobOptProcess_evt_desc = "Wino-Bino"
    process = """
    generate p p > n2 x1+        @1
    """

else:
    raise RuntimeError("Only Higgsino or WinoBino supported.")


decays["1000023"] = """DECAY  1000023       9.37327589E-04   # neutralino2 decays
     1.00000000E+00    2     1000022        22             # BR(~chi_20 -> ~chi_10 gamma )"""

decays["1000024"] = """DECAY   1000024     7.00367294E-03   # chargino1+ decays

#    BR                NDA      ID1      ID2       ID3
     0.33333333E+00    3     1000022        -1         2   # BR(chi^+_1 -> chi^0_1 d_bar u)
     0.33333333E+00    3     1000022        -3         4   # BR(chi^+_1 -> chi^0_1 s_bar c)
     0.11111111E+00    3     1000022       -11        12   # BR(chi^+_1 -> chi^0_1 e^+ nu_e)
     0.11111111E+00    3     1000022       -13        14   # BR(chi^+_1 -> chi^0_1 mu^+ nu_mu)
     0.11111111E+00    3     1000022       -15        16   # BR(chi^+_1 -> chi^0_1 tau^+ nu_tau)"""


# Photon Filter
# filtSeq += xAODPhotonFilter("PhotonFilter")
filtSeq.xAODPhotonFilter.PtMin = 5000.0
filtSeq.xAODPhotonFilter.NPhotons = 1

# MET Filter
# filtSeq += xAODMETFilter("METFilter")
filtSeq.xAODMissingEtFilter.METCut = float(METCut) * GeV
evt_multiplier = 25


# Lepton Filter
# filtSeq += xAODMultiElecMuTauFilter("MultiElecMuTauFilter")
# ElecMuTauFilter = filtSeq.xAODMultiElecMuTauFilter
filtSeq.xAODMultiElecMuTauFilter.MinPt = 20.0 * GeV
# ElecMuTauFilter.MaxEta = 2.8
filtSeq.xAODMultiElecMuTauFilter.NLeptons = 1
filtSeq.xAODMultiElecMuTauFilter.IncludeHadTaus = 0  # don't include hadronic taus


filtSeq.Expression = (
    "xAODPhotonFilter and (xAODMissingEtFilter or xAODMultiElecMuTauFilter)"
)


evgenLog.info("evt_multiplier == " + str(evt_multiplier))


# exact mass spectrum and mixing matrices depend on scenario
if higgsino:
    print("Choosing Higgsino...")
    # see also: https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SUSYCrossSections13TeVhinosplit
    # masses['1000023'] = -1.0 * MassToFloat(splitConfig[3]) # N2, make LSP higgsino like (positive for wino)
    # masses['1000024'] =  0.5 * (MassToFloat(splitConfig[3])+MassToFloat(splitConfig[4])) # Chargino is between N1 and N2
    masses["1000022"] = mN1
    masses["1000023"] = -1.0 * mN2
    masses["1000024"] = str((float(mN2) + float(mN1)) / 2.0)

    # Off-diagonal chargino mixing matrix V
    param_blocks["VMIX"] = {}
    param_blocks["VMIX"]["1 1"] = "0.00E+00"
    param_blocks["VMIX"]["1 2"] = "1.00E+00"
    param_blocks["VMIX"]["2 1"] = "1.00E+00"
    param_blocks["VMIX"]["2 2"] = "0.00E+00"
    # Off-diagonal chargino mixing matrix U
    param_blocks["UMIX"] = {}
    param_blocks["UMIX"]["1 1"] = "0.00E+00"
    param_blocks["UMIX"]["1 2"] = "1.00E+00"
    param_blocks["UMIX"]["2 1"] = "1.00E+00"
    param_blocks["UMIX"]["2 2"] = "0.00E+00"
    # Neutralino mixing matrix chi_i0 = N_ij (B,W,H_d,H_u)_j
    param_blocks["NMIX"] = {}
    param_blocks["NMIX"]["1  1"] = " 0.00E+00"  # N_11 bino
    param_blocks["NMIX"]["1  2"] = " 0.00E+00"  # N_12
    param_blocks["NMIX"]["1  3"] = " 7.07E-01"  # N_13
    param_blocks["NMIX"]["1  4"] = "-7.07E-01"  # N_14
    param_blocks["NMIX"]["2  1"] = " 0.00E+00"  # N_21
    param_blocks["NMIX"]["2  2"] = " 0.00E+00"  # N_22
    param_blocks["NMIX"]["2  3"] = "-7.07E-01"  # N_23 higgsino
    param_blocks["NMIX"]["2  4"] = "-7.07E-01"  # N_24 higgsino
    param_blocks["NMIX"]["3  1"] = " 1.00E+00"  # N_31
    param_blocks["NMIX"]["3  2"] = " 0.00E+00"  # N_32
    param_blocks["NMIX"]["3  3"] = " 0.00E+00"  # N_33 higgsino
    param_blocks["NMIX"]["3  4"] = " 0.00E+00"  # N_34 higgsino
    param_blocks["NMIX"]["4  1"] = " 0.00E+00"  # N_41
    param_blocks["NMIX"]["4  2"] = "-1.00E+00"  # N_42 wino
    param_blocks["NMIX"]["4  3"] = " 0.00E+00"  # N_43
    param_blocks["NMIX"]["4  4"] = " 0.00E+00"  # N_44
elif winobino:
    print("Choosing Wino-Bino...")
    # masses['1000023'] =  1.0 * MassToFloat(splitConfig[3]) # N2, make LSP wino like (negative for higgsino)
    masses["1000022"] = mN1
    masses["1000023"] = mN2
    masses["1000024"] = masses["1000023"]  # C1 = N2

    # mixing used in R19 samples: https://gitlab.cern.ch/atlas-physics/pmg/infrastructure/mc15joboptions/-/blob/master/common/MadGraph/param_card.SM.C1N2.WZ.dat
    # the off-diagonal entries lead to small but non-zero cross sections for e.g. N2N1 and N1C1 (these vanish for pure Winos/Binos)
    # Chargino mixing matrix V
    param_blocks["VMIX"] = {}
    param_blocks["VMIX"]["1 1"] = "9.72557835E-01"  # V_11
    param_blocks["VMIX"]["1 2"] = "-2.32661249E-01"  # V_12
    param_blocks["VMIX"]["2 1"] = "2.32661249E-01"  # V_21
    param_blocks["VMIX"]["2 2"] = "9.72557835E-01"  # V_22
    # Chargino mixing matrix U
    param_blocks["UMIX"] = {}
    param_blocks["UMIX"]["1 1"] = "9.16834859E-01"  # U_11
    param_blocks["UMIX"]["1 2"] = "-3.99266629E-01"  # U_12
    param_blocks["UMIX"]["2 1"] = "3.99266629E-01"  # U_21
    param_blocks["UMIX"]["2 2"] = "9.16834859E-01"  # U_22
    # Neutralino mixing matrix
    param_blocks["NMIX"] = {}
    param_blocks["NMIX"]["1  1"] = "9.86364430E-01"  # N_11
    param_blocks["NMIX"]["1  2"] = "-5.31103553E-02"  # N_12
    param_blocks["NMIX"]["1  3"] = "1.46433995E-01"  # N_13
    param_blocks["NMIX"]["1  4"] = "-5.31186117E-02"  # N_14
    param_blocks["NMIX"]["2  1"] = "9.93505358E-02"  # N_21
    param_blocks["NMIX"]["2  2"] = "9.44949299E-01"  # N_22
    param_blocks["NMIX"]["2  3"] = "-2.69846720E-01"  # N_23
    param_blocks["NMIX"]["2  4"] = "1.56150698E-01"  # N_24
    param_blocks["NMIX"]["3  1"] = "-6.03388002E-02"  # N_31
    param_blocks["NMIX"]["3  2"] = "8.77004854E-02"  # N_32
    param_blocks["NMIX"]["3  3"] = "6.95877493E-01"  # N_33
    param_blocks["NMIX"]["3  4"] = "7.10226984E-01"  # N_34
    param_blocks["NMIX"]["4  1"] = "-1.16507132E-01"  # N_41
    param_blocks["NMIX"]["4  2"] = "3.10739017E-01"  # N_42
    param_blocks["NMIX"]["4  3"] = "6.49225960E-01"  # N_43
    param_blocks["NMIX"]["4  4"] = "-6.84377823E-01"  # N_44


njets = 2

# if 'MET' in JOName.split('_')[-1]:
#    include ( 'GeneratorFilters/MissingEtFilter.py' )
#
#    metFilter = JOName.split('_')[-1]
#    metFilter = int(metFilter.split("MET")[1].split(".")[0])

#    print "Using MET Filter: " + str(metFilter)
#    filtSeq.MissingEtFilter.METCut = metFilter*GeV
#    evt_multiplier = metFilter / 10

# else:
#    print "No MET Filter applied"


# evgenLog.info('Registered generation of stop pair production, stop to c+LSP and t+LSP; grid point '+str(runArgs.jobConfig[0])+' decoded into mass point mstop=' + str(masses['1000006']) + ', mlsp='+str(masses['1000022']))

# evgenConfig.contact  = [ "alvaro.lopez.solis@cern.ch","armin.fehr@lhep.unibe.ch","john.kenneth.anders@cern.ch" ]
# evgenConfig.keywords += ['simplifiedModel','charm']
evgenConfig.description = jobOptProcess_evt_desc + " N2->N1 + gam"

if njets > 0:
    # genSeq.Pythia8.Commands += ["Merging:Process = pp>{t1,1000006}{t1~,-1000006}"]
    genSeq.Pythia8.Commands += ["Merging:Process = guess"]
    genSeq.Pythia8.UserHooks += ["JetMergingaMCatNLO"]

include("MadGraphControl/SUSY_SimplifiedModel_PostInclude.py")
