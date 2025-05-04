# 🐾 Pawsistant

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Discord](https://img.shields.io/discord/898088826134757426?label=Join%20Us%21&logo=discord)](https://discord.gg/6dzteBrQyg)

A modern Discord bot for welcoming users, managing roles, creating private voice channels, celebrating birthdays, and adding fun reactions!

## 🚀 Features

- **Slash Commands**: `/ping`, `/roll`, `/clear`, `/birthday`
- **Birthday System**: Users can set, view, or remove their birthday. The bot sends automatic greetings and assigns a birthday role.
- **Auto Voice Channel Creation**: Personalized voice channels for users
- **Auto Role Assignment**: Automatically gives roles to new users using role IDs
- **Welcome Messages**: Custom welcome messages with GIFs
- **Reaction Roles**: Auto-assign roles based on emoji reactions
- **Tenor GIF Integration**: Fun GIFs triggered by keywords
- **Docker Support**: Easy deployment with `docker-compose`

---

## 🛠️ Installation

### Requirements

- Python 3.10 or higher
- Docker & Docker-Compose (optional)
- Discord Bot Token
- Tenor API Key (optional)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/pawbot.git
   cd pawbot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file:
   ```env
   DISCORD_BOT_TOKEN=your-token
   DISCORD_WELCOME_CHANNEL_IDS=1234567890/0987654321
   DISCORD_RULES_MESSAGE_ID=1234567890
   DISCORD_CREATE_CHANNEL_ID=1234567890
   DISCORD_BIRTHDAY_CHANNEL_ID=1234567890/9876543210
   TENOR_API_KEY=your-tenor-api-key
   DISCORD_AUTO_ROLE_IDS=111111111111111111/222222222222222222
   ```

4. Run the bot:
   ```bash
   python bot.py
   ```

Or with Docker:
   ```bash
   docker-compose up --build
   ```

---

## 📥 Auto Role Assignment (New Members)

When a new user joins the server, the bot can automatically assign one or more roles using role IDs.

### Setup

In your `.env` file, add:

```env
DISCORD_AUTO_ROLE_IDS=111111111111111111/222222222222222222
```

- Use `/` to separate multiple role IDs.

- Make sure your bot has the Manage Roles permission.

- The bot's highest role must be above the roles it's trying to assign.

---

## 📂 Project Structure

```bash
/assets/
    bot_icon.png
    bot_banner.png
/commands/
    __init__.py
    general.py
    birthday.py
/events/
    member_events.py
    message_events.py
    reaction_events.py
    voice_events.py
/utils/
    role_utils.py
    tenor.py
bot.py    
.gitignore
Dockerfile
docker-compose.yml
requirements.txt
.env.example
README.md
LICENSE
```

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).  
© 2025 Eileen Jenke

---

## 🤝 Contributing

Pull requests are welcome!  
Please follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) guidelines when submitting commits.

---

## ❤️ Thanks

Special thanks to all Open Source tools and the Discord Developer Community!

---
