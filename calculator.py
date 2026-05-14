import tkinter as tk
import re

class Calculator:
    def __init__(self, root):
        self.root = root
        root.title("계산기")
        root.geometry("340x520")
        root.resizable(False, False)
        root.configure(bg="#1a1a2e")
        root.option_add("*Font", "SegoeUI 14")

        self.expression = ""

        disp_frame = tk.Frame(root, bg="#16213e", bd=0, highlightthickness=0)
        disp_frame.pack(pady=(20, 10), padx=20, fill="x")

        self.input_label = tk.Label(disp_frame, text="", anchor="e", bg="#0f3460",
                                     fg="#a8b2d1", font=("SegoeUI", 14), height=1)
        self.input_label.pack(fill="x", padx=10, pady=(10, 0))

        self.result_label = tk.Label(disp_frame, text="0", anchor="e", bg="#0f3460",
                                      fg="#e2e8f0", font=("SegoeUI", 32, "bold"), height=1)
        self.result_label.pack(fill="x", padx=10, pady=(0, 10))

        btn_frame = tk.Frame(root, bg="#16213e")
        btn_frame.pack(pady=(0, 20), padx=20, fill="both", expand=True)

        btn_frame.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="col")
        btn_frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=1, uniform="row")

        buttons = [
            ("C", 0, 0, "#2d2d5e", self.clear_all),
            ("⌫", 0, 1, "#2d2d5e", self.backspace),
            ("%", 0, 2, "#e94560", lambda: self.append("%")),
            ("÷", 0, 3, "#e94560", lambda: self.append("/")),
            ("7", 1, 0, "#1a1a40", lambda: self.append("7")),
            ("8", 1, 1, "#1a1a40", lambda: self.append("8")),
            ("9", 1, 2, "#1a1a40", lambda: self.append("9")),
            ("×", 1, 3, "#e94560", lambda: self.append("*")),
            ("4", 2, 0, "#1a1a40", lambda: self.append("4")),
            ("5", 2, 1, "#1a1a40", lambda: self.append("5")),
            ("6", 2, 2, "#1a1a40", lambda: self.append("6")),
            ("−", 2, 3, "#e94560", lambda: self.append("-")),
            ("1", 3, 0, "#1a1a40", lambda: self.append("1")),
            ("2", 3, 1, "#1a1a40", lambda: self.append("2")),
            ("3", 3, 2, "#1a1a40", lambda: self.append("3")),
            ("+", 3, 3, "#e94560", lambda: self.append("+")),
            ("0", 4, 0, "#1a1a40", self.append_zero, 2),
            (".", 4, 2, "#1a1a40", lambda: self.append(".")),
            ("=", 4, 3, "#533483", self.calculate),
        ]

        for btn in buttons:
            text, r, c, bg, cmd = btn[:5]
            colspan = btn[5] if len(btn) > 5 else 1
            b = tk.Button(btn_frame, text=text, bg=bg, fg="#e2e8f0",
                          font=("SegoeUI", 18, "bold"), bd=0,
                          activebackground=self._lighten(bg),
                          activeforeground="#fff", cursor="hand2",
                          command=cmd)
            b.grid(row=r, column=c, columnspan=colspan, sticky="nsew", padx=4, pady=4)
            b.bind("<Enter>", lambda e, bt=b: bt.configure(bg=self._lighten(bt.cget("bg"))))
            b.bind("<Leave>", lambda e, bt=b: bt.configure(bg=bt.bg_orig))

        for btn in buttons:
            text, r, c, bg, cmd = btn[:5]
            colspan = btn[5] if len(btn) > 5 else 1
            widgets = btn_frame.grid_slaves(row=r, column=c)
            for w in widgets:
                if isinstance(w, tk.Button):
                    w.bg_orig = bg

        root.bind("<Key>", self.key_press)

    def _lighten(self, color):
        try:
            r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
            r = min(255, r + 30)
            g = min(255, g + 30)
            b = min(255, b + 30)
            return f"#{r:02x}{g:02x}{b:02x}"
        except Exception:
            return color

    def _update_display(self):
        self.input_label.configure(text=self.expression)
        if not self.expression:
            self.result_label.configure(text="0")
            return
        try:
            sanitized = self.expression
            result = eval(sanitized, {"__builtins__": {}}, {})
            display = int(result) if result == int(result) else result
            self.result_label.configure(text=str(display))
        except Exception:
            self.result_label.configure(text="...")

    def append(self, val):
        self.expression += val
        self._update_display()

    def append_zero(self):
        self.expression += "0"
        self._update_display()

    def calculate(self):
        try:
            sanitized = self.expression
            result = eval(sanitized, {"__builtins__": {}}, {})
            display = int(result) if result == int(result) else result
            self.result_label.configure(text=str(display))
            self.expression = str(display)
            self.input_label.configure(text=self.expression)
        except Exception:
            self.result_label.configure(text="오류")

    def clear_all(self):
        self.expression = ""
        self.input_label.configure(text="")
        self.result_label.configure(text="0")

    def backspace(self):
        self.expression = self.expression[:-1]
        self._update_display()

    def key_press(self, event):
        if event.char in "0123456789.+-*/%":
            self.append(event.char)
        elif event.keysym == "Return":
            self.calculate()
        elif event.keysym == "BackSpace":
            self.backspace()
        elif event.keysym == "Escape":
            self.clear_all()

if __name__ == "__main__":
    root = tk.Tk()
    Calculator(root)
    root.mainloop()
