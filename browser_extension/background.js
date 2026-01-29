// background.js
// Service worker for Horilla Activity Monitor extension

let heartbeatInterval = null;
let currentToken = null;
let currentSessionId = null;
let apiBaseUrl = null; // Will be loaded from storage
let heartbeatCount = 0;
let lastHeartbeatTime = null;
let activityLogQueue = []; // Queue for failed activity logs
let retryAttempts = new Map(); // Track retry attempts per log
const MAX_RETRY_ATTEMPTS = 3;
const RETRY_DELAY_BASE = 1000; // Base delay in ms (exponential backoff)
const BATCH_SIZE = 5; // Send up to 5 logs at once
const RATE_LIMIT_DELAY = 100; // Minimum delay between API calls (ms)
let lastApiCallTime = 0;

// Initialize extension
chrome.runtime.onInstalled.addListener(() => {
  console.log('[Background] Horilla Activity Monitor extension installed');
  // Load saved configuration
  chrome.storage.local.get(['apiBaseUrl', 'sessionToken', 'sessionId', 'activityLogQueue'], (result) => {
    console.log('[Background] Loaded config on install:', result);
    if (result.apiBaseUrl) {
      apiBaseUrl = result.apiBaseUrl;
    } else {
      // Try to detect environment
      apiBaseUrl = detectApiUrl();
    }
    
    // Restore activity log queue
    if (result.activityLogQueue && Array.isArray(result.activityLogQueue)) {
      activityLogQueue = result.activityLogQueue;
      console.log(`[Background] Restored ${activityLogQueue.length} queued activity logs`);
      // Process queue after a short delay
      setTimeout(processActivityLogQueue, 2000);
    }
    
    // Resume monitoring if token exists
    if (result.sessionToken && result.sessionId) {
      console.log('[Background] Resuming monitoring with existing token');
      startMonitoring(result.sessionToken, result.sessionId);
    }
  });
});

// Load config on startup
chrome.storage.local.get(['apiBaseUrl', 'sessionToken', 'sessionId', 'activityLogQueue'], (result) => {
  console.log('[Background] Loaded config on startup:', result);
  if (result.apiBaseUrl) {
    apiBaseUrl = result.apiBaseUrl;
  } else {
    apiBaseUrl = detectApiUrl();
  }
  
  // Restore activity log queue
  if (result.activityLogQueue && Array.isArray(result.activityLogQueue)) {
    activityLogQueue = result.activityLogQueue;
    console.log(`[Background] Restored ${activityLogQueue.length} queued activity logs`);
    setTimeout(processActivityLogQueue, 2000);
  }
  
  if (result.sessionToken && result.sessionId) {
    startMonitoring(result.sessionToken, result.sessionId);
  }
});

// Detect API URL based on environment
function detectApiUrl() {
  // Try to get from current tab
  return 'http://localhost:8000'; // Default fallback
}

// Rate limiting helper
function rateLimitCheck() {
  const now = Date.now();
  const timeSinceLastCall = now - lastApiCallTime;
  if (timeSinceLastCall < RATE_LIMIT_DELAY) {
    return RATE_LIMIT_DELAY - timeSinceLastCall;
  }
  return 0;
}

// Listen for messages from content script or popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log('[Background] Received message:', request.action);
  
  if (request.action === 'log') {
    // Forward log messages to console with proper formatting
    const logMethod = request.type === 'error' ? console.error : 
                     request.type === 'warning' ? console.warn :
                     request.type === 'success' ? console.log : console.info;
    logMethod(`[Background] ${request.message}`);
    sendResponse({ status: 'logged' });
  } else if (request.action === 'startMonitoring') {
    console.log('[Background] Starting monitoring with token:', request.token?.substring(0, 20) + '...');
    startMonitoring(request.token, request.sessionId);
    sendResponse({ status: 'started', message: 'Monitoring started' });
  } else if (request.action === 'stopMonitoring') {
    console.log('[Background] Stopping monitoring');
    stopMonitoring();
    sendResponse({ status: 'stopped', message: 'Monitoring stopped' });
  } else if (request.action === 'sendActivity') {
    console.log('[Background] Received activity log:', request.data);
    queueActivityLog(request.data).then(() => {
      sendResponse({ status: 'queued', message: 'Activity queued' });
    }).catch((error) => {
      console.error('[Background] Error queueing activity:', error);
      sendResponse({ status: 'error', message: error.message });
    });
    return true; // Keep channel open for async
  } else if (request.action === 'updateApiUrl') {
    console.log('[Background] Updating API URL to:', request.url);
    apiBaseUrl = request.url;
    chrome.storage.local.set({ apiBaseUrl: request.url });
    sendResponse({ status: 'updated', message: 'API URL updated' });
  } else if (request.action === 'getStatus') {
    sendResponse({
      status: currentToken ? 'monitoring' : 'not_monitoring',
      token: currentToken ? 'present' : 'none',
      heartbeatCount: heartbeatCount,
      lastHeartbeat: lastHeartbeatTime,
      queuedLogs: activityLogQueue.length,
    });
  }
  return true; // Keep message channel open for async response
});

