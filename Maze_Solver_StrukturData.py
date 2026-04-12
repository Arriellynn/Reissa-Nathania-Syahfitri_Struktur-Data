import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

FONT_MAIN  = "Times New Roman"
FONT_MONO  = "Courier New"

# =============================================
#   IMPLEMENTASI STACK - PYTHON LIST
# =============================================
class StackList:
    def __init__(self):
        self._items = list()

    def isEmpty(self):
        return len(self) == 0

    def __len__(self):
        return len(self._items)

    def peek(self):
        assert not self.isEmpty(), "Stack kosong!"
        return self._items[-1]

    def push(self, item):
        # Tambah ke atas (akhir list)
        self._items.append(item)

    def pop(self):
        # Hapus dari atas (akhir list)
        assert not self.isEmpty(), "Stack kosong!"
        return self._items.pop()

    def toList(self):
        return list(self._items)


# =============================================
#   IMPLEMENTASI STACK - LINKED LIST
# =============================================
class _StackNode:
    def __init__(self, item, link):
        self.item = item
        self.next = link

class StackLinked:
    def __init__(self):
        self._top = None
        self._size = 0

    def isEmpty(self):
        return self._top is None

    def __len__(self):
        return self._size

    def peek(self):
        assert not self.isEmpty(), "Stack kosong!"
        return self._top.item

    def push(self, item):
        # Node baru jadi top
        self._top = _StackNode(item, self._top)
        self._size += 1

    def pop(self):
        assert not self.isEmpty(), "Stack kosong!"
        node = self._top
        self._top = self._top.next
        self._size -= 1
        return node.item

    def toList(self):
        result = []
        cur = self._top
        while cur:
            result.append(cur.item)
            cur = cur.next
        return list(reversed(result))


# =============================================
#   MAZE GENERATOR & SOLVER
# =============================================
WALL   = 1
OPEN   = 0
PATH   = 2
TRIED  = 3
START  = 4
EXIT   = 5

DIRS = [(-1,0),(1,0),(0,-1),(0,1)]

