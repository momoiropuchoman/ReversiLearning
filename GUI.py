from BButton import BButton
from Board import Board
from Common import Common
from MassType import MassType

from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox


class GUI:

	def __init__(self, root, game):
		self.root = root

		# Top画面
		self.top_frame = tk.Frame(self.root, width=Common.WINDOW_WIDTH, height=Common.WINDOW_HEIGHT, bg='#006400')

		self.logo_canvas = tk.Canvas(self.top_frame, width=Common.WINDOW_WIDTH, height=200,
									 highlightthickness=0, bg=self.top_frame['bg'])
		self.logo_canvas.place(x=0, y=0)

		logo_image_tmp = Image.open('logo.png')
		self.logo_image = ImageTk.PhotoImage(image=logo_image_tmp)
		self.logo_canvas.create_image((Common.WINDOW_WIDTH - 240) // 2,
									  (200 - 150) // 2,
									  image=self.logo_image, anchor='nw')

		self.play_first_button = BButton(self.top_frame, text='先攻(黒)でスタート', font=Common.TOP_BUTTON_FONT,
										 fg='Black', bg='Grey',
										 width=Common.TOP_BUTTON_WIDTH, height=Common.BUTTON_HEIGHT,
										 command=game.on_clicked_play_first_button)
		self.play_first_button.place(x=(Common.WINDOW_WIDTH - Common.TOP_BUTTON_WIDTH) / 2, y=200)

		self.play_second_button = BButton(self.top_frame, text='後攻(白)でスタート', font=Common.TOP_BUTTON_FONT,
										  fg='Black', bg='Grey',
										  width=Common.TOP_BUTTON_WIDTH, height=Common.BUTTON_HEIGHT,
										  command=game.on_clicked_play_second_button)
		self.play_second_button.place(x=(Common.WINDOW_WIDTH - Common.TOP_BUTTON_WIDTH) / 2, y=300)

		self.human_match_button = BButton(self.top_frame, text='人間同士で対戦', font=Common.TOP_BUTTON_FONT,
										  fg='Black', bg='Grey',
										  width=Common.TOP_BUTTON_WIDTH, height=Common.BUTTON_HEIGHT,
										  command=game.on_clicked_human_match_button)
		self.human_match_button.place(x=(Common.WINDOW_WIDTH - Common.TOP_BUTTON_WIDTH) / 2, y=400)

		self.cpu_match_button = BButton(self.top_frame, text='CPU対戦を見る', font=Common.TOP_BUTTON_FONT,
										fg='Black', bg='Grey',
										width=Common.TOP_BUTTON_WIDTH, height=Common.BUTTON_HEIGHT,
										command=game.on_clicked_cpu_match_button)
		self.cpu_match_button.place(x=(Common.WINDOW_WIDTH - Common.TOP_BUTTON_WIDTH) / 2, y=500)

		# 対戦画面
		self.game_frame = tk.Frame(self.root, width=Common.WINDOW_WIDTH, height=Common.WINDOW_HEIGHT, bg='Grey')

		self.game_canvas = tk.Canvas(self.game_frame, width=Common.WINDOW_WIDTH, height=Common.WINDOW_HEIGHT,
									 highlightthickness=0, background='Gray')
		self.game_canvas.place(x=0, y=0)

		self.board_canvas = tk.Canvas(self.game_canvas, width=Common.BOARD_WIDTH, height=Common.BOARD_HEIGHT,
									  highlightthickness=0, background='#006400')
		self.board_canvas.place(x=Common.MASS_INDEX_WIDTH, y=Common.MASS_INDEX_HEIGHT)
		self.board_canvas.bind('<ButtonPress-1>', game.on_clicked_mass)

		# 得点表示画面の準備
		piece_offset_x = (Common.SCORE_WIDTH - Common.SCORE_PIECE_SIZE) // 2
		piece_offset_y = (Common.SCORE_HEIGHT // 2 - Common.SCORE_PIECE_SIZE) // 2

		self.black_score_canvas = tk.Canvas(self.game_frame, width=Common.SCORE_WIDTH, height=Common.SCORE_HEIGHT,
											highlightthickness=0, bg='Red')
		self.black_score_canvas.place(x=Common.MASS_INDEX_WIDTH + Common.BOARD_WIDTH, y=Common.MASS_INDEX_HEIGHT)
		self.black_score_canvas.create_oval(piece_offset_x,
											piece_offset_y,
											piece_offset_x + Common.SCORE_PIECE_SIZE,
											piece_offset_y + Common.SCORE_PIECE_SIZE,
											fill='Black', outline='White')
		self.black_score_canvas.create_text(Common.SCORE_WIDTH // 2,
											Common.SCORE_HEIGHT // 2 + Common.SCORE_HEIGHT // 4,
											text='',
											fill='Black',
											font=("MSゴシック", "60", "bold"),
											tag='black_score')

		self.white_score_canvas = tk.Canvas(self.game_frame, width=Common.SCORE_WIDTH, height=Common.SCORE_HEIGHT,
											highlightthickness=0, bg='Black')
		self.white_score_canvas.place(x=Common.MASS_INDEX_WIDTH + Common.BOARD_WIDTH,
									  y=Common.MASS_INDEX_HEIGHT + Common.SCORE_HEIGHT + Common.BUTTON_HEIGHT * 3)
		self.white_score_canvas.create_oval(piece_offset_x,
											piece_offset_y,
											piece_offset_x + Common.SCORE_PIECE_SIZE,
											piece_offset_y + Common.SCORE_PIECE_SIZE,
											fill='White', outline='White')
		self.white_score_canvas.create_text(Common.SCORE_WIDTH // 2,
											Common.SCORE_HEIGHT // 2 + Common.SCORE_HEIGHT // 4,
											text='',
											fill='White',
											font=("MSゴシック", "60", "bold"),
											tag='white_score')

		self.undo_button = BButton(self.game_frame, text='1手戻る', font=("MSゴシック", "24", "bold"),
								   fg='Black', bg='Grey',
								   width=Common.BUTTON_WIDTH, height=Common.BUTTON_HEIGHT,
								   command=game.on_clicked_undo_button)
		self.undo_button.place(x=Common.MASS_INDEX_WIDTH + Common.BOARD_WIDTH,
							   y=Common.MASS_INDEX_HEIGHT + Common.SCORE_HEIGHT)

		self.restart_button = BButton(self.game_frame, text='はじめから', font=("MSゴシック", "24", "bold"),
									  fg='Black', bg='Grey',
									  width=Common.BUTTON_WIDTH, height=Common.BUTTON_HEIGHT,
									  command=game.on_clicked_restart_button)
		self.restart_button.place(x=Common.MASS_INDEX_WIDTH + Common.BOARD_WIDTH,
								  y=Common.MASS_INDEX_HEIGHT + Common.SCORE_HEIGHT + Common.BUTTON_HEIGHT)

		self.top_back_button = BButton(self.game_frame, text='Topに戻る', font=("MSゴシック", "24", "bold"),
									   fg='Black', bg='Grey',
									   width=Common.BUTTON_WIDTH, height=Common.BUTTON_HEIGHT,
									   command=game.on_clicked_top_back_button)
		self.top_back_button.place(x=Common.MASS_INDEX_WIDTH + Common.BOARD_WIDTH,
								   y=Common.MASS_INDEX_HEIGHT + Common.SCORE_HEIGHT + Common.BUTTON_HEIGHT * 2)

		self.score_canvas = {
			MassType.BLACK: self.black_score_canvas,
			MassType.WHITE: self.white_score_canvas,
		}

		for i in range(9):
			self.game_canvas.create_line(Common.MASS_INDEX_WIDTH + Common.MASS_SIZE * i, 0,
										 Common.MASS_INDEX_WIDTH + Common.MASS_SIZE * i, Common.BOARD_WIDTH,
										 fill='White')
		for j in range(9):
			self.game_canvas.create_line(0, Common.MASS_INDEX_HEIGHT + Common.MASS_SIZE * j, Common.BOARD_HEIGHT,
										 Common.MASS_INDEX_HEIGHT + Common.MASS_SIZE * j, fill='White')

		for i in range(8):
			self.game_canvas.create_text(Common.MASS_INDEX_WIDTH + Common.MASS_SIZE * i + 40,
										 20,
										 text=str(i+1),
										 fill='Black',
										 font=("MSゴシック", "32", "bold"),
										 tag='black_score')

			self.game_canvas.create_text(20,
										 Common.MASS_INDEX_HEIGHT + Common.MASS_SIZE * i + 40,
										 text=str(i + 1),
										 fill='Black',
										 font=("MSゴシック", "32", "bold"),
										 tag='black_score')

		for i in range(9):
			self.board_canvas.create_line(Common.MASS_SIZE * i, 0, Common.MASS_SIZE * i, Common.BOARD_WIDTH,
										  fill='White')
		for j in range(9):
			self.board_canvas.create_line(0, Common.MASS_SIZE * j, Common.BOARD_HEIGHT, Common.MASS_SIZE * j,
										  fill='White')

		self.piece_id_set = set()
		self.puttable_id_set = set()

	def show_top(self):
		self.game_frame.place_forget()
		self.top_frame.place(x=0, y=0)

	def show_game(self):
		self.top_frame.place_forget()
		self.game_frame.place(x=0, y=0)

	def clear_board(self):
		for piece_id in self.piece_id_set:
			self.board_canvas.delete(piece_id)
		for puttable_id in self.puttable_id_set:
			self.board_canvas.delete(puttable_id)
		self.score_canvas[MassType.BLACK].delete('turn_border')
		self.score_canvas[MassType.WHITE].delete('turn_border')

	def clear_latest_mass(self):
		self.board_canvas.delete('latest_mass')

	def draw_board(self, piece_list, puttable_list, black_score, white_score, mass_type):
		self.draw_pieces(piece_list)
		self.draw_puttable(puttable_list)
		self.draw_score(black_score, white_score, mass_type)

	def draw_pieces(self, mass_list):
		offset = (Common.MASS_SIZE - Common.BOARD_PIECE_SIZE) // 2
		for i in range(Common.MASS_NUM):
			for j in range(Common.MASS_NUM):
				id = 0
				if mass_list[i][j] == MassType.BLACK:
					id = self.board_canvas.create_oval(i * Common.MASS_SIZE + offset,
													   j * Common.MASS_SIZE + offset,
													   i * Common.MASS_SIZE + offset + Common.BOARD_PIECE_SIZE,
													   j * Common.MASS_SIZE + offset + Common.BOARD_PIECE_SIZE,
													   fill='Black')
				elif mass_list[i][j] == MassType.WHITE:
					id = self.board_canvas.create_oval(i * Common.MASS_SIZE + offset,
													   j * Common.MASS_SIZE + offset,
													   i * Common.MASS_SIZE + offset + Common.BOARD_PIECE_SIZE,
													   j * Common.MASS_SIZE + offset + Common.BOARD_PIECE_SIZE,
													   fill='White')
				self.piece_id_set.add(id)

	def draw_puttable(self, puttable_list):
		# tag = 'puttable' + str(self.index_x) + str(self.index_y)
		# self.canvas.delete(tag)
		for i in range(Common.MASS_NUM):
			for j in range(Common.MASS_NUM):
				if puttable_list[i][j]:
					id = self.board_canvas.create_rectangle(i * Common.MASS_SIZE + 1,
															j * Common.MASS_SIZE + 1,
															i * Common.MASS_SIZE + Common.MASS_SIZE - 1,
															j * Common.MASS_SIZE + Common.MASS_SIZE - 1,
															outline='#3cb371', width=0, fill='#3cb371')
					self.puttable_id_set.add(id)

	def draw_score(self, black_score, white_score, mass_type):
		# self.score_labels[MassType.BLACK]['text'] = black_score
		# self.score_labels[MassType.WHITE]['text'] = white_score
		self.score_canvas[mass_type].create_rectangle(0, 0, Common.SCORE_WIDTH,
													  Common.SCORE_HEIGHT,
													  outline='Blue',
													  width=Common.TURN_BORDER_THICKNESS,
													  tag='turn_border')
		self.score_canvas[MassType.BLACK].itemconfig('black_score', text=str(black_score))
		self.score_canvas[MassType.WHITE].itemconfig('white_score', text=str(white_score))

	def draw_latest_mass(self, x, y):
		self.board_canvas.create_rectangle(x * Common.MASS_SIZE + 1,
										   y * Common.MASS_SIZE + 1,
										   x * Common.MASS_SIZE + Common.MASS_SIZE - 1,
										   y * Common.MASS_SIZE + Common.MASS_SIZE - 1,
										   outline='Yellow', width=4,
										   tag='latest_mass')

	def show_skip_dialog(self):
		self.root.after(200, lambda: messagebox.showinfo('通知', '置く場所がないためパスします'))

	def show_result_dialog(self, black_score, white_score):
		if white_score < black_score:
			message = '黒の勝ちです'
		elif black_score < white_score:
			message = '白の勝ちです'
		else:
			message = '引き分けです'

		self.root.after(200, lambda: messagebox.showinfo('ゲーム終了', message))
