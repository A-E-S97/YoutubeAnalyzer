
from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import Tool
from datetime import datetime


def save_to_txt(data: str, filename_prefix: str = "video_analysis"):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.txt"
    formatted_text = f"---GPT Output---\nTimestamp: {timestamp}\n\n{data}\n\n"
    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)
    return f"Data successfully saved to {filename}"

save_tool = Tool(
    name = "save_text_to_file",
    func = save_to_txt,
    description = "Saves structured response to text file.",
)
search = DuckDuckGoSearchRun()
search_tool = Tool(
    name = "search",
    func = search.run,
    description = "Search DuckDuckGo for information to validate the information provided.",
)

# api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max= 300, wiki_client=search)
# wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)
