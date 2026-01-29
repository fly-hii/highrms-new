# Debugging the Extension

## Viewing Logs

### 1. Browser Console (Extension Popup)
1. Right-click on the extension popup
2. Select "Inspect" or "Inspect Popup"
3. Go to the "Console" tab
4. All logs prefixed with `[Popup]` will appear here

### 2. Service Worker Console (Background Script)
1. Go to `chrome://extensions/` (or `edge://extensions/`)
2. Find "Horilla Activity Monitor"
3. Click "Inspect views: service worker" or "background page"
4. Go to the "Console" tab
5. All logs prefixed with `[Background]` will appear here

### 3. Content Script Console
1. Open the HRMS page
2. Press F12 to open DevTools
3. Go to the "Console" tab
4. All logs prefixed with `[Content]` will appear here

### 4. Extension Popup Logs Panel
- The popup now shows logs in a scrollable panel
- Click "Show Logs" / "Hide Logs" to toggle visibility
- Logs are color-coded:
  - Blue: Info
  - Green: Success
  - Red: Error
  - Orange: Warning

## Common Issues

### Extension stuck on "Initializing..."
- Check browser console for errors
- Verify all files are loaded correctly
- Check if there are JavaScript errors preventing initialization

### "Not Authenticated" error
- Make sure you're logged into HRMS
- The extension needs to be on the HRMS page to access cookies
- Try refreshing the HRMS page and logging in again

### "Not Checked In" error
- Check in via the attendance system first
- The extension can only start monitoring when you're checked in

### Connection errors
- Verify the API URL is correct
- Make sure the Django server is running
- Check CORS settings if using a different domain

## Testing Steps

1. Open extension popup
2. Check logs panel - should show initialization messages
3. Enter API URL and click "Save & Test Connection"
4. Watch logs for connection test results
5. If on HRMS page and logged in, monitoring should start automatically
6. Check background script console for heartbeat logs

