from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_pages(pages):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50
    )
    return splitter.split_documents(pages)
