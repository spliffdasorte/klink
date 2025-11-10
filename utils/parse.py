import re
from urllib.parse import urlparse
import requests
# import aiohttp
# import json


def parse_url(url):
    parsed = urlparse(url)
    parts = parsed.path.strip('/').split('/')
    if len(parts) < 5: return None
    user, repo, blob, branch = parts[:4]
    file_path = '/'.join(parts[4:])
    line_match = re.search(r"#L(\d+)(?:-L(\d+))?", url)
    if not line_match: return None
    start_line = int(line_match.group(1))
    end_line = int(line_match.group(2)) if line_match.group(2) else start_line
    return {"user": user, "repo": repo, "branch": branch, "file_path": file_path, "start_line": start_line, "end_line": end_line}

def get_file_content(data):
    raw_url = f"https://raw.githubusercontent.com/{data['user']}/{data['repo']}/{data['branch']}/{data['file_path']}"
    response = requests.get(raw_url)
    if response.status_code != 200: return None
    lines = response.text.splitlines()
    return lines[data['start_line'] - 1 : data['end_line']]

# def parseX_url(url):
#     parsed = urlparse(url)
#     parts = parsed.path.strip('/').split('/')
#     if len(parts) < 3 or parts[1] != 'status': return None
#     username = parts[0]
#     tweet_id = parts[2]
#     return {'username': username, 'tweet_id': tweet_id}


# async def fetch_x_data(username: str, tweet_id: str):
#     url = f"https://api.fxtwitter.com/{username}/status/{tweet_id}"
#     print(f"=> [API] Chamando a URL: {url}")
    
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as resp:
#             print(f"=> [API] Status da resposta: {resp.status}")
#             if resp.status != 200:
#                 return None

#             try:
#                 data = await resp.json()
#                 print("=> [API] Resposta JSON recebida:")
#                 print(json.dumps(data, indent=2))
#             except Exception as e:
#                 print(f"=> [API] ERRO ao decodificar JSON: {e}")
#                 return None

#             if not data or "tweet" not in data:
#                 print("=> [API] JSON inválido ou sem a chave 'tweet'.")
#                 return None
            
#             tweet = data["tweet"]
#             video_url = None
            
#             if "media" in tweet and "videos" in tweet["media"]:
#                 if tweet["media"]["videos"]:
#                     video_url = tweet["media"]["videos"][0].get("url")
#                     print(f"=> [API] URL do vídeo encontrada: {video_url}")
#                 else:
#                     print("=> [API] Chave 'videos' está vazia.")
#             else:
#                 print("=> [API] Não foram encontradas as chaves 'media' ou 'videos' no tweet.")

#             result = {
#                 "text": tweet.get("text", ""),
#                 "video_url": video_url,
#                 "user": {
#                     "name": tweet["author"].get("name", ""),
#                     "screen_name": tweet["author"].get("screen_name", "")
#                 }
#             }
#             print("=> [API] Retornando dados processados.")
#             return result