from .skychannel import CustomChannels


def setup(bot):
    bot.add_cog(CustomChannels(bot))
