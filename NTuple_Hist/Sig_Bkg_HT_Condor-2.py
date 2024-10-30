#!/usr/bin/env python

# this portion is done to ignore warnings from coffea for now
from __future__ import annotations

import warnings
import pickle
import awkward as ak
import dask
import hist.dask as had
import numpy as np
import matplotlib.pyplot as plt
from coffea import processor
from coffea.nanoevents import NanoEventsFactory
from distributed import Client
import glob
from light_roast.schema import LightRoastSchema
import numpy as np
from coffea.dataset_tools import (apply_to_fileset, max_chunks, preprocess)
import time
from dask_jobqueue.htcondor import HTCondorCluster
from dask.distributed import Client

warnings.filterwarnings("ignore", module="coffea.*")


class MyProcessor(processor.ProcessorABC):
    def __init__(self):
        pass

    def process(self, events):
        
        dataset = events.metadata['dataset']
        xs = events.metadata['xs']
        lum = events.metadata['luminosity']
        process = events.metadata['process']
        genFiltEff = events.metadata["genFiltEff"] 

        print(f"Start of process {process}...")
        print("metadata: ", events.metadata)


        #Histograms for ID
        h_lepton_id = (
            had.Hist.new.StrCat([dataset], name="process")
            .Regular(3, 0.5, 3.5, name="Lepton_ID", label="Lepton ID")
            .Weight()
        )


        #Preselection Histograms
        h_met_preselection = (
            had.Hist.new.StrCat([dataset], name="process")
            .Regular(50, 0, 4000.0, name="met_preselection", label="MET [GeV]")
            .Weight()
        )

        h_leading_jet_preselection = (
            had.Hist.new.StrCat([dataset], name="process")
            .Regular(50, 0, 4000.0, name="leading_jet_preselection", label="Leading Jet [GeV]")
            .Weight()
        )

        h_leading_ph_pt_loose_preselection = (
            had.Hist.new.StrCat([dataset], name="process")
            .Regular(6, 0, 30, name="leading_ph_pt_loose_preselection", label="Leading Loose Photon Pt [GeV]")
            .Weight()
        )

        h_min_dphi_jet_met_preselection = (
            had.Hist.new.StrCat([dataset], name="process")
            .Regular(20, 0, 4, name="min_dphi_jet_met_preselection", label="min_dphi_jet_MET")
            .Weight()
        )

        h_min_dR_ph_loose_jet_preselection = (
            had.Hist.new.StrCat([dataset], name="process")
            .Regular(20, 0, 10.0, name="min_dR_ph_loose_jet_preselection", label="min_dR_ph_jet")
            .Weight()
        )
        
        #
        h_lep_n_preselection = (
            had.Hist.new.StrCat([dataset], name="process")
            .Regular(10, 0, 10.0, name="lep_n_preselection", label="Lepton Count")
            .Weight()
        )
        
        h_leading_ph_pt_tight_preselection = (
            had.Hist.new.StrCat([dataset], name="process")
            .Regular(6, 0, 30, name="leading_ph_pt_tight_preselection", label="Leading Tight Photon Pt [GeV]")
            .Weight()
        )
        
        h_leading_ph_eta_tight_preselection = (
            had.Hist.new.StrCat([dataset], name="process")
            .Regular(6, 0, 3, name="leading_ph_eta_tight_preselection", label="Leading Tight Photon Eta")
            .Weight()
        )
        
        h_dphi_met_leading_ph_tight_preselection = (
            had.Hist.new.StrCat([dataset], name="process")
            .Regular(8, 0, 4, name="dphi_met_leading_ph_tight_preselection", label="dphi_leading_tight_ph_met")
            .Weight()
        )
        
        h_dphi_leading_jet_met_preselection = (
            had.Hist.new.StrCat([dataset], name="process")
            .Regular(8, 0, 4, name="dphi_leading_jet_met_preselection", label="dphi_leading_jet_met")
            .Weight()
        )
        
        h_leading_ph_pt_tight_div_met_preselction = (
            had.Hist.new.StrCat([dataset], name="process")
            .Regular(8, 0, 4, name="leading_ph_pt_tight_div_met_preselection", label="Leading Tight Photon Pt / MET")
            .Weight()
        )
        
        h_dphi_div_dR_leading_ph_tight_met_preselection = (
            had.Hist.new.StrCat([dataset], name="process")
            .Regular(8, 0, 4, name="dphi_div_dR_leading_ph_tight_met_preselection", label="dphi_div_dR_leading_tight_photon_met")
            .Weight()
        )
        
        h_ph_truthOrigin_preselection = (
            had.Hist.new.StrCat([dataset], name="process")
            .Regular(48, -0.5, 47.5, name="ph_truthOrigin_preselection", label="Photon Truth Origin")
            .Weight()
        )
        
        
        #Signal Region Histograms
        
        
        
        h_met_SR = (
            had.Hist.new.StrCat([dataset], name="process")
            .Regular(50, 0, 4000.0, name="met_SR", label="MET [GeV]")
            .Weight()
        )

        h_leading_jet_SR = (
            had.Hist.new.StrCat([dataset], name="process")
            .Regular(50, 0, 4000.0, name="leading_jet_SR", label="Leading Jet [GeV]")
            .Weight()
        )

        h_leading_ph_pt_loose_SR = (
            had.Hist.new.StrCat([dataset], name="process")
            .Regular(6, 0, 30, name="leading_ph_pt_loose_SR", label="Leading Loose Photon Pt [GeV]")
            .Weight()
        )

        h_min_dphi_jet_met_SR = (
            had.Hist.new.StrCat([dataset], name="process")
            .Regular(20, 0, 4, name="min_dphi_jet_met_SR", label="min_dphi_jet_MET")
            .Weight()
        )

        h_min_dR_ph_loose_jet_SR= (
            had.Hist.new.StrCat([dataset], name="process")
            .Regular(20, 0, 10.0, name="min_dR_ph_loose_jet_SR", label="min_dR_ph_jet")
            .Weight()
        )
        
        #
        h_lep_n_SR = (
            had.Hist.new.StrCat([dataset], name="process")
            .Regular(10, 0, 10.0, name="lep_n_SR", label="Lepton Count")
            .Weight()
        )
        
        h_leading_ph_pt_tight_SR = (
            had.Hist.new.StrCat([dataset], name="process")
            .Regular(6, 0, 30, name="leading_ph_pt_tight_SR", label="Leading Tight Photon Pt [GeV]")
            .Weight()
        )
        
        h_leading_ph_eta_tight_SR = (
            had.Hist.new.StrCat([dataset], name="process")
            .Regular(6, 0, 3, name="leading_ph_eta_tight_SR", label="Leading Tight Photon Eta")
            .Weight()
        )
        
        h_dphi_met_leading_ph_tight_SR = (
            had.Hist.new.StrCat([dataset], name="process")
            .Regular(8, 0, 4, name="dphi_met_leading_ph_tight_SR", label="dphi_met_leading_ph_tight")
            .Weight()
        )
        
        h_dphi_leading_jet_met_SR = (
            had.Hist.new.StrCat([dataset], name="process")
            .Regular(8, 0, 4, name="dphi_leading_jet_met_SR", label="dphi_leading_jet_met")
            .Weight()
        )
        
        h_leading_ph_pt_tight_div_met_SR = (
            had.Hist.new.StrCat([dataset], name="process")
            .Regular(8, 0, 4, name="leading_ph_pt_tight_div_met_SR", label="Leading Tight Photon Pt / MET")
            .Weight()
        )
        
        h_dphi_div_dR_leading_ph_tight_met_SR = (
            had.Hist.new.StrCat([dataset], name="process")
            .Regular(8, 0, 4, name="dphi_div_dR_leading_ph_tight_met_SR", label="dphi_div_dR_leading_tight_photon_met")
            .Weight()
        )
        
        h_ph_truthOrigin_SR = (
            had.Hist.new.StrCat([dataset], name="process")
            .Regular(48, -0.5, 47.5, name="ph_truthOrigin_SR", label="Photon Truth Origin")
            .Weight()
        )




        evt_count = ak.num(events, axis = 0).compute()
        weights = (xs * genFiltEff * lum / evt_count) * np.ones(evt_count)  
        #weights = (xs * lum / evt_count) * np.ones(evt_count)

        #From ntuples
        jet_pt = events.jet.pt
        jet_phi = events.jet.phi
        jet_eta = events.jet.eta
        el_pt = events.el.pt
        el_phi = events.el.phi
        el_eta = events.el.eta
        mu_pt = events.mu.pt
        mu_phi = events.mu.phi
        mu_eta = events.mu.eta
        lep_pt = ak.concatenate((el_pt, mu_pt), axis = 1)
        lep_phi = ak.concatenate((el_phi, mu_phi), axis = 1)
        lep_eta = ak.concatenate((el_eta, mu_eta), axis = 1)
        lep_n = ak.num(lep_pt, axis = 1)
        ph_pt = events.ph.pt
        ph_phi = events.ph.phi
        ph_eta = events.ph.eta
        ph_isLoose = events.ph.select_loose
        ph_isTight = events.ph.select_tight
        ph_truthOrigin = events.ph.truthOrigin
        jet_n = ak.num(jet_pt, axis = 1)
        met_pt = events.met.met
        met_phi = events.met.phi
        b_jet_tag = events.jet.btag_select
       
    
        el_isLoose = events.el.select_loose
        el_isMedium = events.el.select_medium
        el_isTight = events.el.select_tight

        mu_isLoose = events.mu.select_loose
        mu_isMedium = events.mu.select_medium
        mu_isTight = events.mu.select_tight

        lep_isLoose = ak.concatenate((el_isLoose, mu_isLoose), axis = 1)
        lep_isMedium = ak.concatenate((el_isMedium, mu_isMedium), axis = 1) * 2
        lep_isTight = ak.concatenate((el_isTight, mu_isTight), axis = 1) * 3

        lep_ID = ak.concatenate((lep_isLoose, lep_isMedium, lep_isTight), axis = 1)
        #Calculated from variables from ntuples
        leading_jet_pt = ak.fill_none(ak.max(jet_pt, axis = 1), -999)

        ph_pt_loose = ph_pt * ph_isLoose
        ph_eta_loose = ph_eta * ph_isLoose
        ph_phi_loose = ph_phi * ph_isLoose
        #Get rid of zeros
        ph_pt_loose = ak.where(ph_pt_loose == 0, -999, ph_pt_loose)
        ph_eta_loose = ak.where(ph_pt_loose == 0, -999, ph_eta_loose)
        ph_phi_loose = ak.where(ph_pt_loose == 0, -999, ph_phi_loose)
        
        ph_pt_loose_sorted = ak.sort(ph_pt_loose, axis = 1, ascending = False)
        ph_eta_loose_sorted = ph_eta_loose[ak.argsort(ph_pt_loose, axis = 1, ascending = False)]
        ph_phi_loose_sorted = ph_phi_loose[ak.argsort(ph_pt_loose, axis = 1, ascending = False)]
       

        
        ph_pt_tight = ph_pt * ph_isTight
        ph_eta_tight = ph_eta * ph_isTight
        ph_phi_tight = ph_phi * ph_isTight
        #Get rid of zeros
        ph_pt_tight = ak.where(ph_pt_tight == 0, -999, ph_pt_tight)
        ph_eta_tight = ak.where(ph_pt_tight == 0, -999, ph_eta_tight)
        ph_phi_tight = ak.where(ph_pt_tight == 0, -999, ph_phi_tight)
        ph_pt_tight_sorted = ak.sort(ph_pt_tight, axis = 1, ascending = False)
        ph_eta_tight_sorted = ph_eta_tight[ak.argsort(ph_pt_tight, axis = 1, ascending = False)]
        ph_phi_tight_sorted = ph_phi_tight[ak.argsort(ph_pt_tight, axis = 1, ascending = False)]
        ph_tight_cond = ak.sum((ph_pt_tight != -999) * ak.ones_like(ph_pt_tight), axis = 1) > 1


        leading_ph_pt_tight_div_met = ak.fill_none(ak.max(ph_pt_tight, axis = 1) / met_pt, -999)

        b_jet_n = ak.sum(b_jet_tag, axis = 1)
        
        dphi_met_ph_tight = ak.fill_none(ak.firsts(ph_phi_tight_sorted, axis = 1) - met_phi, -999)
        dphi_jet_MET = abs(jet_phi - met_phi)
        dphi_leading_jet_met = ak.fill_none(abs(ak.firsts(jet_phi, axis = 1) - met_phi), -999)
        min_dphi_jet_MET = ak.fill_none(ak.min(dphi_jet_MET, axis = 1), -999) 
        
        dR_ph_loose_jet = ((ak.firsts(ph_eta_loose_sorted, axis = 1) - jet_eta)**2 + (ak.firsts(ph_phi_loose_sorted, axis = 1) - jet_phi)**2)**0.5
        min_dR_ph_loose_jet = ak.fill_none(ak.min(dR_ph_loose_jet, axis = 1), -999)
        
        dR_met_ph_tight = ((ak.firsts(ph_eta_tight_sorted, axis = 1))**2 + (ak.firsts(ph_phi_tight_sorted, axis = 1) - met_phi)**2)**0.5
        
        
        dphi_div_dR_leading_ph_tight_met = ak.fill_none(dphi_met_ph_tight / dR_met_ph_tight, -999)

        
        
        cut_preselection = (met_pt > 250 * 1000) & (lep_n == 0) & (leading_jet_pt > 100 * 1000) & (ak.max(ph_pt_loose, axis = 1) > 10 * 1000) & (min_dphi_jet_MET > 0.4) & (min_dR_ph_loose_jet > 0.4) & (b_jet_n == 0)
        
        cut_Nathan_SR = (ak.max(ph_pt_tight, axis = 1) > 10 * 1.0e3) & (met_pt > 375 * 1.0e3) & (ak.firsts(ph_eta_tight_sorted, axis = 1) < 2.5) & (lep_n == 0) & (dphi_met_ph_tight < 2.0) & (dphi_leading_jet_met > 3.1) & (leading_ph_pt_tight_div_met < 0.04) & (dphi_div_dR_leading_ph_tight_met > 0.75)
      
        
        #Apply preselection cuts
        
        met_pt_preselection = met_pt[cut_preselection]
        leading_jet_preselection = ak.fill_none(ak.max(jet_pt, axis = 1)[cut_preselection], 0)
        leading_ph_pt_loose_preselection = ak.fill_none(ak.max(ph_pt_loose, axis = 1),0)[cut_preselection]
        min_dphi_jet_MET_preselection = min_dphi_jet_MET[cut_preselection]
        min_dR_ph_loose_jet_preselection = min_dR_ph_loose_jet[cut_preselection]
        
        lep_n_preselection = lep_n[cut_preselection]
        leading_ph_pt_tight_preselection = ak.max(ph_pt_tight_sorted, axis = 1)[cut_preselection]
        leading_ph_eta_tight_preselection = ak.max(ph_eta_tight_sorted, axis = 1)[cut_preselection]
        dphi_met_ph_tight_preselection = dphi_met_ph_tight[cut_preselection]
        dphi_leading_jet_met_preselection = dphi_leading_jet_met[cut_preselection]
        leading_ph_pt_tight_div_met_preselection = leading_ph_pt_tight_div_met[cut_preselection]
        dphi_div_dR_leading_ph_tight_met_preselection = dphi_div_dR_leading_ph_tight_met[cut_preselection]
        ph_truthOrigin_preselection = ph_truthOrigin[cut_preselection]

        #Apply Nathan's SR to events that passed preselection
        cut_Nathan_SR_Preselection = cut_Nathan_SR[cut_preselection]
        
        met_pt_SR = met_pt_preselection[cut_Nathan_SR_Preselection]
        leading_jet_SR = leading_jet_preselection[cut_Nathan_SR_Preselection]
        leading_ph_pt_loose_SR = leading_ph_pt_loose_preselection[cut_Nathan_SR_Preselection]
        min_dphi_jet_met_SR = min_dphi_jet_MET_preselection[cut_Nathan_SR_Preselection]
        min_dR_ph_loose_jet_SR = min_dR_ph_loose_jet_preselection[cut_Nathan_SR_Preselection]
        
        lep_n_SR = lep_n_preselection[cut_Nathan_SR_Preselection]
        leading_ph_pt_tight_SR = leading_ph_pt_tight_preselection[cut_Nathan_SR_Preselection]
        leading_ph_eta_tight_SR = leading_ph_eta_tight_preselection[cut_Nathan_SR_Preselection]
        dphi_met_ph_tight_SR = dphi_met_ph_tight_preselection[cut_Nathan_SR_Preselection]
        dphi_leading_jet_met_SR = dphi_leading_jet_met_preselection[cut_Nathan_SR_Preselection]
        leading_ph_pt_tight_div_met_SR = leading_ph_pt_tight_div_met_preselection[cut_Nathan_SR_Preselection]
        dphi_div_dR_leading_ph_tight_met_SR = dphi_div_dR_leading_ph_tight_met_preselection[cut_Nathan_SR_Preselection]
        
        ph_truthOrigin_SR = ph_truthOrigin_preselection[cut_Nathan_SR_Preselection]

        #Histogram for ID
        h_lepton_id.fill(process = dataset, Lepton_ID = ak.flatten(lep_ID), weight = weights[0])
        print("Filled h_lepton_id")
        #Histograms for kinematics cut on
        
        #Preselection
        h_met_preselection.fill(process = dataset, met_preselection = met_pt_preselection / 1.0e3, weight = weights[0])

        print("Filled h_met_preselection")

        h_leading_jet_preselection.fill(process = dataset, leading_jet_preselection = leading_jet_preselection / 1.0e3, weight = weights[0])

        print("Filled h_leading_jet_preselection")

        h_leading_ph_pt_loose_preselection.fill(process = dataset, leading_ph_pt_loose_preselection = leading_ph_pt_loose_preselection / 1.0e3, weight = weights[0])

        print("Filled h_leading_ph_pt_loose_preselection")
        
        h_min_dphi_jet_met_preselection.fill(process = dataset, min_dphi_jet_met_preselection = min_dphi_jet_MET_preselection, weight = weights[0])

        print("Filled h_min_dphi_jet_met_preselection")

        h_min_dR_ph_loose_jet_preselection.fill(process = dataset, min_dR_ph_loose_jet_preselection = min_dR_ph_loose_jet_preselection, weight = weights[0])
        print("Filled h_min_dR_ph_loose_jet_preselection")
        
        #
        h_lep_n_preselection.fill(process = dataset, lep_n_preselection = lep_n_preselection, weight = weights[0])
        print("Filled h_lep_n_preselction")
        
        h_leading_ph_pt_tight_preselection.fill(process = dataset, leading_ph_pt_tight_preselection = leading_ph_pt_tight_preselection / 1.0e3, weight = weights[0])
        print("Filled h_leading_ph_pt_tight_preselection")
        
        h_leading_ph_eta_tight_preselection.fill(process = dataset, leading_ph_eta_tight_preselection = leading_ph_eta_tight_preselection, weight = weights[0])
        print("Filled h_leading_ph_eta_tight_preselection")
        
        h_dphi_met_leading_ph_tight_preselection.fill(process = dataset, dphi_met_leading_ph_tight_preselection = dphi_met_ph_tight_preselection, weight = weights[0])
        print("Filled h_dphi_met_leading_ph_tight_preselection")
        
        h_dphi_leading_jet_met_preselection.fill(process = dataset, dphi_leading_jet_met_preselection = dphi_leading_jet_met_preselection, weight = weights[0])
        print("Filled h_dphi_leading_jet_met_preselection")
        
        h_leading_ph_pt_tight_div_met_preselction.fill(process = dataset, leading_ph_pt_tight_div_met_preselection = leading_ph_pt_tight_div_met_preselection, weight = weights[0])
        print("Filled h_leading_ph_pt_tight_div_met_preselction")
        
        h_dphi_div_dR_leading_ph_tight_met_preselection.fill(process = dataset, dphi_div_dR_leading_ph_tight_met_preselection = dphi_div_dR_leading_ph_tight_met_preselection, weight = weights[0])
        print("Filled h_dphi_div_dR_leading_ph_tight_met_preselection")
        
        h_ph_truthOrigin_preselection.fill(process = dataset, ph_truthOrigin_preselection = ak.ravel(ph_truthOrigin_preselection), weight = weights[0]) 
        print("Filled h_ph_truthOrigin_preselection")
        
        
        #Signal Region
        h_met_SR.fill(process = dataset, met_SR = met_pt_SR / 1.0e3, weight = weights[0])

        print("Filled h_met_SR")

        h_leading_jet_SR.fill(process = dataset, leading_jet_SR = leading_jet_SR / 1.0e3, weight = weights[0])

        print("Filled h_leading_jet_SR")

        h_leading_ph_pt_loose_SR.fill(process = dataset, leading_ph_pt_loose_SR = leading_ph_pt_loose_SR / 1.0e3, weight = weights[0])

        print("Filled h_leading_ph_pt_loose_SR")
        
        h_min_dphi_jet_met_SR.fill(process = dataset, min_dphi_jet_met_SR = min_dphi_jet_met_SR, weight = weights[0])

        print("Filled h_min_dphi_jet_met_SR")

        h_min_dR_ph_loose_jet_SR.fill(process = dataset, min_dR_ph_loose_jet_SR = min_dR_ph_loose_jet_SR, weight = weights[0])
        print("Filled h_min_dR_ph_loose_jet_SR")
        
        #
        
        h_lep_n_SR.fill(process = dataset, lep_n_SR = lep_n_SR, weight = weights[0])
        print("Filled h_lep_n_SR")
        
        h_leading_ph_pt_tight_SR.fill(process = dataset, leading_ph_pt_tight_SR = leading_ph_pt_tight_SR / 1.0e3, weight = weights[0])
        print("Filled h_leading_ph_pt_tight_SR")
        
        h_leading_ph_eta_tight_SR.fill(process = dataset, leading_ph_eta_tight_SR = leading_ph_eta_tight_SR, weight = weights[0])
        print("Filled h_leading_ph_eta_tight_SR")
        
        h_dphi_met_leading_ph_tight_SR.fill(process = dataset, dphi_met_leading_ph_tight_SR = dphi_met_ph_tight_SR, weight = weights[0])
        print("Filled h_dphi_met_leading_ph_tight_SR")
        
        h_dphi_leading_jet_met_SR.fill(process = dataset, dphi_leading_jet_met_SR = dphi_leading_jet_met_SR, weight = weights[0])
        print("Filled dphi_leading_jet_met_SR")
        
        h_leading_ph_pt_tight_div_met_SR.fill(process = dataset, leading_ph_pt_tight_div_met_SR = leading_ph_pt_tight_div_met_SR, weight = weights[0])
        print("Filled h_leading_ph_pt_tight_div_met_SR")
        
        h_dphi_div_dR_leading_ph_tight_met_SR.fill(process = dataset, dphi_div_dR_leading_ph_tight_met_SR = dphi_div_dR_leading_ph_tight_met_SR, weight = weights[0])
        print("Filled h_dphi_div_dR_leading_ph_tight_met_SR")

        h_ph_truthOrigin_SR.fill(process = dataset, ph_truthOrigin_SR = ak.ravel(ph_truthOrigin_SR), weight = weights[0])
        print("Filled h_ph_truthOrigin_SR")
        
        return {"histograms": {"h_met_preselection": h_met_preselection, "h_leading_jet_preselection": h_leading_jet_preselection, "h_leading_ph_pt_loose_preselction": h_leading_ph_pt_loose_preselection, "h_min_dphi_jet_met_preselection": h_min_dphi_jet_met_preselection, "h_min_dR_ph_loose_jet_preselection": h_min_dR_ph_loose_jet_preselection, "h_lep_n_preselection": h_lep_n_preselection, "h_leading_ph_pt_tight_preselection": h_leading_ph_pt_tight_preselection, "h_leading_ph_eta_tight_preselection": h_leading_ph_eta_tight_preselection, "h_dphi_met_leading_ph_tight_preselection": h_dphi_met_leading_ph_tight_preselection, "h_dphi_leading_jet_met_preselection": h_dphi_leading_jet_met_preselection, "h_leading_ph_pt_tight_div_met_preselction": h_leading_ph_pt_tight_div_met_preselction, "h_dphi_div_dR_leading_ph_tight_met_preselection": h_dphi_div_dR_leading_ph_tight_met_preselection, "h_ph_truthOrigin_preselection": h_ph_truthOrigin_preselection, "h_met_SR": h_met_SR, "h_leading_jet_SR": h_leading_jet_SR, "h_leading_ph_pt_loose_SR": h_leading_ph_pt_loose_SR, "h_min_dphi_jet_met_SR": h_min_dphi_jet_met_SR, "h_min_dR_ph_loose_jet_SR": h_min_dR_ph_loose_jet_SR, "h_lep_n_SR": h_lep_n_SR, "h_leading_ph_pt_tight_SR": h_leading_ph_pt_tight_SR, "h_leading_ph_eta_tight_SR": h_leading_ph_eta_tight_SR, "h_dphi_met_leading_ph_tight_SR": h_dphi_met_leading_ph_tight_SR, "h_dphi_leading_jet_met_SR": h_dphi_leading_jet_met_SR, "h_leading_ph_pt_tight_div_met_SR": h_leading_ph_pt_tight_div_met_SR, "h_dphi_div_dR_leading_ph_tight_met_SR": h_dphi_div_dR_leading_ph_tight_met_SR, "h_ph_truthOrigin_SR": h_ph_truthOrigin_SR, "h_select_id": h_lepton_id}, "process": process}

    def postprocess(self, accumulator):
        pass


