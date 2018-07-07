#!/usr/bin/env python
import os
import sys
import traceback

import vas.handler as handler

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

    @handler.command(prompts=["shutdown"], name="shutdown")
    def shutdown(self, responder, args):
        responder.say("Shutting down assistant...")
        os.system('taskkill /IM python.exe /F')

    @handler.command(prompts=["eval"], name="evaluate")
    def eval(self, responder, args):
        to_eval = ' '.join(args)
        try:
            res = eval(to_eval)
        except:
            traceback.print_exc()
            responder.say("That evaluation resulted in an error. Please check console for more information.")
            return
        responder.say(f"Evaluated. The result is {res}")

def setup(cmdhandler):
    cmdhandler.load_category(Basic(cmdhandler), module_name="vas.commands.basic")
