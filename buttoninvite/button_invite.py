import re

import discord
from redbot.core import Config, commands
from redbot.core.bot import Red

from . import url_button

old_invite = None


class ButtonInvite(commands.Cog):
    """
    A highly customizable invite cog with buttons without using any extra lib.
    """

    async def red_delete_data_for_user(self, **kwargs):
        """
        Nothing to delete.
        """
        return

    @commands.Cog.listener()
    async def on_connect(self):
        await self.bot.wait_until_red_ready()
        await self.config.thumbnail.set(f"{self.bot.user.avatar_url}")
        await self.config.icon_url.set(f"{self.bot.user.avatar_url}")

    def __init__(self, bot: Red):
        self.bot = bot
        default = {
            "description": "Thanks for choosing to invite {bot} to your server.",
            "invite_description": "Invite me!",
            "setpermissions": "",
            "commandscope": False,
            "footer": "{bot} Hosted by {owner}",
            "author": "{bot}",
            "link_text": "Add {bot} to your server.",
            "thumbnail": f"https://cdn.discordapp.com/attachments/954643340811456553/980231043409903666/output-onlinegiftools_11.gif?size=4096",
            "icon_url": f"https://cdn.discordapp.com/attachments/954643340811456553/980231043409903666/output-onlinegiftools_11.gif?size=4096",
        }
        self.config = Config.get_conf(self, 69, force_registration=True)
        self.config.register_global(**default)

    def cog_unload(self):
        if old_invite:
            try:
                self.bot.remove_command("invite")
            except Exception:
                pass
            self.bot.add_command(old_invite)

    @commands.is_owner()
    @commands.group()
    async def setinvite(self, ctx):
        """
        Settings for buttoninvite cog.
        """

    @commands.is_owner()
    @setinvite.command()
    async def description(self, ctx, *, text: str = ""):
        """
        Set the embed description.Leave blank for default description.

        Use `{bot}` in your message to display bot name. Enter `None` to
        disable the description.

        """
        if not text:
            await self.config.description.clear()
            return await ctx.send("Embed description set to default.")
        elif text == "None":
            await self.config.description.set("")
            return await ctx.send("Embed description disabled.")
        await self.config.description.set(text)
        await ctx.send(f"Embed description set to :\n`{text}`")

    @commands.is_owner()
    @setinvite.command()
    async def button(self, ctx, *, text: str = ""):
        """
        Set the button description.
        """
        if not text:
            await self.config.invite_description.clear()
            return await ctx.send("Button description set to default.")
        await self.config.invite_description.set(text)
        await ctx.send(f"Button description set to :\n`{text}`")

    @commands.is_owner()
    @setinvite.command()
    async def permissions(self, ctx, *, text: int = ""):
        """
        Set the default permissions value for your bot.

        Get the permissions value from
        https://discordapi.com/permissions.html. If left blank, resets
        permissions value to none. Enter `None` to disable the
        permissions value.

        """
        if text == "":
            await self.config.setpermissions.clear()
            return await ctx.send("Permissions value reset")
        elif text == "None":
            await self.config.setpermission.set("")
            return await ctx.send("Permissions value disabled")
        await self.config.setpermissions.set(text)
        await ctx.send("Permissions set")

    @commands.is_owner()
    @setinvite.command()
    async def scope(self, ctx, value: bool = None):
        """
        Add the `applications.commands` scope to your invite URL.

        This allows the usage of slash commands on the servers that
        invited your bot with that scope. Note that previous servers
        that invited the bot without the scope cannot have slash
        commands, they will have to invite the bot a second time.

        """
        if value:
            await self.config.commandscope.set(True)
            await ctx.send(
                "The `applications.commands` scope set to `True` and added to invite URL."
            )
        else:
            await self.config.commandscope.set(False)
            await ctx.send(
                "The `applications.commands` scope set to `False` and removed from invite URL."
            )

    @commands.is_owner()
    @setinvite.command()
    async def footer(self, ctx, *, text: str = ""):
        """
        Set the embed footer.

        Leave blank for default author. Use `{bot}` in your message to
        display bot name. Enter `None` to disable the description.

        """
        if not text:
            await self.config.footer.clear()
            return await ctx.send("Embed footer set to default.")
        elif text == "None":
            await self.config.footer.set("")
            return await ctx.send("Embed footer disabled.")
        await self.config.footer.set(text)
        await ctx.send(f"Embed footer set to :\n`{text}`")

    @commands.is_owner()
    @setinvite.command()
    async def author(self, ctx, *, text: str = ""):
        """
        Set the embed author.

        Leave blank for default author. Use `{bot}` in your message to
        display bot name. Enter `None` to disable the author.

        """
        if not text:
            await self.config.author.clear()
            return await ctx.send("Embed author set to default.")
        elif text == "None":
            await self.config.author.set("")
            return await ctx.send("Embed author disabled.")
        await self.config.author.set(text)
        await ctx.send(f"Embed author set to :\n`{text}`")

    @commands.is_owner()
    @setinvite.command()
    async def text(self, ctx, *, text: str = ""):
        """
        Set the embed link text.

        Leave blank for default link text. Use `{bot}` in your message
        to display bot name. Enter `None` to disable the link text.

        """
        if not text:
            await self.config.link_text.clear()
            return await ctx.send("Embed link text set to default.")
        elif text == "None":
            await self.config.link_text.set("")
            return await ctx.send("Embed link text disabled.")
        await self.config.link_text.set(text)
        await ctx.send(f"Embed link text set to :\n`{text}`")

    @commands.is_owner()
    @setinvite.command()
    async def thumbnail(self, ctx, *, link: str = ""):
        """
        Set the embed thumbnail url.

        Leave blank for default thumbnail.

        """
        if not link:
            await self.config.thumbnail.clear()
            return await ctx.send("Embed thumbnail set to default.")
        regex = r"^https?://(?:[a-z0-9\-]+\.)+[a-z]{2,6}(?:/[^/#?]+)+\.(?:jpg|gif|png)$"
        url = re.findall(regex, link)
        urls = [x[0] for x in url]
        if not urls:
            return await ctx.send("Couldn't find a valid url in your message")
        await self.config.thumbnail.set(link)
        await ctx.send(f"Embed thumbnail set to :\n`{link}`")

    @commands.is_owner()
    @setinvite.command()
    async def icon(self, ctx, *, link: str = ""):
        """
        Set the embed icon url.

        Leave blank for default icon.

        """
        if not link:
            await self.config.icon_url.clear()
            return await ctx.send("Embed icon set to default.")
        regex = r"^https?://(?:[a-z0-9\-]+\.)+[a-z]{2,6}(?:/[^/#?]+)+\.(?:jpg|gif|png)$"
        url = re.findall(regex, link)
        urls = [x[0] for x in url]
        if not urls:
            return await ctx.send("Couldn't find a valid url in your message")
        await self.config.icon_url.set(link)
        await ctx.send(f"Embed icon set to :\n`{link}`")

    @commands.command()
    async def invite(self, ctx):
        """
        Send personalized invite for the bot with a button!
        """
        bot_info = await self.bot.application_info()
        params = {"owner": f"{bot_info.owner}", "bot": f"{self.bot.user.name}"}
        embed = discord.Embed(
            description=(await self.config.description()).format(**params),
            colour=await ctx.embed_colour(),
        )
        embed.set_author(
            name=(await self.config.author()).format(**params),
            icon_url=(await self.config.icon_url()),
        )
        embed.set_thumbnail(url=(await self.config.thumbnail()))
        if await self.config.commandscope():
            embed.add_field(
                name="\N{Zero Width Space}",
                value=f"[{(await self.config.link_text()).format(**params)}](https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot+applications.commands&permissions={await self.config.setpermissions()})",
            )
            button = url_button.URLButton(
                f"{await self.config.invite_description()}",
                f"https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot+applications.commands&permissions={await self.config.setpermissions()}",
            )

        else:
            embed.add_field(
                name="\N{Zero Width Space}",
                value=f"[{(await self.config.link_text()).format(**params)}](https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions={await self.config.setpermissions()})",
            )
            button = url_button.URLButton(
                f"{await self.config.invite_description()}",
                f"https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions={await self.config.setpermissions()}",
            )
        embed.set_footer(text=(await self.config.footer()).format(**params))
        await url_button.send_message(self.bot, ctx.channel.id, embed=embed, url_button=button)


def setup(bot):
    if old_invite := bot.get_command("invite"):
        bot.remove_command(old_invite.name)
    bot.add_cog(ButtonInvite(bot))
