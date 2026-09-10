"""Animal & Phonics Spelling - Kids Word Spelling Game."""

import random
import tkinter as tk
from common import (
    PALETTE,
    TEXT_COLORS,
    get_tts_engine,
    center_window,
)

# List of kid-friendly animal words with emoji, speech sound, and celebration phrase
ANIMAL_DATA = [
    {"word": "CAT", "emoji": "🐱", "sound": "Meow! Cat!", "hint": "C-A-T"},
    {"word": "DOG", "emoji": "🐶", "sound": "Woof woof! Dog!", "hint": "D-O-G"},
    {"word": "PIG", "emoji": "🐷", "sound": "Oink oink! Pig!", "hint": "P-I-G"},
    {"word": "COW", "emoji": "🐮", "sound": "Mooo! Cow!", "hint": "C-O-W"},
    {"word": "FOX", "emoji": "🦊", "sound": "What does the fox say! Fox!", "hint": "F-O-X"},
    {"word": "BEE", "emoji": "🐝", "sound": "Buzzzz! Bee!", "hint": "B-E-E"},
    {"word": "OWL", "emoji": "🦉", "sound": "Hoo hoo! Owl!", "hint": "O-W-L"},
    {"word": "LION", "emoji": "🦁", "sound": "Roaaar! Lion!", "hint": "L-I-O-N"},
    {"word": "BEAR", "emoji": "🐻", "sound": "Grrr! Bear!", "hint": "B-E-A-R"},
    {"word": "FROG", "emoji": "🐸", "sound": "Ribbit ribbit! Frog!", "hint": "F-R-O-G"},
    {"word": "DUCK", "emoji": "🦆", "sound": "Quack quack! Duck!", "hint": "D-U-C-K"},
    {"word": "FISH", "emoji": "🐟", "sound": "Splash! Fish!", "hint": "F-I-S-H"},
    {"word": "BIRD", "emoji": "🐦", "sound": "Tweet tweet! Bird!", "hint": "B-I-R-D"},
    {"word": "MONKEY", "emoji": "🐵", "sound": "Ooh ooh aah aah! Monkey!", "hint": "M-O-N-K-E-Y"},
    {"word": "RABBIT", "emoji": "🐰", "sound": "Hop hop! Rabbit!", "hint": "R-A-B-B-I-T"},
    {"word": "TIGER", "emoji": "🐯", "sound": "Roaaar! Tiger!", "hint": "T-I-G-E-R"},
]

CARD_BG = "#FFFFFF"


