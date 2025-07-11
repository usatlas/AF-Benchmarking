import ROOT as r
import json
import os

from pathlib import Path

# PreID the branches in the tree that I'm going to use; create arrays (in advance) that when tree data is loaded it goes into it automatically
# FIXME: Have it produce a hitogram in a root file

def photon_ABCD_eventloop(f_name):
    print(f_name)

    f=r.TFile(f_name, "RO")
    t=f.Get("analysis")
    h_baseline_pt=r.TH1F("baseline_pt","baseline_pt",10000,0,10000)

    
    totalevents=t.GetEntriesFast()
    for e in t:
        eventcount+=1
        if eventcount%50000 == 0:
            print(f"Processed {eventcount:6d}/{totalevents} events")

        # FIXME: Like in Coffea have it fill using the same method
        # e.weight_c
        h_baseline_pt.Fill(e.ph_pt_NOSYS[photon_index]/1000.)


# FIXME: Optimize this code
file_dir=Path('/data/maclwong/Ben_Bkg_Samples/v2/user.bhodkins.700402.Wmunugamma.mc20e.v2.0_ANALYSIS.root/')

files_full_path=sorted(file_dir.glob("*.root"))

for f in files_full_path:
    photon_ABCD_eventloop(f)
