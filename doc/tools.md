# Tools
This catalog documents each MCP tool, its handler, inputs, and the Obsidian REST endpoint it calls.
Tool discovery is exposed by [list_tools()](src/mcp_obsidian/server.py:59); dispatch is handled by [call_tool()](src/mcp_obsidian/server.py:65).

## Conventions
- Handler class link points to its definition in [src/mcp_obsidian/tools.py](src/mcp_obsidian/tools.py).
- Client method link points to the HTTP wrapper in [src/mcp_obsidian/obsidian.py](src/mcp_obsidian/obsidian.py).
- Endpoints are relative to the plugin base; see [get_base_url()](src/mcp_obsidian/obsidian.py:27).

```mermaid
flowchart LR
Tool[Tool handler] --> Client[HTTP client]
Client --> API[Local REST API]
API --> Vault[Vault]
```

## obsidian_list_files_in_vault
- Handler: [ListFilesInVaultToolHandler](src/mcp_obsidian/tools.py:31) using [run_tool()](src/mcp_obsidian/tools.py:46).
- Client: [list_files_in_vault()](src/mcp_obsidian/obsidian.py:47) → GET `/vault/`.
- Input: none.
- Returns: JSON array of names wrapped in MCP TextContent.

## obsidian_list_files_in_dir
- Handler: [ListFilesInDirToolHandler](src/mcp_obsidian/tools.py:58) using [run_tool()](src/mcp_obsidian/tools.py:78).
- Client: [list_files_in_dir()](src/mcp_obsidian/obsidian.py:59) → GET `/vault/{dir}/`.
- Input: `dirpath` string.
- Returns: JSON array of entries.

## obsidian_get_file_contents
- Handler: [GetFileContentsToolHandler](src/mcp_obsidian/tools.py:94) using [run_tool()](src/mcp_obsidian/tools.py:115).
- Client: [get_file_contents()](src/mcp_obsidian/obsidian.py:70) → GET `/vault/{filepath}`.
- Input: `filepath` string.
- Returns: Markdown text.

## obsidian_simple_search
- Handler: [SearchToolHandler](src/mcp_obsidian/tools.py:130) using [run_tool()](src/mcp_obsidian/tools.py:156).
- Client: [search()](src/mcp_obsidian/obsidian.py:102) → POST `/search/simple/` with query and contextLength params.
- Input: `query` string, optional `context_length` integer.
- Returns: JSON results with matches and context.

## obsidian_complex_search
- Handler: [ComplexSearchToolHandler](src/mcp_obsidian/tools.py:373) using [run_tool()](src/mcp_obsidian/tools.py:423).
- Client: [search_json()](src/mcp_obsidian/obsidian.py:183) → POST `/search/` with Content-Type `application/vnd.olrapi.jsonlogic+json`.
- Input: `query` object (JsonLogic).
- Returns: JSON array of matches.

## obsidian_append_content
- Handler: [AppendContentToolHandler](src/mcp_obsidian/tools.py:192) using [run_tool()](src/mcp_obsidian/tools.py:217).
- Client: [append_content()](src/mcp_obsidian/obsidian.py:116) → POST `/vault/{filepath}` with `text/markdown` body.
- Input: `filepath` string; `content` markdown.
- Returns: success message.

## obsidian_patch_content
- Handler: [PatchContentToolHandler](src/mcp_obsidian/tools.py:231) using [run_tool()](src/mcp_obsidian/tools.py:270).
- Client: [patch_content()](src/mcp_obsidian/obsidian.py:132) → PATCH `/vault/{filepath}` with headers `Operation`, `Target-Type`, `Target`.
- Input: `filepath`, `operation` one of append/prepend/replace, `target_type` heading/block/frontmatter, `target`, `content`.
- Returns: success message.

## obsidian_put_content
- Handler: [PutContentToolHandler](src/mcp_obsidian/tools.py:290) using [run_tool()](src/mcp_obsidian/tools.py:315).
- Client: [put_content()](src/mcp_obsidian/obsidian.py:149) → PUT `/vault/{filepath}` with `text/markdown` body.
- Input: `filepath` string; `content` markdown.
- Returns: success message.

## obsidian_delete_file
- Handler: [DeleteFileToolHandler](src/mcp_obsidian/tools.py:330) using [run_tool()](src/mcp_obsidian/tools.py:356).
- Client: [delete_file()](src/mcp_obsidian/obsidian.py:165) → DELETE `/vault/{filepath}`.
- Input: `filepath` string; `confirm` boolean must be true.
- Returns: success message.

## obsidian_batch_get_file_contents
- Handler: [BatchGetFileContentsToolHandler](src/mcp_obsidian/tools.py:437) using [run_tool()](src/mcp_obsidian/tools.py:462).
- Client: [get_batch_file_contents()](src/mcp_obsidian/obsidian.py:81) which loops [get_file_contents()](src/mcp_obsidian/obsidian.py:70).
- Input: `filepaths` array of strings.
- Returns: Concatenated content with per-file headers.

## obsidian_get_periodic_note
- Handler: [PeriodicNotesToolHandler](src/mcp_obsidian/tools.py:476) using [run_tool()](src/mcp_obsidian/tools.py:503).
- Client: [get_periodic_note()](src/mcp_obsidian/obsidian.py:197) → GET `/periodic/{period}/`, optional `Accept: application/vnd.olrapi.note+json`.
- Input: `period` enum daily|weekly|monthly|quarterly|yearly; optional `type` content|metadata.
- Returns: Markdown content or JSON metadata depending on `type`.

## obsidian_get_recent_periodic_notes
- Handler: [RecentPeriodicNotesToolHandler](src/mcp_obsidian/tools.py:527) using [run_tool()](src/mcp_obsidian/tools.py:560).
- Client: [get_recent_periodic_notes()](src/mcp_obsidian/obsidian.py:222) → GET `/periodic/{period}/recent` with params `limit` and `includeContent`.
- Input: `period` enum; `limit` int; `include_content` bool.
- Returns: JSON array of notes; may include content when requested.
- Note: This endpoint may not appear in the bundled [openapi.yaml](openapi.yaml); it is supported by the plugin at runtime.

## obsidian_get_recent_changes
- Handler: [RecentChangesToolHandler](src/mcp_obsidian/tools.py:587) using [run_tool()](src/mcp_obsidian/tools.py:615).
- Client: [get_recent_changes()](src/mcp_obsidian/obsidian.py:253) which posts a Dataview DQL TABLE to `/search/` with Content-Type `application/vnd.olrapi.dataview.dql+txt`.
- Input: `limit` int; `days` int.
- Returns: JSON rows with file and modification time.

## Error and Validation Behavior
- Server wraps handler exceptions in [call_tool()](src/mcp_obsidian/server.py:65) logging then raising RuntimeError; client normalizes HTTP errors in [_safe_call()](src/mcp_obsidian/obsidian.py:36).
- Handlers validate required inputs explicitly; see examples like [SearchToolHandler.run_tool()](src/mcp_obsidian/tools.py:156).