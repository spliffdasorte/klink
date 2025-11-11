import re
from discord.ext import commands
from utils import parse


class GitHubListener(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.guild is None:
            await message.channel.send("no time for dms, tro.")
            return

        match = re.search(
            r"https?://(?:www\.)?github\.com/[\w\-\.]+/[\w\-\.]+/blob/[\w\-\/\.]+#L\d+(?:-L\d+)?",
            message.content,
        )
        if not match:
            return

        url = match.group(0)
        data = parse.parse_url(url)
        if not data:
            return

        lines = parse.get_file_content(data)
        if not lines:
            return

        snippet = "\n".join(lines)

        if len(snippet) > 1900:
            snippet = snippet[:1900] + "\n..."

        ext = data["file_path"].split(".")[-1] if "." in data["file_path"] else ""
        lang = ext if len(ext) <= 10 else ""

        await message.channel.send(f"```{lang}\n{snippet}\n```")


async def setup(bot):
    await bot.add_cog(GitHubListener(bot))
