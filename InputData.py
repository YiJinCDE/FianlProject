

# simulation settings
POP_SIZE = 2000         # cohort population size
SIM_LENGTH = 50    # length of simulation (years)
ALPHA = 0.05        # significance level for calculating confidence intervals
DISCOUNT = 0.03
ANNUAL_PROB_BACKGROUND_MORT = 0.1135

PROB_MATRIX=[
    [0.7694132,0.0004,0,0.0001868,0.23],
    [0,0,0.533,0.467,0],
    [0.0004,0.7694132,0.0001868,0.23],
    [0,0,0,1,0],
    [0,0,0,0,1]
]

RATE_MATRIX_0=[
[0,0.0001738,0,0.00008113,0.1135],
    [0,0,52,0,0],
    [0,0.0001738,0,0.00008113,0.1135],
    [0,0,0,0,0],
    [0,0,0,0,0]
]

RATE_MATRIX_1=[
[0,0.0003476,0,0.000162283,0.1135],
    [0,0,52,0,0],
    [0,0.0003476,0,0.000162283,0.1135],
    [0,0,0,0,0],
    [0,0,0,0,0]
]


# annual cost of each health state
ANNUAL_STATE_COST_NO = [
    4700,
    47315,
    4700,
    0,
    0
    ]

ANNUAL_STATE_COST_ASP = [
    4714,
    47315,
    4714,
    0,
    0
]

# annual health utility of each health state
ANNUAL_STATE_UTILITY_1 = [
    0.998,
    0.39,
    0.75848,
    0,
    0
    ]

ANNUAL_STATE_UTILITY_0 = [
    1,
    0.39,
    0.76,
    0,
    0
    ]

COST_ASP=14
COST_NO=0

TREATMENT_RR = 2
