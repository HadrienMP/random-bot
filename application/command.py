import re

PARAMETER_PATTERN = '.*'

COMMAND_PATTERN = r'[^\s]+'

class Command:
    def __init__(self, json):
        self.name, self.parameters = Command.__parse(json)

    @staticmethod
    def __parse(json):
        message = Command.__get_message(json)
        m = re.search(r'^/[^\s]+\s(' + COMMAND_PATTERN + ')\s?(' + PARAMETER_PATTERN + ')$', message)
        if m:
            command_name = m.group(1)
            parameter_string = m.group(2)
            parameters = Command.__get_parameters(parameter_string)
            return command_name, parameters
            
        raise ValueError("unkown message format")
        
    @staticmethod
    def __get_message(json):
        if Command.__is_well_formed(json):
            return json['item']['message']['message']
        raise ValueError("unkown message format")

    @staticmethod
    def __is_well_formed(json):
        return "item" in json and "message" in json["item"] and "message" in json["item"]["message"]
    
    @staticmethod
    def __get_parameters(parameter_string):
        # TODO test command with unicode blanks or tabs instead of spaces
        parameter_parts = parameter_string.split(" ")
        parameters = dict()
        while len(parameter_parts) >= 2:
            parameter_name = parameter_parts.pop(0)[2:]
            parameter_value = parameter_parts.pop(0)
            parameters[parameter_name] = parameter_value
            
        return parameters