if __name__ == "__main__":
    start_time = time.time()


    sig_xs = {"545759": 22670.1, "545760": 22670.1, "545761": 22670.1,"545762": 22670.1, "545763": 22670.1, "545764": 22670.1, 
            "545765": 1807.39, "545766": 1807.39, "545767": 1807.39, "545768": 1807.39, "545769": 1807.39, "545770": 1807.39,
            "545771": 121.013, "545772": 121.013, "545773": 121.013, "545774": 121.013, "545775": 121.013, "545776": 121.013,
            545777: 545.57} #fb

    sig_filter_eff = {"545759": 5.029841E-02, "5457560": 5.091961E-02, "545761": 5.187749E-02, "545762": 5.713781E-02, "545763": 1.138526E-01, "545764": 1.513492E-01,
            "545765": 9.503700E-02, "545766": 9.814262E-02, "545767": 1.022704E-01, "545768": 1.087524E-01, "545769": 1.784614E-01, "545770": 2.310872E-01,
            "545771": 1.461057E-01, "545772": 1.531744E-01, "545773": 1.599781E-01, "545774": 1.677462E-01, "545775": 2.452122E-01, "545776": 3.095950E-01,
            "545777": 1.087590E-01}

    bkg_xs = {"700335": 447130.00000000005, "700336": 447130.00000000005, "700337": 447130.00000000005, "700338": 21742000., "700339": 21742000, "700340": 21742000,
            "700341": 21806000, "700342": 21806000, "700343": 21806000, "700344": 7680000, "700345": 7680000, "700346": 7680000, "700347": 14126000, "700348": 14126000, 
            "700349": 14126000, "700401": 56438., "700402": 364840., "700403": 364830., "700404": 364840.} #fb

    bkg_filter_eff = {"700335": 8.426931E-02, "700336": 0.202381, "700337": 7.127170E-01, "700338": 9.376371E-03, "700339": 0.1489766, "700340": 8.435958E-01, 
            "700341": 0.0097968, "700342": 0.1460112, "700343": 8.435538E-01, "700344": 9.011307E-03, "700345": 0.146033, "700346": 8.474706E-01, "700347": 0.00867775, "700348": 1.433724E-01,
            "700349": 8.474573E-01, "700401": 1.000000E+00, "700402": 1.000000E+00, "700403": 1.000000E+00, "700404": 1.000000E+00}

    lum = 140 #fb-1


    
    files_signal_N2_100_N1_97 = glob.glob("/data/maclwong/Signal_Sample_Ntuples/09_11_2024/*N2_100_N1_97*ANALYSIS.root/*")
    files_signal_N2_100_N1_95 = glob.glob("/data/maclwong/Signal_Sample_Ntuples/09_11_2024/*N2_100_N1_95*ANALYSIS.root/*")
    files_signal_N2_100_N1_90 = glob.glob("/data/maclwong/Signal_Sample_Ntuples/09_11_2024/*N2_100_N1_90*ANALYSIS.root/*")
    files_signal_N2_100_N1_85 = glob.glob("/data/maclwong/Signal_Sample_Ntuples/09_11_2024/*N2_100_N1_85*ANALYSIS.root/*")
    files_signal_N2_100_N1_60 = glob.glob("/data/maclwong/Signal_Sample_Ntuples/09_11_2024/*N2_100_N1_60*ANALYSIS.root/*")
    files_signal_N2_100_N1_40 = glob.glob("/data/maclwong/Signal_Sample_Ntuples/09_11_2024/*N2_100_N1_40*ANALYSIS.root/*")

    files_signal_N2_200_N1_197 = glob.glob("/data/maclwong/Signal_Sample_Ntuples/09_11_2024/*N2_200_N1_197*ANALYSIS.root/*")
    files_signal_N2_200_N1_195 = glob.glob("/data/maclwong/Signal_Sample_Ntuples/09_11_2024/*N2_200_N1_195*ANALYSIS.root/*")
    files_signal_N2_200_N1_190 = glob.glob("/data/maclwong/Signal_Sample_Ntuples/09_11_2024/*N2_200_N1_190*ANALYSIS.root/*")
    files_signal_N2_200_N1_185 = glob.glob("/data/maclwong/Signal_Sample_Ntuples/09_11_2024/*N2_200_N1_185*ANALYSIS.root/*")
    files_signal_N2_200_N1_160 = glob.glob("/data/maclwong/Signal_Sample_Ntuples/09_11_2024/*N2_200_N1_160*ANALYSIS.root/*")
    files_signal_N2_200_N1_140 = glob.glob("/data/maclwong/Signal_Sample_Ntuples/09_11_2024/*N2_200_N1_140*ANALYSIS.root/*")

    files_signal_N2_400_N1_397 = glob.glob("/data/maclwong/Signal_Sample_Ntuples/09_11_2024/*N2_400_N1_397*ANALYSIS.root/*")
    files_signal_N2_400_N1_395 = glob.glob("/data/maclwong/Signal_Sample_Ntuples/09_11_2024/*N2_400_N1_395*ANALYSIS.root/*")
    files_signal_N2_400_N1_390 = glob.glob("/data/maclwong/Signal_Sample_Ntuples/09_11_2024/*N2_400_N1_390*ANALYSIS.root/*")
    files_signal_N2_400_N1_385 = glob.glob("/data/maclwong/Signal_Sample_Ntuples/09_11_2024/*N2_400_N1_385*ANALYSIS.root/*")
    files_signal_N2_400_N1_360 = glob.glob("/data/maclwong/Signal_Sample_Ntuples/09_11_2024/*N2_400_N1_360*ANALYSIS.root/*")
    files_signal_N2_400_N1_340 = glob.glob("/data/maclwong/Signal_Sample_Ntuples/09_11_2024/*N2_400_N1_340*ANALYSIS.root/*")

    files_signal_N2_220_N1_200_HH = glob.glob("/data/maclwong/Signal_Sample_Ntuples/09_11_2024/*N2_220_N1_200_HH*ANALYSIS.root/*")



    files_bkg_Znunu1 = glob.glob("/data/maclwong/Ben_Bkg_Samples/08_06_2024/*700335*Znunu*ANALYSIS.root/*")
    files_bkg_Znunu2 = glob.glob("/data/maclwong/Ben_Bkg_Samples/08_06_2024/*700336*Znunu*ANALYSIS.root/*")
    files_bkg_Znunu3 = glob.glob("/data/maclwong/Ben_Bkg_Samples/08_06_2024/*700337*Znunu*ANALYSIS.root/*")
    
    files_bkg_Wenu1 = glob.glob("/data/maclwong/Ben_Bkg_Samples/08_06_2024/*700338*Wenu*ANALYSIS.root/*")
    files_bkg_Wenu2 = glob.glob("/data/maclwong/Ben_Bkg_Samples/08_06_2024/*700339*Wenu*ANALYSIS.root/*")
    files_bkg_Wenu3 = glob.glob("/data/maclwong/Ben_Bkg_Samples/08_06_2024/*700340*Wenu*ANALYSIS.root/*")
    
    files_bkg_Wmunu1 = glob.glob("/data/maclwong/Ben_Bkg_Samples/08_06_2024/*700341*Wmunu*ANALYSIS.root/*")
    files_bkg_Wmunu2 = glob.glob("/data/maclwong/Ben_Bkg_Samples/08_06_2024/*700342*Wmunu*ANALYSIS.root/*")
    files_bkg_Wmunu3 = glob.glob("/data/maclwong/Ben_Bkg_Samples/08_06_2024/*700343*Wmunu*ANALYSIS.root/*")
    
    files_bkg_WtaunuL1 = glob.glob("/data/maclwong/Ben_Bkg_Samples/08_06_2024/*700344*Wtaunu_L*ANALYSIS.root/*")
    files_bkg_WtaunuL2 = glob.glob("/data/maclwong/Ben_Bkg_Samples/08_06_2024/*700345*Wtaunu_L*ANALYSIS.root/*")
    files_bkg_WtaunuL3 = glob.glob("/data/maclwong/Ben_Bkg_Samples/08_06_2024/*700346*Wtaunu_L*ANALYSIS.root/*")
    
    files_bkg_WtaunuH1 = glob.glob("/data/maclwong/Ben_Bkg_Samples/08_06_2024/*700347*Wtaunu_H*ANALYSIS.root/*")
    files_bkg_WtaunuH2 = glob.glob("/data/maclwong/Ben_Bkg_Samples/08_06_2024/*700348*Wtaunu_H*ANALYSIS.root/*")
    files_bkg_WtaunuH3 = glob.glob("/data/maclwong/Ben_Bkg_Samples/08_06_2024/*700349*Wtaunu_H*ANALYSIS.root/*")
    
    files_bkg_Znunugamma = glob.glob("/data/maclwong/Ben_Bkg_Samples/08_06_2024/*700401*Znunugamma*ANALYSIS.root/*")
    
    files_bkg_Wmunugamma = glob.glob("/data/maclwong/Ben_Bkg_Samples/08_06_2024/*700402*Wmunugamma*ANALYSIS.root/*")
    
    files_bkg_Wenugamma = glob.glob("/data/maclwong/Ben_Bkg_Samples/08_06_2024/*700403*Wenugamma*ANALYSIS.root/*")
    
    files_bkg_Wtaunugamma = glob.glob("/data/maclwong/Ben_Bkg_Samples/08_06_2024/*700404*Wtaunugamma*ANALYSIS.root/*")


    dataset_signal_N2_100_N1_97 = {fname: "analysis" for fname in files_signal_N2_100_N1_97} 
    dataset_signal_N2_100_N1_95 = {fname: "analysis" for fname in files_signal_N2_100_N1_95}
    dataset_signal_N2_100_N1_90 = {fname: "analysis" for fname in files_signal_N2_100_N1_90}
    dataset_signal_N2_100_N1_85 = {fname: "analysis" for fname in files_signal_N2_100_N1_85}
    dataset_signal_N2_100_N1_60 = {fname: "analysis" for fname in files_signal_N2_100_N1_60}
    dataset_signal_N2_100_N1_40 = {fname: "analysis" for fname in files_signal_N2_100_N1_40}

    dataset_signal_N2_200_N1_197 = {fname: "analysis" for fname in files_signal_N2_200_N1_197}
    dataset_signal_N2_200_N1_195 = {fname: "analysis" for fname in files_signal_N2_200_N1_195}
    dataset_signal_N2_200_N1_190 = {fname: "analysis" for fname in files_signal_N2_200_N1_190}
    dataset_signal_N2_200_N1_185 = {fname: "analysis" for fname in files_signal_N2_200_N1_185}
    dataset_signal_N2_200_N1_160 = {fname: "analysis" for fname in files_signal_N2_200_N1_160}
    dataset_signal_N2_200_N1_140 = {fname: "analysis" for fname in files_signal_N2_200_N1_140}

    dataset_signal_N2_400_N1_397 = {fname: "analysis" for fname in files_signal_N2_400_N1_397}
    dataset_signal_N2_400_N1_395 = {fname: "analysis" for fname in files_signal_N2_400_N1_395}
    dataset_signal_N2_400_N1_390 = {fname: "analysis" for fname in files_signal_N2_400_N1_390}
    dataset_signal_N2_400_N1_385 = {fname: "analysis" for fname in files_signal_N2_400_N1_385}
    dataset_signal_N2_400_N1_360 = {fname: "analysis" for fname in files_signal_N2_400_N1_360}
    dataset_signal_N2_400_N1_340 = {fname: "analysis" for fname in files_signal_N2_400_N1_340}
    
    dataset_signal_N2_220_N1_200_HH = {fname: "analysis" for fname in files_signal_N2_220_N1_200_HH}
    


    dataset_bkg_Znunu1 = {fname: "analysis" for fname in files_bkg_Znunu1}
    dataset_bkg_Znunu2 = {fname: "analysis" for fname in files_bkg_Znunu2}
    dataset_bkg_Znunu3 = {fname: "analysis" for fname in files_bkg_Znunu3}

    dataset_bkg_Wenu1 = {fname: "analysis" for fname in files_bkg_Wenu1}
    dataset_bkg_Wenu2 = {fname: "analysis" for fname in files_bkg_Wenu2}
    dataset_bkg_Wenu3 = {fname: "analysis" for fname in files_bkg_Wenu3}

    dataset_bkg_Wmunu1 = {fname: "analysis" for fname in files_bkg_Wmunu1} 
    dataset_bkg_Wmunu2 = {fname: "analysis" for fname in files_bkg_Wmunu2}
    dataset_bkg_Wmunu3 = {fname: "analysis" for fname in files_bkg_Wmunu3}

    dataset_bkg_WtaunuL1 = {fname: "analysis" for fname in files_bkg_WtaunuL1}
    dataset_bkg_WtaunuL2 = {fname: "analysis" for fname in files_bkg_WtaunuL2}
    dataset_bkg_WtaunuL3 = {fname: "analysis" for fname in files_bkg_WtaunuL3}

    dataset_bkg_WtaunuH1 = {fname: "analysis" for fname in files_bkg_WtaunuH1}
    dataset_bkg_WtaunuH2 = {fname: "analysis" for fname in files_bkg_WtaunuH2}
    dataset_bkg_WtaunuH3 = {fname: "analysis" for fname in files_bkg_WtaunuH3}

    dataset_bkg_Znunugamma = {fname: "analysis" for fname in files_bkg_Znunugamma}
    dataset_bkg_Wmunugamma = {fname: "analysis" for fname in files_bkg_Wmunugamma}
    dataset_bkg_Wenugamma = {fname: "analysis" for fname in files_bkg_Wenugamma}
    dataset_bkg_Wtaunugamma = {fname: "analysis" for fname in files_bkg_Wtaunugamma}


    p = MyProcessor()

    fileset = {"N2_100_N1_97_WB_signal": {"files": dataset_signal_N2_100_N1_97, "metadata": {"xs": sig_xs["545759"], "genFiltEff": sig_filter_eff["545759"], "process": "N2_100_N1_97_WB_signal", "luminosity": lum}},
            "Znunu_bkg1": {"files": dataset_bkg_Znunu1, "metadata": {"xs": bkg_xs["700335"], "genFiltEff": bkg_filter_eff["700335"], "process": "Znunu", "luminosity": lum}},
            "Znunu_bkg2": {"files": dataset_bkg_Znunu2, "metadata": {"xs": bkg_xs["700336"], "genFiltEff": bkg_filter_eff["700336"], "process": "Znunu", "luminosity": lum}},
            "Znunu_bkg3": {"files": dataset_bkg_Znunu3, "metadata": {"xs": bkg_xs["700337"], "genFiltEff": bkg_filter_eff["700337"], "process": "Znunu", "luminosity": lum}},
            
            "Wenu_bkg1": {"files": dataset_bkg_Wenu1, "metadata": {"xs": bkg_xs["700338"], "genFiltEff": bkg_filter_eff["700338"],"process": "Wenu", "luminosity": lum}},
            "Wenu_bkg2": {"files": dataset_bkg_Wenu2, "metadata": {"xs": bkg_xs["700339"], "genFiltEff": bkg_filter_eff["700339"],"process": "Wenu", "luminosity": lum}},
            "Wenu_bkg3": {"files": dataset_bkg_Wenu3, "metadata": {"xs": bkg_xs["700340"], "genFiltEff": bkg_filter_eff["700340"],"process": "Wenu", "luminosity": lum}},
                                    
            "Wmunu_bkg1": {"files": dataset_bkg_Wmunu1, "metadata": {"xs": bkg_xs["700341"], "genFiltEff": bkg_filter_eff["700341"],"process": "Wmunu", "luminosity": lum}},
            "Wmunu_bkg2": {"files": dataset_bkg_Wmunu2, "metadata": {"xs": bkg_xs["700342"], "genFiltEff": bkg_filter_eff["700342"],"process": "Wmunu", "luminosity": lum}},
            "Wmunu_bkg3": {"files": dataset_bkg_Wmunu3, "metadata": {"xs": bkg_xs["700343"], "genFiltEff": bkg_filter_eff["700343"],"process": "Wmunu", "luminosity": lum}},
                                    
            "Wtaunu_L_bkg1": {"files": dataset_bkg_WtaunuL1, "metadata": {"xs": bkg_xs["700344"], "genFiltEff": bkg_filter_eff["700344"], "process": "Wtaunu_L", "luminosity": lum}},
            "Wtaunu_L_bkg2": {"files": dataset_bkg_WtaunuL2, "metadata": {"xs": bkg_xs["700345"], "genFiltEff": bkg_filter_eff["700345"], "process": "Wtaunu_L", "luminosity": lum}},
            "Wtaunu_L_bkg3": {"files": dataset_bkg_WtaunuL3, "metadata": {"xs": bkg_xs["700346"], "genFiltEff": bkg_filter_eff["700346"], "process": "Wtaunu_L", "luminosity": lum}},
                                    
            "Wtaunu_H_bkg1": {"files": dataset_bkg_WtaunuH1, "metadata": {"xs": bkg_xs["700347"], "genFiltEff": bkg_filter_eff["700347"], "process": "Wtaunu_H", "luminosity": lum}},
            "Wtaunu_H_bkg2": {"files": dataset_bkg_WtaunuH2, "metadata": {"xs": bkg_xs["700348"], "genFiltEff": bkg_filter_eff["700348"], "process": "Wtaunu_H", "luminosity": lum}},
            "Wtaunu_H_bkg3": {"files": dataset_bkg_WtaunuH3, "metadata": {"xs": bkg_xs["700349"], "genFiltEff": bkg_filter_eff["700349"], "process": "Wtaunu_H", "luminosity": lum}},
            
            "Znunugamma_bkg": {"files": dataset_bkg_Znunugamma, "metadata": {"xs": bkg_xs["700401"], "genFiltEff": bkg_filter_eff["700401"], "process": "Znunugamma", "luminosity": lum}},
            "Wmunugamma_bkg": {"files": dataset_bkg_Wmunugamma, "metadata": {"xs": bkg_xs["700402"], "genFiltEff": bkg_filter_eff["700402"], "process": "Wmunugamma", "luminosity": lum}},
            "Wenugamma_bkg": {"files": dataset_bkg_Wenugamma, "metadata": {"xs": bkg_xs["700403"], "genFiltEff": bkg_filter_eff["700403"], "process": "Wenugamma", "luminosity": lum}},
            "Wtaunugamma_bkg": {"files": dataset_bkg_Wtaunugamma, "metadata": {"xs": bkg_xs["700404"], "genFiltEff": bkg_filter_eff["700404"], "process": "Wtaunugamma", "luminosity": lum}},
            }
    







    #To faciliate usage with HTCondor 
    cluster = HTCondorCluster(log_directory="/home/maclwong/SUSY_Run3/light-roast/", cores=2, memory="32GB", disk="32GB", n_workers = 500)
 
    cluster.scale(jobs= 10 * len(fileset))
    print(f"JOB SCRIPT: {cluster.job_script()}")
    client = Client(cluster)
    #dask.config.set(scheduler='multiprocessing')

    dataset_runnable, dataset_updated = preprocess(
        fileset,
        align_clusters=False,
        step_size=100_000,
        files_per_batch=1,
        skip_bad_files=True,
        save_form=False,
    )

    out = apply_to_fileset(
                p,
                max_chunks(dataset_runnable, 300),
                schemaclass=LightRoastSchema, 
            )
    #print(out['Znunu']['histograms']['h_met'].keys())
    #out['Znunu']['histograms']['h_met'].dask.visualize(filename="visualization.png")   
    print("Beginning of dask.compute()")
    (computed,) = dask.compute(out)

    print("Finshed dask.compute")
    print("Computed Objects: ", computed)

    #List of special histograms.  These histograms need special modifications
    special_hists = ["h_ph_truthOrigin_SR", "h_ph_truthOrigin_preselection"]
    for h in computed[list(fileset.keys())[0]]['histograms'].keys():
        

        bins = []
        process_contrib_sig = []
        process_contrib_bkg = []
        
        labels_sig = []
        labels_bkg = []

        #Dictionary to collect all events of the same process separated by file due to a difference in DSID.  Will combine into a single process array
        contrib_sig_separated = {}
        contrib_bkg_separated = {}
        
        for process in computed.keys():
            pc, f, b = computed[process]['histograms'][h].to_numpy()
            pc_mod_dim = np.concatenate((pc[0], [0])) #Adds one element so shape of b matches shape of pc
            bins = b
            l = computed[process]['process']
            if "signal" in process:
                #process_contrib_sig.append(pc_mod_dim.tolist())
                #labels_sig.append(l)
                if(l not in contrib_sig_separated.keys()):
                    contrib_sig_separated[l] = np.array(pc_mod_dim)
                else:
                    contrib_sig_separated[l] = contrib_sig_separated[l] + pc_mod_dim
            elif "bkg" in process:
                if(l not in contrib_bkg_separated.keys()):
                    contrib_bkg_separated[l] = np.array(pc_mod_dim)
                else:
                    contrib_bkg_separated[l] = contrib_bkg_separated[l] + pc_mod_dim
                    
                #process_contrib_bkg.append(pc_mod_dim.tolist())
                #labels_bkg.append(l)
        
        #Sort and plot sig and bkg data

        for process in contrib_sig_separated.keys():
            process_contrib_sig.append(contrib_sig_separated[process].tolist())
            labels_sig.append(process)
        
        for process in contrib_bkg_separated.keys():
            process_contrib_bkg.append(contrib_bkg_separated[process].tolist())
            labels_bkg.append(process)
        
        sample_count = ak.sum(process_contrib_bkg, axis = 1)
        process_contrib_bkg_sorted = np.array(process_contrib_bkg)[np.argsort(sample_count)]
        labels_bkg_sorted = np.array(labels_bkg)[np.argsort(sample_count)]
        
        #Checks if it is a special hist

        if(h in special_hists):
            if("h_ph_truthOrigin" in h):
                fig, ax = plt.subplots(2,1,figsize = (15,12)) 
                bins_mid = int(len(bins)/2)
                bins1 = bins[:bins_mid + 1]
                bins2 = bins[bins_mid:]

                
                #Split process_contrib_bkg_sorted into 2
                process_contrib_bkg_sorted1 = []
                process_contrib_bkg_sorted2 = []
                for pc_sep in process_contrib_bkg_sorted:
                    process_contrib_bkg_sorted1.append(pc_sep[:bins_mid + 1])
                    process_contrib_bkg_sorted2.append(pc_sep[bins_mid:])
                

                ax[0].stackplot(bins1, process_contrib_bkg_sorted1, step = 'post', labels = labels_bkg_sorted)
                ax[1].stackplot(bins2, process_contrib_bkg_sorted2, step = 'post', labels = labels_bkg_sorted)
                
                ax[0].set_xticks(np.arange(len(bins)))
                ax[1].set_xticks(np.arange(len(bins)))

                for i, pc_sig in enumerate(process_contrib_sig):
                    pc_sig1 = pc_sig[:bins_mid + 1]
                    pc_sig2 = pc_sig[bins_mid:]

                    ax[0].step(bins1, pc_sig1, where = 'post', label = labels_sig[i])
                    ax[1].step(bins2, pc_sig2, where = 'post', label = labels_sig[i])
           

                ax[1].legend(loc = "upper center", fontsize = 12)
     
                ax[0].set_yscale("log")
                ax[1].set_yscale("log")
                ax[0].tick_params(axis='y', labelsize=20)
                ax[1].tick_params(axis='y', labelsize=20)
                ax[0].set_xlabel("Photon Origin", fontsize = 20)
                ax[1].set_xlabel(f"Photon Origin", fontsize = 20)
                ax[0].set_xlim(-0.5,bins1[-1])
                ax[1].set_xlim(bins2[0], bins2[-1])
               
                #x-tick labels
                particle_id = {"Undef": 0, "SingleElec": 1, "SingleMuon": 2, "SinglePhot": 3, "SingleTau": 4, "PhotonConv": 5, "DalitzDec": 6, 
                        "ElMagProc": 7, "Mu": 8, "TauLep": 9, "top": 10, "QuarkWeakDec": 11, "WBoson": 12, "ZBoson": 13, "Higgs": 14, "HiggsMSSM": 15, "HeavyBoson": 16, 
                        "WBosonLRSM": 17, "NuREle": 18, "NuRMu": 19, "NuRTau": 20, "LQ": 21, "SUSY": 22, "LightMeson": 23, "StrangeMeson": 24, "CharmedMeson": 25, 
                        "BottomMeson": 26, "CCbarMeson": 27, "JPsi": 28, "BBbarMeson": 29, "LightBaryon": 30, "StrangeBaryon": 31, "CharmedBaryon": 32, "BottomBaryon": 33, 
                        "PionDecay": 34, "KaonDecay": 35, "BremPhot": 36, "PromptPhot": 37, "UndrPhot": 38, "ISRPhot": 39, "FSRPhot": 40, "NucReact": 41, "PiZero": 42, 
                        "DiBoson": 43, "ZorHeavyBoson":44, "QCD":45, "OtherBSM": 46, "MultiBoson": 47, "Null": 999}

                particle_id_key = np.array(list(particle_id.keys()))
                particle_id_num = np.array(list(particle_id.values()))

                particle_id_key_sorted = particle_id_key[np.argsort(particle_id_num)]
                particle_id_num_sorted = np.sort(particle_id_num)
                
                ax[0].set_xticklabels(particle_id_key_sorted, rotation = -45)
                ax[1].set_xticklabels(particle_id_key_sorted, rotation = -45)
                #Find max y-value
                max_y = 10 * np.max(np.sum(np.transpose(process_contrib_bkg_sorted), axis = 1))
                ax[0].set_ylim(top = max_y)
                ax[1].set_ylim(top = max_y)
                fig.suptitle(f'{h} for All Samples', fontsize = 30)
                fig.savefig(f"SUSY_Hists/{h}.png")
                plt.close(fig)
                #ax.set_xticklabels(failed_ch, rotation = -45)
        else:
            fig, ax = plt.subplots()
            ax.stackplot(bins, process_contrib_bkg_sorted, step = 'post', labels = labels_bkg_sorted)
        
            #Plot signal
        
            for i, pc_sig in enumerate(process_contrib_sig):
                ax.step(bins, pc_sig, where = 'post', label = labels_sig[i])

            ax.legend()
            ax.set_yscale("log")
            ax.set_xlabel(f"{h} [GeV]")
            ax.set_title(f'{h} for All Samples')
        
            fig.savefig(f"SUSY_Hists/{h}.png")
            plt.close(fig)

    end_time = time.time()

    print("Execution time: ", end_time - start_time)

