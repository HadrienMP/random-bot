import inspect
import re

from application.message_parser import parse
from application.commands import *

class CommandFactory:
    def __init__(self):
        self.command_definitions = dict()

    def register(self, function, command_name, parameters):
        if _is_legal(command_name):
            self.command_definitions[command_name] = CommandDefinition(function, parameters)
        else:
            raise CommandNameError

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


def _is_legal(command_name):
    return re.match(r'^[^\s]+$', command_name)


class CommandDefinition:
    def __init__(self, function, parameters):
        self.function = function
        parameters += _detect_function_parameters(function)
        self.parameters_mapping = _build_mapping(parameters)


def _detect_function_parameters(function):
    function_parameters = [param.name for param in inspect.signature(function).parameters.values()]
    function_parameters = [param for param in function_parameters if param not in ['args', 'kwargs']]
    return function_parameters


def _build_mapping(parameters) -> dict:
    parameters_mapping = dict()
    for parameter in parameters:
        if "->" in parameter:
            source_name, destination_name = parameter.split("->")
            __checkParameterName(destination_name)
            parameters_mapping[source_name] = destination_name
        else:
            __checkParameterName(parameter)
            parameters_mapping[parameter] = parameter
    return parameters_mapping


def __checkParameterName(destination_name):
    if not str(destination_name).isidentifier():
        raise ParameterNameError


class ParameterNameError(Exception):
    pass


class CommandNameError(Exception):
    pass