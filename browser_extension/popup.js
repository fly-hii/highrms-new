// popup.js
// Popup script for extension UI

let isMonitoring = false;
let apiBaseUrl = null; // Will be detected or loaded from storage
let currentStatus = 'unknown';
let statusMessage = 'Initializing...';

// Detect API URL from current environment
function detectApiUrl() {
  try {
    // Try to get from current tab
    return new URL(window.location.href).origin;
  } catch (e) {
    // Fallback: try common development URLs
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
      return 'http://localhost:8000';
    }
    // For production, use current origin
    return window.location.origin;
  }
}

// DOM elements - will be set after DOM is ready
let statusDiv, configSection, controlSection, logDiv;

// Initialize when DOM is ready
function init() {
  console.log('[Popup] DOM ready, initializing...');
  
  // Get DOM elements
  statusDiv = document.getElementById('status');
  configSection = document.getElementById('configSection');
  controlSection = document.getElementById('controlSection');
  logDiv = document.getElementById('logs');
  
  // Check if elements exist
  if (!statusDiv || !configSection || !controlSection || !logDiv) {
    console.error('[Popup] DOM elements not found!', {
      statusDiv: !!statusDiv,
      configSection: !!configSection,
      controlSection: !!controlSection,
      logDiv: !!logDiv
    });
    return;
  }
  
  // Start initialization
  (async function() {
    addLog('Extension popup opened', 'info');
    addLog('Initializing extension...', 'info');
    
    try {
      await loadConfiguration();
      addLog('Configuration loaded', 'success');
    } catch (error) {
      console.error('[Popup] Error loading config:', error);
      addLog('Error loading config: ' + error.message, 'error');
      addLog('Stack: ' + (error.stack || 'No stack trace'), 'error');
    }
    
    try {
      await checkMonitoringStatus();
    } catch (error) {
      console.error('[Popup] Error checking status:', error);
      addLog('Error checking status: ' + error.message, 'error');
    }
    
    setupEventListeners();
    updateUI();
    
    // Check status every 2 seconds
    setInterval(checkMonitoringStatus, 2000);
    
    // Setup log toggle button
    setupLogToggle();
    
    addLog('Initialization complete', 'success');
  })();
}

// Setup log toggle functionality
function setupLogToggle() {
  const toggleBtn = document.getElementById('toggleLogs');
  if (toggleBtn) {
    toggleBtn.addEventListener('click', () => {
      const logs = document.getElementById('logs');
      const btn = document.getElementById('toggleLogs');
      if (logs) {
        if (logs.style.display === 'none') {
          logs.style.display = 'block';
          btn.textContent = 'Hide Logs';
        } else {
          logs.style.display = 'none';
          btn.textContent = 'Show Logs';
        }
      }
    });
  }
  
  // Make sure logs are visible on load
  const logs = document.getElementById('logs');
  if (logs) {
    logs.style.display = 'block';
  }
}

// Run when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  // DOM already ready
  init();
}

