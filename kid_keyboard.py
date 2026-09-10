"""Kid's Keyboard Learning App - Free Explore Mode."""

import random
import sys
import tkinter as tk
from common import (
    PALETTE,
    TEXT_COLORS,
    NUMBER_WORDS,
    NUMPAD_KEYS,
    SPECIAL_KEYS,
    get_tts_engine,
    center_window,
)

CARD_BG = "#FFFFFF"


class KidKeyboardApp:
    def __init__(self, root, on_close=None):
        self.root = root
        self.on_close = on_close
        self.root.title("Kids Keyboard - Explore & Learn!")
        self.root.minsize(600, 500)
        center_window(self.root, 900, 700)
        self.root.configure(bg="#FFEAA7")

        self.tts = get_tts_engine()
        self._build_ui()
        self._bind_events()

    def _build_ui(self):
        # Top banner with friendly instructions
        self.header_label = tk.Label(
            self.root,
            text="Press any key on the keyboard!",
            font=("Segoe UI", 22, "bold"),
            bg="#FFEAA7",
            fg="#2D3436",
        )
        self.header_label.pack(side=tk.TOP, pady=(25, 10))

        # Big central card frame
        self.card = tk.Frame(
            self.root,
            bg=CARD_BG,
            highlightbackground="#DFE6E9",
            highlightthickness=4,
            padx=40,
            pady=40,
        )
        self.card.pack(expand=True, fill=tk.BOTH, padx=40, pady=20)

        # Main big display for the pressed key
        self.key_label = tk.Label(
            self.card,
            text="★",
            font=("Arial Rounded MT Bold", 160, "bold"),
            bg=CARD_BG,
            fg="#6C5CE7",
        )
        self.key_label.pack(expand=True)

        # Sub-label for spelling/pronunciation description
        self.desc_label = tk.Label(
            self.card,
            text="Ready!",
            font=("Segoe UI", 32, "bold"),
            bg=CARD_BG,
            fg="#636E72",
        )
        self.desc_label.pack(side=tk.BOTTOM, pady=(0, 20))

        # Bottom tip
        self.footer_label = tk.Label(
            self.root,
            text="💡 Tip: Press Esc to return | F11 for Fullscreen",
            font=("Segoe UI", 12),
            bg="#FFEAA7",
            fg="#636E72",
        )
        self.footer_label.pack(side=tk.BOTTOM, pady=(5, 15))

    def _bind_events(self):
        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<F11>", self.toggle_fullscreen)

    def toggle_fullscreen(self, event=None):
        is_fs = self.root.attributes("-fullscreen")
        self.root.attributes("-fullscreen", not is_fs)

    def on_key_press(self, event):
        keysym = event.keysym
        char = event.char

        # Exit or return to launcher
        if keysym == "Escape":
            if self.on_close:
                self.on_close()
            else:
                self.root.destroy()
            return

        display_text = ""
        speech_text = ""
        desc_text = ""

        # 1. Check NumPad keys
        if keysym in NUMPAD_KEYS:
            val = NUMPAD_KEYS[keysym]
            if val in NUMBER_WORDS:
                display_text = val
                speech_text = NUMBER_WORDS[val]
                desc_text = f"Number {speech_text}"
            else:
                display_text = val
                speech_text = val
                desc_text = val

        # 2. Check Standard Numbers 0-9
        elif char and char in NUMBER_WORDS:
            display_text = char
            speech_text = NUMBER_WORDS[char]
            desc_text = f"Number {speech_text}"

        # 3. Check English Letters (a-z, A-Z)
        elif char and char.isalpha() and len(char) == 1:
            upper_char = char.upper()
            lower_char = char.lower()
            display_text = f"{upper_char} {lower_char}"
            speech_text = upper_char
            desc_text = f"Letter {upper_char}"

        # 4. Check Special Keys
        elif keysym in SPECIAL_KEYS:
            disp, spk = SPECIAL_KEYS[keysym]
            display_text = disp
            speech_text = spk
            desc_text = spk

        # 5. Check other single printable characters
        elif char and char.isprintable():
            display_text = char
            speech_text = char
            desc_text = f"Symbol '{char}'"

        # Ignore modifier keys (Shift, Ctrl, Alt, Caps_Lock, etc.)
        elif keysym in (
            "Shift_L", "Shift_R", "Control_L", "Control_R", "Alt_L", "Alt_R",
            "Caps_Lock", "Num_Lock", "Scroll_Lock", "Win_L", "Win_R", "F11"
        ):
            return
        else:
            display_text = keysym
            speech_text = keysym
            desc_text = keysym

        self.update_display(display_text, desc_text, speech_text)

    def update_display(self, display_text, desc_text, speech_text):
        new_bg = random.choice(PALETTE)
        self.root.configure(bg=new_bg)
        self.header_label.configure(bg=new_bg)
        self.footer_label.configure(bg=new_bg)

        if len(display_text) <= 3:
            font_size = 140
        elif len(display_text) <= 6:
            font_size = 90
        else:
            font_size = 60

        chosen_color = random.choice(TEXT_COLORS)

        self.key_label.configure(
            text=display_text,
            font=("Arial Rounded MT Bold", font_size, "bold"),
            fg=chosen_color,
        )
        self.desc_label.configure(text=desc_text)

        if speech_text:
            self.tts.speak(speech_text)


def run_keyboard_app(root=None, on_close=None):
    should_run_loop = False
    if root is None:
        root = tk.Tk()
        should_run_loop = True

    app = KidKeyboardApp(root, on_close=on_close)

    if should_run_loop:
        root.mainloop()
    return app


if __name__ == "__main__":
    run_keyboard_app()
