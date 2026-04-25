import tkinter as tk
from tkinter import font as tkfont
import time
import random
import collections

# ── DPI awareness (Windows) ──────────────────────────────────────────────────
try:
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

# ══════════════════════════════════════════════════════════════════════════════
#  THEME PALETTE
# ══════════════════════════════════════════════════════════════════════════════
THEMES = {
    "printer": {
        "bg": "#FFD6E0", "elem": "#FF8FAB", "elem2": "#FF4D7A",
        "fg": "#3D0014", "btn": "#FF8FAB", "btn_fg": "#3D0014",
        "title": "#3D0014", "accent": "#FF4D7A", "card": "#FFE8EF",
        "shadow": "#FFB3C6"
    },
    "hotpotato": {
        "bg": "#C8E6FF", "elem": "#5BA4CF", "elem2": "#2176AE",
        "fg": "#002147", "btn": "#5BA4CF", "btn_fg": "#002147",
        "title": "#002147", "accent": "#2176AE", "card": "#DDF0FF",
        "shadow": "#A8D4F5"
    },
    "hospital": {
        "bg": "#C8F5E0", "elem": "#4CAF82", "elem2": "#2E7D5A",
        "fg": "#003320", "btn": "#4CAF82", "btn_fg": "#003320",
        "title": "#003320", "accent": "#2E7D5A", "card": "#DFFFF0",
        "shadow": "#A8E6C8"
    },
    "bfs": {
        "bg": "#E8D5FF", "elem": "#A67CC5", "elem2": "#6A3EA1",
        "fg": "#2D0052", "btn": "#A67CC5", "btn_fg": "#2D0052",
        "title": "#2D0052", "accent": "#6A3EA1", "card": "#F2E8FF",
        "shadow": "#CDB3F0"
    },
    "airport": {
        "bg": "#FFE5CC", "elem": "#FF9A57", "elem2": "#D4622A",
        "fg": "#4A1C00", "btn": "#FF9A57", "btn_fg": "#4A1C00",
        "title": "#4A1C00", "accent": "#D4622A", "card": "#FFF0E0",
        "shadow": "#FFD0A8"
    },
}

W, H = 1280, 800


# ══════════════════════════════════════════════════════════════════════════════
#  HELPER — rounded rectangle on canvas
# ══════════════════════════════════════════════════════════════════════════════
def rounded_rect(canvas, x1, y1, x2, y2, r=18, **kw):
    pts = [x1+r,y1, x2-r,y1, x2,y1, x2,y1+r, x2,y2-r, x2,y2,
           x2-r,y2, x1+r,y2, x1,y2, x1,y2-r, x1,y1+r, x1,y1]
    return canvas.create_polygon(pts, smooth=True, **kw)


# ══════════════════════════════════════════════════════════════════════════════
#  BASE WINDOW
# ══════════════════════════════════════════════════════════════════════════════
class BaseWindow(tk.Toplevel):
    def __init__(self, master, theme_key, title_text):
        super().__init__(master)
        self.t = THEMES[theme_key]
        self.title(title_text)
        self.geometry(f"{W}x{H}")
        self.resizable(False, False)
        self.configure(bg=self.t["bg"])
        self._anim_id = None

        # fonts
        self.f_title  = tkfont.Font(family="Times New Roman", size=26, weight="bold")
        self.f_sub    = tkfont.Font(family="Times New Roman", size=15, weight="bold")
        self.f_body   = tkfont.Font(family="Times New Roman", size=13)
        self.f_small  = tkfont.Font(family="Times New Roman", size=11)
        self.f_elem   = tkfont.Font(family="Times New Roman", size=12, weight="bold")
        self.f_btn    = tkfont.Font(family="Times New Roman", size=13, weight="bold")
        self.f_mono   = tkfont.Font(family="Courier New",     size=12)

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _on_close(self):
        if self._anim_id:
            self.after_cancel(self._anim_id)
        self.destroy()

    # ── nice button ──────────────────────────────────────────────────────────
    def make_btn(self, parent, text, cmd, width=18):
        return tk.Button(
            parent, text=text, command=cmd, font=self.f_btn,
            bg=self.t["btn"], fg=self.t["btn_fg"],
            activebackground=self.t["elem2"], activeforeground="#ffffff",
            relief="flat", bd=0, padx=14, pady=8, cursor="hand2", width=width
        )

    # ── log panel ────────────────────────────────────────────────────────────
    def make_log(self, parent, height=10):
        frame = tk.Frame(parent, bg=self.t["card"], bd=0)
        sb = tk.Scrollbar(frame)
        lb = tk.Text(frame, font=self.f_small, bg=self.t["card"],
                     fg=self.t["fg"], height=height, width=42,
                     relief="flat", state="disabled", yscrollcommand=sb.set,
                     wrap="word", padx=8, pady=6)
        sb.config(command=lb.yview)
        sb.pack(side="right", fill="y")
        lb.pack(side="left", fill="both", expand=True)
        return frame, lb

    def log(self, widget, msg):
        widget.config(state="normal")
        widget.insert("end", msg + "\n")
        widget.see("end")
        widget.config(state="disabled")