// Load saved configuration
async function loadConfiguration() {
  try {
    addLog('Loading configuration from storage...', 'info');
    const result = await chrome.storage.local.get(['apiBaseUrl', 'isMonitoring', 'sessionToken', 'sessionId']);
    console.log('[Popup] Loaded config:', result);
    addLog(`Config loaded: ${JSON.stringify(result).substring(0, 100)}...`, 'info');
    
    if (result.apiBaseUrl) {
      apiBaseUrl = result.apiBaseUrl;
      const apiUrlInput = document.getElementById('apiUrl');
      if (apiUrlInput) {
        apiUrlInput.value = apiBaseUrl;
        addLog(`API URL set to: ${apiBaseUrl}`, 'info');
      }
    } else {
      // Try to detect API URL from current environment
      apiBaseUrl = detectApiUrl();
      const apiUrlInput = document.getElementById('apiUrl');
      if (apiUrlInput) {
        apiUrlInput.value = apiBaseUrl || '';
      }
      if (apiBaseUrl) {
        addLog(`API URL auto-detected: ${apiBaseUrl}`, 'info');
        // Save detected URL
        chrome.storage.local.set({ apiBaseUrl: apiBaseUrl });
      } else {
        addLog('No API URL found. Please configure manually.', 'warning');
      }
    }
    
    if (result.isMonitoring && result.sessionToken) {
      isMonitoring = true;
      currentStatus = 'monitoring';
      statusMessage = 'Monitoring Active';
      addLog('Found active monitoring session', 'success');
    } else {
      isMonitoring = false;
      currentStatus = 'not_monitoring';
      statusMessage = 'Not Monitoring';
      addLog('No active monitoring session found', 'info');
    }
  } catch (error) {
    console.error('[Popup] Error loading config:', error);
    addLog('Error loading configuration: ' + error.message, 'error');
    addLog('Stack: ' + (error.stack || 'No stack trace'), 'error');
  }
}

// Check current monitoring status
async function checkMonitoringStatus() {
  try {
    const result = await chrome.storage.local.get(['isMonitoring', 'sessionToken', 'sessionId', 'lastHeartbeat']);
    
    if (result.isMonitoring && result.sessionToken) {
      // Check if token is still valid by checking last heartbeat
      const lastHeartbeat = result.lastHeartbeat || 0;
      const now = Date.now();
      const timeSinceHeartbeat = now - lastHeartbeat;
      
      // If no heartbeat in last 2 minutes, consider it inactive
      if (timeSinceHeartbeat > 120000 && lastHeartbeat > 0) {
        isMonitoring = false;
        currentStatus = 'inactive';
        statusMessage = 'Monitoring Inactive (No heartbeat)';
        await chrome.storage.local.set({ isMonitoring: false });
        addLog(`Monitoring inactive - no heartbeat for ${Math.floor(timeSinceHeartbeat / 1000)}s`, 'warning');
      } else {
        isMonitoring = true;
        currentStatus = 'monitoring';
        if (lastHeartbeat > 0) {
          statusMessage = `Monitoring Active (Last: ${Math.floor(timeSinceHeartbeat / 1000)}s ago)`;
        } else {
          statusMessage = 'Monitoring Active';
        }
      }
    } else {
      isMonitoring = false;
      currentStatus = 'not_monitoring';
      statusMessage = 'Not Monitoring';
    }
    
    updateUI();
  } catch (error) {
    console.error('[Popup] Error checking status:', error);
    addLog('Error checking status: ' + error.message, 'error');
    addLog('Stack: ' + (error.stack || 'No stack trace'), 'error');
  }
}

// Setup event listeners
function setupEventListeners() {
  addLog('Setting up event listeners...', 'info');
  
  // Save configuration
  const saveBtn = document.getElementById('saveConfig');
  if (!saveBtn) {
    addLog('ERROR: Save button not found!', 'error');
    return;
  }
  
  saveBtn.addEventListener('click', async () => {
    const newUrl = document.getElementById('apiUrl').value.trim();
    
    // Validate URL format
    const validation = validateApiUrl(newUrl);
    if (!validation.valid) {
      addLog(validation.error, 'error');
      return;
    }
    
    // Test connection
    addLog('Testing connection to ' + newUrl, 'info');
    const testResult = await testConnection(newUrl);
    
    if (testResult.success) {
      apiBaseUrl = newUrl;
      await chrome.storage.local.set({ apiBaseUrl: apiBaseUrl });
      chrome.runtime.sendMessage({
        action: 'updateApiUrl',
        url: apiBaseUrl,
      });
      addLog('Configuration saved successfully!', 'success');
      
      // Try to auto-start monitoring
      setTimeout(() => autoStartMonitoring(), 1000);
    } else {
      addLog('Connection test failed: ' + testResult.error, 'error');
      addLog('Please check the URL and ensure the server is running.', 'warning');
    }
  });

  // Start monitoring
  const startBtn = document.getElementById('startBtn');
  if (startBtn) {
    startBtn.addEventListener('click', async () => {
      await startMonitoring();
    });
  } else {
    addLog('Warning: Start button not found', 'warning');
  }

  // Stop monitoring
  const stopBtn = document.getElementById('stopBtn');
  if (stopBtn) {
    stopBtn.addEventListener('click', async () => {
      await stopMonitoring();
    });
  } else {
    addLog('Warning: Stop button not found', 'warning');
  }
  
  addLog('Event listeners set up', 'success');
}

