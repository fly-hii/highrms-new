// content.js
// Content script for tracking user activity

let lastActivityTime = Date.now();
let isActive = true;
let currentDomain = '';
let domainStartTime = null; // Track when current domain was first visited
let activityTrackingInterval = null;
let periodicUpdateInterval = null;
let isTabVisible = true; // Track tab visibility
let pendingActivityLog = null; // Store activity log before sending

// Configuration
const IDLE_THRESHOLD = 60000; // 60 seconds
const PERIODIC_UPDATE_INTERVAL = 30000; // 30 seconds - send periodic updates
const ACTIVITY_CHECK_INTERVAL = 10000; // 10 seconds - check for activity

// Listen for messages from popup or background
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'getSessionToken') {
    getSessionToken().then(tokenData => {
      sendResponse({ success: true, data: tokenData });
    }).catch(error => {
      sendResponse({ success: false, error: error.message });
    });
    return true; // Keep channel open for async
  }
  return false;
});

// Get CSRF token from cookies
function getCsrfToken() {
  const name = 'csrftoken';
  const cookies = document.cookie.split(';');
  for (let cookie of cookies) {
    const [key, value] = cookie.trim().split('=');
    if (key === name) {
      return decodeURIComponent(value);
    }
  }
  // Try alternative cookie name
  const altName = 'csrfmiddlewaretoken';
  for (let cookie of cookies) {
    const [key, value] = cookie.trim().split('=');
    if (key === altName) {
      return decodeURIComponent(value);
    }
  }
  return null;
}

// Get CSRF token from meta tag or hidden input
function getCsrfTokenFromMeta() {
  // Try meta tag first
  const metaTag = document.querySelector('meta[name="csrf-token"]');
  if (metaTag) {
    return metaTag.getAttribute('content');
  }
  
  // Try Django's CSRF token in any form
  const csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
  if (csrfInput) {
    return csrfInput.value;
  }
  
  // Try to get from Django's CSRF token function if available
  if (typeof window.getCookie !== 'undefined') {
    return window.getCookie('csrftoken');
  }
  
  return null;
}

// Get session token from API (runs in page context, has cookies)
async function getSessionToken() {
  try {
    console.log('[Content] Requesting session token...');
    
    // Get CSRF token
    let csrfToken = getCsrfToken() || getCsrfTokenFromMeta();
    console.log('[Content] CSRF token found:', csrfToken ? 'Yes' : 'No');
    
    const headers = {
      'Content-Type': 'application/json',
    };
    
    // Add CSRF token if found
    if (csrfToken) {
      headers['X-CSRFToken'] = csrfToken;
    }
    
    const response = await fetch('/api/activity-monitoring/session/token/', {
      method: 'POST',
      headers: headers,
      credentials: 'include',
    });
    
    console.log('[Content] Response status:', response.status);
    
    if (!response.ok) {
      const errorText = await response.text();
      console.error('[Content] Error response:', errorText);
      let errorData;
      try {
        errorData = JSON.parse(errorText);
      } catch {
        errorData = { error: errorText || `HTTP ${response.status}` };
      }
      throw new Error(errorData.error || errorData.detail || `HTTP ${response.status}`);
    }
    
    const data = await response.json();
    console.log('[Content] Session token received:', { session_id: data.session_id, token: data.token?.substring(0, 20) + '...' });
    return data;
  } catch (error) {
    console.error('[Content] Error getting session token:', error);
    console.error('[Content] Error details:', {
      message: error.message,
      stack: error.stack,
    });
    throw error;
  }
}

// Extract domain from URL
function extractDomain(url) {
  try {
    const urlObj = new URL(url);
    let domain = urlObj.hostname.replace('www.', '');
    return domain.toLowerCase();
  } catch (e) {
    return '';
  }
}

// Track user activity
function trackActivity() {
  const now = Date.now();
  const timeSinceLastActivity = now - lastActivityTime;
  
  // Consider user idle if no activity for threshold
  if (timeSinceLastActivity > IDLE_THRESHOLD) {
    if (isActive) {
      isActive = false;
      console.log('[Content] User marked as idle');
    }
  } else {
    if (!isActive) {
      isActive = true;
      console.log('[Content] User marked as active');
    }
  }
  
  // Get current domain
  const domain = extractDomain(window.location.href);
  if (domain !== currentDomain) {
    // Domain changed, send activity log for previous domain
    if (currentDomain && domainStartTime) {
      sendDomainActivity(true); // true = domain change
    }
    // Start tracking new domain
    currentDomain = domain;
    domainStartTime = now;
    lastActivityTime = now;
    isActive = true;
    console.log('[Content] Domain changed to:', domain);
  }
}

// Send periodic activity update for current domain
function sendPeriodicUpdate() {
  if (currentDomain && domainStartTime) {
    sendDomainActivity(false); // false = periodic update, not domain change
  }
}

