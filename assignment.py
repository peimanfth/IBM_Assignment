import os
import config
import requests
import wikipedia
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain.tools.base import ToolException

os.environ["OPENAI_API_KEY"] = config.OPENAI_API_KEY
os.environ["SERPAPI_API_KEY"] = config.SERPAPI_API_KEY
os.environ["OPENWEATHER_API_KEY"] = config.OPENWEATHER_API_KEY


################################################################
# Tools
################################################################

def serpapi_web_search(query: str) -> str:
    """
    Optional: General web search tool using SerpAPI.
    Requires a SERPAPI_API_KEY.
    """
    serpapi_api_key = os.environ.get("SERPAPI_API_KEY", None)
    if not serpapi_api_key:
        raise ToolException("SERPAPI_API_KEY not set in environment.")

    try:
        url = "https://serpapi.com/search"
        params = {
            "engine": "google",
            "q": query,
            "api_key": serpapi_api_key,
            "num": 5,
            "hl": "en",
            "gl": "us",
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        results = data.get("organic_results", [])
        if not results:
            return "No search results found."

        summary_lines = []
        for idx, result in enumerate(results, start=1):
            title = result.get("title", "No Title")
            link = result.get("link", "No Link")
            snippet = result.get("snippet", "No Snippet")
            summary_lines.append(
                f"Result {idx}:\nTitle: {title}\nLink: {link}\nSnippet: {snippet}\n"
            )
        return "\n".join(summary_lines)

    except Exception as e:
        return f"Error in serpapi_web_search: {str(e)}"


def wikipedia_lookup(query: str) -> str:
    """
    Look up information on Wikipedia using the `wikipedia` Python library.
    Returns a summary or content snippet of the best matching article.
    """
    try:
        search_results = wikipedia.search(query, results=5)
        if not search_results:
            return f"No Wikipedia results found for query: {query}"

        best_match = search_results[0]
        page_summary = wikipedia.summary(best_match, sentences=3)
        return f"**Wikipedia Page:** {best_match}\n\n{page_summary}"
    
    except wikipedia.DisambiguationError as de:
        return f"DisambiguationError: This query can refer to multiple pages: {de.options}"
    except wikipedia.PageError:
        return f"PageError: No page found for query '{query}'."
    except Exception as e:
        return f"Error in wikipedia_lookup: {str(e)}"
    
def get_weather(city: str) -> str:
    """Retrieve weather conditions for a specified city."""
    api_key = os.environ.get("OPENWEATHER_API_KEY", None)
    if not api_key:
        raise ToolException("OPENWEATHER_API_KEY not set in environment.")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        return f"The weather in {city} is {weather_desc} with a temperature of {temp}°C."
    return "Weather data not available."

################################################################
# LangChain Tool Objects
################################################################

wikipedia_tool = Tool(
    name="Wikipedia Search",
    func=wikipedia_lookup,
    description="Use this tool to look up information on Wikipedia. Input is a search query string.",
)


search_tool = Tool(
    name="Web Search",
    func=serpapi_web_search,
    description="Use this tool to search the web for information. Input is a user query string."
)

weather_tool = Tool(
    name="Weather Checker",
    func=get_weather,
    description="Retrieve current weather conditions for any city."
)


################################################################
# LLM Setup  &Conversation Memory
################################################################

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    max_retries=2,
)

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

################################################################
#  Initialize Agent
################################################################

tools = [wikipedia_tool, weather_tool, search_tool]  

# prompt = ChatPromptTemplate.from_messages([
#     SystemMessage(content="You are a helpful AI assistant that looks up Wikipedia articles and answers user queries."),
#     MessagesPlaceholder(variable_name="chat_history"),
#      ("human", "Available tools:\n{tool_names}\n\n{tools}\n\nUser query: {input}"),
#     ("ai", "{agent_scratchpad}")
# ])
prompt = ChatPromptTemplate.from_template(
    """You are a knowledgeable AI assistant. Answer user questions as best as you can. 
You have access to the following tools, which you can use when needed:

{tools}

If no tools provide useful results, use your own knowledge to answer.

Use the following format:

Chat History:
{chat_history}

Question: {input}
Thought: You should always think about what to do next.
Action: The action to take, should be one of [{tool_names}]
Action Input: The input to the action
Observation: The result of the action
... (this Thought/Action/Action Input/Observation can only repeat 5 times, then you must answer the question.)
Thought: If I have sufficient information, I will answer the question.
Final Answer: The final answer to the original input question

If no tool is needed, respond with:

Final Answer: [Your direct answer here]

Begin!

Chat History:
{chat_history}

Question: {input}
{agent_scratchpad}"""
)

# Create agent
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
)

# Wrap it in an AgentExecutor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    memory=memory,
    handle_parsing_errors=True,
    max_iterations=10,
    max_execution_time=60  
)

################################################################
# Query Function
################################################################
def query_agent(user_input: str) -> str:
    try:
        response = agent_executor.invoke({"input": user_input})
        return response["output"]
    except Exception as e:
        return f"An error occurred: {str(e)}"

################################################################
# Application Loop
################################################################
if __name__ == "__main__":
    print("LangChain AI Agent with Wikipedia. Type 'exit' or 'quit' to stop.\n")

    while True:
        user_input = input("User: ")
        if user_input.strip().lower() in ["exit", "quit"]:
            print("Exiting. Goodbye!")
            break

        answer = query_agent(user_input)
        print(f"Agent: {answer}\n")
