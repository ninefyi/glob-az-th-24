from pymongo import MongoClient
from langchain_openai import AzureOpenAIEmbeddings
from datasets import load_dataset
import pandas as pd
import numpy as np
import secret

client = MongoClient(secret.MONGODB_URI)
dbName = secret.MONGODB_DB
collectionName = secret.MONGODB_COLLECTION
collection = client[dbName][collectionName]

embeddings = AzureOpenAIEmbeddings(api_key=secret.AZURE_OPENAI_API_KEY, azure_endpoint=secret.AZURE_OPENAI_ENDPOINT, azure_deployment=secret.AZURE_OPENAI_DEPLOYMENT,api_version=secret.AZURE_OPENAI_VERSION)

# https://huggingface.co/datasets/MongoDB/embedded_movies
ds = load_dataset("MongoDB/embedded_movies")

# Convert the dataset to a pandas dataframe
df = pd.DataFrame(ds["train"])

df = df.dropna(how='any',axis=0) 

def get_embedding(text: str) -> list[float]:
    return embeddings.embed_query(text)

df["embedding"] = df["fullplot"].apply(get_embedding)

documents = df.to_dict("records")

# collection.delete_many({})
collection.insert_many(documents)

print("Data ingestion into MongoDB completed")