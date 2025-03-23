from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI

model = OpenAIChatCompletionsModel(
    model="gemma3:4b",
    openai_client=AsyncOpenAI(base_url="http://localhost:11434/v1")
)

agent = Agent(
    name="Assistant", 
    instructions="You are a helpful assistant.",
    model=model
)
result = Runner.run_sync(agent, "What is the capital of France?")
print(result.final_output)