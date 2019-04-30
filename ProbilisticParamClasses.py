from ParameterClasses import *  # import everything from the ParameterClass module
import InputData as Data
import SimPy.RandomVariantGenerators as RVGs
import SimPy.FittingProbDist_MM as MM
import math
import scipy.stats as stat


class Parameters:

    def __init__(self, therapy):

        self.therapy = therapy              # selected therapy
        self.initialHealthState = HealthStates.AFI     # initial health state
        self.annualTreatmentCost = 0        # annual treatment cost
        self.rateMatrix = []                # transition probability matrix of the selected therapy
        self.annualStateCosts = []          # annual state costs
        self.annualStateUtilities = []      # annual state utilities
        self.discountRate = Data.DISCOUNT   # discount rate


class ParameterGenerator:

    def __init__(self, therapy):

        self.therapy = therapy
        self.probMatrixRVG = []     # list of dirichlet distributions for transition probabilities
        self.lnRelativeRiskRVG = None  # normal distribution for the natural log of the treatment relative risk
        self.annualStateCostRVG = []  # list of gamma distributions for the annual cost of states
        self.annualStateUtilityRVG = []  # list of beta distributions for the annual utility of states

        # create Dirichlet distributions for transition probabilities
        j = 0
        for prob in Data.PROB_MATRIX:
            self.probMatrixRVG.append(RVGs.Dirichlet(a=prob[j:]))
            j += 1

        # treatment relative risk
        rr_ci = [1.2,3]   # confidence interval of the treatment relative risk

        # find the mean and st_dev of the normal distribution assumed for ln(RR)
        # sample mean ln(RR)
        mean_ln_rr = math.log(Data.TREATMENT_RR)
        # sample standard deviation of ln(RR)
        std_ln_rr = \
            (math.log(rr_ci[1]) - math.log(rr_ci[0])) / (2 * stat.norm.ppf(1 - 0.05 / 2))
        # create a normal distribution for ln(RR)
        self.lnRelativeRiskRVG = RVGs.Normal(loc=mean_ln_rr,
                                             scale=std_ln_rr)

        # create gamma distributions for annual state cost
        for cost in Data.ANNUAL_STATE_COST_NO:

            # if cost is zero, add a constant 0, otherwise add a gamma distribution
            if cost == 0:
                self.annualStateCostRVG.append(RVGs.Constant(value=0))
            else:
                # find shape and scale of the assumed gamma distribution
                # no data available to estimate the standard deviation, so we assumed st_dev=cost / 5
                fit_output = MM.get_gamma_params(mean=cost, st_dev=cost / 5)
                # append the distribution
                self.annualStateCostRVG.append(
                    RVGs.Gamma(a=fit_output["a"],
                               loc=0,
                               scale=fit_output["scale"]))

        # create beta distributions for annual state utility
        for utility in Data.ANNUAL_STATE_UTILITY_0:
            # if utility is zero, add a constant 0, otherwise add a beta distribution
            if utility == 0:
                self.annualStateCostRVG.append(RVGs.Constant(value=0))
            else:
                # find alpha and beta of the assumed beta distribution
                # no data available to estimate the standard deviation, so we assumed st_dev=cost / 4
                fit_output = MM.get_beta_params(mean=utility, st_dev=utility / 4)
                # append the distribution
                self.annualStateUtilityRVG.append(
                    RVGs.Beta(a=fit_output["a"], b=fit_output["b"]))

    def get_new_parameters(self, rng):
        """
        :param rng: random number generator
        :return: a new parameter set
        """

        # create a parameter set
        param = Parameters(therapy=self.therapy)

        # calculate transition probabilities
        prob_matrix = []    # probability matrix without background mortality added
        # for all health states
        for s in HealthStates:

            # if the current state is death
            if s not in [HealthStates.SDH_DEATH, HealthStates.NATURAL_DEATH]:
                # create a row populated with zeroes
                prob_matrix.append([0] * (len(HealthStates)-1))
                # sample from the dirichlet distribution to find the transition probabilities between health states
                sample = self.probMatrixRVG[s.value].sample(rng)
                # fill in the transition probabilities out of this state
                for j in range(len(sample)):
                    prob_matrix[s.value][s.value + j] = sample[j]

        # sampled relative risk
        rr = math.exp(self.lnRelativeRiskRVG.sample(rng))

        # calculate transition probabilities between hiv states
        if self.therapy == Therapies.NO:
            # calculate transition probability matrix for the mono therapy
            param.rateMatrix = Data.RATE_MATRIX_0

        elif self.therapy == Therapies.ASP:
            # calculate transition probability matrix for the combination therapy
            param.rateMatrix = Data.RATE_MATRIX_1

        # sample from gamma distributions that are assumed for annual state costs
        for dist in self.annualStateCostRVG:
            param.annualStateCosts.append(dist.sample(rng))

        # sample from beta distributions that are assumed for annual state utilities
        for dist in self.annualStateUtilityRVG:
            param.annualStateUtilities.append(dist.sample(rng))

        # return the parameter set
        return param
