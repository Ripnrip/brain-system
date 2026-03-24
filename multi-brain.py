#!/usr/bin/env python3
"""
Multi-Vault Brain System
Manages multiple Obsidian vaults with fast SQLite databases
"""

import os
import sys
import json
import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Optional, List

# Vault configurations - updated with actual vault paths
VAULTS = {
    "realm": {
        "path": Path(os.path.expanduser("~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Realm-Obsidian")),
        "db": Path(os.path.expanduser("~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Realm-Obsidian/brain/brain.db")),
        "description": "Main second brain with PARA, Zettelkasten, and daily notes"
    },
    "remote": {
        "path": Path(os.path.expanduser("~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Remote-Vault")),
        "db": Path(os.path.expanduser("~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Remote-Vault/brain/brain.db")),
        "description": "Cloud-synced vault with Todoist integration"
    },
    "apple": {
        "path": Path(os.path.expanduser("~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Apple Notes")),
        "db": Path(os.path.expanduser("~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Apple Notes/brain/brain.db")),
        "description": "Apple Notes exported to Obsidian format"
    },
    "assets": {
        "path": Path(os.path.expanduser("~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Apple Notes Assets")),
        "db": Path(os.path.expanduser("~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Apple Notes Assets/brain/brain.db")),
        "description": "Assets and attachments"
    },
    "second": {
        "path": Path(os.path.expanduser("~/Documents/SecondBrain")),
        "db": Path(os.path.expanduser("~/Documents/SecondBrain/brain/brain.db")),
        "description": "Local second brain (old location, redirecting)"
    }
}


