# Simpomni Bot

**Simpomni Bot** (derived from "Simple" and "Omnipotent") is a versatile and easy-to-use Telegram bot built using Python and the `python-telegram-bot` library. The bot offers a variety of functionalities, from weather updates and random facts to reminders, a calculator, task management, and more.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Commands](#commands)
- [License](#license)

## Features

- **Weather Updates**: Get the current weather for any city.
- **Reminders**: Set reminders for specific times.
- **Random Facts**: Receive a random fun fact.
- **Calculator**: Perform basic calculations.
- **Task Management**: Add, list, and mark tasks as done.

## Prerequisites

- Python 3.7+
- python-telegram-bot module 
- A Telegram bot token from [BotFather](https://core.telegram.org/bots#botfather)
- API key for [OpenWeatherMap](https://openweathermap.org/) (for weather updates)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/simpomni_bot.git
   cd simpomni_bot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create .env file in your directory and add variables in the file with your own API keys.
   You can check the .env.example file for guidance on how to do this:
   - **Telegram Bot Token**: Add `TOKEN` with your bot's token from BotFather.
   - **OpenWeatherMap API Key**: Add `API_KEY` with your OpenWeatherMap API key.
   - **Bot Username**: Add `BOTUSERNAME` with your bot username. 
## Usage

1. **Run the bot**:
   ```bash
   python bot.py
   ```
2. **Interact with the bot** on Telegram by searching for your bot's username and sending commands.

## Commands

| Command       | Description                                                                                              | Example Usage              |
|---------------|----------------------------------------------------------------------------------------------------------|-----------------------------|
| `/start`      | Initiates the bot and sends a greeting message.                                                          | `/start`                    |
| `/help`       | Provides information about available commands or specific command details.                               | `/help`, `/help weather`    |
| `/weather`    | Retrieves current weather for a given city. Requires a city name.                                        | `/weather London`           |
| `/remind`     | Sets a reminder for a specified time. Format: `/remind message HH:MM`.                                   | `/remind "Meeting" 15:30`   |
| `/fact`       | Sends a random fun fact.                                                                                 | `/fact`                     |
| `/calculator` | Evaluates a mathematical expression (e.g., addition, subtraction, multiplication, division).             | `/calculator 2+3*4`         |
| `/tasks`      | Manages a to-do list. Add tasks, list all tasks, or mark tasks as done.                                  | `/tasks list`, `/tasks buy groceries` |
| `/done`       | Marks a specific task (by number) as completed.                                                          | `/done 1`                   |

## Example Interaction

```
User: /start
Bot: Hello there, thanks for chatting with me! What do you want me to do for you today?

User: /weather New York
Bot: The weather in New York is cloudy with a temperature of 22°C.

User: /remind "Doctor appointment" 14:30
Bot: Reminder has been set.

User: /tasks Buy groceries
Bot: You have added the task: Buy groceries
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
Hi, I'm Matthew, the creator of this bot. If you'd like to contact me you could send me an email at [Matthew](mailto:olagunjunifemi6@gmail.com)
