from .simon import Simon

__red_end_user_data_statement__ = (
    "This cog does not persistently store data or metadata about users."
)


def setup(bot):
    bot.add_cog(Simon(bot))
