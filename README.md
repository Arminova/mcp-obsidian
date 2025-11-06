# MCP server for Obsidian (Enhanced Fork)

MCP server to interact with Obsidian via the Local REST API community plugin.

**This is an enhanced fork of the original [mcp-obsidian](https://github.com/modelcontextprotocol/servers/tree/main/src/obsidian) with runtime environment variable support.**

## What's New in This Fork

✨ **Fixed Runtime Configuration**: Environment variables (`OBSIDIAN_HOST`, `OBSIDIAN_PORT`, `OBSIDIAN_PROTOCOL`) are now properly read at runtime, allowing you to connect to non-local Obsidian instances.

The original implementation captured environment variables at module import time, causing MCP client configurations to be ignored. This fork reads configuration when tools are called, ensuring your settings are respected.

<a href="https://glama.ai/mcp/servers/3wko1bhuek"><img width="380" height="200" src="https://glama.ai/mcp/servers/3wko1bhuek/badge" alt="server for Obsidian MCP server" /></a>

## Components

### Tools

The server implements multiple tools to interact with Obsidian:

- list_files_in_vault: Lists all files and directories in the root directory of your Obsidian vault
- list_files_in_dir: Lists all files and directories in a specific Obsidian directory
- get_file_contents: Return the content of a single file in your vault.
- search: Search for documents matching a specified text query across all files in the vault
- patch_content: Insert content into an existing note relative to a heading, block reference, or frontmatter field.
- append_content: Append content to a new or existing file in the vault.
- delete_file: Delete a file or directory from your vault.

### Example prompts

Its good to first instruct Claude to use Obsidian. Then it will always call the tool.

The use prompts like this:
- Get the contents of the last architecture call note and summarize them
- Search for all files where Azure CosmosDb is mentioned and quickly explain to me the context in which it is mentioned
- Summarize the last meeting notes and put them into a new note 'summary meeting.md'. Add an introduction so that I can send it via email.

## Configuration

### Obsidian REST API Key

There are two ways to configure the environment with the Obsidian REST API Key. 

1. Add to server config (preferred)

```json
{
  "mcp-obsidian": {
    "command": "uvx",
    "args": [
      "mcp-obsidian"
    ],
    "env": {
      "OBSIDIAN_API_KEY": "<your_api_key_here>",
      "OBSIDIAN_HOST": "<your_obsidian_host>",
      "OBSIDIAN_PORT": "<your_obsidian_port>"
    }
  }
}
```
Sometimes Claude has issues detecting the location of uv / uvx. You can use `which uvx` to find and paste the full path in above config in such cases.

2. Create a `.env` file in the working directory with the following required variables:

```
OBSIDIAN_API_KEY=your_api_key_here
OBSIDIAN_HOST=your_obsidian_host
OBSIDIAN_PORT=your_obsidian_port
```

Note:
- You can find the API key in the Obsidian plugin config
- Default port is 27124 if not specified
- Default host is 127.0.0.1 if not specified

## Quickstart

### Install

#### Obsidian REST API

You need the Obsidian REST API community plugin running: https://github.com/coddingtonbear/obsidian-local-rest-api

Install and enable it in the settings and copy the api key.

#### Claude Desktop

On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`

On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

<details>
  <summary>Development/Unpublished Servers Configuration</summary>
  
```json
{
  "mcpServers": {
    "mcp-obsidian": {
      "command": "uv",
      "args": [
        "--directory",
        "<dir_to>/mcp-obsidian",
        "run",
        "mcp-obsidian"
      ],
      "env": {
        "OBSIDIAN_API_KEY": "<your_api_key_here>",
        "OBSIDIAN_HOST": "<your_obsidian_host>",
        "OBSIDIAN_PORT": "<your_obsidian_port>"
      }
    }
  }
}
```
</details>

<details>
  <summary>Published Servers Configuration</summary>
  
```json
{
  "mcpServers": {
    "mcp-obsidian": {
      "command": "uvx",
      "args": [
        "mcp-obsidian"
      ],
      "env": {
        "OBSIDIAN_API_KEY": "<YOUR_OBSIDIAN_API_KEY>",
        "OBSIDIAN_HOST": "<your_obsidian_host>",
        "OBSIDIAN_PORT": "<your_obsidian_port>"
      }
    }
  }
}
```
</details>

## Development

### Building

To prepare the package for distribution:

1. Sync dependencies and update lockfile:
```bash
uv sync
```

2. Build the package:
```bash
uv build
```

### Testing

#### Test Runtime Configuration

Run the included test to verify environment variables are read correctly:

```bash
uv run python test_config.py
```

This will verify that `OBSIDIAN_HOST`, `OBSIDIAN_PORT`, and `OBSIDIAN_PROTOCOL` are properly read at runtime.

#### Test with MCP Inspector

Test the server with custom configuration:

```bash
OBSIDIAN_HOST=192.168.1.100 OBSIDIAN_PORT=27124 \
npx @modelcontextprotocol/inspector uv --directory /path/to/mcp-obsidian run mcp-obsidian
```

The startup log should show:
```
INFO:mcp-obsidian:Obsidian API configured: http://192.168.1.100:27124
```

### Debugging

Since MCP servers run over stdio, debugging can be challenging. For the best debugging
experience, we strongly recommend using the [MCP Inspector](https://github.com/modelcontextprotocol/inspector).

You can launch the MCP Inspector via [`npm`](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) with this command:

```bash
npx @modelcontextprotocol/inspector uv --directory /path/to/mcp-obsidian run mcp-obsidian
```

Upon launching, the Inspector will display a URL that you can access in your browser to begin debugging.

You can also watch the server logs with this command:

```bash
tail -n 20 -f ~/Library/Logs/Claude/mcp-server-mcp-obsidian.log
```

## Publishing

### To PyPI

1. Build the package:
```bash
uv build
```

2. Publish to PyPI:
```bash
uv publish
```

You'll need PyPI credentials. Set them up with:
```bash
# Create a PyPI account at https://pypi.org/account/register/
# Generate an API token at https://pypi.org/manage/account/token/
# Then use:
uv publish --username __token__ --password <your-pypi-token>
```

### Testing Before Publishing

Test the built package locally:

```bash
# Install from local build
uvx --from dist/mcp_obsidian-*.whl mcp-obsidian

# Or test in a clean environment
uv run --with ./dist/mcp_obsidian-*.whl mcp-obsidian
```

### Version Bumping

Update the version in `pyproject.toml` before publishing:

```toml
[project]
version = "0.2.2"  # Increment for bug fixes
# or
version = "0.3.0"  # Increment for new features
```

## Contributing

This fork maintains compatibility with the original mcp-obsidian API while adding runtime configuration support. Contributions are welcome!

See [doc/](doc/) for detailed architecture documentation.
