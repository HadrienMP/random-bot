import hipchat_bot as bot


@bot.command("blame")
def blame(parameters):
    bot.get_members(room="12345678")
    return bot.response(message="Réponse", color="RED")


@bot.command("sensei")
def sensei(parameters):
    pass
