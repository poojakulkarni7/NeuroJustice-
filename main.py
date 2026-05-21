import tkinter as tk
from tkinter import scrolledtext, messagebox
from PIL import Image, ImageTk
import re
import datetime
from database import save_case
from database import get_all_cases

from predictor import analyze_situation
from database import init_db, save_case
from utils import now_string

init_db()

current_q = ""
current_a = ""

BG = "white" 
BTN = "#1f4b99"

root = tk.Tk()
root.state("zoomed")   
root.geometry("1000x1000")
root.title("NeuroJustice")
root.configure(bg=BG)
root.resizable(True, True)
root.state("zoomed")

container = tk.Frame(root, bg=BG)
container.pack(expand=True, fill="both")

container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

frames = {}

for name in ("splash","register","welcome","input","result","history"):
    f = tk.Frame(container, bg=BG)
    f.grid(row=0, column=0, sticky="nsew")   # ✅ important
    f.grid_rowconfigure(0, weight=1)
    f.grid_columnconfigure(0, weight=1)
    frames[name] = f

def show(f_name):
    frames[f_name].tkraise()

# ================= VALIDATION =================
def valid_email(e):
    return re.match(r"[^@]+@[^@]+\.[^@]+", e)

# ================= THEME COLORS =================
NAVY = "#001a4d" 
GRAY_TEXT = "#555555"
LIGHT_BG = "#f0f2f5"

# ================= REGISTER SCREEN (UPDATED) =================
register_frame = frames["register"]
register_frame.configure(bg="#E2E7E7")

# --- Central Card ---
card = tk.Frame(register_frame, bg="white", padx=40, pady=30, highlightthickness=1, highlightbackground="#dddddd")
card.place(relx=0.5, rely=0.5, anchor="center")

# --- Title with Icon ---
header_text = "👤+  Register"
tk.Label(card, text=header_text, font=("Arial", 26, "bold"), bg="white", fg=NAVY).pack(pady=(0, 25))

# --- Input Helper Function ---
def create_input(parent, label_text, is_pass=False):
    tk.Label(parent, text=label_text, font=("Arial", 11, "bold"), bg="white", fg=GRAY_TEXT).pack(anchor="w", pady=(10, 2))
    entry = tk.Entry(
        parent, 
        font=("Arial", 12), 
        width=35, 
        bd=1, 
        relief="solid", 
        highlightthickness=1, 
        highlightcolor=NAVY,
        show="*" if is_pass else ""
    )
    # Adding internal padding to make the box taller/modern
    entry.pack(ipady=8) 
    return entry

user_entry = create_input(card, "Username")
email_entry = create_input(card, "Email")
pass_entry = create_input(card, "Password", is_pass=True)

# --- Register Button ---
def register_user():
    u = user_entry.get()
    e = email_entry.get()
    p = pass_entry.get()
    
    if len(u) < 3:
        messagebox.showerror("Error", "Username too short")
        return
    if not valid_email(e):
        messagebox.showerror("Error", "Invalid email")
        return
    if len(p) < 6:
        messagebox.showerror("Error", "Password min 6 chars")
        return

    messagebox.showinfo("Success", f"Welcome {u}!\nRegistration Successful!")
    
    show("welcome")
    
btn_reg = tk.Button(
    card, 
    text="Register", 
    bg=NAVY, 
    fg="white", 
    font=("Arial", 12, "bold"),
    width=25, 
    bd=0, 
    cursor="hand2",
    activebackground="#002d80",
    activeforeground="white",
    command=register_user
)
btn_reg.pack(pady=30, ipady=5)

# --- Footer Link ---
footer_frame = tk.Frame(card, bg="white")
footer_frame.pack()

# ================= SPLASH =================
img = Image.open("logo.png").resize((1300,800))
photo = ImageTk.PhotoImage(img)
frames["splash"].photo = photo

tk.Label(frames["splash"], image=photo, bg=BG).pack(expand=True)
tk.Label(frames["splash"], text="Loading...", fg="white", bg=BG).pack()

root.after(2000, lambda: show(frames["register"]))

btn = tk.Button(
    
    text="Register",
    bg=BTN,
    fg="white",
    width=30,
    activebackground="#ab54b5",
    activeforeground="white",
    relief="flat",
    bd=0,
    pady=8,
    command=register_user
)
btn.pack()

# ===== HOVER EFFECT =====
def on_enter(e):
    btn.config(bg="#8964e8")   

def on_leave(e):
    btn.config(bg=BTN)         

btn.bind("<Enter>", on_enter)
btn.bind("<Leave>", on_leave)
bg_welcome = Image.open("legal_bg.png")

bg = Image.open("legal_bg.png")

bg = bg.resize(
    (root.winfo_screenwidth(), root.winfo_screenheight())
)

bgp = ImageTk.PhotoImage(bg)

frame = frames["welcome"]

canvas = tk.Canvas(frame, highlightthickness=0)
canvas.pack(fill="both", expand=True)

canvas.create_image(0, 0, image=bgp, anchor="nw")
canvas.image = bgp

start_btn = tk.Button(
    frame,
    text="Start",
    bg="#f7b447",
    fg="brown",
    font=("Arial", 15, "bold"),
    width=24,
    height=2,
    bd=0,
    cursor="hand2",
    command=lambda: show("input")
)

cx = root.winfo_screenwidth() // 2

canvas.create_window(cx,635,window=start_btn)

canvas.create_window(
        int(root.winfo_screenwidth()*0.67),
        int(root.winfo_screenheight()*0.67
            ),
        window=start_btn)

