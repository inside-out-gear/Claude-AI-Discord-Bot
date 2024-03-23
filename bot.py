import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
import anthropic
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)

# Load .env file to get environment variables
load_dotenv()

# Environment variables
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

# Setting up intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# Initialize the bot
bot = commands.Bot(command_prefix="!", intents=intents)

# Initialize the Anthropic client
client = anthropic.Client(api_key=ANTHROPIC_API_KEY)

# Store conversation history
conversation_history = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    # Prevent the bot from responding to its own messages
    if message.author == bot.user:
        return

    if message.content.startswith('Claude'):
        user_message = message.content[len('Claude'):].strip()
        user_id = message.author.id

        # Initialize conversation history for the user if it doesn't exist
        if user_id not in conversation_history:
            conversation_history[user_id] = []

        try:
            # Append user's message to the conversation history
            conversation_history[user_id].append(f"{anthropic.HUMAN_PROMPT} {user_message}")

            # Construct the prompt with conversation history
            prompt = "\n".join(conversation_history[user_id]) + anthropic.AI_PROMPT

            # Sending a request to the Claude API
            response = client.completions.create(
                prompt=prompt,
                stop_sequences=[anthropic.HUMAN_PROMPT],
                max_tokens_to_sample=1024,
                model="claude-v1",
            )

            # Process and send Claude's response
            if response.completion:
                response_text = response.completion.strip()

                # Split the response into pages
                page_size = 2000  # Discord's maximum message length
                response_pages = [response_text[i:i+page_size] for i in range(0, len(response_text), page_size)]

                # Send the response pages
                for page in response_pages:
                    await message.channel.send(f"```\n{page}\n```")

                # Append Claude's response to the conversation history
                conversation_history[user_id].append(f"{anthropic.AI_PROMPT} {response_text}")
            else:
                await message.channel.send("I didn't get a response from Claude.")

        except anthropic.APIError as e:
            if e.status_code == 400:
                await message.channel.send("Unable to process your request due to low credit balance on the Claude API.")
            else:
                await message.channel.send("Sorry, I encountered an error trying to process your request.")
            logging.error(f"APIError: {e}")

        except Exception as e:
            await message.channel.send("Sorry, I encountered an error trying to process your request.")
            logging.error(f"Unhandled exception: {e}")

# Start the bot
bot.run(BOT_TOKEN)
