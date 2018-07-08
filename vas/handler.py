#!/usr/bin/env python
import inspect
import importlib

class Command:
    def __init__(self, prompts: list, name: str, invoke):
        self.name = name
        self.prompts = prompts
        self.invoke_func = invoke
        self.category = None
        self.module = None

    def invoke(self, *arguments: list):
        self.invoke_func(*arguments)

class Handler:
    CONNECTING_WORDS = ["to"]

    def __init__(self, parent, responder):
        self.parent = parent
        self.responder = responder

        self.modules = {}
        self.categories = {}
        self.commands = {}

    def handle_command(self, prompts):
        """Handles a command with prompts"""
        for cmd_prompts in self.commands:
            cmd_list_prompts = cmd_prompts.split()
            print(f'[HNDL] Comparing {prompts} to {cmd_list_prompts}')
            if ' '.join(cmd_list_prompts) in ' '.join(prompts):
                filtered_args = [p for p in prompts if p not in cmd_list_prompts and p\
                                 not in self.CONNECTING_WORDS]

                print("[INFO] Found a command matching those prompts,"+\
                    f" invoking command:{self.commands[cmd_prompts].name}")

                if self.commands[cmd_prompts].module in self.modules:
                    category = self.categories[self.commands[cmd_prompts].category]
                    self.commands[cmd_prompts].invoke(category, self.responder, filtered_args)
                else:
                    self.commands[cmd_prompts].invoke(self.responder, filtered_args)
                return

    def add_command(self, command: Command):
        """Add a command to the commands list."""
        if ' '.join(command.prompts) in self.commands:
            raise Exception('Already a command with those prompts.')
    
        self.commands[' '.join(command.prompts)] = command

    def load_module(self, module_name: str):
        """Loads a module. 
        
        Module must have a setup function."""
        module = importlib.import_module(module_name)
        try:
            module.setup(self)
            self.modules[module_name] = module
        except AttributeError:
            raise Exception('Module does not have a setup function.')
        else:
            print(f'[LOAD] Loaded module {module_name} successfully!')

    def unload_module(self, module_name: str):
        """Unloads a module."""
        if module_name not in self.modules:
            raise Exception("Module does not exist")
        
        del self.modules[module_name]

        to_delete = []
        for command in self.commands:
            if self.commands[command].module == module_name:
                to_delete.append(command)
        
        for d in to_delete:
            del self.commands[d]

        print(f'[LOAD] Unloaded module {module_name}')
        
    def reload_module(self, module_name: str):
        """Reloads a module."""
        self.unload_module(module_name)
        self.load_module(module_name)

    def load_category(self, category, module_name):
        """Loads commands from a module's category class."""
        self.categories[category.__name__] = category
        for func in inspect.getmembers(category):
            if isinstance(func[1], Command):
                func[1].category = category.__name__
                func[1].module = module_name
                self.add_command(func[1])

def command(prompts=None, name=None, module=None):
    """Decorator to transform a function into a command."""
    def predicate(func):
        return Command(prompts=prompts, name=name, invoke=func)
    return predicate
