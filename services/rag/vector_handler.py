from vector_db_utils import store_to_vector_db, retrieve_from_vector_db

def store_chunks_to_vectorstore(chunks: list[str]):
    store_to_vector_db(chunks)

def query_vectorstore(query: str) -> list[str]:
    return retrieve_from_vector_db(query)