class AnimalSpellingGame:
    def __init__(self, root, on_close=None):
        self.root = root
        self.on_close = on_close
        self.root.title("Animal & Phonics Spelling - Spell the Animal!")
        self.root.minsize(700, 550)
        center_window(self.root, 900, 700)
        self.root.configure(bg="#A29BFE")

        self.tts = get_tts_engine()

        self.score = 0
        self.current_index = 0
        self.typed_letters = []
        self.shuffled_animals = list(ANIMAL_DATA)
        random.shuffle(self.shuffled_animals)

        self.slot_frames = []
        self.slot_labels = []

        self._build_ui()
        self._bind_events()
        self.load_current_animal()

    def _build_ui(self):
        # Top Stats Bar
        self.stats_bar = tk.Frame(self.root, bg="#FFFFFF", height=50, padx=20, pady=10)
        self.stats_bar.pack(side=tk.TOP, fill=tk.X)

        self.score_label = tk.Label(
            self.stats_bar,
            text="⭐ Stars: 0",
            font=("Segoe UI", 18, "bold"),
            bg="#FFFFFF",
            fg="#6C5CE7",
        )
        self.score_label.pack(side=tk.LEFT, padx=10)

        self.streak_label = tk.Label(
            self.stats_bar,
            text="🐾 Animal 1 of " + str(len(self.shuffled_animals)),
            font=("Segoe UI", 14, "bold"),
            bg="#FFFFFF",
            fg="#00B894",
        )
        self.streak_label.pack(side=tk.RIGHT, padx=10)

        # Central Card
        self.card = tk.Frame(
            self.root,
            bg=CARD_BG,
            highlightbackground="#DFE6E9",
            highlightthickness=4,
            padx=30,
            pady=20,
        )
        self.card.pack(expand=True, fill=tk.BOTH, padx=40, pady=15)

        # Big Emoji Display
        self.emoji_label = tk.Label(
            self.card,
            text="🐱",
            font=("Segoe UI Emoji", 90),
            bg=CARD_BG,
        )
        self.emoji_label.pack(pady=(5, 5))

        # Encouraging prompt
        self.prompt_label = tk.Label(
            self.card,
            text="Spell the animal!",
            font=("Segoe UI", 20, "bold"),
            bg=CARD_BG,
            fg="#2D3436",
        )
        self.prompt_label.pack(pady=(0, 15))

        # Letter Slots Container
        self.slots_container = tk.Frame(self.card, bg=CARD_BG)
        self.slots_container.pack(pady=10)

        # Hint / Pronunciation label
        self.hint_label = tk.Label(
            self.card,
            text="",
            font=("Segoe UI", 16, "bold"),
            bg=CARD_BG,
            fg="#636E72",
        )
        self.hint_label.pack(side=tk.BOTTOM, pady=10)

        # Bottom tip
        self.footer = tk.Label(
            self.root,
            text="💡 Type the highlighted letter on your keyboard | Esc to return | F11 for Fullscreen",
            font=("Segoe UI", 11),
            bg="#A29BFE",
            fg="#2D3436",
        )
        self.footer.pack(side=tk.BOTTOM, pady=10)

    def _bind_events(self):
        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<F11>", self.toggle_fullscreen)

    def toggle_fullscreen(self, event=None):
        is_fs = self.root.attributes("-fullscreen")
        self.root.attributes("-fullscreen", not is_fs)

    def load_current_animal(self):
        self.current_animal = self.shuffled_animals[self.current_index]
        word = self.current_animal["word"]
        self.typed_letters = []

        # Update visuals
        new_bg = random.choice(PALETTE)
        self.root.configure(bg=new_bg)
        self.footer.configure(bg=new_bg)

        self.emoji_label.configure(text=self.current_animal["emoji"])
        self.prompt_label.configure(
            text=f"Can you spell {word}?",
            fg=random.choice(TEXT_COLORS),
        )
        self.streak_label.configure(
            text=f"🐾 Animal {self.current_index + 1} of {len(self.shuffled_animals)}"
        )
        self.hint_label.configure(text=f"Press '{word[0]}'", fg="#636E72")

        # Build letter slots
        for f in self.slot_frames:
            f.destroy()
        self.slot_frames.clear()
        self.slot_labels.clear()

        for i, char in enumerate(word):
            frame = tk.Frame(
                self.slots_container,
                bg="#F1F2F6" if i > 0 else "#FFEAA7",
                highlightbackground="#6C5CE7" if i == 0 else "#DFE6E9",
                highlightthickness=3,
                width=75,
                height=85,
            )
            frame.pack_propagate(False)
            frame.pack(side=tk.LEFT, padx=8)

            lbl = tk.Label(
                frame,
                text="_",
                font=("Arial Rounded MT Bold", 36, "bold"),
                bg="#F1F2F6" if i > 0 else "#FFEAA7",
                fg="#2D3436",
            )
            lbl.pack(expand=True)

            self.slot_frames.append(frame)
            self.slot_labels.append(lbl)

        # Speak the word prompt
        self.tts.speak(f"Spell {word}! Press {word[0]}")

    def on_key_press(self, event):
        keysym = event.keysym
        char = event.char

        if keysym == "Escape":
            if self.on_close:
                self.on_close()
            else:
                self.root.destroy()
            return

        if not char or not char.isalpha():
            return

        pressed = char.upper()
        word = self.current_animal["word"]
        expected_index = len(self.typed_letters)

        if expected_index >= len(word):
            return

        expected_char = word[expected_index]

        if pressed == expected_char:
            # Correct letter!
            self.typed_letters.append(pressed)
            idx = len(self.typed_letters) - 1

            # Update filled slot
            self.slot_frames[idx].configure(
                bg="#55EFC4", highlightbackground="#00B894"
            )
            self.slot_labels[idx].configure(
                text=pressed, bg="#55EFC4", fg="#2D3436"
            )

            # Check if whole word complete
            if len(self.typed_letters) == len(word):
                self.on_word_completed()
            else:
                # Highlight next required letter slot
                next_idx = len(self.typed_letters)
                self.slot_frames[next_idx].configure(
                    bg="#FFEAA7", highlightbackground="#6C5CE7"
                )
                self.slot_labels[next_idx].configure(bg="#FFEAA7")
                next_char = word[next_idx]
                self.hint_label.configure(text=f"Great! Now press '{next_char}'", fg="#00B894")
                self.tts.speak(pressed)
        else:
            # Mistake on letter
            self.hint_label.configure(
                text=f"Try again! Press '{expected_char}'", fg="#D63031"
            )
            # Shake / flash current slot
            self.slot_frames[expected_index].configure(
                bg="#FF7675", highlightbackground="#D63031"
            )
            self.slot_labels[expected_index].configure(bg="#FF7675")
            self.root.after(
                200,
                lambda: self._reset_active_slot(expected_index),
            )
            self.tts.speak(f"{pressed}? Try {expected_char}")

    def _reset_active_slot(self, index):
        if index < len(self.slot_frames):
            self.slot_frames[index].configure(
                bg="#FFEAA7", highlightbackground="#6C5CE7"
            )
            self.slot_labels[index].configure(bg="#FFEAA7")

    def on_word_completed(self):
        self.score += 1
        self.score_label.configure(text=f"⭐ Stars: {self.score}")
        word = self.current_animal["word"]
        sound_phrase = self.current_animal["sound"]

        self.prompt_label.configure(
            text=f"🎉 Awesome! {word}! 🎉",
            fg="#00B894",
        )
        self.hint_label.configure(
            text=f"⭐ You spelled {word}! ⭐",
            fg="#6C5CE7",
        )

        # Celebrate with TTS
        self.tts.speak(f"{word}! {sound_phrase}")

        # Transition to next animal after a brief joyful pause
        self.root.after(2200, self.next_animal)

    def next_animal(self):
        self.current_index = (self.current_index + 1) % len(self.shuffled_animals)
        if self.current_index == 0:
            random.shuffle(self.shuffled_animals)
        self.load_current_animal()


def run_animal_spelling(root=None, on_close=None):
    should_run_loop = False
    if root is None:
        root = tk.Tk()
        should_run_loop = True

    app = AnimalSpellingGame(root, on_close=on_close)

    if should_run_loop:
        root.mainloop()
    return app


if __name__ == "__main__":
    run_animal_spelling()