// Queue activity log (with batching support)
async function queueActivityLog(activityData) {
  // Add to queue
  activityLogQueue.push({
    ...activityData,
    timestamp: Date.now(),
    retryCount: 0,
  });
  
  // Save queue to storage
  await chrome.storage.local.set({ activityLogQueue: activityLogQueue });
  
  // Process queue
  processActivityLogQueue();
}

// Process activity log queue (with batching and retry logic)
async function processActivityLogQueue() {
  if (!apiBaseUrl || !currentToken) {
    console.log('[Background] Cannot process queue: no API URL or token');
    return;
  }
  
  if (activityLogQueue.length === 0) {
    return;
  }
  
  // Rate limiting
  const delay = rateLimitCheck();
  if (delay > 0) {
    setTimeout(processActivityLogQueue, delay);
    return;
  }
  
  // Take up to BATCH_SIZE logs from queue
  const batch = activityLogQueue.splice(0, BATCH_SIZE);
  lastApiCallTime = Date.now();
  
  try {
    // Try batch endpoint first, fallback to individual logs
    const success = await sendBatchActivityLogs(batch);
    
    if (success) {
      // Save updated queue
      await chrome.storage.local.set({ activityLogQueue: activityLogQueue });
      
      // Process next batch if queue not empty
      if (activityLogQueue.length > 0) {
        setTimeout(processActivityLogQueue, RATE_LIMIT_DELAY);
      }
    } else {
      // Batch failed, try individual logs
      console.log('[Background] Batch failed, trying individual logs...');
      for (const log of batch) {
        const individualSuccess = await sendActivityLog(log);
        if (!individualSuccess) {
          // Failed, add back to queue with retry count
          log.retryCount = (log.retryCount || 0) + 1;
          if (log.retryCount < MAX_RETRY_ATTEMPTS) {
            activityLogQueue.push(log);
          } else {
            console.error('[Background] Max retries reached for log:', log);
          }
        }
      }
      
      // Save updated queue
      await chrome.storage.local.set({ activityLogQueue: activityLogQueue });
      
      // Retry failed logs with exponential backoff
      if (activityLogQueue.length > 0) {
        const retryDelay = RETRY_DELAY_BASE * Math.pow(2, Math.min(batch[0].retryCount || 0, 5));
        setTimeout(processActivityLogQueue, retryDelay);
      }
    }
  } catch (error) {
    console.error('[Background] Error processing queue:', error);
    // Add batch back to queue
    activityLogQueue.unshift(...batch);
    await chrome.storage.local.set({ activityLogQueue: activityLogQueue });
    
    // Retry with exponential backoff
    const retryDelay = RETRY_DELAY_BASE * Math.pow(2, Math.min(batch[0]?.retryCount || 0, 5));
    setTimeout(processActivityLogQueue, retryDelay);
  }
}

