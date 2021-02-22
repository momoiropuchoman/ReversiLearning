from Common import Common
from MassType import MassType
from Util import Util

class Board:

	def __init__(self):

		self.mass_list = Util.get_initial_mass_list()

	def set_mass_list(self, mass_list):
		self.mass_list = mass_list

	def update(self, x, y, mass_type):

		if Util.can_put(self.mass_list, x, y, mass_type):

			# 駒を配置
			self.mass_list[x][y] = mass_type

			# 駒をひっくり返す
			self.mass_list = Util.reverse(self.mass_list, x, y, mass_type)

			return True

		else:
			return False

	def has_finished(self):
		for i in range(Common.MASS_NUM):
			for j in range(Common.MASS_NUM):
				if Util.can_put(self.mass_list, i, j, MassType.BLACK) or Util.can_put(self.mass_list, i, j, MassType.WHITE):
					return False
		return True

	def get_puttable_list(self, mass_type):
		return Util.get_puttable_list(self.mass_list, mass_type)

	def can_put_somewhere(self, mass_type):
		return Util.can_put_somewhere(self.mass_list, mass_type)

	def get_piece_num(self, mass_type):
		return Util.get_piece_num(self.mass_list, mass_type)