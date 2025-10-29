from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import serial
import serial.tools.list_ports
import json
import os
import time
import datetime

# Set up
BAUDRATE = 9600
invalid_char = "~`!@#$%^&*()/|{}[]\\.,/?':;"

users = ["Tuấn","Quân","Khang","Toàn","Dũng"]
colorwheel = ["#F00001","#03FF3A","#00B7FF","#4C00FF","white"]
time_format = "00:00:00"
num = "1234567890"

LOG_FILE = "taikhoan.json"
PPASS_FILE = "pripass.json"
DATA_FILE = "date.json"

def find_arduinoPort():
    ports = serial.tools.list_ports.comports()
    arduino_port = None

    for port in ports:
        if ("Arduino" in port.description) or ("CH340" in port.description) or ("USB Serial" in port.description):
            arduino_port = port.device
            break

    if arduino_port:
        try:
            arduino = serial.Serial(port=arduino_port, baudrate=BAUDRATE, timeout=1)
            time.sleep(2)
            print(f"Kết nối Arduino cổng: {arduino_port}")
            return arduino
        except Exception as e:
            print("Không tìm thấy cổng", e)
            return None
    else:
        print("Lỗi kết nối")
        return None


def load_accounts():
    if not os.path.exists(LOG_FILE):
        return []
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            else:
                return []
    except Exception:
        return []

def save_account(user: str, password: str) -> bool:
    accounts = load_accounts()
    for acc in accounts:
        if acc.get("user") == user:
            return False
    accounts.append({"user": user, "passw": password}) 
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(accounts, f, indent=4, ensure_ascii=False)
    return True

def save_private_pass(user: str, pripass: str) -> bool:
    accounts = load_accounts()
    for acc in accounts:
        if acc["user"] == user:
            acc["pripass"] = pripass
            with open(LOG_FILE, "w", encoding="utf-8") as f:
                json.dump(accounts, f, indent=4, ensure_ascii=False)
            return True
    return False

