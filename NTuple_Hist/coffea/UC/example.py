# this portion is done to ignore warnings from coffea for now
from __future__ import annotations

import awkward as ak
import dask
import hist.dask as had
import matplotlib.pyplot as plt
from coffea import processor
from coffea.nanoevents import NanoEventsFactory
from distributed import Client, LocalCluster
import os
from atlas_schema.schema import NtupleSchema
from dask.distributed import performance_report
import json
import warnings
import time

from pathlib import Path
from coffea.dataset_tools import apply_to_fileset

warnings.filterwarnings("ignore", module="coffea.*")
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore")


class MyFirstProcessor(processor.ProcessorABC):
    def __init__(self):
        pass
    def process(self, events):
        # Accessing per-dataset meta-data
        dataset = events.metadata["dataset"]
        # Defining histogram properties
        h_ph_pt = (
            had.Hist.new.StrCat(["all"], name="isEM")
            .Regular(200, 0.0, 1000.0, name="pt", label="$pt_{\\gamma}$ [GeV]")
            .Int64()
        )

        # Defining the cut
        cut = ak.all(events.ph.isEM, axis=1)


        xs = events.metadata["xs"]
        lum = events.metadata["luminosity"]
        genFiltEff = events.metadata["genFiltEff"]
        #kfactor = events.metadata["kFactor"]
        kfactor = 1.
        # sumOfWeights = events.metadata["sum_of_weights"]
        # sumOfEvents = events.metadata["sum_of_events"]
        sumOfWeights = 4345667100606464.0
        weight_norm = xs * genFiltEff * kfactor * lum / sumOfWeights
        h_ph_pt.fill(isEM="all", pt=ak.firsts(events.ph.pt/1000.), weight=(weight_norm*events.weight.mc*events.weight.pileup))
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


def main():
    # Defining "MyFirstProcessor" object
    p = MyFirstProcessor()

    #client = Client()
    # Limit to 4 total CPU cores, across 2 workers with 2 threads each
    cluster = LocalCluster(n_workers=2, threads_per_worker=2)
    with Client(cluster) as client:
        dataset_runnable = json.loads(Path("/data/selbor/dataset_runnable/af_v2_700402.json").read_text())
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

         Saves hist figure as a pdf
        fig.savefig("ph_pt.pdf")

if __name__ == "__main__":
    main()
   
