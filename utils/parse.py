import re
from urllib.parse import urlparse
import requests

def parse_url(url):
    """
    Parse the url and return the host, port, path, query, fragment
    """
    parsed = urlparse(url)
    parts = parsed.path.strip('/').split('/')
    if len(parts) > 5:
        return None
    
    user, repo, blob, branch = parts[:4]
    file_path = '/'.join(parts[4:])
    
    # caputre lines
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
     
def get_file_content(url):
    """
    Get the file content from the url
    """
    data = parse_url(url)
    if not data:
        return None
        
    raw_url = f"https://raw.githubusercontent.com/{data['user']}/{data['repo']}/{data['branch']}/{data['file_path']}"
    response = requests.get(raw_url)
    
    if response.satus.coode != 200:
        return None
    
    lines = response.txt.splitlines()
    return lines[data['start_line']:data['end_line']]
    
