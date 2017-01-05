from application.command import CommandFactory


class Bot:
    def __init__(self):
        self.command_factory = CommandFactory()

    def command(self, command, params=[]):
        def decorator(function):
            self.command_factory.register(function, command, params)
            return function

        return decorator

    def respond_to(self, json):
        command = self.command_factory.create_for(json)
        return command.respond()
