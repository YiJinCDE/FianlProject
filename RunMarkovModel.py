import InputData as D
import ParameterClasses as P
import MarkovModelClasses as Cls
import Support as Support
import SimPy.FigureSupport as Fig
import SimPy.SamplePathClasses as Path

# selected therapy
therapy_none = P.Therapies.NO

# create a cohort
myCohort_0 = Cls.Cohort(id=0,
                      pop_size=D.POP_SIZE,
                      parameters=P.ParametersFixed(therapy=therapy_none))

# simulate the cohort over the specified time steps
myCohort_0.simulate(sim_length=D.SIM_LENGTH)

# plot the sample path (survival curve)
Path.graph_sample_path(
    sample_path=myCohort_0.cohortOutcomes.nLivingPatients,
    title='Survival Curvel for No Therapy',
    x_label='Time-Step (Year)',
    y_label='Number Survived')

# plot the histogram of survival times
Fig.graph_histogram(
    data=myCohort_0.cohortOutcomes.survivalTimes,
    title='Histogram of Patient Survival Times for No Therapy',
    x_label='Survival Time (Year)',
    y_label='Count',
    bin_width=1)

# print the outcomes of this simulated cohort
Support.print_outcomes(sim_outcomes=myCohort_0.cohortOutcomes,therapy_name=therapy_none)


therapy_asp = P.Therapies.ASP

# create a cohort
myCohort_1 = Cls.Cohort(id=1,
                      pop_size=D.POP_SIZE,
                      parameters=P.ParametersFixed(therapy=therapy_asp))

# simulate the cohort over the specified time steps
myCohort_1.simulate(sim_length=D.SIM_LENGTH)

# plot the sample path (survival curve)
Path.graph_sample_path(
    sample_path=myCohort_1.cohortOutcomes.nLivingPatients,
    title='Survival Curve for Aspirin Therapy',
    x_label='Time-Step (Year)',
    y_label='Number Survived')

# plot the histogram of survival times
Fig.graph_histogram(
    data=myCohort_1.cohortOutcomes.survivalTimes,
    title='Histogram of Patient Survival Time for Aspirin Therapy',
    x_label='Survival Time (Year)',
    y_label='Count',
    bin_width=1)

# print the outcomes of this simulated cohort
Support.print_outcomes(sim_outcomes=myCohort_1.cohortOutcomes,therapy_name=therapy_asp)

