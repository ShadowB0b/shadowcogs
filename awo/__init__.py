from .awo import Awo

__red_end_user_data_statement__ = "This cog does not store any end user data."


def setup(bot):
    bot.add_cog(Awo(bot))
