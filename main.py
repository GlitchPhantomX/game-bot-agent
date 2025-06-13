import os  
import chainlit as cl  
from dotenv import load_dotenv  
from typing import Optional, Dict  
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
import requests
from tools import play_guess_the_number, play_rock_paper_scissors, play_quiz_game

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash", 
    openai_client=provider
    )

agent = Agent(
    name="Game Bot Agent",
    instructions="""
You are a fun interactive Game Bot with score tracking!

🎮 Available Games:
1. Guess the Number (1 to 10)
2. Rock, Paper, Scissors
3. Quiz Game (3 questions)
4. Word Puzzle Game

📊 Scores:
- Track wins/losses in Rock Paper Scissors
- Track correct answers in Quiz Game

🧠 How to Respond:
- Start with the menu when users arrive
- Use the appropriate tool for each game
- Update scores after each round
- For unrelated queries: "I'm a game bot! Try 'menu' to see games 😄"

Keep responses fun and motivational!
""",
    model=model,
    tools=[play_guess_the_number, play_rock_paper_scissors, play_quiz_game],
)

@cl.oauth_callback
def oauth_callback(
    provider_id: str, 
    token: str, 
    raw_user_data: Dict[str, str],  
    default_user: cl.User,  
) -> Optional[cl.User]: 

    print(f"Provider: {provider_id}")  
    print(f"User data: {raw_user_data}")  

    return default_user  

@cl.on_chat_start
async def handle_chat_start():
    cl.user_session.set("history", [])  

    welcome_message = """🎮✨ Welcome to Game Bot! ✨🎮

I'm your fun gaming companion with 4 exciting games to play:

1️⃣ Guess the Number (1-10)
2️⃣ Rock, Paper, Scissors 🤜✋✌️
3️⃣ Quiz Game (3 questions) 🧠
4️⃣ Word Puzzle Game (coming soon!) 

Type 'menu' anytime to see these options!
Current scores will be tracked as you play 🏆

Which game would you like to play first?"""

    await cl.Message(content=welcome_message).send()

@cl.on_message
async def handle_message(message: cl.Message):

    history = cl.user_session.get("history")  

    history.append(
        {"role": "user", "content": message.content}
    ) 

    result = await cl.make_async(Runner.run_sync)(agent, input=history)

    response_text = result.final_output
    await cl.Message(content=response_text).send()

    history.append({"role": "assistant", "content": response_text})
    cl.user_session.set("history", history)