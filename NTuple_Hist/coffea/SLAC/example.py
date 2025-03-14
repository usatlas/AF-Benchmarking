#this portion is done to ignore warnings from coffea for now
from __future__ import annotations

import warnings
import awkward as ak
import dask
import hist.dask as had
import matplotlib.pyplot as plt
from distributed import Client
from coffea import processor
from atlas_schema.schema import NtupleSchema
from coffea.nanoevents import NanoEventsFactory
from distributed import Client
from datetime import datetime

warnings.filterwarnings("ignore", module="coffea.*")


class MyProcessor(processor.ProcessorABC):
    def __init__(self):
        pass

    def process(self, events):
        dataset = events.metadata["dataset"]
        h_ph_pt = (
            had.Hist.new.StrCat(["all", "pass", "fail"], name="isEM")
            .Regular(200, 0.0, 2000.0, name="pt", label="$pt_{\gamma}$ [GeV]")
            .Int64()
        )

        cut = ak.all(events.ph.isEM, axis=1)
        h_ph_pt.fill(isEM="all", pt=ak.firsts(events.ph.pt / 1.0e3))
        h_ph_pt.fill(isEM="pass", pt=ak.firsts(events[cut].ph.pt / 1.0e3))
        h_ph_pt.fill(isEM="fail", pt=ak.firsts(events[~cut].ph.pt / 1.0e3))

        return {
            dataset: {
                "entries": ak.num(events, axis=0),
                "ph_pt": h_ph_pt,
            }
        }

    def postprocess(self, accumulator):
        pass


if __name__ == "__main__":
    # Gets the current time
    start_time = datetime.now()
    print(start_time)

    client = Client()

    # Input file goes in here; requires absolute path

    client = Client()

    fname = "/sdf/home/s/selbor/Ntuple_Hist/coffea/user.bhodkins.data2018_AllYear.v2.0_ANALYSIS.root/user.bhodkins.42164748._000288.ANALYSIS.root"
    events = NanoEventsFactory.from_root(
        {fname: "analysis"},
        schemaclass=NtupleSchema,
        metadata={"dataset": "700402.Wmunugamma.2024-08-06"},
    ).events()

    p = MyProcessor()
    out = p.process(events)
    (computed,) = dask.compute(out)
    print(computed)

    fig, ax = plt.subplots()
    computed["700402.Wmunugamma.2024-08-06"]["ph_pt"].plot1d(ax=ax)
    ax.set_xscale("log")
    ax.legend(title="NTuple -> Hist Coffea Frame Work")

    fig.savefig("ntuple_cfw.pdf")

    # Gets the current time
    end_time = datetime.now()
    print(end_time)