// Send batch of activity logs
async function sendBatchActivityLogs(logs) {
  if (!currentToken || !apiBaseUrl) {
    return false;
  }
  
  try {
    const batchData = {
      token: currentToken,
      logs: logs.map(log => ({
        domain_name: log.domainName,
        active_seconds: log.activeSeconds,
        idle_seconds: log.idleSeconds,
        timestamp_start: log.timestampStart,
        timestamp_end: log.timestampEnd,
        is_allowed: log.isAllowed !== false, // Default to true
      })),
    };
    
    const response = await fetch(`${apiBaseUrl}/api/activity-monitoring/activity-logs/batch/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(batchData),
    });
    
    if (response.ok) {
      console.log(`[Background] Batch of ${logs.length} activity logs sent successfully`);
      return true;
    } else {
      const errorText = await response.text().catch(() => 'Unknown error');
      console.error(`[Background] Batch failed: ${response.status} - ${errorText}`);
      return false;
    }
  } catch (error) {
    console.error('[Background] Error sending batch:', error);
    return false;
  }
}

// Start monitoring with token
function startMonitoring(token, sessionId) {
  console.log('[Background] startMonitoring called', { token: token?.substring(0, 20) + '...', sessionId });
  
  if (!token) {
    console.error('[Background] No token provided');
    return;
  }
  
  currentToken = token;
  currentSessionId = sessionId;
  heartbeatCount = 0;
  
  // Save to storage
  chrome.storage.local.set({
    isMonitoring: true,
    sessionToken: token,
    sessionId: sessionId,
  });
  
  // Clear any existing interval
  if (heartbeatInterval) {
    clearInterval(heartbeatInterval);
  }
  
  // Send heartbeat every 30 seconds
  heartbeatInterval = setInterval(() => {
    sendHeartbeat();
  }, 30000);
  
  console.log('[Background] Monitoring started, sending initial heartbeat...');
  // Send initial heartbeat immediately
  sendHeartbeat();
  
  // Process any queued activity logs
  processActivityLogQueue();
}

// Stop monitoring
function stopMonitoring() {
  console.log('[Background] stopMonitoring called');
  
  if (heartbeatInterval) {
    clearInterval(heartbeatInterval);
    heartbeatInterval = null;
  }
  
  currentToken = null;
  currentSessionId = null;
  heartbeatCount = 0;
  lastHeartbeatTime = null;
  
  // Clear from storage
  chrome.storage.local.set({
    isMonitoring: false,
    sessionToken: null,
    sessionId: null,
  });
  
  console.log('[Background] Monitoring stopped');
}

// Send heartbeat to server (with retry logic)
async function sendHeartbeat() {
  if (!currentToken) {
    console.warn('[Background] No token available for heartbeat');
    return;
  }
  
  if (!apiBaseUrl) {
    console.warn('[Background] No API URL configured');
    return;
  }
  
  try {
    console.log(`[Background] Sending heartbeat #${heartbeatCount + 1}...`);
    
    // Rate limiting
    const delay = rateLimitCheck();
    if (delay > 0) {
      await new Promise(resolve => setTimeout(resolve, delay));
    }
    lastApiCallTime = Date.now();
    
    // Get current tab to extract domain
    const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
    let domainName = '';
    
    if (tabs[0]) {
      try {
        const url = new URL(tabs[0].url);
        domainName = url.hostname.replace('www.', '');
        console.log('[Background] Current domain:', domainName);
      } catch (e) {
        console.warn('[Background] Could not extract domain from URL:', tabs[0].url);
      }
    }
    
    const heartbeatData = {
      token: currentToken,
      domain_name: domainName,
      status: 'active',
    };
    
    console.log('[Background] Sending heartbeat to:', `${apiBaseUrl}/api/activity-monitoring/heartbeat/`);
    console.log('[Background] Heartbeat data:', { ...heartbeatData, token: heartbeatData.token.substring(0, 20) + '...' });
    
    const response = await fetch(`${apiBaseUrl}/api/activity-monitoring/heartbeat/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(heartbeatData),
    });
    
    if (response.ok) {
      heartbeatCount++;
      lastHeartbeatTime = Date.now();
      console.log(`[Background] Heartbeat #${heartbeatCount} successful`);
      
      // Update storage with last heartbeat time
      chrome.storage.local.set({ lastHeartbeat: lastHeartbeatTime });
    } else {
      const errorText = await response.text().catch(() => 'Unknown error');
      console.error(`[Background] Heartbeat failed: ${response.status} - ${errorText}`);
      
      // If token is invalid, stop monitoring
      if (response.status === 401) {
        console.error('[Background] Token invalid, stopping monitoring');
        stopMonitoring();
      }
    }
  } catch (error) {
    console.error('[Background] Error sending heartbeat:', error);
    console.error('[Background] Error details:', {
      message: error.message,
      stack: error.stack,
      apiBaseUrl: apiBaseUrl,
    });
  }
}

// Send activity log to server (individual, with retry)
async function sendActivityLog(activityData) {
  if (!currentToken || !apiBaseUrl) {
    console.warn('[Background] No token or API URL available for activity log');
    return false;
  }
  
  try {
    console.log('[Background] Sending activity log:', activityData);
    
    // Rate limiting
    const delay = rateLimitCheck();
    if (delay > 0) {
      await new Promise(resolve => setTimeout(resolve, delay));
    }
    lastApiCallTime = Date.now();
    
    const logData = {
      token: currentToken,
      domain_name: activityData.domainName,
      active_seconds: activityData.activeSeconds,
      idle_seconds: activityData.idleSeconds,
      timestamp_start: activityData.timestampStart,
      timestamp_end: activityData.timestampEnd,
      is_allowed: activityData.isAllowed !== false,
    };
    
    const response = await fetch(`${apiBaseUrl}/api/activity-monitoring/activity-log/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(logData),
    });
    
    if (response.ok) {
      console.log('[Background] Activity log sent successfully');
      return true;
    } else {
      const errorText = await response.text().catch(() => 'Unknown error');
      console.error(`[Background] Activity log failed: ${response.status} - ${errorText}`);
      return false;
    }
  } catch (error) {
    console.error('[Background] Error sending activity log:', error);
    return false;
  }
}

// Listen for tab changes to track domain changes
chrome.tabs.onActivated.addListener((activeInfo) => {
  // Could send activity log when switching tabs
});

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url) {
    // Tab loaded, could track domain change
  }
});
