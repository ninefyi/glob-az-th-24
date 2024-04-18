# glob-az-th-24
Global Azure Thailand 2024

## Preparation
- Python 3.11
- `python -m pip install datasets pandas numpy gradio langchain_openai langchain_community langchain pymongo bs4 tiktoken gradio requests lxml argparse unstructured`
- Atlas Vector Search Index
```json
{
  "fields": [{
    "path": "embedding",
    "numDimensions": 1536,
    "similarity": "cosine",
    "type": "vector"
  }]
}
```
- File: secret.py
```bash
OPENAI_API_KEY=""
MONGODB_URI="mongodb+srv://"
MONGODB_DB="demo"
MONGODB_COLLECTION="collection1"
AZURE_OPENAI_ENDPOINT="https://xxxxx.openai.azure.com/"
AZURE_OPENAI_API_KEY=""
AZURE_OPENAI_VERSION="2024-02-15-preview"
AZURE_OPENAI_DEPLOYMENT=""
AZURE_OPENAI_CHAT_MODEL=""
```