class Bot:
    def __init__(self):
        self.commands = dict()
    
    def command(self, command):
        
        def decorator(function):
            self.commands[command] = function
            return function
            
        return decorator
        
    def respond_to(self, message):
        if "item" in message.keys():
        
            command = message['item']['message']['message'].split(" ")[1]
            command_function = self.commands.get(command)
            if command_function:
                return command_function()
            else:
                return "Oops I don't know this command :-("
        else:
            return "Oops I don't understand this message, maybe hipchat changed it's api ? :'("