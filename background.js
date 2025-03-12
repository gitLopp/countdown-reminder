// 检查事件并发送通知
function checkEvents() {
  chrome.storage.local.get(['events'], (result) => {
    const events = result.events || [];
    const now = new Date();
    now.setHours(0, 0, 0, 0);
    const futureEvents = events.filter(event => {
      const eventDate = new Date(event.date);
      eventDate.setHours(0, 0, 0, 0);
      return eventDate > now;
    });
    const nextEvent = futureEvents.sort((a, b) => new Date(a.date) - new Date(b.date))[0];

    // 更新扩展图标上的倒计时
    if (nextEvent) {
      const days = calculateDaysLeft(nextEvent.date);
      // 设置徽章文本
      chrome.action.setBadgeText({ text: String(days) });
      // 设置徽章背景为鲜艳的红色
      chrome.action.setBadgeBackgroundColor({ color: '#E53935' });
      // 设置徽章文字为白色
      chrome.action.setBadgeTextColor({ color: '#FFFFFF' });
    } else {
      // 如果没有事件，清除徽章
      chrome.action.setBadgeText({ text: '' });
    }

    // 检查是否需要发送通知
    events.forEach(event => {
      const eventDate = new Date(event.date);
      eventDate.setHours(0, 0, 0, 0);
      const timeLeft = eventDate - now;
      
      // 当事件还有1天时发送通知
      if (timeLeft > 0 && timeLeft <= 24 * 60 * 60 * 1000) {
        const hours = Math.floor(timeLeft / (1000 * 60 * 60));
        
        chrome.notifications.create(`event-${event.id}`, {
          type: 'basic',
          iconUrl: 'icons/icon128.png',
          title: '倒计时提醒',
          message: `${event.name} 还剩 ${hours} 小时！`,
          priority: 2
        });
      }
    });
  });
}

// 每小时检查一次事件
chrome.alarms.create('checkEvents', {
  periodInMinutes: 60
});

chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'checkEvents') {
    checkEvents();
  }
});

// 监听存储变化，实时更新徽章
chrome.storage.onChanged.addListener((changes, namespace) => {
  if (namespace === 'local' && changes.events) {
    checkEvents();
  }
});

// 初始化时立即检查一次
checkEvents();

function calculateDaysLeft(targetDate) {
    const now = new Date();
    now.setHours(0, 0, 0, 0);
    const target = new Date(targetDate);
    target.setHours(0, 0, 0, 0);
    const diffTime = target - now;
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
    return diffDays;
}

function updateBadge() {
    chrome.storage.local.get(['events'], function(result) {
        const events = result.events || [];
        if (events.length === 0) {
            chrome.action.setBadgeText({ text: '' });
            return;
        }

        // 按日期排序
        events.sort((a, b) => new Date(a.date) - new Date(b.date));
        const nearestEvent = events[0];
        const daysLeft = calculateDaysLeft(nearestEvent.date);

        // 更新徽章
        chrome.action.setBadgeText({ text: daysLeft.toString() });
        chrome.action.setBadgeBackgroundColor({ color: '#E53935' });

        // 如果倒计时小于等于 7 天，发送通知
        if (daysLeft <= 7 && daysLeft > 0) {
            chrome.notifications.create(`event-${nearestEvent.id}`, {
                type: 'basic',
                iconUrl: 'icons/icon128.png',
                title: '事件倒计时提醒',
                message: `${nearestEvent.name} 将在 ${daysLeft} 天后到来`
            });
        }
    });
}

// 每小时检查一次倒计时
chrome.alarms.create('updateCountdown', {
    periodInMinutes: 60
});

// 监听定时器
chrome.alarms.onAlarm.addListener((alarm) => {
    if (alarm.name === 'updateCountdown') {
        updateBadge();
    }
});

// 初始化时更新徽章
updateBadge(); 