# Elevator Music Plugin

Plays soothing elevator music while Claude Code is waiting for user input. Letting you know it's time to switch back to your terminal.

## Overview

This plugin enhances the Claude Code experience by playing pleasant elevator music during idle waiting periods, making the development workflow more enjoyable.

## Installation

From the sevii-agent-marketplace:

```bash
claude-code plugin install sevii-agent-marketplace/elevator-music
```

## Features

- Automatically plays elevator music when Claude Code is waiting for user input
- Plays on idle prompts, permission prompts, and Stop events
- Auto-stops after 10 seconds to prevent indefinite playback
- Supports multiple audio players (ffplay, mpv, afplay, paplay, cvlc)
- Includes "Quiet Floors" elevator music track

## Configuration

The plugin uses hooks to trigger elevator music playback. The configuration is handled through Claude Code's hook system.

### Example Configuration

See `settings.example.json` for a complete configuration example. The plugin hooks on:
- **Stop**: When Claude finishes and is idle
- **Notification** (idle_prompt): When waiting for user input
- **Notification** (permission_prompt): When requesting permissions
- **PermissionRequest**: When permissions are being requested

### Audio Player Requirements

The plugin automatically detects and uses one of the following audio players (in order of preference):
1. `ffplay` (from FFmpeg)
2. `mpv`
3. `afplay` (macOS)
4. `paplay` (PulseAudio)
5. `cvlc` (VLC command-line)

Make sure at least one of these is installed on your system.

## Music Info

**Song**: Quiet Floors

This song is a derivative of an audio sample created with GarageBand, then transformed using Suno AI. This was done using a paid Suno account granting commercial and non-personal use of the output audio.

For questions or license concerns, email: nick@sledgeworx.io

## License

MIT (except for music - see Music Info section)
