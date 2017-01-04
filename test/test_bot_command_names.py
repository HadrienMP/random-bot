import re

from assertpy import assert_that
from hypothesis import assume
from hypothesis import given
from hypothesis.strategies import text

from application.bot import Bot
from test.utils import build_message

bot = Bot()

expected_response = "Je suis la commande test "


@bot.command("command")
def command_function():
    return expected_response


def test_should_call_the_mapped_function_for_a_mapped_command():
    # GIVEN
    message = build_message("/r command")

    # WHEN
    response = bot.respond_to(message)

    # THEN
    assert_that(response).is_equal_to(expected_response)


@given(text())
def should_be_able_to_respond_to_all_non_blank_command_names(random_command_name):
    assume(not re.match(r"^\s*$", random_command_name))

    # GIVEN
    @bot.command(random_command_name)
    def other_command():
        return "Called"

    message = build_message("/r " + random_command_name)

    # WHEN
    response = bot.respond_to(message)

    # THEN
    assert_that(response).is_equal_to("Called")
