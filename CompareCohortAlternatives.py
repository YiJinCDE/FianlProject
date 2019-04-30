import InputData as D
import MultiCohortClasses as Cls
import MultiCohortSupport as Support
import ProbilisticParamClasses as P

N_COHORTS = 25  # number of cohorts

# create a multi-cohort to simulate under mono therapy
multiCohortNo = Cls.MultiCohort(
    ids=range(N_COHORTS),
    pop_size=D.POP_SIZE,
    therapy=P.Therapies.NO
)

multiCohortNo.simulate(sim_length=D.SIM_LENGTH)

# create a multi-cohort to simulate under combo therapy
multiCohortAsp = Cls.MultiCohort(
    ids=range(N_COHORTS, 2*N_COHORTS),
    pop_size=D.POP_SIZE,
    therapy=P.Therapies.ASP
)

multiCohortAsp.simulate(sim_length=D.SIM_LENGTH)

# print the estimates for the mean survival time and mean time to AIDS
Support.print_outcomes(multi_cohort_outcomes=multiCohortNo.multiCohortOutcomes,
                       therapy_name=P.Therapies.NO)
Support.print_outcomes(multi_cohort_outcomes=multiCohortAsp.multiCohortOutcomes,
                       therapy_name=P.Therapies.ASP)

# draw survival curves and histograms
Support.plot_survival_curves_and_histograms(multi_cohort_outcomes_mono=multiCohortNo.multiCohortOutcomes,
                                            multi_cohort_outcomes_combo=multiCohortAsp.multiCohortOutcomes)

# print comparative outcomes
Support.print_comparative_outcomes(multi_cohort_outcomes_no=multiCohortNo.multiCohortOutcomes,
                                   multi_cohort_outcomes_asp=multiCohortAsp.multiCohortOutcomes)

# report the CEA results
Support.report_CEA_CBA(multi_cohort_outcomes_no=multiCohortNo.multiCohortOutcomes,
                       multi_cohort_outcomes_asp=multiCohortAsp.multiCohortOutcomes)