def generate_maze(n):
    grid = [[WALL]*n for _ in range(n)]

    def carve(r, c):
        grid[r][c] = OPEN
        directions = [(0,2),(2,0),(0,-2),(-2,0)]
        random.shuffle(directions)
        for dr, dc in directions:
            nr, nc = r+dr, c+dc
            if 0 < nr < n-1 and 0 < nc < n-1 and grid[nr][nc] == WALL:
                grid[r+dr//2][c+dc//2] = OPEN
                carve(nr, nc)

    carve(1, 1)
    grid[1][1] = START
    grid[n-2][n-2] = EXIT
    return grid


# =============================================
#   GUI UTAMA
# =============================================

# Warna pastel
COLORS = {
    WALL:  "#c9b8e8",   # lavender gelap
    OPEN:  "#f5f0ff",   # lavender muda
    PATH:  "#a8d8ea",   # biru pastel
    TRIED: "#ffd6e0",   # pink pastel
    START: "#b5ead7",   # mint
    EXIT:  "#ffb7b2",   # coral pastel
}

BG         = "#fef6fb"
PANEL_BG   = "#ffffff"
ACCENT1    = "#c9b8e8"  # lavender
ACCENT2    = "#a8d8ea"  # biru
ACCENT3    = "#ffb7b2"  # coral
TEXT_MAIN  = "#5a5275"
TEXT_MUTED = "#b0a8c8"
BTN_GEN    = "#c9b8e8"
BTN_SOL    = "#a8d8ea"
BTN_RES    = "#ffb7b2"

class MazeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Labirin + Stack Backtracking")
        self.root.configure(bg=BG)
        self.root.resizable(True, True)

        self.grid = []
        self.rows = 0
        self.cols = 0
        self.cell = 30
        self.solving = False
        self.after_id = None
        self.steps = 0
        self.backs = 0
        self.start_time = 0
        self.stack_snapshot = []

        self._build_ui()
        self._generate()

    def _build_ui(self):
        # ---- HEADER ----
        hdr = tk.Frame(self.root, bg=BG)
        hdr.pack(fill="x", padx=20, pady=(18,0))
        tk.Label(hdr, text="Labirin + Stack Backtracking",
                 font=(FONT_MAIN,18,"bold"), bg=BG, fg=TEXT_MAIN).pack(anchor="w")
        tk.Label(hdr, text="Generate labirin random & selesaikan otomatis dengan Stack LIFO — Bab 7 Struktur Data",
                 font=(FONT_MAIN,10), bg=BG, fg=TEXT_MUTED).pack(anchor="w")

        # ---- CONTROLS ----
        ctrl = tk.Frame(self.root, bg=PANEL_BG, bd=0)
        ctrl.pack(fill="x", padx=20, pady=12)
        ctrl.configure(highlightbackground=ACCENT1, highlightthickness=1)

        inner = tk.Frame(ctrl, bg=PANEL_BG)
        inner.pack(padx=14, pady=10)

        def lbl(parent, text):
            tk.Label(parent, text=text, font=(FONT_MAIN,10,"bold"),
                     bg=PANEL_BG, fg=TEXT_MUTED).pack(side="left", padx=(10,3))

        lbl(inner, "Ukuran:")
        self.size_var = tk.StringVar(value="15")
        sz = ttk.Combobox(inner, textvariable=self.size_var, width=10,
                          values=["11","15","21"], state="readonly",
                          font=(FONT_MAIN,10))
        sz.pack(side="left")

        lbl(inner, "Kecepatan:")
        self.speed_var = tk.StringVar(value="Normal")
        sp = ttk.Combobox(inner, textvariable=self.speed_var, width=10,
                          values=["Lambat","Normal","Cepat","Turbo"], state="readonly",
                          font=(FONT_MAIN,10))
        sp.pack(side="left")

        lbl(inner, "Stack:")
        self.impl_var = tk.StringVar(value="Python List")
        im = ttk.Combobox(inner, textvariable=self.impl_var, width=12,
                          values=["Python List","Linked List"], state="readonly",
                          font=(FONT_MAIN,10))
        im.pack(side="left")
        im.bind("<<ComboboxSelected>>", lambda e: self._show_code())

        tk.Button(inner, text="  Generate", font=(FONT_MAIN,10,"bold"),
                  bg=BTN_GEN, fg=TEXT_MAIN, bd=0, padx=12, pady=5,
                  relief="flat", cursor="hand2",
                  command=self._generate).pack(side="left", padx=(14,3))

        self.btn_solve = tk.Button(inner, text="  Selesaikan", font=(FONT_MAIN,10,"bold"),
                  bg=BTN_SOL, fg=TEXT_MAIN, bd=0, padx=12, pady=5,
                  relief="flat", cursor="hand2", state="disabled",
                  command=self._solve)
        self.btn_solve.pack(side="left", padx=3)

        self.btn_reset = tk.Button(inner, text="  Reset", font=(FONT_MAIN,10,"bold"),
                  bg=BTN_RES, fg=TEXT_MAIN, bd=0, padx=12, pady=5,
                  relief="flat", cursor="hand2", state="disabled",
                  command=self._reset)
        self.btn_reset.pack(side="left", padx=3)

        # ---- MAIN AREA ----
        main = tk.Frame(self.root, bg=BG)
        main.pack(fill="both", expand=True, padx=20, pady=(0,16))

        # Canvas labirin
        canvas_frame = tk.Frame(main, bg=PANEL_BG,
                                highlightbackground=ACCENT1, highlightthickness=1)
        canvas_frame.pack(side="left", anchor="nw")

        self.canvas = tk.Canvas(canvas_frame, bg=COLORS[OPEN], bd=0,
                                highlightthickness=0)
        self.canvas.pack()

        # Panel kanan
        panel = tk.Frame(main, bg=BG)
        panel.pack(side="left", fill="y", padx=(14,0), anchor="nw")

        # Status card
        self._status_card(panel)

        # Stack viz card
        self._stack_card(panel)

        # Legend card
        self._legend_card(panel)

        # Kode card
        self._code_card(panel)

    def _card(self, parent, title):
        f = tk.Frame(parent, bg=PANEL_BG,
                     highlightbackground=ACCENT1, highlightthickness=1)
        f.pack(fill="x", pady=(0,10))
        tk.Label(f, text=title, font=(FONT_MAIN,9,"bold"),
                 bg=PANEL_BG, fg=TEXT_MUTED).pack(anchor="w", padx=12, pady=(8,4))
        return f

    def _status_card(self, parent):
        f = self._card(parent, "✨ STATUS")
        self.lbl_status = tk.Label(f, text="Generate labirin dulu...",
                                   font=(FONT_MAIN,11,"bold"), bg=PANEL_BG, fg=TEXT_MAIN,
                                   wraplength=240, justify="left")
        self.lbl_status.pack(anchor="w", padx=12, pady=(0,6))

        grid_f = tk.Frame(f, bg=PANEL_BG)
        grid_f.pack(fill="x", padx=12, pady=(0,10))

        self.metrics = {}
        items = [("Stack size","0"),("Langkah","0"),("Backtrack","0"),("Waktu (ms)","-")]
        for i,(label,val) in enumerate(items):
            box = tk.Frame(grid_f, bg="#f5f0ff", padx=10, pady=6)
            box.grid(row=i//2, column=i%2, padx=3, pady=3, sticky="ew")
            grid_f.columnconfigure(i%2, weight=1)
            tk.Label(box, text=label, font=(FONT_MAIN,9), bg="#f5f0ff", fg=TEXT_MUTED).pack(anchor="w")
            v = tk.Label(box, text=val, font=(FONT_MAIN,16,"bold"), bg="#f5f0ff", fg=TEXT_MAIN)
            v.pack(anchor="w")
            self.metrics[label] = v

    def _stack_card(self, parent):
        f = self._card(parent, "📦 STACK SAAT INI (LIFO)")
        self.stack_frame = tk.Frame(f, bg=PANEL_BG)
        self.stack_frame.pack(fill="x", padx=12, pady=(0,10))
        self._render_stack([])

    def _render_stack(self, items):
        for w in self.stack_frame.winfo_children():
            w.destroy()
        if not items:
            tk.Label(self.stack_frame, text="Stack kosong",
                     font=(FONT_MAIN,10,"italic"), bg=PANEL_BG, fg=TEXT_MUTED).pack(anchor="w")
            return
        display = items[-10:]
        for i, item in enumerate(reversed(display)):
            is_top = (i == 0)
            color = "#a8d8ea" if is_top else "#e8f4fb"
            fg    = "#3a7a99" if is_top else TEXT_MUTED
            row = tk.Frame(self.stack_frame, bg=color, padx=8, pady=3)
            row.pack(fill="x", pady=1)
            txt = f"({item[0]}, {item[1]})"
            tk.Label(row, text=txt, font=(FONT_MAIN,10,"bold" if is_top else "normal"),
                     bg=color, fg=fg).pack(side="left")
            if is_top:
                tk.Label(row, text="← top", font=(FONT_MAIN,9),
                         bg=color, fg="#7ab8d4").pack(side="right")

    def _legend_card(self, parent):
        f = self._card(parent, "🎨 KETERANGAN WARNA")
        items = [
            (COLORS[START],  "Start (S)"),
            (COLORS[EXIT],   "Exit (E)"),
            (COLORS[PATH],   "Jalur aktif (x)"),
            (COLORS[TRIED],  "Jalan buntu (o)"),
            (COLORS[WALL],   "Dinding (*)"),
        ]
        g = tk.Frame(f, bg=PANEL_BG)
        g.pack(padx=12, pady=(0,10), anchor="w")
        for color, label in items:
            row = tk.Frame(g, bg=PANEL_BG)
            row.pack(anchor="w", pady=2)
            tk.Canvas(row, width=16, height=16, bg=color, bd=0,
                      highlightthickness=1,
                      highlightbackground=ACCENT1).pack(side="left")
            tk.Label(row, text=f"  {label}", font=(FONT_MAIN,10),
                     bg=PANEL_BG, fg=TEXT_MAIN).pack(side="left")

    def _code_card(self, parent):
        f = self._card(parent, "💻 KODE IMPLEMENTASI")

        tab_f = tk.Frame(f, bg=PANEL_BG)
        tab_f.pack(anchor="w", padx=12)

        self.tab_list = tk.Button(tab_f, text="Python List",
                                  font=(FONT_MAIN,9,"bold"),
                                  bg=ACCENT1, fg=TEXT_MAIN, bd=0, padx=8, pady=3,
                                  relief="flat", cursor="hand2",
                                  command=lambda: self._show_code("list"))
        self.tab_list.pack(side="left", padx=(0,4))

        self.tab_linked = tk.Button(tab_f, text="Linked List",
                                    font=(FONT_MAIN,9,"bold"),
                                    bg="#ede8fa", fg=TEXT_MUTED, bd=0, padx=8, pady=3,
                                    relief="flat", cursor="hand2",
                                    command=lambda: self._show_code("linked"))
        self.tab_linked.pack(side="left")

        code_wrap = tk.Frame(f, bg="#f5f0ff",
                             highlightbackground=ACCENT1, highlightthickness=1)
        code_wrap.pack(fill="x", padx=12, pady=(6,12))

        self.code_text = tk.Text(code_wrap, font=(FONT_MONO,9),
                                 bg="#f5f0ff", fg=TEXT_MAIN,
                                 bd=0, padx=6, pady=6,
                                 height=10, width=32,
                                 state="disabled", wrap="none",
                                 highlightthickness=0)
        self.code_text.pack(fill="both")

        self._show_code("list")

    CODE = {
        "list": """\
class Stack:
  def __init__(self):
    self._items = list()

  def isEmpty(self):
    return len(self) == 0

  def __len__(self):
    return len(self._items)

  def peek(self):
    assert not self.isEmpty()
    return self._items[-1]

  def push(self, item):
    # tambah ke atas (akhir list)
    self._items.append(item)

  def pop(self):
    # hapus dari atas
    assert not self.isEmpty()
    return self._items.pop()

# Semua operasi: O(1) amortized""",

        "linked": """\
class _StackNode:
  def __init__(self, item, link):
    self.item = item
    self.next = link

class Stack:
  def __init__(self):
    self._top = None
    self._size = 0

  def isEmpty(self):
    return self._top is None

  def __len__(self):
    return self._size

  def peek(self):
    assert not self.isEmpty()
    return self._top.item

  def push(self, item):
    # node baru jadi top
    self._top = _StackNode(item,
                  self._top)
    self._size += 1

  def pop(self):
    assert not self.isEmpty()
    node = self._top
    self._top = self._top.next
    self._size -= 1
    return node.item

# Semua operasi: O(1) worst case!"""
    }

    def _show_code(self, which=None):
        if which is None:
            which = "list" if self.impl_var.get() == "Python List" else "linked"
        self.code_text.config(state="normal")
        self.code_text.delete("1.0","end")
        self.code_text.insert("1.0", self.CODE[which])
        self.code_text.config(state="disabled")
        if which == "list":
            self.tab_list.config(bg=ACCENT1, fg=TEXT_MAIN)
            self.tab_linked.config(bg="#ede8fa", fg=TEXT_MUTED)
        else:
            self.tab_linked.config(bg=ACCENT1, fg=TEXT_MAIN)
            self.tab_list.config(bg="#ede8fa", fg=TEXT_MUTED)

    # ---- MAZE LOGIC ----
    def _generate(self):
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self.solving = False
        n = int(self.size_var.get())
        self.rows = n
        self.cols = n
        self.cell = max(18, min(34, 420 // n))
        self.grid = generate_maze(n)
        self.steps = 0
        self.backs = 0
        self.start_time = 0
        self._update_metrics()
        self._render_stack([])
        self.lbl_status.config(text='Labirin siap! Klik Selesaikan!', fg=TEXT_MAIN)
        self.btn_solve.config(state="normal")
        self.btn_reset.config(state="normal")
        self._draw()

    def _draw(self):
        C = self.cell
        N = self.rows
        w, h = N*C, N*C
        self.canvas.config(width=w, height=h)
        self.canvas.delete("all")
        for r in range(N):
            for c in range(N):
                val = self.grid[r][c]
                color = COLORS[val]
                x0, y0 = c*C, r*C
                self.canvas.create_rectangle(x0, y0, x0+C, y0+C,
                                             fill=color, outline="", width=0)
                if val == START:
                    self.canvas.create_text(x0+C//2, y0+C//2, text="S",
                                            font=(FONT_MAIN, max(8,C-8), "bold"),
                                            fill="#2d7a5f")
                elif val == EXIT:
                    self.canvas.create_text(x0+C//2, y0+C//2, text="E",
                                            font=(FONT_MAIN, max(8,C-8), "bold"),
                                            fill="#c0504d")

    def _update_metrics(self):
        self.metrics["Stack size"].config(text=str(len(self.stack_snapshot)))
        self.metrics["Langkah"].config(text=str(self.steps))
        self.metrics["Backtrack"].config(text=str(self.backs))
        if self.start_time > 0:
            elapsed = int((time.time() - self.start_time) * 1000)
            self.metrics["Waktu (ms)"].config(text=str(elapsed))

    def _speed_ms(self):
        return {"Lambat":200, "Normal":60, "Cepat":20, "Turbo":1}[self.speed_var.get()]

    def _solve(self):
        if self.solving:
            return
        self.solving = True
        self.btn_solve.config(state="disabled")
        self.start_time = time.time()

        impl = self.impl_var.get()
        stack = StackList() if impl == "Python List" else StackLinked()

        sr, sc = 1, 1
        er, ec = self.rows-2, self.cols-2

        stack.push((sr, sc))
        self.grid[sr][sc] = PATH

        def is_valid(r, c):
            return (0 <= r < self.rows and 0 <= c < self.cols and
                    self.grid[r][c] in (OPEN, EXIT))

        def step():
            if not self.solving:
                return
            if stack.isEmpty():
                self.lbl_status.config(text="Tidak ada jalur ditemukan!", fg="#c0504d")
                self.solving = False
                return

            self.steps += 1
            r, c = stack.peek()

            if r == er and c == ec:
                self.grid[er][ec] = EXIT
                elapsed = int((time.time()-self.start_time)*1000)
                self.metrics["Waktu (ms)"].config(text=str(elapsed))
                self.lbl_status.config(
                    text=f"🌸 Jalur ditemukan! {self.steps} langkah, {self.backs}x backtrack",
                    fg="#2d7a5f")
                self.solving = False
                self.stack_snapshot = stack.toList()
                self._update_metrics()
                self._render_stack(self.stack_snapshot)
                self._draw()
                return

            moved = False
            for dr, dc in DIRS:
                nr, nc = r+dr, c+dc
                if is_valid(nr, nc):
                    if self.grid[nr][nc] == EXIT:
                        stack.push((nr, nc))
                        self.stack_snapshot = stack.toList()
                        self._update_metrics()
                        self._render_stack(self.stack_snapshot)
                        self._draw()
                        self.after_id = self.root.after(self._speed_ms(), step)
                        return
                    self.grid[nr][nc] = PATH
                    stack.push((nr, nc))
                    moved = True
                    break

            if not moved:
                self.backs += 1
                pr, pc = stack.pop()
                if self.grid[pr][pc] != START:
                    self.grid[pr][pc] = TRIED

            self.stack_snapshot = stack.toList()
            self._update_metrics()
            self._render_stack(self.stack_snapshot)
            self._draw()
            self.after_id = self.root.after(self._speed_ms(), step)

        self.after_id = self.root.after(self._speed_ms(), step)

    def _reset(self):
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self._generate()


if __name__ == "__main__":
    root = tk.Tk()
    app = MazeApp(root)
    root.mainloop()
