import os

from dotenv import load_dotenv
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser, format_instructions
from youtube_transcript_api import YouTubeTranscriptApi
from tools import search_tool, save_tool
load_dotenv()

link = (input("Enter the youtube link: "))
video_id = ""
if 'v=' in link:
    start = link.find('v=') + 2
    video_id = link[start: start+11]

transcript = ""
try:
    fetched_transcript = YouTubeTranscriptApi().fetch(video_id)
    for snip in fetched_transcript:
        transcript += snip.text + " "
except Exception as v:
    print("video_id is not accepted\n", v)


class ResearchResponse(BaseModel):
    topic: str
    summary: str
    tools_used: list[str]
    todo: list[str]
    actions_items: list[str]

llm = ChatOpenAI(model="gpt-5.4", api_key=os.getenv("OPENAI_API_KEY"))
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

prompt = ChatPromptTemplate.from_messages(
        [
            (
            "system"
            """
            You will be provided with the transcript of a video and you should analyze it,
            and generate a summary of the video/playlist and if the video is a guide
            to do something, then you will create a todo list and action items.
            Wrap the output in this format and provide no other text.
            Always save the final response to a text file using the save_text_to_file tool.\n{format_instructions}
            """
            ),
            ("placeholder", "{chat_history}"),
            ("human", "{query}"),
            ("placeholder", "{agent_scratchpad}"),
        ]).partial(format_instructions=parser.get_format_instructions())

tools = [search_tool, save_tool]
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
raw_response = agent_executor.invoke({"query": transcript})

try:
    structured_response = parser.parse(raw_response.get("output"))
except Exception as e:
    print("Error parsing response", e, "Raw Response: ", raw_response)
