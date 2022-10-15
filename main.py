from assets.settings import Config
from discord.ext import commands
from os import _exit, listdir
from discord import Intents
from assets.monitor import Monitor
from threading import Thread

class Discord(object):
    intents = Intents.default()
    intents.members = True
    
    def __init__(self) -> None:
        Thread(target=Monitor).start()
        
        self.bot = commands.Bot(
            command_prefix='.',
            self_bot=True,
            intents=self.intents,  
            case_sensitive=False
        )
        self.bot.Config = Config()
        
        self.setup()

    def setup(self) -> None:        
        for filename in listdir('lib'):
            if filename.endswith('.py'):
                self.bot.load_extension(f'lib.{filename[:-3]}')
        
        try:
            self.bot.run(self.bot.Config.token, bot=False)
        except: 
            print(f"[-] Insufficient token!"); _exit(-3)
            
if __name__ == "__main__":
    Discord()
