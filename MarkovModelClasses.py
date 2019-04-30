import ParameterClasses as P
import SimPy.RandomVariantGenerators as RVGs
import SimPy.SamplePathClasses as Path
import SimPy.EconEvalClasses as Econ
import SimPy.StatisticalClasses as Stat
import SimPy.MarkovClasses as Markov


class Patient:
    def __init__(self, id, parameters):

        self.id = id
        self.rng = RVGs.RNG(seed=id)
        self.params = parameters
        self.gillespie = Markov.Gillespie(transition_rate_matrix=parameters.rateMatrix)
        self.stateMonitor = PatientStateMonitor(parameters=parameters)

    def simulate(self, sim_length):

        t = 0
        if_stop = False
        # while the patient is alive and simulation length is not yet reached
        while not if_stop:
            dt, new_state_index = self.gillespie.get_next_state(
                current_state_index=self.stateMonitor.currentState.value,
                rng=self.rng)

            if dt is None:
                if_stop = True


            elif dt + t > sim_length:
                if_stop = True
                # collect cost and health outcomes
                self.stateMonitor.costUtilityMonitor.update(time=sim_length,
                                                            current_state=self.stateMonitor.currentState,
                                                            next_state=self.stateMonitor.currentState)
            else:
                # increment time
                t += dt
                # update health state
                self.stateMonitor.update(time=t, new_state=P.HealthStates(new_state_index))


class PatientStateMonitor:
    def __init__(self, parameters):

        self.currentState = parameters.initialHealthState    # assuming everyone starts in "Well"
        self.survivalTime = None
        self.costUtilityMonitor = PatientCostUtilityMonitor(parameters=parameters)

    def update(self, time, new_state):

        if new_state == P.HealthStates.SDH_DEATH or P.HealthStates.NATURAL_DEATH:
            self.survivalTime = time


        self.costUtilityMonitor.update(time=time,
                                       current_state=self.currentState,
                                       next_state=new_state)

        self.currentState = new_state

    def get_if_alive(self):
        if self.currentState != P.HealthStates.SDH_DEATH or P.HealthStates.NATURAL_DEATH:
            return True
        else:
            return False


class PatientCostUtilityMonitor:

    def __init__(self, parameters):

        self.tLastRecorded = 0  # time when the last cost and outcomes got recorded

        # model parameters for this patient
        self.params = parameters

        # total cost and utility
        self.totalDiscountedCost = 0
        self.totalDiscountedUtility = 0

    def update(self, time, current_state, next_state):
        """ updates the discounted total cost and health utility
        :param time: simulation time
        :param current_state: current health state
        :param next_state: next health state
        """

        # cost and utility (per unit of time) during the period since the last recording until now
        cost = self.params.annualStateCosts[current_state.value] + self.params.annualTreatmentCost
        utility = self.params.annualStateUtilities[current_state.value]

        # discounted cost and utility (continuously compounded)
        discounted_cost = Econ.pv_continuous_payment(payment=cost,
                                                     discount_rate=self.params.discountRate,
                                                     discount_period=(self.tLastRecorded, time))
        discounted_utility = Econ.pv_continuous_payment(payment=utility,
                                                        discount_rate=self.params.discountRate,
                                                        discount_period=(self.tLastRecorded, time))

        # update total discounted cost and utility
        self.totalDiscountedCost += discounted_cost
        self.totalDiscountedUtility += discounted_utility

        # update the time since last recording to the current time
        self.tLastRecorded = time


class Cohort:
    def __init__(self, id, pop_size, parameters):
        self.id = id
        self.patients = []
        self.cohortOutcomes = CohortOutcomes()

        for i in range(pop_size):
            patient = Patient(id=id*pop_size + i, parameters=parameters)
            self.patients.append(patient)

    def simulate(self, sim_length):

        for patient in self.patients:
            patient.simulate(sim_length=sim_length)

        self.cohortOutcomes.extract_outcomes(self.patients)


class CohortOutcomes:
    def __init__(self):

        self.survivalTimes = []
        self.costs = []
        self.utilities = []
        self.nLivingPatients = None

        self.statSurvivalTime = None
        self.statCost = None
        self.statUtility = None
        self.statTotalSDH = None

    def extract_outcomes(self, simulated_patients):
        for patient in simulated_patients:
            if not (patient.stateMonitor.survivalTime is None):
                self.survivalTimes.append(patient.stateMonitor.survivalTime)
            self.costs.append(patient.stateMonitor.costUtilityMonitor.totalDiscountedCost)
            self.utilities.append(patient.stateMonitor.costUtilityMonitor.totalDiscountedUtility)

        self.statSurvivalTime = Stat.SummaryStat('Survival time',self.survivalTimes)
        self.statCost = Stat.SummaryStat('Discounted cost', self.costs)
        self.statUtility = Stat.SummaryStat('Discounted utility', self.utilities)

        self.nLivingPatients = Path.PrevalencePathBatchUpdate(
            name='# of living patients',
            initial_size=len(simulated_patients),
            times_of_changes=self.survivalTimes,
            increments=[-1]*len(self.survivalTimes)
        )
