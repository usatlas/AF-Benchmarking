# this portion is done to ignore warnings from coffea for now
from __future__ import annotations

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
        kfactor = 1.
        sumOfWeights = 4345667100606464.0
        weight_norm = xs * genFiltEff * kfactor * lum / sumOfWeights
        h_ph_pt.fill(isEM="all", pt=ak.firsts(events.ph.pt/1000.), weight=(weight_norm*events.weight.mc*events.weight.pileup))

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

    client = Client()

    # FIXME: Update the path to the json file containing the weights
    dataset_runnable = json.loads(Path("/pscratch/sd/s/selbor/ntuple/coffea/dataset_runnable/af_v2_700402.json").read_text())

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
   
