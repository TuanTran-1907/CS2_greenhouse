# def create_widgets(self):
    #     Label(self, text="BẢNG ĐIỀU KHIỂN", font=("Arial", 18, "bold")).grid(row=0, column=0, columnspan=3, pady=8)
    #     self.label_temp = Label(self, text="Nhiệt độ: -- °C", font=("Arial", 12))
    #     self.label_hum = Label(self, text="Độ ẩm: -- %", font=("Arial", 12))
    #     self.label_temp.grid(row=1, column=0, padx=8,pady=6)
    #     self.label_hum.grid(row=1, column=1, padx=8,pady=6)

    #     Label(self, text="CHỌN CÂY:").grid(row=2, column=0 ,pady=6)
    #     Label(self, text="HẸN GIỜ TƯỚI: ").grid(row=6, column=0,pady=6)
    #     self.combo = ttk.Combobox(self,values=list(cay_list.keys()))
    #     self.combo.grid(row=2,column=1,pady=6)
    #     self.entry_time = Entry(self)
    #     self.entry_time.grid(row=6,column=1,pady=6)
    #     self.scaleFan = Scale(self, from_=100, to=0, orient='vertical')

    #     Button(self, text="Gửi LED", command=self.send_led).grid(row=3, column=0, pady=6)
    #     Button(self, text="Tắt LED", command=self.turn_off).grid(row=3, column=1, pady=6)
    #     Button(self, text="Blink", command=self.blink_led).grid(row=3, column=2, pady=6)

    #     Button(self, text="Đọc DHT", command=self.read_DHT).grid(row=4, column=0, pady=6)
    #     Button(self, text="Độ ẩm đất", command=self.read_soil).grid(row=4, column=1, pady=6)
    #     Button(self, text="Quạt", command= self.turn_fan).grid(row= 4, column=2, pady=6)
    #     Button(self, text="Off quạt", command= self.off_fan).grid(row= 4, column=3, pady=6)

    # def send_command(self, cmd: bytes):
    #     if not arduino:
    #         messagebox.showerror("Lỗi", "Không kết nối Arduino.")
    #         return
    #     try:
    #         arduino.write(cmd)
    #     except Exception as e:
    #         messagebox.showerror("Lỗi", f"Gửi lệnh thất bại: {e}")

    # def send_led(self):
    #     cay = self.combo.get()
    #     color = cay_list.get(cay, 'r')
    #     self.send_command(f"3{color}".encode())

    # def turn_off(self):
    #     self.send_command(b'4')

    # def blink_led(self):
    #     self.send_command(b'6')

    # def rem_thuan(self):
    #     self.send_command(b'7')

    # def rem_nguoc(self):
    #     self.send_command(b'8')

    # def rem_dung(self):
    #     self.send_command(b'9')

    # def read_DHT(self):
    #     if not arduino:
    #         messagebox.showerror("Lỗi", "Không kết nối Arduino.")
    #         return
    #     try:
    #         arduino.write(b'5')
    #         self.after(300, self.update_DHT)
    #     except Exception as e:
    #         print("Lỗi gửi lệnh DHT:", e)

    # def update_DHT(self):
    #     try:
    #         line = arduino.readline().decode().strip()
    #         if "," in line:
    #             t, h = line.split(",", 1)
    #             self.label_temp.config(text=f"Nhiệt độ: {t} °C")
    #             self.label_hum.config(text=f"Độ ẩm: {h} %")
    #         else:
    #             # nếu rỗng hoặc khác định dạng, không cập nhật
    #             print("Dòng nhận được (DHT):", repr(line))
    #     except Exception as e:
    #         print("Lỗi đọc DHT:", e)

    # def read_soil(self):
    #     if not arduino:
    #         messagebox.showerror("Lỗi", "Không kết nối Arduino.")
    #         return
    #     try:
    #         arduino.write(b'1')
    #         self.after(300, self.update_soil)
    #     except Exception as e:
    #         print("Lỗi gửi lệnh soil:", e)

    # def update_soil(self):
    #     try:
    #         line = arduino.readline().decode().strip()
    #         if ":" in line:
    #             parts = line.split(":", 1)
    #             value = parts[1].strip()
    #             self.label_hum.config(text=f"Độ ẩm đất: {value}")
    #         else:
    #             print("Dòng nhận được (Soil):", repr(line))
    #     except Exception as e:
    #         print("Lỗi đọc Soil:", e)

    # # def set_alarm(self,alarm_time):
    # #     alarm_time = self.entry_time.get()
    # #     running = True

    # #     while running:
    # #         current_time = datetime.datetime.now().strftime("%H:%M:%S")
    # #         if current_time == alarm_time:
    # #             print("Da tuoi nuoc")

        
    # #         time.sleep(1)
    # def set_alarm(self):
    #     alarm_time = self.entry_time.get().strip()
    #     self.check_alarm(alarm_time)

    # def check_alarm(self, alarm_time):
    #     current_time = datetime.datetime.now().strftime("%H:%M:%S")
    #     if current_time == alarm_time:
    #         print("Đã tưới nước!")
    #         self.send_command(b'7')
    #         return
    #     self.after(1000, lambda: self.check_alarm(alarm_time))

    # def turn_fan(self):
    #     self.scaleFan.grid(row= 5, column=2, pady=6)

    # def off_fan(self):
    #     self.scaleFan.grid_remove()

    # def logout(self):
    #     # Quay lại màn hình login
    #     self.master.show_login_frame()




