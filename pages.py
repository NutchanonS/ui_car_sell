import tkinter as tk
from tkinter import ttk
import mysql.connector
import pandas as pd
from pandas.api.types import CategoricalDtype
from tkcalendar import DateEntry, Calendar
# import tkinter.font as font
from tkinter import font
from tkinter import Frame
class startpage(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.myFont = font.Font(family='Helvetica',size=20)
		# #---------------------------------home page-------------------------------------------------
		# #----------------------------user info---------------------------
		self.controller = controller

		self.frame1 = Frame(self)
		self.frame1.grid(row= 0, column=0, sticky='ns',padx=0,pady=0)
		self.frame1.grid_columnconfigure(0, weight = 1)
		self.frame1.grid_rowconfigure(0, weight = 1)
		self.frame1.grid_propagate(1)#-------------------------------------------------------------แก้

		user_info_frame = tk.Label(self.frame1)
		user_info_frame.grid(row= 0, column=0, padx=20, pady=0)
		user_info = tk.Label(user_info_frame, text="ทะเบียน/ชื่อลูกค้า/เบอร์โทร", font=self.myFont)
		user_info.grid(row=0, column=0)
		self.user_info_entry = tk.Entry(user_info_frame, font=self.myFont)
		self.user_info_entry.grid(row=1, column=0)
		# #----------------------------info button---------------------------
		search_but = tk.Button(self.frame1, text="ค้นหา", command = self.search, font=self.myFont)
		search_but.grid(row=0, column=1, padx=10, pady=10)
		delete_but = tk.Button(self.frame1, text="ลบ", command= self.delete, font=self.myFont)
		delete_but.grid(row=0, column=2, padx=10, pady=10)
		# regist_but = tk.Button(self.frame1, text="ลงทะเบียน", command = lambda : self.controller.show_frame(firstpage), font=self.myFont)
		regist_but = tk.Button(self.frame1, text="ลงทะเบียน", command = self.regist_showframe, font=self.myFont)
		regist_but.grid(row=0, column=3, padx=10, pady=10)
		# #----------------------------table---------------------------
		self.frame2 = Frame(self)
		self.frame2.grid(row= 1, column=0, sticky='ns',padx=0,pady=0)
		self.frame2.grid_columnconfigure(0, weight = 1)
		self.frame2.grid_rowconfigure(0, weight = 1)
		self.frame2.grid_propagate(1)#-------------------------------------------------------------แก้

		style = ttk.Style()
		style.configure("Treeview.Heading", font=self.myFont)
		style.configure("Treeview", font=self.myFont,rowheight=60)
		self.car_table = ttk.Treeview(self.frame2, show='headings',height=8)#---------------------------table & scroll---------------------------
		self.verscrlbar = tk.Scrollbar(self.frame2,)
		self.verscrlbar.configure(orient="vertical",
								command = self.car_table.yview)
		self.car_table.configure(yscrollcommand = self.verscrlbar.set)
		self.car_table.grid(row=0, column=0,padx=10,pady=10)
		self.verscrlbar.grid(row=0,column=1,sticky='ns')
		
		self.xscrlbar = tk.Scrollbar(self.frame2,)
		self.xscrlbar.configure(orient="horizontal",
								command = self.car_table.xview)
		self.car_table.configure(xscrollcommand = self.xscrlbar.set)
		self.xscrlbar.grid(row=1,column=0,sticky='nsew')

		self.car_table.bind("<ButtonRelease-1>", self.On_table_click_button_release)
		self.car_table.bind("<Double-1>", self.On_table_click)
		table_col = ('No.', 'ชื่อผู้ซื้อ','ทะเบียนรถ', 'ราคารถ', \
							'ยี่ห้อ/สีรถ', 'สถานะ', 'วันที่ซื้อรถ', 'วันขายรถ', 'วันนัดจ่ายค้าง','วันจดทะเบียนรถ','เบอร์โทร')
		self.car_table['columns'] = table_col
		self.db_labels = ["car_no","date_buy","car_price","brand_color","car_year","sell_date","client_name",
			"Tel","deposit","finance","pay_down","remain_down","pay_down_date","fee","oil_price",
			"na","transfer_book_price","repair_price","driver_price","engine_oil_price","other_price",
			"state","car_regist_date","finance_place"]
		self.ui_labels = ["ทะเบียนรถ","วันที่ซื้อรถ","ราคารถ","ยี่ห้อ/สีรถ","ปีรถ",
		"วันขายรถ","ชื่อผู้ซื้อ","เบอร์โทร","มัดจำ","ไฟแนนซ์","จ่ายดาว","ค้างดาว","วันนัดจ่ายค้าง",
		"ค่าพรบ.","ค่าน้ำมัน","ค่าจ้างนา","โอนเล่ม","ค่าซ่อม","ค่าคนขับ","น้ำมันเครื่อง","ค่าทำเรื่อง/อื่นๆ",
		"สถานะ","วันจดทะเบียนรถ","ที่ทำไฟแนนซ์"]
		self.db_labels = {self.ui_labels[i]:self.db_labels[i] for i in range(len(self.ui_labels))}
		# ["ทะเบียนรถ","วันที่ซื้อรถ","ราคารถ","ยี่ห้อ/สีรถ","ปีรถ",
		# "วันขายรถ","ชื่อผู้ซื้อ","เบอร์โทร","มัดจำ","ไฟแนนซ์","จ่ายดาว","ค้างดาว","วันนัดจ่ายค้าง",
		# "ค่าพรบ.","ค่าน้ำมัน","ค่าจ้างนา","โอนเล่ม","ค่าซ่อม","ค่าคนขับ","น้ำมันเครื่อง","ค่าทำเรื่อง/อื่นๆ",
		# "สถานะ","วันจดทะเบียนรถ","ที่ทำไฟแนนซ์"]
		self.car_table.column("No.", width=50, anchor=tk.CENTER)
		self.car_table.column("ชื่อผู้ซื้อ", width=180, anchor=tk.CENTER)
		self.car_table.column("ทะเบียนรถ", width=180, anchor=tk.CENTER)
		self.car_table.column("ราคารถ", width=180, anchor=tk.CENTER)
		self.car_table.column("ยี่ห้อ/สีรถ", width=180, anchor=tk.CENTER)
		self.car_table.column("สถานะ",width=180, anchor=tk.CENTER)
		self.car_table.column("วันที่ซื้อรถ",width=180, anchor=tk.CENTER )
		self.car_table.column("วันขายรถ",width=180, anchor=tk.CENTER )
		self.car_table.column("วันนัดจ่ายค้าง",width=180, anchor=tk.CENTER )
		self.car_table.column("วันจดทะเบียนรถ",width=180, anchor=tk.CENTER )
		self.car_table.column("เบอร์โทร",width=180, anchor=tk.CENTER)

		self.car_table.heading("No.",text="No.")
		self.car_table.heading("ชื่อผู้ซื้อ",text="ชื่อผู้ซื้อ")
		self.car_table.heading("ทะเบียนรถ",text="ทะเบียนรถ")
		self.car_table.heading("ราคารถ",text="ราคารถ")
		self.car_table.heading("ยี่ห้อ/สีรถ",text="ยี่ห้อ/สีรถ")
		self.car_table.heading("สถานะ",text="สถานะ", command = self.state_asc)
		self.car_table.heading("วันที่ซื้อรถ",text="วันที่ซื้อรถ", command = self.date_buy_asc)
		self.car_table.heading("วันขายรถ",text="วันขายรถ",command = self.sell_date_asc)
		self.car_table.heading("วันนัดจ่ายค้าง",text="วันนัดจ่ายค้าง",command = self.pay_down_date_asc)
		self.car_table.heading("วันจดทะเบียนรถ",text="วันจดทะเบียนรถ",command = self.car_regist_date_asc)
		self.car_table.heading("เบอร์โทร",text="เบอร์โทร")
# 		self.car_table['columns'] = ('No.', 'ชื่อผู้ซื้อ','ทะเบียนรถ', 'ยี่ห้อ/สีรถ', \
# 							'สถานะ', 'วันขายรถ','เบอร์โทร')
# #'No.', 'ชื่อผู้ซื้อ','ทะเบียนรถ', 'ราคารถ'
# # 'ยี่ห้อ/สีรถ', 'สถานะ', 'วันซื้อรถ', 'วันขายรถ', วันนัดจ่ายค้างดาว','เบอร์โทร'
# 		self.car_table.column("No.", width=50, anchor=tk.CENTER)
# 		self.car_table.column("ชื่อผู้ซื้อ", width=180, anchor=tk.CENTER)
# 		self.car_table.column("ทะเบียนรถ", width=180, anchor=tk.CENTER)
# 		self.car_table.column("ยี่ห้อ/สีรถ", width=180, anchor=tk.CENTER)
# 		self.car_table.column("สถานะ",width=180, anchor=tk.CENTER)
# 		self.car_table.column("วันขายรถ",width=180, anchor=tk.CENTER )
# 		self.car_table.column("เบอร์โทร",width=180, anchor=tk.CENTER)

# 		self.car_table.heading("No.",text="No.")
# 		self.car_table.heading("ชื่อผู้ซื้อ",text="ชื่อผู้ซื้อ")
# 		self.car_table.heading("ทะเบียนรถ",text="ทะเบียนรถ")
# 		self.car_table.heading("ยี่ห้อ/สีรถ",text="ยี่ห้อ/สีรถ")
# 		self.car_table.heading("สถานะ",text="สถานะ")
# 		self.car_table.heading("วันขายรถ",text="วันขายรถ",command = self.sell_date)
		self.sell_date_asc = True
		self.state_asc = True
		self.date_buy_asc = True
		# self.car_price_asc = True
		self.pay_down_date_asc = True
		self.car_regist_date_asc = True
		
		self.query2df()
		self.row_select = None
		#-----------------show all table in naiwork db--------
	def reset_index(self):
		col = [ 'ชื่อผู้ซื้อ','ทะเบียนรถ', 'ราคารถ', \
					'ยี่ห้อ/สีรถ', 'สถานะ', 'วันที่ซื้อรถ', 'วันขายรถ', 'วันนัดจ่ายค้าง','วันจดทะเบียนรถ','เบอร์โทร']
		self.carinfo_df = self.carinfo_df.reset_index(drop=True)
		self.carinfo_df["No."] = self.carinfo_df.index +1
		self.carinfo_df = self.carinfo_df[['No.'] + col]
	def query2df(self):
		self.controller.mycursor.execute("use naiwork;")
		self.controller.mycursor.execute("show tables;")
		myresult = self.controller.mycursor.fetchall()
		for x in myresult:
			print("tables:",x)
		#----------------------create dataframe;---------------------------
		# self.controller.mycursor.execute("select ROW_NUMBER() OVER(order by date_buy) AS NUM, date_buy,car_no,price,brand from carinfo;")

		# col = ('No.', 'ชื่อผู้ซื้อ','ทะเบียนรถ', 'ราคารถ', \
		# 					'ยี่ห้อ/สีรถ', 'สถานะ', 'วันที่ซื้อรถ', 'วันขายรถ', 'วันนัดจ่ายค้าง','วันจดทะเบียนรถ','เบอร์โทร')
		col = [ 'ชื่อผู้ซื้อ','ทะเบียนรถ', 'ราคารถ', \
					'ยี่ห้อ/สีรถ', 'สถานะ', 'วันที่ซื้อรถ', 'วันขายรถ', 'วันนัดจ่ายค้าง','วันจดทะเบียนรถ','เบอร์โทร']
		query = (self.db_labels[i] for i in col[1:])
		##print("select {} from carinfo;".format(','.join(query)))
		q='select client_name,car_no,car_price,brand_color,state,date_buy,sell_date,pay_down_date,car_regist_date,Tel from carinfo;'
		# self.controller.mycursor.execute("SELECT {} from carinfo;".format(','.join(query)))
		self.controller.mycursor.execute(q)
		# ##print('----------')
		# self.controller.mycursor.execute("select client_name,car_no,brand_color,\
		# 		   state,sell_date,Tel from carinfo;")
		myresult = self.controller.mycursor.fetchall()
		# # columns = [col[0] for col in controller.mycursor.description]
		# col = [ 'ชื่อผู้ซื้อ', 'ทะเบียนรถ', 'ยี่ห้อ/สีรถ', 'สถานะ','วันขายรถ','เบอร์โทร']
		self.carinfo_df = pd.DataFrame(myresult, columns=col)
		self.carinfo_df[["ราคารถ"]]  = self.carinfo_df[["ราคารถ"]].fillna(0)
		# self.carinfo_df.groupby(["สถานะ"])
		# self.carinfo_df.sort_values(["รอขาย", "รอเข้าขนส่ง", "ค้างขนส่ง", "รอเข้าแนนซ์","เข้าแนนซ์"],ascending=False).groupby('สถานะ')
		# self.carinfo_df["วันขายรถ"] = pd.to_datetime(self.carinfo_df["วันขายรถ"], format='%Y-%m-%d')
		# self.carinfo_df.to_csv('test.csv')


		# ##print(self.carinfo_df.head())
		self.reset_index()

		# self.carinfo_df.to_csv('test.csv',index=False)
		self.clear_table(self.car_table)
		self.insert_dataframe(self.car_table, self.carinfo_df)
	def sell_date_asc(self):
		if self.sell_date_asc:
			self.carinfo_df = self.carinfo_df.sort_values(by='วันขายรถ', ascending=True)
			self.sell_date_asc = False
		else: 
			self.carinfo_df = self.carinfo_df.sort_values(by='วันขายรถ', ascending=False)
			self.sell_date_asc = True
		self.reset_index()
		self.clear_table(self.car_table)
		self.insert_dataframe(self.car_table, self.carinfo_df)
	def regist_showframe(self):
		self.controller.show_frame(firstpage)
	def state_asc(self):

		cat_state = CategoricalDtype(
			["รอขาย", "รอเข้าขนส่ง", "ค้างขนส่ง", "รอเข้าแนนซ์","เข้าแนนซ์"], 
			ordered=True,
		)
		self.carinfo_df['สถานะ'] = self.carinfo_df['สถานะ'].astype(cat_state)
		# self.carinfo_df.sort_values(['สถานะ'], ascending=False)

		if self.sell_date_asc:
			self.carinfo_df = self.carinfo_df.sort_values(by='สถานะ', ascending=True)
			self.sell_date_asc = False
		else: 
			self.carinfo_df = self.carinfo_df.sort_values(by='สถานะ', ascending=False)
			self.sell_date_asc = True
		self.reset_index()
		self.clear_table(self.car_table)
		self.insert_dataframe(self.car_table, self.carinfo_df)
	def date_buy_asc(self):
		if self.sell_date_asc:
			self.carinfo_df = self.carinfo_df.sort_values(by='วันที่ซื้อรถ', ascending=True)
			self.sell_date_asc = False
		else: 
			self.carinfo_df = self.carinfo_df.sort_values(by='วันที่ซื้อรถ', ascending=False)
			self.sell_date_asc = True
		self.reset_index()
		self.clear_table(self.car_table)
		self.insert_dataframe(self.car_table, self.carinfo_df)
	def pay_down_date_asc(self):
		if self.sell_date_asc:
			self.carinfo_df = self.carinfo_df.sort_values(by='วันนัดจ่ายค้าง', ascending=True)
			self.sell_date_asc = False
		else: 
			self.carinfo_df = self.carinfo_df.sort_values(by='วันนัดจ่ายค้าง', ascending=False)
			self.sell_date_asc = True
		self.reset_index()
		self.clear_table(self.car_table)
		self.insert_dataframe(self.car_table, self.carinfo_df)
	def car_regist_date_asc(self):
		if self.sell_date_asc:
			self.carinfo_df = self.carinfo_df.sort_values(by='วันจดทะเบียนรถ', ascending=True)
			self.sell_date_asc = False
		else: 
			self.carinfo_df = self.carinfo_df.sort_values(by='วันจดทะเบียนรถ', ascending=False)
			self.sell_date_asc = True
		self.reset_index()
		self.clear_table(self.car_table)
		self.insert_dataframe(self.car_table, self.carinfo_df)
	def refresh_table(self):
		self.clear_table(self.car_table)
		self.insert_dataframe(self.car_table, self.carinfo_df)
	def insert_dataframe(self, table ,df):
		for i in range(len(df)):
			table.insert("", tk.END, values=df.iloc[i].tolist())  
	def clear_table(self, table):
		for row in table.get_children():
			table.delete(row)
	def search(self):
		searh_val = self.user_info_entry.get()
		##print('search...',searh_val)
		if searh_val:
			qdf = self.carinfo_df[(self.carinfo_df["ทะเบียนรถ"] == searh_val) | (self.carinfo_df["เบอร์โทร"] == searh_val) | \
				(self.carinfo_df["ชื่อผู้ซื้อ"] == searh_val)]
			self.clear_table(self.car_table)
			self.insert_dataframe(self.car_table, qdf)
		else: self.refresh_table()
	def delete(self):
		self.controller.mycursor.execute("""DELETE FROM carinfo WHERE car_no="{}";""".format(self.row_select))
		self.query2df()
	def On_table_click(self, event):
		region = self.car_table.identify("region", event.x, event.y)
		if region!="heading":
			item = self.car_table.selection()
			for i in item:
				# ##print("you clicked on", self.car_table.item(i, "values"))
				self.row_select = self.car_table.item(i, "values")[2]

				container = tk.Tk()
				# container = tk.Frame(self.controller)
				# container.pack(side = "top", fill = "both",expand = True)
				# container.grid_rowconfigure(0, weight = 1)
				# container.grid_columnconfigure(0, weight = 1)
				self.row_select_page = detail_page(self.row_select, container, self.controller)
				# self.controller.frames[detail_page] = self.row_select_page
				# self.row_select_page.grid(row = 0, column = 0, sticky ="nsew")
				# self.row_select_page.grid_columnconfigure(0, weight = 1)
				# self.row_select_page.grid_rowconfigure(0, weight = 1)
				# self.row_select_page.grid_propagate(1)
				# # self.row_select_page.tkraise()
				# self.controller.show_frame(detail_page)
				# print(self.controller.frames)


				# self.controller.frames[detail_page] = self.row_select_page
				# self.controller.show_frame(detail_page)

				# self.controller.show_frame(detail_page)
			# ##print("u clicked on",self.row_select)
	def On_table_click_button_release(self, event):
		region = self.car_table.identify("region", event.x, event.y)
		if region!="heading":
			item = self.car_table.selection()
			for i in item:
				# ##print("you clicked on", self.car_table.item(i, "values"))
				self.row_select = self.car_table.item(i, "values")[2]
class firstpage(Frame):
	def __init__(self, parent, controller):
		
		Frame.__init__(self, parent)
		self.myFont = font.Font(family='Helvetica',size=25)

		self.controller = controller
		#------------------------------------------frame1--------------------
		self.frame1 = Frame(self,highlightbackground="black", highlightthickness=0.8)
		self.frame1.grid(row= 0, column=0, padx=5, pady=5, sticky='ns')

		all_labels1 = ["ทะเบียนรถ","วันที่ซื้อรถ","ราคารถ","ยี่ห้อ/สีรถ","ปีรถ"]
		self.labels = {}
		self.labels_other = {}
		for i,t in enumerate(all_labels1):
			if t!="วันที่ซื้อรถ" and t!="ปีรถ":
				label_ = tk.Label( self.frame1 , text=t,font=self.myFont)
				label_.grid(row = i, column = 0, padx = 5, pady = 5)
				self.labels[t] = tk.Entry(self.frame1, font=self.myFont, highlightthickness=2)
				self.labels[t].grid(row=i, column=1, padx = 5, pady = 5)
			else:
				if t == "วันที่ซื้อรถ":
					label_ = tk.Label( self.frame1 , text=t, font=self.myFont)
					label_.grid(row = i, column = 0, padx = 5, pady = 5)
					entry_date = tk.Entry(self.frame1, font=self.myFont)
					entry_date.grid(row=i, column=1, padx = 5, pady = 5)
					self.labels[t] = ""
					self.labels_other[f"{t}"] = entry_date
					# entry_date.bind("<ButtonRelease-1>", lambda event="eiei", entry=entry_date, t=t : self.On_date_click1(event,t, entry))
					entry_date.bind("<Double-1>", lambda event="eiei", entry=entry_date, t=t : self.On_date_click1(event,t, entry))
				else:
					self.year_car = ttk.Combobox(
						self.frame1,
						state="readonly",
						values=["60","61","62","63","64","65","66"], font=self.myFont
					)
					self.year_car.grid(row=4,column=1,padx=5,pady=5)
					year_car_label = tk.Label( self.frame1 , text="ปีรถ", font=self.myFont)
					year_car_label.grid(row = 4, column = 0, padx = 5, pady = 5)

					self.labels["ปีรถ"] = self.year_car
		#--------------------------------------------------------------

		#------------------------------------------frame2--------------------
		self.frame2 = Frame(self,highlightbackground="black", highlightthickness=0.8)
		self.frame2.grid(row= 1, column=0, padx=5, pady=5, sticky='ns',rowspan=3)
		all_labels2 = ["วันขายรถ","ชื่อผู้ซื้อ","เบอร์โทร","มัดจำ",
		 "ไฟแนนซ์","จ่ายดาว","ค้างดาว","วันนัดจ่ายค้าง"]
		for i,t in enumerate(all_labels2):
			if t!="วันขายรถ" and t!="วันนัดจ่ายค้าง":
				label_ = tk.Label( self.frame2 , text=t, font=self.myFont)
				label_.grid(row = i, column = 0, padx = 5, pady = 5)
				self.labels[t] = tk.Entry(self.frame2, font=self.myFont)
				self.labels[t].grid(row=i, column=1, padx = 5, pady = 5)
			else:
				pass
				# label_ = tk.Label( self.frame2 , text=t, font=self.myFont)
				# label_.grid(row = i, column = 0, padx = 5, pady = 5)
				# entry_date = tk.Entry(self.frame2, font=self.myFont, textvariable="eiei")
				# entry_date.grid(row=i, column=1, padx = 5, pady = 5)
				# entry_date.bind("<ButtonRelease-1>", lambda t=t, entry=entry_date: self.On_date_click2(t,entry))
				# entry_date.set(self.labels[i].get_date())
				# self.labels[t] = DateEntry(self.frame2,selectmode='day', font=self.myFont)
				# self.labels[t].grid(row=i, column=1, padx = 5, pady = 5)
		label_ = tk.Label( self.frame2 , text="วันขายรถ", font=self.myFont)
		label_.grid(row = 0, column = 0, padx = 5, pady = 5)
		entry_date = tk.Entry(self.frame2, font=self.myFont)
		entry_date.grid(row=0, column=1, padx = 5, pady = 5)
		self.labels["วันขายรถ"] = ""
		self.labels_other["วันขายรถ"] = entry_date
		# entry_date.bind("<ButtonRelease-1>", lambda event="eiei", entry=entry_date, t="วันขายรถ" : self.On_date_click2(event,t, entry))
		entry_date.bind("<Double-1>", lambda event="eiei", entry=entry_date, t="วันขายรถ" : self.On_date_click2(event,t, entry))

		label_ = tk.Label( self.frame2 , text="วันนัดจ่ายค้าง", font=self.myFont)
		label_.grid(row = 7, column = 0, padx = 5, pady = 5)
		entry_date = tk.Entry(self.frame2, font=self.myFont)
		entry_date.grid(row=7, column=1, padx = 5, pady = 5)
		self.labels["วันนัดจ่ายค้าง"] = ""
		self.labels_other["วันนัดจ่ายค้าง"] = entry_date
		entry_date.bind("<Double-1>", lambda event="eiei", entry=entry_date, t="วันนัดจ่ายค้าง" : self.On_date_click3(event,t, entry))

		#------------------------------------------frame3--------------------
		self.frame3 = Frame(self,highlightbackground="black", highlightthickness=0.8)
		self.frame3.grid(row= 0, column=1, padx=5, pady=5,sticky='ns',rowspan=2)
		
		all_labels2 = ["ค่าพรบ.","ค่าน้ำมัน","ค่าจ้างนา","โอนเล่ม","ค่าซ่อม",
		 "ค่าคนขับ","น้ำมันเครื่อง","ค่าทำเรื่อง/อื่นๆ"]
		for i,t in enumerate(all_labels2):
			label_ = tk.Label( self.frame3 , text=t, font=self.myFont)
			label_.grid(row = i, column = 0, padx = 5, pady = 5)
			self.labels[t] = tk.Entry(self.frame3, font=self.myFont)
			self.labels[t].grid(row=i, column=1, padx = 5, pady = 5)
		#---------------------------------------------------------------
		self.frame4 = Frame(self,highlightbackground="black", highlightthickness=0.8)
		self.frame4.grid(row= 2, column=1, padx=5, pady=5,sticky='n')
		self.state = ttk.Combobox(
			self.frame4,
			state="readonly",
			values=["รอขาย", "รอเข้าขนส่ง", "ค้างขนส่ง", "รอเข้าแนนซ์","เข้าแนนซ์"], font=self.myFont
		)
		self.state.grid(row=0,column=1,padx=5,pady=5)
		comb_label = tk.Label( self.frame4 , text="สถานะ", font=self.myFont)
		comb_label.grid(row = 0, column = 0, padx = 5, pady = 5)
		self.labels["สถานะ"] = self.state

		label_ = tk.Label( self.frame4 , text="วันจดทะเบียนรถ", font=self.myFont)
		label_.grid(row = 1, column = 0, padx = 5, pady = 5)
		entry_date = tk.Entry(self.frame4, font=self.myFont)
		entry_date.grid(row=1, column=1, padx = 5, pady = 5)
		self.labels["วันจดทะเบียนรถ"] = ""
		self.labels_other["วันจดทะเบียนรถ"] = entry_date
		entry_date.bind("<Double-1>", lambda event="eiei", entry=entry_date, t="วันจดทะเบียนรถ" : self.On_date_click4(event,t, entry))

		self.finance_place = ttk.Combobox(
			self.frame4,
			state="readonly",
			values=["ศรีสวัสดิ์", "สมหวัง"], font=self.myFont
		)
		self.finance_place.grid(row=2,column=1,padx=5,pady=5)
		comb_label = tk.Label( self.frame4 , text="ที่ทำไฟแนนซ์", font=self.myFont)
		comb_label.grid(row = 2, column = 0, padx = 5, pady = 5)
		self.labels["ที่ทำไฟแนนซ์"] = self.finance_place
		#--------------------------------------------------------------	
		self.frame5 = Frame(self)
		self.frame5.grid(row= 3, column=1, padx=5, pady=5,sticky='ns')	
		button1 = tk.Button(self.frame5, text ="บันทึก/แก้ไข", font=self.myFont,
							command = self.save_data)
		button1.grid(row = 1, column = 0, padx = 10, pady = 10)
		button2 = tk.Button(self.frame5, text ="หน้าหลัก", font=self.myFont,
							command = lambda : controller.show_frame(startpage))
		button2.grid(row = 1, column = 1, padx = 10, pady = 10)
	def display_selection(self):
		selection = self.combo.get()
		##print(selection)
	def save_data(self):
		self.db_labels = ["car_no","date_buy","car_price","brand_color","car_year","sell_date","client_name",
			"Tel","deposit","finance","pay_down","remain_down","pay_down_date","fee","oil_price",
			"na","transfer_book_price","repair_price","driver_price","engine_oil_price","other_price",
			"state","car_regist_date","finance_place"]
		self.ui_labels = ["ทะเบียนรถ","วันที่ซื้อรถ","ราคารถ","ยี่ห้อ/สีรถ","ปีรถ",
		"วันขายรถ","ชื่อผู้ซื้อ","เบอร์โทร","มัดจำ","ไฟแนนซ์","จ่ายดาว","ค้างดาว","วันนัดจ่ายค้าง",
		"ค่าพรบ.","ค่าน้ำมัน","ค่าจ้างนา","โอนเล่ม","ค่าซ่อม","ค่าคนขับ","น้ำมันเครื่อง","ค่าทำเรื่อง/อื่นๆ",
		"สถานะ","วันจดทะเบียนรถ","ที่ทำไฟแนนซ์"]
		self.db_labels = {self.ui_labels[i]:self.db_labels[i] for i in range(len(self.ui_labels))}

		# db_labels_inv = {db_labels[i]:ui_labels[i] for i in range(len(ui_labels))}
		# self.ui_values = {self.db_labels[i]:self.labels[i].get() for i in self.labels}
		self.ui_values = {}
		# date_list = ["วันที่ซื้อรถ","วันขายรถ",	"วันจดทะเบียนรถ", "วันนัดจ่ายค้าง"]
		data_check = False
		for i in self.labels:
			if i=="ราคารถ" or i=="":
				try:
					checkdtype = int(self.labels[i].get())
					data_check = True
				except Exception as e:
					##print('///////',e)
					self.labels[i].configure(highlightbackground="red", highlightcolor="red")
					self.labels[i].delete(0, tk.END)
					self.labels[i].insert(0, "need number")
		if data_check:
			date_list = ["วันที่ซื้อรถ","วันขายรถ",	"วันจดทะเบียนรถ", "วันนัดจ่ายค้าง"]
			for i in self.labels:
				try:
					if i in date_list:
						self.ui_values[self.db_labels[i]] = self.labels[i].get_date()
					else:
						if i=="ราคารถ":
							try:
								self.ui_values[self.db_labels[i]] = int(self.labels[i].get())
							except Exception as e:
								# #print('///////',e)
								self.labels[i].configure(highlightbackground="red", highlightcolor="red")
								self.labels[i].delete(0, tk.END)
								self.labels[i].insert(0, "need number")
						else:
							# #print('iiii',i)
							self.ui_values[self.db_labels[i]] = self.labels[i].get()
				except Exception as e:
					self.ui_values[self.db_labels[i]] = ""
					#print('***********',self.labels[i],e)
			# #print(ui_values)
			command1 = []
			command2 = []
			for k,v in self.ui_values.items():
				# #print(k,v)
				try:
					command1.append(k)
					if str(v).strip() == "": command2.append("NULL")
					else: command2.append('''"{}"'''.format(v))
				except: 
					command1.append(k)
					command2.append('''"{}"'''.format(v))
			save_command = """INSERT INTO carinfo({}) VALUES({});""".format(", ".join(command1),", ".join(command2))
			# #print(save_command, command1, command2, '---------',self.ui_values)
			#print('----',save_command,len(command1),len(command2))
			# #print('-----',len(self.labels))
			# for i in self.ui_labels:
			# 	if i not in self.labels:
			# 		#print(',,,,,,,',i)
			# 	else:
			# 		#print('////',i)
			#print("len self.labelsssssssssssss", len(self.labels))
			for i in self.labels:
				try: # for entry labels object
					if i in ["ปีรถ","สถานะ","ที่ทำไฟแนนซ์"]: self.labels[i].set('')						
					self.labels[i].delete(0, tk.END)
				except: # for calendar
					if self.labels_other[i]!="": self.labels_other[i].delete(0, tk.END)
				
			self.controller.mycursor.execute(save_command)
			self.controller.frames[startpage].query2df()
			self.controller.show_frame(startpage)
	def On_date_click1(self,event, t, entry):
		self.myFont = font.Font(family='Helvetica',size=25)
		win = tk.Tk()
		self.labels[t] = Calendar(win ,selectmode='day', font=self.myFont , date_pattern="yy-mm-dd")
		self.labels[t].grid(row=0, column=0, padx = 5, pady = 5)
		save_date_but = tk.Button(win, text="save", command = lambda win=win ,entry=entry, t=t: self.save_date_but(win,entry,t), font=self.myFont)
		save_date_but.grid(row=1, column=0, padx=10, pady=10)
	def On_date_click2(self,event, t, entry):
		self.myFont = font.Font(family='Helvetica',size=25)
		win = tk.Tk()
		self.labels[t] = Calendar(win ,selectmode='day', font=self.myFont ,date_pattern="yy-mm-dd")
		self.labels[t].grid(row=0, column=0, padx = 5, pady = 5)
		save_date_but = tk.Button(win, text="save", command = lambda win=win ,entry=entry, t=t: self.save_date_but(win,entry,t), font=self.myFont)
		save_date_but.grid(row=1, column=0, padx=10, pady=10)
	def On_date_click3(self,event, t, entry):
		self.myFont = font.Font(family='Helvetica',size=25)
		win = tk.Tk()
		self.labels[t] = Calendar(win ,selectmode='day', font=self.myFont, date_pattern="yy-mm-dd")
		self.labels[t].grid(row=0, column=0, padx = 5, pady = 5)
		save_date_but = tk.Button(win, text="save", command = lambda win=win ,entry=entry, t=t: self.save_date_but(win,entry,t), font=self.myFont)
		save_date_but.grid(row=1, column=0, padx=10, pady=10)
	def On_date_click4(self,event, t, entry):
		self.myFont = font.Font(family='Helvetica',size=25)
		win = tk.Tk()
		self.labels[t] = Calendar(win ,selectmode='day', font=self.myFont , date_pattern="yy-mm-dd")
		self.labels[t].grid(row=0, column=0, padx = 5, pady = 5)
		save_date_but = tk.Button(win, text="save", command = lambda win=win ,entry=entry, t=t: self.save_date_but(win,entry,t), font=self.myFont)
		save_date_but.grid(row=1, column=0, padx=10, pady=10)
	def save_date_but(self, win,entry, t):
		win.destroy()
		entry.delete(0, tk.END)
		entry.insert(-1, self.labels[t].get_date())

class detail_page(Frame):
	def __init__(self, row_select, parent, controller):	
		self.myFont = font.Font(family='Helvetica',size=30)
		#  ------------------------------------------createwindow--------------------
		# self.window = tk.Tk.__init__(self, parent)
		self.window = parent
		# Frame.__init__(self, parent)
		# self.window = tk.Tk()
		# self.window.title("detail")
		self.main_frame = Frame(self.window)
		self.main_frame.grid(column=0, row=0)
		#---------------------------------------------------------------------------
		self.row_select = row_select
		db_labels = ["car_no","date_buy","car_price","brand_color","car_year","sell_date","client_name",
			"Tel","deposit","finance","pay_down","remain_down","pay_down_date","fee","oil_price",
			"na","transfer_book_price","repair_price","driver_price","engine_oil_price","other_price",
			"state","car_regist_date","finance_place"]
		ui_labels = ["ทะเบียนรถ","วันที่ซื้อรถ","ราคารถ","ยี่ห้อ/สีรถ","ปีรถ",
		"วันขายรถ","ชื่อผู้ซื้อ","เบอร์โทร","มัดจำ","ไฟแนนซ์","จ่ายดาว","ค้างดาว","วันนัดจ่ายค้าง",
		"ค่าพรบ.","ค่าน้ำมัน","ค่าจ้างนา","โอนเล่ม","ค่าซ่อม","ค่าคนขับ","น้ำมันเครื่อง","ค่าทำเรื่อง/อื่นๆ",
		"สถานะ","วันจดทะเบียนรถ","ที่ทำไฟแนนซ์"]
		self.db_labels = {ui_labels[i]:db_labels[i] for i in range(len(ui_labels))}
		self.controller = controller
		# self.row_select = self.controller.frames[startpage].row_select
		#  ------------------------------------------query sql--------------------
		query = """select * from carinfo where car_no='{}'""".format(self.row_select)
		self.controller.mycursor.execute(query)
		myresult = self.controller.mycursor.fetchall()
		columns = [col[0] for col in controller.mycursor.description]
		self.carinfo_df = pd.DataFrame(myresult, columns=columns)
		fillcol = ["ราคารถ","มัดจำ","ไฟแนนซ์","จ่ายดาว","ค้างดาว","ค่าพรบ.",
		  "ค่าน้ำมัน","ค่าจ้างนา","โอนเล่ม","ค่าซ่อม","ค่าคนขับ","น้ำมันเครื่อง","ค่าทำเรื่อง/อื่นๆ"]
		fillcol = [self.db_labels[i] for i in fillcol]
		self.carinfo_df[fillcol] = self.carinfo_df[fillcol].fillna(0)
		# self.carinfo_df.to_csv('test2.csv')
		# ------------------------------------------frame1--------------------
		self.frame1 = Frame(self.main_frame,highlightbackground="black", highlightthickness=0.8)
		self.frame1.grid(row= 0, column=0, padx=5, pady=5, sticky='ns')

		all_labels1 = ["ทะเบียนรถ","วันที่ซื้อรถ","ราคารถ","ยี่ห้อ/สีรถ","ปีรถ"]
		self.labels = {} #for entry
		self.labels_ = {} # for note query
		for i,t in enumerate(all_labels1):
			if t!="วันที่ซื้อรถ" and t!="ปีรถ":
				label_ = tk.Label( self.frame1 , text=t, font=self.myFont)
				label_.grid(row = i, column = 0, padx = 5, pady = 5)
				self.labels[t] = tk.Entry(self.frame1, font=self.myFont)
				self.labels[t].grid(row=i, column=1, padx = 5, pady = 5)
				self.labels[t].delete(0, tk.END)
				self.labels[t].insert(0, str(self.carinfo_df[self.db_labels[t]][0]))
				self.labels_[t] = str(self.carinfo_df[self.db_labels[t]][0])
			else:
				if t == "วันที่ซื้อรถ":
					label_ = tk.Label( self.frame1 , text=t, font=self.myFont)
					label_.grid(row = i, column = 0, padx = 5, pady = 5)
					entry_date = tk.Entry(self.frame1, font=self.myFont)
					entry_date.grid(row=i, column=1, padx = 5, pady = 5)
					self.labels[t] = ""
					entry_date.bind("<Double-1>", lambda event="eiei", entry=entry_date, t=t : self.On_date_click1(event,t, entry))
					entry_date.delete(0, tk.END)
					entry_date.insert(0, str(self.carinfo_df[self.db_labels[t]][0]))
					self.labels_[t] = str(self.carinfo_df[self.db_labels[t]][0])
				else:
					self.year_car_label = ["60","61","62","63","64","65","66"]
					self.year_car = ttk.Combobox(
						self.frame1,
						state="readonly",
						values=self.year_car_label, font=self.myFont
					)
					self.year_car.grid(row=4,column=1,padx=5,pady=5)
					self.year_car_label2 = {j:i for i,j in enumerate(self.year_car_label)}
					if not (self.carinfo_df["car_year"].isnull()[0]):
						#print("ปีรถถถถถถถถถถถถถ",self.year_car_label2[self.carinfo_df["car_year"].astype("string")[0]])
						self.year_car.current(self.year_car_label2[self.carinfo_df["car_year"].astype("string")[0]])
						self.labels_["ปีรถ"] = self.carinfo_df["car_year"].astype("string")[0]
					year_car_label = tk.Label( self.frame1 , text="ปีรถ", font=self.myFont)
					year_car_label.grid(row = 4, column = 0, padx = 5, pady = 5)
					self.labels["ปีรถ"] = self.year_car

		#--------------------------------------------------------------

		#------------------------------------------frame2--------------------
		self.frame2 = Frame(self.main_frame,highlightbackground="black", highlightthickness=0.8)
		self.frame2.grid(row= 1, column=0, padx=5, pady=5, sticky='ns',rowspan=3)
		all_labels2 = ["วันขายรถ","ชื่อผู้ซื้อ","เบอร์โทร","มัดจำ",
		 "ไฟแนนซ์","จ่ายดาว","ค้างดาว","วันนัดจ่ายค้าง"]
		for i,t in enumerate(all_labels2):
			if t!="วันขายรถ" and t!="วันนัดจ่ายค้าง":
				label_ = tk.Label( self.frame2 , text=t, font=self.myFont)
				label_.grid(row = i, column = 0, padx = 5, pady = 5)
				self.labels[t] = tk.Entry(self.frame2, font=self.myFont)
				self.labels[t].grid(row=i, column=1, padx = 5, pady = 5)
				self.labels[t].delete(0, tk.END)
				self.labels[t].insert(0, str(self.carinfo_df[self.db_labels[t]][0]))
				self.labels_[t] = str(self.carinfo_df[self.db_labels[t]][0])
			else:
				pass
				# label_ = tk.Label( self.frame2 , text=t, font=self.myFont)
				# label_.grid(row = i, column = 0, padx = 5, pady = 5)
				# entry_date = tk.Entry(self.frame2, font=self.myFont, textvariable="eiei")
				# entry_date.grid(row=i, column=1, padx = 5, pady = 5)
				# entry_date.bind("<ButtonRelease-1>", lambda t=t, entry=entry_date: self.On_date_click2(t,entry))
				# entry_date.set(self.labels[i].get_date())
				# self.labels[t] = DateEntry(self.frame2,selectmode='day', font=self.myFont)
				# self.labels[t].grid(row=i, column=1, padx = 5, pady = 5)
		label_ = tk.Label( self.frame2 , text="วันขายรถ", font=self.myFont)
		label_.grid(row = 0, column = 0, padx = 5, pady = 5)
		entry_date = tk.Entry(self.frame2, font=self.myFont)
		entry_date.grid(row=0, column=1, padx = 5, pady = 5)
		self.labels["วันขายรถ"] = ""
		entry_date.bind("<Double-1>", lambda event="eiei", entry=entry_date, t="วันขายรถ" : self.On_date_click2(event,t, entry))
		entry_date.delete(0, tk.END)
		entry_date.insert(0, str(self.carinfo_df[self.db_labels["วันขายรถ"]][0]))
		self.labels_["วันขายรถ"] = str(self.carinfo_df[self.db_labels["วันขายรถ"]][0])

		label_ = tk.Label( self.frame2 , text="วันนัดจ่ายค้าง", font=self.myFont)
		label_.grid(row = 7, column = 0, padx = 5, pady = 5)
		entry_date = tk.Entry(self.frame2, font=self.myFont)
		entry_date.grid(row=7, column=1, padx = 5, pady = 5)
		self.labels["วันนัดจ่ายค้าง"] = ""
		entry_date.bind("<Double-1>", lambda event="eiei", entry=entry_date, t="วันนัดจ่ายค้าง" : self.On_date_click3(event,t, entry))
		entry_date.delete(0, tk.END)
		entry_date.insert(0, str(self.carinfo_df[self.db_labels["วันนัดจ่ายค้าง"]][0]))
		self.labels_["วันนัดจ่ายค้าง"] = str(self.carinfo_df[self.db_labels["วันนัดจ่ายค้าง"]][0])
		#------------------------------------------frame3--------------------
		self.frame3 = Frame(self.main_frame,highlightbackground="black", highlightthickness=0.8)
		self.frame3.grid(row= 0, column=1, padx=5, pady=5,sticky='ns',rowspan=2)
		
		all_labels2 = ["ค่าพรบ.","ค่าน้ำมัน","ค่าจ้างนา","โอนเล่ม","ค่าซ่อม",
		 "ค่าคนขับ","น้ำมันเครื่อง","ค่าทำเรื่อง/อื่นๆ"]
		for i,t in enumerate(all_labels2):
			label_ = tk.Label( self.frame3 , text=t, font=self.myFont)
			label_.grid(row = i, column = 0, padx = 5, pady = 5)
			self.labels[t] = tk.Entry(self.frame3)
			self.labels[t].grid(row=i, column=1, padx = 5, pady = 5)
			self.labels[t].delete(0, tk.END)
			self.labels[t].insert(0, str(self.carinfo_df[self.db_labels[t]][0]))
			self.labels_[t] = str(self.carinfo_df[self.db_labels[t]][0])
		#---------------------------------------------------------------
		self.frame4 = Frame(self.main_frame,highlightbackground="black", highlightthickness=0.8)
		self.frame4.grid(row= 2, column=1, padx=5, pady=5,sticky='n')
		
		self.state_label = ["รอขาย", "รอเข้าขนส่ง", "ค้างขนส่ง", "รอเข้าแนนซ์","เข้าแนนซ์"]
		self.state = ttk.Combobox(
			self.frame4,
			state="readonly",
			values=self.state_label, font=self.myFont
		)
		self.state.grid(row=0,column=1,padx=5,pady=5)
		self.state_label2 = {j:i for i,j in enumerate(self.state_label)}
		if not (self.carinfo_df["state"].isnull()[0]):
			self.state.current(self.state_label2[self.carinfo_df["state"].astype("string")[0]])
			self.labels_["สถานะ"] = self.carinfo_df["state"].astype("string")[0]
		comb_label = tk.Label( self.frame4 , text="สถานะ", font=self.myFont)
		comb_label.grid(row = 0, column = 0, padx = 5, pady = 5)
		self.labels["สถานะ"] = self.state

		label_ = tk.Label( self.frame4 , text="วันจดทะเบียนรถ", font=self.myFont)
		label_.grid(row = 1, column = 0, padx = 5, pady = 5)
		entry_date = tk.Entry(self.frame4, font=self.myFont)
		entry_date.grid(row=1, column=1, padx = 5, pady = 5)
		self.labels["วันจดทะเบียนรถ"] = ""
		entry_date.bind("<Double-1>", lambda event="eiei", entry=entry_date, t="วันจดทะเบียนรถ" : self.On_date_click4(event,t, entry))
		entry_date.delete(0, tk.END)
		entry_date.insert(0, str(self.carinfo_df[self.db_labels["วันจดทะเบียนรถ"]][0]))
		self.labels_["วันจดทะเบียนรถ"] = str(self.carinfo_df[self.db_labels["วันจดทะเบียนรถ"]][0])

		self.finance_place_label = ["ศรีสวัสดิ์", "สมหวัง"]
		self.finance_place = ttk.Combobox(
			self.frame4,
			state="readonly",
			values=self.finance_place_label, font=self.myFont
		)
		self.finance_place.grid(row=2,column=1,padx=5,pady=5)
		self.finance_place_label2 = {j:i for i,j in enumerate(self.finance_place_label)}
		if not (self.carinfo_df["finance_place"].isnull()[0]):
			self.finance_place.current(self.finance_place_label2[self.carinfo_df["finance_place"].astype("string")[0]])
			self.labels_["ที่ทำไฟแนนซ์"] = self.carinfo_df["finance_place"].astype("string")[0]
		comb_label = tk.Label( self.frame4 , text="ที่ทำไฟแนนซ์", font=self.myFont)
		comb_label.grid(row = 2, column = 0, padx = 5, pady = 5)
		self.labels["ที่ทำไฟแนนซ์"] = self.finance_place
		# self.finance_place = ttk.Combobox(
		# 	self.frame4,
		# 	state="readonly",
		# 	values=["ศรีสวัสดิ์", "สมหวัง"], font=self.myFont
		# )
		# self.finance_place.grid(row=2,column=1,padx=5,pady=5)
		# self.finance_place.current(2)
		# comb_label = tk.Label( self.frame4 , text="ที่ทำไฟแนนซ์", font=self.myFont)
		# comb_label.grid(row = 2, column = 2, padx = 5, pady = 5)
		# self.labels["ที่ทำไฟแนนซ์"] = self.finance_place
		#--------------------------------------------------------------	
		self.frame5 = Frame(self.main_frame)
		self.frame5.grid(row= 3, column=1, padx=5, pady=5,sticky='ns')	
		button1 = ttk.Button(self.frame5, text ="บันทึก/แก้ไข",
							command = self.save_data)
		button1.grid(row = 1, column = 0, padx = 10, pady = 10)
		button2 = ttk.Button(self.frame5, text ="ออก",
							command = lambda : self.window.destroy())
		button2.grid(row = 1, column = 1, padx = 10, pady = 10)
		button2 = ttk.Button(self.frame5, text ="ลบข้อมูล",
							command = lambda : self.delete())
		button2.grid(row = 1, column = 2, padx = 10, pady = 10)
	def delete(self):
		# self.controller.frames[startpage].query2df()
		# self.controller.show_frame(startpage)
		self.controller.frames[startpage].delete()
		self.window.destroy()
		# #print('delete...',self.row_select)
		# self.controller.mycursor.execute("""DELETE FROM carinfo WHERE car_no="{}";""".format(self.row_select))
		# self.query2df()
	def display_selection(self):
		selection = self.combo.get()
		#print(selection)
	def save_data(self):
		# #print(self.labels["ทะเบียนรถ"].get())
		self.db_labels = ["car_no","date_buy","car_price","brand_color","car_year","sell_date","client_name",
			"Tel","deposit","finance","pay_down","remain_down","pay_down_date","fee","oil_price",
			"na","transfer_book_price","repair_price","driver_price","engine_oil_price","other_price",
			"state","car_regist_date","finance_place"]
		self.ui_labels = ["ทะเบียนรถ","วันที่ซื้อรถ","ราคารถ","ยี่ห้อ/สีรถ","ปีรถ",
		"วันขายรถ","ชื่อผู้ซื้อ","เบอร์โทร","มัดจำ","ไฟแนนซ์","จ่ายดาว","ค้างดาว","วันนัดจ่ายค้าง",
		"ค่าพรบ.","ค่าน้ำมัน","ค่าจ้างนา","โอนเล่ม","ค่าซ่อม","ค่าคนขับ","น้ำมันเครื่อง","ค่าทำเรื่อง/อื่นๆ",
		"สถานะ","วันจดทะเบียนรถ","ที่ทำไฟแนนซ์"]
		self.db_labels = {self.ui_labels[i]:self.db_labels[i] for i in range(len(self.ui_labels))}
		# self.ui_values = {self.db_labels[i]:self.labels[i].get() for i in self.labels}
		self.ui_values = {}
		data_check = False
		# #print("---self.labels_-----",self.labels_)
		for i in self.labels_:
			if i=="ราคารถ" or i=="":
				try:
					checkdtype = int(self.labels[i].get())
					# checkdtype = int(self.labels_[i])
					data_check = True
				except Exception as e:
					#print('///////',e)
					self.labels_[i].configure(highlightbackground="red", highlightcolor="red")
					self.labels_[i].delete(0, tk.END)
					self.labels_[i].insert(0, "need number")
		if data_check:
			date_list = ["วันที่ซื้อรถ","วันขายรถ",	"วันจดทะเบียนรถ", "วันนัดจ่ายค้าง"]
			for i in self.labels:
				try:
					if i in date_list:
						# self.ui_values[self.db_labels[i]] = self.labels_[i].get_date()
						try: 
							#print("00000000000000000",self.labels[i].get_date())
							self.ui_values[self.db_labels[i]] = self.labels[i].get_date()
						except: 
							self.ui_values[self.db_labels[i]] = self.labels_[i]
							# if self.labels_[i] !=None: 
							# 	#print("11111111111111111",self.labels_[i])
							# 	self.ui_values[self.db_labels[i]] = self.labels_[i]
							# else: self.ui_values[self.db_labels[i]] = "NULL"

					else:
						if i=="ราคารถ":
							try:
								# self.ui_values[self.db_labels[i]] = int(self.labels[i].get())
								self.ui_values[self.db_labels[i]] = int(self.labels_[i])
							except Exception as e:
								# #print('///////',e)
								self.labels_[i].configure(highlightbackground="red", highlightcolor="red")
								self.labels_[i].delete(0, tk.END)
								self.labels_[i].insert(0, "need number")
						else:
							self.ui_values[self.db_labels[i]] = self.labels[i].get()
							# self.ui_values[self.db_labels[i]] = self.labels_[i]
				except Exception as e:
					self.ui_values[self.db_labels[i]] = ""
					#print('***********',i,e)
			#print("uivaluessssssssssssssssss",self.ui_values)
			command1 = []
			command2 = []
			for k,v in self.ui_values.items():
				# #print(k,v)
				try:
					command1.append(k)
					if str(v).strip() == "" or str(v).strip()=="None": command2.append("NULL")
					else: command2.append('''"{}"'''.format(v))
				except: 
					command1.append(k)
					command2.append('''"{}"'''.format(v))
			delete_command = """DELETE FROM carinfo WHERE car_no='{}'""".format(self.ui_values["car_no"])
			self.controller.mycursor.execute(delete_command)

			save_command = """INSERT INTO carinfo({}) VALUES({});""".format(", ".join(command1),", ".join(command2))
			#print('----------------', save_command, len(command1), len(command2))
			self.controller.mycursor.execute(save_command)
			self.controller.frames[startpage].query2df()
			self.controller.show_frame(startpage)
			self.window.destroy()
	def On_date_click1(self,event, t, entry):
		self.myFont = font.Font(family='Helvetica',size=25)
		win = tk.Tk()
		self.labels[t] = Calendar(win ,selectmode='day', font=self.myFont , date_pattern="yy-mm-dd")
		self.labels[t].grid(row=0, column=0, padx = 5, pady = 5)
		save_date_but = tk.Button(win, text="save", command = lambda win=win ,entry=entry, t=t: self.save_date_but(win,entry,t), font=self.myFont)
		save_date_but.grid(row=1, column=0, padx=10, pady=10)
	def On_date_click2(self,event, t, entry):
		self.myFont = font.Font(family='Helvetica',size=25)
		win = tk.Tk()
		self.labels[t] = Calendar(win ,selectmode='day', font=self.myFont ,date_pattern="yy-mm-dd")
		self.labels[t].grid(row=0, column=0, padx = 5, pady = 5)
		save_date_but = tk.Button(win, text="save", command = lambda win=win ,entry=entry, t=t: self.save_date_but(win,entry,t), font=self.myFont)
		save_date_but.grid(row=1, column=0, padx=10, pady=10)
	def On_date_click3(self,event, t, entry):
		self.myFont = font.Font(family='Helvetica',size=25)
		win = tk.Tk()
		self.labels[t] = Calendar(win ,selectmode='day', font=self.myFont, date_pattern="yy-mm-dd")
		self.labels[t].grid(row=0, column=0, padx = 5, pady = 5)
		save_date_but = tk.Button(win, text="save", command = lambda win=win ,entry=entry, t=t: self.save_date_but(win,entry,t), font=self.myFont)
		save_date_but.grid(row=1, column=0, padx=10, pady=10)
	def On_date_click4(self,event, t, entry):
		self.myFont = font.Font(family='Helvetica',size=25)
		win = tk.Tk()
		self.labels[t] = Calendar(win ,selectmode='day', font=self.myFont , date_pattern="yy-mm-dd")
		self.labels[t].grid(row=0, column=0, padx = 5, pady = 5)
		save_date_but = tk.Button(win, text="save", command = lambda win=win ,entry=entry, t=t: self.save_date_but(win,entry,t), font=self.myFont)
		save_date_but.grid(row=1, column=0, padx=10, pady=10)
	def save_date_but(self, win,entry, t):
		win.destroy()
		entry.delete(0, tk.END)
		entry.insert(-1, self.labels[t].get_date())