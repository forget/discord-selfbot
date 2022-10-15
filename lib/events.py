from discord.ext import commands
from datetime import datetime
from threading import Thread

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(
            f"[?] User: {self.bot.user}\n"
            f"[?] ID: {self.bot.user.id}\n"
            f"[?] Last Login: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
        )

    @commands.Cog.listener()
    async def on_command(self, ctx):
        if not self.bot.Config.delete_after_execution:
            return False
        else:
            await ctx.message.delete()
            
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f"[-] Issue: {error}!")

def setup(bot):
    bot.add_cog(Events(bot))
