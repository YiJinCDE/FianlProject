import InputData as D
import MultiCohortClasses as Cls
import MultiCohortSupport as Support
import ProbilisticParamClasses as P
import SimPy.FigureSupport as Fig
import SimPy.SamplePathClasses as Path

# NO THERAPY
N_COHORTS = 20              # number of cohorts
therapy_no = P.Therapies.NO  # selected therapy

# create multiple cohort
multiCohort_no = Cls.MultiCohort(
    ids=range(N_COHORTS),
    pop_size=D.POP_SIZE,
    therapy=therapy_no)

multiCohort_no.simulate(sim_length=D.SIM_LENGTH)

# plot the sample paths
Path.graph_sample_paths(
    sample_paths=multiCohort_no.multiCohortOutcomes.survivalCurves,
    title='Survival Curves',
    x_label='Time-Step (Year)',
    y_label='Number Survived',
    transparency=0.5)

# plot the histogram of average survival time
Fig.graph_histogram(
    data=multiCohort_no.multiCohortOutcomes.meanSurvivalTimes,
    title='Histogram of Mean Survival Time',
    x_label='Mean Survival Time (Year)',
    y_label='Count')

# print the outcomes of this simulated cohort
Support.print_outcomes(multi_cohort_outcomes=multiCohort_no.multiCohortOutcomes,
                       therapy_name=therapy_no)




# ASPIRIN THERAPY
N_COHORTS = 20              # number of cohorts
therapy_asp = P.Therapies.ASP  # selected therapy

# create multiple cohort
multiCohort_asp = Cls.MultiCohort(
    ids=range(N_COHORTS),
    pop_size=D.POP_SIZE,
    therapy=therapy_asp)

multiCohort_asp.simulate(sim_length=D.SIM_LENGTH)

# plot the sample paths
Path.graph_sample_paths(
    sample_paths=multiCohort_asp.multiCohortOutcomes.survivalCurves,
    title='Survival Curves',
    x_label='Time-Step (Year)',
    y_label='Number Survived',
    transparency=0.5)

# plot the histogram of average survival time
Fig.graph_histogram(
    data=multiCohort_asp.multiCohortOutcomes.meanSurvivalTimes,
    title='Histogram of Mean Survival Time',
    x_label='Mean Survival Time (Year)',
    y_label='Count')

# print the outcomes of this simulated cohort
Support.print_outcomes(multi_cohort_outcomes=multiCohort_asp.multiCohortOutcomes,
                       therapy_name=therapy_asp)

