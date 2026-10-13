"""
Opens 5 big gray "sticky note" windows, types a text into each one
in big red letters, then moves the windows around the screen.

Requires only Python 3 (tkinter ships with the standard installers).
Run:  python sticky_notes.py
Close all notes with Esc (or close any window).
"""
import math
import tkinter as tk

# ---- Put your 5 texts here ----------------------------------------------
TEXTS = [
    "TEXT 1",
    "TEXT 2",
    "TEXT 3",
    "TEXT 4",
    "TEXT 5",
]

# ---- Appearance / timing -------------------------------------------------
NOTE_WIDTH = 420
NOTE_HEIGHT = 320
BG_COLOR = "#b0b0b0"        # gray
TEXT_COLOR = "red"
FONT = ("Arial", 36, "bold")
TYPE_DELAY_MS = 80          # delay between typed characters
MOVE_DELAY_MS = 20          # delay between animation frames (~50 fps)
SPEED = 6                   # pixels per frame


class StickyNote:
    def __init__(self, root, text, x, y, dx, dy):
        self.win = tk.Toplevel(root)
        self.win.title("Sticky Note")
        self.win.configure(bg=BG_COLOR)
        self.win.attributes("-topmost", True)
        self.win.geometry(f"{NOTE_WIDTH}x{NOTE_HEIGHT}+{x}+{y}")
        self.win.bind("<Escape>", lambda e: root.destroy())
        self.win.protocol("WM_DELETE_WINDOW", root.destroy)

        self.label = tk.Label(
            self.win, text="", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT,
            wraplength=NOTE_WIDTH - 40, justify="center",
        )
        self.label.pack(expand=True, fill="both", padx=20, pady=20)

        self.text = text
        self.x, self.y = x, y
        self.dx, self.dy = dx, dy

    def type_text(self, on_done, i=0):
        """Type the text one character at a time, then call on_done."""
        if i <= len(self.text):
            self.label.config(text=self.text[:i])
            self.win.after(TYPE_DELAY_MS, self.type_text, on_done, i + 1)
        else:
            on_done()

    def step(self, screen_w, screen_h):
        """Move one frame, bouncing off the screen edges."""
        self.x += self.dx
        self.y += self.dy
        if self.x <= 0 or self.x + NOTE_WIDTH >= screen_w:
            self.dx = -self.dx
            self.x = max(0, min(self.x, screen_w - NOTE_WIDTH))
        if self.y <= 0 or self.y + NOTE_HEIGHT >= screen_h:
            self.dy = -self.dy
            self.y = max(0, min(self.y, screen_h - NOTE_HEIGHT))
        self.win.geometry(f"+{int(self.x)}+{int(self.y)}")


def main():
    root = tk.Tk()
    root.withdraw()  # hide the empty main window

    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()

    # Start positions spread across the screen, each moving a different direction
    notes = []
    for i, text in enumerate(TEXTS):
        x = int((screen_w - NOTE_WIDTH) * i / max(1, len(TEXTS) - 1))
        y = int((screen_h - NOTE_HEIGHT) * (0.15 + 0.7 * (i % 2)))
        angle = math.radians(35 + i * 72)
        dx, dy = SPEED * math.cos(angle), SPEED * math.sin(angle)
        notes.append(StickyNote(root, text, x, y, dx, dy))

    def animate():
        for note in notes:
            note.step(screen_w, screen_h)
        root.after(MOVE_DELAY_MS, animate)

    # Type into the notes one after another, then start moving them
    def type_note(i=0):
        if i < len(notes):
            notes[i].type_text(lambda: type_note(i + 1))
        else:
            animate()

    root.after(500, type_note)
    root.mainloop()


if __name__ == "__main__":
    main()
