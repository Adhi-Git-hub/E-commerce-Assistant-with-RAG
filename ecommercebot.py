
import cohere
import pinecone
from sentence_transformers import SentenceTransformer
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
import os

os.environ["PINECONE_API_KEY"] = "b2bb88c2-b9fa-4e21-a52e-7a28a36f81e5"

pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))

index_name = "ecommerceproducts-rag-qa"

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

index = pc.Index(index_name)


# Retrieve matching documents based on query
def retrieve_documents(query, index, model, top_k=2): # modify the k value
    # Embed the query
    query_embedding = model.encode(query)

    # Query Pinecone index
    results = index.query(
        vector=query_embedding.tolist(),
        top_k=top_k,
        include_metadata=True
    )

    # Extract matched documents' content from metadata
    matched_documents = [match['metadata']['content'] for match in results['matches']]

    return matched_documents

cohere_api_key = 'TU6TQq3r8pHomFp7QTFjNrXVoNmR6ByAjfFYljtW'
co = cohere.Client(cohere_api_key)

conversation_history = []

# Modify the generate_response function to include conversation history
def generate_response(query):
    # Retrieve relevant documents from Pinecone
    documents = retrieve_documents(query, index, embedding_model)

    # Update conversation history
    conversation_history.append(f"User: {query}")
    conversation_history.append(f"Bot: {' '.join(documents)}")

    # Combine conversation history into a single context
    context = "\n".join(conversation_history)

    # Create prompt for Cohere API including the conversation history
    prompt = f"{context}\n\nQ: {query}\nA:"

    # Generate response using Cohere
    response = co.generate(
        model='command-xlarge-nightly',
        prompt=prompt,
        max_tokens=100,
        temperature=0.7
    )

    # Append bot's latest response to conversation history
    conversation_history.append(f"Bot: {response.generations[0].text.strip()}")
    return response.generations[0].text.strip()





