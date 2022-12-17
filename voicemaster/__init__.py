from .voicemaster import VoiceMaster


def setup(bot):
    bot.add_cog(VoiceMaster(bot))