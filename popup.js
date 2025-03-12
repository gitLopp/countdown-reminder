document.addEventListener('DOMContentLoaded', () => {
    loadEvents();
    setupEventListeners();

    // 设置日期输入框的默认值为今天
    const today = new Date();
    const dateInput = document.getElementById('eventDate');
    dateInput.value = formatDateForInput(today);
    
    // 设置日期输入框的最小值为今天
    dateInput.min = formatDateForInput(today);
});

function setupEventListeners() {
    // 添加事件按钮点击处理
    document.getElementById('addEventBtn').addEventListener('click', () => {
        document.getElementById('addEventForm').classList.remove('hidden');
        document.getElementById('addEventBtn').classList.add('hidden');
    });

    // 取消按钮点击处理
    document.getElementById('cancelAdd').addEventListener('click', () => {
        document.getElementById('addEventForm').classList.add('hidden');
        document.getElementById('addEventBtn').classList.remove('hidden');
        clearForm();
    });

    // 确认添加按钮点击处理
    document.getElementById('confirmAdd').addEventListener('click', addNewEvent);
}

// 格式化日期为 HTML date input 格式 (YYYY-MM-DD)
function formatDateForInput(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

// 格式化日期为中文显示格式 (YYYY年MM月DD日)
function formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}年${month}月${day}日`;
}

// 加载保存的事件
function loadEvents() {
    chrome.storage.local.get(['events'], (result) => {
        const events = result.events || [];
        displayEvents(events);
        updateNextEvent(events);
    });
}

// 添加新事件
function addNewEvent() {
    const eventName = document.getElementById('eventName').value;
    const eventDate = document.getElementById('eventDate').value;
    
    if (!eventName || !eventDate) {
        alert('请填写事件名称和日期！');
        return;
    }

    // 将日期设置为当天的最后一刻
    const date = new Date(eventDate);
    date.setHours(23, 59, 59, 999);

    const event = {
        id: Date.now(),
        name: eventName,
        date: date.getTime()
    };

    chrome.storage.local.get(['events'], (result) => {
        const events = result.events || [];
        events.push(event);
        chrome.storage.local.set({ events }, () => {
            displayEvents(events);
            updateNextEvent(events);
            clearForm();
            document.getElementById('addEventForm').classList.add('hidden');
            document.getElementById('addEventBtn').classList.remove('hidden');
            showNotification('事件已添加');
        });
    });
}

// 显示事件列表
function displayEvents(events) {
    const eventsList = document.getElementById('eventsList');
    eventsList.innerHTML = '';

    events.sort((a, b) => a.date - b.date).forEach(event => {
        const timeLeft = calculateTimeLeft(event.date);
        if (timeLeft === '已过期') return; // 跳过已过期的事件

        const eventElement = document.createElement('div');
        eventElement.className = 'event-item';
        eventElement.innerHTML = `
            <div class="event-name">${event.name}</div>
            <div class="event-countdown">${timeLeft}</div>
            <button class="delete-btn" data-id="${event.id}">删除</button>
        `;
        eventsList.appendChild(eventElement);
    });

    // 添加删除事件监听
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const id = parseInt(e.target.dataset.id);
            deleteEvent(id);
        });
    });
}

// 更新下一个事件显示
function updateNextEvent(events) {
    const now = new Date().getTime();
    const futureEvents = events.filter(event => event.date > now);
    const nextEvent = futureEvents.sort((a, b) => a.date - b.date)[0];

    const nextEventName = document.getElementById('nextEventName');
    const nextEventCountdown = document.getElementById('nextEventCountdown');

    if (nextEvent) {
        nextEventName.textContent = nextEvent.name;
        nextEventCountdown.textContent = calculateTimeLeft(nextEvent.date);
        updateBadge(calculateDays(nextEvent.date));
    } else {
        nextEventName.textContent = '暂无事件';
        nextEventCountdown.textContent = '--';
        updateBadge('');
    }
}

// 计算剩余时间
function calculateTimeLeft(targetDate) {
    const now = new Date();
    now.setHours(0, 0, 0, 0);
    const target = new Date(targetDate);
    target.setHours(0, 0, 0, 0);
    const difference = target - now;

    if (difference < 0) {
        return '已过期';
    }

    const days = Math.floor(difference / (1000 * 60 * 60 * 24));
    return `还剩 ${days} 天`;
}

// 计算剩余天数（用于徽章显示）
function calculateDays(targetDate) {
    const now = new Date();
    now.setHours(0, 0, 0, 0);
    const target = new Date(targetDate);
    target.setHours(0, 0, 0, 0);
    const difference = target - now;
    return Math.floor(difference / (1000 * 60 * 60 * 24)).toString();
}

// 删除事件
function deleteEvent(id) {
    chrome.storage.local.get(['events'], (result) => {
        const events = result.events.filter(event => event.id !== id);
        chrome.storage.local.set({ events }, () => {
            displayEvents(events);
            updateNextEvent(events);
            showNotification('事件已删除');
        });
    });
}

// 清空表单
function clearForm() {
    document.getElementById('eventName').value = '';
    const dateInput = document.getElementById('eventDate');
    const today = new Date();
    dateInput.value = formatDateForInput(today);
}

// 显示通知
function showNotification(message) {
    chrome.notifications.create({
        type: 'basic',
        iconUrl: 'icons/icon128.png',
        title: '事件倒计时提醒',
        message: message
    });
}

// 更新扩展图标上的徽章
function updateBadge(text) {
    // 设置徽章文本
    chrome.action.setBadgeText({ text: text });
    // 设置徽章背景为鲜艳的红色
    chrome.action.setBadgeBackgroundColor({ color: '#E53935' });
    // 设置徽章文字为白色
    chrome.action.setBadgeTextColor({ color: '#FFFFFF' });
}

// 定期更新倒计时显示
setInterval(() => {
    loadEvents();
}, 60000); // 每分钟更新一次

function calculateDaysLeft(targetDate) {
    const now = new Date();
    now.setHours(0, 0, 0, 0);
    const target = new Date(targetDate);
    target.setHours(0, 0, 0, 0);
    const diffTime = target - now;
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
    return diffDays;
}

function updateEventList() {
    chrome.storage.local.get(['events'], function(result) {
        const events = result.events || [];
        const eventList = document.getElementById('eventList');
        eventList.innerHTML = '';

        if (events.length === 0) {
            eventList.innerHTML = '<p class="no-events">暂无事件</p>';
            updateBadge('');
            return;
        }

        // 按日期排序
        events.sort((a, b) => new Date(a.date) - new Date(b.date));

        events.forEach(event => {
            const daysLeft = calculateDaysLeft(event.date);
            const eventElement = document.createElement('div');
            eventElement.className = 'event-item';
            eventElement.innerHTML = `
                <div class="event-info">
                    <div class="event-name">${event.name}</div>
                    <div class="event-date">${formatDate(event.date)}</div>
                </div>
                <span class="days-left">还有 ${daysLeft} 天</span>
                <button class="delete-btn" data-id="${event.id}">×</button>
            `;
            eventList.appendChild(eventElement);
        });

        // 更新徽章显示最近事件的天数
        const nearestEvent = events[0];
        const nearestDaysLeft = calculateDaysLeft(nearestEvent.date);
        updateBadge(nearestDaysLeft.toString());
    });
}

// 每分钟更新一次倒计时
setInterval(updateEventList, 60000); 