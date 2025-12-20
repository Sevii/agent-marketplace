# Elevator Music Plugin

Plays soothing elevator music while Claude Code is waiting for user input. Letting you know its time to switch back to your terminal.

## Demo

https://github.com/user-attachments/assets/afb170bf-83cd-4a4b-b62e-2dc84fb816ad


## Requirements
Make sure you have Claude Code Version 2.0+ installed
`claude --version`


## Installation

Inside Claude Code run

```bash
/plugin marketplace add sevii/agent-marketplace

/plugin install elevator-music@agent-marketplace
```

## Features

- Automatically plays elevator music when Claude Code is waiting for user input
- Plays on idle prompts, permission prompts, and Stop events
- Auto-stops after 30 seconds to prevent indefinite playback
- Supports multiple audio players (ffplay, mpv, afplay, paplay, cvlc)
- Includes "Quiet Floors" elevator music track
- Implemented using python 3

## Operating Systems
We have only tested on MacOS Sonoma 14.7.8 (23H730)


## Music Info


The songs are derivatives of an audio sample I created with GarageBand.
Then I used Suno to transform that sample into various elevator songs. 
This was done using a paid Suno account granting me commercial and non-personal use of the output audio. 
For questions or other license concerns email me via nick@sledgeworx.io


## License

MIT except for music
Music - All rights reserved except those required for you to use the Elevator Music Plugin.
