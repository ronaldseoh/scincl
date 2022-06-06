import faiss

index = None


def load_faiss_index(path):
    index = faiss.read_index(paths)
