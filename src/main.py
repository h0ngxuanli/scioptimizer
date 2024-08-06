import asyncio
import semantic_kernel as sk
from agents_sk import ResearchTools

import os
from openai import AsyncOpenAI
from semantic_kernel.connectors.ai.open_ai.services.open_ai_chat_completion import OpenAIChatCompletion
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.functions.kernel_arguments import KernelArguments
import json
from utils import extract_parameters

# async def main():

#     chat_history.add_user_message(user_input)

#     answer = await kernel.invoke(
#         chat_func,
#         user_input=user_input,
#         chat_history=chat_history,
#     )
#     chat_history.add_assistant_message(str(answer))



    
    
    

    
    
#     keywords = await kernel.run_async("research_tools", "extract_keywords", kernel = kernel, query=query, num_keywords=num_keywords)
#     print(f"Extracted keywords: {keywords}")

#     # Retrieve papers
#     max_results = 10
#     papers = await kernel.run_async("research_tools", "retrieve_papers", keywords=keywords, max_results=max_results)
    
#     # Optionally, add user-provided keywords
#     papers_list = json.loads(papers)
#     user_keywords = ["artificial intelligence", "neural networks"]  # Example user-provided keywords
#     for paper in papers_list:
#         paper['keywords'] = list(set(paper['keywords'] + user_keywords))
#     papers = json.dumps(papers_list)

#     # Save to CSV
#     filename = "papers.csv"
#     csv_result = await kernel.run_async("research_tools", "save_to_csv", papers=papers, filename=filename)
#     print(csv_result)
    
#     # Save to Zotero (you need to provide your Zotero credentials)
#     library_id = "your_zotero_library_id"
#     zotero_api_key = "your_zotero_api_key"
#     zotero_result = await kernel.run_async("research_tools", "save_to_zotero", papers=papers, library_id=library_id, api_key=zotero_api_key)
#     print(zotero_result)

#     # Fine-grained retrieval example
#     extracted_keywords = keywords.split(',')[:2]  # Use the first two extracted keywords for filtering
#     filters = json.dumps({"keywords": extracted_keywords})
#     filtered_papers = await kernel.run_async("research_tools", "fine_grained_retrieval", papers=papers, filters=filters)
#     print(filtered_papers)




async def chat(kernel, chat_history) -> bool:
    try:
        user_input = input("User:> ")
    except KeyboardInterrupt:
        print("\n\nExiting chat...")
        return False
    except EOFError:
        print("\n\nExiting chat...")
        return False

    if user_input == "exit":
        print("\n\nExiting chat...")
        return False


    
    #Extract keywords
    keywords = await kernel.invoke(
        function_name="get_keywords",
        plugin_name="research_tools", 
        kernel = kernel, chat_history = chat_history, query=user_input)
    
    results = str(keywords.value[0])
    params = extract_parameters(results)
    print(f"Mosscap:> {params}")
    
    
    #Save reuslts to dataframe
    keywords = await kernel.invoke(
        function_name="retrieve_papers",
        plugin_name="research_tools", 
        num_papers = 2,
        **params)
    
    
    
    chat_history.add_user_message(user_input)
    chat_history.add_assistant_message(str(keywords))
    return True, chat_history


async def main() -> None:
    
    # Initialize the kernel
    kernel = sk.Kernel()

    # Create ResearchTools instance
    research_tools = ResearchTools()
    kernel.add_plugin(research_tools, plugin_name="research_tools")
    research_tools.setup_llm(kernel)
    research_tools.setup_keywords_extractor()
    chat_history = ChatHistory()
    
    chatting = True
    while chatting:
        chatting, chat_history  = await chat(kernel, chat_history)


if __name__ == "__main__":
    asyncio.run(main())
    
# research_tools_chat_func = 