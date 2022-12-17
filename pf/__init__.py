from .pf import PF


def setup(bot):
    bot.add_cog(PF(bot))