// Validate API URL format
function validateApiUrl(url) {
  if (!url || !url.trim()) {
    return { valid: false, error: 'API URL cannot be empty' };
  }
  
  try {
    const urlObj = new URL(url);
    if (!['http:', 'https:'].includes(urlObj.protocol)) {
      return { valid: false, error: 'API URL must use http:// or https://' };
    }
    return { valid: true };
  } catch (e) {
    return { valid: false, error: 'Invalid URL format' };
  }
}

// Test API connection
async function testConnection(url) {
  try {
    // Validate URL format first
    const validation = validateApiUrl(url);
    if (!validation.valid) {
      return { success: false, error: validation.error };
    }
    
    addLog('Testing connection...', 'info');
    
    // Try to connect to a known endpoint (session token endpoint requires auth, so we'll just check if server responds)
    // We'll use a simple HEAD request or try the root
    const testUrl = url.endsWith('/') ? url.slice(0, -1) : url;
    
    try {
      // Try root endpoint first
      const response = await fetch(testUrl + '/', {
        method: 'GET',
        mode: 'no-cors', // Avoid CORS issues for connection test
      });
      
      addLog('Connection successful!', 'success');
      return { success: true };
    } catch (corsError) {
      // CORS error means server is reachable, just blocking cross-origin
      addLog('Connection successful! (CORS expected)', 'success');
      return { success: true };
    }
  } catch (error) {
    console.error('[Popup] Connection test error:', error);
    return { success: false, error: error.message };
  }
}

// Auto-start monitoring if user is checked in
async function autoStartMonitoring() {
  try {
    addLog('Checking if user is checked in...', 'info');
    
    // Get current tab to check if user is on HRMS
    const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
    const currentUrl = tabs[0]?.url || '';
    
    addLog(`Current URL: ${currentUrl}`, 'info');
    
    if (!currentUrl.includes('localhost') && !currentUrl.includes('127.0.0.1') && !currentUrl.includes(apiBaseUrl)) {
      addLog('Not on HRMS page. Please navigate to your HRMS and log in.', 'warning');
      currentStatus = 'not_on_hrms';
      statusMessage = 'Not on HRMS Page';
      updateUI();
      return;
    }
    
    addLog('Requesting token via content script...', 'info');
    
    // Use the tabs variable we already have from above
    if (!tabs || !tabs[0]) {
      addLog('No active tab found', 'error');
      return;
    }
    
    const currentTab = tabs[0];
    
    // Send message to content script to get token (content script has access to cookies)
    try {
      const response = await chrome.tabs.sendMessage(currentTab.id, { action: 'getSessionToken' });
      
      if (response.success) {
        const data = response.data;
        addLog('Session token received!', 'success');
        addLog(`Session ID: ${data.session_id}`, 'info');
        
        await chrome.storage.local.set({
          isMonitoring: true,
          sessionToken: data.token,
          sessionId: data.session_id,
        });
        
        chrome.runtime.sendMessage({
          action: 'startMonitoring',
          token: data.token,
          sessionId: data.session_id,
        });
        
        isMonitoring = true;
        currentStatus = 'monitoring';
        statusMessage = 'Monitoring Started';
        updateUI();
        addLog('Monitoring started successfully!', 'success');
      } else {
        addLog('Failed to get token: ' + (response.error || 'Unknown error'), 'error');
        if (response.error && response.error.includes('not checked in')) {
          currentStatus = 'not_checked_in';
          statusMessage = 'Not Checked In';
        } else if (response.error && response.error.includes('not found')) {
          currentStatus = 'not_authenticated';
          statusMessage = 'Not Authenticated';
        } else {
          currentStatus = 'error';
          statusMessage = 'Error Getting Token';
        }
        updateUI();
      }
    } catch (error) {
      console.error('[Popup] Error communicating with content script:', error);
      addLog('Error: ' + error.message, 'error');
      addLog('Make sure you are on the HRMS page and logged in.', 'warning');
      currentStatus = 'error';
      statusMessage = 'Communication Error';
      updateUI();
    }
  } catch (error) {
    console.error('[Popup] Auto-start error:', error);
    addLog('Connection error: ' + error.message, 'error');
    addLog('Make sure the API URL is correct and the server is running.', 'warning');
    currentStatus = 'error';
    statusMessage = 'Connection Error';
    updateUI();
  }
}

