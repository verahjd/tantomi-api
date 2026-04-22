import os 
import json
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from dotenv import load_dotenv

load_dotenv()

embedding_function = OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="text-embedding-3-small"
)

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="tantomi_resources",
    embedding_function=embedding_function
)

def build_knowledge_base():
    if collection.count() > 0:
        print("Knowledge base already exists, skipping build")
        return collection
    
    with open("app/data/resources.json", "r") as f:
        resources = json.load(f)

    documents = []
    metadatas = []
    ids = []

    for resource in resources:
        document = f"{resource['title']}. {resource['description']}. Topic: {resource['topic']}. Level:{resource['level']}"
        documents.append(document)
        metadatas.append({
            "title": resource['title'],
            "url": resource['url'],
            "topic": resource['topic'],
            "level": resource['level'],
            "description": resource['description']
        })
        ids.append(resource["id"])

    collection.add(
        documents=documents, 
        metadatas=metadatas,
        ids=ids
    )

    print(f"Knowledge base built with {len(documents)} resources")
    return collection

def search_resources(query: str, n_results: int = 3):
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    clean_results = []
    for metadata, distance in zip(metadatas, distances):
        clean_results.append({
            "title": metadata["title"],
            "url": metadata["url"],
            "topic": metadata["topic"],
            "level": metadata["level"],
            "description": metadata["description"],
            "distance": distance
        })

    return clean_results