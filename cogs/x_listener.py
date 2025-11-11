import discord
from discord.ext import commands
import asyncio
from utils.twitter import TwitterPost
from discord.http import Route 

class XListener(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or message.guild is None:
            return

        found_tweets = [
            parsed_data for word in message.content.split() 
            if (parsed_data := TwitterPost.parse_url(word)) is not None
        ]

        if not found_tweets:
            return

        try:
            await asyncio.sleep(0.5)
            await message.edit(suppress=True)
        except (discord.Forbidden, discord.NotFound):
            pass

        for tweet_data in found_tweets:
            post = await TwitterPost.fetch(tweet_data['username'], tweet_data['tweet_id'])

            if not post or not post.video_urls:
                continue  

            content = f"**{post.author}** (@{post.username})"
            if post.replying_to:
                content += f"\nReplying to @{post.replying_to}"
            if post.text:
                content += f"\n{post.text}"

            if post.quote_author and post.quote_username and post.quote_text:
                quoted_lines = post.quote_text.split('\n')
                formatted_quote = "\n> ".join(quoted_lines)
                content += f"\n\n> **{post.quote_author}** (@{post.quote_username})\n> {formatted_quote}"

            container_components = [{"type": 10, "content": content}]

            media_items = [{"media": {"url": url}} for url in post.video_urls]
            container_components.append({"type": 12, "items": media_items})

            payload = {
                "components": [{
                    "type": 17,
                    "accent_color": 0x1DA1F2, 
                    "components": container_components
                }],
                "message_reference": {
                    "message_id": str(message.id)
                },
                "flags": 32768  
            }

            try:
                route = Route('POST', '/channels/{channel_id}/messages', channel_id=message.channel.id)
                await self.bot.http.request(route, json=payload)
            except Exception as e:
                print(f"Erro ao enviar embed do Twitter: {e}")

async def setup(bot: commands.Bot):
    await bot.add_cog(XListener(bot))