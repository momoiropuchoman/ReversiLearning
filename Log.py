from Common import Common
from MassType import MassType
from Util import Util

class Point:

	def __init__(self, mass_type, x, y):
		self.mass_type = mass_type
		self.x = x
		self.y = y

	def to_string(self):
		return str(self.mass_type) + ',' + str(self.x) + ',' + str(self.y)

class Log:

	def __init__(self, file_name):
		self.file_name = file_name
		with open(self.file_name, 'a') as file:
			file.write('---start---' + '\n')

		self.history = []

	def write(self, mass_type, x, y):
		with open(self.file_name, 'a') as file:
			file.write(str(mass_type.value) + ',' + str(x) + ',' + str(y) + '\n')

		self.history.append(Point(mass_type, x, y))

	# 指定ターン数の盤面を再現する
	def get_board_from_history(self, turn):
		mass_list = Util.get_initial_mass_list()
		for i in range(0, turn + 1):
			print(str(self.history[i].mass_type) + ', ' + str(self.history[i].x) + ', ' + str(self.history[i].y))
			mass_list[self.history[i].x][self.history[i].y] = self.history[i].mass_type
			mass_list = Util.reverse(mass_list, self.history[i].x, self.history[i].y, self.history[i].mass_type)
			print(str(Util.get_piece_num(mass_list, MassType.BLACK)))

		# 戻したターン以降のログを削除
		self.history = self.history[0:turn+1]

		return mass_list

	# 前回のプレイヤーが打つ場面の盤面を再現する
	def get_board_last_player_turn(self, human_mass_type):

		print(human_mass_type)

		# 最近の手から順番にチェックし、プレイヤーの最後のターンを検索
		for i in reversed(range(0, len(self.history)-1, 1)):
			if self.history[i].mass_type == human_mass_type:
				print('hoge')
				player_turn = i
				break

		print(player_turn)

		# 最後のプレイヤーが打つ場面の1つ前までの手から盤面を作る
		return self.get_board_from_history(player_turn - 1)






