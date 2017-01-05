from application.message_parser import parse

class CommandFactory:
    def __init__(self):
        self.command_definitions = dict()

    def register(self, function, command_name, params):
        self.command_definitions[command_name] = function

    # TODO test if the command match the parameters given (name, number)
    def create_for(self, json):
        try:
            command_name, parameters = parse(json)
            function = self.command_definitions.get(command_name)
            if function:
                return Command(function, parameters)
            else:
                return StaticResponse("Oops, I don't know this command :-(")
        except ValueError:
            return StaticResponse("Oops, I don't understand what you are saying :'(")


class AbstractCommand:
    def respond(self):
        pass


class StaticResponse(AbstractCommand):
    def __init__(self, message):
        self.message = message

    def respond(self):
        return self.message


class Command(AbstractCommand):
    def __init__(self, function, parameters):
        self.function = function
        self.parameters = parameters

    def respond(self):
        return self.function(**self.parameters)
