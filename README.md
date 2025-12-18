# Sevii Agent Marketplace

A curated collection of Claude Code plugins for enhanced development workflows.

## Installation

To install this marketplace in Claude Code:

```bash
# Install the marketplace
claude-code marketplace add https://github.com/sevii/agent-marketplace
```

Or add it manually to your Claude Code settings:

```json
{
  "marketplaces": [
    {
      "source": "github",
      "repo": "sevii/agent-marketplace"
    }
  ]
}
```

## Available Plugins

### Elevator Music

Plays soothing elevator music while Claude Code is waiting for user input, making the waiting experience more pleasant.

**Install:**
```bash
claude-code plugin install sevii-agent-marketplace/elevator-music
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT
