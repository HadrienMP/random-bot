class Bot:
    def __init__(self):
        self.commands = dict()

    def command(self, command):
        def decorator(function):
            self.commands[command] = function
            return function

        return decorator

    def respond_to(self, json):
        try:
            command = Command(json)
            command_function = self.commands.get(command.name)
            if command_function:
                return command_function(command.parameters)
            else:
                return "Oops I don't know this command :-("
        except ValueError:
            return "Oops I don't understand this message, maybe hipchat changed it's api ? :'("


class Command:
    def __init__(self, json):
        if self.__is_well_formed(json):
            message = json['item']['message']['message']
            message_parts = message.split(" ")
            self.name = message_parts[1]
            self.parameters = message_parts[2] if len(message_parts) > 2 else ""
        else:
            raise ValueError("unkown message format")

    @staticmethod
    def __is_well_formed(json):
        return "item" in json and "message" in json["item"] and "message" in json["item"]["message"]
