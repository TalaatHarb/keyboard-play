"""Falling Letters & Numbers - Kids Typing & Sound Game."""

import math
import random
import string
import time
import tkinter as tk
from common import (
    PALETTE,
    TEXT_COLORS,
    NUMBER_WORDS,
    NUMPAD_KEYS,
    get_tts_engine,
    center_window,
)

MAX_LIVES = 7
BASE_SPAWN_INTERVAL_MS = 2500  # Starts relaxed ~24 per min
MIN_SPAWN_INTERVAL_MS = 500    # Capped at 120 per min (60,000 / 120 = 500ms)
BUBBLE_RADIUS = 38


class FallingItem:
    def __init__(self, char: str, speech_text: str, x: float, speed: float, color: str):
        self.char = char
        self.speech_text = speech_text
        self.x = x
        self.y = -BUBBLE_RADIUS
        self.speed = speed
        self.color = color
        self.tag = f"item_{id(self)}"
        self.popping = False
        self.pop_frame = 0


class FallingLettersGame:
    def __init__(self, root, on_close=None):
        self.root = root
        self.on_close = on_close
        self.root.title("Falling Letters Game - Pop the Keys!")
        self.root.minsize(700, 550)
        center_window(self.root, 900, 700)
        self.root.configure(bg="#DFF9FB")

        self.tts = get_tts_engine()

        # Game state variables
        self.score = 0
        self.lives = MAX_LIVES
        self.game_active = False
        self.game_over = False
        self.items: list[FallingItem] = []
        self.last_spawn_time = 0.0
        self.animation_job = None
        self.current_bg = "#DFF9FB"

        self._build_ui()
        self._bind_events()
        self.start_game()

    def _build_ui(self):
        # Header / Stats Bar
        self.stats_bar = tk.Frame(self.root, bg="#FFFFFF", height=60, padx=20, pady=10)
        self.stats_bar.pack(side=tk.TOP, fill=tk.X)

        self.score_label = tk.Label(
            self.stats_bar,
            text="⭐ Score: 0",
            font=("Segoe UI", 18, "bold"),
            bg="#FFFFFF",
            fg="#6C5CE7",
        )
        self.score_label.pack(side=tk.LEFT, padx=10)

        self.speed_label = tk.Label(
            self.stats_bar,
            text="🚀 Speed: 24/min",
            font=("Segoe UI", 14, "bold"),
            bg="#FFFFFF",
            fg="#00B894",
        )
        self.speed_label.pack(side=tk.LEFT, padx=20)

        self.lives_label = tk.Label(
            self.stats_bar,
            text="❤️❤️❤️❤️❤️❤️❤️",
            font=("Segoe UI", 18),
            bg="#FFFFFF",
            fg="#D63031",
        )
        self.lives_label.pack(side=tk.RIGHT, padx=10)

        # Main Game Canvas
        self.canvas = tk.Canvas(
            self.root,
            bg=self.current_bg,
            highlightthickness=0,
        )
        self.canvas.pack(expand=True, fill=tk.BOTH, padx=15, pady=(10, 5))

        # Bottom control/tip bar
        self.footer = tk.Frame(self.root, bg=self.current_bg)
        self.footer.pack(side=tk.BOTTOM, fill=tk.X, pady=(0, 10))

        self.tip_label = tk.Label(
            self.footer,
            text="Type the falling letters/numbers on your keyboard! | Esc to return | F11 Fullscreen",
            font=("Segoe UI", 11),
            bg=self.current_bg,
            fg="#636E72",
        )
        self.tip_label.pack()

    def _bind_events(self):
        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<F11>", self.toggle_fullscreen)

    def toggle_fullscreen(self, event=None):
        is_fs = self.root.attributes("-fullscreen")
        self.root.attributes("-fullscreen", not is_fs)

    def get_current_spawn_interval_ms(self) -> float:
        """Gradually scale spawn speed from 24 lpm (2500ms) down to 120 lpm (500ms)."""
        # Score of 50 reaches max difficulty
        progress = min(1.0, self.score / 50.0)
        return BASE_SPAWN_INTERVAL_MS - progress * (BASE_SPAWN_INTERVAL_MS - MIN_SPAWN_INTERVAL_MS)

    def get_current_falling_speed(self) -> float:
        """Item falling speed in pixels per frame (smooth motion)."""
        progress = min(1.0, self.score / 50.0)
        return 2.5 + progress * 4.5

    def start_game(self):
        self.score = 0
        self.lives = MAX_LIVES
        self.game_active = True
        self.game_over = False
        self.items.clear()
        self.canvas.delete("all")
        self.last_spawn_time = time.time()
        self.update_stats_display()
        self.tts.speak("Let's play! Catch the letters!")
        self._game_loop()

    def update_stats_display(self):
        self.score_label.configure(text=f"⭐ Score: {self.score}")
        lpm = int(60000 / self.get_current_spawn_interval_ms())
        self.speed_label.configure(text=f"🚀 Speed: {lpm}/min")
        hearts = "❤️" * self.lives + "🖤" * (MAX_LIVES - self.lives)
        self.lives_label.configure(text=hearts)

    def spawn_item(self):
        canvas_width = max(400, self.canvas.winfo_width())
        min_x = BUBBLE_RADIUS + 20
        max_x = max(min_x + 50, canvas_width - BUBBLE_RADIUS - 20)
        x = random.uniform(min_x, max_x)

        # 75% uppercase letters, 25% numbers
        if random.random() < 0.75:
            char = random.choice(string.ascii_uppercase)
            speech = char
        else:
            num = random.choice(string.digits)
            char = num
            speech = NUMBER_WORDS[num]

        color = random.choice(TEXT_COLORS)
        speed = self.get_current_falling_speed()
        item = FallingItem(char, speech, x, speed, color)
        self.items.append(item)

    def _game_loop(self):
        if not self.game_active:
            return

        now = time.time()
        interval_s = self.get_current_spawn_interval_ms() / 1000.0
        if now - self.last_spawn_time >= interval_s:
            self.spawn_item()
            self.last_spawn_time = now

        canvas_height = self.canvas.winfo_height()
        if canvas_height < 100:
            canvas_height = 500

        to_remove = []
        for item in self.items:
            if item.popping:
                item.pop_frame += 1
                if item.pop_frame > 6:
                    to_remove.append(item)
                    continue
            else:
                item.y += item.speed

                # Check if item reached the bottom
                if item.y - BUBBLE_RADIUS > canvas_height:
                    to_remove.append(item)
                    self.on_miss(item)

        for it in to_remove:
            if it in self.items:
                self.items.remove(it)
            self.canvas.delete(it.tag)

        self._draw_items()

        if self.lives > 0:
            self.animation_job = self.root.after(20, self._game_loop)
        else:
            self.trigger_game_over()

    def _draw_items(self):
        for item in self.items:
            self.canvas.delete(item.tag)
            r = BUBBLE_RADIUS
            if item.popping:
                # Expand radius and fade out
                r = BUBBLE_RADIUS + item.pop_frame * 6
                # Draw starburst / pop ring
                self.canvas.create_oval(
                    item.x - r, item.y - r, item.x + r, item.y + r,
                    outline="#FFD700", width=3, tag=item.tag
                )
                self.canvas.create_text(
                    item.x, item.y,
                    text="✨",
                    font=("Segoe UI", 24),
                    tag=item.tag
                )
            else:
                # Shadow
                self.canvas.create_oval(
                    item.x - r + 3, item.y - r + 3, item.x + r + 3, item.y + r + 3,
                    fill="#BDC3C7", outline="", tag=item.tag
                )
                # Outer colorful bubble
                self.canvas.create_oval(
                    item.x - r, item.y - r, item.x + r, item.y + r,
                    fill="#FFFFFF", outline=item.color, width=4, tag=item.tag
                )
                # Character
                self.canvas.create_text(
                    item.x, item.y,
                    text=item.char,
                    font=("Arial Rounded MT Bold", 32, "bold"),
                    fill=item.color,
                    tag=item.tag
                )

    def on_key_press(self, event):
        keysym = event.keysym
        char = event.char

        if keysym == "Escape":
            self.game_active = False
            if self.on_close:
                self.on_close()
            else:
                self.root.destroy()
            return

        if self.game_over:
            if keysym in ("space", "Return"):
                self.start_game()
            return

        pressed_val = None

        # Handle numpad
        if keysym in NUMPAD_KEYS:
            pressed_val = NUMPAD_KEYS[keysym]
        elif char:
            pressed_val = char.upper()

        if not pressed_val:
            return

        # Find matching falling item (prioritize the lowest item on screen)
        matched_item = None
        lowest_y = -9999
        for item in self.items:
            if not item.popping and item.char == pressed_val:
                if item.y > lowest_y:
                    lowest_y = item.y
                    matched_item = item

        if matched_item:
            # Correct hit!
            matched_item.popping = True
            self.score += 1
            self.update_stats_display()
            # Speak the hit letter / number name
            self.tts.speak(matched_item.speech_text)
        else:
            # Wrong key pressed -> counts as a mistake (life lost)
            if pressed_val.isalnum() and len(pressed_val) == 1:
                self.lives = max(0, self.lives - 1)
                self.update_stats_display()
                # Flash background briefly
                self._flash_canvas("#FF7675")
                self.tts.speak("Oops!")
                if self.lives == 0:
                    self.trigger_game_over()

    def on_miss(self, item: FallingItem):
        """When an item drops off the bottom of the screen."""
        self.lives = max(0, self.lives - 1)
        self.update_stats_display()
        self._flash_canvas("#FAB1A0")
        if self.lives == 0:
            self.trigger_game_over()

    def _flash_canvas(self, color):
        self.canvas.configure(bg=color)
        self.root.after(150, lambda: self.canvas.configure(bg=self.current_bg))

    def trigger_game_over(self):
        self.game_active = False
        self.game_over = True
        self.canvas.delete("all")

        self.canvas.create_text(
            self.canvas.winfo_width() / 2, 160,
            text="🎉 Great Job! 🎉",
            font=("Segoe UI", 36, "bold"),
            fill="#2D3436"
        )
        self.canvas.create_text(
            self.canvas.winfo_width() / 2, 230,
            text=f"Final Score: {self.score}",
            font=("Segoe UI", 28, "bold"),
            fill="#6C5CE7"
        )
        self.canvas.create_text(
            self.canvas.winfo_width() / 2, 310,
            text="Press SPACE to Play Again\nPress ESC to Return to Menu",
            font=("Segoe UI", 18),
            fill="#636E72",
            justify=tk.CENTER
        )
        self.tts.speak(f"Game over! Your score is {self.score}!")


def run_falling_game(root=None, on_close=None):
    should_run_loop = False
    if root is None:
        root = tk.Tk()
        should_run_loop = True

    app = FallingLettersGame(root, on_close=on_close)

    if should_run_loop:
        root.mainloop()
    return app


if __name__ == "__main__":
    run_falling_game()
