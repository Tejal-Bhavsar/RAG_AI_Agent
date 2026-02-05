import numpy as np
import faiss
import requests  # Make sure to: pip install requests
from sentence_transformers import SentenceTransformer

# 1. Load the same local embedding model we used for ingestion
model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_query(query: str):
    """Turns the user's question into a vector using the local Mac CPU."""
    embedding = model.encode([query])
    vec = np.array(embedding, dtype="float32")
    faiss.normalize_L2(vec)
    return vec

def retrieve(query, index, chunks, k=4):
    """Finds the most relevant snippets from your FAISS index."""
    qvec = embed_query(query)
    _, ids = index.search(qvec, k)
    results = [chunks[i] for i in ids[0] if i != -1]
    return results

def generate_answer(user_question, retrieved_chunks):
    """Sends the retrieved text to your local Ollama server to get an answer."""
    context = "\n\n".join(retrieved_chunks)
    
    prompt = f"""
    You are a precise International Student Advisor. 
    Use the following pieces of context to answer the student's question. 
    If the information is not in the context, say you don't know and advise them to contact the ISO.
    
    Context:
    {context}
    
    Question: 
    {user_question}
    """

    # This talks to the Ollama app running on your MacBook
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "system": "You are a helpful University Advisor.",
                "stream": False
            }
        )
        response.raise_for_status()
        return response.json().get("response")
    except Exception as e:
        return f"Local AI Error: Make sure Ollama is running! ({str(e)})"


# import numpy as np
# import faiss
# from sentence_transformers import SentenceTransformer
# from openai import OpenAI
# from dotenv import load_dotenv

# load_dotenv()
# client = OpenAI() # Keep this for the FINAL answer (GPT-4/5)
# model = SentenceTransformer('all-MiniLM-L6-v2')

# def embed_query(query: str):
#     # Use the same local model as the store
#     embedding = model.encode([query])
#     vec = np.array(embedding, dtype="float32")
#     faiss.normalize_L2(vec)
#     return vec

# def retrieve(query, index, chunks, k=4):
#     qvec = embed_query(query)
#     _, ids = index.search(qvec, k)
#     results = [chunks[i] for i in ids[0] if i != -1]
#     return results

# def generate_answer(user_question, retrieved_chunks):
#     context = "\n\n".join(retrieved_chunks)
    
#     # Note: You still need a tiny bit of credit for this GPT call.
#     # If GPT also fails, I can show you how to use a local LLM (Ollama)!
#     response = client.chat.completions.create(
#         model="gpt-4-turbo", # Use gpt-4 or gpt-3.5-turbo
#         messages=[
#             {"role": "system", "content": "You are a precise International Student Advisor. Use the context to answer."},
#             {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{user_question}"}
#         ]
#     )
#     return response.choices[0].message.content



# # import os
# # import numpy as np
# # import faiss
# # from dotenv import load_dotenv  # 1. Keep the import
# # from openai import OpenAI

# # #first looks for .env file and loads the key
# # load_dotenv() 

# # # then call the openapi
# # client = OpenAI()
# # CHAT_MODEL = "gpt-5.2"
# # EMBED_MODEL = "text-embedding-3-small"


# # def embed_query(query: str):
# #     resp = client.embeddings.create(model=EMBED_MODEL, input=[query])
# #     vec = np.array([resp.data[0].embedding], dtype="float32")
# #     faiss.normalize_L2(vec)
# #     return vec


# # def retrieve(query, index, chunks, k=4):
# #     qvec = embed_query(query)
# #     _, ids = index.search(qvec, k)

# #     results = []
# #     for i in ids[0]:
# #         if i != -1:
# #             results.append(chunks[i])

# #     return results


# # def generate_answer(user_question, retrieved_chunks):
# #     context = "\n\n".join(retrieved_chunks)

# #     response = client.responses.create(
# #         model=CHAT_MODEL,
# #         instructions=(
# #             "You are an Insurance Agency Customer Care assistant. "
# #             "Use only the provided context to answer. "
# #             "If the answer is not present, say you do not have it and offer human support."
# #         ),
# #         input=f"Context:\n{context}\n\nQuestion:\n{user_question}",
# #     )

# #     return response.output_text