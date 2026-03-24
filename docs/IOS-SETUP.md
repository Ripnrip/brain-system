# iOS Shortcuts Setup Guide

## Prerequisites

1. **Mac Requirements:**
   - Brain System installed at `~/.brain/brain`
   - Python 3.11+ with Flask
   - Brain web server running (see below)

2. **iOS Requirements:**
   - iPhone/iPad with iOS 17+
   - Shortcuts app (installed by default)
   - Same local network as your Mac

---

## Step 1: Start the Brain Server

On your Mac, start the brain web server with URL scheme support:

```bash
cd ~/Library/Mobile\ Documents/iCloud~md~obsidian/Documents/Brain-System
python3 server/brain_server.py
```

The server will start on `http://0.0.0.0:5789` and display your local IP address.

**Optional: Run as a background service**

```bash
# Create LaunchAgent for auto-start
~/Library/Mobile\ Documents/iCloud~md~obsidian/Documents/Brain-System/server/install-service.sh
```

---

## Step 2: Install the Shortcuts

### Method A: AirDrop (Recommended)

1. On your Mac, open the shortcuts folder in Finder:
   ```
   open ~/Library/Mobile\ Documents/iCloud~md~obsidian/Documents/Brain-System/shortcuts
   ```

2. AirDrop each `.shortcut` file to your iPhone/iPad

3. When prompted, tap "Add Shortcut" for each one

### Method B: iCloud Drive

1. Copy shortcuts to iCloud Drive/Shortcuts folder
2. On iOS, open Files app > iCloud Drive > Shortcuts
3. Tap each shortcut to import

---

## Step 3: Configure Your Server IP

After installing, you need to tell shortcuts where your brain server is:

1. Open any installed shortcut
2. Find the "Get Server IP" or similar text variable
3. Replace `YOUR_MAC_IP` with your actual Mac's IP address
   - Find it by running on Mac: `ipconfig getifaddr en0`
   - Example: `192.168.1.100`

**Pro Tip:** Create a "Set Brain Server" shortcut to update all shortcuts at once.

---

## Available Shortcuts

| Shortcut | Description | URL Scheme |
|----------|-------------|------------|
| **Quick Note** | Add note to realm vault | `brain://add-note` |
| **Quick Search** | Search brain from iOS | `brain://search` |
| **Quick Task** | Add task to brain | `brain://add-task` |
| **View Graph** | Open graph view | `brain://graph` |
| **Sync Now** | Trigger sync | `brain://sync` |
| **Today's Notes** | Show notes created today | `brain://today` |
| **Get Tasks** | List pending tasks | `brain://tasks` |
| **Open Vault** | Open in Obsidian | `brain://open` |

---

## Step 4: Add to Home Screen (Optional)

For quick access:

1. Long-press on a shortcut in the app
2. Select "Details"
3. Toggle "Add to Home Screen"
4. Arrange icons on your home screen

建议排列:
```
[Quick Note] [Quick Task] [Quick Search]
[Today's Notes] [Get Tasks] [View Graph]
[Sync Now]
```

---

## Step 5: Configure Widget (Optional)

Add a brain widget to your home screen:

1. Long-press home screen > Tap "+"
2. Search "Shortcuts"
3. Choose "Quick Note" or "Quick Task"
4. Place widget for 1-tap access

---

## Troubleshooting

### "Could not connect to server"

- Ensure your Mac and iOS device are on the same network
- Check brain server is running on Mac
- Verify IP address is correct in shortcut
- Try `http://YOUR_MAC_IP:5789` in Safari to test

### "Vault not found"

- Run `brain vaults` on Mac to see available vaults
- Check vault paths in `~/.brain/brain`

### Shortcut runs but nothing happens

- Open shortcut in editor and run step-by-step
- Check the "Get Contents of URL" step for errors
- Ensure URL scheme is formatted correctly

### Slow response

- Run `brain sync` on Mac to update indices
- Check for large vaults (consider limiting search results)

---

## Advanced Configuration

### Custom Vaults per Shortcut

Edit a shortcut to change the default vault:

1. Open shortcut editor
2. Find the URL construction step
3. Change `vault=realm` to your preferred vault

### Custom Folders for Notes

When adding notes, specify PARA folder:

```
brain://add-note?content=My%20note&folder=Projects
```

Options: `Inbox`, `Projects`, `Areas`, `Resources`, `Archives`

### Siri Integration

Add Siri phrases to shortcuts:

1. Open shortcut > Details > "Add to Siri"
2. Record phrase like "Add to brain" or "Search my brain"

---

## Security Notes

- Brain server only listens on your local network
- No data is sent to external servers
- Consider using a VPN if accessing from remote networks
- Keep your Mac updated with security patches

---

## Next Steps

1. Test each shortcut to ensure connectivity
2. Customize shortcuts for your workflow
3. Set up the LaunchAgent for auto-start on Mac boot
4. Explore the graph view on your iPad

Enjoy your brain from anywhere!
