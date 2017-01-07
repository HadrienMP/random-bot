from unittest.mock import Mock

from application.bot import Bot
from tests.utils import build_message

bot = Bot()


def test_should_pass_a_named_parameter_to_the_command_when_defined():
    # GIVEN
    function_mock = Mock()
    bot.command("mock-command", params=["parameter"])(function_mock)
    message = build_message("/r mock-command --parameter one")

    # WHEN
    bot.respond_to(message)

    # THEN
    function_mock.assert_called_once_with(parameter="one")


def test_should_pass_named_parameters_to_the_command_when_defined():
    # GIVEN
    function_mock = Mock()
    bot.command("mock-command", params=["named1", "named2"])(function_mock)
    message = build_message("/r mock-command --named1 one --named2 two")

    # WHEN
    bot.respond_to(message)

    # THEN
    function_mock.assert_called_once_with(named1="one", named2="two")


def test_should_pass_named_parameters_to_the_command_even_when_separated_by_non_space_blanks():
    # GIVEN
    function_mock = Mock()
    bot.command("mock-command", params=["named1", "named2"])(function_mock)
    message = build_message("/r\t\u2002mock-command\u2002\t--named1\u2002one\t\u2002--named2\u2002two")

    # WHEN
    bot.respond_to(message)

    # THEN
    function_mock.assert_called_once_with(named1="one", named2="two")


def test_should_pass_parameter_with_different_names_in_definition_and_in_function():
    # GIVEN
    function = Mock()
    bot.command("command", params=["two->one"])(function)
    message = build_message("/r command --two one")

    # WHEN
    bot.respond_to(message)

    # THEN
    function.assert_called_once_with(one="one")

