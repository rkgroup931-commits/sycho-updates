
# SYCHO v1.2.0 - Auto-build ready. Upload run.py to GitHub -> Actions builds EXE automatically.
import tkinter as tk
from tkinter import ttk, messagebox
import json, os, hashlib, urllib.request, zipfile, threading, datetime, random, subprocess, sys, shutil
APP="SYCHO"; VERSION="1.2.0"
DATA=os.path.join(os.path.expanduser("~"), ".sycho"); os.makedirs(DATA, exist_ok=True)
CONFIG=os.path.join(DATA,"config.json"); MANIFEST_URL="https://rkgroup931-commits.github.io/sycho-updates/manifest.json"
BG,CARD,FG,MUTED,ACCENT,GREEN,RED="#0d1117","#161b22","#e6edf3","#8b949e","#58a6ff","#238636","#f85149"
def load(p,d):
    try:
        with open(p,"r",encoding="utf-8") as f: return json.load(f)
    except Exception: return d
def save(p,d):
    with open(p,"w",encoding="utf-8") as f: json.dump(d,f,indent=2)
config=load(CONFIG,{})
LANGS={"English":{"briefing":"Briefing","habits":"Habits","diary":"Diary","vault":"Vault","timer":"Timer","todo":"To-Do","notes":"Notes","countdown":"Countdown","converter":"Converter","calc":"Calculator","text":"Text Tools","expenses":"Expenses","world":"World Clock","units":"Units"},
"اردو":{"briefing":"بریفنگ","habits":"عادات","diary":"ڈائری","vault":"والٹ","timer":"ٹائمر","todo":"ٹو-ڈو","notes":"نوٹس","countdown":"کاؤنٹ ڈاؤن","converter":"کنورٹر","calc":"کیلکولیٹر","text":"ٹیکسٹ ٹولز","expenses":"اخراجات","world":"ورلڈ کلاک","units":"یونٹس"},
"العربية":{"briefing":"الملخص","habits":"العادات","diary":"اليوميات","vault":"الخزنة","timer":"المؤقت","todo":"المهام","notes":"الملاحظات","countdown":"العد التنازلي","converter":"المحول","calc":"الآلة الحاسبة","text":"أدوات النص","expenses":"المصروفات","world":"ساعة عالمية","units":"الوحدات"},
"हिन्दी":{"briefing":"ब्रीफिंग","habits":"आदतें","diary":"डायरी","vault":"वॉल्ट","timer":"टाइमर","todo":"टू-डू","notes":"नोट्स","countdown":"काउंटडाउन","converter":"कनवर्टर","calc":"कैलकुलेटर","text":"टेक्स्ट टूल्स","expenses":"खर्चे","world":"वर्ल्ड क्लॉक","units":"यूनिट्स"},
"Türkçe":{"briefing":"Özet","habits":"Alışkanlıklar","diary":"Günlük","vault":"Kasa","timer":"Zamanlayıcı","todo":"Yapılacaklar","notes":"Notlar","countdown":"Geri Sayım","converter":"Dönüştürücü","calc":"Hesap Makinesi","text":"Metin Araçları","expenses":"Giderler","world":"Dünya Saati","units":"Birimler"}}
current_lang={"name":"English"}
def T(k): return LANGS[current_lang["name"]].get(k,k)
def start():
    root=tk.Tk(); root.title(APP+" v"+VERSION); root.geometry("1150x720"); root.configure(bg=BG); root.resizable(True,True)
    root.eval('tk::PlaceWindow . center')
    root.bind("<F11>",lambda e: root.attributes("-fullscreen",not root.attributes("-fullscreen")))
    def splash():
        for w in root.winfo_children(): w.destroy()
        frame=tk.Frame(root,bg=BG); frame.place(relx=0.5,rely=0.5,anchor="center")
        def draw(scale,alpha):
            for w in frame.winfo_children(): w.destroy()
            tk.Label(frame,text="\U0001F6E1\uFE0F",font=("Segoe UI Emoji",int(100*scale)),bg=BG,fg=ACCENT).pack()
            tk.Label(frame,text="SYCHO",font=("Segoe UI",int(52*scale),"bold"),bg=BG,fg=FG).pack()
            tk.Label(frame,text="Your personal command center",font=("Segoe UI",13),bg=BG,fg=MUTED).pack(pady=8)
            root.attributes("-alpha",min(alpha,1.0))
        draw(1.0,0.0)
        def anim(step=0,alpha=0.0,scale=1.0):
            if step<20:
                alpha+=0.05; scale+=0.015; draw(scale,alpha); root.after(30,anim,step+1,alpha,scale)
            else: root.after(1500,lock)
        anim()
    def lock():
        for w in root.winfo_children(): w.destroy()
        root.attributes("-alpha",1.0)
        tk.Label(root,text="\U0001F6E1\uFE0F",font=("Segoe UI Emoji",48),bg=BG,fg=ACCENT).pack(pady=(110,10))
        tk.Label(root,text="Welcome back",font=("Segoe UI",22,"bold"),bg=BG,fg=FG).pack()
        tk.Label(root,text="Please enter your password to continue",font=("Segoe UI",11),bg=BG,fg=MUTED).pack(pady=6)
        e=tk.Entry(root,show="\u25CF",font=("Segoe UI",14),width=26,justify="center",bg=CARD,fg=FG,insertbackground=FG,relief="flat"); e.pack(ipady=9,pady=16)
        msg=tk.Label(root,text="",bg=BG,fg=RED,font=("Segoe UI",10))
        def check(ev=None):
            pw=hashlib.sha256(e.get().encode()).hexdigest()
            if "password" not in config: config["password"]=pw; save(CONFIG,config); main()
            elif pw==config["password"]: main()
            else: msg.config(text="Incorrect password. Try again."); msg.pack(pady=8)
        e.bind("<Return>",check); e.focus(); msg.pack(pady=8); root.after(200,e.focus)
    def main(): build_main(root)
    splash(); root.mainloop()