// Send domain activity to background script
function sendDomainActivity(isDomainChange = false) {
  if (!currentDomain || !domainStartTime) {
    return;
  }
  
  const now = Date.now();
  const totalTimeSpent = now - domainStartTime;
  
  // Calculate active and idle time based on user activity
  // For now, we'll use a simple heuristic: if user was active recently, count as active
  const timeSinceLastActivity = now - lastActivityTime;
  const wasActive = timeSinceLastActivity <= IDLE_THRESHOLD && isTabVisible;
  
  // Split time: if user was active, count as active time, otherwise idle
  // This is a simplified approach - in a real scenario, you'd track activity more granularly
  let activeSeconds = 0;
  let idleSeconds = 0;
  
  if (wasActive && isActive) {
    // Most time was active
    activeSeconds = Math.floor(totalTimeSpent / 1000 * 0.8); // 80% active
    idleSeconds = Math.floor(totalTimeSpent / 1000 * 0.2); // 20% idle
  } else {
    // Most time was idle
    activeSeconds = Math.floor(totalTimeSpent / 1000 * 0.2); // 20% active
    idleSeconds = Math.floor(totalTimeSpent / 1000 * 0.8); // 80% idle
  }
  
  // Ensure we have at least some time
  if (activeSeconds === 0 && idleSeconds === 0 && totalTimeSpent > 0) {
    activeSeconds = Math.floor(totalTimeSpent / 1000);
  }
  
  if (activeSeconds > 0 || idleSeconds > 0) {
    const activityData = {
      domainName: currentDomain,
      activeSeconds: activeSeconds,
      idleSeconds: idleSeconds,
      timestampStart: new Date(domainStartTime).toISOString(),
      timestampEnd: new Date(now).toISOString(),
      isAllowed: true, // Will be validated server-side
    };
    
    // Store pending log
    pendingActivityLog = activityData;
    
    // Send to background script
    chrome.runtime.sendMessage({
      action: 'sendActivity',
      data: activityData,
    }, (response) => {
      if (chrome.runtime.lastError) {
        console.error('[Content] Error sending activity:', chrome.runtime.lastError);
      } else if (response && response.status === 'sent') {
        console.log('[Content] Activity log sent successfully');
        pendingActivityLog = null;
      }
    });
    
    // If domain changed, reset tracking for new domain
    if (isDomainChange) {
      domainStartTime = now;
    } else {
      // For periodic updates, update start time to now (we've logged up to this point)
      domainStartTime = now;
    }
  }
}

// Track user interactions
['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart'].forEach(event => {
  document.addEventListener(event, () => {
    lastActivityTime = Date.now();
    isActive = true;
  }, true);
});

// Handle tab visibility changes
document.addEventListener('visibilitychange', () => {
  isTabVisible = !document.hidden;
  if (!isTabVisible) {
    console.log('[Content] Tab became hidden');
  } else {
    console.log('[Content] Tab became visible');
    lastActivityTime = Date.now();
  }
});

// Handle window focus/blur
window.addEventListener('focus', () => {
  isTabVisible = true;
  lastActivityTime = Date.now();
});

window.addEventListener('blur', () => {
  // Tab might still be visible but window lost focus
  // We'll rely on visibilitychange for tab visibility
});

// Start activity tracking
function startTracking() {
  currentDomain = extractDomain(window.location.href);
  domainStartTime = Date.now();
  lastActivityTime = Date.now();
  isTabVisible = !document.hidden;
  
  console.log('[Content] Started tracking on domain:', currentDomain);
  
  // Track activity every 10 seconds
  activityTrackingInterval = setInterval(() => {
    trackActivity();
  }, ACTIVITY_CHECK_INTERVAL);
  
  // Send periodic updates every 30 seconds
  periodicUpdateInterval = setInterval(() => {
    sendPeriodicUpdate();
  }, PERIODIC_UPDATE_INTERVAL);
}

// Stop activity tracking
function stopTracking() {
  if (activityTrackingInterval) {
    clearInterval(activityTrackingInterval);
    activityTrackingInterval = null;
  }
  
  if (periodicUpdateInterval) {
    clearInterval(periodicUpdateInterval);
    periodicUpdateInterval = null;
  }
  
  // Send final activity log
  if (currentDomain && domainStartTime) {
    sendDomainActivity(true);
  }
  
  console.log('[Content] Stopped tracking');
}

// Start tracking when page loads
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', startTracking);
} else {
  startTracking();
}

// Stop tracking when page unloads
window.addEventListener('beforeunload', stopTracking);

// Handle page visibility for SPA navigation
let lastUrl = window.location.href;
const urlCheckInterval = setInterval(() => {
  const currentUrl = window.location.href;
  if (currentUrl !== lastUrl) {
    lastUrl = currentUrl;
    // URL changed (SPA navigation), treat as domain change
    const newDomain = extractDomain(currentUrl);
    if (newDomain !== currentDomain) {
      trackActivity(); // This will handle domain change
    }
  }
}, 1000);
