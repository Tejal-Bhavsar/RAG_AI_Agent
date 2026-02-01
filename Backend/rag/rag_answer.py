import os
import numpy as np
import faiss
from dotenv import load_dotenv  # 1. Keep the import
from openai import OpenAI

#first looks for .env file and loads the key
load_dotenv() 

# then call the openapi
client = OpenAI()
CHAT_MODEL = "gpt-5.2"
EMBED_MODEL = "text-embedding-3-small"


def embed_query(query: str):
    resp = client.embeddings.create(model=EMBED_MODEL, input=[query])
    vec = np.array([resp.data[0].embedding], dtype="float32")
    faiss.normalize_L2(vec)
    return vec


def retrieve(query, index, chunks, k=4):
    qvec = embed_query(query)
    _, ids = index.search(qvec, k)

    results = []
    for i in ids[0]:
        if i != -1:
            results.append(chunks[i])

    return results


def generate_answer(user_question, retrieved_chunks):
    context = "\n\n".join(retrieved_chunks)

    response = client.responses.create(
        model=CHAT_MODEL,
        instructions=(
            "You are an Insurance Agency Customer Care assistant. "
            "Use only the provided context to answer. "
            "If the answer is not present, say you do not have it and offer human support."
        ),
        input=f"Context:\n{context}\n\nQuestion:\n{user_question}",
    )

    return response.output_text