from discord.ext import commands
from discord import Member

class Users(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def pfp(self, ctx, user: Member=None):
        if user:
            try: await ctx.send(content=user.avatar_url)
            except Exception as e: await ctx.send(f"[-] Fail: {e}"); return
        elif user is None:
            try: await ctx.send(content=ctx.message.author.avatar_url)
            except Exception as e: await ctx.send(f"[-] Fail: {e}"); return
        print(f"[+] Success: Sent the profile image for {user if user else ctx.author}!")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: Member=None, *, reason: str=None or "bye bye"):
        if user is None or user == ctx.author: return

        try: await user.kick(reason=reason)
        except Exception as e: await ctx.send(f"[-] Fail: {e}"); return
        print(f"[+] Success: {user}({user.id}) has been kicked! ({reason})")
                    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, id: int):
        if id is None: return
    
        try: user = await self.bot.fetch_user(id); await ctx.guild.unban(user)
        except Exception as e: await ctx.send(f"[-] Fail: {e}"); return
        print(f"[+] Success: {user}({id}) has been unbanned!")
                   
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: Member=None, *, reason: str=None or "bye bye"):
        if user is None or user == ctx.author: return

        try: await user.ban(reason=reason)
        except Exception as e: await ctx.send(f"[-] Fail: {e}"); return
        print(f"[+] Success: {user}({user.id}) has been banned! ({reason})")
                    
def setup(bot):
    bot.add_cog(Users(bot))