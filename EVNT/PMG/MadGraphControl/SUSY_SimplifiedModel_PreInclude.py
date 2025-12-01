# Generator transform pre-include
#  Gets us ready for on-the-fly SUSY SM generation

# Simple variable setups
param_blocks = {}  # For general params
decoupled_mass = "4.5E9"
masses = {}
for p in [
    "1000001",
    "1000002",
    "1000003",
    "1000004",
    "1000005",
    "1000006",
    "2000001",
    "2000002",
    "2000003",
    "2000004",
    "2000005",
    "2000006",
    "1000021",
    "1000023",
    "1000024",
    "1000025",
    "1000011",
    "1000013",
    "1000015",
    "2000011",
    "2000013",
    "2000015",
    "1000012",
    "1000014",
    "1000016",
    "1000022",
    "1000035",
    "1000037",
    "35",
    "36",
    "37",
]:  # Note that gravitino is non-standard
    masses[p] = decoupled_mass
decays = {}

# Useful definitions
squarks = []
squarksl = []
for anum in [1, 2, 3, 4]:
    squarks += [
        str(1000000 + anum),
        str(-1000000 - anum),
        str(2000000 + anum),
        str(-2000000 - anum),
    ]
    squarksl += [str(1000000 + anum), str(-1000000 - anum)]
dict_index_syst = {
    0: "scalefactup",
    1: "scalefactdown",
    2: "alpsfactup",
    3: "alpsfactdown",
    4: "moreFSR",
    5: "lessFSR",
    6: "qup",
    7: "qdown",
}

# Basic settings for production and filters
syst_mod = None
ktdurham = None  # Only set if you want a non-standard setting (1/4 heavy mass)
madspin_card = None
param_card = None  # Only set if you *can't* just modify the default param card to get your settings (e.g. pMSSM)

# Default run settings
run_settings = {
    "event_norm": "average",
    "drjj": 0.0,
    "lhe_version": "3.0",
    "cut_decays": "F",
    "ickkw": 0,
    "xqcut": 0,
}  # use CKKW-L merging (yes, this is a weird setting)
# Set up default PDF and systematic settings (note: action in import module)
import MadGraphControl.MadGraph_NNPDF30NLO_Base_Fragment  # noqa: F401
from AthenaCommon import Logging

presusylog = Logging.logging.getLogger("SUSY_PreInclude")

# Setting for writing out a gridpack
writeGridpack = False

# Event multipliers for getting more events out of madgraph to feed through athena (esp. for filters)
evt_multiplier = -1

# in case someone needs to be able to keep the output directory for testing
keepOutput = False

# fixing LHE files after madspin?  do that here.
fixEventWeightsForBridgeMode = False

# In case you want to keep lifetimes in the LHE files
add_lifetimes_lhe = False

# Do we want to use PDG defaults?
usePMGSettings = True

# Do we need to use a custom plugin?
plugin = None

# Do we want 4FS or 5FS? 5 is now default
# * 5-flavor scheme always should use nQuarksMerge=5 [5FS -> nQuarksMerge=5]
# * 4-flavor scheme with light-flavor MEs (p p > go go j , with j = g d u s c)
#       should use nQuarksMerge=4 [4FS -> nQuarksMerge=4]
# * 4-flavor scheme with HF MEs (p p > go go j, with j = g d u s c b) should
#       use nQuarksMerge=5 [4FS + final state b -> nQuarksMerge=5]
flavourScheme = 5
define_pj_5FS = True  # Defines p and j to include b in process string with 5FS
force_nobmass_5FS = True  # Forces massless b with 5FS
finalStateB = False  # Used with 4FS

from MadGraphControl.MadGraphUtilsHelpers import get_physics_short

phys_short = get_physics_short()
if "py1up" in phys_short:
    include("Pythia8_i/Pythia8_A14_NNPDF23LO_Var1Up_EvtGen_Common.py")
elif "py1dw" in phys_short:
    include("Pythia8_i/Pythia8_A14_NNPDF23LO_Var1Down_EvtGen_Common.py")
elif "py2up" in phys_short:
    include("Pythia8_i/Pythia8_A14_NNPDF23LO_Var2Up_EvtGen_Common.py")
elif "py2dw" in phys_short:
    include("Pythia8_i/Pythia8_A14_NNPDF23LO_Var2Down_EvtGen_Common.py")
elif "py3aup" in phys_short:
    include("Pythia8_i/Pythia8_A14_NNPDF23LO_Var3aUp_EvtGen_Common.py")
elif "py3adw" in phys_short:
    include("Pythia8_i/Pythia8_A14_NNPDF23LO_Var3aDown_EvtGen_Common.py")
elif "py3bup" in phys_short:
    include("Pythia8_i/Pythia8_A14_NNPDF23LO_Var3bUp_EvtGen_Common.py")
elif "py3bdw" in phys_short:
    include("Pythia8_i/Pythia8_A14_NNPDF23LO_Var3bDown_EvtGen_Common.py")
elif "py3cup" in phys_short:
    include("Pythia8_i/Pythia8_A14_NNPDF23LO_Var3cUp_EvtGen_Common.py")
elif "py3cdw" in phys_short:
    include("Pythia8_i/Pythia8_A14_NNPDF23LO_Var3cDown_EvtGen_Common.py")
else:
    include("Pythia8_i/Pythia8_A14_NNPDF23LO_EvtGen_Common.py")

include("Pythia8_i/Pythia8_MadGraph.py")


# Helper function that can be called from control file to use common mixing matrices
def common_mixing_matrix(mtype):
    presusylog.info(f"Will set mixing to {mtype}")
    # Include various cases for common mixing matrices here
    if mtype == "higgsino":
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
        if masses["1000022"] * masses["1000023"] > 0:
            presusylog.warning(
                "Expected N1 and N2 masses to have opposite sign for a higgsino signal. Possibly set after the mixing."
            )
    elif mtype == "winobino":
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
    elif mtype == "stau_maxmix":
        param_blocks["selmix"] = {}
        # use maximally mixed status
        param_blocks["selmix"]["3   3"] = "0.70710678118"  # # RRl3x3
        param_blocks["selmix"]["3   6"] = "0.70710678118"  # # RRl3x6
        param_blocks["selmix"]["6   3"] = "-0.70710678118"  # # RRl6x3
        param_blocks["selmix"]["6   6"] = "0.70710678118"  # # RRl6x6
    elif mtype == "stau_nomix":
        param_blocks["selmix"] = {}
        # No mixing
        param_blocks["selmix"]["3   3"] = "1.0"  # # RRl3x3
        param_blocks["selmix"]["3   6"] = "0.0"  # # RRl3x6
        param_blocks["selmix"]["6   3"] = "0.0"  # # RRl6x3
        param_blocks["selmix"]["6   6"] = "1.0"  # # RRl6x6
