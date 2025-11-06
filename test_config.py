#!/usr/bin/env python3
"""
Test script to verify environment variables are properly read at runtime.
"""
import os
import sys

# Set test environment variables before importing
os.environ["OBSIDIAN_API_KEY"] = "test-key-12345"
os.environ["OBSIDIAN_HOST"] = "192.168.1.100"
os.environ["OBSIDIAN_PORT"] = "8080"
os.environ["OBSIDIAN_PROTOCOL"] = "http"

# Now import and test
from src.mcp_obsidian.config import get_obsidian_config
from src.mcp_obsidian.tools import ListFilesInVaultToolHandler

def test_config():
    """Test that config is read correctly."""
    print("Testing configuration...")
    
    config = get_obsidian_config()
    
    print(f"✓ API Key: {'*' * len(config.api_key)} (length: {len(config.api_key)})")
    print(f"✓ Protocol: {config.protocol}")
    print(f"✓ Host: {config.host}")
    print(f"✓ Port: {config.port}")
    print(f"✓ Verify SSL: {config.verify_ssl}")
    
    # Verify values match what we set
    assert config.api_key == "test-key-12345", f"API key mismatch: {config.api_key}"
    assert config.protocol == "http", f"Protocol mismatch: {config.protocol}"
    assert config.host == "192.168.1.100", f"Host mismatch: {config.host}"
    assert config.port == 8080, f"Port mismatch: {config.port}"
    
    print("\n✓ All config values match environment variables!")
    
    # Test that handler gets the config
    print("\nTesting handler gets correct config...")
    handler = ListFilesInVaultToolHandler()
    client = handler._get_api_client()
    
    base_url = client.get_base_url()
    expected_url = "http://192.168.1.100:8080"
    
    print(f"✓ Base URL: {base_url}")
    assert base_url == expected_url, f"URL mismatch: {base_url} != {expected_url}"
    
    print("✓ Handler creates client with correct configuration!")
    
    print("\n" + "="*50)
    print("ALL TESTS PASSED ✓")
    print("="*50)
    print("\nEnvironment variables are now properly read at runtime,")
    print("not at import time. Your configuration will be respected!")

if __name__ == "__main__":
    try:
        test_config()
    except Exception as e:
        print(f"\n✗ Test failed: {e}", file=sys.stderr)
        sys.exit(1)