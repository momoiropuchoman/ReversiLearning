from Common import Common
from MassType import MassType
from QTable import QTable
from Util import Util

import numpy
from abc import ABC, abstractmethod
from enum import Enum, auto
import random

class StrategyType(Enum):
    EVALUATION = 0
    DECREASING_OPP_EVALUATION = 1
    BALANCE_EVALUATION = 2
    MAX_REVERSIBLE = 3
    FORECAST = 4
    Q_LEARNING = 5


# 駒配置アルゴリズムのインタフェース
class Strategy(ABC):
    def __init__(self, mass_type, strategy_type):
        self.mass_type = mass_type
        self.type = strategy_type

    @abstractmethod
    def put(self, board):
        pass



# 駒配置アルゴリズム
# 評価値マップを使い、評価値が高いところに置く
class EvaluationStrategy(Strategy):

    def __init__(self, mass_type):
        super().__init__(mass_type, StrategyType.EVALUATION)
        self.evaluation = [[5, 1, 4, 4, 4, 4, 1, 5],
                           [1, 1, 2, 2, 2, 2, 1, 1],
                           [4, 2, 3, 3, 3, 3, 2, 4],
                           [4, 2, 3, 0, 0, 3, 2, 4],
                           [4, 2, 3, 0, 0, 3, 2, 4],
                           [4, 2, 3, 3, 3, 3, 2, 4],
                           [1, 1, 2, 2, 2, 2, 1, 1],
                           [5, 1, 4, 4, 4, 4, 1, 5]]

    def put(self, mass_list):

        max_value = 0
        x = 0
        y = 0
        for i in range(Common.MASS_NUM):
            for j in range(Common.MASS_NUM):
                if Util.can_put(mass_list, i, j, self.mass_type):
                    if self.evaluation[i][j] > max_value:
                        max_value = self.evaluation[i][j]
                        x = i
                        y = j

        print(str(self.type) + ": " + str(x) + " " + str(y))
        return x, y

# 駒配置アルゴリズム
# 置いた結果、相手が置けるマスの最大評価値が最も低くなるように置く
class DecreasingOppEvaluation(Strategy):

    def __init__(self, mass_type):
        super().__init__(mass_type, StrategyType.DECREASING_OPP_EVALUATION)
        self.evaluation = [[5, 1, 4, 4, 4, 4, 1, 5],
                           [1, 1, 2, 2, 2, 2, 1, 1],
                           [4, 2, 3, 3, 3, 3, 2, 4],
                           [4, 2, 3, 0, 0, 3, 2, 4],
                           [4, 2, 3, 0, 0, 3, 2, 4],
                           [4, 2, 3, 3, 3, 3, 2, 4],
                           [1, 1, 2, 2, 2, 2, 1, 1],
                           [5, 1, 4, 4, 4, 4, 1, 5]]


    def put(self, mass_list):
        min_max_value = 5
        x = 0
        y = 0
        mass_list_origin = Util.copy_mass_list(mass_list)
        opp_mass_type = Util.get_opp_type(self.mass_type)

        for i in range(Common.MASS_NUM):
            for j in range(Common.MASS_NUM):
                if Util.can_put(mass_list, i, j, self.mass_type):
                    new_mass_list = Util.copy_mass_list(mass_list)
                    max_value_this_time = 0

                    # 配置してひっくり返す
                    new_mass_list[i][j] = self.mass_type
                    new_mass_list = Util.reverse(new_mass_list, i, j, self.mass_type)

                    for s in range(Common.MASS_NUM):
                        for t in range(Common.MASS_NUM):
                            if Util.can_put(new_mass_list, s, t, opp_mass_type):
                                if max_value_this_time < self.evaluation[s][t]:
                                    max_value_this_time = self.evaluation[s][t]

                    if max_value_this_time <= min_max_value:
                        min_max_value = max_value_this_time
                        x = i
                        y = j

        print(str(self.type) + ": " + str(x) + " " + str(y))
        return x, y


