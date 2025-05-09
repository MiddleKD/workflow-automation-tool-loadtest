from pathlib import Path

# Path settings
DATA_DIR = Path(__file__).parent.parent / "pdfs"

# Default settings
DEFAULT_CHUNK_SIZE = 600
DEFAULT_CHUNK_OVERLAP = 50
DEFAULT_TOP_K = 5
DEFAULT_EMBEDDING_MODEL = "llama3.1:latest"
DEFAULT_LLM = "llama3.1:latest"
