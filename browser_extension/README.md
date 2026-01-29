# Horilla Activity Monitor Browser Extension

Browser extension for tracking employee work activity during check-in/check-out sessions.

## Installation

1. Open Chrome/Edge browser
2. Go to `chrome://extensions/` (or `edge://extensions/`)
3. Enable "Developer mode"
4. Click "Load unpacked"
5. Select the `browser_extension` directory

## Configuration

1. Click the extension icon in the browser toolbar
2. Enter the API base URL (e.g., `http://localhost:8000` or your production URL)
3. Click "Save Configuration"

## Usage

1. Employee checks in via Horilla HRMS
2. Extension automatically requests a session token
3. Monitoring starts automatically
4. Extension sends heartbeat every 30 seconds
5. Activity logs are sent periodically
6. When employee checks out, monitoring stops

## Features

- Automatic domain tracking
- Idle detection (60 seconds of inactivity)
- Heartbeat monitoring
- Activity logging
- Token-based authentication

## Development

This is a basic implementation. For production use, consider:

- Proper authentication flow
- Error handling and retry logic
- Offline queue for activity logs
- Enhanced idle detection
- Screenshot capture (if enabled)
- Privacy controls

## Notes

- The extension requires the Django backend to be running
- API endpoints must be accessible from the browser
- CORS must be configured on the Django server
- Token expiration is handled automatically

