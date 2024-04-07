from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.tools import Tool
from tools.tools import get_profile_url


def lookup(name: str) -> str:

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    template = """given the name {name_of_person} I want you to find a link to their Twitter profile page, and extract from it their username
       In Your Final answer only the person's username"""

    tools_for_agent = [
        Tool(
            name="Crawl Google 4 Twitter profile page",
            func=get_profile_url,
            description="useful for when you need get the Twitter Page URL",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")

    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )

    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)

    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )

    twitter_username = result["output"]
    return twitter_username