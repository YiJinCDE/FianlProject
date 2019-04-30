import matplotlib.pyplot as plt
import InputData as D
import SimPy.EconEvalClasses as Econ
import SimPy.FigureSupport as Figs
import SimPy.SamplePathClasses as PathCls
import SimPy.StatisticalClasses as Stat


def print_outcomes(multi_cohort_outcomes, therapy_name):
    """ prints the outcomes of a simulated cohort
    :param multi_cohort_outcomes: outcomes of a simulated multi-cohort
    :param therapy_name: the name of the selected therapy
    """
    # mean and prediction interval of patient survival time
    survival_mean_PI_text = multi_cohort_outcomes.statMeanSurvivalTime\
        .get_formatted_mean_and_interval(interval_type='p',
                                         alpha=D.ALPHA,
                                         deci=2)

    # mean and prediction interval text of discounted total cost
    cost_mean_PI_text = multi_cohort_outcomes.statMeanCost\
        .get_formatted_mean_and_interval(interval_type='p',
                                         alpha=D.ALPHA,
                                         deci=0,
                                         form=',')

    # mean and prediction interval text of discounted total QALY
    utility_mean_PI_text = multi_cohort_outcomes.statMeanQALY\
        .get_formatted_mean_and_interval(interval_type='p',
                                         alpha=D.ALPHA,
                                         deci=2)

    # print outcomes
    print(therapy_name)
    print("  Estimate of mean survival time and {:.{prec}%} uncertainty interval:".format(1 - D.ALPHA, prec=0),
          survival_mean_PI_text)
    print("  Estimate of mean discounted cost and {:.{prec}%} uncertainty interval:".format(1 - D.ALPHA, prec=0),
          cost_mean_PI_text)
    print("  Estimate of mean discounted utility and {:.{prec}%} uncertainty interval:".format(1 - D.ALPHA, prec=0),
          utility_mean_PI_text)
    print("")


def plot_survival_curves_and_histograms(multi_cohort_outcomes_mono, multi_cohort_outcomes_combo):
    """ plot the survival curves and the histograms of survival times
    :param multi_cohort_outcomes_mono: outcomes of a multi-cohort simulated under mono therapy
    :param multi_cohort_outcomes_combo: outcomes of a multi-cohort simulated under combination therapy
    """

    # get survival curves of both treatments
    sets_of_survival_curves = [
        multi_cohort_outcomes_mono.survivalCurves,
        multi_cohort_outcomes_combo.survivalCurves
    ]

    # graph survival curve
    PathCls.graph_sets_of_sample_paths(
        sets_of_sample_paths=sets_of_survival_curves,
        title='Survival Curves',
        x_label='Simulation Time Step (year)',
        y_label='Number of Patients Alive',
        legends=['Mono Therapy', 'Combination Therapy'],
        transparency=0.4,
        color_codes=['green', 'blue']
    )

    # histograms of survival times
    set_of_survival_times = [
        multi_cohort_outcomes_mono.meanSurvivalTimes,
        multi_cohort_outcomes_combo.meanSurvivalTimes
    ]

    # graph histograms
    Figs.graph_histograms(
        data_sets=set_of_survival_times,
        title='Histograms of Average Patient Survival Time',
        x_label='Survival Time (year)',
        y_label='Counts',
        bin_width=0.25,
        x_range=[5.25, 17.75],
        legends=['No Therapy', 'Aspirin Therapy'],
        color_codes=['green', 'blue'],
        transparency=0.5
    )


