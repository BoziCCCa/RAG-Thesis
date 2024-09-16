def add_vectors_to_database(vectors):
    index=initialize_pinecone()
    index.upsert(vectors)

def get_existing_vector_ids():
    index=initialize_pinecone()
    existing_ids = set()
    for id in index.list():
        existing_ids.update(id)  
    return existing_ids

import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

def create_new_index(pc,index_name):
    pc.create_index(
    name=index_name,
    dimension=1536,
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    )
    )

def initialize_pinecone():
    
    index_name="quickstart-index"
    load_dotenv()
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    existing_indexes = [index['name'] for index in pc.list_indexes()]

    if index_name not in existing_indexes:
        create_new_index(pc,index_name)

    index = pc.Index(index_name)
    return index





