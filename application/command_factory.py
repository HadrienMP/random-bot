import inspect

from application.message_parser import parse
from application.commands import *

class CommandFactory:
    def __init__(self):
        self.command_definitions = dict()

    def register(self, function, command_name, parameters):
        self.command_definitions[command_name] = CommandDefinition(function, parameters)

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
        parameters += CommandDefinition.__detect_function_parameters(function)
        self.parameters_mapping = CommandDefinition.__build_mapping(parameters)

    @staticmethod
    def __detect_function_parameters(function):
        function_parameters = [param.name for param in inspect.signature(function).parameters.values()]
        function_parameters = [param for param in function_parameters if param not in ['args', 'kwargs']]
        return function_parameters

    @staticmethod
    def __build_mapping(parameters) -> dict:
        parameters_mapping = dict()
        for parameter in parameters:
            if "->" in parameter:
                source_name, destination_name = parameter.split("->")
                CommandDefinition.checkParameterName(destination_name)
                parameters_mapping[source_name] = destination_name
            else:
                CommandDefinition.checkParameterName(parameter)
                parameters_mapping[parameter] = parameter
        return parameters_mapping

    @staticmethod
    def checkParameterName(destination_name):
        if not str(destination_name).isidentifier():
            raise ParameterNameError


class ParameterNameError(Exception):
    pass