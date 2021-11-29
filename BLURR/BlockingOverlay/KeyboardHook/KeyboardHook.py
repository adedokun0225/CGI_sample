import keyboard
from typing import Callable

PIN_KEYS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'backspace']
FORBIDDEN_KEYS = ['left alt', 'right alt',
                  'left control', 'right control', 'delete', 'windows']


class KeyboardHook():

    def __init__(self, pinFn: Callable, blockFn: Callable):
        self.pinFn = pinFn
        self.blockFn = blockFn
        pass

    # hooks for pinInput and blocks the control keys
    def hook(self):
        for key in PIN_KEYS:
            keyboard.add_hotkey(key, lambda: self.pinInput(key))
            keyboard.block_key(key)

        for key in FORBIDDEN_KEYS:
            keyboard.add_hotkey(key, lambda: self.blockFn(key))
            keyboard.block_key(key)

    def unhook():
        keyboard.unhook_all()
