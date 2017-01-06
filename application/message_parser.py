import re

PARAMETER_PATTERN = '.*'

COMMAND_PATTERN = r'[^\s]+'


def parse(json):
    message = __get_message(json)
    command_name, parameter_string = __parse(message)
    parameters = __get_parameters(parameter_string)
    return command_name, parameters


def __get_message(json):
    if __is_well_formed(json):
        return json['item']['message']['message']
    raise ValueError("unkown message format")


def __parse(message):
    m = re.search(r'^/[^\s]+\s+(' + COMMAND_PATTERN + ')\s*(' + PARAMETER_PATTERN + ')?$', message)
    if m:
        command_name = m.group(1)
        parameter_string = m.group(2)
        return command_name, parameter_string

    raise ValueError("unkown message format")


def __is_well_formed(json):
    return "item" in json and "message" in json["item"] and "message" in json["item"]["message"]


def __get_parameters(parameter_string):
    parameter_parts = re.split(r'\s+', parameter_string)
    parameters = dict()
    while len(parameter_parts) >= 2:
        parameter_name = parameter_parts.pop(0)[2:]
        parameter_value = parameter_parts.pop(0)
        parameters[parameter_name] = parameter_value

    return parameters
