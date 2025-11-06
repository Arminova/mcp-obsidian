import os
from typing import Optional
from dataclasses import dataclass

@dataclass
class ObsidianConfig:
    """Configuration for Obsidian API connection."""
    api_key: str
    protocol: str
    host: str
    port: int
    verify_ssl: bool

def get_obsidian_config() -> ObsidianConfig:
    """
    Load Obsidian configuration from environment variables at runtime.
    
    This ensures environment variables are read when the function is called,
    not at module import time, allowing proper configuration in different contexts.
    
    Returns:
        ObsidianConfig with all connection parameters
        
    Raises:
        ValueError: If OBSIDIAN_API_KEY is not set
    """
    api_key = os.getenv("OBSIDIAN_API_KEY")
    if not api_key:
        raise ValueError(
            f"OBSIDIAN_API_KEY environment variable required. "
            f"Working directory: {os.getcwd()}"
        )
    
    protocol = os.getenv("OBSIDIAN_PROTOCOL", "https").lower()
    if protocol not in ("http", "https"):
        protocol = "https"
    
    host = os.getenv("OBSIDIAN_HOST", "127.0.0.1")
    
    try:
        port = int(os.getenv("OBSIDIAN_PORT", "27124"))
    except ValueError:
        port = 27124
    
    # SSL verification disabled by default for self-signed local certs
    verify_ssl = os.getenv("OBSIDIAN_VERIFY_SSL", "false").lower() == "true"
    
    return ObsidianConfig(
        api_key=api_key,
        protocol=protocol,
        host=host,
        port=port,
        verify_ssl=verify_ssl
    )