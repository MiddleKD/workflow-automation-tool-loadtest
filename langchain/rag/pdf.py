import os
from typing import Any, List

from config import DEFAULT_CHUNK_OVERLAP, DEFAULT_CHUNK_SIZE
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_community.vectorstores import Qdrant
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from rag.base import RetrievalChain


class PDFRetrievalChain(RetrievalChain):
    """
    PDF-specific implementation of the RetrievalChain.

    This class specializes in loading, splitting, and indexing PDF documents
    for retrieval.
    """

    def __init__(self, source_uri: List[str], **kwargs) -> None:
        """
        Initialize a PDF retrieval chain.

        Args:
            source_uri: List of PDF file paths
            **kwargs: Additional keyword arguments for the base RetrievalChain
        """

        super().__init__(source_uri=source_uri, **kwargs)

    def load_documents(self, source_uris: List[str]) -> List[Document]:
        """
        Load PDF documents from file paths.

        Args:
            source_uris: List of PDF file paths

        Returns:
            List of loaded documents
        """

        docs = []
        for source_uri in source_uris:
            if not os.path.exists(source_uri):
                print(f"File not found: {source_uri}")
                continue

            print(f"Loading PDF: {source_uri}")
            loader = PDFPlumberLoader(source_uri)
            docs.extend(loader.load())

        return docs

    def create_text_splitter(self) -> RecursiveCharacterTextSplitter:
        """
        Create a text splitter optimized for PDF documents.

        Returns:
            A text splitter instance suitable for PDFs
        """

        return RecursiveCharacterTextSplitter(
            chunk_size=DEFAULT_CHUNK_SIZE, chunk_overlap=DEFAULT_CHUNK_OVERLAP
        )

    def create_vectorstore(self, split_docs: List[Document]) -> Any:
        """
        Create a vector store from split PDF documents using Qdrant.

        Args:
            split_docs: Split document chunks

        Returns:
            A vector store instance

        Raises:
            ValueError: If there are no split documents
        """

        if not split_docs:
            raise ValueError("No split documents available.")

        # Qdrant 설정 (필요에 따라 값 수정)
        qdrant_host = "localhost"
        qdrant_port = 6333
        collection_name = "pdf_docs"

        client = QdrantClient(host=qdrant_host, port=qdrant_port)

        print("Creating/loading Qdrant vector store...")

        vectorstore = Qdrant.from_documents(
            documents=split_docs,
            embedding=self.create_embedding(),
            url=f"http://{qdrant_host}:{qdrant_port}",
            collection_name=collection_name,
            prefer_grpc=False,
        )

        return vectorstore
