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
            parameters_to_send[destination_name] = given_parameters.get(source_name)

        return parameters_to_send

    def respond(self):
        return self.function(**self.parameters)