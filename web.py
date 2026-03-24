#!/usr/bin/env python3
"""
Brain Web Server - Access your vaults from any device
With graph visualization, clustering, and search
"""

import os
import json
import sqlite3
import hashlib
from pathlib import Path
from flask import Flask, render_template_string, request, jsonify
from datetime import datetime
import re

# Inline vault config (same as multi-brain.py)
VAULTS = {
    "realm": {
        "path": Path(os.path.expanduser("~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Realm-Obsidian")),
        "db": Path(os.path.expanduser("~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Realm-Obsidian/brain/brain.db")),
        "color": "#6366f1"
    },
    "remote": {
        "path": Path(os.path.expanduser("~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Remote-Vault")),
        "db": Path(os.path.expanduser("~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Remote-Vault/brain/brain.db")),
        "color": "#f59e0b"
    },
    "apple": {
        "path": Path(os.path.expanduser("~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Apple Notes")),
        "db": Path(os.path.expanduser("~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Apple Notes/brain/brain.db")),
        "color": "#22c55e"
    },
    "assets": {
        "path": Path(os.path.expanduser("~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Apple Notes Assets")),
        "db": Path(os.path.expanduser("~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Apple Notes Assets/brain/brain.db")),
        "color": "#8b5cf6"
    },
    "second": {
        "path": Path(os.path.expanduser("~/Documents/SecondBrain")),
        "db": Path(os.path.expanduser("~/Documents/SecondBrain/brain/brain.db")),
        "color": "#ec4899"
    }
}

def get_vault_stats(vault_name):
    """Get stats for a single vault"""
    config = VAULTS.get(vault_name)
    if not config or not config["db"].exists():
        return {"notes": 0}

    try:
        conn = sqlite3.connect(config["db"])
        cursor = conn.execute("SELECT COUNT(*) FROM notes")
        return {"notes": cursor.fetchone()[0]}
    except:
        return {"notes": 0}

