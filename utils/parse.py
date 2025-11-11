import re
from urllib.parse import urlparse
import requests


def parse_url(url: str):
    """
    extracts information from a github url that references specific lines of code.

    returns a dictionary containing:
    - user: username or organization name
    - repo: repository name
    - branch: branch name
    - file_path: path to the file
    - start_line: starting line number
    - end_line: ending line number (same as start_line if only one line is specified)
    """
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
        "end_line": end_line,
    }


def get_file_content(data: dict):
    """
    downloads the raw content of a github file and returns
    only the lines specified (from start_line to end_line).
    """
    raw_url = (
        f"https://raw.githubusercontent.com/"
        f"{data['user']}/{data['repo']}/{data['branch']}/{data['file_path']}"
    )

    response = requests.get(raw_url)
    if response.status_code != 200:
        return None

    lines = response.text.splitlines()
    return lines[data['start_line'] - 1 : data['end_line']]