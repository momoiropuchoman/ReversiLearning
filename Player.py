from Strategy import *

from enum import Enum, auto

class PlayerType(Enum):
	HUMAN = auto()
	CPU = auto()


class Player:

	def __init__(self, mass_type):
		self.mass_type = mass_type
		self.score = 2
		self.type = PlayerType.HUMAN

	def set_strategy(self, strategy_type):

		if strategy_type == StrategyType.EVALUATION:
			self.strategy = EvaluationStrategy(self.mass_type)
		elif strategy_type == StrategyType.DECREASING_OPP_EVALUATION:
			self.strategy = DecreasingOppEvaluation(self.mass_type)
		elif strategy_type == StrategyType.BALANCE_EVALUATION:
			self.strategy = BalanceEvaluation(self.mass_type)
		elif strategy_type == StrategyType.FORECAST:
			self.strategy = Forecast(self.mass_type)
		else:
			pass

	def put(self, mass_list):
		return self.strategy.put(mass_list)
