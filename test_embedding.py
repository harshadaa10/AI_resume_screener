from ai_engine import get_embedding

text = "We are hiring a professional with experience in early childhood education."
embedding = get_embedding(text)
print("Embedding vector (first 5 values):", embedding[:5])
