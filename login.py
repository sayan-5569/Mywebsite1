from tkinter import *
from tkinter import messagebox, ttk
from PIL import Image, ImageTk, ImageDraw
import datetime
import math
import sqlite3
import os

# Initialize the SQLite database
def init_db():
    con = sqlite3.connect("ams.db")
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS employee (
            f_name TEXT,
            l_name TEXT,
            contact TEXT,
            email TEXT PRIMARY KEY,
            password TEXT,
            question TEXT,
            answer TEXT
        )
    """)
    con.commit()
    con.close()

class Login_window:
    def __init__(self, root):
        self.root = root
        self.root.title("Login System")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#021e2f")

        # Background
        left_lbl = Label(self.root, bg="#00C3FF", bd=0)
        left_lbl.place(x=0, y=0, relheight=1, width=600)

        right_lbl = Label(self.root, bg="#031F3C", bd=0)
        right_lbl.place(x=600, y=0, relheight=1, relwidth=1)

        # Login Frame
        login_frame = Frame(self.root, bg="white")
        login_frame.place(x=250, y=95, width=800, height=500)

        title = Label(login_frame, text="USER  LOGIN", font=("times new roman", 30, "bold"), bg="white", fg="#08A3D2")
        title.place(x=250, y=50)

        email = Label(login_frame, text="EMAIL ADDRESS", font=("times new roman", 15, "bold"), bg="white", fg="gray")
        email.place(x=250, y=150)
        self.txt_email = Entry(login_frame, font=("times new roman", 15), bg="lightgray")
        self.txt_email.place(x=250, y=180, width=350, height=35)

        pass_ = Label(login_frame, text="PASSWORD", font=("times new roman", 15, "bold"), bg="white", fg="gray")
        pass_.place(x=250, y=250)
        self.txt_pass_ = Entry(login_frame, font=("times new roman", 15), bg="lightgray", show="*")
        self.txt_pass_.place(x=250, y=280, width=350, height=35)

        btn_reg = Button(login_frame, text="Register new Account?", font=("times new roman", 12), bg="white", bd=0,
                         fg="#FF00A2", cursor="hand2", command=self.open_register_window)
        btn_reg.place(x=250, y=320)

        btn_forget = Button(login_frame, text="Forget Password?", font=("times new roman", 12), bg="white", bd=0,
                            fg="#4A9801", cursor="hand2", command=self.forget_password_window)
        btn_forget.place(x=480, y=320)

        btn_login = Button(login_frame, text="Login", command=self.login_user, font=("times new roman", 18, "bold"),
                           fg="white", bg="#FF00A2", cursor="hand2")
        btn_login.place(x=250, y=380, width=180, height=40)

        # Clock
        self.lbl = Label(self.root, text="\nWebCode clock", font=("Book Antiqua", 25, "bold"), compound=BOTTOM,
                         bg="#081923", fg="white", bd=0)
        self.lbl.place(x=90, y=120, height=450, width=350)
        self.update_clock()

    def open_register_window(self):
        self.root.destroy()
        os.system("python register.py")

    def forget_password_window(self):
        email_input = self.txt_email.get().strip()
        if email_input == "":
            messagebox.showerror("Error", "Please enter your email address first", parent=self.root)
            return

        try:
            con = sqlite3.connect("ams.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM employee WHERE email=?", (email_input,))
            row = cur.fetchone()
            con.close()

            if row is None:
                messagebox.showerror("Error", "Email not found", parent=self.root)
                return

            # Open Reset Password Window with email and security question
            self.reset_password_window(email_input)

        except Exception as e:
            messagebox.showerror("Error", f"Error due to {str(e)}", parent=self.root)

    def reset_password_window(self, email):
        self.reset_win = Toplevel(self.root)
        self.reset_win.title("Reset Password")
        self.reset_win.geometry("400x400+500+150")
        self.reset_win.config(bg="white")

        # Fetch security question for the email
        con = sqlite3.connect("ams.db")
        cur = con.cursor()
        cur.execute("SELECT question FROM employee WHERE email=?", (email,))
        question_row = cur.fetchone()
        con.close()

        question = question_row[0] if question_row else "No question set"

        title = Label(self.reset_win, text="Reset Password", font=("times new roman", 20, "bold"), bg="white", fg="red")
        title.pack(pady=20)

        lbl_email = Label(self.reset_win, text=f"Email: {email}", font=("times new roman", 12), bg="white")
        lbl_email.pack(pady=5)

        lbl_question = Label(self.reset_win, text=f"Security Question:", font=("times new roman", 12, "bold"), bg="white")
        lbl_question.pack(pady=5)

        lbl_q = Label(self.reset_win, text=question, font=("times new roman", 12), bg="white", fg="blue")
        lbl_q.pack(pady=5)

        lbl_answer = Label(self.reset_win, text="Answer", font=("times new roman", 12, "bold"), bg="white")
        lbl_answer.pack(pady=5)

        self.txt_answer = Entry(self.reset_win, font=("times new roman", 12), bg="lightgray")
        self.txt_answer.pack(pady=5)

        lbl_new_pass = Label(self.reset_win, text="New Password", font=("times new roman", 12, "bold"), bg="white")
        lbl_new_pass.pack(pady=5)

        self.txt_new_pass = Entry(self.reset_win, font=("times new roman", 12), bg="lightgray", show="*")
        self.txt_new_pass.pack(pady=5)

        btn_reset = Button(self.reset_win, text="Reset Password", font=("times new roman", 14, "bold"),
                           bg="#FF00A2", fg="white", cursor="hand2",
                           command=lambda: self.reset_password(email))
        btn_reset.pack(pady=20)

    def reset_password(self, email):
        answer = self.txt_answer.get().strip()
        new_pass = self.txt_new_pass.get().strip()

        if answer == "" or new_pass == "":
            messagebox.showerror("Error", "All fields are required", parent=self.reset_win)
            return

        try:
            con = sqlite3.connect("ams.db")
            cur = con.cursor()
            cur.execute("SELECT answer FROM employee WHERE email=?", (email,))
            row = cur.fetchone()

            if row and row[0].lower() == answer.lower():
                cur.execute("UPDATE employee SET password=? WHERE email=?", (new_pass, email))
                con.commit()
                con.close()
                messagebox.showinfo("Success", "Password reset successfully", parent=self.reset_win)
                self.reset_win.destroy()
            else:
                messagebox.showerror("Error", "Incorrect answer", parent=self.reset_win)

        except Exception as e:
            messagebox.showerror("Error", f"Error due to {str(e)}", parent=self.reset_win)

    def login_user(self):
        if self.txt_email.get().strip() == "" or self.txt_pass_.get().strip() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        else:
            try:
                con = sqlite3.connect("ams.db")
                cur = con.cursor()
                cur.execute("SELECT * FROM employee WHERE email=? AND password=?", 
                            (self.txt_email.get().strip(), self.txt_pass_.get().strip()))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Email or Password", parent=self.root)
                else:
                    messagebox.showinfo("Success", f"Welcome {self.txt_email.get().strip()}", parent=self.root)
                    self.root.destroy()
                    os.system("python Database.py")  # Or your next screen
                con.close()
            except Exception as e:
                messagebox.showerror("Error", f"Error due to {str(e)}", parent=self.root)

    def clock_image(self, hr, min, sec):
        Clock = Image.new("RGB", (400, 400), (8, 25, 35))
        draw = ImageDraw.Draw(Clock)
        try:
            bg = Image.open("image/c.png")
            bg = bg.resize((300, 300), Image.Resampling.LANCZOS)
            Clock.paste(bg, (50, 50))
        except:
            draw.ellipse((50, 50, 350, 350), outline="white", width=2)

        draw.ellipse((195, 195, 205, 205), fill="#87CEEB")

        angle_hr = (hr % 12 + min / 60) * 30
        angle_min = (min + sec / 60) * 6
        angle_sec = sec * 6

        x_hr = 200 + 50 * math.sin(math.radians(angle_hr))
        y_hr = 200 - 50 * math.cos(math.radians(angle_hr))

        x_min = 200 + 70 * math.sin(math.radians(angle_min))
        y_min = 200 - 70 * math.cos(math.radians(angle_min))

        x_sec = 200 + 90 * math.sin(math.radians(angle_sec))
        y_sec = 200 - 90 * math.cos(math.radians(angle_sec))

        draw.line((200, 200, x_hr, y_hr), fill="#EA00FF", width=4)
        draw.line((200, 200, x_min, y_min), fill="#FBFF00", width=3)
        draw.line((200, 200, x_sec, y_sec), fill="#FFFFFF", width=2)

        return Clock

    def update_clock(self):
        now = datetime.datetime.now()
        img = self.clock_image(now.hour, now.minute, now.second)
        self.imgtk = ImageTk.PhotoImage(img)
        self.lbl.config(image=self.imgtk)
        self.root.after(1000, self.update_clock)

# Run the App
init_db()
root = Tk()
obj = Login_window(root)
root.mainloop()