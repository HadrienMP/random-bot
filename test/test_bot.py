from application.bot import Bot
from assertpy import assert_that
from test.utils import build_message
from nose_parameterized import parameterized
from ast import literal_eval
from mock import patch
from mock import Mock

bot = Bot()

expected_response = "Je suis la commande test "


@bot.command("command")
def command_function(parameters=""):
    return expected_response


def test_should_call_the_mapped_function_for_a_mapped_command():
    # GIVEN
    message = build_message("/r command")

    # WHEN
    response = bot.respond_to(message)

    # THEN
    assert_that(response).is_equal_to(expected_response)
    
    
def test_should_pass_a_named_parameter_to_the_command_when_defined():
    # GIVEN
    @bot.command("other-command", params=["without"])
    def other_command(without):
        return without
        
    message = build_message("/r other-command --without you")
    
    # WHEN
    response = bot.respond_to(message)
    
    # THEN
    assert_that(response).is_equal_to("you")
    
# TODO handle presence parameters like --on to behave like on=true
# TODO handle short parameter names like -w instead of --without
# TODO handle hyphens and underscores in parameter names
    
def test_should_pass_a_named_parameter_to_the_command_when_defined():
    # GIVEN
    @bot.command("other-command", params=["without"])
    def other_command(without):
        return without
        
    message = build_message("/r other-command --without you")
    
    # WHEN
    response = bot.respond_to(message)
    
    # THEN
    assert_that(response).is_equal_to("you")
    
    
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
    


def test_should_return_a_static_error_message_for_an_unmapped_command():
    # GIVEN
    message = build_message("/r toto")

    # WHEN
    response = bot.respond_to(message)

    # THEN
    assert_that(response).is_equal_to("Oops, I don't know this command :-(")


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
    assert_that(response).is_equal_to("Oops, I don't understand what you are saying :'(")
