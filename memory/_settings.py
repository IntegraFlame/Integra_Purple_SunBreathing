"""
INTEGRA O/S: MONGODB TOOL SETTINGS FOR PHOENIX-RODIN VECTOR & HYBRID SEARCH
Module: memory/_settings.py
Layer: 3 (The Memory — Document & Vector Manifold Settings)
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class MongoDbToolSettings:
    """Configuration settings for PhoenixRodin MongoDB vector and hybrid search."""

    default_limit: int = 10
    max_results: int = 50
    default_num_candidates: int = 100
    default_vector_index_name: str = "integra_hoard_vector_idx"
    default_search_index_name: str = "integra_hoard_text_idx"
    default_embedding_field: str = "embedding_768d"
    vertex_ai_embedding_model_name: str = "gemini-embedding-2"
    vertex_ai_embedding_output_dimensionality: Optional[int] = 768
    timeout_ms: int = 5000
    database_name: str = "integra_os_metatron"


DEFAULT_MONGODB_TOOL_SETTINGS = MongoDbToolSettings()
