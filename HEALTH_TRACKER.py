
import tkinter as tk
from tkinter import messagebox
import json
import matplotlib.pyplot as plt
from datetime import datetime

users_file = "users.json"
health_file = "health_data.json"


# ---------------- FILE HANDLING ----------------

def load_json(file):
    try:
        with open(file,"r") as f:
            return json.load(f)
    except:
        return {}

def save_json(file,data):
    with open(file,"w") as f:
        json.dump(data,f,indent=4)


# ---------------- LOGIN WINDOW ----------------

class LoginWindow:

    def __init__(self,root):

        self.root=root
        self.root.title("PulseTrack Login")
        self.root.geometry("420x550")
        self.root.configure(bg="#E8F0FE")

        self.users=load_json(users_file)

        header=tk.Frame(root,bg="#1E3A8A",height=130)
        header.pack(fill="x")

        tk.Label(header,text="❤",font=("Segoe UI",28),
        bg="#1E3A8A",fg="white").pack(pady=(20,0))

        tk.Label(header,text="PulseTrack",
        font=("Segoe UI",22,"bold"),
        bg="#1E3A8A",fg="white").pack()

        tk.Label(header,text="Your personal health companion",
        font=("Segoe UI",10),
        bg="#1E3A8A",fg="#DDE7FF").pack()

        card=tk.Frame(root,bg="white",padx=30,pady=30)
        card.pack(pady=40)

        tk.Label(card,text="Welcome Back",
        font=("Segoe UI",14,"bold"),bg="white").pack(pady=10)

        tk.Label(card,text="Username",bg="white").pack(anchor="w")
        self.username=tk.Entry(card,width=28)
        self.username.pack(pady=5)

        tk.Label(card,text="Password",bg="white").pack(anchor="w")
        self.password=tk.Entry(card,show="*",width=28)
        self.password.pack(pady=5)

        self.show=tk.BooleanVar()

        tk.Checkbutton(card,text="Show Password",
        variable=self.show,bg="white",
        command=self.toggle).pack(anchor="w")

        btn_frame=tk.Frame(card,bg="white")
        btn_frame.pack(pady=15)

        tk.Button(btn_frame,text="Login",
        bg="#1E3A8A",fg="white",
        width=12,command=self.login).grid(row=0,column=0,padx=5)

        tk.Button(btn_frame,text="Sign Up",
        bg="#E0E0E0",width=12,command=self.signup).grid(row=0,column=1,padx=5)

        tk.Button(card,text="Forgot Password?",
        bg="white",fg="blue",bd=0,command=self.forgot_password).pack()

    def toggle(self):
        if self.show.get():
            self.password.config(show="")
        else:
            self.password.config(show="*")

    def signup(self):

        u = self.username.get().strip()
        p = self.password.get().strip()

        if u == "" or p == "":
            messagebox.showerror("Error", "Username and Password required")
            return

        if len(p) < 4:
            messagebox.showerror("Error", "Password must be at least 4 characters")
            return

        if u in self.users:
            messagebox.showerror("Error", "User already exists")
            return

        self.users[u] = p
        save_json(users_file, self.users)

        messagebox.showinfo("Success", "Account created successfully")

        self.username.delete(0, tk.END)
        self.password.delete(0, tk.END)

    def login(self):

        u=self.username.get()
        p=self.password.get()

        if u in self.users and self.users[u]==p:

            self.root.destroy()

            main=tk.Tk()
            HealthTracker(main,u)
            main.mainloop()

        else:
            messagebox.showerror("Error","Invalid login")

    def forgot_password(self):

        win=tk.Toplevel()
        win.title("Reset Password")
        win.geometry("300x220")

        tk.Label(win,text="Username").pack(pady=5)
        user=tk.Entry(win)
        user.pack()

        tk.Label(win,text="New Password").pack(pady=5)
        new_pass=tk.Entry(win,show="*")
        new_pass.pack()

        tk.Label(win,text="Confirm Password").pack(pady=5)
        confirm=tk.Entry(win,show="*")
        confirm.pack()

        def reset():

            u=user.get()
            p=new_pass.get()
            c=confirm.get()

            if u not in self.users:
                messagebox.showerror("Error","User not found")
                return

            if p!=c:
                messagebox.showerror("Error","Passwords do not match")
                return

            self.users[u]=p
            save_json(users_file,self.users)

            messagebox.showinfo("Success","Password reset successful")

            win.destroy()

        tk.Button(win,text="Reset Password",command=reset).pack(pady=10)


# ---------------- DASHBOARD ----------------

