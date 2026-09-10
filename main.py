"""Kids Learning Suite - Main Entry Point and Game Selector."""

import sys
import tkinter as tk
from common import PALETTE, center_window, get_tts_engine
from kid_keyboard import KidKeyboardApp
from falling_letters import FallingLettersGame


class KidsAppLauncher:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Kids Fun Keyboard & Letter Games")
        self.root.minsize(750, 580)
        center_window(self.root, 900, 680)
        self.root.configure(bg="#FFEAA7")

        self.tts = get_tts_engine()
        self.active_subapp = None
        self._build_menu()

    def _clear_window(self):
        # Cancel any bindings or widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.unbind("<KeyPress>")
        self.root.unbind("<F11>")

    def _build_menu(self):
        self._clear_window()
        self.root.configure(bg="#FFEAA7")

        # Header Title
        title_frame = tk.Frame(self.root, bg="#FFEAA7")
        title_frame.pack(side=tk.TOP, pady=(40, 20))

        title_label = tk.Label(
            title_frame,
            text="🎈 Kids Fun Typing & Sounds 🎈",
            font=("Segoe UI", 32, "bold"),
            bg="#FFEAA7",
            fg="#2D3436",
        )
        title_label.pack()

        subtitle_label = tk.Label(
            title_frame,
            text="Choose an activity to start playing and learning!",
            font=("Segoe UI", 16),
            bg="#FFEAA7",
            fg="#636E72",
        )
        subtitle_label.pack(pady=(5, 0))

        # Cards container for game buttons
        cards_frame = tk.Frame(self.root, bg="#FFEAA7")
        cards_frame.pack(expand=True, fill=tk.BOTH, padx=50, pady=20)
        cards_frame.columnconfigure(0, weight=1)
        cards_frame.columnconfigure(1, weight=1)
        cards_frame.rowconfigure(0, weight=1)

        # Card 1: Explore Keyboard
        card1 = tk.Frame(
            cards_frame,
            bg="#FFFFFF",
            highlightbackground="#74B9FF",
            highlightthickness=4,
            cursor="hand2",
            padx=20,
            pady=20,
        )
        card1.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        tk.Label(
            card1,
            text="🔤",
            font=("Segoe UI", 55),
            bg="#FFFFFF",
        ).pack(pady=(10, 5))

        tk.Label(
            card1,
            text="Explore Keyboard",
            font=("Segoe UI", 20, "bold"),
            bg="#FFFFFF",
            fg="#0984E3",
        ).pack()

        tk.Label(
            card1,
            text="Press any key to see big colorful\nletters & hear their sounds!",
            font=("Segoe UI", 12),
            bg="#FFFFFF",
            fg="#636E72",
            justify=tk.CENTER,
        ).pack(pady=10)

        btn1 = tk.Button(
            card1,
            text="Play Explore",
            font=("Segoe UI", 14, "bold"),
            bg="#74B9FF",
            fg="#FFFFFF",
            activebackground="#0984E3",
            activeforeground="#FFFFFF",
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.launch_keyboard_explorer,
        )
        btn1.pack(side=tk.BOTTOM, pady=10)
        card1.bind("<Button-1>", lambda e: self.launch_keyboard_explorer())

        # Card 2: Falling Letters Game
        card2 = tk.Frame(
            cards_frame,
            bg="#FFFFFF",
            highlightbackground="#FD79A8",
            highlightthickness=4,
            cursor="hand2",
            padx=20,
            pady=20,
        )
        card2.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")

        tk.Label(
            card2,
            text="⭐",
            font=("Segoe UI", 55),
            bg="#FFFFFF",
        ).pack(pady=(10, 5))

        tk.Label(
            card2,
            text="Falling Letters Game",
            font=("Segoe UI", 20, "bold"),
            bg="#FFFFFF",
            fg="#E84393",
        ).pack()

        tk.Label(
            card2,
            text="Pop falling letters before they drop!\nScore points and keep your 7 lives.",
            font=("Segoe UI", 12),
            bg="#FFFFFF",
            fg="#636E72",
            justify=tk.CENTER,
        ).pack(pady=10)

        btn2 = tk.Button(
            card2,
            text="Play Falling Game",
            font=("Segoe UI", 14, "bold"),
            bg="#FD79A8",
            fg="#FFFFFF",
            activebackground="#E84393",
            activeforeground="#FFFFFF",
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.launch_falling_game,
        )
        btn2.pack(side=tk.BOTTOM, pady=10)
        card2.bind("<Button-1>", lambda e: self.launch_falling_game())

        # Footer
        footer = tk.Label(
            self.root,
            text="Made for kids with speech & visual keyboard feedback | Press Esc on menu to exit",
            font=("Segoe UI", 11),
            bg="#FFEAA7",
            fg="#636E72",
        )
        footer.pack(side=tk.BOTTOM, pady=15)

        self.root.bind("<Escape>", lambda e: self.root.destroy())

    def launch_keyboard_explorer(self):
        self._clear_window()
        self.active_subapp = KidKeyboardApp(self.root, on_close=self._build_menu)

    def launch_falling_game(self):
        self._clear_window()
        self.active_subapp = FallingLettersGame(self.root, on_close=self._build_menu)


def main():
    root = tk.Tk()
    app = KidsAppLauncher(root)
    root.mainloop()


if __name__ == "__main__":
    main()
