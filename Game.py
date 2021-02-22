from Board import *
from Common import Common
#from GUI import GUI
from Log import Log
from MassType import MassType
from Player import Player, PlayerType
from Strategy import StrategyType
from Util import Util

#import pygame


class Game:

	def __init__(self):

		#self.root = parent
		#self.gui = GUI(parent, self)

		self.log = Log('log.txt')

		self.players = {
			MassType.BLACK: Player(MassType.BLACK),
			MassType.WHITE: Player(MassType.WHITE),
		}

		self.start_app()

	def start_app(self):

		# BGMの再生を開始
		# pygame.mixer.init()
		# pygame.mixer.music.set_volume(0.10)
		# self.bgm = pygame.mixer.Sound('bgm.wav')
		# self.bgm.play(-1)

		# Top画面を表示
		#self.gui.show_top()

		self.start_game(PlayerType.CPU, PlayerType.CPU)

	def start_game(self, black_player_type, white_player_type):

		# 盤面を初期化
		self.board = Board()

		# 黒が先手
		self.turn = MassType.BLACK

		# プレイヤータイプをセット
		self.players[MassType.BLACK].type = black_player_type
		self.players[MassType.WHITE].type = white_player_type

		# CPUが使用する駒配置アルゴリズムをセット
		if black_player_type == PlayerType.CPU:
			self.players[MassType.BLACK].set_strategy(StrategyType.FORECAST)
		if white_player_type == PlayerType.CPU:
			self.players[MassType.WHITE].set_strategy(StrategyType.DECREASING_OPP_EVALUATION)

		print('Black Strategy: ' + str(self.players[MassType.BLACK].strategy.type))
		print('White Strategy: ' + str(self.players[MassType.WHITE].strategy.type))

		# スコアを初期化
		self.players[MassType.BLACK].score = 2
		self.players[MassType.WHITE].score = 2

		while True:

			mass_list_temp = Util.copy_mass_list(self.board.mass_list)
			x, y = self.players[self.turn].put(mass_list_temp)
			has_finished = self.update(x, y)

			if has_finished:
				break

		if self.players[MassType.BLACK].score < self.players[MassType.WHITE].score:
			winner = 'White'
		elif self.players[MassType.BLACK].score > self.players[MassType.WHITE].score:
			winner = 'Black'
		else:
			winner = 'Draw'

		print('Winner: ' + winner)
		print('Black: ' + str(self.players[MassType.BLACK].score))
		print('White: ' + str(self.players[MassType.WHITE].score))

	def update(self, x, y):

		if self.board.update(x, y, self.turn):

			# ログ書き込み
			self.log.write(self.turn, x, y)

			# スコアを更新
			self.players[MassType.BLACK].score = self.board.get_piece_num(MassType.BLACK)
			self.players[MassType.WHITE].score = self.board.get_piece_num(MassType.WHITE)

			# ターン交代
			self.turn = Util.get_opp_type(self.turn)

			# 終了した場合
			has_finished = self.board.has_finished()

			if not has_finished:
				# パスを判定
				if not self.board.can_put_somewhere(self.turn):
					self.turn = Util.get_opp_type(self.turn)

			return has_finished

	def show_board(self, mass_list):

		for i in range(Common.MASS_NUM):
			for j in range(Common.MASS_NUM):
				mass_type = self.board.mass_list[i][j]
				if mass_type == MassType.BLACK:
					print('⚫️', end='')
				elif mass_type == MassType.WHITE:
					print('⚪️', end='')
				else:
					print('　', end='')
			print()