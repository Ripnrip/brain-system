# Setup Guide

Complete setup instructions for Brain-System on macOS.

## Prerequisites

- macOS 12.0 (Monterey) or later
- Python 3.11 or higher
- Obsidian (optional, for viewing notes)
- iCloud Drive enabled

## Installation

### 1. Clone or Download

Brain-System should be located in your Obsidian vaults directory:

```bash
cd ~/Library/Mobile\ Documents/iCloud~md~obsidian/Documents/Brain-System
```

### 2. Install Python Dependencies

```bash
# Install Flask for web interface
pip3 install flask

# Verify installation
python3 -c "import flask; print('Flask installed')"
```

### 3. Install CLI

```bash
# Create brain directory
mkdir -p ~/.brain

# Copy files
cp multi-brain.py ~/.brain/
cp sync.py ~/.brain/
cp brain ~/.brain/

# Make executable
chmod +x ~/.brain/brain
chmod +x ~/.brain/multi-brain.py
chmod +x ~/.brain/sync.py
```

### 4. Add to PATH

Add to your shell configuration (`~/.zshrc`):

```bash
# Add to PATH
export PATH="$HOME/.brain:$PATH"
```

Then reload:

```bash
source ~/.zshrc
```

### 5. Verify Installation

```bash
# Should display all vaults
brain vaults

# Sync all vaults
brain sync

# Search
brain search "test"
```

## Vault Configuration

Edit vault paths in `~/.brain/multi-brain.py`:

```python
VAULTS = {
    "myvault": {
        "path": Path("/path/to/your/vault"),
        "db": Path("/path/to/your/vault/brain/brain.db"),
        "description": "My vault description"
    }
}
```

## Auto-Sync Setup

### Create LaunchAgent

Create `~/Library/LaunchAgents/com.brain.sync.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.brain.sync</string>

    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/yourusername/.brain/multi-brain.py</string>
        <string>sync</string>
    </array>

    <key>StartInterval</key>
    <integer>300</integer>

    <key>StandardOutPath</key>
    <string>/tmp/brain-sync.log</string>

    <key>StandardErrorPath</key>
    <string>/tmp/brain-sync-error.log</string>

    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
```

### Load LaunchAgent

```bash
# Load the agent
launchctl load ~/Library/LaunchAgents/com.brain.sync.plist

# Verify it's running
launchctl list | grep brain

# View logs
tail -f /tmp/brain-sync.log
```

### Unload LaunchAgent

```bash
launchctl unload ~/Library/LaunchAgents/com.brain.sync.plist
```

## Web Server Setup

### Start Server

```bash
# From Brain-System directory
python3 web.py
```

The server starts on `http://0.0.0.0:5789`

### Auto-Start Web Server (Optional)

Create another LaunchAgent for the web server:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.brain.web</string>

    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/yourusername/Library/Mobile Documents/iCloud~md~obsidian/Documents/Brain-System/web.py</string>
    </array>

    <key>RunAtLoad</key>
    <true/>

    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

## Shell Integration

Add useful functions to `~/.zshrc`:

```bash
# Brain quick search
function bs() {
    brain search "$*" --all
}

# Brain quick tasks
function bt() {
    brain tasks --all
}

# Brain quick add
function ba() {
    brain add-task "$*"
}

# Open vault in Obsidian
function bo() {
    brain open "${1:-realm}"
}

# cd to vault
function bcd() {
    cd "$(~/Library/Mobile\ Documents/iCloud~md~obsidian/Documents/Brain-System/multi-brain.py vault-path ${1:-realm})"
}
```

## Verification

Run these commands to verify everything works:

```bash
# 1. CLI works
brain vaults

# 2. Search works
brain search "test" --all

# 3. Tasks work
brain tasks --all

# 4. Sync works
brain sync

# 5. Web server starts
python3 web.py
# Then visit http://localhost:5789
```

## Troubleshooting

### Command not found

```bash
# Check PATH
echo $PATH | grep brain

# Add to PATH if missing
export PATH="$HOME/.brain:$PATH"
```

### Python module errors

```bash
# Install dependencies
pip3 install flask

# Check Python version
python3 --version  # Should be 3.11+
```

### Database errors

```bash
# Re-sync all vaults
brain sync

# Or delete specific database
rm ~/path/to/vault/brain/brain.db
brain sync
```

### LaunchAgent not running

```bash
# Check if loaded
launchctl list | grep brain

# Check logs
cat /tmp/brain-sync.log

# Reload
launchctl unload ~/Library/LaunchAgents/com.brain.sync.plist
launchctl load ~/Library/LaunchAgents/com.brain.sync.plist
```

### Web server port in use

```bash
# Find process using port
lsof -i :5789

# Kill process
kill -9 $(lsof -ti :5789)

# Or change port in web.py
```

## Next Steps

- Read [User Guide](USER_GUIDE.md) for usage
- Read [Configuration Guide](CONFIGURATION.md) for customization
- Set up [iOS Shortcuts](IOS_SHORTCUTS.md) for mobile access