# class addPass(Toplevel):
#     def __init__(self, master):
#         super().__init__(master)
#         self.title("Đăng ký private pass")
#         self.geometry("360x220")
#         self.resizable(True, True)
#         self.addP_widgets()
#         # đặt focus vào cửa sổ đăng ký
#         self.transient(master)
#         self.grab_set()

#     def addP_widgets(self):
#         self.askEntry = Entry(self)
#         self.askEntry.pack(pady=20,anchor='center')
#         Button(self,text="Confirm",command=self.confirm).pack()

#     def confirm(self):
#         pp = self.askEntry.get()
#         if not pp:
#             messagebox.showwarning("canh cao","Không để trống")
#             return
#         if any(c in invalid_char for c in pp) or " " in pp:
#             messagebox.showerror("Cảnh cáo","Không sài ký tự đặc biệt")
#             return
#         success = save_pass(pp)
#         if not success:
#             messagebox.showerror("Cảnh cáo","Mật khẩu không hợp lệ")
#         else:
#             messagebox.showinfo("Thành công")
#             self.destroy()


# class Users(Frame):
#     def __init__(self,master,show_arduino_frame):
#         super().__init__(master)
#         self.master = master
#         self.show_arduino_frame = show_arduino_frame
#         self.userImages = PhotoImage(file="users.png")
#         self.image = PhotoImage(file='loginapp.png')
#         self.x = IntVar()
#         # self.user_buttons = []
#         self.users_widgets()

#     def users_widgets(self):
#         bg = Label(self,background="#250c6a",image=self.image)
#         bg.place(x=0,y=0)
#         bg.lower()
#         self.frm_1 = Frame(self,bg="#250c6a")
#         self.frm_1.pack(padx= 20,pady=(20,0))
#         self.frm_2 = Frame(self,bg="#250c6a")
#         self.frm_2.pack(pady=10, padx=10)
#         self.title1=Button(self.frm_1,text= "Xin Chào, Ai Đang Sử Dụng?",fg="white",disabledforeground="white",bg="#f36bc5",font=("Arial",30,'bold'),state='disable')
#         self.title1.grid(row=0,column=0)
#         for i in range(len(users)):
#             radio = Button(self.frm_2,
#                                 text=users[i],
#                                 # variable=self.x,
#                                 # value=i,
#                                 image= self.userImages,
#                                 compound='top',
#                                 font=("Arial",16),
#                                 fg="black",
#                                 # indicatoron=0,
#                                 background="white",
#                                 activebackground="#f36bc5",
#                                 command= lambda u=users[i]: self.checkb_openApp(u)
#                                 )
#             radio.grid(row= 1, column=i,padx=(5,0))
#             # self.user_buttons.append(radio)

#         self.frm_h = Frame(self)
#         self.frm_h.place(x=90,y=120)

#     def Hola(self,name):
#         self.frm_1.pack_forget()
#         self.frm_2.pack_forget()
#         Label(self.frm_h,text=f"Chào mừng quay lại {name}",fg="white",bg="#250c6a",font=("Pacifico",30,'italic')).pack()

#     # check private pass trc khi vao:
#     def checkb_openApp(self, name):
#         accounts = load_accounts()
#         user_acc = next((a for a in accounts if a["user"] == name), None)

#         if not user_acc:
#             mess = messagebox.askyesno(
#                 "Người dùng mới",
#                 f"Người dùng {name} chưa được đăng ký trong hệ thống!\nBạn có muốn tạo tài khoản mới không?"
#             )
#             if mess:
#                 addPass(self, name)
#             else:
#                 self.openApp(name)
#             return

#         # Nếu user đã có private pass → hỏi mật khẩu
#         if user_acc.get("pripass"):
#             Askpass(self, name, lambda: self.openApp(name))
#         # else:
#         #     # Nếu chưa có → hỏi muốn tạo không
#         #     mess = messagebox.askyesno(
#         #         "Thông báo",
#         #         f"{name} chưa có mật khẩu riêng. Bạn có muốn tạo không?"
#         #     )
#         #     if mess:
#         #         addPass(self, name)
#         #     else:
#         #         self.openApp(name)



#     def openApp(self,name):
#         self.Hola(name)
#         self.after(4000,self.show_arduino_frame)

# class Askpass(Toplevel):
#     def __init__(self, master, openApp):
#         super().__init__(master)
#         self.title("Pass")
#         self.geometry("360x220")
#         self.resizable(False, False)
#         self.ask_widgets()
#         self.openApp = openApp
#         # đặt focus vào cửa sổ đăng ký
#         self.transient(master)
#         self.grab_set()

#     def ask_widgets(self):
#         Label(self,text="Enter Password",font=("Arial", 16, "bold")).pack(pady=15,anchor='center')
#         self.askEntry = Entry(self)
#         self.askEntry.pack()
#         Button(self,text="submit",font=("Arial", 16, "bold"),command=self.pass_in).pack()

#     def pass_in(self):
#         passw = self.askEntry.get().strip()
#         if check_ppass(passw):
#             self.destroy()
#             self.openApp()
#         else:
#             messagebox.showerror("Lỗi", "Sai username hoặc password.")
#             return