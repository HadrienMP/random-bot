from application.command import CommandFactory


class Bot:
    def __init__(self):
        self.command_factory = CommandFactory()

    def command(self, command, params=[]):
        """
        Decorator function to register python functions as able to answer
        specific bot commands.
        """
        def decorator(function):
            self.command_factory.register(function, command, params)
            return function

        return decorator

    def respond_to(self, json):
        """
        Function that will call the function that is able to answer to the 
        command given in the hipchat json
        """
        command = self.command_factory.create_for(json)
        return command.respond()
