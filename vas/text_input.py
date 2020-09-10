#!/usr/bin/env python
import sys
import time
from threading import Thread

import pyperclip

if sys.platform == 'win32':
    import pyWinhook as pyHook
    import pythoncom
elif sys.platform == 'linux' or sys.platform == 'linux2':
    import linux.pyxhook as pyxhook


class Input:
    def __init__(self, parent):
        self.parent = parent

    def poll_keyboard(self):
        def on_keypress(event):
            nonlocal self
            key = event.Key
            if key == "F7":
                query = pyperclip.paste()
                print(f'[INFO] Processing query "{query}"...')
                
                self.parent.command_handler.handle_command(query.split())

            return True
        
        if sys.platform == 'win32':
            hook_manager = pyHook.HookManager()
            hook_manager.KeyDown = on_keypress
            hook_manager.HookKeyboard()
            pythoncom.PumpMessages()
        elif sys.platform == 'linux' or sys.platform == 'linux2':
            hook_manager = pyxhook.HookManager()
            hook_manager.KeyDown = on_keypress
            hook_manager.HookKeyboard()
            hook_manager.start()
    
    def launch(self):
        poll_keyboard_thread = Thread(target=self.poll_keyboard)
        poll_keyboard_thread.daemon = True
        poll_keyboard_thread.start()
