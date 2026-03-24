# iOS Shortcuts Guide

Access Brain-System from your iPhone using iOS Shortcuts and the web interface.

## Table of Contents

- [Setup](#setup)
- [Web Interface on iOS](#web-interface-on-ios)
- [iOS Shortcuts](#ios-shortcuts)
- [Siri Integration](#siri-integration)
- [Home Screen Widgets](#home-screen-widgets)

## Setup

### Prerequisites

1. Brain-System web server running on your Mac
2. Mac and iPhone on same network
3. iOS Shortcuts app installed

### Find Your Mac's IP Address

```bash
# On your Mac
ipconfig getifaddr en0  # WiFi
# or
ipconfig getifaddr en1  # Ethernet
```

Example output: `192.168.1.100`

### Start Web Server

On your Mac:

```bash
cd ~/Library/Mobile\ Documents/iCloud~md~obsidian/Documents/Brain-System
python3 web.py
```

The server will be available at `http://your-ip:5789`

## Web Interface on iOS

### Access from Safari

1. Open Safari on iPhone
2. Navigate to `http://your-mac-ip:5789`
3. Test search functionality

### Add to Home Screen

1. Open the web interface in Safari
2. Tap Share button
3. Scroll down and tap "Add to Home Screen"
4. Name it "Brain Search"
5. Tap "Add"

Now you can access Brain-System like a native app!

## iOS Shortcuts

### Create "Brain Search" Shortcut

1. Open Shortcuts app
2. Tap `+` to create new shortcut
3. Add actions:

```
1. Ask for Input
   - Prompt: "Search brain"
   - Input type: Text

2. Get Contents of URL
   - URL: http://your-mac-ip:5789/search?q={Ask for Input}
   - Method: GET

3. Dictionary
   - Get "results" from Get Contents of URL

4. Repeat with Each
   - For each item in dictionary
   - Show result
```

4. Name shortcut: "Brain Search"
5. Add to Home Screen

### Create "Quick Add Task" Shortcut

```
1. Ask for Input
   - Prompt: "New task"
   - Input type: Text

2. Ask for Input
   - Prompt: "Which vault?"
   - Input type: Menu
   - Options: realm, remote, apple

3. Get Contents of URL
   - URL: http://your-mac-ip:5789/add-task?task={Ask for Input}&vault={Ask for Input}
   - Method: GET

4. Show Notification
   - Text: "Task added: {Ask for Input}"
```

### Create "Get Tasks" Shortcut

```
1. Get Contents of URL
   - URL: http://your-mac-ip:5789/tasks
   - Method: GET

2. Dictionary
   - Get "tasks" from contents

3. Repeat with Each
   - Show each task
```

### Create "Brain Stats" Shortcut

```
1. Get Contents of URL
   - URL: http://your-mac-ip:5789/api/stats
   - Method: GET

2. Show Result
```

## Siri Integration

### Add Siri Phrases

1. Open Settings > Siri & Search
2. Find your shortcuts
3. Add custom phrases:

| Shortcut | Siri Phrase |
|----------|-------------|
| Brain Search | "Search my brain" |
| Quick Add Task | "Add to brain" |
| Get Tasks | "Show my tasks" |
| Brain Stats | "Brain stats" |

### Example Usage

- "Hey Siri, search my brain for python"
- "Hey Siri, add to brain: buy milk"
- "Hey Siri, show my tasks"

## Home Screen Widgets

### Create Task Widget

1. Create "Get Tasks" shortcut (above)
2. Long press on home screen
3. Tap `+` in top left
4. Search for "Shortcuts"
5. Choose "Get Tasks" shortcut
6. Select widget size
7. Add widget

### Smart Stack

Add multiple brain shortcuts to a Smart Stack:

1. Create all shortcuts
2. Add them to home screen
3. Long press and stack them together

## Advanced Shortcuts

### Search Specific Vault

```
1. Choose from Menu
   - Options: realm, remote, apple, assets, second

2. Ask for Input
   - Prompt: "Search term"

3. Get Contents of URL
   - URL: http://your-mac-ip:5789/search?q={Ask for Input}&vault={Choose from Menu}

4. Show Results
```

### View Graph

```
1. Open URL
   - URL: http://your-mac-ip:5789/graph-view
```

### Daily Note with Tasks

```
1. Get Contents of URL
   - URL: http://your-mac-ip:5789/tasks

2. Create Note
   - In: Notes app or Obsidian
   - Title: "Daily - {Current Date}"
   - Body: {Tasks from step 1}
```

### Capture Quick Note

```
1. Ask for Input
   - Prompt: "Quick capture"

2. Get Contents of URL
   - URL: http://your-mac-ip:5789/capture?note={Ask for Input}
   - Method: POST

3. Show Confirmation
```

## Troubleshooting

### Can't Connect from iPhone

1. **Check Mac is awake** - Mac must not be sleeping
2. **Check same network** - Both devices on same WiFi
3. **Check firewall** - Allow Python in System Settings > Security
4. **Check IP address** - May have changed

```bash
# Verify Mac is listening
lsof -i :5789

# Get current IP
ipconfig getifaddr en0
```

### Slow Loading

1. **Reduce graph data** - Edit graph.html limit
2. **Use 5GHz WiFi** - Faster than 2.4GHz
3. **Limit search results** - Add &limit=10 to URL

### Auto-Start Web Server

Create LaunchAgent for web server:

```xml
<!-- ~/Library/LaunchAgents/com.brain.web.plist -->
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

## Alternative: ngrok for Remote Access

For access outside your home network:

1. Install ngrok:
```bash
brew install ngrok
```

2. Start ngrok:
```bash
ngrok http 5789
```

3. Use ngrok URL in iOS shortcuts

## Recommended Setup

### Home Screen Layout

```
[Brain Search]  [Tasks]  [Add Task]
[Brain Graph]   [Stats]
```

### Today View

Add to Today View (left of home screen):
- Brain Tasks widget
- Quick actions

### Apple Watch

Create complications for:
- Task count
- Quick search trigger
- Voice dictation capture

## Future Enhancements

- [ ] Native iOS app (planned for v2.0)
- [ ] Apple Watch app
- [ ] Share sheet integration
- [ ] Widget improvements
- [ ] Local-only mode (no Mac required)

## Example Shortcut Configurations

### JSON Export for Import

Save this as `brain-search.shortcut` and import:

```json
{
  "WFWorkflowActions": [
    {
      "WFWorkflowActionIdentifier": "is.workflow.actions.comment",
      "WFWorkflowActionParameters": {
        "WFCommentActionText": "Search your brain"
      }
    }
  ],
  "WFWorkflowClientVersion": "2302.0.5",
  "WFWorkflowTypes": ["NCWidget", "WatchKit"]
}
```

## Community Shortcuts

Share your shortcuts with the community!

1. Export shortcut
2. Upload to iCloud or Reddit
3. Share link with #BrainSystem hashtag
