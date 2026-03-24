# Brain URL Schemes Documentation

## Overview

The Brain System supports custom URL schemes for iOS integration via the Shortcuts app. This allows you to interact with your vaults directly from your iPhone or iPad.

## Base URL

```
brain://
```

## Available Endpoints

### 1. Quick Note - Add a new note

**Scheme:** `brain://add-note`

**Parameters:**
- `content` (required) - Note content
- `vault` (optional) - Target vault (default: realm)
- `folder` (optional) - PARA folder (Inbox, Projects, Areas, Resources, Archives)
- `tags` (optional) - Comma-separated tags

**Examples:**
```
brain://add-note?content=Meeting%20notes%20today
brain://add-note?content=Project%20idea&folder=Projects&tags=work,idea
brain://add-note?content=Quick%20thought&vault=remote
```

**Response:** JSON confirmation with note ID and file path

---

### 2. Quick Search - Search your brain

**Scheme:** `brain://search`

**Parameters:**
- `q` (required) - Search query
- `vault` (optional) - Specific vault or "all" (default: current)
- `limit` (optional) - Max results (default: 20)

**Examples:**
```
brain://search?q=python
brain://search?q=project%20alpha&vault=all
brain://search?q=tasks&limit=50
```

**Response:** JSON array of matching notes with title, preview, and vault

---

### 3. Quick Task - Add a task

**Scheme:** `brain://add-task`

**Parameters:**
- `content` (required) - Task description
- `vault` (optional) - Target vault (default: realm)
- `priority` (optional) - Priority 1-3 (default: 2)
- `due` (optional) - Due date (ISO format)

**Examples:**
```
brain://add-task?content=Call%20mom%20Sunday
brain://add-task?content=Review%20PR&priority=1&vault=remote
brain://add-task?content=Finish%20report&due=2026-03-25
```

**Response:** JSON confirmation with task ID

---

### 4. View Graph - Open graph visualization

**Scheme:** `brain://graph`

**Parameters:**
- `vault` (optional) - Specific vault or "all" (default: all)
- `filter` (optional) - Filter notes by keyword

**Examples:**
```
brain://graph
brain://graph?vault=realm
brain://graph?filter=project
```

**Response:** Redirects to web graph view

---

### 5. Sync Now - Trigger vault sync

**Scheme:** `brain://sync`

**Parameters:**
- `vault` (optional) - Specific vault or omit for all

**Examples:**
```
brain://sync
brain://sync?vault=realm
```

**Response:** JSON sync status

---

### 6. Today's Notes - Show notes created today

**Scheme:** `brain://today`

**Parameters:**
- `vault` (optional) - Specific vault or "all" (default: all)

**Examples:**
```
brain://today
brain://today?vault=realm
```

**Response:** JSON array of today's notes

---

### 7. Get Tasks - List pending tasks

**Scheme:** `brain://tasks`

**Parameters:**
- `vault` (optional) - Specific vault or "all" (default: current)
- `completed` (optional) - Include completed tasks (true/false)

**Examples:**
```
brain://tasks
brain://tasks?vault=all
brain://tasks?completed=true
```

**Response:** JSON array of tasks

---

### 8. Open Vault - Open in Obsidian

**Scheme:** `brain://open`

**Parameters:**
- `vault` (required) - Vault name to open

**Examples:**
```
brain://open?vault=realm
brain://open?vault=remote
```

**Response:** Opens Obsidian to the specified vault

---

## Response Format

All endpoints return JSON responses:

```json
{
  "success": true,
  "data": { ... },
  "message": "Operation completed"
}
```

Error responses:
```json
{
  "success": false,
  "error": "Error message"
}
```

---

## Available Vaults

| Vault | Description |
|-------|-------------|
| realm | Main second brain (PARA, Zettelkasten) |
| remote | Cloud-synced vault with Todoist integration |
| apple | Apple Notes archive |
| assets | Attachments and media |
| second | Local development/backup |

---

## Security Notes

- URL schemes work on your local network only
- The brain server must be running on your Mac
- No data is sent to external servers
- All requests stay within your local network
