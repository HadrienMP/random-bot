import re

PARAMETER_PATTERN = '.*'

COMMAND_PATTERN = r'[^\s]+'


class Bot:
    def __init__(self):
        self.commands = dict()

    def command(self, command, params=[]):
        def decorator(function):
            self.commands[command] = CommandDefinition(function, params)
            return function

        return decorator

    def respond_to(self, json):
        try:
            command = Command(json)
            command_definition = self.commands.get(command.name)
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


class Command:
    def __init__(self, json):
        self.name, parameter_string = Command.__parse(json)
        self.parameters = Command.__get_parameters(parameter_string)

    @staticmethod
    def __get_message(json):
        if Command.__is_well_formed(json):
            return json['item']['message']['message']
        raise ValueError("unkown message format")

    @staticmethod
    def __parse(json):
        if Command.__is_well_formed(json):
            message = json['item']['message']['message']
            m = re.search(r'^/[^\s]+\s(' + COMMAND_PATTERN + ')\s?(' + PARAMETER_PATTERN + ')$', message)
            if m:
                return m.group(1), m.group(2)
        
        raise ValueError("unkown message format")

    @staticmethod
    def __is_well_formed(json):
        return "item" in json and "message" in json["item"] and "message" in json["item"]["message"]
    
    @staticmethod
    def __get_parameters(parameter_string):
        parameter_parts = parameter_string.split(" ")
        parameters = dict()
        while len(parameter_parts) >= 2:
            parameter_name = parameter_parts.pop(0)[2:]
            parameter_value = parameter_parts.pop(0)
            parameters[parameter_name] = parameter_value
            
        return parameters
