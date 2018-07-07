#!/usr/bin/env python
import os
import sys

import vas.handler as handler
from vas.handler import Command

class Basic:
    def __init__(self, cmdhandler):
        self.__name__ = "Basic"
        self.cmdhandler = cmdhandler

    @handler.command(prompts=["hello", "there"], name="hello")
    def hello(self, responder, args):
        responder.say("Hi there. I exist.")

    @handler.command(prompts=["restart"], name="restart")
    def restart(self, responder, args):
        responder.say("Restarting...")
        os.system('cls')
        os.execl(sys.executable, sys.executable, * sys.argv)

    @handler.command(prompts=["eval"], name="evaluate")
    def eval(self, responder, args):
        to_eval = ' '.join(args)
        res = eval(to_eval)
        responder.say(f"Evaluated. The result is {res}")

def setup(cmdhandler):
    cmdhandler.load_category(Basic(cmdhandler), module_name="vas.commands.basic")
    