app = Flask(__name__)

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧠 Brain Search</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            color: #eee;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .header h1 {
            font-size: 2rem;
            margin-bottom: 5px;
        }
        .stats {
            opacity: 0.7;
            font-size: 0.9rem;
        }
        .search-box {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .search-box input {
            width: 100%;
            padding: 15px 20px;
            font-size: 1.1rem;
            border: none;
            border-radius: 10px;
            background: rgba(255,255,255,0.15);
            color: #fff;
        }
        .search-box input::placeholder {
            color: rgba(255,255,255,0.5);
        }
        .search-box input:focus {
            outline: none;
            background: rgba(255,255,255,0.2);
        }
        .vault-toggle {
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
            flex-wrap: wrap;
        }
        .vault-btn {
            padding: 8px 16px;
            border: 1px solid rgba(255,255,255,0.3);
            border-radius: 20px;
            background: transparent;
            color: #fff;
            cursor: pointer;
            font-size: 0.85rem;
            transition: all 0.2s;
        }
        .vault-btn.active {
            background: rgba(255,255,255,0.2);
            border-color: #fff;
        }
        .vault-btn:hover {
            background: rgba(255,255,255,0.1);
        }
        .results {
            display: grid;
            gap: 15px;
        }
        .note-card {
            background: rgba(255,255,255,0.08);
            border-radius: 12px;
            padding: 15px;
            border: 1px solid rgba(255,255,255,0.1);
            transition: transform 0.2s;
        }
        .note-card:hover {
            transform: translateY(-2px);
            background: rgba(255,255,255,0.12);
        }
        .note-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        .note-title {
            font-weight: 600;
            font-size: 1.05rem;
        }
        .note-vault {
            font-size: 0.75rem;
            padding: 3px 10px;
            border-radius: 12px;
            background: rgba(99, 102, 241, 0.3);
            color: #a5b4fc;
        }
        .note-preview {
            font-size: 0.9rem;
            opacity: 0.8;
            line-height: 1.5;
            max-height: 100px;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .loading {
            text-align: center;
            padding: 40px;
            opacity: 0.6;
        }
        .no-results {
            text-align: center;
            padding: 40px;
            opacity: 0.5;
        }
        @media (max-width: 600px) {
            .header h1 { font-size: 1.5rem; }
            .note-card { padding: 12px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 Brain Search</h1>
            <p class="stats">{{ stats }}</p>
            <p style="margin-top: 10px;">
                <a href="/graph-view" style="color: #8b5cf6; text-decoration: none; font-weight: 500;">🕸️ View Graph</a>
            </p>
        </div>

        <div class="search-box">
            <div class="vault-toggle">
                <button class="vault-btn active" data-vault="all">All Vaults</button>
                <button class="vault-btn" data-vault="realm">Realm (692)</button>
                <button class="vault-btn" data-vault="apple">Apple (662)</button>
                <button class="vault-btn" data-vault="remote">Remote (29)</button>
                <button class="vault-btn" data-vault="second">Second (37)</button>
            </div>
            <input type="text" id="search" placeholder="Search your brain..." autofocus>
        </div>

        <div class="results" id="results">
            <div class="no-results">
                <p>🔍 Start typing to search...</p>
            </div>
        </div>
    </div>

    <script>
        let currentVault = 'all';
        let debounceTimer;

        document.querySelectorAll('.vault-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.vault-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentVault = btn.dataset.vault;
                doSearch();
            });
        });

        document.getElementById('search').addEventListener('input', () => {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(doSearch, 300);
        });

        async function doSearch() {
            const query = document.getElementById('search').value;
            const results = document.getElementById('results');

            if (!query) {
                results.innerHTML = '<div class="no-results"><p>🔍 Start typing to search...</p></div>';
                return;
            }

            results.innerHTML = '<div class="loading"><p>Searching...</p></div>';

            try {
                const response = await fetch(`/search?q=${encodeURIComponent(query)}&vault=${currentVault}`);
                const data = await response.json();

                if (data.results.length === 0) {
                    results.innerHTML = '<div class="no-results"><p>No results found</p></div>';
                    return;
                }

                results.innerHTML = data.results.map(note => `
                    <div class="note-card">
                        <div class="note-header">
                            <span class="note-title">${escapeHtml(note.title)}</span>
                            <span class="note-vault">${note.vault}</span>
                        </div>
                        <div class="note-preview">${escapeHtml(note.content?.substring(0, 200) || '')}</div>
                        ${note.tags ? `<div class="note-tags">🏷️ ${escapeHtml(note.tags)}</div>` : ''}
                    </div>
                `).join('');
            } catch (error) {
                results.innerHTML = '<div class="no-results"><p>Error searching</p></div>';
            }
        }

        function escapeHtml(text) {
            if (!text) return '';
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        // Focus search on load
        document.getElementById('search').focus();
    </script>
</body>
</html>
"""

def get_total_stats():
    """Get total statistics across all vaults"""
    total_notes = 0
    for name in VAULTS:
        stats = get_vault_stats(name)
        total_notes += stats['notes']
    return f"{total_notes:,} notes across {len(VAULTS)} vaults"

@app.route('/')
def home():
    stats = get_total_stats()
    return render_template_string(HTML_TEMPLATE, stats=stats)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    vault = request.args.get('vault', 'all')

    if not query:
        return jsonify({'results': []})

    results = []
    vaults_to_search = VAULTS.keys() if vault == 'all' else [vault]

    for vault_name in vaults_to_search:
        config = VAULTS.get(vault_name)
        if not config or not config["db"].exists():
            continue

        try:
            conn = sqlite3.connect(config["db"])
            conn.row_factory = sqlite3.Row
            vault_results = conn.execute("""
                SELECT id, title, content, tags, vault
                FROM notes
                WHERE content LIKE ? OR title LIKE ?
                ORDER BY updated_at DESC LIMIT 20
            """, (f"%{query}%", f"%{query}%")).fetchall()

            for note in vault_results:
                results.append({
                    'id': note['id'],
                    'title': note['title'],
                    'content': note['content'][:500] if note['content'] else '',
                    'tags': note['tags'] if note['tags'] else '',
                    'vault': note['vault'] if note['vault'] else vault_name
                })
        except Exception as e:
            pass

    results = results[:20]
    return jsonify({'results': results})

@app.route('/api/stats')
def api_stats():
    stats = {}
    for name in VAULTS:
        stats[name] = get_vault_stats(name)
    return jsonify(stats)

@app.route('/graph')
def graph_data():
    """Get enhanced graph data with more connections"""
    vault = request.args.get('vault', 'all')
    search_query = request.args.get('q', '').lower()
    vaults_to_search = VAULTS.keys() if vault == 'all' else [vault]

    points = []
    links = []
    title_to_index = {}
    link_set = set()

    # First pass: collect all points
    for vault_name in vaults_to_search:
        config = VAULTS.get(vault_name)
        if not config or not config["db"].exists():
            continue

        try:
            conn = sqlite3.connect(config["db"])
            conn.row_factory = sqlite3.Row

            # Get notes with content
            notes = conn.execute("""
                SELECT id, title, content, tags, vault, para_folder
                FROM notes
                LIMIT 1000
            """).fetchall()

            for note in notes:
                # Apply search filter if provided
                if search_query:
                    content = (note['content'] or '').lower()
                    title = note['title'].lower()
                    if search_query not in content and search_query not in title:
                        continue

                idx = len(points)
                content = note['content'] or ''
                wikilink_count = len(re.findall(r'\[\[([^\]]+)\]\]', content))

                # Extract words for similarity matching
                words = set(re.findall(r'\b[a-zA-Z]{3,}\b', content.lower()))

                points.append({
                    'id': note['id'],
                    'title': note['title'],
                    'content': content[:500],
                    'tags': note['tags'],
                    'vault': note['vault'] if note['vault'] else vault_name,
                    'folder': note['para_folder'],
                    'connections': wikilink_count,
                    'words': list(words)  # Convert set to list for JSON serialization
                })

                title_key = f"{vault_name}:{note['title']}"
                title_to_index[title_key] = idx

        except Exception as e:
            pass

    # Early return if no points
    if not points:
        return jsonify({'points': [], 'links': []})

    # Second pass: create wikilink connections
    for i, point in enumerate(points):
        if point['content']:
            # Find all wikilinks [[note]]
            for match in re.finditer(r'\[\[([^\]]+)\]\]', point['content']):
                linked_title = match.group(1).strip().lower()
                # Try exact match
                if linked_title in title_to_index:
                    j = title_to_index[linked_title]
                    if i != j:
                        link_key = tuple(sorted([i, j]))
                        if link_key not in link_set:
                            links.append({'source': i, 'target': j, 'type': 'wikilink'})
                            link_set.add(link_key)
                            points[j]['connections'] = points[j].get('connections', 0) + 1
                else:
                    # Partial match
                    for title_key, j in title_to_index.items():
                        if linked_title in title_key.lower() and i != j:
                            link_key = tuple(sorted([i, j]))
                            if link_key not in link_set:
                                links.append({'source': i, 'target': j, 'type': 'wikilink'})
                                link_set.add(link_key)
                                break

    # Create word-to-points index for similarity linking
    word_to_points = {}
    for i, point in enumerate(points):
        for word in point.get('words', []):
            if word not in word_to_points:
                word_to_points[word] = []
            word_to_points[word].append(i)

    # Create links based on shared words (content similarity)
    for word, indices in word_to_points.items():
        # Skip very common words
        if len(indices) < 2 or len(indices) > 30:
            continue
        # Connect notes that share meaningful words
        for i_idx in range(min(len(indices) - 1, 5)):
            i = indices[i_idx]
            j = indices[(i_idx + 1) % len(indices)]
            if i != j:
                link_key = tuple(sorted([i, j]))
                if link_key not in link_set:
                    links.append({'source': i, 'target': j, 'type': 'similar'})
                    link_set.add(link_key)
                    points[i]['connections'] = points[i].get('connections', 0) + 1
                    points[j]['connections'] = points[j].get('connections', 0) + 1

    # Create tag-based links
    tag_to_points = {}
    for i, point in enumerate(points):
        try:
            note_tags = json.loads(point['tags']) if point['tags'] else []
            for tag in note_tags:
                if isinstance(tag, str) and tag and len(tag) < 50:
                    if tag not in tag_to_points:
                        tag_to_points[tag] = []
                    tag_to_points[tag].append(i)
        except:
            pass

    # Link notes sharing tags
    for tag, indices in tag_to_points.items():
        if 2 <= len(indices) <= 100:
            max_links = min(len(indices) * 3, 30)
            for i_idx in range(max_links):
                i = indices[i_idx % len(indices)]
                j = indices[(i_idx + 1) % len(indices)]
                if i != j:
                    link_key = tuple(sorted([i, j]))
                    if link_key not in link_set:
                        links.append({'source': i, 'target': j, 'type': 'tag'})
                        link_set.add(link_key)

    # Create folder-based links
    folder_points = {}
    for i, point in enumerate(points):
        folder = point.get('folder')
        if folder and folder not in ['Inbox', None]:
            if folder not in folder_points:
                folder_points[folder] = []
            folder_points[folder].append(i)

    # Link notes in same folder (with clustering)
    for folder, indices in folder_points.items():
        if len(indices) > 1:
            # Create cluster connections
            for i in range(min(len(indices), 30)):
                # Connect each point to 2-3 nearest in the array
                for offset in [1, 2, 3]:
                    j = indices[(i + offset) % len(indices)]
                    if i != j:
                        link_key = tuple(sorted([indices[i], j]))
                        if link_key not in link_set:
                            links.append({'source': indices[i], 'target': j, 'type': 'folder'})
                            link_set.add(link_key)

    # Create inter-vault links (connect related notes across vaults)
    if vault == 'all':
        for i in range(min(len(points) - 1, 100)):
            j = (i + 1) % len(points)
            link_key = tuple(sorted([i, j]))
            if link_key not in link_set and points[i]['vault'] != points[j]['vault']:
                # Only connect if they have some similarity
                i_words = points[i].get('words', set())
                j_words = points[j].get('words', set())
                similarity = len(i_words & j_words)
                if similarity > 5:  # At least 5 shared words
                    links.append({'source': i, 'target': j, 'type': 'cross-vault'})
                    link_set.add(link_key)

    return jsonify({
        'points': points,
        'links': links[:5000],  # Increased limit
        'stats': {
            'total_points': len(points),
            'total_links': len(links),
            'vaults': len(set(p['vault'] for p in points))
        }
    })

@app.route('/graph-view')
def graph_view():
    """Serve the enhanced graph visualization page"""
    with open(Path(__file__).parent / 'graph.html') as f:
        return f.read()

if __name__ == '__main__':
    print("\n🌐 Brain Web Server + Graph View")
    print("=" * 50)

    LOCAL_IP = os.popen("ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo 'localhost'").read().strip()

    print("📱 Open on your devices:")
    print(f"   Search:  http://{LOCAL_IP}:5555")
    print(f"   Graph:   http://{LOCAL_IP}:5555/graph-view")
    print("")
    print("Press Ctrl+C to stop")
    print("=" * 50 + "\n")

    app.run(host='0.0.0.0', port=5789, debug=False)
