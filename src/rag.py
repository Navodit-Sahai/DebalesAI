import requests
from bs4 import BeautifulSoup
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

URLS = [
    "https://debales.ai",
    "https://debales.ai/about",
    "https://debales.ai/blog",
]


def scrape_urls(urls):
    docs = []

    for url in urls:
        print(f"Scraping: {url}")
        try:
            res = requests.get(url, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")

            # Removing useless tags
            for tag in soup(["script", "style", "nav", "footer"]):
                tag.decompose()

            text = soup.get_text(separator="\n", strip=True)

            docs.append(Document(
                page_content=text,
                metadata={"source": url}
            ))

        except Exception as e:
            print(f"Error: {e}")

    return docs



def build_index(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    store = FAISS.from_documents(chunks, embeddings)
    return store



def retrieve_context(query, store, k=3):
    results = store.similarity_search(query, k=k)

    context = ""
    for i, doc in enumerate(results, 1):
        context += f"\n[Chunk {i} - {doc.metadata['source']}]\n"
        context += doc.page_content + "\n"

    return context


#WORKFLOW
docs = scrape_urls(URLS)
store = build_index(docs)

# query = "What does Debales AI do?"
# context = retrieve_context(query, store)

# print(context)