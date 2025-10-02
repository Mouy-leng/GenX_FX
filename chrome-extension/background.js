// This is the service worker for the GenX FX Chrome Extension.
// It will handle background tasks such as fetching data from the API
// and managing notifications.

chrome.runtime.onInstalled.addListener(() => {
  console.log('GenX FX Extension installed.');
});