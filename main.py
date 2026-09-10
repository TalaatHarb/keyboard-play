"""Kids Learning Suite - Main Entry Point and Game Selector."""

import sys
import tkinter as tk
from common import PALETTE, center_window, get_tts_engine
from kid_keyboard import KidKeyboardApp
from falling_letters import FallingLettersGame
from animal_spelling import AnimalSpellingGame


class KidsAppLauncher:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Kids Fun Keyboard & Letter Games")
        self.root.minsize(850, 580)
        center_window(self.root, 1020, 680)
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
        title_frame.pack(side=tk.TOP, pady=(35, 15))

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
        cards_frame.pack(expand=True, fill=tk.BOTH, padx=35, pady=15)
        cards_frame.columnconfigure(0, weight=1)
        cards_frame.columnconfigure(1, weight=1)
        cards_frame.columnconfigure(2, weight=1)
        cards_frame.rowconfigure(0, weight=1)

        # Card 1: Explore Keyboard
        card1 = tk.Frame(
            cards_frame,
            bg="#FFFFFF",
            highlightbackground="#74B9FF",
            highlightthickness=4,
            cursor="hand2",
            padx=15,
            pady=15,
        )
        card1.grid(row=0, column=0, padx=12, pady=10, sticky="nsew")

        tk.Label(
            card1,
            text="🔤",
            font=("Segoe UI", 50),
            bg="#FFFFFF",
        ).pack(pady=(5, 0))

        tk.Label(
            card1,
            text="Explore Keys",
            font=("Segoe UI", 18, "bold"),
            bg="#FFFFFF",
            fg="#0984E3",
        ).pack()

        tk.Label(
            card1,
            text="Press any key to see\nbig colorful letters\n& hear their sounds!",
            font=("Segoe UI", 11),
            bg="#FFFFFF",
            fg="#636E72",
            justify=tk.CENTER,
        ).pack(pady=8)

        btn1 = tk.Button(
            card1,
            text="Play Explore",
            font=("Segoe UI", 13, "bold"),
            bg="#74B9FF",
            fg="#FFFFFF",
            activebackground="#0984E3",
            activeforeground="#FFFFFF",
            relief=tk.FLAT,
            padx=16,
            pady=6,
            cursor="hand2",
            command=self.launch_keyboard_explorer,
        )
        btn1.pack(side=tk.BOTTOM, pady=8)
        card1.bind("<Button-1>", lambda e: self.launch_keyboard_explorer())

        # Card 2: Falling Letters Game
        card2 = tk.Frame(
            cards_frame,
            bg="#FFFFFF",
            highlightbackground="#FD79A8",
            highlightthickness=4,
            cursor="hand2",
            padx=15,
            pady=15,
        )
        card2.grid(row=0, column=1, padx=12, pady=10, sticky="nsew")

        tk.Label(
            card2,
            text="⭐",
            font=("Segoe UI", 50),
            bg="#FFFFFF",
        ).pack(pady=(5, 0))

        tk.Label(
            card2,
            text="Falling Letters",
            font=("Segoe UI", 18, "bold"),
            bg="#FFFFFF",
            fg="#E84393",
        ).pack()

        tk.Label(
            card2,
            text="Pop falling letters before\nthey drop! Score points\nand keep 7 lives.",
            font=("Segoe UI", 11),
            bg="#FFFFFF",
            fg="#636E72",
            justify=tk.CENTER,
        ).pack(pady=8)

        btn2 = tk.Button(
            card2,
            text="Play Falling Game",
            font=("Segoe UI", 13, "bold"),
            bg="#FD79A8",
            fg="#FFFFFF",
            activebackground="#E84393",
            activeforeground="#FFFFFF",
            relief=tk.FLAT,
            padx=16,
            pady=6,
            cursor="hand2",
            command=self.launch_falling_game,
        )
        btn2.pack(side=tk.BOTTOM, pady=8)
        card2.bind("<Button-1>", lambda e: self.launch_falling_game())

        # Card 3: Animal & Phonics Spelling Game
        card3 = tk.Frame(
            cards_frame,
            bg="#FFFFFF",
            highlightbackground="#A29BFE",
            highlightthickness=4,
            cursor="hand2",
            padx=15,
            pady=15,
        )
        card3.grid(row=0, column=2, padx=12, pady=10, sticky="nsew")

        tk.Label(
            card3,
            text="🦁",
            font=("Segoe UI", 50),
            bg="#FFFFFF",
        ).pack(pady=(5, 0))

        tk.Label(
            card3,
            text="Animal Spelling",
            font=("Segoe UI", 18, "bold"),
            bg="#FFFFFF",
            fg="#6C5CE7",
        ).pack()

        tk.Label(
            card3,
            text="Spell cute animals letter\nby letter and hear their\nfun animal sounds!",
            font=("Segoe UI", 11),
            bg="#FFFFFF",
            fg="#636E72",
            justify=tk.CENTER,
        ).pack(pady=8)

        btn3 = tk.Button(
            card3,
            text="Play Spelling",
            font=("Segoe UI", 13, "bold"),
            bg="#A29BFE",
            fg="#FFFFFF",
            activebackground="#6C5CE7",
            activeforeground="#FFFFFF",
            relief=tk.FLAT,
            padx=16,
            pady=6,
            cursor="hand2",
            command=self.launch_animal_spelling,
        )
        btn3.pack(side=tk.BOTTOM, pady=8)
        card3.bind("<Button-1>", lambda e: self.launch_animal_spelling())

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

    def launch_animal_spelling(self):
        self._clear_window()
        self.active_subapp = AnimalSpellingGame(self.root, on_close=self._build_menu)


def main():
    root = tk.Tk()
    app = KidsAppLauncher(root)
    root.mainloop()


if __name__ == "__main__":
    main()


def main():
    root = tk.Tk()
    app = KidsAppLauncher(root)
    root.mainloop()


if __name__ == "__main__":
    main()
