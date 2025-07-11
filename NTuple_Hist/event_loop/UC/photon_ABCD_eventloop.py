def photon_ABCD_eventloop(f_name):
    print(f_name)
    fp=r.TFile(f_name,"RO")
    tree=fp.Get("analysis")
    eventcount=0
    totalevents=t.GetEntriesFast()
    h_baseline_pt=r.TH1D("baseline_pt","baseline_pt",100,0,1000)

    # Metadata dictionary
    metadata={"genFiltEff": 1.0,
              "luminosity": 58.7916,
              "process": "Wmunugamma",
              "xs": 364840.0,
              "sum_of_weights": 1816229744476160.0}

    xs = metadata["xs"]
    lum = metadata["luminosity"]
    genFiltEff = metadata["genFiltEff"]
    kfactor = 1.
    sumOfWeights = metadata["sum_of_weights"]
    weight_norm = xs * genFiltEff * kfactor * lum / sumOfWeights

    for event in tree:
        eventcount+=1
        if eventcount%50000 == 0:
            print(f"Processed {eventcount:6d}/{totalevents} events")
        for index, photon_pt in enumerate(event.ph_pt_NOSYS):
            photon_id = ord(event.ph_select_tightID_NOSYS[index])
            if photon_id == 0:
                continue
            
            weight=(weight_norm*event.weight_mc_NOSYS*event.weight_pileup_NOSYS)
            h_baseline_pt.Fill(photon_pt/1000.,weight)
            break


def main():
    # Path to the input root files
    file_dir=Path('/data/maclwong/Ben_Bkg_Samples/v2/user.bhodkins.700402.Wmunugamma.mc20e.v2.0_ANALYSIS.root/')

    # For-loop iterating over all data files in file_dir and inputting into function
    for f in sorted(file_dir.iterdir()):
        photon_ABCD_eventloop(str(f))


    # Output ROOT file
    output_file = r.TFile("event_loop_output_hist.root", "RECREATE")
    h_baseline_pt.Write()
    output_file.Close()

if __name__ == "__main__":
        main()
