Discord Bot with Anthropic's Claude API
This repository contains a Python script for a Discord bot that integrates with Anthropic's Claude API. The bot listens for messages starting with the word "Claude" and sends the message content to the Claude API for processing. The bot then formats the response from Claude as pages using Discord markup and sends it back to the user.
Prerequisites
Before setting up the bot, make sure you have the following:
•	Python 3.7 or higher installed on your system
•	A Discord bot token (obtained from the Discord Developer Portal)
•	An Anthropic API key (obtained from the Anthropic website)
Setup
1.	Clone this repository to your local machine:
Copy code
git clone https://github.com/yourusername/discord-claude-bot.git
2.	Navigate to the project directory:
Copy code
cd discord-claude-bot
3.	Install the required dependencies using pip:
Copy code
pip install -r requirements.txt
4.	Create a .env file in the project directory and add your Discord bot token and Anthropic API key:
Copy code
DISCORD_BOT_TOKEN=your_discord_bot_token
ANTHROPIC_API_KEY=your_anthropic_api_key
Replace your_discord_bot_token with your actual Discord bot token and your_anthropic_api_key with your Anthropic API key.
5.	Run the bot script:
Copy code
python bot.py
The bot should now be online and ready to respond to messages in your Discord server.
Usage
To interact with the bot, send a message in a channel where the bot is present, starting with the word "Claude" followed by your message or question. For example:
Copy code
Claude What is the capital of France?
The bot will process your message, send it to the Claude API, and respond with the generated answer formatted as pages using Discord markup.
The bot also maintains a conversation history for each user, allowing it to remember and consider the historical questions
Claude does not have the ability to run the code it generates yet.

