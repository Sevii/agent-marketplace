#!/bin/bash

# Elevator Music Hook for Claude Code
# This script plays elevator music when Claude is idle and stops it when you interact

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOUNDS_DIR="${SCRIPT_DIR}/sounds"
MUSIC_FILE="${SOUNDS_DIR}/QuietFloors.mp3"
PID_DIR="/tmp/claude-elevator-music"

# Ensure PID directory exists
mkdir -p "$PID_DIR"

# Logging function (optional, disabled by default)
log() {
    # Uncomment to enable logging
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "${SCRIPT_DIR}/elevator-music.log"
}

# Detect available audio player
detect_audio_player() {
    if command -v ffplay >/dev/null 2>&1; then
        echo "ffplay"
    elif command -v mpv >/dev/null 2>&1; then
        echo "mpv"
    elif command -v afplay >/dev/null 2>&1; then
        echo "afplay"
    elif command -v paplay >/dev/null 2>&1; then
        echo "paplay"
    elif command -v cvlc >/dev/null 2>&1; then
        echo "cvlc"
    else
        echo "none"
    fi
}

# Start playing music
start_music() {
    local session_id="$1"
    local pid_file="${PID_DIR}/${session_id}.pid"

    # Check if already playing
    if [ -f "$pid_file" ]; then
        local existing_pid=$(cat "$pid_file")
        if kill -0 "$existing_pid" 2>/dev/null; then
            log "Music already playing for session $session_id (PID: $existing_pid)"
            return 0
        else
            # Stale PID file, remove it
            rm -f "$pid_file"
        fi
    fi

    local player=$(detect_audio_player)

    if [ "$player" = "none" ]; then
        log "No audio player found. Please install ffmpeg, mpv, or vlc."
        return 1
    fi

    log "Starting elevator music with $player for session $session_id"

    # Start music player based on what's available
    case "$player" in
        ffplay)
            nohup ffplay -nodisp -autoexit -loop 0 "$MUSIC_FILE" >/dev/null 2>&1 &
            ;;
        mpv)
            nohup mpv --no-video --loop=inf "$MUSIC_FILE" >/dev/null 2>&1 &
            ;;
        afplay)
            # afplay doesn't loop, so we'll just play once
            nohup afplay "$MUSIC_FILE" >/dev/null 2>&1 &
            ;;
        paplay)
            nohup paplay --raw "$MUSIC_FILE" >/dev/null 2>&1 &
            ;;
        cvlc)
            nohup cvlc --no-video --loop --quiet "$MUSIC_FILE" >/dev/null 2>&1 &
            ;;
    esac

    local music_pid=$!
    echo "$music_pid" > "$pid_file"
    log "Music started with PID $music_pid"
    
    # Start background timer to stop music after 10 seconds
    (
        sleep 10
        if [ -f "$pid_file" ] && kill -0 "$music_pid" 2>/dev/null; then
            log "Auto-stopping music after 10 seconds (PID: $music_pid)"
            kill "$music_pid" 2>/dev/null || true
            sleep 0.1
            kill -9 "$music_pid" 2>/dev/null || true
            rm -f "$pid_file"
        fi
    ) &
}

# Stop playing music
stop_music() {
    local session_id="$1"
    local pid_file="${PID_DIR}/${session_id}.pid"

    if [ ! -f "$pid_file" ]; then
        log "No music playing for session $session_id"
        return 0
    fi

    local music_pid=$(cat "$pid_file")

    if kill -0 "$music_pid" 2>/dev/null; then
        log "Stopping music (PID: $music_pid)"
        kill "$music_pid" 2>/dev/null || true
        # Give it a moment, then force kill if needed
        sleep 0.1
        kill -9 "$music_pid" 2>/dev/null || true
    fi

    rm -f "$pid_file"
    log "Music stopped for session $session_id"
}

# Clean up all music processes for this session
cleanup_all() {
    local session_id="$1"
    stop_music "$session_id"
}

# Main execution
main() {
    # Log every script invocation immediately
    log "Script called with arguments: $*"
    
    # Read hook event data from stdin
    local event_data=""
    if [ -t 0 ]; then
        # If stdin is a terminal, we're being run manually
        log "Running in manual mode (stdin is terminal)"
    else
        # Read from stdin (hook mode)
        event_data=$(cat)
    fi

    # Parse event data or use defaults for manual testing
    local hook_name="${1:-}"
    local session_id="${2:-test-session}"

    if [ -n "$event_data" ]; then
        # Extract data from JSON if jq is available
        if command -v jq >/dev/null 2>&1; then
            hook_name=$(echo "$event_data" | jq -r '.hook_event_name // empty')
            session_id=$(echo "$event_data" | jq -r '.session_id // "unknown"')
        fi
    fi

    log "Hook: $hook_name, Session: $session_id"

    # Handle different hook events
    case "$hook_name" in
        Stop)
            start_music "$session_id"
            ;;
        UserPromptSubmit)
            stop_music "$session_id"
            ;;
        SessionEnd)
            cleanup_all "$session_id"
            ;;
        Notification)
            # Handle notification events - check matcher
            local matcher=""
            if [ -n "$event_data" ] && command -v jq >/dev/null 2>&1; then
                log "Event data received: $event_data"
                matcher=$(echo "$event_data" | jq -r '.matcher // empty')
                log "Parsed matcher: '$matcher'"
            else
                log "No event data or jq not available"
            fi
            case "$matcher" in
                permission_prompt|idle_prompt)
                    log "Matcher matched, starting music"
                    start_music "$session_id"
                    ;;
                *)
                    log "Matcher did not match (got: '$matcher')"
                    ;;
            esac
            ;;
        start)
            # Manual start
            start_music "$session_id"
            ;;
        stop)
            # Manual stop
            stop_music "$session_id"
            ;;
        test)
            echo "Testing elevator music extension..."
            echo "Audio player: $(detect_audio_player)"
            echo "Music file: $MUSIC_FILE"
            if [ -f "$MUSIC_FILE" ]; then
                echo "Music file found"
            else
                echo "Warning: Music file not found at $MUSIC_FILE"
            fi
            echo "Starting test playback..."
            start_music "test"
            echo "Playing for 5 seconds..."
            sleep 5
            echo "Stopping..."
            stop_music "test"
            echo "Test complete!"
            ;;
        *)
            echo "Usage: $0 {start|stop|test} [session_id]"
            echo "Or pipe hook event JSON to stdin"
            exit 1
            ;;
    esac

    exit 0
}

main "$@"
