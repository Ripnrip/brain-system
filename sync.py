#!/usr/bin/env python3
"""
Vault Sync Script - Standalone version for each vault
Run this to import markdown files into the local database
"""

import sqlite3
import json
import os
from datetime import datetime
from pathlib import Path
import hashlib

# Auto-detect vault from current directory
def get_vault_config():
    cwd = Path.cwd()
    # Check if we're in a vault
    if (cwd / ".obsidian").exists():
        return cwd
    # Check parent directories
    for parent in [cwd] + list(cwd.parents):
        if (parent / ".obsidian").exists():
            return parent
    # Default to current directory
    return cwd

VAULT_PATH = get_vault_config()
DB_PATH = VAULT_PATH / "brain" / "brain.db"
VAULT_NAME = VAULT_PATH.name

class BrainDB:
    def __init__(self):
        self.db_path = DB_PATH
        self.vault_path = VAULT_PATH
        self.vault_name = VAULT_NAME
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.init_db()

    def init_db(self):
        """Initialize database schema"""
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
            CREATE INDEX IF NOT EXISTS idx_notes_tags ON notes(tags);
            CREATE INDEX IF NOT EXISTS idx_notes_updated ON notes(updated_at);
            CREATE INDEX IF NOT EXISTS idx_tasks_vault ON tasks(vault);
        """)
        self.conn.commit()
        print(f"✅ Database initialized: {self.db_path}")

    def upsert_note(self, file_path, title, content, yaml_data, tags):
        """Insert or update a note"""
        file_path = str(file_path)
        file_id = f"{self.vault_name}_{hashlib.md5(file_path.encode()).hexdigest()}"

        now = datetime.now().isoformat()
        yaml_str = json.dumps(yaml_data) if yaml_data else "{}"
        tags_str = json.dumps(tags) if tags else "[]"

        # Determine PARA folder
        para_folder = None
        path_parts = Path(file_path).relative_to(self.vault_path).parts
        for folder in ["Inbox", "Projects", "Areas", "Resources", "Archives"]:
            if folder in path_parts or any(folder.replace(" ", "").lower() in p.lower() for p in path_parts):
                para_folder = folder
                break

        self.conn.execute("""
            INSERT OR REPLACE INTO notes
            (id, file_path, title, content, yaml_frontmatter, tags, vault, para_folder, created_at, updated_at, synced)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?,
                COALESCE((SELECT created_at FROM notes WHERE id = ?), ?),
                ?, 0)
        """, (file_id, file_path, title, content, yaml_str, tags_str,
              self.vault_name, para_folder, file_id, now, now))
        self.conn.commit()
        return file_id

    def get_note(self, note_id):
        """Get a note by ID"""
        cursor = self.conn.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
        return cursor.fetchone()

    def search_notes(self, query, limit=20):
        """Full-text search in notes"""
        cursor = self.conn.execute("""
            SELECT id, title, content, tags, file_path
            FROM notes
            WHERE content LIKE ? OR title LIKE ? OR tags LIKE ?
            ORDER BY updated_at DESC
            LIMIT ?
        """, (f"%{query}%", f"%{query}%", f"%{query}%", limit))
        return cursor.fetchall()

    def get_by_para(self, folder):
        """Get notes by PARA folder"""
        cursor = self.conn.execute("""
            SELECT * FROM notes WHERE para_folder = ?
            ORDER BY updated_at DESC
        """, (folder,))
        return cursor.fetchall()

    def add_task(self, content, note_id=None, due_date=None, priority=2):
        """Add a task"""
        task_id = f"{self.vault_name}_{datetime.now().timestamp()}"
        now = datetime.now().isoformat()

        self.conn.execute("""
            INSERT OR REPLACE INTO tasks (id, note_id, content, due_date, priority, vault, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (task_id, note_id, content, due_date, priority, self.vault_name, now))
        self.conn.commit()
        return task_id

    def get_tasks(self, include_completed=False):
        """Get all tasks"""
        if include_completed:
            cursor = self.conn.execute("SELECT * FROM tasks ORDER BY created_at DESC")
        else:
            cursor = self.conn.execute("SELECT * FROM tasks WHERE completed = 0 ORDER BY priority DESC, created_at DESC")
        return cursor.fetchall()

    def get_stats(self):
        """Get vault statistics"""
        cursor = self.conn.execute("SELECT COUNT(*) FROM notes")
        notes_count = cursor.fetchone()[0]

        cursor = self.conn.execute("SELECT COUNT(DISTINCT para_folder) FROM notes WHERE para_folder IS NOT NULL")
        folder_count = cursor.fetchone()[0]

        cursor = self.conn.execute("SELECT COUNT(*) FROM tasks WHERE completed = 0")
        task_count = cursor.fetchone()[0]

        return {
            "vault": self.vault_name,
            "notes": notes_count,
            "folders": folder_count,
            "pending_tasks": task_count,
            "db_path": str(self.db_path),
            "vault_path": str(self.vault_path)
        }

    def import_vault(self, vault_path=None):
        """Import all markdown files from vault"""
        vault_path = vault_path or self.vault_path
        count = 0

        for md_file in Path(vault_path).rglob("*.md"):
            # Skip system files
            if ".git" in str(md_file) or "brain/" in str(md_file):
                continue

            try:
                content = md_file.read_text()

                # Parse frontmatter
                yaml_data = {}
                content_body = content
                tags = []
                title = md_file.stem

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

                self.upsert_note(md_file, title, content_body, yaml_data, tags)
                count += 1

            except Exception as e:
                print(f"Error importing {md_file}: {e}")

        self.conn.commit()
        return count


if __name__ == "__main__":
    import sys

    db = BrainDB()
    print(f"\n🧠 Brain DB: {db.vault_name}")
    print(f"📁 Vault: {db.vault_path}")

    cmd = sys.argv[1] if len(sys.argv) > 1 else "import"

    if cmd == "import" or cmd == "sync":
        count = db.import_vault()
        print(f"✅ Imported {count} notes")

        stats = db.get_stats()
        print(f"\n📊 {stats['vault']}:")
        print(f"   • {stats['notes']} notes")
        print(f"   • {stats['folders']} PARA folders")
        print(f"   • {stats['pending_tasks']} pending tasks")

    elif cmd == "search" and len(sys.argv) > 2:
        query = sys.argv[2]
        results = db.search_notes(query)
        print(f"\n🔍 Found {len(results)} results for '{query}':")
        for note in results[:10]:
            print(f"  • {note['title']}")

    elif cmd == "tasks":
        tasks = db.get_tasks()
        print(f"\n✅ Tasks ({len(tasks)} pending):")
        for task in tasks[:10]:
            print(f"  ☐ {task['content']}")

    elif cmd == "stats":
        stats = db.get_stats()
        print(f"\n📊 {stats['vault']}:")
        print(f"   Notes: {stats['notes']}")
        print(f"   Folders: {stats['folders']}")
        print(f"   Tasks: {stats['pending_tasks']}")
