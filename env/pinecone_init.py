import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

def add_vectors_to_database(vectors):
    index.upsert(vectors)

def create_new_index(pc):
    pc.create_index(
    name=index_name,
    dimension=1536,
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    )
    )

def get_existing_vector_ids():
    existing_ids = set()
    for id in index.list():
        existing_ids.update(id)  
    return existing_ids

index_name="quickstart-index"

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

existing_indexes = [index['name'] for index in pc.list_indexes()]

# if index_name in existing_indexes:
#     pc.delete_index(index_name)
#     create_new_index(pc)

if index_name not in existing_indexes:
    create_new_index(pc)

index = pc.Index(index_name)





