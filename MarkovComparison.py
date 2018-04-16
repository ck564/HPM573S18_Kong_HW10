import ParameterClasses as P
import MarkovModel as MarkovCls
import SupportMarkovModel as SupportMarkov


# create and cohort without drug
cohort_nodrug = MarkovCls.Cohort(
    id=0,
    therapy=P.Therapies.NONE)

simOutputs_nodrug = cohort_nodrug.simulate()


# create and simulate cohort with drug
cohort_drugtx = MarkovCls.Cohort(
    id=1,
    therapy=P.Therapies.ANTICOAG)

simOutputs_drugtx = cohort_drugtx.simulate()


# report CEA results
SupportMarkov.report_CEA_CBA(simOutputs_nodrug, simOutputs_drugtx)

