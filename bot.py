import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
import anthropic
import logging
import time

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

def detect_script_type(response_text):
    # Implement your script type detection logic here
    # Return the detected script type as a string or None if no specific type is detected
    # Example:
    if response_text.startswith("```python"):
        return "python"
    elif response_text.startswith("```javascript"):
        return "javascript"
    elif response_text.startswith("```bash"):
        return "bash"
    else:
        return None

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

        max_retries = 3
        retry_delay = 1

        for attempt in range(max_retries):
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
                    page_size = 1900  # Reduced to leave room for code block markup
                    response_pages = [response_text[i:i+page_size] for i in range(0, len(response_text), page_size)]

                    # Detect the script type based on the file extension or content
                    script_type = detect_script_type(response_text)

                    # Send the response pages with the appropriate markup
                    for page in response_pages:
                        # Remove any problematic characters or formatting
                        page = page.replace("```", "")  # Remove triple backticks to avoid nested code blocks
                        page = page.replace("`", "'")  # Replace backticks with single quotes

                        if script_type:
                            message_content = f"```{script_type}\n{page}\n```"
                        else:
                            message_content = f"```\n{page}\n```"

                        if len(message_content) <= 2000:
                            await message.channel.send(message_content)
                        else:
                            # Split the message content into smaller chunks
                            chunks = [message_content[i:i+1900] for i in range(0, len(message_content), 1900)]
                            for chunk in chunks:
                                await message.channel.send(chunk)

                    # Append Claude's response to the conversation history
                    conversation_history[user_id].append(f"{anthropic.AI_PROMPT} {response_text}")
                    break  # Exit the retry loop if the request is successful
                else:
                    await message.channel.send("I didn't get a response from Claude.")
                    break  # Exit the retry loop if no response is received
            except anthropic.APIError as e:
                if e.status_code == 400:
                    await message.channel.send("Unable to process your request due to low credit balance on the Claude API.")
                    break  # Exit the retry loop if there's a credit balance issue
                elif e.status_code == 529:
                    logging.error(f"APIError: {e}")
                    if attempt < max_retries - 1:
                        # Retry with exponential backoff
                        time.sleep(retry_delay)
                        retry_delay *= 2
                    else:
                        await message.channel.send("Sorry, the Claude API is currently overloaded. Please try again later.")
                else:
                    await message.channel.send("Sorry, I encountered an error trying to process your request.")
                    logging.error(f"APIError: {e}")
                    break  # Exit the retry loop for other API errors
            except Exception as e:
                await message.channel.send("Sorry, I encountered an error trying to process your request.")
                logging.error(f"Unhandled exception: {e}")
                break  # Exit the retry loop for unhandled exceptions

# Start the bot
bot.run(BOT_TOKEN)
