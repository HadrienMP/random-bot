from application.command import Command

class Bot:
    def __init__(self):
        self.command_definitions = dict()

    def command(self, command, params=[]):
        def decorator(function):
            self.command_definitions[command] = CommandDefinition(function, params)
            return function

        return decorator

    def respond_to(self, json):
        try:
            command = Command(json)
            command_definition = self.command_definitions.get(command.name)
            if command_definition:
                return command_definition.function(**command.parameters)
            else:
                return "Oops, I don't know this command :-("
        except ValueError:
            return "Oops, I don't understand what you are saying :'("


class CommandDefinition:
    def __init__(self, function, params):
        self.function = function
        self.params = params
