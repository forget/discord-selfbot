import discord

class Config(object):
    def __init__(self) -> None:
        self.token = "" #your access token

        self.delete_after_execute = True #delete command after execution (i.e delete .pfp @user message after it's been executed)
        self.colour = discord.Color.blue() #random colour for embeds if you want to add to it
