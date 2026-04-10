from .loader import load_file
from .splitter import split_pages
import os

def run_ingestion_pipeline(file_path):
    print(f"Loading document... from {file_path}")
    pages = load_file(file_path)

    print("splitting document...")
    chunks = split_pages(pages)

    #tag each chunk with source metadata (filename + page number)
    file_name = os.path.basename(file_path)
    for chunk in chunks:
        chunk.metadata["source"] = file_name
        chunk.metadata["file_path"] = file_path
        if "page_number" in chunk.metadata:
            chunk.metadata["page"] = chunk.metadata["page_number"]

    print(f"Document split into {len(chunks)} chunks.")
    return chunks

if __name__ == "__main__":
    run_ingestion_pipeline(r"data\NIPS-2017-attention-is-all-you-need-Paper.pdf")