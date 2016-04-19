import FWCore.ParameterSet.Config as cms

process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")
# UNCOMMENT ME process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
# UNCOMMENT ME process.load("CondCore.DBCommon.CondDBSetup_cfi")
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
jetsInputTag = cms.InputTag("selectedLayer1Jets") #added from http://uaf-2.t2.ucsd.edu/~ibloch/CMS2/NtupleMaker/python/jetMaker_cfi.py through comparison

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

# UNCOMMENT ME from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, '74X_dataRun2_Prompt_v2', '')
#process.GlobalTag.globaltag = 'GR_R_44_V12::All'
# UNCOMMENT ME process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data', '')

process.source = cms.Source("PoolSource",
                                # replace 'myfile.root' with the source file you want to use
                                fileNames = cms.untracked.vstring(
            #'file:/afs/cern.ch/cms/Tutorials/TWIKI_DATA/TTJets_8TeV_53X.root'
            '/store/data/Run2015D/JetHT/AOD/PromptReco-v3/000/256/630/00000/A20F1D45-3C5F-E511-8351-02163E0146AE.root'
                )
                            )


process.demo = cms.EDAnalyzer('QGAnalyzer'
)
process.TFileService = cms.Service("TFileService",
                                       fileName = cms.string('histodemo.root')
                                   )

process.p = cms.Path(process.demo)
