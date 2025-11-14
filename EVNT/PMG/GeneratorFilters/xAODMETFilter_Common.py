# common fragment for xAODMissingEt filter
# conversion to XAOD, 
# creation of slimmed container containing MET
# connecting the filter

include ("GeneratorFilters/CreatexAODSlimContainers.py")
createxAODSlimmedContainer("TruthMET",prefiltSeq)
prefiltSeq.xAODCnv.AODContainerName = 'GEN_EVENT'

from GeneratorFilters.GeneratorFiltersConf import xAODMETFilter
xAODMissingEtFilter = xAODMETFilter("xAODMissingEtFilter")  
filtSeq += xAODMissingEtFilter

# to modiify cuts put into JOs e.g.:
#filtSeq.xAODMissingEtFilter.METCut = 12000.0
#filtSeq.xAODMissingEtFilter.UseNeutrinosFromHadrons = False