# 駒配置アルゴリズム
# 自分が置くときの評価値から、自分が置いた結果相手が置けるマスの評価値を差し引きする
class BalanceEvaluation(Strategy):

    def __init__(self, mass_type):
        super().__init__(mass_type, StrategyType.BALANCE_EVALUATION)
        self.evaluation = [[5, 1, 4, 4, 4, 4, 1, 5],
                           [1, 1, 2, 2, 2, 2, 1, 1],
                           [4, 2, 3, 3, 3, 3, 2, 4],
                           [4, 2, 3, 0, 0, 3, 2, 4],
                           [4, 2, 3, 0, 0, 3, 2, 4],
                           [4, 2, 3, 3, 3, 3, 2, 4],
                           [1, 1, 2, 2, 2, 2, 1, 1],
                           [5, 1, 4, 4, 4, 4, 1, 5]]

    def put(self, mass_list):
        max_balance_value = -100
        x = 0
        y = 0
        mass_list_origin = Util.copy_mass_list(mass_list)
        opp_mass_type = Util.get_opp_type(self.mass_type)

        for i in range(Common.MASS_NUM):
            for j in range(Common.MASS_NUM):
                if Util.can_put(mass_list, i, j, self.mass_type):
                    new_mass_list = Util.copy_mass_list(mass_list)
                    max_value_this_time = 0

                    # 配置してひっくり返す
                    new_mass_list[i][j] = self.mass_type
                    new_mass_list = Util.reverse(new_mass_list, i, j, self.mass_type)

                    for s in range(Common.MASS_NUM):
                        for t in range(Common.MASS_NUM):
                            if Util.can_put(new_mass_list, s, t, opp_mass_type):
                                if max_value_this_time < self.evaluation[s][t]:
                                    max_value_this_time = self.evaluation[s][t]

                    # 自分が置くときの評価値と、次相手が置くときの評価値を差し引き
                    balance_value = self.evaluation[i][j] - max_value_this_time

                    if max_balance_value < balance_value:
                        max_balance_value = balance_value
                        x = i
                        y = j

        print(str(self.type) + ": " + str(x) + " " + str(y))
        return x, y

# 駒配置アルゴリズム
# 数手先まで読んで駒の数が多くなるように置く
class Forecast(Strategy):

    def __init__(self, mass_type):
        super().__init__(mass_type, StrategyType.FORECAST)
        self.evaluation = [[5, 1, 4, 4, 4, 4, 1, 5],
                           [1, 1, 2, 2, 2, 2, 1, 1],
                           [4, 2, 3, 3, 3, 3, 2, 4],
                           [4, 2, 3, 0, 0, 3, 2, 4],
                           [4, 2, 3, 0, 0, 3, 2, 4],
                           [4, 2, 3, 3, 3, 3, 2, 4],
                           [1, 1, 2, 2, 2, 2, 1, 1],
                           [5, 1, 4, 4, 4, 4, 1, 5]]

    def put(self, mass_list):
        max_balance_value = -100
        x = 0
        y = 0

        opp_mass_type = Util.get_opp_type(self.mass_type)

        max_piece_num = 0
        FORECAST_TURN = 3

        for i in range(Common.MASS_NUM):
            for j in range(Common.MASS_NUM):
                if Util.can_put(mass_list, i, j, self.mass_type):
                    mass_list_process = Util.copy_mass_list(mass_list)

                    # まず今回の探索位置におく
                    mass_list_process = Util.reverse(mass_list_process, i, j, self.mass_type)

                    # 指定ターン数先まで繰り返す
                    for count in range(FORECAST_TURN):

                        # 敵→自分→敵→自分の順番
                        if count % 2 == 0:
                            turn_mass_type = opp_mass_type
                        else:
                            turn_mass_type = self.mass_type

                        # 一番多くひっくり返せるところに置く
                        this_x, this_y = self.put_most_piece(mass_list_process, turn_mass_type)
                        if this_x != 0 and this_y != 0:
                            mass_list_process = Util.reverse(mass_list_process, this_x, this_y, turn_mass_type)

                        # どちらも置けなくなったら強制終了
                        if Util.can_put_somewhere(mass_list_process, self.mass_type) or Util.can_put_somewhere(mass_list_process, opp_mass_type):
                            break

                    # 数ターン後の自分の枚数
                    final_piece_num = Util.get_piece_num(mass_list_process, self.mass_type)

                    # 現時点の最大値より大きければ更新
                    if max_piece_num < final_piece_num:
                        max_piece_num = final_piece_num
                        x = i
                        y = j


        return x, y



    def put_most_piece(self, mass_list, mass_type):
        reversible_max = 0
        x = 0
        y = 0

        for i in range(Common.MASS_NUM):
            for j in range(Common.MASS_NUM):
                if Util.can_put(mass_list, i, j, mass_type):

                    reversible_num = Util.get_reversible_num(mass_list, i, j, mass_type)
                    if reversible_max < reversible_num:
                        reversible_max = reversible_num
                        x = i
                        y = j

        return x, y