def build_main(root):
    for w in root.winfo_children(): w.destroy()
    root.configure(bg=BG)
    top=tk.Frame(root,bg=BG); top.pack(fill="x",padx=16,pady=(14,6))
    tk.Label(top,text="\U0001F6E1\uFE0F SYCHO",font=("Segoe UI",16,"bold"),bg=BG,fg=FG).pack(side="left")
    tk.Label(top,text="v"+VERSION,font=("Segoe UI",10),bg=BG,fg=MUTED).pack(side="left",padx=8)
    lang=ttk.Combobox(top,values=list(LANGS),state="readonly",width=10); lang.set("English"); lang.pack(side="right",padx=8)
    tk.Button(top,text="\u21BB Check Updates",font=("Segoe UI",10),bg=CARD,fg=FG,relief="flat",padx=10,pady=4,command=lambda:check_update(root)).pack(side="right")
    tk.Label(top,text="F11 = Fullscreen",font=("Segoe UI",9),bg=BG,fg=MUTED).pack(side="right",padx=8)
    nb=ttk.Notebook(root); nb.pack(fill="both",expand=True,padx=12,pady=8)
    st=ttk.Style(); st.theme_use("clam"); st.configure("TNotebook",background=BG,borderwidth=0); st.configure("TNotebook.Tab",background=CARD,foreground=FG,padding=[10,8]); st.map("TNotebook.Tab",background=[("selected",ACCENT)])
    f=tk.Frame(nb,bg=BG); nb.add(f,text=" "+T("briefing")+" ")
    now=datetime.datetime.now(); q=["Small steps every day.","Focus on progress, not perfection.","Discipline beats motivation."]
    tk.Label(f,text=now.strftime("%A, %d %B %Y"),font=("Segoe UI",15,"bold"),bg=BG,fg=FG).pack(pady=(30,4))
    clk=tk.Label(f,text="",font=("Segoe UI",44,"bold"),bg=BG,fg=ACCENT)
    def tick():
        clk.config(text=datetime.datetime.now().strftime("%H:%M:%S")); clk.after(1000,tick)
    clk.pack(); tick()
    tk.Label(f,text="\u201C"+random.choice(q)+"\u201D",font=("Segoe UI",11,"italic"),bg=BG,fg=MUTED).pack(pady=16)
    f=tk.Frame(nb,bg=BG); nb.add(f,text=" "+T("habits")+" ")
    habits=load(os.path.join(DATA,"habits.json"),[])
    lb=tk.Listbox(f,bg=CARD,fg=FG,font=("Segoe UI",11),relief="flat",highlightthickness=0); lb.pack(fill="both",expand=True,padx=16,pady=10)
    def refresh():
        lb.delete(0,tk.END)
        for h in habits: lb.insert(tk.END,("\u2705 " if h["done"] else "\u2B1C ")+h["name"])
    def add():
        d=tk.simpledialog.askstring("New Habit","Habit name:",parent=root)
        if d: habits.append({"name":d,"done":False}); save(os.path.join(DATA,"habits.json"),habits); refresh()
    def toggle(ev=None):
        i=lb.curselection()
        if i>=0: habits[i]["done"]=not habits[i]["done"]; save(os.path.join(DATA,"habits.json"),habits); refresh()
    lb.bind("<Double-1>",toggle)
    tk.Button(f,text="+ Add Habit",bg=GREEN,fg="white",relief="flat",font=("Segoe UI",10,"bold"),padx=14,pady=6,command=add).pack(pady=8)
    refresh()
    f=tk.Frame(nb,bg=BG); nb.add(f,text=" "+T("diary")+" ")
    txt=tk.Text(f,bg=CARD,fg=FG,font=("Segoe UI",11),relief="flat",padx=12,pady=12); txt.pack(fill="both",expand=True,padx=16,pady=10)
    df=os.path.join(DATA,"diary.json"); diary=load(df,{}); today=datetime.date.today().isoformat()
    if today in diary: txt.insert("1.0",diary[today])
    def sd():
        diary[today]=txt.get("1.0","end").strip(); save(df,diary); messagebox.showinfo("Saved","Diary saved \u2705",parent=root)
    tk.Button(f,text="Save Entry",bg=ACCENT,fg="white",relief="flat",font=("Segoe UI",10,"bold"),padx=14,pady=6,command=sd).pack(pady=8)
    f=tk.Frame(nb,bg=BG); nb.add(f,text=" "+T("vault")+" ")
    vf=os.path.join(DATA,"vault.json"); vault=load(vf,[])
    vl=tk.Listbox(f,bg=CARD,fg=FG,font=("Segoe UI",11),relief="flat",highlightthickness=0); vl.pack(fill="both",expand=True,padx=16,pady=10)
    def vr(): vl.delete(0,tk.END); [vl.insert(tk.END,v["site"]+"  \u2022  "+v["user"]) for v in vault]
    def va():
        a=tk.simpledialog.askstring("Vault","Site / App:",parent=root); b=tk.simpledialog.askstring("Vault","Username:",parent=root); c=tk.simpledialog.askstring("Vault","Password:",parent=root)
        if a and b and c: vault.append({"site":a,"user":b,"pass":c}); save(vf,vault); vr()
    def vs(ev=None):
        i=vl.curselection()
        if i>=0: messagebox.showinfo("Password",vault[i]["pass"],parent=root)
    vl.bind("<Double-1>",vs)
    tk.Button(f,text="+ Add Password",bg=ACCENT,fg="white",relief="flat",font=("Segoe UI",10,"bold"),padx=14,pady=6,command=va).pack(pady=8)
    vr()
    f=tk.Frame(nb,bg=BG); nb.add(f,text=" "+T("timer")+" ")
    tk.Label(f,text="Pomodoro Timer",font=("Segoe UI",16,"bold"),bg=BG,fg=FG).pack(pady=(24,10))
    tl=tk.Label(f,text="25:00",font=("Segoe UI",52,"bold"),bg=BG,fg=ACCENT); tl.pack()
    secs={"left":1500,"run":False}
    def upd():
        m,s=divmod(secs["left"],60); tl.config(text="{:02d}:{:02d}".format(m,s))
    def run():
        if secs["run"] and secs["left"]>0:
            secs["left"]-=1; upd()
            if secs["left"]==0: messagebox.showinfo("Timer","Time is up! Take a break \u2705",parent=root); secs["left"]=1500; upd(); secs["run"]=False; return
            root.after(1000,run)
    def start_t():
        if not secs["run"]: secs["run"]=True; run()
    def pause_t(): secs["run"]=False
    def reset_t(): secs["run"]=False; secs["left"]=1500; upd()
    row=tk.Frame(f,bg=BG); row.pack(pady=14)
    for x,c in [("Start",start_t),("Pause",pause_t),("Reset",reset_t)]:
        tk.Button(row,text=x,bg=(GREEN if x=="Start" else CARD),fg="white" if x=="Start" else FG,relief="flat",font=("Segoe UI",10,"bold"),padx=14,pady=6,command=c).pack(side="left",padx=6)
    upd()
    f=tk.Frame(nb,bg=BG); nb.add(f,text=" "+T("todo")+" ")
    todos=load(os.path.join(DATA,"todos.json"),[])
    tl2=tk.Listbox(f,bg=CARD,fg=FG,font=("Segoe UI",11),relief="flat",highlightthickness=0); tl2.pack(fill="both",expand=True,padx=16,pady=10)
    def tref(): tl2.delete(0,tk.END); [tl2.insert(tk.END,("\u2705 " if t["done"] else "\u2B1C ")+t["task"]) for t in todos]
    def tadd():
        d=tk.simpledialog.askstring("New Task","Task:",parent=root)
        if d: todos.append({"task":d,"done":False}); save(os.path.join(DATA,"todos.json"),todos); tref()
    def ttoggle(ev=None):
        i=tl2.curselection()
        if i>=0: todos[i]["done"]=not todos[i]["done"]; save(os.path.join(DATA,"todos.json"),todos); tref()
    tl2.bind("<Double-1>",ttoggle)
    tk.Button(f,text="+ Add Task",bg=GREEN,fg="white",relief="flat",font=("Segoe UI",10,"bold"),padx=14,pady=6,command=tadd).pack(pady=8)
    tref()
    f=tk.Frame(nb,bg=BG); nb.add(f,text=" "+T("notes")+" ")
    nt=tk.Text(f,bg=CARD,fg=FG,font=("Segoe UI",11),relief="flat",padx=12,pady=12); nt.pack(fill="both",expand=True,padx=16,pady=10)
    nf=os.path.join(DATA,"notes.txt")
    if os.path.exists(nf): nt.insert("1.0",open(nf,encoding="utf-8").read())
    def sn():
        open(nf,"w",encoding="utf-8").write(nt.get("1.0","end")); messagebox.showinfo("Saved","Notes saved \u2705",parent=root)
    tk.Button(f,text="Save Notes",bg=ACCENT,fg="white",relief="flat",font=("Segoe UI",10,"bold"),padx=14,pady=6,command=sn).pack(pady=8)
    f=tk.Frame(nb,bg=BG); nb.add(f,text=" "+T("expenses")+" ")
    exps=load(os.path.join(DATA,"expenses.json"),[])
    el=tk.Listbox(f,bg=CARD,fg=FG,font=("Segoe UI",11),relief="flat",highlightthickness=0); el.pack(fill="both",expand=True,padx=16,pady=10)
    def eref():
        el.delete(0,tk.END); tot=0
        for x in exps: el.insert(tk.END,"{}  \u2022  {:.2f}".format(x["name"],x["amt"])); tot+=x["amt"]
        el.insert(tk.END,"--- TOTAL: {:.2f} ---".format(tot))
    def eadd():
        n=tk.simpledialog.askstring("Expense","Name:",parent=root); a=tk.simpledialog.askstring("Expense","Amount:",parent=root)
        if n and a:
            try: exps.append({"name":n,"amt":float(a)}); save(os.path.join(DATA,"expenses.json"),exps); eref()
            except Exception: pass
    tk.Button(f,text="+ Add Expense",bg=GREEN,fg="white",relief="flat",font=("Segoe UI",10,"bold"),padx=14,pady=6,command=eadd).pack(pady=8)
    eref()
    f=tk.Frame(nb,bg=BG); nb.add(f,text=" "+T("world")+" ")
    zones=[("Pakistan",5),("Dubai",4),("London",1),("New York",-4),("Tokyo",9)]
    wc=tk.Label(f,text="",font=("Segoe UI",14),bg=BG,fg=FG,justify="left")
    def wtick():
        now=datetime.datetime.utcnow()
        wc.config(text="\n".join("{}: {}".format(n,(now+datetime.timedelta(hours=h)).strftime("%H:%M")) for n,h in zones))
        wc.after(30000,wtick)
    wc.pack(pady=30); wtick()
    f=tk.Frame(nb,bg=BG); nb.add(f,text=" "+T("units")+" ")
    units={"km":1000.0,"m":1.0,"cm":0.01,"mile":1609.34,"kg":1.0,"g":0.001,"lb":0.453592}
    tk.Label(f,text="Value:",bg=BG,fg=FG,font=("Segoe UI",11)).pack(pady=(30,4))
    ue=tk.Entry(f,bg=CARD,fg=FG,relief="flat",justify="center",font=("Segoe UI",12)); ue.pack(ipady=6)
    r3=tk.Frame(f,bg=BG); r3.pack(pady=10)
    uf=ttk.Combobox(r3,values=list(units),state="readonly",width=8); uf.set("km"); uf.pack(side="left",padx=6)
    ut=ttk.Combobox(r3,values=list(units),state="readonly",width=8); ut.set("mile"); ut.pack(side="left",padx=6)
    ures=tk.Label(f,text="",font=("Segoe UI",16,"bold"),bg=BG,fg=ACCENT)
    def uconv():
        try:
            v=float(ue.get()); r=v*units[uf.get()]/units[ut.get()]; ures.config(text="{:,.4f} {}".format(r,ut.get())); ures.pack(pady=14)
        except Exception: ures.config(text="Error"); ures.pack(pady=14)
    tk.Button(f,text="Convert",bg=ACCENT,fg="white",relief="flat",font=("Segoe UI",10,"bold"),padx=14,pady=6,command=uconv).pack(pady=6)
    f=tk.Frame(nb,bg=BG); nb.add(f,text=" "+T("countdown")+" ")
    tk.Label(f,text="Days until:",font=("Segoe UI",12),bg=BG,fg=FG).pack(pady=(30,6))
    e=tk.Entry(f,bg=CARD,fg=FG,relief="flat",justify="center",font=("Segoe UI",12)); e.pack(ipady=6); e.insert(0,"2026-12-31")
    o=tk.Label(f,text="",font=("Segoe UI",22,"bold"),bg=BG,fg=ACCENT)
    def calc():
        try:
            d=(datetime.date.fromisoformat(e.get())-datetime.date.today()).days; o.config(text=str(d)+" days"); o.pack(pady=16)
        except Exception: o.config(text="Invalid date"); o.pack(pady=16)
    tk.Button(f,text="Calculate",bg=ACCENT,fg="white",relief="flat",font=("Segoe UI",10,"bold"),padx=14,pady=6,command=calc).pack(pady=8)
    f=tk.Frame(nb,bg=BG); nb.add(f,text=" "+T("converter")+" ")
    rates={"USD":1.0,"EUR":0.92,"PKR":278.0,"INR":83.0,"GBP":0.79}
    tk.Label(f,text="Amount:",bg=BG,fg=FG,font=("Segoe UI",11)).pack(pady=(30,4))
    amt=tk.Entry(f,bg=CARD,fg=FG,relief="flat",justify="center",font=("Segoe UI",12)); amt.pack(ipady=6)
    row=tk.Frame(f,bg=BG); row.pack(pady=10)
    fr=ttk.Combobox(row,values=list(rates),state="readonly",width=8); fr.set("USD"); fr.pack(side="left",padx=6)
    to=ttk.Combobox(row,values=list(rates),state="readonly",width=8); to.set("PKR"); to.pack(side="left",padx=6)
    res=tk.Label(f,text="",font=("Segoe UI",18,"bold"),bg=BG,fg=ACCENT)
    def conv():
        try:
            v=float(amt.get()); r=v/rates[fr.get()]*rates[to.get()]; res.config(text="{:,.2f} {}".format(r,to.get())); res.pack(pady=14)
        except Exception: res.config(text="Invalid amount"); res.pack(pady=14)
    tk.Button(f,text="Convert",bg=ACCENT,fg="white",relief="flat",font=("Segoe UI",10,"bold"),padx=14,pady=6,command=conv).pack(pady=6)
    f=tk.Frame(nb,bg=BG); nb.add(f,text=" "+T("calc")+" ")
    ce=tk.Entry(f,bg=CARD,fg=FG,relief="flat",justify="center",font=("Segoe UI",14)); ce.pack(ipady=8,pady=(30,10))
    cres=tk.Label(f,text="",font=("Segoe UI",20,"bold"),bg=BG,fg=ACCENT)
    def ccalc():
        try: cres.config(text="= "+str(eval(ce.get()))); cres.pack(pady=10)
        except Exception: cres.config(text="Error"); cres.pack(pady=10)
    tk.Button(f,text="Calculate",bg=ACCENT,fg="white",relief="flat",font=("Segoe UI",10,"bold"),padx=14,pady=6,command=ccalc).pack(pady=6)
    f=tk.Frame(nb,bg=BG); nb.add(f,text=" "+T("text")+" ")
    t=tk.Text(f,bg=CARD,fg=FG,font=("Segoe UI",11),relief="flat",padx=12,pady=12,height=8); t.pack(fill="x",padx=16,pady=10)
    o2=tk.Label(f,text="",bg=BG,fg=ACCENT,font=("Segoe UI",11),wraplength=360)
    def stats():
        s=t.get("1.0","end").strip(); o2.config(text="Words: {}  \u2022  Characters: {}  \u2022  Lines: {}".format(len(s.split()),len(s),len(s.splitlines()))); o2.pack(pady=8)
    def up(): t.delete("1.0","end"); t.insert("1.0",t.get("1.0","end").upper())
    def lo(): t.delete("1.0","end"); t.insert("1.0",t.get("1.0","end").lower())
    r2=tk.Frame(f,bg=BG); r2.pack()
    for x,c in [("Stats",stats),("UPPER",up),("lower",lo)]:
        tk.Button(r2,text=x,bg=CARD,fg=FG,relief="flat",font=("Segoe UI",10),padx=12,pady=5,command=c).pack(side="left",padx=5)
