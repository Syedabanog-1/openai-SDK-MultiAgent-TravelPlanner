import chainlit as cl
from app import run  # Make sure app.py is in the same directory or properly imported

# Triggered when the chat starts
@cl.on_chat_start
async def start():
    await cl.Message(
        content="👋 Hello! I am your travel assistant. I can give you weather updates or help you find flights. How may I help you today?"
    ).send()

# Triggered when a message is sent by the user
@cl.on_message
async def handle_message(message: cl.Message):
    if message and message.content:
        user_input = message.content
        print("User message:", user_input)

        # Call the agent logic from app.py
        result = run(user_input)

        # Send the response back to the user
        await cl.Message(content=result).send()
