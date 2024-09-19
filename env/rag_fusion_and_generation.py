import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from retrieval_and_ranking import retrieve_documents, reciprocal_rank_fusion
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

load_dotenv()
llm = ChatOpenAI(model_name="gpt-4o-mini-2024-07-18", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))

map_prompt = ChatPromptTemplate.from_template("""
Write a concise summary for the following document: {doc}.
The summary should contain crucial information regarding this question about board game rules: {question}.
""")
map_chain = map_prompt | llm

reduce_prompt = ChatPromptTemplate.from_template("""
The following is a set of summaries:
{docs}
Take these and distill them into a final, consolidated summary
of the main themes. You are writing summaries about board game rules, so you need to be precise and correct.
The summary should have all the crucial information regarding this question:
{question}
""")
reduce_chain = reduce_prompt | llm | StrOutputParser()


rag_fusion_prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant that generates multiple search queries based on a single input query about board game rules.
Generate multiple search queries related to: {question}
Output (4 queries):
""")
generate_queries_chain = rag_fusion_prompt | llm | StrOutputParser()


generation_prompt = ChatPromptTemplate.from_template("""
Answer the question based only on the following context, be precise and answer only what is asked:
{context}

Question: {question}
""")
generation_chain = generation_prompt | llm | StrOutputParser()


def rag_fusion_pipeline(question):
    
    generated_queries = generate_queries_chain.invoke({"question": question})
    generated_queries_list = generated_queries.split("\n")
    generated_queries_list = [query.strip() for query in generated_queries_list if query.strip()]

    retrieved_docs = retrieve_documents(generated_queries_list)

    ranked_docs = reciprocal_rank_fusion(retrieved_docs)
    ranked_docs_content = [doc[0]['page_content'] for doc in ranked_docs]
    top_ranked_docs_content = ranked_docs_content[0:5]

    mapped_summaries = []
    for doc in top_ranked_docs_content:
        summary = map_chain.invoke({"doc": doc, "question": question})
        mapped_summaries.append(summary.content)

    result_summary = reduce_chain.invoke({
        "docs": "\n".join(mapped_summaries),
        "question": question
    })

    final_answer = generation_chain.invoke({
        "context": result_summary,
        "question": question
    })

    return final_answer
