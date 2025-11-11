# 📦 Klink — Discord Utility Bot

![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg?logo=python&logoColor=white)
![Discord.py](https://img.shields.io/badge/discord.py-2.3%2B-5865F2.svg?logo=discord&logoColor=white)
![License](https://img.shields.io/badge/license-GNU%20GPLv3-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
![Maintained](https://img.shields.io/badge/maintained-yes-brightgreen.svg)

A lightweight Discord bot written in **Python** that automatically detects and enhances links from  
**GitHub** and **Twitter/X** — fetching code snippets and re-embedding tweets with style and precision.

---

## ✨ Features

- **GitHub Line Snippets** → Detects GitHub links with line references (e.g. `#L15` or `#L10-L20`) and returns syntax-highlighted snippets.  
- **Twitter/X Post Enhancer** → Replaces default Discord embeds with custom blue embeds featuring author info, tweet text, replies, quotes, and media (videos prioritized).  
- **Modular Design** → Organized into self-contained cogs for easy extension and maintenance.  
- **Rate Limiting & Error Handling** → Prevents spam and gracefully handles API failures.  
- **Multi-Line & Media Support** → Handles code ranges, images, videos, and quoted/replied tweets seamlessly.

---

## 🧩 Project Structure

```

klink/
├── main.py              # Bot startup, intents setup, and cog loading
├── config.py            # Discord bot token and configuration
├── requirements.txt     # Python dependencies (discord.py, aiohttp, etc.)
├── cogs/
│   ├── git_listener.py  # GitHub code snippet listener
│   └── x_listener.py    # Twitter/X post embed listener
└── utils/
├── parse.py         # GitHub URL parser and raw content fetcher
└── twitter.py       # Twitter/X API client and post parser

````

---

## 🚀 Setup

### 1. Clone the repository
```bash
git clone https://github.com/spliffdasorte/klink.git
cd klink
````

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your Discord bot token

Edit the file `config.py`:

```python
DISCORD_TOKEN = "YOUR_DISCORD_TOKEN_HERE"
```

### 4. Invite the bot to your server

* Create a bot at the [Discord Developer Portal](https://discord.com/developers/applications)
* Enable **Message Content Intent**
* Use the OAuth2 URL generator with these permissions:

  * ✅ Send Messages
  * ✅ Read Message History
  * ✅ Embed Links
  * ✅ Manage Messages *(for embed suppression)*

### 5. Run the bot

```bash
python main.py
```

The bot will log in and automatically load all cogs.

---

## 💡 Examples

### 🔹 GitHub Code Snippets

When a user sends a GitHub link like:

```
https://github.com/user/repo/blob/main/example.py#L10
```

The bot replies with:

> ```py
> print("Hello, world!")
> ```

For multiple lines:

```
https://github.com/user/repo/blob/main/app/main.py#L5-L8
```

Response:

> ```py
> def greet():
>     print("Hi!")
>     return True
> ```

---

### 🔹 Twitter/X Post Embedding

When a user sends:

```
https://x.com/verycoolguy/status/1234567890
```

The bot:

* Suppresses the default Discord embed
* Sends a **custom blue embed** containing:

  * 🧑 Author & handle
  * 📝 Tweet text
  * 🔁 Replies and quotes (if present)
  * 🎥 Embedded media (videos prioritized)

Example output:

> **Very Cool Guy** (@verycoolguy)
> Just started a live!
>
> 🎥 *Embedded video from the tweet*

---

## ⚠️ Limitations

* Depends on **third-party APIs** (e.g. `fxtwitter.com` for tweet data).
* Only works with **public GitHub repositories** (no private repo access).
* Twitter/X endpoints may occasionally change, requiring small updates.
