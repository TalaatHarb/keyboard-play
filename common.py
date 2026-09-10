"""Common shared utilities, constants, and Text-to-Speech engine for Kids Learning Apps."""

import queue
import random
import sys
import threading
import tkinter as tk

# Try initializing Windows native TTS (SAPI.SpVoice via win32com or COM)
try:
    import pythoncom
    import win32com.client
    HAS_SAPI = True
except ImportError:
    HAS_SAPI = False

if not HAS_SAPI:
    try:
        import pyttsx3
        HAS_PYTTSX3 = True
    except ImportError:
        HAS_PYTTSX3 = False
else:
    HAS_PYTTSX3 = False

# Bright, friendly color palette
PALETTE = [
    "#FFEAA7",  # Soft Banana Yellow
    "#FAB1A0",  # Peach
    "#81ECEC",  # Light Aqua
    "#74B9FF",  # Sky Blue
    "#A29BFE",  # Lavender Purple
    "#55EFC4",  # Mint Green
    "#FD79A8",  # Bubblegum Pink
    "#FF7675",  # Coral Red
    "#FEEAA7",  # Cream
    "#DFF9FB",  # Ice Blue
]

TEXT_COLORS = [
    "#6C5CE7",  # Purple
    "#D63031",  # Red
    "#0984E3",  # Blue
    "#00B894",  # Emerald
    "#E17055",  # Orange
    "#E84393",  # Pink
    "#2D3436",  # Charcoal
]

# Spoken representations for numbers
NUMBER_WORDS = {
    '0': "Zero", '1': "One", '2': "Two", '3': "Three", '4': "Four",
    '5': "Five", '6': "Six", '7': "Seven", '8': "Eight", '9': "Nine"
}

# Key symbols for NumPad keys
NUMPAD_KEYS = {
    'KP_0': '0', 'KP_1': '1', 'KP_2': '2', 'KP_3': '3', 'KP_4': '4',
    'KP_5': '5', 'KP_6': '6', 'KP_7': '7', 'KP_8': '8', 'KP_9': '9',
    'KP_Decimal': '.', 'KP_Add': '+', 'KP_Subtract': '-', 'KP_Multiply': '*', 'KP_Divide': '/',
    'KP_Enter': 'Enter',
}

# Spoken descriptions for special keys
SPECIAL_KEYS = {
    'space': ("SPACE", "Space"),
    'Return': ("ENTER", "Enter"),
    'BackSpace': ("\u232B", "Backspace"),
    'Tab': ("TAB", "Tab"),
    'Escape': ("ESC", "Escape"),
    'plus': ("+", "Plus"),
    'minus': ("-", "Minus"),
    'asterisk': ("*", "Multiply"),
    'slash': ("/", "Divide"),
    'equal': ("=", "Equals"),
    'period': (".", "Dot"),
    'comma': (",", "Comma"),
    'exclam': ("!", "Exclamation mark"),
    'question': ("?", "Question mark"),
}


class TTSEngine:
    """Thread-safe persistent TTS engine worker."""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(TTSEngine, cls).__new__(cls)
                cls._instance._init_worker()
            return cls._instance

    def _init_worker(self):
        self.speech_queue = queue.Queue()
        self.thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.thread.start()

    def _worker_loop(self):
        if HAS_SAPI:
            pythoncom.CoInitialize()
            try:
                speaker = win32com.client.Dispatch("SAPI.SpVoice")
                speaker.Rate = 0
                speaker.Volume = 100
                while True:
                    text = self.speech_queue.get()
                    if text is None:
                        break
                    try:
                        # Flag 2 = SVSFPurgeBeforeSpeak
                        speaker.Speak(text, 2)
                    except Exception as e:
                        print(f"TTS Speech Error: {e}", file=sys.stderr)
                    self.speech_queue.task_done()
            finally:
                pythoncom.CoUninitialize()
        elif HAS_PYTTSX3:
            try:
                engine = pyttsx3.init()
                while True:
                    text = self.speech_queue.get()
                    if text is None:
                        break
                    try:
                        engine.say(text)
                        engine.runAndWait()
                    except Exception as e:
                        print(f"TTS Error: {e}", file=sys.stderr)
                    self.speech_queue.task_done()
            except Exception as e:
                print(f"Failed to init pyttsx3: {e}", file=sys.stderr)

    def speak(self, text: str, purge: bool = True):
        """Queue text to be spoken. If purge is True, clears older queued speech."""
        if not text:
            return
        if purge:
            while not self.speech_queue.empty():
                try:
                    self.speech_queue.get_nowait()
                    self.speech_queue.task_done()
                except queue.Empty:
                    break
        self.speech_queue.put(text)


def get_tts_engine() -> TTSEngine:
    return TTSEngine()


def center_window(window: tk.Tk | tk.Toplevel, width: int = 900, height: int = 700):
    """Centers a tkinter window on the user's primary monitor."""
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = max(0, (screen_width - width) // 2)
    y = max(0, (screen_height - height) // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")
