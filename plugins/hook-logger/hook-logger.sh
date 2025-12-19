#!/bin/bash
set -euo pipefail

# ============================================================================
# Hook Logger - Logs all Claude Code hook invocations to JSON file
# ============================================================================

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOGS_DIR="${SCRIPT_DIR}/logs"
LOG_FILE="${LOGS_DIR}/hooks.json"
LOCK_FILE="/tmp/claude-hook-logger-${USER}.lock"
MAX_ENTRIES=1000

# Ensure logs directory exists
mkdir -p "$LOGS_DIR"

# Check for jq dependency
if ! command -v jq >/dev/null 2>&1; then
    echo "Warning: jq not installed, hook logging disabled" >&2
    echo "Install jq to enable hook logging: brew install jq (macOS) or apt-get install jq (Linux)" >&2
    exit 0  # Exit successfully to not block Claude Code
fi

# ============================================================================
# Test Mode - For manual testing
# ============================================================================
test_mode() {
    echo "=== Hook Logger Test Mode ==="
    echo "Log file: $LOG_FILE"

    if [ -f "$LOG_FILE" ]; then
        echo "Current entries: $(wc -l < "$LOG_FILE" 2>/dev/null || echo "0")"
    else
        echo "Log file does not exist yet"
    fi

    echo ""
    echo "Creating test event..."

    # Create test event
    TEST_EVENT='{"hook_event_name":"Test","session_id":"test-session","message":"Manual test invocation"}'
    echo "$TEST_EVENT" | "$0"

    echo ""
    echo "Test event logged successfully!"
    echo ""
    echo "Latest 3 entries:"
    tail -n 3 "$LOG_FILE" 2>/dev/null | jq '.' || echo "No entries yet"

    exit 0
}

# Check for test mode
if [ "${1:-}" = "test" ]; then
    test_mode
fi

# ============================================================================
# Main Logging Logic
# ============================================================================

# Read event data from stdin
if [ -t 0 ]; then
    echo "Error: This script must be called by Claude Code hooks (reads from stdin)" >&2
    echo "For testing, use: $0 test" >&2
    exit 0  # Exit successfully to not block Claude Code
fi

EVENT_DATA=$(cat)

# Validate we got data
if [ -z "$EVENT_DATA" ]; then
    exit 0  # No data, exit silently
fi

# Add timestamp to event data
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS date format
    TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
else
    # Linux date format
    TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%S%z")
fi

TIMESTAMPED_EVENT=$(echo "$EVENT_DATA" | jq -c --arg ts "$TIMESTAMP" '. + {timestamp: $ts}' 2>/dev/null || echo "$EVENT_DATA")

# ============================================================================
# File Locking - Ensure atomic operations
# ============================================================================

# Acquire exclusive lock (cross-platform approach)
acquire_lock() {
    local max_wait=5
    local elapsed=0

    # Try to create lock file atomically
    while ! mkdir "$LOCK_FILE" 2>/dev/null; do
        sleep 0.1
        elapsed=$((elapsed + 1))

        # Timeout after 5 seconds (50 iterations * 0.1s)
        if [ $elapsed -ge 50 ]; then
            return 1
        fi

        # Clean up stale locks (older than 10 seconds)
        if [ -d "$LOCK_FILE" ]; then
            if [[ "$OSTYPE" == "darwin"* ]]; then
                # macOS
                lock_age=$(( $(date +%s) - $(stat -f %m "$LOCK_FILE" 2>/dev/null || echo 0) ))
            else
                # Linux
                lock_age=$(( $(date +%s) - $(stat -c %Y "$LOCK_FILE" 2>/dev/null || echo 0) ))
            fi

            if [ $lock_age -gt 10 ]; then
                rmdir "$LOCK_FILE" 2>/dev/null || true
            fi
        fi
    done

    return 0
}

# Release lock on exit
cleanup_lock() {
    rmdir "$LOCK_FILE" 2>/dev/null || true
}

trap cleanup_lock EXIT

# Acquire the lock
if ! acquire_lock; then
    # Could not acquire lock, exit silently
    exit 0
fi

# ============================================================================
# Log File Operations
# ============================================================================

# Initialize log file if it doesn't exist
if [ ! -f "$LOG_FILE" ]; then
    touch "$LOG_FILE"
fi

# Append the timestamped event as a single line (NDJSON format)
echo "$TIMESTAMPED_EVENT" >> "$LOG_FILE"

# Rotate log file if it exceeds MAX_ENTRIES
# Keep only the last MAX_ENTRIES lines
LINE_COUNT=$(wc -l < "$LOG_FILE" 2>/dev/null || echo "0")
if [ "$LINE_COUNT" -gt "$MAX_ENTRIES" ]; then
    # Keep only the last MAX_ENTRIES lines
    TEMP_FILE="${LOG_FILE}.tmp.$$"
    tail -n "$MAX_ENTRIES" "$LOG_FILE" > "$TEMP_FILE"
    mv "$TEMP_FILE" "$LOG_FILE"
fi

# Lock automatically released on script exit
exit 0
