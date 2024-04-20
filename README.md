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
- Build Docker from Local.
```
docker build --platform linux/amd64 --tag azthailand/py-rag:0.0.1 . 
```
- Build Docker from Azure Container Registry.
```
az acr build --registry azthailand --image azthailand.azurecr.io/py-rag:0.0.1 .
```
- References
1. https://github.com/ninefyi/glob-az-th-24
2. https://www.gradio.app/docs/mount_gradio_app 
3. https://www.mongodb.com/developer/products/atlas/gemma-mongodb-huggingface-rag 
4. https://www.mongodb.com/developer/products/atlas/rag-atlas-vector-search-langchain-openai  
5. https://medium.com/@dehhmesquita/deploy-a-gradio-app-on-azure-using-a-python-azure-app-service-9ea718390a89 
6. https://learn.microsoft.com/en-us/azure/ai-services/openai/
7. https://huggingface.co/datasets/MongoDB/embedded_movies  