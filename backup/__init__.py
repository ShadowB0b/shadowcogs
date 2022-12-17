
from redbot.core.bot import Red

from .backup import Backup


async def setup(bot: Red) -> None:
    bot.add_cog(Backup(bot))
