import re
from urllib.parse import urlparse
import requests
import aiohttp


def parse_url(url):
    parsed = urlparse(url)
    parts = parsed.path.strip('/').split('/')
    if len(parts) < 5:
        return None
    
    user, repo, blob, branch = parts[:4]
    file_path = '/'.join(parts[4:])
    
    line_match = re.search(r"#L(\d+)(?:-L(\d+))?", url)
    if not line_match:
        return None
        
    start_line = int(line_match.group(1))
    end_line = int(line_match.group(2)) if line_match.group(2) else start_line
    
    return {
        "user": user,
        "repo": repo,
        "branch": branch,
        "file_path": file_path,
        "start_line": start_line,
        "end_line": end_line
    }


def get_file_content(data):
    raw_url = f"https://raw.githubusercontent.com/{data['user']}/{data['repo']}/{data['branch']}/{data['file_path']}"
    response = requests.get(raw_url)
    
    if response.status_code != 200:
        return None
    
    lines = response.text.splitlines()
    return lines[data['start_line'] - 1 : data['end_line']]


def parseX_url(url):
    parsed = urlparse(url)
    parts = parsed.path.strip('/').split('/')
    
    if len(parts) < 3 or parts[1] != 'status':
        return None
    
    username = parts[0]
    tweet_id = parts[2]
    
    return {
        'username': username,
        'tweet_id': tweet_id
    }


async def fetch_x_data(tweet_id: str):
    url = f"https://cdn.syndication.twimg.com/tweet-result?id={tweet_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return None

            data = await resp.json()

            video_url = None
            for m in data.get("mediaDetails", []):
                if m.get("type") == "video":
                    video_url = m.get("media_url_https")
                    break

            return {
                "text": data.get("text", ""),
                "video_url": video_url,
                "mediaDetails": data.get("mediaDetails", []),
                "user": {
                    "name": data.get("user", {}).get("name", ""),
                    "screen_name": data.get("user", {}).get("screen_name", "")
                }
            }
