# Example Log Files

This directory contains example log files from various ATLAS experiment analysis
workflows. These logs are used for testing and developing log parsers in the
AF-Benchmarking project.

## Log File Sources

### coffea_hist.log

Output from the [Coffea](https://coffeateam.github.io/coffea/) analysis
framework. Shows histogram production from Wmunugamma Monte Carlo samples with
execution time and event processing rate (~57.6 kHz).

### eventloop_arrays.log

Event loop processing log from an ATLAS analysis reading `.ANALYSIS.root` files.
Processes Wmunugamma (DSID 700402) Monte Carlo samples file-by-file, reporting
progress every 50,000 events. Output is written to
`event_loop_output_hist.root`.

### ff.log

[FastFrames](https://gitlab.cern.ch/atlas-amglab/fastframes) framework log. A
C++/Python framework for producing histograms from ROOT ntuples using
RDataFrame. Processes mc20e campaign samples with configurable regions and
systematics.

### log.Derivation

ATLAS Athena derivation framework log. Shows the production of DAOD_TRUTH3
format from EVNT (generator-level) input files. Configures jet reconstruction
(AntiKt4, AntiKt10) and MET calculations for truth-level analysis.

### log.generate

ATLAS Monte Carlo event generation log using the AthGeneration release. Uses
MadGraph5_aMC@NLO (v3.5.3) with Pythia8 and EvtGen for a SUSY simplified model
(Wino-Bino scenario). Generates events at 13 TeV with photon, lepton, and MET
filters.

### rucio.log

[Rucio](https://rucio.cern.ch/) data management client log. Shows multi-threaded
download of DAOD_PHYSLITE files from the ATLAS distributed computing grid
(downloading from AGLT2_LOCALGROUPDISK). Reports download speeds (~250-400 MBps)
and file transfer status.

## Analysis Facility Context

These logs represent typical workflows run on ATLAS Analysis Facilities:

- **Data access**: Rucio downloads from grid storage
- **Event generation**: MadGraph + Pythia for MC production
- **Derivation**: Athena-based data format conversion
- **Analysis**: Coffea, EventLoop, and FastFrames for physics analysis
