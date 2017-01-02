from application.bot import Bot
from assertpy import assert_that
from test.utils import build_message

bot = Bot()

def test_should_call_the_mapped_function_for_a_mapped_command():
    # GIVEN
    expected_response = "Je suis la commande test"
    
    @bot.command("test")
    def test():
        return expected_response
        
    message = build_message("/r test")
        
    # WHEN
    response = bot.respond_to(message)
        
    # THEN
    assert_that(response).is_equal_to(expected_response)
    

def test_should_return_a_static_error_message_for_an_unmapped_command():
    # GIVEN
    message = build_message("/r toto")
        
    # WHEN
    response = bot.respond_to(message)
        
    # THEN
    assert_that(response).is_equal_to("Oops I don't know this command :-(")
    
    
def test_should_return_a_static_error_message_for_a_wrong_format_message():
    # GIVEN
    message = {'broken': 'message format'}
        
    # WHEN
    response = bot.respond_to(message)
        
    # THEN
    assert_that(response).is_equal_to("Oops I don't understand this message, maybe hipchat changed it's api ? :'(")
    