# ══════════════════════════════════════════════════════════════════════════════
#  KASUS 1 — PRINTER QUEUE
# ══════════════════════════════════════════════════════════════════════════════
class PrinterWindow(BaseWindow):
    DOCS = ["laporan.pdf","tugas.docx","foto.jpg","resume.pdf",
            "proposal.pptx","data.xlsx","skripsi.pdf","surat.docx"]
    ICONS = {"pdf":"📄","docx":"📝","xlsx":"📊","pptx":"📑","jpg":"🖼️"}

    def __init__(self, master):
        super().__init__(master, "printer", "Kasus 1 — Antrian Printer")
        self.queue = collections.deque()
        self.printing = False
        self._build()

    def _icon(self, name):
        ext = name.rsplit(".",1)[-1]
        return self.ICONS.get(ext,"📄")

    def _build(self):
        t = self.t
        # title bar
        tk.Label(self, text="🖨️  Antrian Printer Bersama", font=self.f_title,
                 bg=t["bg"], fg=t["title"]).pack(pady=(22,4))
        tk.Label(self, text="Dokumen dicetak sesuai urutan kedatangan (FIFO)",
                 font=self.f_body, bg=t["bg"], fg=t["fg"]).pack()

        # canvas for queue visual
        self.canvas = tk.Canvas(self, width=W-40, height=200,
                                bg=t["card"], highlightthickness=0)
        self.canvas.pack(padx=20, pady=14)

        # printer status
        self.status_var = tk.StringVar(value="🖨️  Printer siap")
        tk.Label(self, textvariable=self.status_var, font=self.f_sub,
                 bg=t["bg"], fg=t["accent"]).pack(pady=4)

        # controls
        ctrl = tk.Frame(self, bg=t["bg"])
        ctrl.pack(pady=6)
        for doc in self.DOCS[:4]:
            self.make_btn(ctrl, f"➕ {doc}", lambda d=doc: self._enqueue(d), width=20).pack(side="left", padx=6)

        ctrl2 = tk.Frame(self, bg=t["bg"])
        ctrl2.pack(pady=4)
        for doc in self.DOCS[4:]:
            self.make_btn(ctrl2, f"➕ {doc}", lambda d=doc: self._enqueue(d), width=20).pack(side="left", padx=6)

        ctrl3 = tk.Frame(self, bg=t["bg"])
        ctrl3.pack(pady=8)
        self.make_btn(ctrl3, "▶ Cetak Berikutnya", self._print_next, width=22).pack(side="left", padx=10)
        self.make_btn(ctrl3, "⚡ Cetak Semua", self._print_all, width=22).pack(side="left", padx=10)
        self.make_btn(ctrl3, "🗑 Reset", self._reset, width=14).pack(side="left", padx=10)

        # log
        lf, self.log_widget = self.make_log(self, height=8)
        lf.pack(padx=20, pady=6, fill="x")

        self._draw()

    def _draw(self):
        c = self.canvas
        t = self.t
        c.delete("all")
        items = list(self.queue)
        if not items:
            c.create_text(W//2-20, 100, text="— Antrian Kosong —",
                          font=self.f_sub, fill=t["fg"])
            return

        box_w, box_h, gap = 160, 80, 16
        total = len(items) * (box_w + gap) - gap
        start_x = max(20, (W-40-total)//2)
        y = 60

        # arrow label
        c.create_text(start_x-10, y+40, text="KELUAR\n←", font=self.f_small,
                      fill=t["accent"], anchor="e")

        for i, doc in enumerate(items):
            x = start_x + i*(box_w+gap)
            color = t["elem"] if i > 0 else t["elem2"]
            rounded_rect(c, x, y, x+box_w, y+box_h, r=14,
                         fill=color, outline=t["shadow"], width=2)
            icon = self._icon(doc)
            c.create_text(x+box_w//2, y+22, text=icon, font=self.f_title)
            c.create_text(x+box_w//2, y+58, text=doc, font=self.f_elem,
                          fill="#fff", width=box_w-10)
            if i == 0:
                c.create_text(x+box_w//2, y+box_h+14, text="▲ front",
                              font=self.f_small, fill=t["accent"])
            if i == len(items)-1:
                c.create_text(x+box_w//2, y+box_h+14, text="▲ rear",
                              font=self.f_small, fill=t["fg"])
            # arrow between
            if i < len(items)-1:
                ax = x+box_w+2
                c.create_line(ax, y+40, ax+gap-2, y+40,
                              fill=t["fg"], width=2, arrow="last")

        end_x = start_x + len(items)*(box_w+gap) + 10
        c.create_text(end_x, y+40, text="→\nMASUK", font=self.f_small,
                      fill=t["accent"], anchor="w")

    def _enqueue(self, doc):
        self.queue.append(doc)
        self.log(self.log_widget, f"➕ enqueue: {doc}  |  queue size = {len(self.queue)}")
        self._draw()

    def _print_next(self):
        if not self.queue:
            self.log(self.log_widget, "⚠️  Antrian kosong!"); return
        doc = self.queue.popleft()
        self.status_var.set(f"🖨️  Sedang mencetak: {doc} ...")
        self.log(self.log_widget, f"🖨️  dequeue → mencetak: {doc}")
        self._draw()
        self.after(1200, lambda: self.status_var.set("✅  Selesai! Printer siap."))

    def _print_all(self):
        if not self.queue: return
        self._print_next()
        if self.queue:
            self._anim_id = self.after(1400, self._print_all)

    def _reset(self):
        self.queue.clear()
        self.status_var.set("🖨️  Printer siap")
        self.log(self.log_widget, "🗑  Queue direset.")
        self._draw()


# ══════════════════════════════════════════════════════════════════════════════
#  KASUS 2 — HOT POTATO
# ══════════════════════════════════════════════════════════════════════════════
class HotPotatoWindow(BaseWindow):
    DEFAULT_NAMES = ["Alice","Bob","Citra","Dedi","Eka","Fajar","Gita","Hana"]

    def __init__(self, master):
        super().__init__(master, "hotpotato", "Kasus 2 — Hot Potato")
        self.players = []
        self.num_pass = 5
        self.step_idx = 0
        self.eliminated = []
        self._build()

    def _build(self):
        t = self.t
        tk.Label(self, text="🥔  Permainan Hot Potato", font=self.f_title,
                 bg=t["bg"], fg=t["title"]).pack(pady=(18,2))
        tk.Label(self, text="Pemain melingkar — oper benda N kali, yang pegang tersingkir!",
                 font=self.f_body, bg=t["bg"], fg=t["fg"]).pack()

        # config row
        cfg = tk.Frame(self, bg=t["bg"])
        cfg.pack(pady=8)
        tk.Label(cfg, text="Pemain:", font=self.f_body, bg=t["bg"], fg=t["fg"]).pack(side="left")
        self.entry = tk.Entry(cfg, font=self.f_body, width=38, relief="flat",
                              bg=t["card"], fg=t["fg"])
        self.entry.insert(0, ", ".join(self.DEFAULT_NAMES))
        self.entry.pack(side="left", padx=8)
        tk.Label(cfg, text="  N:", font=self.f_body, bg=t["bg"], fg=t["fg"]).pack(side="left")
        self.num_var = tk.IntVar(value=5)
        tk.Spinbox(cfg, from_=1, to=20, textvariable=self.num_var, width=4,
                   font=self.f_body, bg=t["card"], fg=t["fg"], relief="flat").pack(side="left", padx=4)

        self.canvas = tk.Canvas(self, width=W-40, height=290,
                                bg=t["card"], highlightthickness=0)
        self.canvas.pack(padx=20, pady=8)

        self.info_var = tk.StringVar(value="Tekan 'Mulai' untuk memulai permainan")
        tk.Label(self, textvariable=self.info_var, font=self.f_sub,
                 bg=t["bg"], fg=t["accent"]).pack(pady=4)

        ctrl = tk.Frame(self, bg=t["bg"])
        ctrl.pack(pady=6)
        self.make_btn(ctrl, "▶ Mulai / Reset", self._start, width=20).pack(side="left", padx=8)
        self.make_btn(ctrl, "⏭ Step", self._step, width=16).pack(side="left", padx=8)
        self.make_btn(ctrl, "⚡ Auto Selesai", self._auto, width=20).pack(side="left", padx=8)

        lf, self.log_widget = self.make_log(self, height=7)
        lf.pack(padx=20, pady=6, fill="x")

    def _start(self):
        if self._anim_id:
            self.after_cancel(self._anim_id); self._anim_id = None
        raw = self.entry.get()
        self.players = collections.deque([n.strip() for n in raw.split(",") if n.strip()])
        self.num_pass = self.num_var.get()
        self.eliminated = []
        self.step_idx = 0
        self.log(self.log_widget, f"▶ Mulai! {len(self.players)} pemain, N={self.num_pass}")
        self._draw()
        self.info_var.set(f"Pemain: {', '.join(self.players)}")

    def _step(self):
        if len(self.players) <= 1:
            if self.players:
                self.info_var.set(f"🏆 Pemenang: {self.players[0]}!")
                self.log(self.log_widget, f"🏆 Pemenang: {self.players[0]}!")
            return
        # pass N times
        for _ in range(self.num_pass):
            self.players.append(self.players.popleft())
        elim = self.players.popleft()
        self.eliminated.append(elim)
        self.log(self.log_widget, f"❌ Tersingkir: {elim}  |  sisa: {list(self.players)}")
        self.info_var.set(f"❌ {elim} tersingkir! Sisa {len(self.players)} pemain.")
        self._draw()
        if len(self.players) == 1:
            self.info_var.set(f"🏆 Pemenang: {self.players[0]}!")
            self.log(self.log_widget, f"🏆 Pemenang: {self.players[0]}!")

    def _auto(self):
        if len(self.players) <= 1: return
        self._step()
        if len(self.players) > 1:
            self._anim_id = self.after(900, self._auto)

    def _draw(self):
        c = self.canvas
        t = self.t
        c.delete("all")
        players = list(self.players)
        if not players:
            c.create_text(W//2-20, 145, text="— Belum ada pemain —",
                          font=self.f_sub, fill=t["fg"]); return

        n = len(players)
        cx, cy, r = (W-40)//2, 140, min(110, 30*n)
        import math
        for i, name in enumerate(players):
            angle = math.pi/2 - 2*math.pi*i/n
            px = cx + r*math.cos(angle)
            py = cy - r*math.sin(angle)
            color = t["elem2"] if i == 0 else t["elem"]
            rounded_rect(c, px-44, py-22, px+44, py+22, r=12,
                         fill=color, outline=t["shadow"], width=2)
            c.create_text(px, py, text=name, font=self.f_elem, fill="#fff")
            if i == 0:
                c.create_text(px, py+34, text="🥔", font=self.f_title)

        # eliminated list
        if self.eliminated:
            c.create_text(20, 260, anchor="w",
                          text="❌ Tersingkir: " + ", ".join(self.eliminated),
                          font=self.f_small, fill=t["fg"])


# ══════════════════════════════════════════════════════════════════════════════
#  KASUS 3 — ANTRIAN RUMAH SAKIT (Priority Queue)
# ══════════════════════════════════════════════════════════════════════════════
class HospitalWindow(BaseWindow):
    PRIORITY_LABEL = {0:"🔴 Kritis", 1:"🟠 Darurat", 2:"🟡 Menengah", 3:"🟢 Ringan"}
    PRIORITY_COLOR = {0:"#E53935", 1:"#FF7043", 2:"#FDD835", 3:"#43A047"}
    PRIORITY_FG    = {0:"#fff",    1:"#fff",    2:"#333",   3:"#fff"}

    def __init__(self, master):
        super().__init__(master, "hospital", "Kasus 3 — Antrian Rumah Sakit")
        # BPriorityQueue: list of deques, index = priority
        self.bpq = [collections.deque() for _ in range(4)]
        self.served = []
        self._build()

    def _count(self):
        return sum(len(q) for q in self.bpq)

    def _build(self):
        t = self.t
        tk.Label(self, text="🏥  Antrian Rumah Sakit — Priority Queue", font=self.f_title,
                 bg=t["bg"], fg=t["title"]).pack(pady=(18,2))
        tk.Label(self, text="Pasien darurat didahulukan — bukan murni FIFO",
                 font=self.f_body, bg=t["bg"], fg=t["fg"]).pack()

        # input
        inp = tk.Frame(self, bg=t["bg"])
        inp.pack(pady=8)
        tk.Label(inp, text="Nama:", font=self.f_body, bg=t["bg"], fg=t["fg"]).pack(side="left")
        self.name_entry = tk.Entry(inp, font=self.f_body, width=14, relief="flat",
                                   bg=t["card"], fg=t["fg"])
        self.name_entry.pack(side="left", padx=6)
        tk.Label(inp, text="Prioritas:", font=self.f_body, bg=t["bg"], fg=t["fg"]).pack(side="left")
        self.prio_var = tk.IntVar(value=2)
        for v, lbl in self.PRIORITY_LABEL.items():
            tk.Radiobutton(inp, text=lbl, variable=self.prio_var, value=v,
                           font=self.f_small, bg=t["bg"], fg=t["fg"],
                           selectcolor=t["elem"], activebackground=t["bg"]).pack(side="left", padx=4)
        self.make_btn(inp, "➕ Daftarkan", self._enqueue, width=14).pack(side="left", padx=10)

        self.canvas = tk.Canvas(self, width=W-40, height=240,
                                bg=t["card"], highlightthickness=0)
        self.canvas.pack(padx=20, pady=8)

        self.status_var = tk.StringVar(value="Antrian kosong — daftarkan pasien")
        tk.Label(self, textvariable=self.status_var, font=self.f_sub,
                 bg=t["bg"], fg=t["accent"]).pack(pady=4)

        ctrl = tk.Frame(self, bg=t["bg"])
        ctrl.pack(pady=4)
        self.make_btn(ctrl, "▶ Layani Berikutnya", self._dequeue, width=22).pack(side="left", padx=8)
        self.make_btn(ctrl, "⚡ Layani Semua", self._serve_all, width=20).pack(side="left", padx=8)
        self.make_btn(ctrl, "🗑 Reset", self._reset, width=12).pack(side="left", padx=8)

        lf, self.log_widget = self.make_log(self, height=7)
        lf.pack(padx=20, pady=4, fill="x")
        self._draw()

    def _draw(self):
        c = self.canvas
        t = self.t
        c.delete("all")
        lane_h = 52
        pad = 16
        for prio in range(4):
            y = pad + prio * lane_h
            label = self.PRIORITY_LABEL[prio]
            lc = self.PRIORITY_COLOR[prio]
            rounded_rect(c, 8, y, 170, y+lane_h-6, r=10,
                         fill=lc, outline="", width=0)
            c.create_text(90, y+(lane_h-6)//2, text=label,
                          font=self.f_elem, fill=self.PRIORITY_FG[prio])
            # patients
            for j, name in enumerate(self.bpq[prio]):
                x = 188 + j*110
                rounded_rect(c, x, y+4, x+100, y+lane_h-10, r=10,
                             fill=t["elem"], outline=t["shadow"], width=2)
                c.create_text(x+50, y+(lane_h-6)//2, text=name,
                              font=self.f_elem, fill=t["fg"])
                if j == 0 and prio == 0:
                    pass  # first always
        c.create_text(W//2-20, 228, text=f"Total antrian: {self._count()} pasien",
                      font=self.f_small, fill=t["fg"])

    def _enqueue(self):
        name = self.name_entry.get().strip()
        if not name: name = f"Pasien{self._count()+1}"
        prio = self.prio_var.get()
        self.bpq[prio].append(name)
        self.log(self.log_widget,
                 f"➕ {name} ({self.PRIORITY_LABEL[prio]}) masuk antrian")
        self.name_entry.delete(0, "end")
        self._draw()

    def _dequeue(self):
        for prio in range(4):
            if self.bpq[prio]:
                name = self.bpq[prio].popleft()
                self.served.append(name)
                self.status_var.set(f"✅ Melayani: {name} ({self.PRIORITY_LABEL[prio]})")
                self.log(self.log_widget,
                         f"▶ Dilayani: {name} ({self.PRIORITY_LABEL[prio]})")
                self._draw()
                return
        self.status_var.set("⚠️ Antrian kosong!")

    def _serve_all(self):
        if self._count() == 0: return
        self._dequeue()
        if self._count() > 0:
            self._anim_id = self.after(700, self._serve_all)

    def _reset(self):
        self.bpq = [collections.deque() for _ in range(4)]
        self.served.clear()
        self.status_var.set("Antrian kosong — daftarkan pasien")
        self.log(self.log_widget, "🗑 Queue direset.")
        self._draw()


# ══════════════════════════════════════════════════════════════════════════════
#  KASUS 4 — BFS
# ══════════════════════════════════════════════════════════════════════════════
class BFSWindow(BaseWindow):
    GRAPH = {
        "A": ["B","C"],
        "B": ["A","D","E"],
        "C": ["A","F"],
        "D": ["B"],
        "E": ["B","F"],
        "F": ["C","E","G"],
        "G": ["F"],
    }
    POS = {
        "A": (130,130), "B": (290,80), "C": (290,190),
        "D": (450,40),  "E": (450,130),"F": (450,200),
        "G": (600,170),
    }

    def __init__(self, master):
        super().__init__(master, "bfs", "Kasus 4 — BFS (Breadth-First Search)")
        self.visited = set()
        self.bfs_queue = collections.deque()
        self.order = []
        self._build()

    def _build(self):
        t = self.t
        tk.Label(self, text="🔍  BFS — Breadth-First Search", font=self.f_title,
                 bg=t["bg"], fg=t["title"]).pack(pady=(18,2))
        tk.Label(self, text="Pencarian jalur terpendek pada graf menggunakan queue",
                 font=self.f_body, bg=t["bg"], fg=t["fg"]).pack()

        top = tk.Frame(self, bg=t["bg"])
        top.pack(fill="x", padx=20, pady=6)

        self.canvas = tk.Canvas(top, width=720, height=280,
                                bg=t["card"], highlightthickness=0)
        self.canvas.pack(side="left", padx=(0,12))

        right = tk.Frame(top, bg=t["bg"])
        right.pack(side="left", fill="y")

        tk.Label(right, text="Queue saat ini:", font=self.f_sub,
                 bg=t["bg"], fg=t["fg"]).pack(anchor="w")
        self.q_canvas = tk.Canvas(right, width=460, height=70,
                                  bg=t["card"], highlightthickness=0)
        self.q_canvas.pack(pady=4)

        tk.Label(right, text="Urutan kunjungan:", font=self.f_sub,
                 bg=t["bg"], fg=t["fg"]).pack(anchor="w", pady=(8,0))
        self.order_var = tk.StringVar(value="—")
        tk.Label(right, textvariable=self.order_var, font=self.f_mono,
                 bg=t["card"], fg=t["fg"], wraplength=440, justify="left",
                 relief="flat", padx=8, pady=6).pack(fill="x")

        tk.Label(right, text="Mulai dari node:", font=self.f_body,
                 bg=t["bg"], fg=t["fg"]).pack(anchor="w", pady=(12,0))
        self.start_var = tk.StringVar(value="A")
        row = tk.Frame(right, bg=t["bg"])
        row.pack(anchor="w")
        for n in self.GRAPH:
            tk.Radiobutton(row, text=n, variable=self.start_var, value=n,
                           font=self.f_body, bg=t["bg"], fg=t["fg"],
                           selectcolor=t["elem"], activebackground=t["bg"]).pack(side="left", padx=3)

        ctrl = tk.Frame(right, bg=t["bg"])
        ctrl.pack(pady=8, anchor="w")
        self.make_btn(ctrl, "▶ Mulai / Reset", self._start, width=18).pack(side="left", padx=4)
        self.make_btn(ctrl, "⏭ Step", self._step, width=12).pack(side="left", padx=4)
        self.make_btn(ctrl, "⚡ Auto", self._auto, width=10).pack(side="left", padx=4)

        lf, self.log_widget = self.make_log(self, height=8)
        lf.pack(padx=20, pady=4, fill="x")

        self._draw_graph()

    def _draw_graph(self):
        c = self.canvas
        t = self.t
        c.delete("all")
        # edges
        for node, neighbors in self.GRAPH.items():
            x1,y1 = self.POS[node]
            for nb in neighbors:
                x2,y2 = self.POS[nb]
                c.create_line(x1,y1,x2,y2, fill=t["shadow"], width=2)
        # nodes
        r = 28
        for node,(x,y) in self.POS.items():
            if node in self.visited:
                fill = t["elem2"]
            elif self.bfs_queue and self.bfs_queue[0]==node:
                fill = t["accent"]
            elif node in self.bfs_queue:
                fill = t["elem"]
            else:
                fill = t["card"]
            c.create_oval(x-r,y-r,x+r,y+r, fill=fill,
                          outline=t["fg"], width=2)
            c.create_text(x, y, text=node, font=self.f_sub,
                          fill=t["fg"] if fill==t["card"] else "#fff")

        # legend
        legend = [("⬜ Belum", t["card"]), ("🟦 Di Queue", t["elem"]),
                  ("🟪 Proses", t["accent"]), ("🟩 Selesai", t["elem2"])]
        for i,(lbl,col) in enumerate(legend):
            c.create_rectangle(10, 235+i*0, 24, 249+i*0,
                               fill=col, outline=t["fg"])
        c.create_text(20, 260, anchor="w",
                      text="⬜ Belum  🟦 Dalam Queue  🟪 Sedang Diproses  🟩 Dikunjungi",
                      font=self.f_small, fill=t["fg"])

    def _draw_queue(self):
        c = self.q_canvas
        t = self.t
        c.delete("all")
        items = list(self.bfs_queue)
        if not items:
            c.create_text(230, 35, text="— Queue Kosong —",
                          font=self.f_sub, fill=t["fg"]); return
        box_w = 52
        for i,nd in enumerate(items):
            x = 10 + i*(box_w+8)
            rounded_rect(c, x, 10, x+box_w, 60, r=10,
                         fill=t["elem"], outline=t["shadow"], width=2)
            c.create_text(x+box_w//2, 35, text=nd, font=self.f_sub, fill="#fff")
            if i==0:
                c.create_text(x+box_w//2, 65, text="front",
                              font=self.f_small, fill=t["accent"])

    def _start(self):
        if self._anim_id:
            self.after_cancel(self._anim_id); self._anim_id=None
        self.visited = set()
        self.bfs_queue = collections.deque()
        self.order = []
        start = self.start_var.get()
        self.bfs_queue.append(start)
        self.visited.add(start)
        self.log(self.log_widget, f"▶ BFS mulai dari node {start}")
        self._draw_graph(); self._draw_queue()
        self.order_var.set("—")

    def _step(self):
        if not self.bfs_queue:
            self.log(self.log_widget, "✅ BFS selesai!"); return
        node = self.bfs_queue.popleft()
        self.order.append(node)
        self.log(self.log_widget,
                 f"dequeue → proses {node} | tetangga: {self.GRAPH[node]}")
        for nb in self.GRAPH[node]:
            if nb not in self.visited:
                self.visited.add(nb)
                self.bfs_queue.append(nb)
                self.log(self.log_widget, f"  enqueue {nb}")
        self.order_var.set(" → ".join(self.order))
        self._draw_graph(); self._draw_queue()
        if not self.bfs_queue:
            self.log(self.log_widget, "✅ BFS selesai!")

    def _auto(self):
        if not self.bfs_queue: return
        self._step()
        if self.bfs_queue:
            self._anim_id = self.after(800, self._auto)


# ══════════════════════════════════════════════════════════════════════════════
#  KASUS 5 — SIMULASI LOKET BANDARA
# ══════════════════════════════════════════════════════════════════════════════
class AirportWindow(BaseWindow):
    def __init__(self, master):
        super().__init__(master, "airport", "Kasus 5 — Simulasi Loket Bandara")
        self.running = False
        self._build()

    def _build(self):
        t = self.t
        tk.Label(self, text="✈️  Simulasi Loket Tiket Bandara", font=self.f_title,
                 bg=t["bg"], fg=t["title"]).pack(pady=(18,2))
        tk.Label(self, text="Discrete event simulation — rata-rata waktu tunggu penumpang",
                 font=self.f_body, bg=t["bg"], fg=t["fg"]).pack()

        # params
        prm = tk.Frame(self, bg=t["bg"])
        prm.pack(pady=8)
        params = [("Menit simulasi:", "num_min", 60, 1, 300),
                  ("Jumlah agen:", "num_agt", 2, 1, 10),
                  ("Waktu layanan (mnt):", "srv_time", 5, 1, 30),
                  ("Interval kedatangan:", "between", 3, 1, 20)]
        self.pvars = {}
        for label, key, default, mn, mx in params:
            tk.Label(prm, text=label, font=self.f_body, bg=t["bg"], fg=t["fg"]).pack(side="left", padx=4)
            v = tk.IntVar(value=default)
            self.pvars[key] = v
            tk.Spinbox(prm, from_=mn, to=mx, textvariable=v, width=4,
                       font=self.f_body, bg=t["card"], fg=t["fg"], relief="flat").pack(side="left", padx=2)

        self.canvas = tk.Canvas(self, width=W-40, height=220,
                                bg=t["card"], highlightthickness=0)
        self.canvas.pack(padx=20, pady=8)

        self.stats_var = tk.StringVar(value="Atur parameter lalu tekan ▶ Jalankan")
        tk.Label(self, textvariable=self.stats_var, font=self.f_sub,
                 bg=t["bg"], fg=t["accent"]).pack(pady=4)

        ctrl = tk.Frame(self, bg=t["bg"])
        ctrl.pack(pady=4)
        self.run_btn = self.make_btn(ctrl, "▶ Jalankan Simulasi", self._run, width=22)
        self.run_btn.pack(side="left", padx=8)
        self.make_btn(ctrl, "🗑 Reset", self._reset, width=12).pack(side="left", padx=8)

        lf, self.log_widget = self.make_log(self, height=8)
        lf.pack(padx=20, pady=4, fill="x")

    def _run(self):
        t = self.t
        num_min  = self.pvars["num_min"].get()
        num_agt  = self.pvars["num_agt"].get()
        srv_time = self.pvars["srv_time"].get()
        between  = self.pvars["between"].get()

        queue     = collections.deque()
        agents    = [None]*num_agt  # None=free, else (end_time, wait)
        total_wait= 0
        num_served= 0
        arrivals  = 0

        # run full simulation instantly, collect timeline for chart
        timeline = []  # (tick, q_len, busy_agents)

        for tick in range(num_min+1):
            # R1: Jika penumpang tiba → enqueue
            if random.random() < 1/between:
                queue.append(tick)
                arrivals += 1

            # R2: Jika agen free & queue tidak kosong → dequeue, mulai layani
            for i in range(num_agt):
                if agents[i] is None and queue:
                    arr_time = queue.popleft()
                    wait = tick - arr_time
                    agents[i] = (tick + srv_time, wait)

            # R3: Jika transaksi selesai → penumpang keluar, agen free
            for i in range(num_agt):
                if agents[i] and agents[i][0] == tick:
                    total_wait += agents[i][1]
                    num_served += 1
                    agents[i] = None

            busy = sum(1 for a in agents if a is not None)
            timeline.append((tick, len(queue), busy))

        avg_wait = total_wait/num_served if num_served else 0
        self.stats_var.set(
            f"✈️  Tiba: {arrivals}  |  Dilayani: {num_served}  |"
            f"  Rata-rata tunggu: {avg_wait:.2f} mnt  |  Agen: {num_agt}"
        )
        self.log(self.log_widget,
                 f"Simulasi selesai! Tiba={arrivals}, Dilayani={num_served}, "
                 f"Avg wait={avg_wait:.2f} mnt")

        self._draw_chart(timeline, num_agt)

    def _draw_chart(self, timeline, num_agt):
        c = self.canvas
        t = self.t
        c.delete("all")
        if not timeline: return

        cw, ch = W-40, 220
        pad_l, pad_r, pad_t, pad_b = 60, 20, 20, 40
        plot_w = cw - pad_l - pad_r
        plot_h = ch - pad_t - pad_b

        max_q = max(x[1] for x in timeline) or 1
        ticks = len(timeline)

        # axes
        c.create_line(pad_l, pad_t, pad_l, ch-pad_b, fill=t["fg"], width=2)
        c.create_line(pad_l, ch-pad_b, cw-pad_r, ch-pad_b, fill=t["fg"], width=2)
        c.create_text(pad_l-8, pad_t, text=str(max_q), font=self.f_small,
                      fill=t["fg"], anchor="e")
        c.create_text(pad_l-8, ch-pad_b, text="0", font=self.f_small,
                      fill=t["fg"], anchor="e")
        c.create_text(cw//2, ch-8, text="Waktu (menit)", font=self.f_small,
                      fill=t["fg"])
        c.create_text(12, ch//2, text="Antrian", font=self.f_small,
                      fill=t["fg"], angle=90)

        # queue length line
        pts_q = []
        pts_b = []
        for i,(tick,qlen,busy) in enumerate(timeline):
            x = pad_l + i*plot_w//(ticks-1) if ticks>1 else pad_l
            yq = ch - pad_b - int(qlen/max_q * plot_h)
            yb = ch - pad_b - int(busy/num_agt * plot_h)
            pts_q += [x, yq]
            pts_b += [x, yb]

        if len(pts_q) >= 4:
            c.create_line(*pts_q, fill=t["elem2"], width=2, smooth=True)
            c.create_line(*pts_b, fill=t["accent"], width=2, smooth=True, dash=(6,3))

        # legend
        c.create_line(cw-200, 15, cw-175, 15, fill=t["elem2"], width=2)
        c.create_text(cw-170, 15, anchor="w", text="Panjang antrian",
                      font=self.f_small, fill=t["fg"])
        c.create_line(cw-200, 32, cw-175, 32, fill=t["accent"], width=2, dash=(6,3))
        c.create_text(cw-170, 32, anchor="w", text="Agen sibuk (proporsi)",
                      font=self.f_small, fill=t["fg"])

    def _reset(self):
        self.canvas.delete("all")
        self.stats_var.set("Atur parameter lalu tekan ▶ Jalankan")
        self.log(self.log_widget, "🗑 Direset.")


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN MENU
# ══════════════════════════════════════════════════════════════════════════════
class MainMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Queue Visualizer — Struktur Data & Algoritma")
        self.geometry("760x660")
        self.minsize(760, 660)
        self.resizable(True, True)
        self.configure(bg="#F5F0FF")
        self._build()

    def _build(self):
        tf = tkfont.Font(family="Times New Roman", size=28, weight="bold")
        sf = tkfont.Font(family="Times New Roman", size=14)
        bf = tkfont.Font(family="Times New Roman", size=14, weight="bold")

        tk.Label(self, text="🗂️  Queue Visualizer", font=tf,
                 bg="#F5F0FF", fg="#2D0052").pack(pady=(36,4))
        tk.Label(self, text="Pilih kasus untuk membuka visualisasi animasi",
                 font=sf, bg="#F5F0FF", fg="#555").pack(pady=(0,24))

        cases = [
            ("🖨️  Kasus 1 — Antrian Printer",         "#FFD6E0", "#3D0014", PrinterWindow),
            ("🥔  Kasus 2 — Hot Potato",               "#C8E6FF", "#002147", HotPotatoWindow),
            ("🏥  Kasus 3 — Antrian Rumah Sakit",      "#C8F5E0", "#003320", HospitalWindow),
            ("🔍  Kasus 4 — BFS (Graph Traversal)",    "#E8D5FF", "#2D0052", BFSWindow),
            ("✈️  Kasus 5 — Simulasi Loket Bandara",   "#FFE5CC", "#4A1C00", AirportWindow),
        ]

        for label, bg, fg, cls in cases:
            btn = tk.Button(
                self, text=label, font=bf, bg=bg, fg=fg,
                activebackground=fg, activeforeground=bg,
                relief="flat", bd=0, padx=20, pady=14, cursor="hand2",
                width=44,
                command=lambda c=cls: c(self)
            )
            btn.pack(pady=6)

        tk.Label(self, text="Struktur Data & Algoritma  •  Times New Roman  •  Pastel Theme",
                 font=tkfont.Font(family="Times New Roman", size=11),
                 bg="#F5F0FF", fg="#aaa").pack(side="bottom", pady=12)


if __name__ == "__main__":
    app = MainMenu()
    app.mainloop()