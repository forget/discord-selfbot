from discord.ext import commands

class Messages(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name='clear', pass_context=True)
    async def clear(self, ctx, username=None):
        channel = None
        if not username:
            channel = ctx.channel
        else:
            for private_channel in self.bot.private_channels:
                if str(username) in str(private_channel):
                    channel = private_channel

        if not channel: print("[-] Fail: Channel has not been found!"); return
        
        async for message in channel.history(limit=None).filter(lambda m: m.author == self.bot.user).map(lambda m: m):
            try: await message.delete()
            except: pass
        print(f"[+] Success: Deleted messages in {channel}!")
            
    @commands.command(name='attachments', pass_context=True)
    async def attachments(self, ctx, username=None):        
        channel = None
        if not username:
            channel = ctx.channel
        else:
            for private_channel in self.bot.private_channels:
                if str(username) in str(private_channel):
                    channel = private_channel
        if not channel: print("[-] Fail: Channel has not been found!"); return
        
        async for message in channel.history(limit=None).filter(lambda m: m.author == self.bot.user).map(lambda m: m):
            try: await message.delete() if message.attachments else False
            except: pass
        print(f"[+] Success: Deleted attachments in {channel}!")

    @commands.command(name='clearfriends')
    async def clearfriends(self, ctx):       
        for friend in self.bot.user.friends:        
            async for message in friend.history(limit=None).filter(lambda m: m.author == self.bot.user).map(lambda m: m):
                try: await message.delete()
                except: pass
        print("[+] Success: Cleared all friends!")
                
def setup(bot):
    bot.add_cog(Messages(bot))