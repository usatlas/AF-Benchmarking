import awkward as ak
import dask
import hist.dask as had
import matplotlib.pyplot as plt
from coffea import processor
from coffea.nanoevents import NanoEventsFactory
from distributed import Client
import os
from atlas_schema.schema import NtupleSchema
from dask.distributed import performance_report


class MyFirstProcessor(processor.ProcessorABC):
    def __init__(self):
        pass
    def process(self, events):
        # Accessing per-dataset meta-data
        dataset = events.metadata["dataset"]
        # Defining histogram properties
        h_ph_pt = (
            had.Hist.new.StrCat(["all"], name="isEM")
            .Regular(200, 0.0, 1000.0, name="pt", label="$pt_{\gamma}$ [GeV]")
            .Int64()
        )

        # Defining the cut
        cut = ak.all(events.ph.isEM, axis=1)


        # Filling the histogram
        # FIXME: Update this to handle weighted events
        # Fold in: weight=weight_mc*weight_pileup*weight_beamspot

        # NOSYS weight from FF sum_weights.txt file: 1816229744476160.0
        # (not sure about this part) Number of events (MC): events.ph.pt 
        # (not sure about this part) XS: events.xs or events['xs']
        # (not sure about this part) lumi: events.lumi
        # Putting it all together: weight= (xs*lumi*mc)/sum_weights
        # Error comes from the cross section, it doesn't find it
        h_ph_pt.fill(isEM="all", pt=ak.firsts(events.ph.pt/ 3e3), weights=(events.metadata["cross-section"]*events.metadata["lumi"]*events.weight*mc.events.pileup)/1816229744476160.0)
        #h_ph_pt.fill(isEM="pass", pt=ak.firsts(events[cut].ph.pt / 1.0e3))
        #h_ph_pt.fill(isEM="fail", pt=ak.firsts(events[~cut].ph.pt / 1.0e3))

        # Returns hist entries
        return {
            dataset: {
                "entries": ak.num(events, axis=0),
                "ph_pt": h_ph_pt,
            }
        }

    def postprocess(self, accumulator):
        pass

from pathlib import Path

def main():
    # Path to data set directory
    dataset = Path("/data/maclwong/Ben_Bkg_Samples/v2/user.bhodkins.700402.Wmunugamma.mc20e.v2.0_ANALYSIS.root/")
    client = Client()

    dataset_id=700402
    # Defining input events
    events = NanoEventsFactory.from_root(
            {item: "analysis" for item in dataset.iterdir()},
            schemaclass=NtupleSchema,
                        
            metadata={"dataset": "700402.Wmunugamma.mc20e.v2", "lumi": 59700, "cross-section": "/cvmfs/atlas.cern.ch/repo/sw/database/GroupData/dev/PMGTools/PMGxsecDB_mc16.txt", "kfactor": "/home/selbor/input/sum_weights.txt"},
            ).events()
    kfactor = events.metadata.get("kfactor", 1.0)

    # Defining "MyFirstProcessor" object
    p = MyFirstProcessor()
    out = p.process(events)
    (computed,) = dask.compute(out)
    print(computed)
    fig, ax = plt.subplots()
    # Plots using 'computed'
    computed["700402.Wmunugamma.mc20e.v2"]["ph_pt"].plot1d(ax=ax)
    ax.legend(title="Photon pT for Wmunugamma")

    # Saves hist figure as a pdf
    fig.savefig("ph_pt.pdf")

if __name__ == "__main__":
    main()
   
