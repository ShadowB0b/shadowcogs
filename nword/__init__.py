from .nword import Nword


def setup(bot):
    bot.add_cog(Nword(bot))
