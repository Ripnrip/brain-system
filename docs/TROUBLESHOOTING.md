# Troubleshooting Guide

Solutions to common issues with Brain-System.

## Table of Contents

- [Installation Issues](#installation-issues)
- [Sync Issues](#sync-issues)
- [Search Issues](#search-issues)
- [Web Server Issues](#web-server-issues)
- [Database Issues](#database-issues)
- [Performance Issues](#performance-issues)
- [Auto-Sync Issues](#auto-sync-issues)

## Installation Issues

### Command not found: brain

**Symptoms:**
```bash
brain vaults
zsh: command not found: brain
```

**Solutions:**

1. Check if brain is installed:
```bash
ls -la ~/.brain/
```

2. Check PATH:
```bash
echo $PATH | grep brain
```

3. Add to PATH if missing:
```bash
# Add to ~/.zshrc
export PATH="$HOME/.brain:$PATH"

# Reload shell
source ~/.zshrc
```

### Python version error

**Symptoms:**
```bash
python3 --version
Python 3.9.x
```

**Solution:**
Brain-System requires Python 3.11+. Install newer Python:

```bash
# Using Homebrew
brew install python@3.11

# Using pyenv
pyenv install 3.11
pyenv global 3.11
```

### Flask not found

**Symptoms:**
```bash
ModuleNotFoundError: No module named 'flask'
```

**Solution:**
```bash
pip3 install flask
```

## Sync Issues

### Vault not found

**Symptoms:**
```bash
brain sync
⚠️ realm: Vault path not found
```

**Solutions:**

1. Check vault configuration:
```bash
# Edit ~/.brain/multi-brain.py
# Verify paths are correct
```

2. Update vault paths:
```python
VAULTS = {
    "realm": {
        "path": Path("/correct/path/to/vault"),
        # ...
    }
}
```

3. Verify vault exists:
```bash
ls -la ~/Library/Mobile\ Documents/iCloud~md~obsidian/Documents/
```

### Permission denied

**Symptoms:**
```bash
PermissionError: [Errno 13] Permission denied
```

**Solutions:**

1. Check file permissions:
```bash
ls -la ~/.brain/
```

2. Fix permissions:
```bash
chmod +x ~/.brain/brain
chmod +x ~/.brain/multi-brain.py
```

3. Check vault permissions:
```bash
ls -la ~/path/to/vault/
```

### Sync incomplete

**Symptoms:**
```bash
brain sync
✅ realm: 0 notes  # Expected more
```

**Solutions:**

1. Check for .gitignore exclusions:
```bash
# Ensure brain/ is not ignored
cat ~/path/to/vault/.gitignore
```

2. Manually trigger sync:
```bash
cd ~/path/to/vault
python3 ~/.brain/sync.py sync
```

3. Check for file errors:
```bash
# Look for error messages during sync
brain sync 2>&1 | grep Error
```

## Search Issues

### No results found

**Symptoms:**
```bash
brain search "known topic"
🔍 Found 0 results for 'known topic'
```

**Solutions:**

1. Re-sync vaults:
```bash
brain sync
```

2. Check if vault is indexed:
```bash
brain stats
```

3. Try exact match:
```bash
brain search "exact phrase"
```

4. Search all vaults:
```bash
brain search "topic" --all
```

### Slow search

**Symptoms:** Search takes more than a second.

**Solutions:**

1. Check database size:
```bash
ls -lh ~/path/to/vault/brain/brain.db
```

2. Rebuild indexes:
```bash
rm ~/path/to/vault/brain/brain.db
brain sync
```

3. Check for corrupted database:
```bash
sqlite3 ~/path/to/vault/brain/brain.db "PRAGMA integrity_check;"
```

## Web Server Issues

### Port already in use

**Symptoms:**
```bash
python3 web.py
OSError: [Errno 48] Address already in use
```

**Solutions:**

1. Find and kill existing process:
```bash
lsof -i :5789
kill -9 $(lsof -ti :5789)
```

2. Change port in web.py:
```python
# Find this line in web.py
app.run(host='0.0.0.0', port=5789, debug=False)

# Change to different port
app.run(host='0.0.0.0', port=5790, debug=False)
```

### Graph won't load

**Symptoms:** Graph view shows loading spinner forever.

**Solutions:**

1. Check browser console for errors:
```bash
# Open browser DevTools (Cmd+Option+I)
# Look for red errors
```

2. Clear browser cache:
```bash
# Chrome/Edge: Cmd+Shift+Delete
# Or use incognito mode
```

3. Reduce graph data size:
```python
# In web.py, graph() function:
# Change: .slice(0, 800)
# To: .slice(0, 400)
```

4. Check cosmos.gl CDN:
```bash
# In graph.html, verify CDN is accessible
curl -I https://cdn.jsdelivr.net/npm/@cosmos.gl/graph@2.0.0/dist/graph.esm.min.js
```

### Can't access from other devices

**Symptoms:** Works on localhost but not from phone/other computer.

**Solutions:**

1. Check firewall settings:
```bash
# System Settings > Network > Firewall
# Allow Python or port 5789
```

2. Verify server is listening on all interfaces:
```bash
lsof -i :5789
# Should show 0.0.0.0:5789, not 127.0.0.1:5789
```

3. Get correct IP address:
```bash
ipconfig getifaddr en0  # WiFi
ipconfig getifaddr en1  # Ethernet
```

4. Test locally first:
```bash
curl http://localhost:5789
```

## Database Issues

### Database is locked

**Symptoms:**
```bash
sqlite3.OperationalError: database is locked
```

**Solutions:**

1. Close all connections:
```bash
# Stop web server
# Stop any running brain commands
```

2. Wait for auto-sync to finish:
```bash
# Check sync log
tail -f /tmp/brain-sync.log
```

3. Remove lock file:
```bash
rm ~/path/to/vault/brain/brain.db-shm
rm ~/path/to/vault/brain/brain.db-wal
```

### Database corrupted

**Symptoms:**
```bash
sqlite3.DatabaseError: database disk image is malformed
```

**Solutions:**

1. Check integrity:
```bash
sqlite3 ~/path/to/vault/brain/brain.db "PRAGMA integrity_check;"
```

2. Export and reimport:
```bash
# Dump database
sqlite3 ~/path/to/vault/brain/brain.db ".dump" > dump.sql

# Create new database
sqlite3 ~/path/to/vault/brain/brain.db.new < dump.sql

# Replace old database
mv ~/path/to/vault/brain/brain.db.new ~/path/to/vault/brain/brain.db
```

3. Rebuild from scratch:
```bash
rm ~/path/to/vault/brain/brain.db
brain sync
```

## Performance Issues

### Slow sync

**Symptoms:** Sync takes more than 30 seconds.

**Solutions:**

1. Check vault size:
```bash
find ~/path/to/vault -name "*.md" | wc -l
```

2. Exclude large directories:
```python
# In sync.py, add exclusions:
if ".git" in str(md_file) or "brain/" in str(md_file) or "large_folder/" in str(md_file):
    continue
```

3. Use batch inserts:
```python
# Already implemented, but verify transaction is used
conn.execute("BEGIN TRANSACTION")
# ... inserts ...
conn.commit()
```

### High memory usage

**Symptoms:** Web server using >500MB memory.

**Solutions:**

1. Limit graph nodes:
```python
# In web.py, reduce from 800 to 400
.slice(0, 400)
```

2. Limit search results:
```python
# In web.py, reduce from 20 to 10
LIMIT 10
```

3. Restart server periodically:
```bash
# Add to LaunchAgent to restart daily
```

## Auto-Sync Issues

### LaunchAgent not running

**Symptoms:** Database not updating automatically.

**Solutions:**

1. Check if loaded:
```bash
launchctl list | grep brain
```

2. Load manually:
```bash
launchctl load ~/Library/LaunchAgents/com.brain.sync.plist
```

3. Check for errors:
```bash
launchctl print user/$(id -u)/com.brain.sync
```

### Wrong Python path

**Symptoms:** LaunchAgent fails with "python3: No such file"

**Solutions:**

1. Find Python path:
```bash
which python3
# Output: /usr/bin/python3 or /opt/homebrew/bin/python3
```

2. Update plist:
```xml
<key>ProgramArguments</key>
<array>
    <string>/usr/bin/python3</string>  <!-- Use full path from which -->
    <string>/Users/yourusername/.brain/multi-brain.py</string>
    <string>sync</string>
</array>
```

3. Reload LaunchAgent:
```bash
launchctl unload ~/Library/LaunchAgents/com.brain.sync.plist
launchctl load ~/Library/LaunchAgents/com.brain.sync.plist
```

### Sync log not created

**Symptoms:** No log file in /tmp/

**Solutions:**

1. Create log directory:
```bash
sudo mkdir -p /tmp
sudo chmod 777 /tmp
```

2. Check plist paths:
```xml
<key>StandardOutPath</key>
<string>/tmp/brain-sync.log</string>

<key>StandardErrorPath</key>
<string>/tmp/brain-sync-error.log</string>
```

3. Test manually:
```bash
/usr/bin/python3 ~/.brain/multi-brain.py sync > /tmp/brain-sync.log 2>&1
```

## Getting Help

If issues persist:

1. Check logs:
```bash
tail -f /tmp/brain-sync.log
tail -f /tmp/brain-sync-error.log
```

2. Enable debug mode:
```python
# In multi-brain.py, add:
import logging
logging.basicConfig(level=logging.DEBUG)
```

3. Report issues:
- Include error messages
- Include system info (OS, Python version)
- Include steps to reproduce

## Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `command not found` | PATH not set | Add ~/.brain to PATH |
| `Permission denied` | File permissions | chmod +x ~/.brain/brain |
| `Vault not found` | Wrong path in config | Update VAULTS in multi-brain.py |
| `database is locked` | Concurrent access | Stop web server, wait for sync |
| `No module named 'flask'` | Missing dependency | pip3 install flask |
| `Address already in use` | Port conflict | Kill process or change port |
