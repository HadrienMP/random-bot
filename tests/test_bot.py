from ast import literal_eval

import pytest
from assertpy import assert_that

from application.bot import Bot
from tests.utils import build_message

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


# TODO automatic usage parameter
# TODO custom usage definition

# TODO what should happen when a mandatory defined parameter is not given ?
# TODO what should happen when an optional defined parameter is not given ?
# TODO what should happend when undefined parameters are given ?

# TODO handle short parameter names like -w instead of --without
# TODO handle presence parameters like --on to behave like on=true

