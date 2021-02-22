import tkinter as tk
from tkinter import BOTH


class BButton(tk.Button):
	def __init__(self, parent, width, height, text, font, fg, bg, command):
		self.frame = tk.Frame(parent, width=width, height=height, bg=parent['bg'])
		self.frame.pack_propagate(0)

		super(BButton, self).__init__(self.frame, width=width, height=height, text=text, fg=fg, bg=bg, font=font, command=command)
		self.pack(fill=BOTH, expand=1)

	def place(self, x, y):
		self.frame.place(x=x, y=y)