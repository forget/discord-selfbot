from settings import Config
from discord.ext import commands
from os import _exit, listdir

class Discord(object):
    def __init__(self) -> None:
        self.bot = commands.Bot(
            command_prefix='.',
            self_bot=True,
            case_sensitive=False
        )
        self.bot.Config = Config()
        
        self.setup()

    def setup(self) -> None:
        for filename in listdir('commands'):
            if filename.endswith('.py'):
                self.bot.load_extension(f'commands.{filename[:-3]}')
                
        try: self.bot.run(self.bot.Config.token, bot=False)
        except: print(f"[-] Insufficient token!"); _exit(-3)
        
if __name__ == "__main__":
    Discord()   