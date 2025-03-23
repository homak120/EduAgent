from duckduckgo_search import DDGS
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, function_tool, RunConfig
from datetime import datetime

current_date = datetime.now().strftime("%Y-%m-%d")

model = OpenAIChatCompletionsModel(
    model="llama3.2:latest",
    openai_client=AsyncOpenAI(base_url="http://localhost:11434/v1")
)

# 1. Create Internet Search Agent
@function_tool
def search_news(topic: str) -> str:
    print(f"Searching for news on topic: {topic}")
    with DDGS() as ddgs:
        results = ddgs.text(f"{topic} news {current_date}", max_results=5)
        if results:
            all_text_results = "\n\n";
            print(f"Found {len(results)} results.")
            for result in results:
                print(f"Title: {result['title']}")
                print(f"Link: {result['href']}")
                print(f"Snippet: {result['body']}")
                all_text_results = all_text_results + "Title: " + result['title'] + "\nLink: " + result['href'] + "\nSnippet: " + result['body'] + "\n\n"
            return all_text_results
        else:
            return f"No results found for {topic}."
        
# 2. Create Agent

search_news_agent = Agent(
    name="Search News Assistant", 
    instructions="You provide the latest news articles on a given topic from the internet search.",
    tools=[search_news],
    model=model
)

edit_news_agent = Agent(
    name="Edit News Assistant",
    instructions="You are a helpful assistant that edits the news articles and make sure adding link of the source at the end of each article.", 
    model=model
)

# 3. Run mutlipe agents in a chain
def run_search_news_agents_chain(topic: str):
    print("Running agents chain...")

    run_config = RunConfig(workflow_name="Search & Edit News Workflow")

    # Run the search new agent
    search_news_result = Runner.run_sync(
        search_news_agent, 
        topic,
        run_config=run_config
    )
    print("Search news result:", search_news_result.final_output)

    edit_news_result = Runner.run_sync(
        edit_news_agent, 
        search_news_result.final_output,
        run_config=run_config
    )
    print("Edit new result:", edit_news_result.final_output)

    return edit_news_result.final_output

#print(run_search_news_agents_chain("Generative AI"))