class MultiBrain:
    """Single vault database manager"""

    def __init__(self, vault_name: Optional[str] = None):
        self.vault_name = vault_name or self._detect_vault()
        self.config = VAULTS.get(self.vault_name)
        if not self.config:
            raise ValueError(f"Vault '{vault_name}' not found. Available: {list(VAULTS.keys())}")
        self.init_db()

    def _detect_vault(self) -> str:
        """Detect vault from current directory"""
        cwd = Path.cwd()
        for name, config in VAULTS.items():
            if cwd.is_relative_to(config["path"]):
                return name
        return "realm"  # default

    def init_db(self):
        """Initialize database for this vault"""
        self.db_path = self.config["db"]
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row

        # First create tables if they don't exist
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS notes (
                id TEXT PRIMARY KEY,
                title TEXT,
                content TEXT,
                type TEXT,
                tags TEXT,
                created_at TEXT,
                updated_at TEXT,
                para_folder TEXT,
                yaml_frontmatter TEXT,
                file_path TEXT UNIQUE,
                vault TEXT,
                synced INTEGER DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS links (
                source_id TEXT,
                target_id TEXT,
                link_type TEXT DEFAULT 'wikilink',
                created_at TEXT,
                vault TEXT,
                PRIMARY KEY (source_id, target_id, vault)
            );

            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                note_id TEXT,
                content TEXT,
                completed INTEGER DEFAULT 0,
                due_date TEXT,
                priority INTEGER DEFAULT 2,
                todoist_id TEXT,
                vault TEXT,
                created_at TEXT,
                FOREIGN KEY (note_id) REFERENCES notes(id)
            );

            CREATE INDEX IF NOT EXISTS idx_notes_type ON notes(type);
            CREATE INDEX IF NOT EXISTS idx_notes_vault ON notes(vault);
            CREATE INDEX IF NOT EXISTS idx_tasks_vault ON tasks(vault);
        """)
        self.conn.commit()

    def import_vault(self):
        """Import all markdown files from this vault"""
        vault_path = self.config["path"]
        count = 0

        for md_file in vault_path.rglob("*.md"):
            if ".git" in str(md_file) or "brain/" in str(md_file):
                continue

            try:
                content = md_file.read_text()
                title = md_file.stem
                yaml_data = {}
                content_body = content
                tags = []

                lines = content.split("\n")
                if lines and lines[0] == "---":
                    for i, line in enumerate(lines[1:]):
                        if line == "---":
                            content_body = "\n".join(lines[i+2:]) if i+2 < len(lines) else ""
                            break
                        if ":" in line:
                            k, v = line.split(":", 1)
                            yaml_data[k.strip()] = v.strip()
                    if "tags" in yaml_data:
                        tags = yaml_data["tags"]

                # Determine PARA folder
                para_folder = None
                path_parts = md_file.relative_to(vault_path).parts
                for folder in ["Inbox", "Projects", "Areas", "Resources", "Archives", "00-Inbox", "01-Permanent"]:
                    if folder in path_parts or any(folder.replace(" ", "").replace("0", "").replace("-", "").lower() in p.lower() for p in path_parts):
                        para_folder = folder.replace("00-", "").replace("01-", "").replace("02-", "").replace("03-", "")
                        break

                file_id = f"{self.vault_name}_{hashlib.md5(str(md_file).encode()).hexdigest()}"
                now = datetime.now().isoformat()

                self.conn.execute("""
                    INSERT OR REPLACE INTO notes
                    (id, file_path, title, content, yaml_frontmatter, tags, vault, para_folder, created_at, updated_at, synced)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?,
                        COALESCE((SELECT created_at FROM notes WHERE id = ?), ?), ?, 0)
                """, (file_id, str(md_file), title, content_body, json.dumps(yaml_data),
                      json.dumps(tags) if isinstance(tags, list) else str(tags),
                      self.vault_name, para_folder, file_id, now, now))
                count += 1

            except Exception as e:
                if "brain" not in str(md_file):
                    print(f"  Error importing {md_file.name}: {e}")

        self.conn.commit()
        return count

    def search(self, query: str, limit: int = 20, all_vaults: bool = False):
        """Search notes across vaults"""
        if all_vaults:
            results = []
            for vault_name in VAULTS:
                try:
                    brain = MultiBrain(vault_name)
                    vault_results = brain.conn.execute("""
                        SELECT id, title, content, tags, vault
                        FROM notes
                        WHERE content LIKE ? OR title LIKE ?
                        ORDER BY updated_at DESC LIMIT ?
                    """, (f"%{query}%", f"%{query}%", limit)).fetchall()
                    results.extend(vault_results)
                except:
                    pass
            return results[:limit]
        else:
            return self.conn.execute("""
                SELECT id, title, content, tags, vault
                FROM notes
                WHERE content LIKE ? OR title LIKE ?
                ORDER BY updated_at DESC LIMIT ?
            """, (f"%{query}%", f"%{query}%", limit)).fetchall()

    def get_tasks(self, all_vaults: bool = False):
        """Get all pending tasks"""
        if all_vaults:
            results = []
            for vault_name in VAULTS:
                try:
                    brain = MultiBrain(vault_name)
                    vault_results = brain.conn.execute("""
                        SELECT * FROM tasks WHERE completed = 0 ORDER BY priority DESC, created_at DESC
                    """).fetchall()
                    for r in vault_results:
                        d = dict(r)
                        d['vault'] = vault_name
                        results.append(d)
                except:
                    pass
            return results
        else:
            return self.conn.execute("""
                SELECT * FROM tasks WHERE completed = 0 ORDER BY priority DESC, created_at DESC
            """).fetchall()

    def get_stats(self):
        """Get vault statistics"""
        cursor = self.conn.execute("SELECT COUNT(*) FROM notes")
        notes_count = cursor.fetchone()[0]

        cursor = self.conn.execute("SELECT COUNT(*) FROM tasks WHERE completed = 0")
        tasks_count = cursor.fetchone()[0]

        return {
            "vault": self.vault_name,
            "notes": notes_count,
            "pending_tasks": tasks_count,
            "path": str(self.config["path"])
        }

    def add_task(self, content: str, priority: int = 2):
        """Add a task to this vault"""
        import hashlib
        task_id = f"{self.vault_name}_{hashlib.md5(content.encode()).hexdigest()}"
        now = datetime.now().isoformat()
        self.conn.execute("""
            INSERT INTO tasks (id, content, priority, vault, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (task_id, content, priority, self.vault_name, now))
        self.conn.commit()
        return task_id