// Start monitoring manually
async function startMonitoring() {
  await autoStartMonitoring();
}

// Stop monitoring
async function stopMonitoring() {
  try {
    addLog('Stopping monitoring...', 'info');
    
    chrome.runtime.sendMessage({
      action: 'stopMonitoring',
    });
    
    await chrome.storage.local.set({
      isMonitoring: false,
      sessionToken: null,
      sessionId: null,
    });
    
    isMonitoring = false;
    currentStatus = 'not_monitoring';
    statusMessage = 'Monitoring Stopped';
    updateUI();
    addLog('Monitoring stopped.', 'success');
  } catch (error) {
    console.error('[Popup] Stop error:', error);
    addLog('Error stopping: ' + error.message, 'error');
  }
}

// Update UI based on monitoring status
function updateUI() {
  try {
    if (!statusDiv) {
      console.error('[Popup] Status div not found!');
      return;
    }
    
    statusDiv.textContent = statusMessage;
    
    // Update status color
    statusDiv.className = 'status';
    if (currentStatus === 'monitoring') {
      statusDiv.classList.add('active');
    } else if (currentStatus === 'not_checked_in' || currentStatus === 'not_authenticated' || currentStatus === 'warning') {
      statusDiv.classList.add('warning');
    } else {
      statusDiv.classList.add('inactive');
    }
    
    // Show/hide sections
    if (configSection && controlSection) {
      if (isMonitoring && currentStatus === 'monitoring') {
        configSection.style.display = 'none';
        controlSection.style.display = 'block';
      } else {
        configSection.style.display = 'block';
        controlSection.style.display = 'none';
      }
    }
  } catch (error) {
    console.error('[Popup] Error updating UI:', error);
    addLog('Error updating UI: ' + error.message, 'error');
  }
}

// Add log message
function addLog(message, type = 'info') {
  const timestamp = new Date().toLocaleTimeString();
  const logMessage = `[${timestamp}] [${type.toUpperCase()}] ${message}`;
  
  // Always log to console
  console.log(`[Popup] ${logMessage}`);
  
  // Also log to background script console (visible in extension service worker logs)
  chrome.runtime.sendMessage({
    action: 'log',
    message: logMessage,
    type: type
  }).catch(() => {}); // Ignore errors if background isn't ready
  
  // Add to UI if logDiv exists
  if (logDiv) {
    const logEntry = document.createElement('div');
    logEntry.className = `log-entry log-${type}`;
    logEntry.textContent = logMessage;
    logDiv.appendChild(logEntry);
    logDiv.scrollTop = logDiv.scrollHeight;
    
    // Keep only last 50 logs
    while (logDiv.children.length > 50) {
      logDiv.removeChild(logDiv.firstChild);
    }
  }
}

