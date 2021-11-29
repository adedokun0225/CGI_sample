from pynput import keyboard
from typing import Callable

PIN_KEYS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'backspace']
FORBIDDEN_KEYS = ['left alt', 'right alt',
                  'left control', 'right control', 'delete', 'windows']


class KeyboardHook():

    def __init__(self, pinFn: Callable, blockFn: Callable):
        self.pinFn = pinFn
        self.listener = None
        pass

    # hooks for pinInput and blocks the control keys
    def hook(self):
        if self.listener is not None:
            return
        self.listener = keyboard.Listener(
            suppress=True,
            on_press=self.on_press)
        self.listener.start()

    def on_press(self, key):
        if hasattr(key, "char"):
            self.pinFn(key.char)
            return

        if key == keyboard.Key.backspace:
            self.pinFn("back")
            return

        return

    def unhook(self):
        self.listener.stop()
        self.listener = None
