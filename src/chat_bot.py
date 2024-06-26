from pymongo import MongoClient
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from langchain_community.callbacks import get_openai_callback
from langchain_core.messages import HumanMessage
import gradio as gr
from gradio.themes.base import Base
import secret

client = MongoClient(secret.MONGODB_URI)
dbName = secret.MONGODB_DB
collectionName = secret.MONGODB_COLLECTION
collection = client[dbName][collectionName]

embeddings = AzureOpenAIEmbeddings(api_key=secret.AZURE_OPENAI_API_KEY, azure_endpoint=secret.AZURE_OPENAI_ENDPOINT, azure_deployment=secret.AZURE_OPENAI_DEPLOYMENT,api_version=secret.AZURE_OPENAI_VERSION)

def get_embedding(text: str) -> list[float]:
    return embeddings.embed_query(text)

def vector_search(user_query):

    # Generate embedding for the user query
    query_embedding = get_embedding(user_query)

    if query_embedding is None:
        return "Invalid query or embedding generation failed."

    # Define the vector search pipeline
    vector_search_stage = {
        "$vectorSearch": {
            "index": "vector_index",
            "queryVector": query_embedding,
            "path": "embedding",
            "numCandidates": 150,  # Number of candidate matches to consider
            "limit": 4  # Return top 4 matches
        }
    }

    unset_stage = {
        "$unset": "embedding"  # Exclude the 'embedding' field from the results
    }

    project_stage = {
        "$project": {
            "_id": 0,  # Exclude the _id field
            "fullplot": 1,  # Include the plot field
            "title": 1,  # Include the title field
            "genres": 1, # Include the genres field
            "score": {
                "$meta": "vectorSearchScore"  # Include the search score
            }
        }
    }

    pipeline = [vector_search_stage, unset_stage, project_stage]

    # Execute the search
    results = collection.aggregate(pipeline)
    return list(results)

def query_data(user_query):

    atlas_vector_search = vector_search(user_query)
    vector_response = ""
    for result in atlas_vector_search:
        vector_response += f"Title: {result.get('title', 'N/A')}, Plot: {result.get('fullplot', 'N/A')}\n"

    combined_query = f"Query: {user_query}\nContinue to answer the query by using the Search Results:\n{vector_response}."
    llm  = AzureChatOpenAI(api_key=secret.AZURE_OPENAI_API_KEY, azure_endpoint=secret.AZURE_OPENAI_ENDPOINT, azure_deployment=secret.AZURE_OPENAI_CHAT_MODEL,api_version=secret.AZURE_OPENAI_VERSION)
    llm.invoke(combined_query)

    human_message = HumanMessage(content=combined_query)
    ai_response = llm.invoke([human_message]).content

    return vector_response, ai_response

# query_data("What is the best romantic movie to watch and why?")

# Create a web interface for the app, using Gradio

with gr.Blocks(theme=Base(), title="Question Answering App using Vector Search + RAG") as demo:
    gr.Markdown(
        """
        # Question Answering App using Atlas Vector Search + RAG Architecture
        """)
    textbox = gr.Textbox(label="Enter your Question:")
    with gr.Row():
        button = gr.Button("Submit", variant="primary")
    with gr.Column():
        output1 = gr.Textbox(lines=1, max_lines=10, label="Output with just Atlas Vector Search (returns text field as is):")
        output2 = gr.Textbox(lines=1, max_lines=10, label="Output generated by chaining Atlas Vector Search to Langchain's Azure AI Service LLM:")

# Call query_data function upon clicking the Submit button

    button.click(query_data, textbox, outputs=[output1, output2])

demo.launch(share=True, server_port=7860)