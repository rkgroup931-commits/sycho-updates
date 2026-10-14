import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser, os, sys, json, datetime

VERSION = "v1.8.0"
BG, PANEL, CYAN, TEXT, DIM = "#0a0e1a", "#111a2e", "#00ffff", "#e0e6f0", "#8a9ab8"

try:
    import pyttsx3
    engine = pyttsx3.init()
    def speak(t): engine.say(t); engine.runAndWait()
except Exception:
    def speak(t): pass

class SYCHO(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"SYCHO — J.A.R.V.I.S {VERSION}")
        self.geometry("1100x700"); self.configure(bg=BG)
        self.sidebar = tk.Frame(self, width=230, bg="#0d1424"); self.sidebar.pack(side="left", fill="y"); self.sidebar.pack_propagate(False)
        self.main = tk.Frame(self, bg=BG); self.main.pack(side="right", fill="both", expand=True)
        self.pages = {}
        self.build_sidebar(); self.build_pages()
        self.after(800, self.jarvis_greeting)

    def build_sidebar(self):
        tk.Label(self.sidebar, text="🛡️ SYCHO", bg="#0d1424", fg=CYAN, font=("Segoe UI", 18, "bold")).pack(pady=(20, 2))
        tk.Label(self.sidebar, text=f"J.A.R.V.I.S {VERSION}", bg="#0d1424", fg=DIM, font=("Segoe UI", 9)).pack(pady=(0, 20))
        self.nav_buttons = {}
        items = [("home","🏠 Home"),("memory","🧠 Memory"),("reminders","⏰ Reminders"),("habits","✅ Habits"),
                 ("diary","📔 Diary"),("notes","📝 Notes"),("timer","⏱️ Timer"),("todo","📋 To-Do"),
                 ("expenses","💰 Expenses"),("tools","🛠️ Tools"),("activity","📜 Activity Log"),("backup","💾 Backup")]
        for key, label in items:
            b = tk.Button(self.sidebar, text="  "+label, anchor="w", bg="#0d1424", fg=DIM, activebackground="#0a1a2a",
                          activeforeground=CYAN, relief="flat", font=("Segoe UI", 11), padx=18, pady=10,
                          command=lambda k=key, btn=None: self.show(k))
            b.pack(fill="x"); self.nav_buttons[key] = b
            b.bind("<Enter>", lambda e, x=b: x.config(fg=CYAN))
            b.bind("<Leave>", lambda e, x=b: x.config(fg=DIM))
        bottom = tk.Frame(self.sidebar, bg="#0d1424"); bottom.pack(side="bottom", fill="x", padx=12, pady=12)
        tk.Button(bottom, text="⛔ EMERGENCY STOP", bg="#3a0a0a", fg="#ff4444", relief="flat", font=("Segoe UI", 10, "bold"),
                  pady=8, command=lambda: messagebox.showwarning("EMERGENCY", "EMERGENCY STOP ACTIVATED")).pack(fill="x", pady=(0, 8))
        tk.Button(bottom, text="↻ Check Updates", bg="#0a1a2a", fg=CYAN, relief="flat", font=("Segoe UI", 10),
                  pady=8, command=self.check_updates).pack(fill="x")

    def build_pages(self):
        titles = {"home":"🏠 Home","memory":"🧠 Memory","reminders":"⏰ Reminders","habits":"✅ Habits","diary":"📔 Diary",
                  "notes":"📝 Notes","timer":"⏱️ Timer","todo":"📋 To-Do","expenses":"💰 Expenses","tools":"🛠️ Tools",
                  "activity":"📜 Activity Log","backup":"💾 Backup"}
        for key, title in titles.items():
            page = tk.Frame(self.main, bg=BG)
            tk.Label(page, text=title, bg=BG, fg=CYAN, font=("Segoe UI", 22, "bold")).pack(anchor="w", padx=30, pady=(30, 15))
            card = tk.Frame(page, bg=PANEL, highlightbackground="#1a2540", highlightthickness=1)
            card.pack(fill="both", expand=True, padx=30, pady=(0, 30))
            if key == "tools":
                tk.Label(card, text="Select a tool:", bg=PANEL, fg=TEXT, font=("Segoe UI", 11)).pack(anchor="w", padx=20, pady=(20, 5))
                combo = ttk.Combobox(card, values=["Calculator","Unit Converter","Password Generator","Quick Note"], state="readonly", font=("Segoe UI", 11))
                combo.pack(fill="x", padx=20, pady=(0, 20)); combo.set("Choose a tool...")
            elif key == "backup":
                tk.Button(card, text="💾 Create Backup", bg="#0a1a2a", fg=CYAN, relief="flat", font=("Segoe UI", 11), pady=8,
                          command=lambda: messagebox.showinfo("Backup", "Backup created ✅")).pack(padx=20, pady=20)
            else:
                tk.Label(card, text="Ready, sir.", bg=PANEL, fg=DIM, font=("Segoe UI", 12)).pack(expand=True)
            self.pages[key] = page

    def show(self, key):
        for p in self.pages.values(): p.pack_forget()
        self.pages[key].pack(fill="both", expand=True)
        for k, b in self.nav_buttons.items():
            b.config(fg=CYAN if k == key else DIM, bg="#0a1a2a" if k == key else "#0d1424")

    def check_updates(self):
        messagebox.showinfo("Updates", f"You are on the latest version: {VERSION} ✅")

    def jarvis_greeting(self):
        msg = "Hello, sir. How are you today?"
        top = tk.Toplevel(self); top.overrideredirect(True); top.attributes("-topmost", True)
        top.configure(bg=BG)
        lbl = tk.Label(top, text=msg, bg=BG, fg=CYAN, font=("Segoe UI", 22, "bold"))
        lbl.pack(padx=40, pady=25)
        self.update_idletasks()
        w, h = top.winfo_reqwidth(), top.winfo_reqheight()
        top.geometry(f"+{(self.winfo_screenwidth()-w)//2}+{int(self.winfo_screenheight()*0.15)}")
        def glow(i=0):
            if i > 20 or not top.winfo_exists(): return
            lbl.config(fg=CYAN if i % 2 == 0 else "#0088ff")
            top.after(150, glow, i+1)
        glow(); speak(msg)
        top.after(4000, top.destroy)

if __name__ == "__main__":
    app = SYCHO()
    app.show("home")
    app.mainloop()