def print_comparative_outcomes(multi_cohort_outcomes_no, multi_cohort_outcomes_asp):
    """ prints average increase in survival time, discounted cost, and discounted utility
    under combination therapy compared to mono therapy
    :param multi_cohort_outcomes_mono: outcomes of a multi-cohort simulated under mono therapy
    :param multi_cohort_outcomes_combo: outcomes of a multi-cohort simulated under combination therapy
    """

    # increase in mean survival time under combination therapy with respect to mono therapy
    increase_mean_survival_time = Stat.DifferenceStatPaired(
        name='Increase in mean survival time',
        x=multi_cohort_outcomes_asp.meanSurvivalTimes,
        y_ref=multi_cohort_outcomes_no.meanSurvivalTimes)

    # estimate and PI
    estimate_PI = increase_mean_survival_time.get_formatted_mean_and_interval(interval_type='p',
                                                                              alpha=D.ALPHA,
                                                                              deci=2)
    print("Increase in mean survival time and {:.{prec}%} uncertainty interval:"
          .format(1 - D.ALPHA, prec=0),
          estimate_PI)

    # increase in mean discounted cost under combination therapy with respect to mono therapy
    increase_mean_discounted_cost = Stat.DifferenceStatPaired(
        name='Increase in mean discounted cost',
        x=multi_cohort_outcomes_asp.meanCosts,
        y_ref=multi_cohort_outcomes_no.meanCosts)

    # estimate and PI
    estimate_PI = increase_mean_discounted_cost.get_formatted_mean_and_interval(interval_type='p',
                                                                                alpha=D.ALPHA,
                                                                                deci=2,
                                                                                form=',')
    print("Increase in mean discounted cost and {:.{prec}%} uncertainty interval:"
          .format(1 - D.ALPHA, prec=0),
          estimate_PI)

    # increase in mean discounted QALY under combination therapy with respect to mono therapy
    increase_mean_discounted_qaly = Stat.DifferenceStatPaired(
        name='Increase in mean discounted QALY',
        x=multi_cohort_outcomes_asp.meanQALYs,
        y_ref=multi_cohort_outcomes_no.meanQALYs)

    # estimate and PI
    estimate_PI = increase_mean_discounted_qaly.get_formatted_mean_and_interval(interval_type='p',
                                                                                alpha=D.ALPHA,
                                                                                deci=2)
    print("Increase in mean discounted utility and {:.{prec}%} uncertainty interval:"
          .format(1 - D.ALPHA, prec=0),
          estimate_PI)


def report_CEA_CBA(multi_cohort_outcomes_no, multi_cohort_outcomes_asp):

    # define two strategies
    no_therapy_strategy = Econ.Strategy(
        name='Mono Therapy',
        cost_obs=multi_cohort_outcomes_no.meanCosts,
        effect_obs=multi_cohort_outcomes_asp.meanQALYs,
        color='green'
    )
    asp_therapy_strategy = Econ.Strategy(
        name='Combination Therapy',
        cost_obs=multi_cohort_outcomes_asp.meanCosts,
        effect_obs=multi_cohort_outcomes_no.meanQALYs,
        color='blue'
    )

    # do CEA
    CEA = Econ.CEA(
        strategies=[no_therapy_strategy, asp_therapy_strategy],
        if_paired=True
    )

    # show the cost-effectiveness plane
    show_ce_figure(CEA=CEA)

    # report the CE table
    CEA.build_CE_table(
        interval_type='p',  # prediction intervals
        alpha=D.ALPHA,
        cost_digits=0,
        effect_digits=2,
        icer_digits=2)

    # CBA
    NBA = Econ.CBA(
        strategies=[no_therapy_strategy, asp_therapy_strategy],
        if_paired=True
    )
    # show the net monetary benefit figure
    NBA.graph_incremental_NMBs(
        min_wtp=0,
        max_wtp=50000,
        title='Cost-Benefit Analysis',
        x_label='Willingness-To-Pay for One Additional QALY ($)',
        y_label='Incremental Net Monetary Benefit ($)',
        interval_type='p',
        show_legend=True,
        figure_size=(6, 5)
    )


def show_ce_figure(CEA):

    # create a cost-effectiveness plot
    plt.figure(figsize=(5, 5))

    # find the frontier (x, y)'s
    frontier_utilities = []
    frontier_costs = []
    for s in CEA.get_shifted_strategies_on_frontier():
        frontier_utilities.append(s.aveEffect)
        frontier_costs.append(s.aveCost)

    # draw the frontier line
    plt.plot(frontier_utilities, frontier_costs,
             c='k',  # color
             alpha=0.6,  # transparency
             linewidth=2,  # line width
             label="Frontier")  # label to show in the legend

    # add the strategies
    for s in CEA.get_shifted_strategies():
        # add the center of the cloud
        plt.scatter(s.aveEffect, s.aveCost,
                    c=s.color,      # color
                    alpha=1,        # transparency
                    marker='o',     # markers
                    s=75,          # marker size
                    label=s.name    # name to show in the legend
                    )
        # add the cloud
        plt.scatter(s.effectObs, s.costObs,
                    c=s.color,  # color of dots
                    alpha=0.15,  # transparency of dots
                    s=25,  # size of dots
                    )

    plt.legend()        # show the legend
    plt.axhline(y=0, c='k', linewidth=0.5)  # horizontal line at y = 0
    plt.axvline(x=0, c='k', linewidth=0.5)  # vertical line at x = 0
    plt.xlim([-2, 8])              # x-axis range
    plt.ylim([-20000, 120000])     # y-axis range
    plt.title('Cost-Effectiveness Analysis')
    plt.xlabel('Additional discounted QALY')
    plt.ylabel('Additional discounted cost')
    plt.show()

