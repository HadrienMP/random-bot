from ast import literal_eval
from unittest import TestCase
import pytest

from assertpy import assert_that
from nose_parameterized import parameterized

from application.bot import Bot
from test.utils import build_message

bot = Bot()


def test_should_return_a_static_error_message_for_an_unmapped_command():
    # GIVEN
    message = build_message("/r toto")

    # WHEN
    response = bot.respond_to(message)

    # THEN
    assert_that(response).is_equal_to("Oops, I don't know this command :-(")


@pytest.mark.parametrize("message_str", [
    "{'broken': 'message_format'}",
    "{'item': 'still broken'}",
    "{'item': {'message': 'still broken'}}",
    "{'item': {'message': {'still': 'broken'}}}",
    "{'item': {'message': {'message': 'still broken'}}}",
])
def test_should_return_a_static_error_message_for_a_wrong_format_message(message_str):
    message = literal_eval(message_str)

    # WHEN
    response = bot.respond_to(message)

    # THEN
    assert_that(response).is_equal_to("Oops, I don't understand what you are saying :'(")
