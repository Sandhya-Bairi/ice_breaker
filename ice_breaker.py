from dotenv import load_dotenv

load_dotenv()
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent
from third_parties.twitter_with_stubs import scrape_user_tweets
from output_parsers import person_intel_parser

name = "Sandhya Rani Bairi"


def ice_break(name: str) -> str:
    linkedin_profile_url = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_profile_url)

    twitter_username = twitter_lookup_agent(name=name)
    tweets = scrape_user_tweets(username=twitter_username, num_tweets=100)

    summary_template = """
        given the information {linkedin_information} and twitter {twitter_information} about a person I want you to create:
        1. A short summary
        2. two interesting facts about them
        3. A topic that may interest them
        4. 2 creative ice breakers to open a conversation with them
        \n{format_instructions}
        """

    summary_prompt_template = PromptTemplate(
        input_variables=["linkedin_information", "twitter_information"],
        template=summary_template,
        partial_variables={
            "format_instructions": person_intel_parser.get_format_instructions()
        },
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)
    result = chain.run(linkedin_information=linkedin_data, twitter_information=tweets)

    print(result)
    return person_intel_parser.parse(result)


if __name__ == "__main__":

    print("Hello LangChain!")

    result = ice_break(name="Sandhya Rani Bairi")

    # print(chain.invoke(input={"linkedin_information": linkedin_data, "twitter_information":tweets}))
