#!/usr/bin/env python3
"""
Elevator Notifications Hook for Claude Code
This script sends OS notifications when Claude is idle and when you interact
"""

import sys
import os
import json
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

# Configuration
SCRIPT_DIR = Path(__file__).parent.resolve()
NOTIFICATION_DIR = Path("/tmp/claude-elevator-notifications")

# Ensure notification directory exists
NOTIFICATION_DIR.mkdir(parents=True, exist_ok=True)


def log(message: str) -> None:
    """Log a message with timestamp (optional, disabled by default)"""
    # Uncomment to enable logging
    # log_file = SCRIPT_DIR / "elevator-notifications.log"
    # timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # with open(log_file, "a") as f:
    #     f.write(f"[{timestamp}] {message}\n")
    pass


def detect_notification_system() -> str:
    """Detect available notification system on the system"""
    # Check for notify-send (Linux)
    if shutil.which("notify-send"):
        return "notify-send"

    # Check for osascript (macOS)
    if shutil.which("osascript"):
        return "osascript"

    # Check for powershell (Windows - WSL)
    if shutil.which("powershell.exe"):
        return "powershell"

    return "none"


def send_notification(title: str, message: str, urgency: str = "normal") -> None:
    """Send a notification using the available notification system"""
    notifier = detect_notification_system()

    if notifier == "none":
        log("No notification system found. Please install notify-send (Linux) or use macOS/Windows.")
        return

    log(f"Sending notification with {notifier}: {title} - {message}")

    try:
        if notifier == "notify-send":
            # Linux notification using notify-send
            cmd = [
                "notify-send",
                "-u", urgency,
                "-a", "Claude Code",
                title,
                message
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        elif notifier == "osascript":
            # macOS notification using osascript
            script = f'display notification "{message}" with title "{title}" subtitle "Claude Code"'
            cmd = ["osascript", "-e", script]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        elif notifier == "powershell":
            # Windows notification via PowerShell (from WSL)
            ps_script = f"""
            [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
            [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null
            $template = @"
            <toast>
                <visual>
                    <binding template="ToastText02">
                        <text id="1">{title}</text>
                        <text id="2">{message}</text>
                    </binding>
                </visual>
            </toast>
"@
            $xml = New-Object Windows.Data.Xml.Dom.XmlDocument
            $xml.LoadXml($template)
            $toast = New-Object Windows.UI.Notifications.ToastNotification $xml
            [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Claude Code").Show($toast)
            """
            cmd = ["powershell.exe", "-Command", ps_script]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        log(f"Notification sent successfully")

    except Exception as e:
        log(f"Error sending notification: {e}")


def notify_idle(session_id: str, notification_type: str = "waiting") -> None:
    """Send notification when Claude is idle"""
    state_file = NOTIFICATION_DIR / f"{session_id}.state"

    # Check if we already sent this notification
    if state_file.exists():
        current_state = state_file.read_text().strip()
        if current_state == "idle":
            log(f"Already notified idle state for session {session_id}")
            return

    # Send notification
    if notification_type == "permission_prompt":
        send_notification(
            "Claude Code - Permission Required",
            "Claude needs your permission to continue",
            "critical"
        )
    elif notification_type == "idle_prompt":
        send_notification(
            "Claude Code - Idle",
            "Claude is waiting for your input",
            "normal"
        )
    else:
        send_notification(
            "Claude Code - Waiting",
            "Claude is ready for your next prompt",
            "normal"
        )

    # Mark as idle
    state_file.write_text("idle")
    log(f"Notified idle state for session {session_id}")


def notify_active(session_id: str) -> None:
    """Send notification when user submits a prompt"""
    state_file = NOTIFICATION_DIR / f"{session_id}.state"

    # Check if we need to send active notification
    if state_file.exists():
        current_state = state_file.read_text().strip()
        if current_state == "idle":
            send_notification(
                "Claude Code - Processing",
                "Claude is working on your request",
                "low"
            )

    # Mark as active
    state_file.write_text("active")
    log(f"Notified active state for session {session_id}")


def cleanup_all(session_id: str) -> None:
    """Clean up state files for this session"""
    state_file = NOTIFICATION_DIR / f"{session_id}.state"
    state_file.unlink(missing_ok=True)
    log(f"Cleaned up session {session_id}")


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
        notify_idle(session_id, "waiting")
    elif hook_name == "UserPromptSubmit":
        notify_active(session_id)
    elif hook_name == "SessionEnd":
        cleanup_all(session_id)
    elif hook_name == "Notification":
        # Handle notification events - check notification_type
        notification_type = event_data.get("notification_type", "")
        log(f"Event data received: {event_data}")
        log(f"Parsed notification_type: '{notification_type}'")

        if notification_type in ["permission_prompt", "idle_prompt"]:
            log("Notification type matched, sending notification")
            notify_idle(session_id, notification_type)
        else:
            log(f"Notification type did not match (got: '{notification_type}')")
    elif hook_name == "test":
        print("Testing elevator notifications extension...")
        print(f"Notification system: {detect_notification_system()}")
        print("Sending test notification...")
        send_notification("Claude Code - Test", "This is a test notification", "normal")
        print("Test complete!")
    else:
        print(f"Usage: {sys.argv[0]} {{test}} [session_id]")
        print("Or pipe hook event JSON to stdin")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
