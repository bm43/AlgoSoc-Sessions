# Setup Helper Functions


def setup_agent_0(backtest):
    from agent_0_echo import EchoAgent
    agent = EchoAgent(backtest=backtest)
    agent.run()


def setup_agent_1(backtest, verbose):
    from agent_1_simple_macd import SimpleMACDAgent
    agent = SimpleMACDAgent(fast_length=120, slow_length=250,
                            backtest=backtest, verbose=verbose)
    agent.run()


def setup_agent_2(backtest, verbose):
    from agent_2_simple_risk_managed_macd import SimpleRiskMACDAgent
    agent = SimpleRiskMACDAgent(stop_loss_scaling=2.0,
                                take_profit_scaling=1.5,
                                fast_length=30, slow_length=120,
                                backtest=backtest, verbose=verbose)
    agent.run()


def setup_agent_3(backtest, verbose):
    from agent_3_ret_bound_risk_macd import RetBoundRiskMACDAgent
    agent = RetBoundRiskMACDAgent(ret_length=99,
                                  ret_upper_scaling_factor=5,
                                  ret_lower_scaling_factor=3.1,
                                  fast_length=120, slow_length=243,
                                  backtest=backtest, verbose=verbose)
    agent.run()


def setup_agent_4(backtest, verbose):
    from agent_4_decision_tree import DecisionTreeAgent
    agent = DecisionTreeAgent(horizon=100, max_depth=4,
                              fast_length=110, slow_length=400,
                              backtest=backtest, verbose=verbose)
    agent.run()


# Test Functions

test_file = 'data/backtest_GBPUSD_tiny.csv'


def test_agent_0(backtest=test_file):
    setup_agent_0(backtest=backtest)


def test_agent_1(backtest=test_file):
    setup_agent_1(backtest=backtest, verbose=False)
    setup_agent_1(backtest=backtest, verbose=True)


def test_agent_2(backtest=test_file):
    setup_agent_2(backtest=backtest, verbose=False)
    setup_agent_2(backtest=backtest, verbose=True)


def test_agent_3(backtest=test_file):
    setup_agent_3(backtest=backtest, verbose=False)
    setup_agent_3(backtest=backtest, verbose=True)


def test_agent_4(backtest=test_file):
    setup_agent_4(backtest=backtest, verbose=False)
    setup_agent_4(backtest=backtest, verbose=True)


def test_param_optimisation_agent_1(backtest=test_file):
    from param_optimisation_tests import expicit_optimise_with_agent_1
    expicit_optimise_with_agent_1(backtest=backtest, simple=True)
    from param_optimisation_tests import random_optimise_with_agent_1
    random_optimise_with_agent_1(backtest=backtest)


def test_param_optimisation_agent_2(backtest=test_file):
    from param_optimisation_tests import expicit_optimise_with_agent_2
    expicit_optimise_with_agent_2(backtest=backtest, simple=True)
    from param_optimisation_tests import random_optimise_with_agent_2
    random_optimise_with_agent_2(backtest=backtest)


def test_param_optimisation_agent_3(backtest=test_file):
    from param_optimisation_tests import expicit_optimise_with_agent_3
    expicit_optimise_with_agent_3(backtest=backtest, simple=True)
    from param_optimisation_tests import random_optimise_with_agent_3
    random_optimise_with_agent_3(backtest=backtest)


def test_param_optimisation_agent_4(backtest=test_file):
    from param_optimisation_tests import expicit_optimise_with_agent_4
    expicit_optimise_with_agent_4(backtest=backtest, simple=True)
    from param_optimisation_tests import random_optimise_with_agent_4
    random_optimise_with_agent_4(backtest=backtest)


def test_param_optimisation_verbose_sort(backtest=test_file):
    from param_optimisation_tests import expicit_optimise_with_agent_1
    expicit_optimise_with_agent_1(backtest=backtest, simple=True,
                                  sort=True, verbose=False)
    expicit_optimise_with_agent_1(backtest=backtest, simple=True,
                                  sort=False, verbose=True)
    from param_optimisation_tests import random_optimise_with_agent_2
    random_optimise_with_agent_2(backtest=backtest, sort=True, verbose=False)
    random_optimise_with_agent_2(backtest=backtest, sort=False, verbose=True)