from unittest.mock import Mock

import pytest
from assertpy.assertpy import assert_that

from application.bot import Bot
from application.command_factory import ParameterNameError
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


@pytest.mark.parametrize("impossible_parameter_name", ["imp oss ible", "name->another-impossible_parameter"])
def test_should_throw_an_exception_on_startup_when_an_impossible_parameter_name_is_defined(impossible_parameter_name):
    """Parameter names are mapped directly to python names, so any impossible
    python variable name is an invalid parameter"""
    function = Mock()

    with pytest.raises(ParameterNameError):
        bot.command("command", params=["param", impossible_parameter_name])(function)


def test_should_ignore_missing_optional_parameters():
    # GIVEN
    @bot.command("command", params=["mandatory", "optional"])
    def command(mandatory, optional=None):
        return "called"

    message = build_message("/r command --mandatory value")

    # WHEN
    result = bot.respond_to(message)

    # THEN
    assert_that(result).is_equal_to("called")


def test_should_detect_parameters_from_the_signature():
    # GIVEN
    @bot.command("mock-command")
    def command(parameter, parameter_2, optional=None):
        return parameter, parameter_2, optional

    message = build_message("/r mock-command --parameter one --parameter_2 two --optional three")

    # WHEN
    answer = bot.respond_to(message)

    # THEN
    assert_that(answer).is_equal_to(("one", "two", "three"))

