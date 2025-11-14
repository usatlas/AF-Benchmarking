# common fragment for xAODPhoton filter
# conversion to XAOD, 
# creation of slimmed container containing photons
# connecting the filter

include ("GeneratorFilters/CreatexAODSlimContainers.py")
createxAODSlimmedContainer("TruthPhotons",prefiltSeq)
prefiltSeq.xAODCnv.AODContainerName = 'GEN_EVENT'

from GeneratorFilters.GeneratorFiltersConf import xAODPhotonFilter
xAODPhotonFilter = xAODPhotonFilter("xAODPhotonFilter")  
filtSeq += xAODPhotonFilter

# to modiify cuts put into JOs sth. like:
#filtSeq.xAODPhotonFilter.PtMin = 12000.0
#filtSeq.xAODPhotonFilter.PtMax = 9000000000.0
#filtSeq.xAODPhotonFilter.EtaCut = 10.0
#filtSeq.xAODPhotonFilter.NPhotons = 2

