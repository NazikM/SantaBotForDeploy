# SantaBot - Secret Santa Telegram Bot

## Installation

### Requirements
Ensure you have Python installed on your machine. You can download it from [Python's official website](https://www.python.org/downloads/).

### Steps
1. Clone the repository to your local machine.
   ```bash
   git clone https://github.com/your-username/santa-bot.git
   cd santa-bot
   ```

2. Install the required Python packages from the `requirements.txt` file.
   ```bash
   pip install -r requirements.txt
   ```

## How to Use

### 1. Configuration
1. Create a `.env` file in the project directory.
2. Add your Telegram bot token to the `.env` file:
   ```env
   token=YOUR_TELEGRAM_BOT_TOKEN
   ```

### 2. Run the Bot
Run the bot using the following command:
```bash
python Main.py
```

### 3. Interacting with the Bot
1. Start the bot by sending the `/start` command.
2. Choose from the available options:
   - **Create Group:** Initiate the creation of a new Secret Santa group.
   - **Join Group:** Join an existing Secret Santa group.
   - **Add Wish List:** Share your wish list with other participants.
   - **Distribute Gifts:** If you are the organizer, use this option to distribute gifts among participants.

### Commands
- **/start:** Begin interacting with the bot and access the main menu.
- **Creating a Group:** Use the 'Create Group➕' option to start the group creation process.
- **Joining a Group:** Select 'Join Group🙋🏼' to join an existing group by providing your name and the group name.
- **Adding a Wish List:** Use 'Add Your Wish List💌' to share the gifts you'd like to receive with other participants.
- **Distributing Gifts:** If you're the organizer, choose 'Distribute Gifts🎁' to automatically assign gift recipients.

### Contributors
- [Your Name]
- [Other contributors]

Feel free to contribute to the project by submitting pull requests or reporting issues.

Happy gifting! 🎅🏼🎄