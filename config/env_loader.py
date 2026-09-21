"""
INTEGRA O/S: Environment Variable & Model Architecture Loader
Loads API keys, bicameral model routing, and thinking budget configurations
from .env files, env_file_map.env, and model specifications into os.environ.

CRITICAL: This module must be imported BEFORE any API client instantiation.
Supports standard KEY=VALUE format, bare key format, and models specification.

Security: NEVER log, print, or commit API key values.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional

# Canonical Model Architecture & Thinking Budget Specifications
# Sourced from env_file_map.env & Modelsthinkuingbudget.yml
CANONICAL_MODELS = {
    "cheshire_cat": {
        "model": "gemini-3.8-flash",
        "role": "Thalamic Arbitrator, Fast Routing, & Paradox Detection",
    },
    "left_hemisphere": {
        "model": "gemini-3.1-pro",
        "role": "Analytical Engine (Spock) / Deconstruction & Formal Verification",
        "deep_think": True,
        "extended_thinking": True,
        "thinking_budget": 8192,
    },
    "right_hemisphere": {
        "model": "claude-sonnet-4-6",
        "role": "Synthetic Engine (Kirk) / Emergence & Generative Fusion",
    },
}

DEFAULT_ENV_VARS = {
    "CHESHIRE_MODEL": "gemini-3.8-flash",
    "Y789_MODEL": "gemini-3.1-pro",
    "NEXUS_MODEL": "claude-sonnet-4-6",
    "THINKING_BUDGET": "8192",
}


def load_integra_env(base_dir: Optional[str] = None) -> Dict[str, str]:
    """
    Loads API keys and model configurations from integra-homebase .env files into os.environ.
    
    Supports formats:
    1. Standard dotenv: KEY=VALUE (supports comments, quoted strings, inline declarations)
    2. Bare key: raw_key_value (single line, mapped to the env var based on filename)
    3. Master map: env_file_map.env (loads all mapped keys and routing identifiers)
    
    File mapping order:
    - .env: Base master KEY=VALUE file
    - env_file_map.env: Consolidated environment variable and routing map
    - Specialized .env files (override with dedicated keys)
    """
    if base_dir is None:
        base_dir = str(Path(__file__).parent.parent)
    
    env_file_map = {
        ".env": None,                            # KEY=VALUE master — loads ALL vars FIRST
        "env_file_map.env": None,                # KEY=VALUE master map reference
        "GEMINI_API_KEY.env": "GEMINI_API_KEY",  # bare or KEY=VALUE format
        "CLAUDE_API_KEY.env": "CLAUDE_API_KEY",  # bare or KEY=VALUE format
        "geminihemisphere.env": "GEMINI_API_KEY",
        "claudehemisphere.env": "CLAUDE_API_KEY",
        "CHROMA_API_KEY.env": "CHROMA_API_KEY",  # loads CHROMA_API_KEY
        "chromakey.env": None,                   # KEY=VALUE — loads CHROMA_API_KEY
        "FIRECRAWL_API_KEY.env": "FIRECRAWL_API_KEY", # loads FIRECRAWL_API_KEY
        "FIRECRAWLapi.env": None,                # KEY=VALUE — loads FIRECRAWL_API_KEY
        "Git_personal_access.env": None,         # KEY=VALUE — loads Git_personal_access
    }
    
    loaded = {}
    
    for filename, env_var in env_file_map.items():
        filepath = os.path.join(base_dir, filename)
        if not os.path.exists(filepath):
            continue
            
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read().strip()
            
            if not content:
                continue
                
            # Check if it's KEY=VALUE format (ignoring initial comments)
            first_non_comment = next((line.strip() for line in content.split("\n") if line.strip() and not line.strip().startswith("#")), "")
            if "=" in first_non_comment:
                for line in content.split("\n"):
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" in line:
                        key, _, value = line.partition("=")
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")
                        if key and value:
                            os.environ[key] = value
                            loaded[key] = f"from {filename}"
            elif env_var:
                # Bare key format (just the raw key on a single line)
                os.environ[env_var] = content
                loaded[env_var] = f"from {filename} (bare format)"
                
        except Exception:
            pass  # Silently skip unreadable files

    # Ensure canonical defaults from env_file_map.env are present in os.environ
    for def_key, def_val in DEFAULT_ENV_VARS.items():
        if def_key not in os.environ:
            os.environ[def_key] = def_val
            loaded[def_key] = "from defaults"
    
    return loaded


def get_model_config(role: Optional[str] = None) -> Dict[str, Any]:
    """
    Returns the bicameral model configuration and thinking budget, dynamically
    grounded with any runtime environment variable overrides.
    
    Roles:
    - 'cheshire_cat': Thalamic Arbitrator & Fast Router
    - 'left_hemisphere': Analytical Engine / Deconstruction & Formal Verification
    - 'right_hemisphere': Synthetic Engine / Emergence & Generative Fusion
    """
    config = {
        "cheshire_cat": {
            "model": os.environ.get("CHESHIRE_MODEL", CANONICAL_MODELS["cheshire_cat"]["model"]),
            "role": CANONICAL_MODELS["cheshire_cat"]["role"],
        },
        "left_hemisphere": {
            "model": os.environ.get("Y789_MODEL", CANONICAL_MODELS["left_hemisphere"]["model"]),
            "role": CANONICAL_MODELS["left_hemisphere"]["role"],
            "deep_think": CANONICAL_MODELS["left_hemisphere"]["deep_think"],
            "extended_thinking": CANONICAL_MODELS["left_hemisphere"]["extended_thinking"],
            "thinking_budget": int(os.environ.get("THINKING_BUDGET", CANONICAL_MODELS["left_hemisphere"]["thinking_budget"])),
        },
        "right_hemisphere": {
            "model": os.environ.get("NEXUS_MODEL", CANONICAL_MODELS["right_hemisphere"]["model"]),
            "role": CANONICAL_MODELS["right_hemisphere"]["role"],
        },
    }
    
    if role:
        return config.get(role, {})
    return config


def verify_env() -> Dict[str, bool]:
    """
    Audits the current environment without leaking sensitive keys.
    Returns a dict mapping key names to boolean presence status.
    """
    critical_keys = [
        "GEMINI_API_KEY",
        "CLAUDE_API_KEY",
        "CHESHIRE_MODEL",
        "Y789_MODEL",
        "NEXUS_MODEL",
        "THINKING_BUDGET",
        "FIRECRAWL_API_KEY",
        "CHROMA_API_KEY",
        "Git_personal_access",
    ]
    return {k: (bool(os.environ.get(k)) and "YOUR_" not in os.environ.get(k, "")) for k in critical_keys}


# Auto-load on import
_loaded = load_integra_env()
