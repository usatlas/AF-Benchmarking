# this portion is done to ignore warnings from coffea for now
from __future__ import annotations

import warnings

import awkward as ak
import dask
import hist.dask as had
import matplotlib.pyplot as plt
from coffea import processor
from coffea.nanoevents import NanoEventsFactory
from distributed import Client

from light_roast.schema import LightRoastSchema

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
    client = Client()

    fname = "./user.bhodkins.38118418._000001.ANALYSIS.root"
    events = NanoEventsFactory.from_root(
        {fname: "analysis"},
        schemaclass=LightRoastSchema,
        metadata={"dataset": "700352.Zqqgamma.mc20d.2024-04-12"},
    ).events()

    p = MyProcessor()
    out = p.process(events)
    (computed,) = dask.compute(out)
    print(computed)

    fig, ax = plt.subplots()
    computed["700352.Zqqgamma.mc20d.2024-04-12"]["ph_pt"].plot1d(ax=ax)
    ax.set_xscale("log")
    ax.legend(title="Photon pT for Zqqgamma")

    fig.savefig("ph_pt.pdf")