def load_pripass():
    if not os.path.exists(PPASS_FILE):
        return []
    try:
        with open(PPASS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    except Exception:
        pass
    return []

def save_pass(passw: str) -> bool:
    pripass = load_pripass()
    for pp in pripass:
        if pp.get("pripass") == passw:
            return False
    pripass.append({"pripass": passw})
    with open(PPASS_FILE, "w", encoding="utf-8") as f:
        json.dump(pripass, f, indent=4, ensure_ascii=False)
    return True

def check_ppass(passw: str) -> bool:
    pripass = load_pripass()
    # ppp = passw
    for pp in pripass:
        if pp.get("pripass") == passw:
            return True
    return False

def check_login(user: str, password: str) -> bool:
    accounts = load_accounts()
    hp = password
    for acc in accounts:
        if acc.get("user") == user and acc.get("passw") == hp:
            return True
    return False

def save_time(start_time):
    data = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []

    if start_time not in [item["start_time"] for item in data]:
        data.append({"start_time": start_time})

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_time():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []
    
#Log in
class LoginFrame(Frame):
    def __init__(self, master, show_users_frame):
        super().__init__(master)
        self.master = master
        self.show_users_frame = show_users_frame
        self.image = PhotoImage(file='loginapp.png')
        self.create_widgets()

    def create_widgets(self):
        Label(self,background="#250c6a",image=self.image).place(x=0,y=0)
        no_frame = Frame(self)
        no_frame.grid(row=0, column=0,pady=40,padx=300)
        l3b_frame = Frame(self,background="#250c6a")
        l3b_frame.grid(row=1, column=0,pady=20)
        b4l_frame = Frame(self,background="#250c6a")
        b4l_frame.grid(row=2, column=0,pady=6)
        Label(l3b_frame, text="Username:",bg="#250c6a",fg="white",font=("Montserrat Black",14 )).pack(side=LEFT)
        Label(b4l_frame, text="Password:",bg="#250c6a",fg="white",font=("Montserrat Black",14)).pack(side=LEFT)

        self.user_entry = Entry(l3b_frame,foreground='#4d29a0',font=("Montserrat Black", 12))
        self.pass_entry = Entry(b4l_frame,foreground="#f36bc5",show="*", font=("Montserrat Black", 12))
        self.user_entry.pack(side=LEFT)
        self.pass_entry.pack(side=LEFT)

        btn_frame = Frame(self,bg="#250c6a")
        btn_frame.grid(row=3, column=0, columnspan=2, pady=(6,0))
        Button(btn_frame, text="SIGN IN",bg="#f36bc5",fg="white",font=("Montserrat Black",12) ,width=12, command=self.sign_in).pack(side=LEFT, padx=20)
        Button(btn_frame, text="SIGN UP",bg="#431978",fg="white",font=("Montserrat Black",12) ,width=12, command=self.open_register_window).pack(side=LEFT, padx=(20,0))

    def sign_in(self):
        user = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()
        if not user or not password:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập username và password.")
            return
        if check_login(user, password):
            self.show_users_frame()
        else:
            messagebox.showerror("Lỗi", "Sai username hoặc password.")

    def open_register_window(self):
        RegisterWindow(self.master)

class Askpass(Toplevel):
    def __init__(self, master, username, openApp):
        super().__init__(master)
        self.username = username
        self.openApp = openApp
        self.title(f"Nhập private pass ({username})")
        self.resizable(False, False)
        self.ask_widgets()
        self.transient(master)
        self.grab_set()

    def ask_widgets(self):
        self.config(bg="#250c6a")
        Label(self, text=f"Nhập mật khẩu riêng của {self.username}",fg='white',bg="#250c6a", font=("Montserrat Black", 10, "bold")).pack()
        self.askEntry = Entry(self, show="*",width=15,fg="#f36bc5",font=("Montserrat Black", 12, "bold"))
        self.askEntry.pack()
        keypad = Frame(self,bg="#250c6a")
        keypad.pack(padx=(39,0),pady=(5,2))
        index = 0
        for i in range(3):
            for j in range(3):
                Button(
                    keypad,
                    bg="#f36bc5",
                    text=num[index],
                    fg='white',
                    font=("Montserrat Black", 12, "bold"),
                    width=3, height=1,
                    command=lambda n=num[index]: self.askEntry.insert(END, n)
                ).grid(row=i, column=j, padx=(3,0), pady=(2,0))
                index += 1

        Button(keypad, text="⌫", font=("Montserrat Black", 12, "bold"),bg="#f36bc5",fg='white',command=lambda:self.askEntry.delete(len(self.askEntry.get())-1,END)).grid(row=2, column=3, padx=(3,0), pady=(2,0))
        Button(self, text="0", font=("Montserrat Black", 12, "bold"),width=3, height=1,bg="#f36bc5",fg='white',command=lambda:self.askEntry.insert(END, "0")).pack(pady=(0,2))
        Button(self, text="Xác nhận", font=("Montserrat Black", 10, "bold"),bg="#f36bc5",fg='white',command=self.pass_in).pack()

    def pass_in(self):
        pp = self.askEntry.get().strip()
        data = load_pripass()
        for item in data:
            if item.get("user") == self.username and item.get("pripass") == pp:
                messagebox.showinfo("Thành công", "Đăng nhập thành công!")
                self.destroy()
                self.openApp()
                return
        messagebox.showerror("Lỗi", "Sai mật khẩu riêng!")

class addPass(Toplevel):
    def __init__(self, master, username):
        super().__init__(master)
        self.username = username
        self.title(f"Tạo pripass cho {username}")
        self.resizable(False, False)
        self.addP_widgets()
        self.transient(master)
        self.grab_set()

    def addP_widgets(self):
        self.config(bg="#250c6a")
        Label(self, text=f"Tạo mật khẩu riêng cho {self.username}",fg='white',bg="#250c6a", font=("Montserrat Black", 10, "bold")).pack()
        self.askEntry = Entry(self, show="*",width=15,fg="#f36bc5",font=("Montserrat Black", 12, "bold"))
        self.askEntry.pack()
        keypad = Frame(self,bg="#250c6a")
        keypad.pack(padx=(39,0),pady=(5,2))
        index = 0
        for i in range(3):
            for j in range(3):
                Button(
                    keypad,
                    bg="#f36bc5",
                    text=num[index],
                    fg='white',
                    font=("Montserrat Black", 12, "bold"),
                    width=3, height=1,
                    command=lambda n=num[index]: self.askEntry.insert(END, n)
                ).grid(row=i, column=j, padx=(3,0), pady=2)
                index += 1
        Button(keypad, text="⌫", font=("Montserrat Black", 12, "bold"),bg="#f36bc5",fg='white',command=lambda:self.askEntry.delete(len(self.askEntry.get())-1,END)).grid(row=2, column=3, padx=(3,0), pady=2)
        Button(self, text="0", font=("Montserrat Black", 12, "bold"),width=3, height=1,bg="#f36bc5",fg='white',command=lambda:self.askEntry.insert(END, "0")).pack(pady=(0,2))
        Button(self, text="Xác nhận", font=("Montserrat Black", 10, "bold"),bg="#f36bc5",fg='white',command=self.confirm).pack()

    def confirm(self):
        pp = self.askEntry.get().strip()
        if not pp:
            messagebox.showwarning("Cảnh báo", "Không được để trống!")
            return
        if any(c in invalid_char for c in pp) or " " in pp:
            messagebox.showerror("Lỗi", "Không dùng ký tự đặc biệt!")
            return
        if len(pp) == 6:
            if not os.path.exists(PPASS_FILE):
                with open(PPASS_FILE, "w", encoding="utf-8") as f:
                    json.dump([], f, ensure_ascii=False)

            with open(PPASS_FILE, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    if not isinstance(data, list):
                        data = []
                except:
                    data = []
            data = load_pripass()
            found = False
            for it in data:
                if it.get("user") == self.username:
                    it["pripass"] = pp
                    found = True
                    break
            if not found:
                data.append({"user": self.username, "pripass": pp})
            # ghi lại
            with open(PPASS_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("Thành công", "Tạo mặt khẩu thành công")
            self.destroy()
        else:
            messagebox.showerror("Lỗi", "Mật khẩu dài 6 ký tự")
            self.askEntry.delete(0,END)

# Sign up
class RegisterWindow(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Đăng ký tài khoản")
        self.geometry("620x320")
        self.resizable(False, False)
        self.config(bg="#250c6a")
        self.signin = PhotoImage(file="signin.png")
        self.create_widgets()
        
        # đặt focus vào cửa sổ đăng ký
        self.transient(master)
        self.grab_set()

    def create_widgets(self):
        Label(self,background="#250c6a",image=self.signin).place(x=0,y=0)
        frm = Frame(self,bg="#250c6a")
        frm.place(relx=0.46, rely=0.50,anchor="center")

        Label(frm, text="Username:",bg="#250c6a",fg="white",font=("Montserrat Black",12) ,anchor="w").grid(row=0, column=0,padx=5,pady=6)
        self.user_entry = Entry(frm,font = ("Montserrat", 8))
        self.user_entry.grid(row=0, column=1,pady=6)

        Label(frm, text="Password:",bg="#250c6a",fg="white",font=("Montserrat Black",12), anchor="w").grid(row=1, column=0,pady=6)
        self.pass_entry = Entry(frm, show="*",font = ("Montserrat", 8))
        self.pass_entry.grid(row=1, column=1,pady=6)

        Label(frm, text="Confirm:",bg="#250c6a",fg="white",font=("Montserrat Black",12) ,anchor="w").grid(row=2, column=0,pady=6)
        self.pass_confirm = Entry(frm, show="*",font = ("Montserrat", 8))
        self.pass_confirm.grid(row=2, column=1,pady=6)
        frmB = Frame(self,bg="#250c6a")
        frmB.place(relx=0.45, rely=0.76, anchor="center")

        Button(frmB, text="SIGN UP",bg="#f36bc5", fg="white",font=("Montserrat Black",10),width=9, command=self.register).grid(row=3, padx=70 ,column=0,sticky="w",pady=6)
        Button(frmB, text="CANCEL", bg="#431978",fg="white",font=("Montserrat Black",10),width=9, command=self.cancel).grid(row=3, column=1, sticky="w",pady=(6,0))

    def register(self):
        user = self.user_entry.get().strip()
        pw = self.pass_entry.get()
        pwc = self.pass_confirm.get()
        if not user or not pw or not pwc:
            messagebox.showwarning("Không để trống")
            return
        if any(c in invalid_char for c in pw) or " " in pw:
            messagebox.showerror("","Không sài ký tự đặc biệt")
            return
        if pw != pwc:
            messagebox.showerror("","Mật khẩu xác nhận không khớp")
            return
        success = save_account(user, pw)
        if not success:
            messagebox.showerror("","Tài khoản có rồi")
        else:
            messagebox.showinfo("Thành công", "Ok đăng nhập đi")
            self.destroy()

    def cancel(self):
        self.destroy()

class ArduinoFrame(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("620x780")
        self.resizable(True, True)
        arduino = find_arduinoPort()
        self.background = PhotoImage(file='background.png')
        self.cay_list = {
            "CÀ CHUA":'r',
            "XÀ LÁCH":'g',
            "VIỆT QUẤT":'b'
        }
        self.create_widgets()
        if os.path.exists(DATA_FILE):
            data = load_time()
            alarmTime = data[0]['start_time']
            self.show_time_remaining(alarmTime)

        # self.read_soil()

    def create_widgets(self):
        self.config(bg="#250c6a")
        self.menubar = Menu(self)
        self.config(menu=self.menubar)
        Label(self,background="#250c6a",image=self.background).place(x=0,y=0)
        self.time_set = {
            "3s":3,
            "4s":4,
            "5s": 5,
        }
        self.filmeme= Menu(self.menubar,tearoff=0,font=("Montserrat Black",10),activebackground="#00A01B")
        self.menubar.add_cascade(label='FILE',menu=self.filmeme)
        self.filmeme.add_command(label='QUIT',command=quit)
        # Frame label
        frameL = Frame(self,bg="#250c6a")
        frameL.grid(row=1, column=0,padx=45,pady=(100, 0))

        self.label_temp = Label(frameL, text="NHIỆT ĐỘ: ---- °C", fg='white',background="#250c6a",font=("Montserrat Black",12))
        self.label_hum = Label(frameL, text="ĐỘ ẨM: ---- %", fg='white',background="#250c6a",font=("Montserrat Black",12))
        self.label_soil = Label(frameL, text="ĐỘ ẨM ĐẤT: ---- %",background="#250c6a",fg='white',font=("Montserrat Black",12),)
        self.label_temp.pack(side='left',padx=(0,10))
        self.label_hum.pack(side='left',padx=(60,5))
        self.label_soil.pack(side='left',padx=(50,0))
        # Frame cobo vs label
        self.frameCl = Frame(self,bg="#250c6a")
        self.frameCl.grid(row=3, column=0,padx=1,pady=(30, 30))
        Label(self.frameCl, text="CHỌN CÂY:",fg="#f36bc5",background="#250c6a",font=("Montserrat Black",14)).pack(side="left",padx=(1,0),pady=6)

        # Frame label
        frameLE = Frame(self,background="#250c6a")
        frameLE.grid(row=7, column=0)

        Label(frameLE, text="HẸN GIỜ TƯỚI(HH:MM): ",background="#250c6a",fg='white',font=("Montserrat Black",14)).pack(side="left")

        self.combo = ttk.Combobox(self.frameCl,values=list(self.cay_list.keys()), font=("Montserrat Black",14))
        self.combo.pack(side="left")
        self.combo.bind("<<ComboboxSelected>>", self.on_select_cay)

        Button(self.frameCl,text="+",font=("Montserrat Black",9),width=2,bd=3,bg='#f36bc5',fg='white',command=self.add).pack(side='left')
        
        self.his = Listbox(self,width=50,borderwidth=2,activestyle=None,font=("Montserrat Black",10),height=10)
        self.his.grid(row=11,column=0,columnspan=3)

        framcheck = Frame(self,background="#250c6a")
        framcheck.grid(row=9,column=0,columnspan=3,pady=6)
        self.x = StringVar()
        self.index = list(self.time_set.keys())
        for i in self.time_set.keys():
            self.timeSet = Radiobutton(framcheck,text=i,
                                       variable= self.x,
                                       value= self.index,
                                       font=("Montserrat Black",10),
                                       pady= 10,
                                       padx= 20,
                                       activebackground="#056429",
                                       activeforeground="white",
                                       state="normal",
                                       background="#f36bc5",fg='white',
                                       indicatoron=0,
                                       command=lambda v=i: self.toggle_radio(v)
                                       )
            self.timeSet.pack(side = "left",padx=20)

        self.entry_time = Entry(frameLE,bd=2)
        self.entry_time.pack(side="left")
        # Frame cua scale
        framS = Frame(self,background="#250c6a")
        framS.grid(row=4,column=0,pady=10)
        self.scaleLED = Scale(framS, from_=0, to=1,orient='horizontal',fg='white',font=("Montserrat Black",10),showvalue=0,background="#f36bc5",length=65,label="LED OFF",troughcolor="white",command= self.turn_led)
        self.scaleLED.pack(side='left',padx=(0,70))
        
        self.scaleFan = Scale(framS, from_=0, to=1,orient='horizontal', background="#f36bc5",fg='white',font=("Montserrat Black",10),showvalue=0,length=65,label="FAN OFF",troughcolor="white",command= self.turn_fan)
        self.scaleFan.pack(side='left',padx=(45,50))

        Button(framS, text="Blink",background="#f36bc5",fg='white',font=("Montserrat Black",14),command=self.blink_led).pack(side='left',padx=(70,0))
        self.bright = Scale(self, from_=10 ,to=100,resolution=10,orient='horizontal',background="#f36bc5",fg='white',font=("Montserrat Black",10),troughcolor="white",length=100,label="Brightness",command=self.sendVal)
        self.thongbao = Label(self,background="#250c6a")
        self.thongbao.grid(row=5,column=0,pady=30)

        frame_4 = Frame(self,background="#250c6a")
        frame_4.grid(row=6,columnspan=3,pady=6,padx=5)
        
        framdoor = Frame(self,background="#250c6a")
        framdoor.grid(row=10,column=0,columnspan=3)

        Button(frame_4, text="Đọc DHT", background="#f36bc5",fg='white',font=("Montserrat Black",14),command=self.read_DHT).pack(side='left',padx=10)
        Button(frame_4, text="Mở rèm", background="#f36bc5",fg='white',font=("Montserrat Black",14),command=self.rem_thuan).pack(side='left',padx=10)
        Button(frame_4, text="Đóng rèm", background="#f36bc5",fg='white',font=("Montserrat Black",14),command=self.rem_nguoc).pack(side='left',padx=10)
        Button(frame_4, text="Dừng rèm", background="#f36bc5",fg='white',font=("Montserrat Black",14),command=self.rem_dung).pack(side='left',padx=10)
        Button(framcheck, text="ON", background="#f36bc5",width=4,fg='white',font=("Montserrat Black",13),command=self.on_water).pack(side = "left",padx=20)
        Button(framcheck, text="OFF", background="#f36bc5",width=4,fg='white',font=("Montserrat Black",13),command=self.off_water).pack(side = "left",padx=20)
        Button(framdoor, text="OPEN", background="#f36bc5",width=4,fg='white',font=("Montserrat Black",13),command=self.cua_mo).pack(side = "left",padx=25,pady=(7,3))
        Button(framdoor, text="SHUT", background="#f36bc5",width=4,fg='white',font=("Montserrat Black",13),command=self.cua_dong).pack(side = "left",padx=25,pady=(7,3))


    def send_command(self, cmd: bytes):
        if not arduino:
            messagebox.showerror("Lỗi", "Không kết nối Arduino.")
            return
        try:
            arduino.write(cmd)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Gửi lệnh thất bại: {e}")

    # def sendVal(self,value):
    #     if int(value) > 0:
    #        self.addHis("Độ sáng",f"{value}")

    def turn_led(self,value):
        cay = self.combo.get()
        color = self.cay_list.get(cay)
        if color == None:
            self.addHis("Chưa chọn cây"," ")
            self.scaleLED.config(label="LED OFF",fg="white",troughcolor="white")
            print(cay)

        elif int(value) == 1 and color != None:
            self.scaleLED.config(label="LED ON",fg="green",troughcolor="green")
            # self.send_command(f"3{color}".encode())
            print(color)
            self.addHis("Đã mở",f"LED cho cây {cay}")
            self.thongbao.grid_forget()
            self.bright.grid(row=5,column=0, padx=100,pady=6)
        else:
            self.scaleLED.config(label="LED OFF",fg="white",troughcolor="white")
            # self.send_command(b'4')
            self.combo.delete(0,END)
            self.addHis("Đã tắt","LED")
            self.bright.grid_forget()
            self.thongbao.grid(row=5,column=0,pady=30)
        
    def on_select_cay(self, event=None):
        if self.scaleLED.get() == 1:
            self.turn_led(1)

    def blink_led(self):
        # self.send_command(b'6')
        self.addHis("Nháy","LED")
    
    # def sendVal(self, value):
    #     try:
    #         val = int(value)
    #         if val > 0:
    #             self.addHis("Độ sáng", f"{val}")
    #             command = f"S{val}\n"
    #             self.after(800,self.send_command(command.encode()))
    #     except Exception as e:
    #         print("Lỗi gửi độ sáng:", e)

    def sendVal(self, value):
        try:
            val = int(value)
            val = max(0, min(255, val))
            self.addHis("Độ sáng", f"{val}")
            command = f"S{val}\n"

            if hasattr(self, "pending_after"):
                self.after_cancel(self.pending_after)

            self.pending_after = self.after(1000, lambda: self.send_command(command.encode()))

        except Exception as e:
            print("Lỗi gửi độ sáng:", e)

       
    def rem_thuan(self):
        self.send_command(b'7')
        self.addHis("Đã mở","Rèm")

    def rem_nguoc(self):
        self.send_command(b'8')
        self.addHis("Đã đóng","Rèm")

    def rem_dung(self):
        self.send_command(b'9')
        self.addHis("Đã dừng","Rèm")

    def cua_mo(self):
        self.send_command(b'o')
        self.addHis("Đã mở","Cửa")

    def cua_dong(self):
        self.send_command(b'c')
        self.addHis("Đã đóng","Cửa")

    def read_DHT(self):
        if not arduino:
            messagebox.showerror("Lỗi", "Không kết nối Arduino.")
            return
        try:
            arduino.write(b'5')
            self.addHis("Đã đọc: ","DHT")
            self.after(300, self.update_DHT)
        except Exception as e:
            print("Lỗi gửi lệnh DHT:", e)

    def update_DHT(self):
        try:
            line = arduino.readline().decode().strip()
            if "," in line:
                t, h = line.split(",", 1)
                self.label_temp.config(text=f"Nhiệt độ: {t}°C")
                self.label_hum.config(text=f"Độ ẩm: {h}%")
            else:
                print("Dòng nhận được (DHT):", repr(line))
        except Exception as e:
            print("Lỗi đọc DHT:", e)

    def read_soil(self):
        if not arduino:
            messagebox.showerror("Lỗi", "Không kết nối Arduino.")
            return
        try:
            arduino.write(b'1')
            self.after(300, self.update_soil)
        except Exception as e:
            print("Lỗi gửi lệnh soil:", e)
 
    def update_soil(self):
        try:
            line = arduino.readline().decode().strip()
            if ":" in line:
                parts = line.split(":", 1)
                value = int(parts[1].strip())
                self.label_soil.config(text=f"Độ ẩm đất: {value}%")
                if value >= 1000:
                    mes = messagebox.askyesno("Thông báo độ ẩm","Có cần tưới thêm nước?")
                    if mes:
                        print("Đang tưới nước...")
                        # arduino.write(b'a')
                        self.after(5000, self.off_water)
            else:
                print("Không đọc được:", repr(line))
        except Exception as e:
            print("Lỗi đọc Soil:", e)

    def set_alarm(self, event=None):
        alarm_time = self.entry_time.get().strip()
        if not alarm_time:
            messagebox.showwarning("Lỗi", "Không để trống thời gian hẹn!")
            return
        try:
            datetime.datetime.strptime(alarm_time, "%H:%M")
        except ValueError:
            messagebox.showerror("Lỗi", "Sai định dạng(HH:MM)")
            return
        
        save_time(alarm_time)
        data = load_time()
        if any(item.get("start_time") == alarm_time for item in data):
            messagebox.showinfo("Thành công", f"Hẹn giờ tưới lúc {alarm_time}")
        else:
            messagebox.showerror("Lỗi", "Không thể lưu thời gian")
        stime = self.x.get()
        wtime = self.time_set.get(stime) * 1000 if self.time_set.get(stime) else 3000
        self.after(1000, lambda: self.check_alarm(alarm_time, wtime))
        self.entry_time.delete(0,END)
        self.addHis("Đã hẹn giờ", f"{alarm_time}")

    def on_water(self):
        self.send_command(b'a')

    def on_water(self):
        self.send_command(b'b')      
    
    def show_time_remaining(self,alarm_time):
        try:
            now = datetime.datetime.now()
            alarm_timenot = datetime.datetime.strptime(alarm_time, "%H:%M")
            alarm_timenot = alarm_timenot.replace(year=now.year, month=now.month, day=now.day)

            if alarm_timenot <= now:
                alarm_timenot += datetime.timedelta(days=1)

            remaining = alarm_timenot - now
            total_seconds = int(remaining.total_seconds())

            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60

            msg = f"Còn {hours} giờ {minutes} phút trước khi tưới"
            messagebox.showinfo("Thời gian còn lại", msg)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tính thời gian còn lại!")

    def off_water(self):
        self.send_command(b'b')
        mes = messagebox.askyesno("Hẹn lịch tưới lại","Bạn có muốn giữ lại lịch tưới cũ không?")
        if not mes:
            os.remove(DATA_FILE)

    def check_alarm(self, alarm_time, wtime):
        current_time = datetime.datetime.now().strftime("%H:%M")
        if current_time == alarm_time:
            self.addHis("Đã tưới nước",f"{alarm_time}")
            # self.send_command(b'a')
            self.after(wtime, lambda: self.off_water())
            return
        self.after(1000,lambda: self.check_alarm(alarm_time,wtime))

    def turn_fan(self,value):
        if int(value) == 1:
            self.scaleFan.config(label="FAN ON",fg="green",troughcolor="green")
            # self.send_command(b'B')
            self.addHis("Đã mở","Quạt")
        else:
            self.scaleFan.config(label="FAN OFF",fg="white",troughcolor="white")
            # self.send_command(b't')
            self.addHis("Đã tắt","Quạt")

    def addHis(self,state,devices):
        time = datetime.datetime.now().strftime("%H:%M:%S")
        self.his.insert(self.his.size(),f"{state}: {devices} ------------------ {time}")
        self.his.see(END)


    def add(self):
        addColor(self.cay_list,self.combo,self.scaleLED,self.his,self.thongbao,self.bright)
        self.scaleLED.set(1)
        self.turn_led(1)

    def toggle_radio(self, value):
        if self.x.get() == value:
            self.x.set("")
        else:
            self.x.set(value)
        self.set_alarm()

    def logout(self):
        # Quay lại màn hình login
        self.master.show_login_frame()

class addColor(Toplevel,ArduinoFrame):
    def __init__(self,cay_list,combo,scaleLED,his,thongbao,bright):
        super().__init__()
        self.cay_list = cay_list
        self.combo = combo
        self.scaleLED = scaleLED
        self.his = his
        self.thongbao = thongbao
        self.bright = bright
        self.title("Chọn màu")
        self.geometry("320x220")
        self.resizable(False, False)
        self.addP_widgets()

    def addP_widgets(self):
        frm_c=Frame(self)
        frm_c.place(x=5,y=110)
        self.color = "rgbpw"
        frm = Frame(self)
        frm.place(x=10,y=20)
        frm1 = Frame(self)
        frm1.place(x=110,y=70)
        Label(frm,text="NHẬP TÊN CÂY: ",font=("Montserrat Black",10)).grid(row=0,column=0)
        self.entryAdd = Entry(frm,font=("Montserrat Black",10))
        self.entryAdd.grid(row=0,column=1)
        Label(frm1,text="CHỌN MÀU ",font=("Montserrat Black",14)).grid(row=1,column=0)
        for i in range(len(self.color)):
            btn = Button(frm_c,text=self.color[i].upper(),font=("Montserrat Black",20),width=2,bg=colorwheel[i],
                         command= lambda color = self.color[i]:  self.read(color))
            btn.grid(row=2,column=i,padx=8)

    def read(self,color):
        new_name = self.entryAdd.get().upper()
        if new_name and new_name in self.cay_list:
            print("INVALID")
        elif len(new_name) == 0:
            print("Empty")
        else:
            self.cay_list[new_name] = color
            self.combo['values'] = list(self.cay_list.keys())
            self.combo.set(new_name)
            if self.scaleLED.get() == 1:
                self.turn_led(1)

class Users(Frame):
    def __init__(self, master, show_arduino_frame):
        super().__init__(master)
        self.master = master
        self.show_arduino_frame = show_arduino_frame
        self.userImages = PhotoImage(file="users.png")
        self.image = PhotoImage(file='loginapp.png')
        self.x = IntVar()
        self.users_widgets()

    def users_widgets(self):
        bg = Label(self, background="#250c6a", image=self.image)
        bg.place(x=0, y=0)
        bg.lower()

        self.frm_1 = Frame(self, bg="#250c6a")
        self.frm_1.pack(padx=20, pady=(20, 0))
        self.frm_2 = Frame(self, bg="#250c6a")
        self.frm_2.pack(pady=10, padx=10)

        self.title1 = Button(
            self.frm_1, text="Xin Chào, Ai Đang Sử Dụng?",
            fg="white", bg="#f36bc5", font=("Montserrat Black", 20, 'bold'),
            disabledforeground="white", state='disable'
        )
        self.title1.grid(row=0, column=0)

        for i in range(len(users)):
            btn = Button(
                self.frm_2,
                text=users[i].upper(),
                image=self.userImages,
                compound='top',
                font=("Montserrat Black", 16),
                fg="#250c6a",
                background="white",
                activebackground="#f36bc5",
                command=lambda n=users[i]: self.checkb_openApp(n)
            )
            btn.grid(row=1, column=i, padx=(5, 0))

        self.frm_h = Frame(self, bg="#250c6a")
        self.frm_h.place(x=90, y=120)

    def Hola(self, name):
        self.frm_1.pack_forget()
        self.frm_2.pack_forget()
        Label(
            self.frm_h,
            text=f"Chào mừng quay lại {name}",
            fg="white",
            bg="#250c6a",
            font=("Montserrat Black",20)
        ).pack()

    def checkb_openApp(self, name):
        pripass_list = load_pripass()
        item = next((it for it in pripass_list if it.get("user") == name), None)
        if item is None:
            create = messagebox.askyesno(
                "Chưa có mật khẩu",
                f"{name} chưa có mật khẩu riêng.\nBạn có muốn tạo không?"
            )
            if create:
                addPass(self, name)  
            else:
                self.openApp(name)
            return
        if not item.get("pripass"):
            create = messagebox.askyesno(
                "Chưa có mật khẩu",
                f"{name} chưa có mật khẩu riêng.\nBạn có muốn tạo không?"
            )
            if create:
                addPass(self, name)
            else:
                self.openApp(name)
            return
        Askpass(self, name, lambda: self.openApp(name))


    def openApp(self, name):
        self.Hola(name)
        self.after(3000, self.show_arduino_frame)

# app
class App(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("620x320")
        self.resizable(False, False)

        self.login_frame = LoginFrame(self, self.show_users_frame)
        self.users_frame = Users(self,self.show_arduino_frame)

        self.login_frame.pack(fill="both", expand=True)

    def show_users_frame(self):
        self.login_frame.pack_forget()
        self.users_frame.pack(fill="both", expand=True)

    def show_arduino_frame(self):
        self.destroy()
        # self.users_frame.pack_forget()
        main = ArduinoFrame()
        main.mainloop()
        
    def show_login_frame(self):
        self.arduino_frame.pack_forget()
        self.login_frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = ArduinoFrame()
    app.mainloop()