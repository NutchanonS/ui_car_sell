import tkinter as tk
from tkinter import ttk
import mysql.connector
import pandas as pd
from tkcalendar import DateEntry
from pages import startpage,firstpage,detail_page

class tkinterApp(tk.Tk):
	# __init__ function for class tkinterApp
	def __init__(self, *args, **kwargs):
		
		# __init__ function for class Tk
		tk.Tk.__init__(self, *args, **kwargs)
		#---------------connect db--------------------------------
		mydb = mysql.connector.connect(
			host="localhost",
			user="root",
			password="Pns1.5997gg"
		)
		self.mydb = mydb
		self.mycursor = self.mydb.cursor(buffered=True)
		self.mydb.autocommit = True
		#---------------connect db--------------------------------
		# creating a container
		self.geometry("700x300")
		self.rowconfigure(0,weight=1)
		self.columnconfigure(0,weight=1)
		
		container = tk.Frame(self)
		# container.pack(side = "top", fill = "both", expand = True)
		container.pack(side = "top", fill = "both",expand = False)
		container.grid_rowconfigure(0, weight = 1)
		container.grid_columnconfigure(0, weight = 1)

		self.frames = {}  

		for F in (startpage, firstpage):
			frame = F(container, self)
			self.frames[F] = frame

			frame.grid(row = 0, column = 0, sticky ="nsew")
			frame.grid_columnconfigure(0, weight = 1)
			frame.grid_rowconfigure(0, weight = 1)
			frame.grid_propagate(1)
			
		self.show_frame(startpage)
	def show_frame(self, cont):
		if cont == startpage:
			self.geometry("1920x720")
			# self.minsize(550, 300)
			# self.maxsize(550, 300)
		elif cont == firstpage:
			# self.minsize(100, 100)
			# self.maxsize(1200, 1200)
			self.geometry("1800x1000")
		frame = self.frames[cont]
		frame.tkraise()