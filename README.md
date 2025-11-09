# GitHub Line Bot

A simple Discord bot written in Python that automatically fetches and formats a specific line from a GitHub file when a user sends a link containing a file and line reference (e.g., `#L15`).

## 📜 Features
- Detects GitHub links in messages  
- Parses repository, branch, file, and line number  
- Fetches and displays the specified line of code  
- Clean modular structure for easy extension  

## 🧩 Project Structure
```

klink/
├── main.py               # bot startup and extension loading
├── config.py             # stores the discord bot token
├── requirements.txt      # python dependencies
└── utils/
├── parser.py         # parses github urls
└── fetcher.py        # fetches code content from github

````

## 🚀 Setup
1. Clone this repository:
   ```bash
   git https://github.com/spliffdasorte/klink.git
   cd klink
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Add your bot token in `config.py`:

   ```python
   token = "YOUR_DISCORD_TOKEN_HERE"
   ```

4. Run the bot:

   ```bash
   python main.py
   ```

## 💡 Example

When a user sends:

```
https://github.com/user/repo/blob/main/example.py#L10
```

The bot replies with:

```
🧾 example.py — line 10:
print("Hello, world!")
```