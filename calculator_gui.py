import tkinter as tk
from tkinter import font as tkfont


class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.resizable(False, False)
        self.configure(bg="#202020")

        self._expression = ""
        self._history = ""
        self._just_evaluated = False

        self._build_ui()
        self._bind_keys()

    # ------------------------------------------------------------------ UI ---

    def _build_ui(self):
        # ---- display ----
        display_frame = tk.Frame(self, bg="#202020", padx=8, pady=8)
        display_frame.pack(fill="x")

        self._history_var = tk.StringVar(value="")
        tk.Label(
            display_frame, textvariable=self._history_var,
            bg="#202020", fg="#888888", anchor="e",
            font=("Segoe UI", 11), height=1,
        ).pack(fill="x")

        self._display_var = tk.StringVar(value="0")
        tk.Label(
            display_frame, textvariable=self._display_var,
            bg="#202020", fg="#ffffff", anchor="e",
            font=("Segoe UI", 36, "bold"), height=2,
        ).pack(fill="x")

        # ---- buttons ----
        btn_frame = tk.Frame(self, bg="#202020")
        btn_frame.pack(fill="both", expand=True)

        # (label, row, col, colspan, style, command)
        buttons = [
            # row 0 — memory row (greyed out, non-functional display)
            ("%",    0, 0, 1, "func",  lambda: self._percent()),
            ("CE",   0, 1, 1, "func",  lambda: self._clear_entry()),
            ("C",    0, 2, 1, "func",  lambda: self._clear()),
            ("⌫",   0, 3, 1, "func",  lambda: self._backspace()),
            # row 1
            ("¹/x",  1, 0, 1, "func",  lambda: self._reciprocal()),
            ("x²",   1, 1, 1, "func",  lambda: self._square()),
            ("²√x",  1, 2, 1, "func",  lambda: self._sqrt()),
            ("÷",    1, 3, 1, "op",    lambda: self._operator("/")),
            # row 2
            ("7",    2, 0, 1, "num",   lambda: self._digit("7")),
            ("8",    2, 1, 1, "num",   lambda: self._digit("8")),
            ("9",    2, 2, 1, "num",   lambda: self._digit("9")),
            ("×",    2, 3, 1, "op",    lambda: self._operator("*")),
            # row 3
            ("4",    3, 0, 1, "num",   lambda: self._digit("4")),
            ("5",    3, 1, 1, "num",   lambda: self._digit("5")),
            ("6",    3, 2, 1, "num",   lambda: self._digit("6")),
            ("−",    3, 3, 1, "op",    lambda: self._operator("-")),
            # row 4
            ("1",    4, 0, 1, "num",   lambda: self._digit("1")),
            ("2",    4, 1, 1, "num",   lambda: self._digit("2")),
            ("3",    4, 2, 1, "num",   lambda: self._digit("3")),
            ("+",    4, 3, 1, "op",    lambda: self._operator("+")),
            # row 5
            ("+/−",  5, 0, 1, "num",   lambda: self._negate()),
            ("0",    5, 1, 1, "num",   lambda: self._digit("0")),
            (".",    5, 2, 1, "num",   lambda: self._dot()),
            ("=",    5, 3, 1, "eq",    lambda: self._evaluate()),
        ]

        styles = {
            "num":  {"bg": "#333333", "fg": "#ffffff", "active": "#4d4d4d"},
            "func": {"bg": "#3b3b3b", "fg": "#ffffff", "active": "#555555"},
            "op":   {"bg": "#3b3b3b", "fg": "#ffffff", "active": "#555555"},
            "eq":   {"bg": "#0078d4", "fg": "#ffffff", "active": "#1a8fe8"},
        }

        for label, row, col, span, style, cmd in buttons:
            s = styles[style]
            btn = tk.Button(
                btn_frame, text=label,
                bg=s["bg"], fg=s["fg"],
                activebackground=s["active"], activeforeground=s["fg"],
                font=("Segoe UI", 14),
                relief="flat", bd=0, cursor="hand2",
                command=cmd,
            )
            btn.grid(
                row=row, column=col, columnspan=span,
                sticky="nsew", padx=1, pady=1, ipady=14,
            )

        for r in range(6):
            btn_frame.rowconfigure(r, weight=1)
        for c in range(4):
            btn_frame.columnconfigure(c, weight=1)

    def _bind_keys(self):
        for d in "0123456789":
            self.bind(d, lambda e, n=d: self._digit(n))
        self.bind(".", lambda e: self._dot())
        self.bind("+", lambda e: self._operator("+"))
        self.bind("-", lambda e: self._operator("-"))
        self.bind("*", lambda e: self._operator("*"))
        self.bind("/", lambda e: self._operator("/"))
        self.bind("<Return>", lambda e: self._evaluate())
        self.bind("=", lambda e: self._evaluate())
        self.bind("<BackSpace>", lambda e: self._backspace())
        self.bind("<Escape>", lambda e: self._clear())

    # -------------------------------------------------------------- Logic ---

    def _set_display(self, value):
        # Show up to 16 significant digits; strip unnecessary trailing zeros
        try:
            f = float(value)
            if f == int(f) and "e" not in str(f).lower():
                text = str(int(f))
            else:
                text = f"{f:.10g}"
        except (ValueError, OverflowError):
            text = str(value)
        self._display_var.set(text)

    def _digit(self, n):
        if self._just_evaluated:
            self._expression = ""
            self._just_evaluated = False
        if self._expression == "0":
            self._expression = n
        else:
            self._expression += n
        self._set_display(self._expression)

    def _dot(self):
        if self._just_evaluated:
            self._expression = "0"
            self._just_evaluated = False
        # Only add dot if the current number segment doesn't have one
        parts = self._expression.replace("(", "").split("+")
        parts = [p for seg in parts for p in seg.split("-")]
        parts = [p for seg in parts for p in seg.split("*")]
        parts = [p for seg in parts for p in seg.split("/")]
        if "." not in (parts[-1] if parts else ""):
            self._expression = self._expression or "0"
            self._expression += "."
            self._display_var.set(self._expression.split("+")[-1]
                                  .split("-")[-1].split("*")[-1].split("/")[-1])

    def _operator(self, op):
        self._just_evaluated = False
        if self._expression and self._expression[-1] in "+-*/":
            self._expression = self._expression[:-1]
        self._expression += op
        display_op = {"*": "×", "/": "÷", "+": "+", "-": "−"}[op]
        self._history_var.set(self._expression[:-1] + " " + display_op)
        self._display_var.set("0")

    def _evaluate(self):
        if not self._expression:
            return
        try:
            self._history_var.set(self._expression + " =")
            result = eval(self._expression, {"__builtins__": {}}, {})  # noqa: S307
            self._expression = str(result)
            self._set_display(result)
            self._just_evaluated = True
        except ZeroDivisionError:
            self._display_var.set("Cannot divide by zero")
            self._expression = ""
            self._history_var.set("")
            self._just_evaluated = True
        except Exception:
            self._display_var.set("Invalid input")
            self._expression = ""
            self._history_var.set("")
            self._just_evaluated = True

    def _clear(self):
        self._expression = ""
        self._history_var.set("")
        self._display_var.set("0")
        self._just_evaluated = False

    def _clear_entry(self):
        # Remove the last number segment
        if self._just_evaluated:
            self._clear()
            return
        for op in reversed(self._expression):
            if op in "+-*/":
                idx = self._expression.rfind(op)
                self._expression = self._expression[: idx + 1]
                self._display_var.set("0")
                return
        self._expression = ""
        self._display_var.set("0")

    def _backspace(self):
        if self._just_evaluated:
            self._clear()
            return
        self._expression = self._expression[:-1]
        if not self._expression or self._expression[-1] in "+-*/":
            self._display_var.set("0")
        else:
            self._set_display(self._expression.split("+")[-1]
                              .split("-")[-1].split("*")[-1].split("/")[-1])

    def _percent(self):
        try:
            # Interpret % as /100 of the current number
            for op in reversed(range(len(self._expression))):
                if self._expression[op] in "+-*/":
                    base = float(self._expression[: op])
                    pct = float(self._expression[op + 1:])
                    result = base * pct / 100
                    self._expression = self._expression[: op + 1] + str(result)
                    self._set_display(result)
                    return
            # No operator — just divide by 100
            result = float(self._expression or "0") / 100
            self._expression = str(result)
            self._set_display(result)
        except Exception:
            pass

    def _negate(self):
        try:
            val = float(self._expression or "0") * -1
            self._expression = str(val)
            self._set_display(val)
        except Exception:
            pass

    def _reciprocal(self):
        try:
            val = float(self._expression or "0")
            if val == 0:
                raise ZeroDivisionError
            result = 1 / val
            self._expression = str(result)
            self._history_var.set(f"1/({val})")
            self._set_display(result)
            self._just_evaluated = True
        except ZeroDivisionError:
            self._display_var.set("Cannot divide by zero")
            self._expression = ""
            self._just_evaluated = True

    def _square(self):
        try:
            val = float(self._expression or "0")
            result = val ** 2
            self._history_var.set(f"sqr({val})")
            self._expression = str(result)
            self._set_display(result)
            self._just_evaluated = True
        except Exception:
            pass

    def _sqrt(self):
        try:
            val = float(self._expression or "0")
            if val < 0:
                self._display_var.set("Invalid input")
                self._expression = ""
                self._just_evaluated = True
                return
            import math
            result = math.sqrt(val)
            self._history_var.set(f"√({val})")
            self._expression = str(result)
            self._set_display(result)
            self._just_evaluated = True
        except Exception:
            pass


if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
