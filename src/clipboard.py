import pyperclip
from pynput.keyboard import Controller, Key
import time

def copy_selection():
    """Simulates Cmd+C to copy selected text and returns it."""
    controller = Controller()
    with controller.pressed(Key.cmd):
        controller.press('c')
        controller.release('c')
    time.sleep(0.1)
    return pyperclip.paste()

def select_all():
    """Simulates Cmd+A to select all text."""
    controller = Controller()
    with controller.pressed(Key.cmd):
        controller.press('a')
        controller.release('a')
    time.sleep(0.1)

def paste_text(text):
    """Pastes the given text using Cmd+V."""
    pyperclip.copy(text)
    controller = Controller()
    with controller.pressed(Key.cmd):
        controller.press('v')
        controller.release('v')
    time.sleep(0.1)

def move_cursor_right():
    """Moves the cursor right to deselect text."""
    controller = Controller()
    controller.press(Key.right)
    controller.release(Key.right)