# ================= INPUT =================

frames["input"].configure(bg="#E2E7E7")
card2 = tk.Frame(frames["input"], bg="white", padx=30, pady=30, highlightthickness=1, highlightbackground="#E2E7E7")

card2.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(card2, text="Write Situation",
         font=("Arial",22,"bold"), bg="white", fg="#001a4d").pack(pady=(0,20))

input_box = scrolledtext.ScrolledText(card2, height=12, width=55, font=("Arial", 11),
    bd=1, 
    relief="solid",
    highlightthickness=1,
    highlightcolor="#001a4d")
input_box.pack(pady=10)

def analyze():
    global current_q, current_a
    
    text = input_box.get("1.0", tk.END).strip()

    if not text:
            messagebox.showwarning("Warning", "Please enter the situation.")
            return
    try:
        category, report = analyze_situation(text)

        current_q = text
        current_a = report

        result_box.delete("1.0", tk.END)
        result_box.insert(tk.END, report)

        show("result")

    except Exception as e:
        messagebox.showerror("Error", str(e))

btn_analyze=tk.Button(card2, text="Analyze", bg="#001a4d", fg="white", font=("arail",12,"bold"),
          width=25, bd=0, cursor="hand2",activebackground="#002d80", command=analyze
)

btn_analyze.pack(pady=(20,0), ipady = 7)

# ================= RESULT SCREEN (EDITED) =================
frames["result"].configure(bg="#E2E7E7")

card3 = tk.Frame(frames["result"], bg="white", padx=20, pady=20, highlightthickness=1, highlightbackground="#E2E7E7")
card3.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(card3, text="Analysis Result", font=("Arial", 22, "bold"), bg="white", fg=NAVY).pack(pady=(0, 15))

result_box = scrolledtext.ScrolledText(card3, height=18, width=65, font=("Arial", 10), bd=1, relief="solid")
result_box.pack()

btn_frame = tk.Frame(card3, bg="white")
btn_frame.pack(pady=20)

def save_data():
    save_case(now_string(), "Result", current_q, current_a)
    messagebox.showinfo("Saved", "Case history saved successfully!")

# --- BUTTONS MATCHING 2nd REFERENCE IMAGE ---
tk.Button(btn_frame, text="Save", bg="green", fg="white", font=("Arial", 10, "bold"), 
          width=12, command=save_data).pack(side="left", padx=5, ipady=5)

tk.Button(btn_frame, text="View History", bg="blue", fg="white", font=("Arial", 10, "bold"), 
          width=15, command=lambda: [load_history(), show("history")]).pack(side="left", padx=5, ipady=5)

tk.Button(btn_frame, text="Back", bg="gray", fg="white", font=("Arial", 10, "bold"), 
          width=12, command=lambda: show("input")).pack(side="left", padx=5, ipady=5)

history_frame = frames["history"]
history_frame.configure(bg="#E2E7E7")

card_hist = tk.Frame(history_frame, bg="white", padx=20, pady=20, highlightthickness=1, highlightbackground="#E2E7E7")
card_hist.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(card_hist, text="History", font=("Arial", 22, "bold"), bg="white", fg=NAVY).pack(pady=(0, 15))

history_list = scrolledtext.ScrolledText(card_hist, height=20, width=70, font=("Arial", 10), bd=1, relief="solid")
history_list.pack()

def load_history():
    history_list.config(state="normal")
    history_list.delete("1.0", tk.END)

    conn = sqlite3.connect("neurojustice.db")
    cur = conn.cursor()

    cur.execute("SELECT date,category,question,answer FROM history ORDER BY id DESC")
    rows = cur.fetchall()

    conn.close()

    if not rows:
        history_list.insert(tk.END, "No History Found")
        return

    for r in rows:
        history_list.insert(tk.END,
            f"Date: {r[0]}\nCategory: {r[1]}\nQ: {r[2]}\nReport: {r[3]}\n"
            + "-"*40 + "\n\n")

    history_list.config(state="disabled")
    
    history_list.config(state='disabled') 
    
tk.Button(btn_frame, text="View History", bg="blue", fg="white", 
          command=lambda: [load_history()])
    

import sqlite3
def clear_history():
    
    confirm = messagebox.askyesno("Confirm", "Do you want to clear all history?")

    if confirm:
        conn = sqlite3.connect("neurojustice.db")
        cur = conn.cursor()

        cur.execute("DELETE FROM history")

        conn.commit()
        conn.close()

        history_list.config(state="normal")
        history_list.delete("1.0", tk.END)
        history_list.insert(tk.END, "History Cleared Successfully")
        history_list.config(state="disabled")

        messagebox.showinfo("Success", "History Cleared")

hist_btn_frame = tk.Frame(card_hist, bg="white")
hist_btn_frame.pack(pady=15)

tk.Button(hist_btn_frame, text="Clear History", bg="#b22222", fg="white", font=("Arial", 10, "bold"), 
          width=15, command=clear_history).pack(side="left", padx=10, ipady=5)

import sqlite3
conn = sqlite3.connect("neurojustice.db")
cur = conn.cursor()
cur.execute("SELECT * FROM history")
print(cur.fetchall())
conn.close()

# Back to Result
tk.Button(hist_btn_frame, text="Back", bg="gray", fg="white", font=("Arial", 10, "bold"), 
          width=15, command=lambda: show("result")).pack(side="left", padx=10, ipady=5)

show("splash")
root.after(2000, lambda: show("register"))

root.mainloop()