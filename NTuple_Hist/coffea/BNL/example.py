# this portion is done to ignore warnings from coffea for now
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

# Making a main function to encapsulate the code
def main(fname, file_num):

    client = Client()

    # Need to run this over the entire data set:
    # /data/maclwong/Ben_Bkg_Samples/v2/user.bhodkins.700402.Wmunugamma.mc20e.v2.0_ANALYSIS.root/

    client = Client()

    fname = "/data/selbor/ntuple_hist/coffea_fw/user.bhodkins.data2018_AllYear.v2.0_ANALYSIS.root/user.bhodkins.42164748._000288.ANALYSIS.root"
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

    fig.savefig("ntuple_cfw_{}.pdf".format(file_num))

if __name__ == "__main__":
file_dir=r'/atlasgpfs01/usatlas/data/jroblesgo/user.bhodkins.700402.Wmunugamma.mc20e.v2.0_ANALYSIS.root/'

files_full_path=[os.path.join(file_dir,i) for i in sorted(os.listdir(file_dir))]

i = 1
for f in files_full_path:
    main(f, i)
    i +=1

