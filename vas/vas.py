#!/usr/bin/env python
import time
import traceback
from threading import Thread
from vas import responder, text_input, handler

class Vas:
    MODULES = [
        'vas.commands.basic'
    ]
    def __init__(self):
        self.responder = responder.Responder(self)
        self.text_input = text_input.Input(self)

        self.command_handler = handler.Handler(self, self.responder)

    def launch(self):
        for module in self.MODULES:
            try:
                self.command_handler.load_module(module)
            except:
                traceback.print_exc()

        self.text_input.launch()
        self.responder.launch()