class HealthTracker:

    def __init__(self,root,user):

        self.root=root
        self.user=user

        self.root.title("PulseTrack Dashboard")
        self.root.geometry("1000x700")
        self.root.configure(bg="#F4F6FB")

        self.data=load_json(health_file)
        

        if user not in self.data:
            self.data[user]=[]


        header=tk.Frame(root,bg="#1E3A8A",height=70)
        header.pack(fill="x")

        title=tk.Label(header,
        text=f"PulseTrack Dashboard - {user}",
        font=("Segoe UI",16,"bold"),
        fg="white",bg="#1E3A8A")

        title.pack(side="left",padx=20,pady=15)

        logout_btn = tk.Button(
        header,
        text="Logout",
        bg="#E53935",     # red background
        fg="white",       # white text
        activebackground="#C62828",  # darker red when clicked
        activeforeground="white",
        width=10,
        command=self.logout
)

        logout_btn.pack(side="right",padx=20,pady=15)
        main=tk.Frame(root,bg="#F4F6FB")
        main.pack(pady=30)

        card=tk.Frame(main,bg="white",padx=30,pady=25)
        card.pack()

        tk.Label(card,text="Daily Metrics",
        font=("Segoe UI",14,"bold"),
        bg="white").grid(row=0,column=0,columnspan=4,pady=(0,20))

        self.entries={}

        fields=[
        ("Height (cm)","height"),
        ("Weight (kg)","weight"),
        ("Sleep (hrs)","sleep"),
        ("Workout (min)","workout"),
        ("Water (L)","water"),
        ("Steps","steps")
        ]

        for i,(label,key) in enumerate(fields):

            tk.Label(card,text=label,bg="white").grid(
                row=i//2+1,column=(i%2)*2,padx=10,pady=8,sticky="w")

            e=tk.Entry(card,width=18)
            e.grid(row=i//2+1,column=(i%2)*2+1,padx=10,pady=8)

            self.entries[key]=e

        tk.Button(card,text="Save Today's Metrics",
        bg="#1E3A8A",fg="white",width=35,
        command=self.calc_score).grid(row=4,column=0,columnspan=4,pady=20)

        btn_frame=tk.Frame(main,bg="#F4F6FB")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame,text="Show Graph",
        width=15,command=self.graph).grid(row=0,column=0,padx=10)

        tk.Button(btn_frame,text="Data Analysis",
        width=15,command=self.analysis).grid(row=0,column=1,padx=10)

        tk.Button(btn_frame,text="Profile",
        width=15,command=self.profile).grid(row=0,column=2,padx=10)

        med_card=tk.Frame(main,bg="white",padx=30,pady=20)
        med_card.pack(pady=20)

        self.result=tk.Label(root,text="",
        font=("Segoe UI",12,"bold"),
        bg="#F4F6FB")

        self.result.pack(pady=15)

# ---------------- BMI ----------------

    def calc_bmi(self):

        try:

            h=float(self.entries["height"].get())/100
            w=float(self.entries["weight"].get())

            bmi=round(w/(h*h),2)

            return bmi

        except:
            messagebox.showerror("Error","Enter height & weight")


# ---------------- HEALTH SCORE ----------------

    def calc_score(self):

        bmi=self.calc_bmi()
        if bmi is None:
            return

        score=0

        if float(self.entries["sleep"].get())>=7:
            score+=2

        if float(self.entries["workout"].get())>=30:
            score+=2

        if float(self.entries["water"].get())>=2:
            score+=2

        if int(self.entries["steps"].get())>=8000:
            score+=2

        if 18.5<=bmi<=24.9:
            score+=2

        record={
        "date":str(datetime.now().date()),
        "steps":int(self.entries["steps"].get()),
        "bmi":bmi
        }

        self.data[self.user].append(record)
        save_json(health_file,self.data)

        self.result.config(text=f"BMI: {bmi} | Health Score: {score}/10")


# ---------------- GRAPH ----------------

    def graph(self):

        records = self.data[self.user]

        if not records:
            messagebox.showinfo("Info","No data available")
            return

        steps = [r["steps"] for r in records]
        bmi = [r["bmi"] for r in records]

        dates = [r["date"] for r in records]
        x = range(len(records))  # index for trend calculation

        # ----- Calculate Trend Line -----
        n = len(x)

        sum_x = sum(x)
        sum_y = sum(bmi)
        sum_xy = sum(x[i] * bmi[i] for i in range(n))
        sum_x2 = sum(i*i for i in x)

        m = (n*sum_xy - sum_x*sum_y) / (n*sum_x2 - sum_x**2)
        b = (sum_y - m*sum_x) / n

        trend = [m*i + b for i in x]

        # ----- Plot -----
        plt.figure(figsize=(6,4))

        plt.plot(x, bmi, marker="o", label="BMI")
        plt.plot(x, trend, linestyle="--", label="Trend")

        plt.title("BMI Progress Trend")
        plt.xlabel("Records Over Time")
        plt.xticks(x, dates, rotation=30)
        plt.ylabel("BMI")

        plt.legend()
        plt.grid(True)

        plt.show()

    def analysis(self):

        records=self.data[self.user]

        if not records:
            messagebox.showinfo("Info","No data available")
            return

        avg_bmi=sum(r["bmi"] for r in records)/len(records)
        avg_steps=sum(r["steps"] for r in records)/len(records)

        msg=f"""
    User: {self.user}

    Records: {len(records)}

    Average BMI: {round(avg_bmi,2)}
    Average Steps: {int(avg_steps)}

    Health Insight:
    More daily steps generally help maintain a healthy BMI.
    """

        messagebox.showinfo("Data Analysis",msg)    



    def profile(self):

        win=tk.Toplevel()
        win.title("User Profile")
        win.geometry("300x250")

        tk.Label(win,text="User Profile",
        font=("Segoe UI",14,"bold")).pack(pady=10)

        tk.Label(win,text=f"Username: {self.user}").pack(pady=5)

        tk.Label(win,text=f"Health Records: {len(self.data[self.user])}").pack(pady=5)

        tk.Button(win,text="Close",command=win.destroy).pack(pady=20)
  
    def logout(self):

        self.root.destroy()

        login_root = tk.Tk()
        LoginWindow(login_root)
        login_root.mainloop()

# ---------------- RUN ----------------

root=tk.Tk()
LoginWindow(root)
root.mainloop()
