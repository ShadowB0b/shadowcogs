"""Module to access eBird API."""
from datetime import datetime
import logging
from urllib.error import URLError
from redbot.core import commands, checks, Config
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
from ebird.api import get_observations
import discord
from .api import EBirdAPI

LOG = logging.getLogger("red.dronefly.ebirdcog")


# TODO: switch to dataclasses-json as per inatcog
class ObsRecord(dict):
    """A human-readable observation record."""

    def __init__(
        self, date_format="%d %b, %Y", datetime_format="%H:%M, %d %b, %Y", **kwargs
    ):
        self.date_format = date_format
        self.datetime_format = datetime_format
        super().__init__(**kwargs)

    def __getitem__(self, key):
        """Reformat datetime into human-readable format."""
        try:
            val = super().__getitem__(key)
        except KeyError:
            val = None
        if key == "obsDt":
            try:
                parsed_time = datetime.strptime(val, "%Y-%m-%d %H:%M")
                return parsed_time.strftime(self.datetime_format)
            except ValueError:
                parsed_time = datetime.strptime(val, "%Y-%m-%d")
                return parsed_time.strftime(self.date_format)
        if key == "howMany" and val is None:
            return "uncounted"
        return val


class EBirdCog(commands.Cog, name="eBird"):
    """An eBird commands cog."""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=8008)
        self.config.register_global(
            region="CA-NS", days=30, date_format="%d %b", datetime_format="%H:%M, %d %b"
        )
        self.api = EBirdAPI(self)

    @commands.group()
    async def ebird(self, ctx):
        """Access the eBird platform."""
        pass  # pylint: disable=unnecessary-pass

    @ebird.command()
    @checks.is_owner()
    async def checkdays(self, ctx):
        """Checks days setting."""
        days = await self.config.days()
        await ctx.send("eBird days is {}.".format(days))

    @ebird.command()
    @checks.is_owner()
    async def checkregion(self, ctx):
        """Checks region setting."""
        region_code = await self.config.region()
        region = {}
        try:
            region = await self.api.get_region(ctx.channel, region_code)
        except ValueError as err:
            msg = (
                "eBird region not valid: {code}; error: {err}.\n"
                "Please set to a valid code with:\n"
                "    [p]ebird setregion code"
            ).format(code=region_code, err=err)
            await ctx.send(msg)
            return

        await ctx.send(
            "eBird region is {region} ({code}).".format(
                region=region["result"], code=region_code
            )
        )

    @ebird.command()
    async def hybrids(self, ctx, region_code=None, days=None):
        """Reports recent hybrid observations."""
        days_back = int(days) if days else await self.config.days()
        if days_back not in range(1, 31):
            await ctx.send(
                "Value for days, %s, must be a number from 1 through 30." % days_back
            )
            return

        if region_code:
            try:
                region = await self.api.get_region(ctx.channel, region_code)
            except ValueError as err:
                await ctx.send(str(err) % region_code)
                return

            if not region:
                await ctx.send("Region not found: {}".format(region_code))
                return
        else:
            region_code = await self.config.region()

        try:
            records = (
                await self.get_hybrid_observations(ctx, region_code, days_back) or []
            )
        except URLError as err:
            LOG.error("eBird request failed: %s", err)
            await ctx.send("eBird could not be contacted. Please try again later.")
            return
        if not records:
            await ctx.send("No hybrids observed in the past %d days." % days_back)
            return

        date_fmt = await self.config.date_format()
        datetime_fmt = await self.config.datetime_format()
        embeds = []
        title = f"Hybrids in {region_code} from past {days_back} days"
        color = 0x90EE90
        embed = discord.Embed(color=color)

        for record in records:
            if len(embed.fields) == 5:
                embeds.append(embed)
                embed = discord.Embed(color=color)
            rec = ObsRecord(date_fmt, datetime_fmt, **record)
            name = rec["comName"].replace(" (hybrid)", "")
            embed.add_field(
                name=name,
                value=("· {obsDt}: {howMany} at {locName}").format_map(rec),
                inline=False,
            )

        if embeds:
            embeds.append(embed)
            pages = len(embeds)
            for page, embed in enumerate(embeds, start=1):
                embed.title = "%s (Page %d of %d)" % (title, page, pages)
            await menu(ctx, embeds, DEFAULT_CONTROLS)
        else:
            embed.title = title
            await ctx.send(embed=embed)

    @ebird.command()
    @checks.is_owner()
    async def setregion(self, ctx, region_code: str):
        """Sets region."""
        region = None

        if region_code.lower() == "world":
            await ctx.send("eBird region cannot be world")
            return

        try:
            region = await self.api.get_region(ctx.channel, region_code)
        except ValueError as err:
            await ctx.send(str(err) % region_code)
            return

        if not region:
            await ctx.send("eBird region not found: {}".format(region_code))
            return

        await self.config.region.set(region_code)
        await ctx.send("eBird region has been changed.")

    @ebird.command()
    @checks.is_owner()
    async def setdays(self, ctx, value: int):
        """Sets days considered recent (1 through 30; default: 30)."""
        days = int(value)
        if days in range(1, 31):
            await self.config.days.set(days)
            await ctx.send("eBird days has been changed.")
        else:
            await ctx.send("eBird days must be a number from 1 through 30.")

    async def get_hybrid_observations(self, ctx, region_code, days):
        """Gets recent hybrid observations."""
        ebird_key = await self.api.get_api_key(ctx.channel)
        if ebird_key is None:
            return False

        try:
            # Docs at: https://github.com/ProjectBabbler/ebird-api
            observations = get_observations(
                ebird_key["api_key"],
                region_code,
                back=days,
                category="hybrid",
                detail="simple",
                provisional=True,
            )
        except ConnectionResetError:
            raise LookupError("Could not contact eBird")
        return observations
