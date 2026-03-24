# API Reference

Complete API documentation for Brain-System CLI and Web interfaces.

## Table of Contents

- [CLI API](#cli-api)
- [Python Module API](#python-module-api)
- [Web REST API](#web-rest-api)
- [Database Schema](#database-schema)

---

## CLI API

### brain vaults

List all configured vaults with statistics.

```bash
brain vaults
```

**Output:**
```
🧠 Multi-Vault Brain System

Available Vaults:
  ✅ realm    -  692 notes - Main second brain with PARA, Zettelkasten, and daily notes
  ✅ remote   -   29 notes - Cloud-synced vault with Todoist integration
  ✅ apple    -  662 notes - Apple Notes exported to Obsidian format
  ✅ assets   -    2 notes - Assets and attachments
  ⚠️ second   - Error: Vault path not found
```

### brain search

Search notes across vaults.

```bash
brain search <query> [--all]
```

**Arguments:**
- `query` - Search string (searches title, content, tags)
- `--all` - Search all vaults instead of current

**Examples:**
```bash
brain search "python"
brain search "machine learning" --all
```

**Output:**
```
🔍 Found 15 results for 'python':

  • [realm] Python Machine Learning Setup
  • [realm] Python Data Structures
  • [apple] Python Study Notes
```

### brain tasks

Display pending tasks.

```bash
brain tasks [--all]
```

**Arguments:**
- `--all` - Show tasks from all vaults

**Output:**
```
✅ Pending Tasks (12):

  [realm] Implement new feature
  [realm] Review pull request
  [remote] Call client Tuesday
```

### brain add-task

Add a new task.

```bash
brain add-task <content> [vault]
```

**Arguments:**
- `content` - Task description
- `vault` - Target vault (default: current/realm)

**Examples:**
```bash
brain add-task "Buy milk"
brain add-task "Finish report" realm
```

### brain sync

Synchronize all vaults (rebuild databases).

```bash
brain sync
```

**Output:**
```
Syncing realm...
  ✅ realm: 692 notes
Syncing remote...
  ✅ remote: 29 notes
...
```

### brain stats

Show statistics for all vaults.

```bash
brain stats
```

**Output:**
```
📊 Vault Statistics

  realm     692 notes   12 tasks
  remote     29 notes    3 tasks
  apple     662 notes    0 tasks
  assets      2 notes    0 tasks
  second     37 notes    1 tasks
```

### brain cd

Change to vault directory (shell integration).

```bash
brain cd <vault>
```

**Note:** Requires shell function or `exec $SHELL`

### brain open

Open vault in Obsidian.

```bash
brain open <vault>
```

---

## Python Module API

### MultiBrain Class

```python
from multi_brain import MultiBrain

# Initialize with vault name
brain = MultiBrain("realm")

# Auto-detect from current directory
brain = MultiBrain()
```

#### Methods

##### `import_vault()`

Import all markdown files from the vault.

```python
count = brain.import_vault()
# Returns: number of notes imported
```

##### `search(query, limit=20, all_vaults=False)`

Search notes.

```python
results = brain.search("python", limit=20, all_vaults=False)

# Returns: list of sqlite3.Row with keys:
# - id, title, content, tags, vault
```

##### `get_tasks(all_vaults=False)`

Get pending tasks.

```python
tasks = brain.get_tasks(all_vaults=True)

# Returns: list of dict with keys:
# - id, note_id, content, completed, due_date, priority, todoist_id, vault, created_at
```

##### `get_stats()`

Get vault statistics.

```python
stats = brain.get_stats()

# Returns: dict
# {
#     "vault": "realm",
#     "notes": 692,
#     "pending_tasks": 12,
#     "path": "/path/to/vault"
# }
```

##### `add_task(content, priority=2)`

Add a task.

```python
task_id = brain.add_task("Review code", priority=1)
# Returns: task ID (string)
# Priority: 1=high, 2=medium, 3=low
```

### BrainDB Class (sync.py)

```python
from sync import BrainDB

db = BrainDB()
```

#### Methods

##### `upsert_note(file_path, title, content, yaml_data, tags)`

Insert or update a note.

```python
note_id = db.upsert_note(
    file_path="/path/to/note.md",
    title="Note Title",
    content="Note body",
    yaml_data={"tags": ["test"], "date": "2024-01-01"},
    tags=["test", "example"]
)
```

##### `get_note(note_id)`

Get note by ID.

```python
note = db.get_note("realm_abc123...")
# Returns: sqlite3.Row or None
```

##### `search_notes(query, limit=20)`

Search notes.

```python
results = db.search_notes("query", limit=20)
```

##### `get_by_para(folder)`

Get notes by PARA folder.

```python
results = db.get_by_para("Projects")
```

##### `add_task(content, note_id=None, due_date=None, priority=2)`

Add a task.

```python
task_id = db.add_task(
    content="Task description",
    note_id="note_id",
    due_date="2024-12-31",
    priority=1
)
```

##### `get_tasks(include_completed=False)`

Get tasks.

```python
pending = db.get_tasks()
all_tasks = db.get_tasks(include_completed=True)
```

---

## Web REST API

Base URL: `http://localhost:5789`

### GET /

Main search interface.

**Response:** HTML page

### GET /search

Search notes across vaults.

**Query Parameters:**
- `q` (required) - Search query
- `vault` - Filter by vault name (default: all)

**Response:**
```json
{
  "results": [
    {
      "id": "realm_abc123...",
      "title": "Note Title",
      "content": "First 500 chars...",
      "tags": "[\"tag1\", \"tag2\"]",
      "vault": "realm"
    }
  ]
}
```

**Example:**
```bash
curl "http://localhost:5789/search?q=python&vault=realm"
```

### GET /api/stats

Get statistics for all vaults.

**Response:**
```json
{
  "realm": {"notes": 692},
  "remote": {"notes": 29},
  "apple": {"notes": 662},
  "assets": {"notes": 2},
  "second": {"notes": 37}
}
```

### GET /graph

Get graph data for visualization.

**Query Parameters:**
- `vault` - Filter by vault name (default: all)
- `q` - Filter notes by search query

**Response:**
```json
{
  "points": [
    {
      "id": "realm_abc123...",
      "title": "Note Title",
      "content": "First 500 chars...",
      "tags": "[\"tag1\"]",
      "vault": "realm",
      "folder": "Projects",
      "connections": 15,
      "words": ["word1", "word2", ...]
    }
  ],
  "links": [
    {
      "source": 0,
      "target": 5,
      "type": "wikilink"
    }
  ],
  "stats": {
    "total_points": 800,
    "total_links": 5217,
    "vaults": 5
  }
}
```

**Link Types:**
- `wikilink` - Direct `[[link]]` reference
- `similar` - Content similarity (shared words)
- `tag` - Shared tags
- `folder` - Same PARA folder
- `cross-vault` - Related across vaults

### GET /graph-view

Graph visualization page.

**Response:** HTML page with cosmos.gl graph

---

## Database Schema

### Notes Table

| Column | Type | Description |
|--------|------|-------------|
| id | TEXT | MD5 hash of file path (primary key) |
| title | TEXT | File name without extension |
| content | TEXT | Body content (YAML removed) |
| type | TEXT | Optional note type |
| tags | TEXT | JSON array of tags |
| created_at | TEXT | ISO 8601 timestamp |
| updated_at | TEXT | ISO 8601 timestamp |
| para_folder | TEXT | PARA category (Inbox/Projects/Areas/Resources/Archives) |
| yaml_frontmatter | TEXT | JSON of YAML frontmatter |
| file_path | TEXT | Absolute file path (unique) |
| vault | TEXT | Vault name |
| synced | INTEGER | Sync status flag |

### Links Table

| Column | Type | Description |
|--------|------|-------------|
| source_id | TEXT | Source note ID |
| target_id | TEXT | Target note ID |
| link_type | TEXT | Connection type (default: wikilink) |
| created_at | TEXT | ISO 8601 timestamp |
| vault | TEXT | Vault name |

**Primary Key:** (source_id, target_id, vault)

### Tasks Table

| Column | Type | Description |
|--------|------|-------------|
| id | TEXT | Task ID (primary key) |
| note_id | TEXT | Associated note ID (foreign key) |
| content | TEXT | Task description |
| completed | INTEGER | 0=pending, 1=completed |
| due_date | TEXT | ISO date string |
| priority | INTEGER | 1=high, 2=medium, 3=low |
| todoist_id | TEXT | Todoist integration ID |
| vault | TEXT | Vault name |
| created_at | TEXT | ISO 8601 timestamp |

**Foreign Key:** note_id REFERENCES notes(id)

---

## Error Codes

| Code | Description |
|------|-------------|
| 0 | Success |
| 1 | Vault not found |
| 2 | Database error |
| 3 | File not found |
| 4 | Parse error |

---

## Configuration

### Vault Configuration

Located in `multi-brain.py`:

```python
VAULTS = {
    "realm": {
        "path": Path(".../Realm-Obsidian"),
        "db": Path(".../Realm-Obsidian/brain/brain.db"),
        "description": "Main second brain"
    },
    # ... more vaults
}
```

### Web Server Configuration

Located in `web.py`:

```python
# Default port
PORT = 5789

# Host binding
HOST = '0.0.0.0'
```

---

## Examples

### Search CLI Example

```python
from multi_brain import MultiBrain

brain = MultiBrain("realm")
results = brain.search("python", limit=10)

for note in results:
    print(f"[{note['vault']}] {note['title']}")
    print(f"  {note['content'][:100]}...")
```

### Web API Example

```bash
# Search notes
curl "http://localhost:5789/search?q=machine+learning"

# Get graph data
curl "http://localhost:5789/graph?vault=realm&q=python"

# Get stats
curl "http://localhost:5789/api/stats"
```

### Database Query Example

```python
import sqlite3

conn = sqlite3.connect("brain/brain.db")
conn.row_factory = sqlite3.Row

# Recent notes in Projects
notes = conn.execute("""
    SELECT * FROM notes
    WHERE para_folder = 'Projects'
    ORDER BY updated_at DESC
    LIMIT 10
""").fetchall()
```
