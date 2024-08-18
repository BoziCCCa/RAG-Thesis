import os
import getpass
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from retrieval_and_ranking import retrieve_documents, reciprocal_rank_fusion
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

load_dotenv()
llm = ChatOpenAI(model_name="gpt-4o-mini-2024-07-18", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))


map_prompt = ChatPromptTemplate.from_template("""Write a concise summary for each document of the following: {docs}.""")
map_chain = map_prompt | llm

reduce_prompt =ChatPromptTemplate.from_template( """
The following is a set of summaries:
{docs}
Take these and distill it into a final, consolidated summary
of the main themes(You should only have one text(paragraph) as an output that will have all the important information from each summary).
""")
reduce_chain = reduce_prompt | llm

map_reduce_chain = map_chain |  reduce_chain | StrOutputParser()

rag_fusion_prompt = ChatPromptTemplate.from_template(
        """You are a helpful assistant that generates multiple search queries based on a single input query. \n
        Generate multiple search queries related to: {question} \n
        Output (4 queries):"""
    )

generate_queries_chain = rag_fusion_prompt | llm | StrOutputParser()


generation_prompt=ChatPromptTemplate.from_template("""Answer the question based only on the following context:
{context}

Question: {question}
""")

generation_chain=generation_prompt | llm | StrOutputParser()


def rag_fusion_pipeline(question):
   
    generated_queries = generate_queries_chain.invoke({"question":question})
    generated_queries_list = generated_queries.split("\n")
    generated_queries_list = [query.strip() for query in generated_queries_list if query.strip()]

    retrieved_docs = retrieve_documents(generated_queries_list)

    ranked_docs = reciprocal_rank_fusion(retrieved_docs)

    ranked_docs_content = [doc[0]['page_content'] for doc in ranked_docs]
    top_ranked_docs_content=ranked_docs_content[0:3]

    result_summary = map_reduce_chain.invoke({"docs": top_ranked_docs_content})

    final_answer = generation_chain.invoke({
        "context": result_summary,   # Summary of the retrieved documents
        "question": question         # Original user question
    })

    print("FINAL ANSWER: ", final_answer)


rag_fusion_pipeline("Na koje grupe se dele ribe?")