# 駒配置アルゴリズム
#
class MaxReversible(Strategy):

    def __init__(self, mass_type):
        super().__init__(mass_type, StrategyType.MAX_REVERSIBLE)

    def put(self, mass_list):

        reversible_max = 0
        x = 0
        y = 0

        for i in range(Common.MASS_NUM):
            for j in range(Common.MASS_NUM):
                if Util.can_put(mass_list, i, j, self.mass_type):

                    reversible_num = Util.get_reversible_num(mass_list, i, j, self.mass_type)
                    if reversible_max < reversible_num:
                        reversible_max = reversible_num
                        x = i
                        y = j

        return x, y


# 駒配置アルゴリズム
#
class QLearning(Strategy):

    def __init__(self, mass_type, q_table):
        super().__init__(mass_type, StrategyType.Q_LEARNING)

        self.q_table = q_table
        self.q_table = QTable() #後で消す

        self.strategies = []
        self.strategies.append(EvaluationStrategy(mass_type))
        self.strategies.append(DecreasingOppEvaluation(mass_type))
        self.strategies.append(BalanceEvaluation(mass_type))
        self.strategies.append(MaxReversible(mass_type))
        self.strategies.append(Forecast(mass_type))

        self.latest_strategy = 0

    def set_q_table(self, q_table):
        self.q_table = q_table

    def get_latest_strategy(self):
        return self.latest_strategy

    def put(self, mass_list):

        black_num = Util.get_piece_num(mass_list, MassType.BLACK)
        white_num = Util.get_piece_num(mass_list, MassType.WHITE)
        total_piece = black_num + white_num

        if black_num == white_num:
            lead_index = 3
        elif black_num > white_num:
            if self.mass_type == MassType.BLACK:
                lead_index = 1
            else:
                lead_index = 2
        elif black_num < white_num:
            if self.mass_type == MassType.BLACK:
                lead_index = 2
            else:
                lead_index = 1

        # 今回の状況(situation)を確定
        q_index = total_piece * lead_index

        max_index_list = []

        # 今回のIndexの戦略報酬一覧を取り出す
        strategy_rewards = self.q_table.table[q_index, :]

        # 今回の戦略報酬の中から最も高い報酬を求める
        max_reward = numpy.max(strategy_rewards)

        # 最も高い報酬を持つ戦略をリストにする
        for i in range(len(strategy_rewards)):
            if strategy_rewards[i] == max_reward:
                max_index_list.append(i)
        print('max reward strategies: ' + str(max_index_list))

        # 最も高い報酬を持つ戦略が複数あれば、ランダムで1つ選ぶ
        random_index = random.randint(0, len(max_index_list))
        decided_strategy = max_index_list[random_index]
        print('selected strategy: ' + str(decided_strategy))

        # 決定した戦略を使って駒を置く場所を決める
        x, y = self.strategies[decided_strategy].put(mass_list)

        # 後で取得するようにセットしておく
        self.latest_strategy = decided_strategy

        return x, y