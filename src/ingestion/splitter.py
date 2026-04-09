from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_pages(pages):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100,
        separators=["\n\n", "\n", " ", "", "."]
    )
    return splitter.split_documents(pages)
