# Elevator Notifications Plugin

Sends desktop notifications when Claude Code is waiting for user input. This is a notification-based alternative to the elevator-music plugin, helping you know when Claude needs your attention without playing audio.

## Features

- Sends OS notifications when Claude Code is waiting for user input
- Notifies on idle prompts, permission prompts, and Stop events
- Also notifies when Claude starts processing your request
- Cross-platform support:
  - **Linux**: Uses `notify-send` (libnotify)
  - **macOS**: Uses native notifications via `osascript`
  - **Windows/WSL**: Uses PowerShell notifications
- Lightweight and fast
- Tracks state to avoid duplicate notifications
- Implemented using Python 3

## Requirements

Make sure you have Claude Code Version 2.0+ installed:
```bash
claude --version
```

### System Requirements

**Linux:**
```bash
# Install libnotify (usually pre-installed on most desktop Linux distributions)
sudo apt-get install libnotify-bin  # Debian/Ubuntu
sudo dnf install libnotify           # Fedora
sudo pacman -S libnotify             # Arch
```

**macOS:**
No additional installation required - uses built-in notification system.

**Windows (WSL):**
No additional installation required - uses PowerShell notifications.

## Installation

Inside Claude Code run:

```bash
/plugin marketplace add sevii/agent-marketplace

/plugin install elevator-notifications@agent-marketplace
```

## Testing

To test if notifications are working, you can run the script manually:

```bash
cd ~/.config/claude/plugins/elevator-notifications
./elevator-notifications.py test
```

You should see a test notification appear on your desktop.

## How It Works

The plugin hooks into several Claude Code events:

- **Stop**: When Claude finishes responding and is waiting for input
- **UserPromptSubmit**: When you submit a new prompt to Claude
- **Notification (idle_prompt)**: When Claude explicitly shows an idle prompt
- **Notification (permission_prompt)**: When Claude needs permission to proceed

Each event triggers a contextual desktop notification to keep you informed of Claude's status.

## Notification Types

- **Waiting**: Normal priority - Claude finished and is ready for your next prompt
- **Idle**: Normal priority - Claude is waiting for your input
- **Permission Required**: Critical priority - Claude needs your permission to continue
- **Processing**: Low priority - Claude is working on your request

## Operating Systems

Tested on:
- Ubuntu 20.04+ (Linux)
- macOS Sonoma 14.7.8
- Windows 11 (via WSL2)

## Troubleshooting

If notifications aren't appearing:

1. **Linux**: Make sure you have a notification daemon running (most desktop environments include one)
2. **macOS**: Check System Preferences → Notifications to ensure terminal notifications are enabled
3. **Check the script**: Run the test command to verify your notification system is detected correctly

## License

MIT

## Credits

Based on the [elevator-music plugin](../elevator-music) by Nicholas Sledgianowski, adapted to use OS notifications instead of audio playback.
