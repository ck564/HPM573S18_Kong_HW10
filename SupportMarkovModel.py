import InputData as Settings
import scr.FormatFunctions as F
import scr.EconEvalClasses as Econ


def print_outcomes(simOutput, therapy_name):
    """ prints the outcomes of a simulated cohort
    :param simOutput: output of a simulated cohort
    :param therapy_name: the name of the selected therapy
    """
    # mean and confidence interval text of patient survival time
    survival_mean_CI_text = F.format_estimate_interval(
        estimate=simOutput.get_sumStat_survival_times().get_mean(),
        interval=simOutput.get_sumStat_survival_times().get_t_CI(alpha=Settings.ALPHA),
        deci=2)

    # mean and confidence interval text of time to stroke
    strokes_mean_CI_text = F.format_estimate_interval(
        estimate=simOutput.get_sumStat_count_strokes().get_mean(),
        interval=simOutput.get_sumStat_count_strokes().get_t_CI(alpha=Settings.ALPHA),
        deci=2)

    # mean and confidence interval text of discounted total cost
    cost_mean_CI_text = F.format_estimate_interval(
        estimate=simOutput.get_sumStat_discounted_cost().get_mean(),
        interval=simOutput.get_sumStat_discounted_cost().get_t_CI(alpha=Settings.ALPHA),
        deci=0,
        form=F.FormatNumber.CURRENCY)

    # mean and confidence interval text of discounted total utility
    utility_mean_CI_text = F.format_estimate_interval(
        estimate=simOutput.get_sumStat_discounted_utility().get_mean(),
        interval=simOutput.get_sumStat_discounted_utility().get_t_CI(alpha=Settings.ALPHA),
        deci=2
    )

    # print outcomes
    print(therapy_name)
    print("  Estimate of mean and {:.{prec}%} confidence interval of survival time:".format(1 - Settings.ALPHA, prec=0),
          survival_mean_CI_text)
    print("  Estimate of mean and {:.{prec}%} confidence interval of time to stroke:".format(1 - Settings.ALPHA, prec=0),
          strokes_mean_CI_text)
    print("  Estimate of discounted cost and {:.{prec}%} confidence interval:".format(1 - Settings.ALPHA, prec=0),
          cost_mean_CI_text)
    print("  Estimate of discounted utility and {:.{prec}%} confidence interval:".format(1 - Settings.ALPHA, prec=0),
          utility_mean_CI_text)
    print("")


def report_CEA_CBA(simOutputs_nodrug, simOutputs_drugtx):
    """ performs cost-effectiveness and cost-benefit analysis"""

    # strategies
    strategy_no_drug = Econ.Strategy(
        name='No drug',
        cost_obs=simOutputs_nodrug.get_costs(),
        effect_obs=simOutputs_nodrug.get_utilities()
    )

    strategy_drug = Econ.Strategy(
        name='Drug Treatment',
        cost_obs=simOutputs_drugtx.get_costs(),
        effect_obs=simOutputs_drugtx.get_utilities()
    )

    # CEA
    CEA = Econ.CEA(
        strategies=[strategy_no_drug, strategy_drug],
        if_paired=False
    )

    # CE plane
    CEA.show_CE_plane(
        title='Cost Effectiveness Analysis',
        x_label='Additional Discounted Utility',
        y_label='Additional Discounted Cost',
        show_names=True,
        show_legend=True,
        show_clouds=True,
        figure_size=6,
        transparency=0.3
    )

    # report CE table
    CEA.build_CE_table(
        interval=Econ.Interval.CONFIDENCE,
        alpha=Settings.ALPHA,
        cost_digits=0,
        effect_digits=2,
        icer_digits=2
    )

    # CBA
    NBA = Econ.CBA(
        strategies=[strategy_no_drug,strategy_drug],
        if_paired=False
    )

    # net monetary benefit figure
    NBA.graph_deltaNMB_lines(
        min_wtp=0,
        max_wtp=100000,
        title='Cost Benefit Analysis',
        x_label='WTP for one addn QALY ($)',
        y_label='Incremental Net Monetary Benefit ($)',
        interval=Econ.Interval.CONFIDENCE,
        show_legend=True,
        figure_size=6
    )

