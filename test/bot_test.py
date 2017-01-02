from application.bot import Bot
from assertpy import assert_that
from test.utils import build_message
from nose_parameterized import parameterized
from ast import literal_eval
from mock import patch

bot = Bot()

expected_response = "Je suis la commande test "


@bot.command("command")
def command_function(parameter=""):
    return expected_response


def test_should_call_the_mapped_function_for_a_mapped_command():
    # GIVEN
    message = build_message("/r command")

    # WHEN
    response = bot.respond_to(message)

    # THEN
    assert_that(response).is_equal_to(expected_response)


@patch("test.bot_test.command_function")
def test_should_call_the_mapped_function_for_a_mapped_command_with_the_parameter(command_function_mock):
    # GIVEN
    bot.command("command")(command_function_mock)
    message = build_message("/r command nameless-param")

    # WHEN
    response = bot.respond_to(message)

    # THEN
    command_function_mock.assert_called_once_with("nameless-param")


def test_should_return_a_static_error_message_for_an_unmapped_command():
    # GIVEN
    message = build_message("/r toto")

    # WHEN
    response = bot.respond_to(message)

    # THEN
    assert_that(response).is_equal_to("Oops I don't know this command :-(")


@parameterized([
    "{'broken': 'message_format'}",
    "{'item': 'still broken'}",
    "{'item': {'message': 'still broken'}}",
    "{'item': {'message': {'still': 'broken'}}}",
])
def test_should_return_a_static_error_message_for_a_wrong_format_message(message_str):
    message = literal_eval(message_str)

    # WHEN
    response = bot.respond_to(message)

    # THEN
    assert_that(response).is_equal_to("Oops I don't understand this message, maybe hipchat changed it's api ? :'(")
