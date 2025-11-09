from discord.ext import commands
import re
from utils import parse

class GitHubListener(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
            
        match = re.search(
            r'https?://(?:www\.)?github\.com/[\w\-\.]+/[\w\-\.]+/blob/[\w\-\/\.]+#L\d+(?:-L\d+)?',
            message.content
        )
        if not match:
            return
        if match:
            await message.channel.send(f'bump:\n{match.group(0)}')


async def setup(bot):
    await bot.add_cog(GitHubListener(bot))
