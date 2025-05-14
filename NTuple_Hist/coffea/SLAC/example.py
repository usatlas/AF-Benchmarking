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

        h_ph_pt = (
            had.Hist.new.StrCat(["all", "pass", "fail"], name="isEM")
            .Regular(200, 0.0, 2000.0, name="pt", label="$pt_{\gamma}$ [GeV]")
            .Int64()
        )

        # Defining the cut
        cut = ak.all(events.ph.isEM, axis=1)

        # Filling the histogram
        h_ph_pt.fill(isEM="all", pt=ak.firsts(events.ph.pt / 1.0e3))
        h_ph_pt.fill(isEM="pass", pt=ak.firsts(events[cut].ph.pt / 1.0e3))
        h_ph_pt.fill(isEM="fail", pt=ak.firsts(events[~cut].ph.pt / 1.0e3))

        # Returns hist entries
        return {
            dataset: {
                "entries": ak.num(events, axis=0),
                "ph_pt": h_ph_pt,
            }
        }

    def postprocess(self, accumulator):
        pass

def gist_block():
    client = Client()
        
    # Defining the root file name used in the analysis
    fname = "/data/maclwong/Ben_Bkg_Samples/v2/user.bhodkins.700402.Wmunugamma.mc20e.v2.0_ANALYSIS.root/user.bhodkins.42165201._000001.ANALYSIS.root"

    events = NanoEventsFactory.from_root(
            {fname: "analysis"},
            schemaclass=NtupleSchema,
            metadata={"dataset": "700402.Wmunugamma.mc20e.v2"},
            ).events()

    p = MyFirstProcessor()
    out = p.process(events)
    #(computed,) = dask.compute(out)
    with performance_report(filename="filename_optimizeFalse.html"):
        (computed,) = dask.compute(out, optimize_graph=False)

    print(computed)

    fig, ax = plt.subplots()
    computed["700402.Wmunugamma.mc20e.v2"]["ph_pt"].plot1d(ax=ax)
    ax.set_xscale("log")
    ax.legend(title="Photon pT for Wmunugamma")

    fig.savefig("ph_pt.pdf")

from pathlib import Path

def main():
    dataset = Path("/sdf/data/atlas/u/selbor/user.bhodkins.700402.Wmunugamma.mc20e.v2.0_ANALYSIS.root/")
    client = Client()

    dataset_runnable = json.loads(Path("/sdf/home/s/selbor/AF-Benchmarking/NTuple_Hist/coffea/dataset_runnable/af_v2_700402.json").read_text())

    nevents=0
    for f in dataset_runnable["Wmunugamma"]["files"]:
        nevents += int(dataset_runnable["Wmunugamma"]["files"][f]["num_entries"])
    
    print("Applying to fileset")
    out = apply_to_fileset(
        p,
        dataset_runnable,
        schemaclass=NtupleSchema,
    )

    start_time = time.time()
    (computed,) = dask.compute(out)
    end_time = time.time()
    execute_time = end_time - start_time
    print(
        f"... execution time: {end_time - start_time:6.2f} s ({(nevents / 1000.0) / execute_time:6.2f} kHz)"
    )
    
    print(computed)
    fig, ax = plt.subplots()
    
    # Plots using 'computed'
    computed["Wmunugamma"]["Wmunugamma"]["ph_pt"].plot1d(ax=ax)
    ax.legend(title="Photon pT for Wmunugamma")

    # Saves hist figure as a pdf
    fig.savefig("ph_pt.pdf")

if __name__ == "__main__":
    main()
   
