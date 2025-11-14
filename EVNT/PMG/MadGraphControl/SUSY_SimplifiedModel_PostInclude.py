# This comes after all Simplified Model setup files
from MadGraphControl.MadGraphUtils import SUSY_Generation,modify_param_card,check_reset_proc_number
from MadGraphControl.MadGraphUtilsHelpers import get_physics_short

phys_short = get_physics_short()

if 'rpv' in phys_short.lower() and not 'import ' in process:
    raise RuntimeError('Please import a model when using an RPV decay; these are not handled by the standard MSSM model in MadGraph')

# Set maximum number of events if the event multiplier has been modified
if evt_multiplier>0:
    if runArgs.maxEvents>0:
        nevts=runArgs.maxEvents*evt_multiplier
    else:
        nevts=evgenConfig.nEventsPerJob*evt_multiplier
else:
    # Sensible default
    nevts=evgenConfig.nEventsPerJob*2.
run_settings.update({'nevents':int(nevts)})

# Only needed for something non-standard (not 1/4 heavy mass)
if ktdurham is not None:
    run_settings.update({'ktdurham':ktdurham})

if flavourScheme not in [4,5]:
    raise RuntimeError('flavourScheme must be 4 or 5.')

if flavourScheme == 4:
    run_settings.update({
        'pdgs_for_merging_cut': '1, 2, 3, 4, 21' # Terrible default in MG
    })
    _nQuarksMerge = 5 if finalStateB else 4
else:
    run_settings.update({
        'pdgs_for_merging_cut': '1, 2, 3, 4, 5, 21',
        'asrwgtflavor': 5,
        'maxjetflavor': 5
    })
    _nQuarksMerge = 5
    if define_pj_5FS:
        # Add the 5FS p and j definition to the beginning of the process string
        process = "define p = g u c d s b u~ c~ d~ s~ b~\ndefine j = g u c d s b u~ c~ d~ s~ b~\n" + process
        # Check that if p and j get redefined that it is consistent with 5FS otherwise raise error
        for l in process.split('\n'):
            l_nocomment = l.split('#')[0]
            if ("define p" in l_nocomment or "define j" in l_nocomment) and l_nocomment.count("=") == 1:
                l_equals = (l_nocomment.split("=")[-1]).split(" ")
                if not set(['g', 'u', 'c', 'd', 's', 'b', 'u~', 'c~', 'd~', 's~', 'b~']) <= set(l_equals):
                    raise RuntimeError('Invalid definition found for p or j in process string while using 5FS')
    if force_nobmass_5FS:
        if masses.get('5',0.0) != 0.0:
            raise RuntimeError('Non-zero mass found for b while using 5FS')
        masses['5'] = 0.0

# systematic variation
if 'scup' in phys_short:
    syst_mod=dict_index_syst[0]
elif 'scdw' in phys_short:
    syst_mod=dict_index_syst[1]
elif 'alup' in phys_short:
    syst_mod=dict_index_syst[2]
elif 'aldw' in phys_short:
    syst_mod=dict_index_syst[3]
elif 'qcup' in phys_short:
    syst_mod=dict_index_syst[6]
elif 'qcdw' in phys_short:
    syst_mod=dict_index_syst[7]

# Pass arguments as a dictionary: the "decays" argument is not accepted in older versions of MadGraphControl
if 'mass' in [x.lower() for x in param_blocks]:
    raise RuntimeError('Do not provide masses in param_blocks; use the masses variable instead')
param_blocks['MASS']=masses
# Add decays in if needed
if len(decays)>0: param_blocks['DECAY']=decays
argdict = {'runArgs'        : runArgs,
           'process'        : process,
           'params'         : param_blocks,
           'fixEventWeightsForBridgeMode': fixEventWeightsForBridgeMode,
           'madspin_card'   : madspin_card,
           'keepOutput'     : keepOutput, # Should only ever be true for testing!
           'run_settings'   : run_settings, # All goes into the run card
           'writeGridpack'  : writeGridpack,
           'syst_mod'       : syst_mod,
           'param_card'     : param_card, # Only set if you *can't* modify the default param card to get your settings
           'add_lifetimes_lhe' : add_lifetimes_lhe,
           'usePMGSettings' : usePMGSettings,
           'plugin'         : plugin,
           }

# First the standard case: No input LHE file
if not hasattr(runArgs,'inputGeneratorFile') or runArgs.inputGeneratorFile is None:
    # Note that for gridpack generation, the job will exit after this command
    ktdurham = SUSY_Generation(**argdict)

else:
    # These manipulations require a dummy SUSY process
    from MadGraphControl.MadGraphUtils import new_process,update_lhe_file,add_madspin,arrange_output,SUSY_process
    process_dir = new_process(SUSY_process('generate p p > go go'))
    modify_param_card(process_dir=process_dir,params={'MASS':masses,'DECAY':decays})
    param_card_old = process_dir+'/Cards/param_card.dat'
    ktdurham = -1
    import tarfile
    if tarfile.is_tarfile(runArgs.inputGeneratorFile):
        myTarball = tarfile.open(runArgs.inputGeneratorFile)
        myEvents = None
        for afile in myTarball.getnames():
            if afile.endswith('.events'): myEvents = afile
        if myEvents is None:
            raise RuntimeError('No input events file found!')
        else:
            events_file = myTarball.extractfile( myEvents )
            update_lhe_file(lhe_file_old=myEvents,param_card_old=param_card_old,masses=masses)
            for aline in events_file:
                # Note that because this was directly extracted, we have a binary file, not a text file!
                if b'ktdurham' in aline and b'=' in aline:
                    ktdurham = float(aline.split(b'=')[0].strip())
                    break
        myTarball.close()
    else:
        # Assume this is already an unzipped file -- happens when we run on multiple LHEs
        update_lhe_file(lhe_file_old=runArgs.inputGeneratorFile,param_card_old=param_card_old,masses=masses)
        with open(runArgs.inputGeneratorFile,'r') as events_file:
            for aline in events_file:
                if 'ktdurham' in aline and "=" in aline:
                    ktdurham = float(aline.split('=')[0].strip())
                    break

    if madspin_card is not None:
        # Do a stupid addition of madspin - requires a dummy process
        add_madspin(madspin_card,process_dir=process_dir)
        arrange_output(process_dir=process_dir,saveProcDir=keepOutput,runArgs=runArgs,fixEventWeightsForBridgeMode=fixEventWeightsForBridgeMode)

# Check if we were running multi-core, and if so move back to single core for Pythia8
check_reset_proc_number(opts)

# Pythia8 setup for matching if necessary
njets=max([l.count('j') for l in process.split('\n')])
njets_min=min([l.count('j') for l in process.split('\n') if 'generate ' in l or 'add process' in l])
if njets>0 and njets!=njets_min and hasattr(genSeq,'Pythia8'):
    genSeq.Pythia8.Commands += ["Merging:mayRemoveDecayProducts = on",
                                "Merging:nJetMax = "+str(njets),
                                "Merging:doKTMerging = on",
                                "Merging:TMS = "+str(ktdurham),
                                "Merging:ktType = 1",
                                "Merging:Dparameter = 0.4",
                                "Merging:nQuarksMerge = {0:d}".format(_nQuarksMerge)]

# Configuration for EvgenJobTransforms
#--------------------------------------------------------------
evgenConfig.keywords += ["SUSY"]
