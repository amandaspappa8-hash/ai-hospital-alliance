// Background service worker for real-time alerts
let alertInterval

function checkAlerts() {
  fetch("http://127.0.0.1:8000/alerts")
    .then(r => r.json())
    .then(alerts => {
      if (Array.isArray(alerts) && alerts.length > 0) {
        chrome.notifications.create({
          type: "basic",
          iconUrl: "icons/icon48.png",
          title: "🚨 AI Hospital — Alert",
          message: `${alerts.length} active alert(s) require attention`,
          priority: 2,
        })
      }
    })
    .catch(() => {})
}

chrome.runtime.onInstalled.addListener(() => {
  chrome.alarms.create("checkAlerts", { periodInMinutes: 5 })
})

chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === "checkAlerts") checkAlerts()
})
