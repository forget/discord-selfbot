from discord.ext import commands
from discord import Member, Role

class Users(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def pfp(self, ctx, user: Member=None):
        if user:
            try: await ctx.send(content=user.avatar_url)
            except Exception as e: return print(f"[-] Fail: {e}")
        elif user is None:
            try: await ctx.send(content=ctx.message.author.avatar_url)
            except Exception as e: return print(f"[-] Fail: {e}")
        print(f"[+] Success: Sent the profile image for {user if user else ctx.author}!")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: Member=None, *, reason: str=None or "bye bye"):
        if user is None or user == ctx.author: return

        try: await user.kick(reason=reason)
        except Exception as e: return print(f"[-] Fail: {e}")
        print(f"[+] Success: {user}({user.id}) has been kicked! ({reason})")
                    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, id: int):
        if id is None: return
    
        try: user = await self.bot.fetch_user(id); await ctx.guild.unban(user)
        except Exception as e: return print(f"[-] Fail: {e}")
        print(f"[+] Success: {user}({id}) has been unbanned!")
                   
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: Member=None, *, reason: str=None or "bye bye"):
        if user is None or user == ctx.author: return

        try: await user.ban(reason=reason)
        except Exception as e: return print(f"[-] Fail: {e}")
        print(f"[+] Success: {user}({user.id}) has been banned! ({reason})")
        
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def role(self, ctx, user:Member, *, role:Role):
        if role.position > ctx.author.top_role.position: return print("[-] Fail: Specified role is above yours.")

        try: await user.remove_roles(role) if role in user.roles else await user.add_roles(role)
        except Exception as e: return print(f"[-] Fail: {e}")
        print(f"[+] Success: Edited role for {user}")
                    
def setup(bot):
    bot.add_cog(Users(bot))