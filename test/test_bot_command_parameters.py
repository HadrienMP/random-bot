from assertpy import assert_that

from application.bot import Bot
from test.utils import build_message

bot = Bot()


def test_should_pass_a_named_parameter_to_the_command_when_defined():
    # GIVEN
    @bot.command("other-command", params=["parameter"])
    def other_command(parameter):
        return parameter

    message = build_message("/r other-command --parameter one")

    # WHEN
    response = bot.respond_to(message)

    # THEN
    assert_that(response).is_equal_to("one")


def test_should_pass_named_parameters_to_the_command_when_defined():
    # GIVEN
    @bot.command("other-command", params=["named1", "named2"])
    def other_command(named1, named2):
        return named1 + " " + named2

    message = build_message("/r other-command --named1 one --named2 two")

    # WHEN
    response = bot.respond_to(message)

    # THEN
    assert_that(response).is_equal_to("one two")
