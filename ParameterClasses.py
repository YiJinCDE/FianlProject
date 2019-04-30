from enum import Enum
import InputData as Data


class HealthStates(Enum):
    AFI = 0
    SDH = 1
    PS = 2
    SDH_DEATH = 3
    NATURAL_DEATH = 4


class Therapies(Enum):
    NO = 0
    ASP = 1


class ParametersFixed:
    def __init__(self, therapy):

        # selected therapy
        self.therapy = therapy

        # initial health state
        self.initialHealthState = HealthStates.AFI

        # annual treatment cost
        if self.therapy == Therapies.NO:
            self.annualTreatmentCost = Data.COST_NO
        else:
            self.annualTreatmentCost = Data.COST_ASP

        # transition probability matrix of the selected therapy
        self.rateMatrix = []

        # calculate transition probabilities between health states
        if self.therapy == Therapies.NO:
            # calculate transition probability matrix for no therapy
            self.rateMatrix = Data.RATE_MATRIX_0
            self.annualStateCosts = Data.ANNUAL_STATE_COST_NO
            self.annualStateUtilities = Data.ANNUAL_STATE_UTILITY_0

        elif self.therapy == Therapies.ASP:
            # calculate transition probability matrix for the combination therapy
            self.rateMatrix = Data.RATE_MATRIX_1
            self.annualStateCosts = Data.ANNUAL_STATE_COST_ASP
            self.annualStateUtilities = Data.ANNUAL_STATE_UTILITY_1


        # discount rate
        self.discountRate = Data.DISCOUNT




