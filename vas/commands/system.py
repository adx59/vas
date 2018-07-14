#!/usr/bin/env python
import subprocess
import vas.handler as handler

class System:
    """Commands for interacting with the system."""
    def __init__(self, cmdhandler):
        self.__name__ = "System"
        self.cmdhandler = cmdhandler

    @handler.command(prompts=["cmd"], name="cmd")
    def cmd(self, responder, args):
        command = ' '.join(args) 

        cmd_process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = str(cmd_process.stdout)[2:-1].replace("\\n", "\n") 
        err = str(cmd_process.stderr)[2:-1].replace("\\n", "\n")

        responder.say("Executed command, check console for output.")
        print(f"Result [stdout]:\n{out}\n\nResult [stderr]:\n{err}")
        

def setup(cmdhandler):
    cmdhandler.load_category(System(cmdhandler), module_name="vas.commands.system")
    