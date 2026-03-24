# Configuration Guide

Customize Brain-System to fit your workflow.

## Table of Contents

- [Vault Configuration](#vault-configuration)
- [CLI Configuration](#cli-configuration)
- [Web Server Configuration](#web-server-configuration)
- [Auto-Sync Configuration](#auto-sync-configuration)
- [Environment Variables](#environment-variables)

## Vault Configuration

### Adding a New Vault

Edit `~/.brain/multi-brain.py` (or `multi-brain.py` in the project):

```python
VAULTS = {
    # ... existing vaults ...

    "myvault": {
        "path": Path(os.path.expanduser("~/path/to/your/vault")),
        "db": Path(os.path.expanduser("~/path/to/your/vault/brain/brain.db")),
        "description": "My awesome vault",
        "color": "#ff6b6b"  # Optional: for graph visualization
    }
}
```

### Vault Options

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| path | Path | Yes | Absolute path to vault |
| db | Path | Yes | Where to store database |
| description | str | No | Human-readable description |
| color | str | No | Hex color for graph |

### Removing a Vault

Simply delete the vault entry from `VAULTS` dictionary:

```python
VAULTS = {
    "realm": {...},
    # "old_vault": {...},  # Remove this line
}
```

## CLI Configuration

### Shell Aliases

Add to `~/.zshrc` or `~/.bashrc`:

```bash
# Quick commands
alias bs='brain search'
alias bt='brain tasks --all'
alias bv='brain vaults'

# Quick add function
ba() {
    brain add-task "$*"
}

# Open vault in Obsidian
bo() {
    local vault="${1:-realm}"
    local vault_path="$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/$vault"
    open -a "Obsidian" "$vault_path"
}
```

### Default Vault

Change the default vault in `multi-brain.py`:

```python
def _detect_vault(self) -> str:
    # ...
    return "myvault"  # Change default here
```

### Search Defaults

Modify default search behavior in `multi-brain.py`:

```python
def search(self, query: str, limit: int = 50, all_vaults: bool = True):
    # Changed: limit=20->50, all_vaults=False->True
```

## Web Server Configuration

### Port Configuration

Edit `web.py`:

```python
# Near the end of the file
app.run(host='0.0.0.0', port=5790, debug=False)  # Changed from 5789
```

### Graph Limits

Adjust graph performance in `web.py`:

```python
# In graph() function
const sortedPoints = graphData.points
    .map((p, i) => ({...p, originalIndex: i}))
    .sort((a, b) => (b.connections || 0) - (a.connections || 0))
    .slice(0, 400);  # Reduce from 800 for better performance
```

### Graph Appearance

Customize colors in `graph.html`:

```javascript
const VAULT_COLORS = {
    realm: [0.39, 0.4, 0.95],    // RGB 0-1
    myvault: [1.0, 0.5, 0.0],    // Custom orange
    // Add more colors...
};
```

### Web Theme

Modify CSS in `web.py` HTML_TEMPLATE:

```css
/* Change background gradient */
body {
    background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%);
}

/* Change accent color */
.vault-btn.active {
    background: rgba(255, 99, 71, 0.3);  /* Tomato red */
    border-color: #ff6347;
}
```

## Auto-Sync Configuration

### Sync Interval

Edit `~/Library/LaunchAgents/com.brain.sync.plist`:

```xml
<!-- Sync every 10 minutes (600 seconds) -->
<key>StartInterval</key>
<integer>600</integer>

<!-- Or use specific times -->
<key>StartCalendarInterval</key>
<array>
    <dict>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
</array>
```

### Sync Logging

Configure log locations:

```xml
<key>StandardOutPath</key>
<string>~/brain-sync.log</string>  <!-- Changed from /tmp/ -->

<key>StandardErrorPath</key>
<string>~/brain-sync-error.log</string>
```

### Sync on File Change

Use fswatch for instant sync:

```bash
# Install fswatch
brew install fswatch

# Create sync script
cat > ~/brain-watch.sh << 'EOF'
#!/bin/bash
fswatch -o ~/Library/Mobile\ Documents/iCloud~md~obsidian/Documents/ | while read; do
    sleep 2  # Debounce
    brain sync
done
EOF

chmod +x ~/brain-watch.sh
```

## Environment Variables

Create `~/.brainrc`:

```bash
# Brain-System Configuration

# Default vault
export BRAIN_DEFAULT_VAULT="realm"

# Web server port
export BRAIN_WEB_PORT="5789"

# Sync interval (seconds)
export BRAIN_SYNC_INTERVAL="300"

# Database location
export BRAIN_DB_DIR="$HOME/.brain/db"

# Log level
export BRAIN_LOG_LEVEL="INFO"
```

Load in shell:

```bash
# Add to ~/.zshrc
source ~/.brainrc
```

Use in scripts:

```python
import os
default_vault = os.getenv("BRAIN_DEFAULT_VAULT", "realm")
```

## Database Configuration

### Index Optimization

For better search performance, add FTS5:

```python
# In sync.py, init_db()
self.conn.execute("""
    CREATE VIRTUAL TABLE IF NOT EXISTS notes_fts USING fts5(
        title, content, tags, content=notes
    )
""")

# Trigger to keep FTS updated
self.conn.execute("""
    CREATE TRIGGER IF NOT EXISTS notes_ai AFTER INSERT ON notes BEGIN
        INSERT INTO notes_fts(rowid, title, content, tags)
        VALUES (new.rowid, new.title, new.content, new.tags);
    END
""")
```

### Database Pruning

Periodically clean old data:

```python
def prune_old_notes(days=365):
    """Remove notes not updated in specified days"""
    cutoff = (datetime.now() - timedelta(days=days)).isoformat()
    self.conn.execute("""
        DELETE FROM notes
        WHERE updated_at < ? AND synced = 1
    """, (cutoff,))
    self.conn.commit()
```

## Obsidian Integration

### Obsidian Command Palette

Add custom commands to Obsidian:

1. Create plugin or use Obsidian Shell Commands
2. Add command for brain search
3. Map to hotkey

### Obsidian Templates

Create template with brain integration:

```markdown
---
tags: template
---

# {{title}}

## Related Notes
<!-- brain search "{{title}}" -- >

## Tasks
<!-- brain tasks -- >
```

## Advanced Configuration

### Custom Parsers

Add support for new file types:

```python
def import_notion(self, file_path):
    """Import Notion export"""
    # Parse Notion HTML/MD
    # Extract metadata
    # Store in database
    pass
```

### Custom Link Types

Add new connection types for the graph:

```python
# In web.py, graph() function
# Add "hashtag" links
for hashtag, indices in hashtag_to_points.items():
    # Connect notes with same hashtags
    pass
```

### Backup Strategy

Automated database backups:

```bash
# Add to crontab
0 0 * * * cp -r ~/Library/Mobile\ Documents/iCloud~md~obsidian/*/brain/ ~/brain-backup/$(date +\%Y\%m\%d)/
```

## Security Configuration

### Web Authentication

Add basic auth to web server:

```python
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    # Check credentials
    return username == 'admin' and password == os.getenv('BRAIN_PASSWORD')

@app.route('/')
@auth.login_required
def home():
    # ...
```

### Database Encryption

Use SQLCipher for encrypted databases:

```python
# Requires SQLCipher
pysqlcipher3 = sqlite3
conn = pysqlcipher3.connect(db_path)
conn.execute(f"PRAGMA key = '{os.getenv('DB_KEY')}'")
```

## Performance Tuning

### Connection Pooling

For web server under high load:

```python
from sqlalchemy.pool import StaticPool

engine = create_engine(
    'sqlite:///' + db_path,
    connect_args={'check_same_thread': False},
    poolclass=StaticPool,
    pool_pre_ping=True
)
```

### Caching

Add Redis for query caching:

```python
import redis

r = redis.Redis()

def search_with_cache(query):
    cache_key = f"search:{query}"
    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)

    results = brain.search(query)
    r.setex(cache_key, 300, json.dumps(results))
    return results
```

## Testing Configuration

Create test vault configuration:

```python
TEST_VAULTS = {
    "test": {
        "path": Path("/tmp/test-vault"),
        "db": Path("/tmp/test-vault/brain.db"),
        "description": "Test vault"
    }
}
```

Run tests in isolation:

```bash
# Run with test config
BRAIN_ENV=test pytest tests/
```
