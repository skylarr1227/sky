from .skysave import skynote


def setup(bot):
    cog = skybot(bot)
    bot.add_cog(cog)