def check_update(root):
    try:
        with urllib.request.urlopen(MANIFEST_URL,timeout=10) as r: m=json.loads(r.read().decode())
        if m["version"]<=VERSION:
            messagebox.showinfo("Updates","You are on the latest version (v"+VERSION+") \u2705",parent=root); return
        size="..."
        try:
            rq=urllib.request.Request(m["url"],method="HEAD")
            with urllib.request.urlopen(rq,timeout=10) as r: size="{:.1f} MB".format(int(r.headers["Content-Length"])/1048576)
        except Exception: pass
        win=tk.Toplevel(root); win.title("Update Available"); win.geometry("380x240"); win.configure(bg=BG); win.resizable(False,False); win.attributes("-topmost",True)
        tk.Label(win,text="\U0001F504  Update Available",font=("Segoe UI",15,"bold"),bg=BG,fg=ACCENT).pack(pady=(24,4))
        tk.Label(win,text="SYCHO v"+m["version"],font=("Segoe UI",12),bg=BG,fg=FG).pack()
        tk.Label(win,text="Size: "+size,font=("Segoe UI",10),bg=BG,fg=MUTED).pack(pady=4)
        bar=ttk.Progressbar(win,length=300,mode="determinate"); s2=tk.Label(win,text="",bg=BG,fg=MUTED,font=("Segoe UI",9))
        def do():
            bar.pack(pady=12); s2.pack()
            def work():
                try:
                    zp=os.path.join(DATA,"update.zip"); urllib.request.urlretrieve(m["url"],zp)
                    win.after(0,lambda:(bar.config(value=70),s2.config(text="Installing\u2026")))
                    tmp=os.path.join(DATA,"update_tmp")
                    if os.path.exists(tmp): shutil.rmtree(tmp)
                    os.makedirs(tmp)
                    with zipfile.ZipFile(zp) as z: z.extractall(tmp)
                    ne=None
                    for dp,_,fs in os.walk(tmp):
                        for fn in fs:
                            if fn.lower().endswith(".exe"): ne=os.path.join(dp,fn); break
                        if ne: break
                    if not ne: win.after(0,lambda:s2.config(text="No EXE found in update zip \u274C")); return
                    ce=os.path.abspath(sys.executable if getattr(sys,"frozen",False) else sys.argv[0])
                    bat=os.path.join(DATA,"update.bat")
                    lines=["@echo off","timeout /t 2 /nobreak >nul","taskkill /f /im "+os.path.basename(ce)+" >nul 2>&1","timeout /t 1 /nobreak >nul",'copy /y "'+ne+'" "'+ce+'" >nul','rmdir /s /q "'+tmp+'"','start "" "'+ce+'"','del "%~f0"']
                    with open(bat,"w") as b: b.write("\r\n".join(lines))
                    win.after(0,lambda:(bar.config(value=100),s2.config(text="Restarting to finish update\u2026")))
                    win.after(1000,lambda:(subprocess.Popen(["cmd","/c",bat],creationflags=subprocess.CREATE_NO_WINDOW),root.destroy()))
                except Exception as e:
                    win.after(0,lambda: s2.config(text="Update failed: "+str(e)))
            threading.Thread(target=work,daemon=True).start()
        b2=tk.Frame(win,bg=BG); b2.pack(pady=14)
        tk.Button(b2,text="UPDATE NOW",bg=GREEN,fg="white",relief="flat",font=("Segoe UI",10,"bold"),padx=14,pady=6,command=do).pack(side="left",padx=8)
        tk.Button(b2,text="Later",bg=CARD,fg=FG,relief="flat",font=("Segoe UI",10),padx=14,pady=6,command=win.destroy).pack(side="left",padx=8)
    except Exception as e:
        messagebox.showerror("Updates","Could not check updates:\n"+str(e),parent=root)
if __name__=="__main__":
    import tkinter.simpledialog
    start()
