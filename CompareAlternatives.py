import InputData as D
import ParameterClasses as P
import MarkovModelClasses as Cls
import Support as Support


# simulating no therapy
# create a cohort
cohort_none = Cls.Cohort(id=0,
                         pop_size=D.POP_SIZE,
                         parameters=P.ParametersFixed(therapy=P.Therapies.NO))
# simulate the cohort
cohort_none.simulate(sim_length=D.SIM_LENGTH)

# simulating asp therapy
# create a cohort
cohort_asp = Cls.Cohort(id=1,
                         pop_size=D.POP_SIZE,
                         parameters=P.ParametersFixed(therapy=P.Therapies.ASP))
# simulate the cohort
cohort_asp.simulate(sim_length=D.SIM_LENGTH)

# print the estimates for the mean survival time
Support.print_outcomes(sim_outcomes=cohort_none.cohortOutcomes,
                       therapy_name=P.Therapies.NO)
Support.print_outcomes(sim_outcomes=cohort_asp.cohortOutcomes,
                       therapy_name=P.Therapies.ASP)


# print comparative outcomes
Support.print_comparative_outcomes(sim_outcomes_NO=cohort_none.cohortOutcomes,
                                   sim_outcomes_ASP=cohort_asp.cohortOutcomes)

# report the CEA results
Support.report_CEA_CBA(sim_outcomes_NO=cohort_none.cohortOutcomes,
                       sim_outcomes_ASP=cohort_asp.cohortOutcomes)

Support.plot_survival_curves_and_histograms(sim_outcomes_NO=cohort_none.cohortOutcomes,
                                            sim_outcomes_ASP=cohort_asp.cohortOutcomes)
