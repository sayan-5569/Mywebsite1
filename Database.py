from tkinter import *
from PIL import Image, ImageTk, ImageDraw
from course import CourseClass
from student import StudentClass
from result import resultclass
from report import reportclass
from tkinter import messagebox, ttk
import datetime
import math
import sqlite3
import os

class SAP:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Academic Performance")
        self.root.geometry("1440x700+0+0")
        self.root.config(bg="white")

        # Title
        title = Label(self.root, text="Academic Evaluation System", padx=10, compound=LEFT,
                      font=("goudy old style", 20, "bold"), bg="#008CFF", fg="white")
        title.place(x=0, y=0, relwidth=1, height=50)

        # Menu
        M_Frame = LabelFrame(self.root, text="Menu", font=("times new roman", 15), bg="white")
        M_Frame.place(x=10, y=70, width=1440, height=80)

        # Buttons
        btn_course = Button(M_Frame, text="Course", font=("goudy old style", 15, "bold"),
                            bg="#040c76", fg="white", cursor="hand2", command=self.add_course)
        btn_course.place(x=20, y=5, width=200, height=40)

        btn_student = Button(M_Frame, text="Student", font=("goudy old style", 15, "bold"),
                             bg="#040c76", fg="white", cursor="hand2", command=self.add_student)
        btn_student.place(x=240, y=5, width=200, height=40)

        btn_result = Button(M_Frame, text="Results", font=("goudy old style", 15, "bold"),
                            bg="#040c76", fg="white", cursor="hand2", command=self.add_result)
        btn_result.place(x=460, y=5, width=200, height=40)

        btn_View = Button(M_Frame, text="View Student Results", font=("goudy old style", 15, "bold"),
                          bg="#040c76", fg="white", cursor="hand2", command=self.add_report)
        btn_View.place(x=680, y=5, width=200, height=40)

        btn_Logout = Button(M_Frame, text="Logout", font=("goudy old style", 15, "bold"),
                            bg="#040c76", fg="white", cursor="hand2", command=self.logout)
        btn_Logout.place(x=900, y=5, width=200, height=40)

        btn_Exit = Button(M_Frame, text="Exit", font=("goudy old style", 15, "bold"),
                          bg="#040c76", fg="white", cursor="hand2", command=self.exit_)
        btn_Exit.place(x=1120, y=5, width=200, height=40)

        # Background Image
        self.bg_img = Image.open("image/bg.png")
        self.bg_img = self.bg_img.resize((920, 350), Image.LANCZOS)
        self.bg_img = ImageTk.PhotoImage(self.bg_img)
        self.lbl_bg = Label(self.root, image=self.bg_img)
        self.lbl_bg.place(x=400, y=180, width=920, height=350)

        # Labels
        self.lbl_course = Label(self.root, text="Total Courses\n[ 0 ]", font=("goudy old style", 20, "bold"),
                                bd=10, relief=RIDGE, bg="#ff00ee", fg="white")
        self.lbl_course.place(x=400, y=530, width=300, height=100)

        self.lbl_student = Label(self.root, text="Total Students\n[ 0 ]", font=("goudy old style", 20),
                                 bd=10, relief=RIDGE, bg="#ff3c00", fg="white")
        self.lbl_student.place(x=710, y=530, width=300, height=100)

        self.lbl_result = Label(self.root, text="Total Results\n[ 0 ]", font=("goudy old style", 20),
                                bd=10, relief=RIDGE, bg="#001eff", fg="white")
        self.lbl_result.place(x=1020, y=530, width=300, height=100)

        # Clock
        self.lbl = Label(self.root, text="\nWebCode clock", font=("Book Antiqua", 25, "bold"),
                         compound=BOTTOM, bg="#081923", fg="white", bd=0)
        self.lbl.place(x=10, y=180, height=450, width=350)
        self.update_clock()

        # Footer
        footer = Label(self.root, text="Contact us for any technical issue\nEmail: contactaes.official@gmail.com",
                       font=("times new roman", 15), bg="#0D00FF", fg="white")
        footer.pack(side=BOTTOM, fill=X)

        # Update counts
        self.update_details()

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

    def update_details(self):
        try:
            con = sqlite3.connect(database="ams.db")
            cur = con.cursor()

            # Courses
            cur.execute("SELECT * FROM course")
            cr = cur.fetchall()
            self.lbl_course.config(text=f"Total Courses\n[ {len(cr)} ]")

            # Students
            cur.execute("SELECT * FROM student")
            sr = cur.fetchall()
            self.lbl_student.config(text=f"Total Students\n[ {len(sr)} ]")

            # Results
            cur.execute("SELECT * FROM result")
            rr = cur.fetchall()
            self.lbl_result.config(text=f"Total Results\n[ {len(rr)} ]")

            con.close()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

        # Repeat every 2 seconds
        self.root.after(2000, self.update_details)

    def add_course(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = CourseClass(self.new_win)

    def add_student(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = StudentClass(self.new_win)

    def add_result(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = resultclass(self.new_win)

    def add_report(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = reportclass(self.new_win)

    def logout(self):
        op = messagebox.askyesno("Confirm", "Do you really want to logout?", parent=self.root)
        if op:
            self.root.destroy()
            os.system("python login.py")

    def exit_(self):
        op = messagebox.askyesno("Confirm", "Do you really want to Exit?", parent=self.root)
        if op:
            self.root.destroy()

if __name__ == "__main__":
    root = Tk()
    app = SAP(root)
    root.mainloop()