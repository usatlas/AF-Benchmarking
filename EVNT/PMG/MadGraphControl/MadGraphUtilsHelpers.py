# Copyright (C) 2002-2019 CERN for the benefit of the ATLAS collaboration

import os

def getDictFromCard(card_loc,lowercase=False):
    card=open(card_loc)
    mydict={}
    for line in iter(card):
        if not line.strip().startswith('#'): # line commented out
            command = line.split('!', 1)[0]
            if '=' in command:
                setting = command.split('=')[-1].strip()
                value = '='.join(command.split('=')[:-1]).strip()
                if lowercase:
                    value=value.lower()
                    setting=setting.lower()
                mydict[setting]=value
    card.close()
    return mydict

def settingIsTrue(setting):
    if setting.replace("'",'').replace('"','').replace('.','').lower() in ['t','true']:
        return True
    return False

def totallyStripped(x):
    y=str(x).lower().strip()
    # remove leading and trailing "/'
    while len(y)>0 and (y[0]=='"' or y[0]=="'"):
        y=y[1:]
    while len(y)>0 and (y[-1]=='"' or y[-1]=="'"):
        y=y[:-1]
    return y

def checkSetting(key_,value_,mydict_):
    key=totallyStripped(key_)
    value=totallyStripped(value_)
    mydict={}
    for k in mydict_:
        mydict[totallyStripped(k)]=totallyStripped(mydict_[k])
    return key in mydict and mydict[key]==value

def checkSettingIsTrue(key_,mydict_):
    key=totallyStripped(key_)
    mydict={}
    for k in mydict_:
        mydict[totallyStripped(k)]=totallyStripped(mydict_[k])
    return key in mydict and mydict[key] in ['t','true']

def checkSettingExists(key_,mydict_):
    key=totallyStripped(key_)
    keys=[]
    for k in mydict_:
        keys+=[totallyStripped(k)]
    return key in keys

def is_version_or_newer(args):
    # also need to find out the version (copied from generate)
    import os
    version=None
    version_file = open(os.environ['MADPATH']+'/VERSION','r')

    for line in version_file:
        if 'version' in line:
            version=line.split('=')[1].strip()
    version_file.close()

    if not version:
        raise RuntimeError('Failed to find MadGraph/MadGraph5_aMC@NLO version in '+version_file)

    vs=[int(v) for v in version.split('.')]

    # this is lazy, let's hope there wont be a subversion > 100...
    y=int(100**max(len(vs),len(args)))
    testnumber=0
    for x in args:
        testnumber+=x*y
        y/=100

    y=int(100**max(len(vs),len(args)))
    versionnumber=0
    for x in vs:
        versionnumber+=x*y
        y/=100
    return versionnumber>=testnumber

def isNLO_from_run_card(run_card):
    f = open(run_card,'r')
    if "parton_shower" in f.read().lower():
        f.close()
        return True
    else:
        f.close()
        return False

def get_runArgs_info(runArgs):
    if runArgs is None:
        raise RuntimeError('runArgs must be provided!')
    if hasattr(runArgs,'ecmEnergy'):
        beamEnergy = runArgs.ecmEnergy / 2.
    else:
        raise RuntimeError("No center of mass energy found in runArgs.")
    if hasattr(runArgs,'randomSeed'):
        random_seed = runArgs.randomSeed
    else:
        raise RuntimeError("No random seed found in runArgs.")
    return beamEnergy,random_seed

def get_physics_short():
    FIRST_DIR = (os.environ['JOBOPTSEARCHPATH']).split(":")[0]
    jofiles = [f for f in os.listdir(FIRST_DIR) if (f.startswith('mc') and f.endswith('.py'))]
    if len(jofiles)==0:
        raise RuntimeError('No job options found in '+FIRST_DIR)
    joparts = os.path.basename(jofiles[0]).split('.')
    if len(joparts)<2:
        raise RuntimeError('Malformed job options file name: '+jofiles[0])
    return joparts[1]
