import FWCore.ParameterSet.Config as cms

process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff")
process.load("CondCore.DBCommon.CondDBSetup_cfi")
process.load('Configuration/StandardSequences/Reconstruction_cff')
process.load('Configuration/StandardSequences/MagneticField_AutoFromDBCurrent_cff')
process.MessageLogger.cerr.threshold = 'INFO'
process.MessageLogger.categories.append('Demo')
process.MessageLogger.cerr.INFO = cms.untracked.PSet(
    limit = cms.untracked.int32(-1)
)
process.load('RecoJets.JetProducers.QGTagger_cfi')
process.QGTagger.srcJets          = cms.InputTag('reco::PFJetCollection')    # Could be reco::PFJetCollection or pat::JetCollection (both AOD and miniAOD)
process.QGTagger.jetsLabel        = cms.string('QGL_AK4PFchs')        # Other options: see https://twiki.cern.ch/twiki/bin/viewauth/CMS/QGDataBaseVersion

process.options   = cms.untracked.PSet( 
                                        SkipEvent = cms.untracked.vstring('ProductNotFound')
                                        ) 


process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )


from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, '74X_dataRun2_Prompt_v2', '')
#process.GlobalTag.globaltag = 'GR_R_44_V12::All'
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data', '')

#######################
# Quark gluon tagging #
#   (added manually)  #
#######################

qgDatabaseVersion = 'v1' # check https://twiki.cern.ch/twiki/bin/viewauth/CMS/QGDataBaseVersion

from CondCore.DBCommon.CondDBSetup_cfi import *
QGPoolDBESSource = cms.ESSource("PoolDBESSource",
      CondDBSetup,
      toGet = cms.VPSet(),
      connect = cms.string('frontier://FrontierProd/CMS_COND_PAT_000'),
)

for type in ['AK4PF','AK4PFchs_antib']:
  QGPoolDBESSource.toGet.extend(cms.VPSet(cms.PSet(
    record = cms.string('QGLikelihoodRcd'),
    tag    = cms.string('QGLikelihoodObject_'+qgDatabaseVersion+'_'+type),
    label  = cms.untracked.string('QGL_'+type)
  )))

###########
#  Input  #
###########

  
process.source = cms.Source("PoolSource",
                                # replace 'myfile.root' with the source file you want to use
                                fileNames = cms.untracked.vstring(
            #'file:/afs/cern.ch/cms/Tutorials/TWIKI_DATA/TTJets_8TeV_53X.root'
            'root://cmsxrootd.fnal.gov///store/mc/RunIISpring15DR74/MinBias_TuneCUETP8M1_13TeV-pythia8/GEN-SIM-RECODEBUG/NoPURealisticRecodebug_741_p1_mcRun2_Realistic_50ns_v0-v1/00000/06967C3F-4A53-E511-91B8-0025904C7DF6.root'
                ),
                            )

############
#  Output  #
############
							
process.TFileService = cms.Service("TFileService",
                                       fileName = cms.string('histodemo.root')
                                   )							
							
							
process.demo = cms.EDAnalyzer('QGAnalyzer',
jetsInputTag = cms.InputTag("ak4PFJets") #added from http://uaf-2.t2.ucsd.edu/~ibloch/CMS2/NtupleMaker/python/jetMaker_cfi.py through comparison. It doesn't work though, so that's an issue.
)


process.p = cms.Path(process.demo)
