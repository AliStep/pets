import os
import tkinter as tk
from tkinter import messagebox

CELL = 70
MARGIN = 10
PAD = 6
SIZE = 6

CHICK_IMAGE = os.path.join(os.path.dirname(__file__), "images", "chick.png")
GRAIN_IMAGE = os.path.join(os.path.dirname(__file__), "images", "grain.png")

try:
    from PIL import Image, ImageTk
except ImportError:
    Image = None
    ImageTk = None


class GameGUI:
    def __init__(self, game, on_move):
        self.game = game
        self.on_move = on_move
        self.root = tk.Tk()
        self.root.title("Покорми птенчика")
        self.root.resizable(False, False)

        canvas_size = SIZE * CELL
        self.canvas = tk.Canvas(
            self.root, width=canvas_size, height=canvas_size, bg="white"
        )
        self.canvas.pack(padx=MARGIN, pady=(MARGIN, 0))
        self.canvas.bind("<Button-1>", self._on_click)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=MARGIN)

        tk.Button(btn_frame, text="Новая игра", command=self._reset).pack(
            side=tk.LEFT, padx=5
        )
        tk.Button(btn_frame, text="Выход", command=self.root.destroy).pack(
            side=tk.LEFT, padx=5
        )

        self.chick_id = None
        self.grain_id = None
        self._load_images()
        self._draw_all()

    def _load_images(self):
        self.chick_img = None
        self.grain_img = None
        if Image is None or ImageTk is None:
            return
        for path, attr in ((CHICK_IMAGE, "chick_img"), (GRAIN_IMAGE, "grain_img")):
            if os.path.exists(path):
                img = self._fit(image=Image.open(path))
                setattr(self, attr, ImageTk.PhotoImage(img))

    def _fit(self, image):
        max_dim = CELL - PAD * 2
        ratio = min(max_dim / image.width, max_dim / image.height)
        if ratio < 1:
            new_w = max(1, int(image.width * ratio))
            new_h = max(1, int(image.height * ratio))
            image = image.resize((new_w, new_h), Image.LANCZOS)
        return image

    def _cell_coords(self, row, col):
        x1 = col * CELL
        y1 = row * CELL
        x2 = x1 + CELL
        y2 = y1 + CELL
        return x1, y1, x2, y2

    def _draw_grid(self):
        for r in range(SIZE):
            for c in range(SIZE):
                x1, y1, x2, y2 = self._cell_coords(r, c)
                self.canvas.create_rectangle(
                    x1, y1, x2, y2, outline="#bbb", fill="#e8f5e9"
                )

    def _draw_chick(self):
        r, c = self.game.chick.row, self.game.chick.col
        x1, y1, x2, y2 = self._cell_coords(r, c)
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        dye = CELL * 0.28
        if self.chick_id:
            self.canvas.delete(self.chick_id)
        if self.chick_img:
            self.chick_id = self.canvas.create_image(cx, cy, image=self.chick_img)
            return
        self.chick_id = self.canvas.create_oval(
            cx - dye, cy - dye, cx + dye, cy + dye,
            fill="#ffd54f", outline="#f9a825", width=2
        )
        bx = cx + dye * 0.7
        by = cy + dye * 0.4
        self.canvas.create_oval(
            bx - dye * 0.35, by - dye * 0.3, bx + dye * 0.35, by + dye * 0.3,
            fill="#ffe082", outline="#f9a825"
        )
        self.canvas.create_text(
            cx, cy - dye * 0.25, text="•", font=("Arial", 12), fill="#3e2723"
        )
        self.canvas.create_polygon(
            cx - dye * 0.4, cy - dye * 0.5, cx - dye * 0.1, cy - dye * 1.05,
            cx + dye * 0.1, cy - dye * 0.5, fill="#f57f17", outline="#e65100"
        )

    def _draw_grain(self):
        r, c = self.game.grain.row, self.game.grain.col
        x1, y1, x2, y2 = self._cell_coords(r, c)
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        s = CELL * 0.16
        if self.grain_id:
            self.canvas.delete(self.grain_id)
        if self.grain_img:
            self.grain_id = self.canvas.create_image(cx, cy, image=self.grain_img)
            return
        self.grain_id = self.canvas.create_oval(
            cx - s, cy - s * 0.5, cx + s, cy + s * 0.5,
            fill="#a1887f", outline="#5d4037", width=1
        )
        self.canvas.create_arc(
            cx - s * 0.2, cy - s * 0.55, cx + s * 0.2, cy + s * 0.55,
            start=0, extent=200, style="arc", outline="#4e342e"
        )

    def _draw_all(self):
        self.canvas.delete("all")
        self.chick_id = None
        self.grain_id = None
        self._draw_grid()
        self._draw_grain()
        self._draw_chick()

    def _on_click(self, event):
        col = event.x // CELL
        row = event.y // CELL
        if not (0 <= row < SIZE and 0 <= col < SIZE):
            return
        success, msg = self.on_move(row, col)
        if not success:
            if not msg:
                msg = "Ходить можно только на ближайшие клетки (вниз-вверх-влево-вправо)."
            self._draw_all()
            self._show_message("Ошибка", msg, error=True)
        elif success and msg:
            self._draw_all()
            self._show_message("Победа!", msg, error=False)
            self._start_new_game()
        else:
            self._draw_all()

    def _start_new_game(self):
        self.game.reset()
        self._draw_all()

    def _reset(self):
        self.game.reset()
        self._draw_all()

    def _show_rules(self):
        rules = (
            "Правила игры «Покорми птенчика»\n\n"
            "1. Птенчик ходит только на "
            "соседние клетки (вправо-влево-вверх-вниз).\n"
            "2. Нельзя ходить по диагонали или "
            "перепрыгивать через клетки.\n"
            "3. За пределы поля выходить нельзя.\n"
            "4. Цель — добраться до зерна и покормить "
            "птенчика.\n"
        )
        self._show_message("Правила игры", rules, error=False)

    def _show_message(self, title, text, error):
        win = tk.Toplevel(self.root)
        win.title(title)
        win.resizable(False, False)
        win.transient(self.root)
        lbl = tk.Label(
            win, text=text, justify="left",
            font=("Arial", 11), padx=24, pady=24, wraplength=520
        )
        if error:
            lbl.config(fg="#b71c1c")
        lbl.pack()

        btn = tk.Button(
            win, text="ОК",
            width=12,
            command=lambda: (win.destroy(), win.grab_release())
        )
        btn.pack(pady=(0, 16))

        btn.focus_set()
        win.bind("<Return>", lambda _: btn.invoke())
        win.bind("<Escape>", lambda _: btn.invoke())
        try:
            win.update_idletasks()
            win.wait_visibility()
            win.grab_set()
        except tk.TclError:
            pass
        self.root.wait_window(win)

    def run(self):
        self._show_rules()
        self.root.mainloop()