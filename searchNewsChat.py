import chainlit as cl
from searchNewsAgents import run_search_news_agents_chain

@cl.on_message
async def main(message: cl.Message):
    """
    Main function to handle incoming messages for run search news agents chain.
    """
    topic = message.content

    await cl.Message(
        content=f"Searching for news articles for '{topic}'...",
        author="EduAgent"
    ).send()

    try:
        result = run_search_news_agents_chain(topic)
        await cl.Message(
            content=f"Here are the latest news articles for '{topic}':\n{result}"
        ).send()
    except Exception as e:
        await cl.Message(
            content=f"An error occurred: {e}",
            author="EduAgent"
        ).send()

@cl.on_chat_start
async def start_chat():
    """
    Function to handle chat start event.
    """
    await cl.Message(
        content="Welcome to the News Search Assistant! Please enter a topic to search for news articles."
    ).send()