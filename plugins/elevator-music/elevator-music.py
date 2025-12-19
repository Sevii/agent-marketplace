#!/usr/bin/env python3
"""
Elevator Music Hook for Claude Code
This script plays elevator music when Claude is idle and stops it when you interact
"""

import sys
import os
import json
import subprocess
import signal
import time
import shutil
from pathlib import Path
from datetime import datetime
from threading import Timer

# Configuration
SCRIPT_DIR = Path(__file__).parent.resolve()
SOUNDS_DIR = SCRIPT_DIR / "sounds"
MUSIC_FILE = SOUNDS_DIR / "QuietFloors.mp3"
PID_DIR = Path("/tmp/claude-elevator-music")

# Ensure PID directory exists
PID_DIR.mkdir(parents=True, exist_ok=True)


def log(message: str) -> None:
    """Log a message with timestamp (optional, disabled by default)"""
    # Uncomment to enable logging
    log_file = SCRIPT_DIR / "elevator-music.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] {message}\n")


def detect_audio_player() -> str:
    """Detect available audio player on the system"""
    players = ["ffplay", "mpv", "afplay", "paplay", "cvlc"]

    for player in players:
        if shutil.which(player):
            return player

    return "none"


def start_music(session_id: str) -> None:
    """Start playing elevator music for the given session"""
    pid_file = PID_DIR / f"{session_id}.pid"

    # Check if already playing
    if pid_file.exists():
        try:
            existing_pid = int(pid_file.read_text().strip())
            # Check if process is still running
            os.kill(existing_pid, 0)
            log(f"Music already playing for session {session_id} (PID: {existing_pid})")
            return
        except (ProcessLookupError, ValueError):
            # Stale PID file, remove it
            pid_file.unlink(missing_ok=True)

    player = detect_audio_player()

    if player == "none":
        log("No audio player found. Please install ffmpeg, mpv, or vlc.")
        return

    log(f"Starting elevator music with {player} for session {session_id}")

    # Start music player based on what's available (single playback, no looping)
    music_file_str = str(MUSIC_FILE)

    if player == "ffplay":
        cmd = ["ffplay", "-nodisp", "-autoexit", music_file_str]
    elif player == "mpv":
        cmd = ["mpv", "--no-video", music_file_str]
    elif player == "afplay":
        cmd = ["afplay", music_file_str]
    elif player == "paplay":
        cmd = ["paplay", "--raw", music_file_str]
    elif player == "cvlc":
        cmd = ["cvlc", "--no-video", "--quiet", "--play-and-exit", music_file_str]
    else:
        return

    # Start the process in the background
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True
    )

    music_pid = process.pid
    pid_file.write_text(str(music_pid))
    log(f"Music started with PID {music_pid}")

    # Start background timer to stop music after 30 seconds
    def auto_stop():
        if pid_file.exists():
            try:
                pid = int(pid_file.read_text().strip())
                os.kill(pid, 0)  # Check if still running
                log(f"Auto-stopping music after 30 seconds (PID: {pid})")
                try:
                    os.kill(pid, signal.SIGTERM)
                    time.sleep(0.1)
                    os.kill(pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                pid_file.unlink(missing_ok=True)
            except (ProcessLookupError, ValueError):
                pass

    timer = Timer(30.0, auto_stop)
    timer.daemon = True
    timer.start()


def stop_music(session_id: str) -> None:
    """Stop playing elevator music for the given session"""
    pid_file = PID_DIR / f"{session_id}.pid"

    if not pid_file.exists():
        log(f"No music playing for session {session_id}")
        return

    try:
        music_pid = int(pid_file.read_text().strip())

        # Check if process is running
        os.kill(music_pid, 0)
        log(f"Stopping music (PID: {music_pid})")

        try:
            os.kill(music_pid, signal.SIGTERM)
            time.sleep(0.1)
            os.kill(music_pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    except (ProcessLookupError, ValueError):
        pass

    pid_file.unlink(missing_ok=True)
    log(f"Music stopped for session {session_id}")


def cleanup_all(session_id: str) -> None:
    """Clean up all music processes for this session"""
    stop_music(session_id)


def main():
    """Main execution"""
    # Log every script invocation immediately
    log(f"Script called with arguments: {sys.argv}")

    # Read hook event data from stdin
    event_data = {}
    if not sys.stdin.isatty():
        # Read from stdin (hook mode)
        try:
            stdin_content = sys.stdin.read()
            if stdin_content:
                event_data = json.loads(stdin_content)
        except json.JSONDecodeError:
            log("Failed to parse JSON from stdin")
    else:
        log("Running in manual mode (stdin is terminal)")

    # Parse event data or use defaults for manual testing
    hook_name = sys.argv[1] if len(sys.argv) > 1 else ""
    session_id = sys.argv[2] if len(sys.argv) > 2 else "test-session"

    if event_data:
        hook_name = event_data.get("hook_event_name", hook_name)
        session_id = event_data.get("session_id", "unknown")

    log(f"Hook: {hook_name}, Session: {session_id}")

    # Handle different hook events
    if hook_name == "Stop":
        start_music(session_id)
    elif hook_name == "UserPromptSubmit":
        stop_music(session_id)
    elif hook_name == "SessionEnd":
        cleanup_all(session_id)
    elif hook_name == "Notification":
        # Handle notification events - check notification_type
        notification_type = event_data.get("notification_type", "")
        log(f"Event data received: {event_data}")
        log(f"Parsed notification_type: '{notification_type}'")

        if notification_type in ["permission_prompt", "idle_prompt"]:
            log("Notification type matched, starting music")
            start_music(session_id)
        else:
            log(f"Notification type did not match (got: '{notification_type}')")
    elif hook_name == "start":
        # Manual start
        start_music(session_id)
    elif hook_name == "stop":
        # Manual stop
        stop_music(session_id)
    elif hook_name == "test":
        print("Testing elevator music extension...")
        print(f"Audio player: {detect_audio_player()}")
        print(f"Music file: {MUSIC_FILE}")
        if MUSIC_FILE.exists():
            print("Music file found")
        else:
            print(f"Warning: Music file not found at {MUSIC_FILE}")
        print("Starting test playback...")
        start_music("test")
        print("Playing for 5 seconds...")
        time.sleep(5)
        print("Stopping...")
        stop_music("test")
        print("Test complete!")
    else:
        print(f"Usage: {sys.argv[0]} {{start|stop|test}} [session_id]")
        print("Or pipe hook event JSON to stdin")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
