import aiohttp
import re
from typing import Optional, List, Dict, Any

class TwitterPost:
    def __init__(self, data: Dict[str, Any]):
        tweet_data = data.get('tweet', {})
        author_data = tweet_data.get('author', {})
        media_data = tweet_data.get('media', {})

        self.author: str = author_data.get('name', '??')
        self.username: str = author_data.get('screen_name', '??')
        self.text: str = tweet_data.get('text', '')
        self.replying_to: Optional[str] = tweet_data.get('replying_to')

        photos = media_data.get('photos', [])
        videos = media_data.get('videos', [])

        self.photo_urls: List[str] = [item['url'] for item in photos if 'url' in item]
        self.video_urls: List[str] = [item['url'] for item in videos if 'url' in item]

        self.quote_author: Optional[str] = None
        self.quote_username: Optional[str] = None
        self.quote_text: Optional[str] = None
        
        quote_data = tweet_data.get('quote')
        if quote_data:
            quote_author_data = quote_data.get('author', {})
            self.quote_author = quote_author_data.get('name')
            self.quote_username = quote_author_data.get('screen_name')
            self.quote_text = quote_data.get('text')

            quote_media = quote_data.get('media', {})
            quote_photos = quote_media.get('photos', [])
            quote_videos = quote_media.get('videos', [])

            self.photo_urls += [item['url'] for item in quote_photos if 'url' in item]
            self.video_urls += [item['url'] for item in quote_videos if 'url' in item]

    @staticmethod
    def parse_url(url: str) -> Optional[Dict[str, str]]:
        pattern = r'(?i)https?://(?:www\.)?(?:twitter|x)\.com/(\w+)/status/(\d+)'
        match = re.search(pattern, url)
        if match:
            return {'username': match.group(1), 'tweet_id': match.group(2)}
        return None

    @staticmethod
    async def fetch(username: str, tweet_id: str) -> Optional['TwitterPost']:
        api_url = f"https://api.fxtwitter.com/{username}/status/{tweet_id}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(api_url) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('code') == 200 and 'tweet' in data:
                            return TwitterPost(data)
            except aiohttp.ClientError:
                pass  
        return None