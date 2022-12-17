from .dose import Dose


def setup(bot):
    bot.add_cog(Dose(bot))
