from .loader import load_file
from .splitter import split_pages

def run_ingestion_pipeline(file_path):
    print(f"Loading document... from {file_path}")
    pages = load_file(file_path)

    print("splitting document...")
    chunks = split_pages(pages)

    print(f"Document split into {len(chunks)} chunks.")
    return chunks

if __name__ == "__main__":
    run_ingestion_pipeline(r"data\NIPS-2017-attention-is-all-you-need-Paper.pdf")