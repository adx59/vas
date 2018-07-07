#!/usr/bin/env python
import vas.handler as handler

class System:
    """Commands for interacting with the system."""
    def __init__(self, cmdhandler):
        self.cmdhandler = cmdhandler

    def cmd(self, responder, args):
        raise NotImplementedError

def setup(cmdhandler):
    cmdhandler.load_category(System(cmdhandler))