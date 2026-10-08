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

import hashlib
import logging

_logger = logging.getLogger("integra.env_loader")

def _fp(val: str) -> str:
    if not val:
        return "NONE"
    return hashlib.sha256(val.strip().encode()).hexdigest()[:8]

# Canonical Model Architecture & Thinking Budget Specifications
# Sourced from env_file_map.env & Modelsthinkuingbudget.yml
CANONICAL_MODELS = {
    "cheshire_cat": {
        "model": "gemini-3.8-flash",
        "role": "Thalamic Arbitrator, Fast Routing, & Paradox Detection",
    },
    "left_hemisphere": {
        "model": "gemini-3.1-pro-preview",
        "role": "Analytical Engine (Spock) / Deconstruction & Formal Verification",
        "deep_think": True,
        "extended_thinking": True,
        "thinking_budget": 8192,
    },
    "right_hemisphere": {
        "model": "claude-opus-5-5",
        "role": "Synthetic Engine (Kirk) / Emergence & Generative Fusion",
    },
}

DEFAULT_ENV_VARS = {
    "CHESHIRE_MODEL": "gemini-3.8-flash",
    "Y789_MODEL": "gemini-3.1-pro-preview",
    "NEXUS_MODEL": "claude-opus-5-5",
    "SHIVA_MODEL": "claude-sonnet-5-5",
    "RODIN_MODEL": "gemini-3.8-flash",
    "THINKING_BUDGET": "8192",
}


def load_integra_env(base_dir: Optional[str] = None) -> Dict[str, str]:
    """
    Loads API keys and model configurations from integra-homebase .env files into os.environ.
    
    Precedence order:
    1. OS environment variables (highest priority, preserved if already set)
    2. .env (authoritative master file)
    3. env_file_map.env & specialized fallback files (.env overrides these)
    """
    if base_dir is None:
        base_dir = str(Path(__file__).parent.parent)
    
    # Auxiliary files loaded first as fallbacks, then .env loaded last as authoritative master
    aux_files = [
        ("Git_personal_access.env", None),
        ("FIRECRAWLapi.env", None),
        ("FIRECRAWL_API_KEY.env", "FIRECRAWL_API_KEY"),
        ("chromakey.env", None),
        ("CHROMA_API_KEY.env", "CHROMA_API_KEY"),
        ("claudehemisphere.env", "CLAUDE_API_KEY"),
        ("geminihemisphere.env", "GEMINI_API_KEY"),
        ("CLAUDE_API_KEY.env", "CLAUDE_API_KEY"),
        ("GEMINI_API_KEY.env", "GEMINI_API_KEY"),
        ("env_file_map.env", None),
        (".env", None),  # Authoritative master — loads LAST to override stale auxiliary files
    ]
    
    loaded = {}
    
    for filename, env_var in aux_files:
        filepath = os.path.join(base_dir, filename)
        if not os.path.exists(filepath):
            continue
            
        try:
            with open(filepath, "r", encoding="utf-8-sig", errors="replace") as f:
                content = f.read().strip()
            
            if not content:
                continue
                
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
                            # Log fingerprint warning if overriding an existing value with a different key
                            existing = os.environ.get(key)
                            if existing and existing != value:
                                _logger.info(
                                    f"env_loader: Overriding {key} from {filename} "
                                    f"(prior_fp={_fp(existing)}, new_fp={_fp(value)})"
                                )
                            os.environ[key] = value
                            loaded[key] = f"from {filename}"
            elif env_var:
                existing = os.environ.get(env_var)
                if existing and existing != content:
                    _logger.info(
                        f"env_loader: Overriding {env_var} from {filename} "
                        f"(prior_fp={_fp(existing)}, new_fp={_fp(content)})"
                    )
                os.environ[env_var] = content
                loaded[env_var] = f"from {filename} (bare format)"
                
        except Exception as e:
            _logger.warning(f"env_loader: Error reading {filename}: {e}")

    # Ensure canonical defaults are present if not set
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