def print_vaults():
    """List all vaults"""
    print("\n🧠 Multi-Vault Brain System\n")
    print("Available Vaults:")
    for name, config in VAULTS.items():
        try:
            brain = MultiBrain(name)
            stats = brain.get_stats()
            status = "✅" if (config["db"].exists()) else "⚠️"
            print(f"  {status} {name:8} - {stats['notes']:4} notes - {config['description']}")
        except:
            status = "❌" if not (config["db"].exists()) else "⚠️"
            print(f"  {status} {name:8} - {config['description']}")


def main():
    import hashlib
    cmd = sys.argv[1] if len(sys.argv) > 1 else "vaults"

    if cmd == "vaults":
        print_vaults()

    elif cmd == "search" and len(sys.argv) > 2:
        # Filter out --all flag
        query_parts = [arg for arg in sys.argv[2:] if arg != "--all"]
        query = " ".join(query_parts)
        all_vaults = "--all" in sys.argv

        if all_vaults:
            brain = MultiBrain("realm")
            results = brain.search(query, all_vaults=True)
        else:
            brain = MultiBrain()
            results = brain.search(query)

        print(f"\n🔍 Found {len(results)} results for '{query}':\n")
        for note in results:
            vault = note['vault'] if 'vault' in note.keys() else brain.vault_name
            title = note['title']
            print(f"  • [{vault}] {title}")

    elif cmd == "tasks":
        all_vaults = "--all" in sys.argv

        if all_vaults:
            brain = MultiBrain("realm")
            results = brain.get_tasks(all_vaults=True)
        else:
            brain = MultiBrain()
            results = brain.get_tasks()

        print(f"\n✅ Pending Tasks ({len(results)}):\n")
        for task in results:
            vault = task.get('vault', brain.vault_name)
            content = task['content']
            print(f"  [{vault}] {content}")

    elif cmd == "add-task" and len(sys.argv) > 2:
        content = " ".join([arg for arg in sys.argv[2:] if arg not in VAULTS])
        vault_arg = next((arg for arg in sys.argv[2:] if arg in VAULTS), "realm")
        brain = MultiBrain(vault_arg)
        task_id = brain.add_task(content)
        print(f"✅ Task added to [{vault_arg}]: {content}")

    elif cmd == "sync":
        for name in VAULTS:
            print(f"Syncing {name}...")
            try:
                brain = MultiBrain(name)
                count = brain.import_vault()
                print(f"  ✅ {name}: {count} notes")
            except Exception as e:
                print(f"  ⚠️ {name}: {e}")

    elif cmd == "stats":
        print("\n📊 Vault Statistics\n")
        for name in VAULTS:
            try:
                brain = MultiBrain(name)
                stats = brain.get_stats()
                print(f"  {stats['vault']:8} {stats['notes']:4} notes  {stats['pending_tasks']:2} tasks")
            except Exception as e:
                print(f"  {name:8} Error: {e}")

    else:
        print("""
🧠 Multi-Vault Brain CLI

Commands:
  vaults              List all vaults
  search <query>      Search current vault
  search <query> --all Search all vaults
  tasks               Show tasks in current vault
  tasks --all         Show tasks across all vaults
  add-task <task>     Add task to current vault
  add-task <task> <vault>  Add to specific vault
  sync                Sync all vaults
  stats               Statistics for all vaults

Vaults:
  realm    - Main second brain (PARA, Zettelkasten)
  remote   - Cloud synced (Todoist integration)
  apple    - Apple Notes exported to Obsidian
  assets   - Assets and attachments
  second   - Local second brain

Examples:
  brain vaults
  brain search "python" --all
  brain tasks --all
  brain add-task "Call mom" apple
        """)


if __name__ == "__main__":
    main()
