import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_cohere import CohereEmbeddings
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from doc_loading import load_documents
from pinecone_init import add_vectors_to_database, get_existing_vector_ids
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
load_dotenv()

documents = load_documents()

embeddings_model = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=os.getenv("OPANAI_API_KEY")
)

def split_documents(documents, chunk_size=200, chunk_overlap=40):
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=chunk_size, 
        chunk_overlap=chunk_overlap,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)

def calculate_chunk_ids(docs):
    last_page_id = None
    current_chunk_index = 0
    chunk_ids = []

    for doc in docs:
        source = doc.metadata.get("source")
        page = doc.metadata.get("page")
        current_page_id = f"{source}:{page}"

        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        chunk_ids.append(chunk_id)

    return chunk_ids

def get_embeddings(content):
    return embeddings_model.embed_query(content)

def embed_and_index_documents(documents):
    docs = split_documents(documents)
    
    embeddings = []
    vectors = []
    
    chunk_ids = calculate_chunk_ids(docs)
    for i, doc in enumerate(docs):
        embedding = get_embeddings(doc.page_content)
        embeddings.append(embedding)
        

        doc.metadata["page_content"] = doc.page_content
        vectors.append((chunk_ids[i], embedding, doc.metadata))

    
    existing_ids = get_existing_vector_ids()
    
    new_vectors = [(id, embedding, metadata) for id, embedding, metadata in vectors if id not in existing_ids]
    
    if new_vectors:
        print(f"Adding {len(new_vectors)} new vectors to Pinecone.")
        
        add_vectors_to_database(new_vectors)
        print(f"Indexed {len(new_vectors)} vectors into Pinecone.")
    else:
        print("No new vectors to add.")

embed_and_index_documents(documents)
