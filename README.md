# 📦 Klink — GitHub Line Bot

A simple Discord bot written in Python that automatically fetches and formats specific lines from GitHub files when users send links containing line references (e.g., `#L15` or `#L10-L20`).

## ✨ Features
- Detects GitHub links in Discord messages  
- Parses repository, branch, file path, and line range  
- Fetches and formats the referenced code snippet  
- Lightweight and modular structure  
- Supports multi-line snippets  

## 🧩 Project Structure
```

klink/
├── main.py               # Bot startup and cog loading
├── config.py             # Stores the discord bot token
├── requirements.txt      # Python dependencies
├── cogs/
│   └── listener.py       # Main listener that reacts to GitHub links
└── utils/
└── parse.py          # URL parser and GitHub raw content fetcher

````

## 🚀 Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/spliffdasorte/klink.git
   cd klink
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Add your bot token**
   Edit `config.py`:

   ```python
   token = "YOUR_DISCORD_TOKEN_HERE"
   ```

4. **Run the bot**

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
```py
print("Hello, world!")
```

Or for multiple lines:

```
https://github.com/user/repo/blob/main/app/main.py#L5-L8
```

The bot replies with:

````
```py
def greet():
    print("Hi!")
    return True
````

<div align="center">
  <img width="746" height="429" alt="image" src="https://i.imgur.com/F7A4Wx4.png" />
</div>