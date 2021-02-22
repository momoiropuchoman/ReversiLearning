from Common import Common
from MassType import MassType

class Util:

	@staticmethod
	def get_initial_mass_list():
		# 盤面を初期化
		mass_list = [[MassType.EMPTY] * Common.MASS_NUM for i in range(Common.MASS_NUM)]
		for i in range(Common.MASS_NUM):
			for j in range(Common.MASS_NUM):
				mass_list[i][j] = MassType.EMPTY

		# 初期配置
		mass_list[3][3] = MassType.BLACK
		mass_list[3][4] = MassType.WHITE
		mass_list[4][3] = MassType.WHITE
		mass_list[4][4] = MassType.BLACK

		return mass_list

	@staticmethod
	def get_puttable_list(mass_list, mass_type):
		puttable_list = [[0 for i in range(Common.MASS_NUM)] for j in range(Common.MASS_NUM)]
		for i in range(Common.MASS_NUM):
			for j in range(Common.MASS_NUM):
				if Util.can_put(mass_list, i, j, mass_type):
					puttable_list[i][j] = True
				else:
					puttable_list[i][j] = False
		return puttable_list


	@staticmethod
	def copy_mass_list(mass_list):
		new_mass_list = [[0 for i in range(8)] for j in range(8)]
		for i in range(Common.MASS_NUM):
			for j in range(Common.MASS_NUM):
				new_mass_list[i][j] = mass_list[i][j]
		return new_mass_list

	@staticmethod
	def reverse(mass_list, x, y, mass_type):
		new_mass_list = Util.copy_mass_list(mass_list)
		new_mass_list = Util.reverse_1dir(new_mass_list, x, y,  1,  1, mass_type)
		new_mass_list = Util.reverse_1dir(new_mass_list, x, y,  0,  1, mass_type)
		new_mass_list = Util.reverse_1dir(new_mass_list, x, y, -1,  1, mass_type)
		new_mass_list = Util.reverse_1dir(new_mass_list, x, y, -1,  0, mass_type)
		new_mass_list = Util.reverse_1dir(new_mass_list, x, y, -1, -1, mass_type)
		new_mass_list = Util.reverse_1dir(new_mass_list, x, y,  0, -1, mass_type)
		new_mass_list = Util.reverse_1dir(new_mass_list, x, y,  1, -1, mass_type)
		new_mass_list = Util.reverse_1dir(new_mass_list, x, y,  1,  0, mass_type)
		return new_mass_list

	@staticmethod
	def reverse_1dir(mass_list, x, y, dx, dy, mass_type):
		new_mass_list = Util.copy_mass_list(mass_list)

		searching_x = x
		searching_y = y

		if mass_list[x][y] != mass_type:
			return new_mass_list

		opp_mass_type = Util.get_opp_type(mass_type)

		while True:
			searching_x += dx
			searching_y += dy
			if 0 <= searching_x < Common.MASS_NUM and 0 <= searching_y < Common.MASS_NUM:
				if mass_list[searching_x][searching_y] == mass_type:
					break
				elif mass_list[searching_x][searching_y] == MassType.EMPTY:
					return new_mass_list
			else:
				return new_mass_list

		while True:
			searching_x -= dx
			searching_y -= dy
			if searching_x == x and searching_y == y:
				break
			else:
				new_mass_list[searching_x][searching_y] = mass_type

		return new_mass_list

	@staticmethod
	def can_put(mass_list, x, y, mass_type):
		if mass_list[x][y] != MassType.EMPTY:
			return False
		elif Util.get_reversible_num(mass_list, x, y, mass_type) <= 0:
			return False
		else:
			return True

	@staticmethod
	def can_put_somewhere(mass_list, mass_type):
		for i in range(Common.MASS_NUM):
			for j in range(Common.MASS_NUM):
				if Util.can_put(mass_list, i, j, mass_type):
					return True
		return False

	@staticmethod
	def get_reversible_num(mass_list, x, y, mass_type):
		num = 0
		num += Util.get_reversible_num_1dir(mass_list, x, y,  1,  1, mass_type)
		num += Util.get_reversible_num_1dir(mass_list, x, y,  0,  1, mass_type)
		num += Util.get_reversible_num_1dir(mass_list, x, y, -1,  1, mass_type)
		num += Util.get_reversible_num_1dir(mass_list, x, y, -1,  0, mass_type)
		num += Util.get_reversible_num_1dir(mass_list, x, y, -1, -1, mass_type)
		num += Util.get_reversible_num_1dir(mass_list, x, y,  0, -1, mass_type)
		num += Util.get_reversible_num_1dir(mass_list, x, y,  1, -1, mass_type)
		num += Util.get_reversible_num_1dir(mass_list, x, y,  1,  0, mass_type)
		return num

	@staticmethod
	def get_reversible_num_1dir(mass_list, x, y, dx, dy, mass_type):
		num = 0
		searching_x = x
		searching_y = y

		if mass_list[x][y] != MassType.EMPTY:
			return 0

		opp_mass_type = Util.get_opp_type(mass_type)

		while True:
			searching_x += dx
			searching_y += dy
			if 0 <= searching_x < Common.MASS_NUM and 0 <= searching_y < Common.MASS_NUM:
				if mass_list[searching_x][searching_y] == mass_type:
					break
				elif mass_list[searching_x][searching_y] == MassType.EMPTY:
					return 0
			else:
				return 0

		while True:
			searching_x -= dx
			searching_y -= dy
			if searching_x == x and searching_y == y:
				break
			else:
				num += 1
		return num

	@staticmethod
	def get_piece_num(mass_list, mass_type):
		num = 0
		for i in range(Common.MASS_NUM):
			for j in range(Common.MASS_NUM):
				if mass_list[i][j] == mass_type:
					num += 1
		return num



	@staticmethod
	def get_opp_type(mass_type):
		if mass_type == MassType.WHITE:
			return MassType.BLACK
		elif mass_type == MassType.BLACK:
			return MassType.WHITE
		else:
			return MassType.EMPTY