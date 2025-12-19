# Hook Logger Plugin

A Claude Code plugin that logs all hook invocations to a JSON file with automatic rotation.

## Overview

This plugin captures every hook event that occurs in Claude Code and logs it to a structured JSON file. Perfect for debugging, monitoring, and understanding Claude Code's behavior during development.

## Features

- **Comprehensive Logging**: Captures all 9 hook event types:
  - PreToolUse (before tool execution)
  - PostToolUse (after tool execution)
  - UserPromptSubmit (when user submits prompt)
  - Stop (when agent stops)
  - SubagentStop (when subagent stops)
  - SessionStart (session begins)
  - SessionEnd (session ends)
  - PreCompact (before context compaction)
  - Notification (various notification types)

- **Pretty-Printed JSON**: Human-readable format for easy inspection
- **Automatic Rotation**: Keeps last 1000 entries to prevent unlimited growth
- **Thread-Safe**: Uses file locking for concurrent hook executions
- **Non-Blocking**: Logging failures won't interrupt Claude Code operations

## Installation

Install from the marketplace:

```Inside Claude Code console
# Add this marketplace to your Claude Code config (if not already added)

/plugin marketplace add sevii/agent-marketplace

# The hook-logger plugin will be available
```

Or install manually by copying this directory to your Claude Code plugins directory.

## Log Location

Logs are stored at:
```
plugins/hook-logger/logs/hooks.json
```

## Log File Format

The log file is a JSON object with the following structure:

```json
{
  "version": "1.0",
  "max_entries": 1000,
  "entries": [
    {
      "timestamp": "2025-12-19T14:30:45Z",
      "hook_event_name": "PreToolUse",
      "session_id": "abc123",
      "tool_name": "Read",
      "tool_input": {
        "file_path": "/path/to/file.txt"
      },
      "cwd": "/path/to/project",
      "permission_mode": "auto",
      "transcript_path": "/path/to/transcript"
    }
  ]
}
```

Each entry contains:
- `timestamp`: ISO-8601 formatted timestamp
- `hook_event_name`: Type of hook event
- Event-specific fields (tool_name, tool_input, notification_type, etc.)
- Common fields: session_id, cwd, permission_mode, transcript_path

## Viewing Logs

### View All Logs (Pretty-Printed)

```bash
jq '.' plugins/hook-logger/logs/hooks.json
```

### View Last 10 Entries

```bash
jq '.entries | .[-10:]' plugins/hook-logger/logs/hooks.json
```

### Filter by Event Type

```bash
# View only PreToolUse events
jq '.entries[] | select(.hook_event_name == "PreToolUse")' plugins/hook-logger/logs/hooks.json

# View only tool executions (Pre and Post)
jq '.entries[] | select(.hook_event_name | test("ToolUse"))' plugins/hook-logger/logs/hooks.json
```

### Filter by Tool Name

```bash
# View all Write tool invocations
jq '.entries[] | select(.tool_name == "Write")' plugins/hook-logger/logs/hooks.json
```

### Filter by Session

```bash
# View all events from a specific session
jq '.entries[] | select(.session_id == "your-session-id")' plugins/hook-logger/logs/hooks.json
```

### Count Events by Type

```bash
jq '.entries | group_by(.hook_event_name) | map({event: .[0].hook_event_name, count: length})' plugins/hook-logger/logs/hooks.json
```

### View Recent Activity

```bash
# Last 20 entries with just timestamp and event name
jq '.entries | .[-20:] | .[] | {timestamp, hook_event_name, tool_name}' plugins/hook-logger/logs/hooks.json
```

### Search for Specific Content

```bash
# Find events containing a specific file path
jq '.entries[] | select(.tool_input.file_path | contains("config"))' plugins/hook-logger/logs/hooks.json
```

## Configuration

The maximum number of entries can be adjusted by editing the script:

```bash
# Edit hook-logger.sh
# Change the MAX_ENTRIES variable:
MAX_ENTRIES=1000  # Change to desired value
```

After changing, restart Claude Code for the change to take effect.

## Testing

Test the plugin manually:

```bash
# Run built-in test
./plugins/hook-logger/hook-logger.sh test

# Simulate a hook event
echo '{"hook_event_name":"PreToolUse","session_id":"test","tool_name":"Read","tool_input":{"file_path":"/test"}}' | ./plugins/hook-logger/hook-logger.sh

# Verify the log was created
jq '.entries | .[-1]' plugins/hook-logger/logs/hooks.json
```

## Dependencies

- **jq**: Required for JSON manipulation and pretty-printing
  - macOS: `brew install jq`
  - Linux: `apt-get install jq` or `yum install jq`
  - If jq is not installed, the plugin will disable itself gracefully

## Performance

- **Typical duration**: 50-200ms per hook invocation
- **File size**: 1-5MB with 1000 entries (depends on payload sizes)
- **Impact**: Minimal - logging happens asynchronously and uses file locking to prevent contention

## Troubleshooting

### Logs not appearing

1. Check if jq is installed: `which jq`
2. Check if the script is executable: `ls -la plugins/hook-logger/hook-logger.sh`
3. Test manually: `./plugins/hook-logger/hook-logger.sh test`
4. Check for errors in Claude Code output

### Log file too large

Reduce MAX_ENTRIES in the script to keep fewer historical entries.

### Concurrent execution issues

The plugin uses flock for file locking. If you experience issues on systems without flock, the plugin will gracefully skip logging.

## How It Works

1. Claude Code triggers a hook event
2. The hook-logger.sh script receives event data via stdin
3. Script adds a timestamp to the event
4. Script acquires a file lock to ensure thread safety
5. Script reads the existing log file (or creates it if missing)
6. Script appends the new entry to the entries array
7. If entries exceed 1000, script keeps only the last 1000
8. Script writes the updated log back with pretty-printing
9. Script releases the lock and exits

## License

MIT

## Author

Nicholas Sledgianowski

## Contributing

Contributions welcome! Please submit issues and pull requests to the [agent-marketplace repository](https://github.com/sevii/agent-marketplace).
