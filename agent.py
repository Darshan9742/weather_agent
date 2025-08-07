import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from tools import get_current_weather, calculate_energy_consumption_tool, _calculate_energy_consumption_func, Appliance

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.1,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

tools = [get_current_weather, calculate_energy_consumption_tool]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an AI energy agent. Your purpose is to provide helpful, actionable, and friendly energy-saving tips to users in India."),
    ("placeholder", "{chat_history}"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

def get_agent_response(user_query: str):
    return agent_executor.invoke({"input": user_query})

def get_proactive_tip(location: str):
    query = f"The user is in {location}. What is the weather like, and based on this, provide a single, specific, and actionable energy-saving tip for today?"
    return agent_executor.invoke({"input": query})

def get_reactive_tips(appliances: list):
    consumption_data = _calculate_energy_consumption_func(appliances)
    high_consumers = consumption_data['high_consumers']
    high_consumer_names = ", ".join(high_consumers)
    
    query = f"""
    The user has the following appliances: {appliances}. Their highest-consuming appliances are {high_consumer_names}.
    Please provide a JSON object with two keys: "general_tips" and "appliance_tips".
    "general_tips" should be an array of 2 objects, each with a "tip" and "details".
    "appliance_tips" should be an array of objects for each high-use appliance, each with "appliance_name", "tip", and "details".
    Make the tips concise and relevant to an Indian context.
    """
    
    agent_response = get_agent_response(query)
    output_string = agent_response.get('output', '')

    # Clean up possible code fences from model output
    json_string = output_string.strip().removeprefix('```json').removesuffix('```').strip()

    try:
        tips_data = json.loads(json_string)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON from LLM output: {e}")
        # Return a simple error message to the frontend
        return {"error": "Failed to parse tips from AI model."}

    return tips_data