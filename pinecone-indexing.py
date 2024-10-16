import pinecone
from sentence_transformers import SentenceTransformer
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
import os

os.environ["PINECONE_API_KEY"] = "your pinecone api"

pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))

index_name = "ecommerceproducts-rag-qa"

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

index = pc.Index(index_name)

import pandas as pd

ds=pd.read_csv("/content/eCommerceProducts.csv")
print(ds.head())

pc.create_index(
    name=index_name,
    dimension=384, # Replace with your model dimensions
    metric="cosine", # Replace with your model metric
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    )
)


from sentence_transformers import SentenceTransformer

# Load embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Create documents by combining all relevant product details
data = ds  # Assuming ds is a Pandas DataFrame

# Concatenate all columns into a single document string
documents = [
    f"URL: {row['url']} Title: {row['title']} Images: {row['images']} Description: {row['description']} Product ID: {row['product_id']} SKU: {row['sku']} GTIN13: {row['gtin13']} Brand: {row['brand']} Price: {row['price']} Currency: {row['currency']} Availability: {row['availability']} Unique ID: {row['uniq_id']}"
    for index, row in data.iterrows()
]

# Embed documents and generate embeddings
def embed_documents_with_metadata(documents, model):
    embeddings = model.encode(documents, show_progress_bar=True)
    # Create tuples of (id, embedding, metadata)
    vectors = [(f'id_{i}', embedding, {'content': doc}) for i, (embedding, doc) in enumerate(zip(embeddings, documents))]
    return vectors

# Generate embeddings for the product documents
vectors_with_metadata = embed_documents_with_metadata(documents, embedding_model)

index.upsert(vectors=vectors_with_metadata)
