from .voices import Voices


def setup(bot):
    bot.add_cog(Voices(bot))
