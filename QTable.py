from Common import Common
from MassType import MassType
from Util import Util
import numpy

# table[s][a] = Q
# s: 状況	0〜127	ある時点での総枚数 0〜63は優勢時、64〜127は劣勢時
# a: 戦略	0〜4
# Q: Q値

class QTable:

	def __init__(self, file_name):
		self.file_name = file_name
		with open(self.file_name, 'a') as file:
			file.write('---start---' + '\n')

		self.table = numpy.zeros((64*3, 5))
		print(self.table)

		self.learning_rate = 0.5
		self.discount_factor = 0.8

	def update(self, reward, ):















