from langchain.text_splitter import RecursiveCharacterTextSplitter
from embedding import get_embeddings
from pinecone_init import index
from langchain.load import dumps, loads
from embedding import embeddings_model


def split_queries(queries):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=100, 
        chunk_overlap=20,
        is_separator_regex=False,
    )
    split_queries = [split for query in queries for split in text_splitter.split_text(query)]
    return split_queries

def embed_query(query):
    return get_embeddings(query)

def retrieve_documents(queries):
    query_splits=split_queries(queries)
    query_embeddings = embeddings_model.embed_documents(query_splits)

    results = []
    for query_embedding in query_embeddings:
        response = index.query(
            vector=query_embedding, 
            top_k=3,
            include_metadata=True
        )
        results.append(response["matches"])
    return results

def reciprocal_rank_fusion(results: list[list[dict]], k=60):
    fused_scores = {}

    for docs in results:
        for rank, doc in enumerate(docs):
            doc_id = doc['id']
            score = doc['score']
            page_content=doc['metadata']['page_content']
            doc_str = dumps({'id': doc_id, 'score': score,'page_content':page_content})

            if doc_str not in fused_scores:
                fused_scores[doc_str] = 0

            fused_scores[doc_str] += score / (rank + k)

    reranked_results = [
        (loads(doc), score)
        for doc, score in sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
    ]

    return reranked_results