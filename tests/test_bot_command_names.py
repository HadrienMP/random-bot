import re
from unittest.mock import Mock

import pytest
from assertpy import assert_that
from hypothesis import assume
from hypothesis import given
from hypothesis.strategies import text

from application.bot import Bot
from application.command_factory import CommandNameError
from tests.utils import build_message

bot = Bot()

expected_response = "Je suis la commande tests "


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


def test_should_call_the_mapped_function_for_a_mapped_command_even_when_non_blank_spaces_are_used():
    # GIVEN
    message = build_message("/r\t\u2002command")

    # WHEN
    response = bot.respond_to(message)

    # THEN
    assert_that(response).is_equal_to(expected_response)


@given(text())
def should_be_able_to_respond_to_all_non_blank_command_names(random_command_name):
    assume(not re.match(r"^\s*$", random_command_name))

    # GIVEN
    function_mock = Mock()
    bot.command(random_command_name)(function_mock)
    message = build_message("/r " + random_command_name)

    # WHEN
    response = bot.respond_to(message)

    # THEN
    function_mock.assert_called_once()


@pytest.mark.parametrize("impossible_command_name", ["imp oss ible", "\u2002", "\t", " ", "\n"])
def test_should_throw_an_exception_on_startup_when_an_impossible_parameter_name_is_defined(impossible_command_name):
    function = Mock()

    with pytest.raises(CommandNameError):
        bot.command(impossible_command_name)(function)

