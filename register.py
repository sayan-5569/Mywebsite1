from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
import os

class Register:
    def __init__(self, root):
        self.root = root
        self.root.title("Registration Window")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="white")

        # Bg image
        self.bg = ImageTk.PhotoImage(file="image/b2.png")
        self.bg_label = Label(self.root, image=self.bg)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Left image
        left_img = Image.open("image/b1.png")
        left_img = left_img.resize((400, 500), Image.Resampling.LANCZOS)
        self.left = ImageTk.PhotoImage(left_img)
        self.left_label = Label(self.root, image=self.left)
        self.left_label.place(x=80, y=100, width=400, height=500)

        # Register Frame
        frame1 = Frame(self.root, bg="white")
        frame1.place(x=480, y=100, width=700, height=500)

        title = Label(frame1, text="REGISTRATION", font=("times new roman", 20, "bold"), bg="white", fg="#1100FF").place(x=200, y=30)

        # Row 1
        f_name = Label(frame1, text="First Name", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=100)
        self.txt_fname = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_fname.place(x=50, y=130, width=250)

        l_name = Label(frame1, text="Last Name", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=370, y=100)
        self.txt_lname = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_lname.place(x=370, y=130, width=250)

        # Row 2
        contact = Label(frame1, text="Contact No", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=170)
        self.txt_contact = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_contact.place(x=50, y=200, width=250)

        email = Label(frame1, text="Email", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=370, y=170)
        self.txt_email = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_email.place(x=370, y=200, width=250)

        # Row 3
        question = Label(frame1, text="Security question", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=240)
        self.cmb_quest = ttk.Combobox(frame1, font=("times new roman", 13), state='readonly', justify=CENTER)
        self.cmb_quest['values'] = ("Select", "Your First pet name", "Your Hobby", "Where is your City", "Your favorite game")
        self.cmb_quest.place(x=50, y=270, width=250)
        self.cmb_quest.current(0)

        answer = Label(frame1, text="Answer", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=370, y=240)
        self.txt_answer = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_answer.place(x=370, y=270, width=250)

        # Row 4
        password = Label(frame1, text="Password", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=310)
        self.txt_password = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_password.place(x=50, y=340, width=250)

        cpassword = Label(frame1, text="Confirm Password", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=370, y=310)
        self.txt_cpassword = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_cpassword.place(x=370, y=340, width=250)

        # Terms and Register button
        self.var_chk = IntVar()
        chk = Checkbutton(frame1, text="I agree the Terms & Conditions", variable=self.var_chk, onvalue=1, offvalue=0, bg="white", font=("times new roman", 12)).place(x=50, y=380)

        self.btn_img = ImageTk.PhotoImage(file="image/register.png")
        btn_register = Button(frame1, image=self.btn_img, bd=0, cursor="hand2", command=self.register_data)
        btn_register.place(x=220, y=420)

        btn_login = Button(self.root, text="Sign In", command=self.login_window, font=("times new roman", 20), bd=0, cursor="hand2").place(x=200, y=500, width=150)

    def login_window(self):
        self.root.destroy()
        os.system("python login.py")

    def clear(self):
        self.txt_fname.delete(0, END)
        self.txt_lname.delete(0, END)
        self.txt_contact.delete(0, END)
        self.txt_email.delete(0, END)
        self.txt_answer.delete(0, END)
        self.txt_password.delete(0, END)
        self.txt_cpassword.delete(0, END)
        self.cmb_quest.current(0)
        self.var_chk.set(0)

    def register_data(self):
        print("Register button clicked")

        if self.txt_fname.get() == "" or self.txt_lname.get() == "" or self.txt_contact.get() == "" or \
           self.txt_email.get() == "" or self.cmb_quest.get() == "Select" or self.txt_answer.get() == "" or \
           self.txt_password.get() == "" or self.txt_cpassword.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
            return

        if self.txt_password.get() != self.txt_cpassword.get():
            messagebox.showerror("Error", "Password & Confirm Password should be the same", parent=self.root)
            return

        if self.var_chk.get() == 0:
            messagebox.showerror("Error", "Please agree to the Terms & Conditions", parent=self.root)
            return

        try:
            con = sqlite3.connect(database="ams.db")
            cur = con.cursor()
            cur.execute("DROP TABLE IF EXISTS employee")
        # ✅ Create the employee table if it doesn't exist
            cur.execute("""
            CREATE TABLE IF NOT EXISTS employee (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                f_name TEXT,
                l_name TEXT,
                contact TEXT,
                email TEXT UNIQUE,
                question TEXT,
                answer TEXT,
                password TEXT
            )
            """)

            cur.execute("SELECT * FROM employee WHERE email = ?", (self.txt_email.get(),))
            row = cur.fetchone()
            if row is not None:
                messagebox.showerror("Error", "User already exists, please try with anothe r email", parent=self.root)
            else:
                cur.execute("""
                    INSERT INTO employee (f_name, l_name, contact, email, question, answer, password)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    self.txt_fname.get(),
                    self.txt_lname.get(),
                    self.txt_contact.get(),
                    self.txt_email.get(),
                    self.cmb_quest.get(),
                    self.txt_answer.get(),
                    self.txt_password.get()
                ))
                con.commit()
                messagebox.showinfo("Success", "Registration Successful", parent=self.root)
                self.clear()
                self.login_window()

            con.close()

        except Exception as es:
            messagebox.showerror("Error", f"Error due to: {str(es)}", parent=self.root)

# Main execution
if __name__ == "__main__":
    root = Tk()
    obj = Register(root)
    root.mainloop()
