# 🐾 Pawsistant

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Discord](https://img.shields.io/discord/898088826134757426?label=Join%20Us%21&logo=discord)](https://discord.gg/6dzteBrQyg)

A modern Discord bot for welcoming users, managing roles, creating private voice channels, celebrating birthdays, and adding fun reactions!

## 🚀 Features

- **Slash Commands**: `/ping`, `/roll`, `/clear`, `/birthday`
- **Birthday System**: Users can set, view, or remove their birthday. The bot sends automatic greetings and assigns a birthday role.
- **Auto Voice Channel Creation**: Personalized voice channels for users
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

## 📂 Project Structure

```bash
bot.py
/commands/
    birthday.py
/events/
    member_events.py
    message_events.py
    reaction_events.py
    voice_events.py
/utils/
    role_utils.py
    tenor.py
Dockerfile
docker-compose.yml
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
