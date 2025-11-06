# Testing and Publishing Guide

This guide explains how to test and publish your enhanced fork of mcp-obsidian.

## Testing Your Changes

### 1. Test Runtime Configuration

Run the included configuration test:

```bash
uv run python test_config.py
```

Expected output:
```
INFO:mcp-obsidian:Obsidian API configured: http://192.168.1.100:8080
Testing configuration...
✓ API Key: ************** (length: 14)
✓ Protocol: http
✓ Host: 192.168.1.100
✓ Port: 8080
✓ Verify SSL: False

✓ All config values match environment variables!
...
ALL TESTS PASSED ✓
```

### 2. Test with MCP Inspector

Test with custom configuration to verify environment variables work:

```bash
OBSIDIAN_API_KEY=your-key-here \
OBSIDIAN_HOST=192.168.1.100 \
OBSIDIAN_PORT=27124 \
OBSIDIAN_PROTOCOL=http \
npx @modelcontextprotocol/inspector uv --directory /path/to/mcp-obsidian run mcp-obsidian
```

Check the startup log shows your custom configuration:
```
INFO:mcp-obsidian:Obsidian API configured: http://192.168.1.100:27124
```

### 3. Test with Claude Desktop

1. Update your Claude Desktop config:

**MacOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "mcp-obsidian": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/your/mcp-obsidian",
        "run",
        "mcp-obsidian"
      ],
      "env": {
        "OBSIDIAN_API_KEY": "your-api-key",
        "OBSIDIAN_HOST": "192.168.1.100",
        "OBSIDIAN_PORT": "27124"
      }
    }
  }
}
```

2. Restart Claude Desktop

3. Test by asking Claude to list files in your vault

4. Check logs to verify configuration:
```bash
tail -f ~/Library/Logs/Claude/mcp-server-mcp-obsidian.log
```

## Publishing to PyPI

### Prerequisites

1. Create a PyPI account: https://pypi.org/account/register/
2. Generate an API token: https://pypi.org/manage/account/token/
3. Save your token securely

### Option 1: Publish Under a New Name (Recommended for Forks)

If you want to publish this as a separate package:

1. Update `pyproject.toml`:
```toml
[project]
name = "mcp-obsidian-enhanced"  # or your preferred name
version = "0.2.2"
```

2. Build and publish:
```bash
uv build
uv publish --username __token__ --password <your-pypi-token>
```

3. Users can then install with:
```bash
uvx mcp-obsidian-enhanced
```

### Option 2: Contribute Back to Original

If you want to merge this into the original project:

1. Create a Pull Request to the upstream repository
2. Wait for maintainer review
3. They can publish a new version once merged

### Testing the Build Locally

Before publishing, test the built package:

```bash
# Build the package
uv build

# Test installation from the wheel file
uvx --from dist/mcp_obsidian-0.2.2-py3-none-any.whl mcp-obsidian

# Or test in a clean environment
uv run --with ./dist/mcp_obsidian-0.2.2-py3-none-any.whl mcp-obsidian
```

## Version Management

Follow semantic versioning:

- **Patch** (0.2.2 → 0.2.3): Bug fixes, no API changes
- **Minor** (0.2.2 → 0.3.0): New features, backward compatible
- **Major** (0.2.2 → 1.0.0): Breaking changes

Update version in `pyproject.toml` before each release.

## Publishing Checklist

- [ ] All tests pass (`uv run python test_config.py`)
- [ ] Documentation updated (README.md, doc/)
- [ ] Version bumped in pyproject.toml
- [ ] Changes committed and pushed to GitHub
- [ ] Package builds successfully (`uv build`)
- [ ] Tested locally with built package
- [ ] Published to PyPI (`uv publish`)
- [ ] GitHub release created with changelog
- [ ] Tested installation from PyPI (`uvx mcp-obsidian-enhanced`)

## Troubleshooting

### Build Fails

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Rebuild
uv build
```

### Publish Fails

```bash
# Check package validity
uv build --check

# Try with verbose output
uv publish --verbose
```

### Installation Issues

```bash
# Clear uv cache
uv cache clean

# Try installing again
uvx mcp-obsidian-enhanced
```

## Additional Resources

- [Python Packaging Guide](https://packaging.python.org/)
- [PyPI Publishing Guide](https://packaging.python.org/tutorials/packaging-projects/)
- [UV Documentation](https://docs.astral.sh/uv/)
- [MCP Documentation](https://modelcontextprotocol.io/)