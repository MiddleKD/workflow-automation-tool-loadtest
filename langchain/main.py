import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from dotenv import load_dotenv
from langchain_core.documents import Document

from rag import PDFRetrievalChain
import config

load_dotenv()

app = FastAPI()

DATA_DIR = Path(os.getenv("DATA_DIR", config.DATA_DIR))
pdf_files = list(DATA_DIR.glob("*.pdf"))
pdf_paths = [str(path) for path in pdf_files]

VECTOR_DIR = Path(os.getenv("VECTOR_DIR", config.VECTOR_DIR))

rag_chain = PDFRetrievalChain(
    source_uri = pdf_paths,
    persist_directory = str(VECTOR_DIR),
    k = config.DEFAULT_TOP_K,
    embedding_model = config.DEFAULT_EMBEDDING_MODEL
).initialize()


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


@app.post("/keyword_search")
async def keyword_search(request: SearchRequest):
    """
    Performs keyword-based search on PDF documents.
    Returns the most relevant results based on exact word/phrase matches.
    Ideal for finding specific terms, definitions, or exact phrases in documents.
    """
    try:
        results = rag_chain.search_keyword(request.query, request.top_k)
        return format_search_results(results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/semantic_search")
async def semantic_search(request: SearchRequest):
    """
    Performs semantic search on PDF documents.
    Finds content semantically similar to the query, delivering relevant information even without exact word matches.
    Best for conceptual questions, understanding themes, or when you need information related to a topic.
    """
    try:
        results = rag_chain.search_semantic(request.query, request.top_k)
        return format_search_results(results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/hybrid_search")
async def hybrid_search(request: SearchRequest):
    """
    Performs hybrid search (keyword + semantic) on PDF documents.
    Combines exact keyword matching and semantic similarity to deliver optimal results.
    The most versatile search option for general questions or when unsure which search type is best.
    """
    try:
        results = rag_chain.search_hybrid(request.query, request.top_k)
        return format_search_results(results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def format_search_results(docs: List[Document]) -> str:
    """
    Format search results as markdown.
    
    Args:
        docs: List of documents to format
        
    Returns:
        Markdown formatted search results

    """

    if not docs:
        return "No relevant information found."
    
    markdown_results = "## Search Results\n\n"
    
    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get("source", "Unknown source")
        page = doc.metadata.get("page", None)
        page_info = f" (Page: {page+1})" if page is not None else ""
        
        markdown_results += f"### Result {i}{page_info}\n\n"
        markdown_results += f"{doc.page_content}\n\n"
        markdown_results += f"Source: {source}\n\n"
        markdown_results += "---\n\n"
    
    return markdown_results
