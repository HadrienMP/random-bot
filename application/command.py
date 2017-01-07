from application.message_parser import parse

class CommandFactory:
    def __init__(self):
        self.command_definitions = dict()

    def register(self, function, command_name, parameters):
        self.command_definitions[command_name] = CommandDefinition(function, parameters)

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


class CommandDefinition:
    def __init__(self, function, parameters):
        self.function = function
        self.parameters_mapping = CommandDefinition.__build_mapping(parameters)

    @staticmethod
    def __build_mapping(parameters) -> dict:
        parameters_mapping = dict()
        for parameter in parameters:
            if "->" in parameter:
                source_name, destination_name = parameter.split("->")
                parameters_mapping[source_name] = destination_name
            else:
                parameters_mapping[parameter] = parameter
        return parameters_mapping


class AbstractCommand:
    def respond(self):
        pass


class StaticResponse(AbstractCommand):
    def __init__(self, message):
        self.message = message

    def respond(self):
        return self.message


class Command(AbstractCommand):
    def __init__(self, definition, given_parameters):
        self.function = definition.function
        self.parameters = Command.__map(given_parameters, definition.parameters_mapping)

    @staticmethod
    def __map(given_parameters, parameters_mapping):
        parameters_to_send = dict()
        for source_name, destination_name in parameters_mapping.items():
            # TODO what should happen when a mandatory defined parameter is not given ?
            # TODO what should happen when an optional defined parameter is not given ?
            # TODO what should happend when undefined parameters are given ?
            parameters_to_send[destination_name] = given_parameters[source_name]

        return parameters_to_send

    def respond(self):
        return self.function(**self.parameters)
