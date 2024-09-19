
from flask import Flask, request, jsonify
from flask_cors import CORS

from rag_fusion_and_generation import rag_fusion_pipeline
from doc_loading import load_documents
from embedding import embed_and_index_documents
from pinecone_init import initialize_pinecone


def initialize():
    global index
    index = initialize_pinecone()  
    documents = load_documents() 
    embed_and_index_documents(documents) 



app = Flask(__name__)
CORS(app)
initialize()

@app.route('/ask-question', methods=['POST'])
def ask_question():
    data = request.get_json()  
    query = data.get("question")
    
    if not query:
        return jsonify({"error": "No question provided"}), 400
    
    answer = rag_fusion_pipeline(query)  
    print("Answer: ",answer)
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(debug=True)  
