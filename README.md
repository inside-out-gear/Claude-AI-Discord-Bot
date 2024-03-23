Here's the formatted version of the README file for Discord:

# Discord Bot with Anthropic's Claude API

This repository contains a Python script for a Discord bot that integrates with Anthropic's Claude API. The bot listens for messages starting with the word "Claude" and sends the message content to the Claude API for processing. The bot then formats the response from Claude as pages using Discord markup and sends it back to the user.

# Discord Bot Features

- Integrates with the Anthropic Claude API to provide conversational responses
- Supports syntax highlighting for code blocks in responses using Discord Markdown
  - Automatically detects the script type based on the presence of specific code block markers (e.g., ```python, ```javascript, etc.)
  - Supports syntax highlighting for Python, JavaScript, HTML, CSS, and Bash
  - Uses generic code block markup (```) if no specific script type is detected
- Handles long responses by splitting them into multiple pages and sending them as separate messages
- Maintains conversation history for each user to provide context-aware responses
- Implements retry logic with exponential backoff to handle API errors and overload situations
- Provides informative error messages to users in case of API issues or low credit balance
- Logs errors and unhandled exceptions for debugging purposes
- Utilizes environment variables for secure storage of sensitive information (e.g., API keys)
- Supports easy customization and extension with modular code structure

## Prerequisites

Before setting up the bot, make sure you have the following:

- Python 3.7 or higher installed on your system
- A Discord bot token (obtained from the Discord Developer Portal)
- An Anthropic API key (obtained from the Anthropic website)

## Setup

1. Clone this repository to your local machine:

   ```
   git clone https://github.com/yourusername/discord-claude-bot.git
   ```

2. Navigate to the project directory:

   ```
   cd discord-claude-bot
   ```

3. Install the required dependencies using pip:

   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project directory and add your Discord bot token and Anthropic API key:

   ```
   DISCORD_BOT_TOKEN=your_discord_bot_token
   ANTHROPIC_API_KEY=your_anthropic_api_key
   ```

   Replace `your_discord_bot_token` with your actual Discord bot token and `your_anthropic_api_key` with your Anthropic API key.

5. Run the bot script:

   ```
   python bot.py
   ```

   The bot should now be online and ready to respond to messages in your Discord server.

## Usage

To interact with the bot, send a message in a channel where the bot is present, starting with the word "Claude" followed by your message or question. For example:

```
Claude What is the capital of France?
```

The bot will process your message, send it to the Claude API, and respond with the generated answer formatted as pages using Discord markup.

The bot also maintains a conversation history for each user, allowing it to remember and consider the historical questions and responses when generating new responses.

## Customization

You can customize the behavior of the bot by modifying the `bot.py` script. Some possible customizations include:

- Changing the command prefix (currently set to "Claude")
- Adjusting the maximum token limit for the Claude API (currently set to 1024)
- Modifying the formatting of the response pages
- Adding additional error handling or logging

## Contributing

If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request. Contributions are welcome!

## License

This project is open-source and available under the [MIT License](LICENSE).

---

This formatted version uses proper Markdown syntax, including headings, bullet points, code blocks, and horizontal rules. It should display nicely when viewed in a Discord channel or on a Git hosting platform like GitHub.
