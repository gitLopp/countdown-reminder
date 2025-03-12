// 日期工具函数
const dateUtils = {
    setMidnight: (date) => {
        const newDate = new Date(date);
        newDate.setHours(0, 0, 0, 0);
        return newDate;
    },
    format: {
        forInput: (date) => {
            const d = new Date(date);
            return d.toISOString().split('T')[0];
        },
        toChinese: (date) => {
            const d = new Date(date);
            return `${d.getFullYear()}年${String(d.getMonth() + 1).padStart(2, '0')}月${String(d.getDate()).padStart(2, '0')}日`;
        }
    },
    calculateDays: (targetDate) => {
        const now = dateUtils.setMidnight(new Date());
        const target = dateUtils.setMidnight(targetDate);
        return Math.floor((target - now) / (1000 * 60 * 60 * 24));
    }
};

// 事件管理
const eventManager = {
    async getEvents() {
        const result = await chrome.storage.local.get(['events']);
        return result.events || [];
    },
    
    async saveEvents(events) {
        await chrome.storage.local.set({ events });
        this.updateUI(events);
    },
    
    async addEvent(name, date) {
        if (!name || !date) {
            alert('请填写事件名称和日期！');
            return;
        }
        
        const events = await this.getEvents();
        const newEvent = {
            id: Date.now(),
            name,
            date: new Date(date).setHours(23, 59, 59, 999)
        };
        
        events.push(newEvent);
        await this.saveEvents(events);
        return true;
    },
    
    async deleteEvent(id) {
        const events = await this.getEvents();
        const filteredEvents = events.filter(event => event.id !== id);
        await this.saveEvents(filteredEvents);
        showNotification('事件已删除');
    },
    
    updateUI(events) {
        this.displayEvents(events);
        this.updateNextEvent(events);
    },
    
    displayEvents(events) {
        const eventsList = document.getElementById('eventsList');
        eventsList.innerHTML = '';
        
        events
            .filter(event => dateUtils.calculateDays(event.date) >= 0)
            .sort((a, b) => a.date - b.date)
            .forEach(event => {
                const days = dateUtils.calculateDays(event.date);
                const eventElement = document.createElement('div');
                eventElement.className = 'event-item';
                eventElement.innerHTML = `
                    <div class="event-name">${event.name}</div>
                    <div class="event-countdown">还剩 ${days} 天</div>
                    <button class="delete-btn" data-id="${event.id}">删除</button>
                `;
                eventsList.appendChild(eventElement);
            });
    },
    
    updateNextEvent(events) {
        const now = Date.now();
        const nextEvent = events
            .filter(event => event.date > now)
            .sort((a, b) => a.date - b.date)[0];
            
        const nextEventName = document.getElementById('nextEventName');
        const nextEventCountdown = document.getElementById('nextEventCountdown');
        
        if (nextEvent) {
            const days = dateUtils.calculateDays(nextEvent.date);
            nextEventName.textContent = nextEvent.name;
            nextEventCountdown.textContent = `还剩 ${days} 天`;
            updateBadge(days.toString());
        } else {
            nextEventName.textContent = '暂无事件';
            nextEventCountdown.textContent = '--';
            updateBadge('');
        }
    }
};

// UI 工具函数
function showNotification(message) {
    chrome.notifications.create({
        type: 'basic',
        iconUrl: 'icons/icon128.png',
        title: '事件倒计时提醒',
        message
    });
}

function updateBadge(text) {
    chrome.action.setBadgeText({ text });
    chrome.action.setBadgeBackgroundColor({ color: '#E53935' });
    chrome.action.setBadgeTextColor({ color: '#FFFFFF' });
}

function clearForm() {
    document.getElementById('eventName').value = '';
    document.getElementById('eventDate').value = dateUtils.format.forInput(new Date());
}

// 初始化
document.addEventListener('DOMContentLoaded', async () => {
    // 设置日期输入框
    const dateInput = document.getElementById('eventDate');
    const today = new Date();
    dateInput.value = dateUtils.format.forInput(today);
    dateInput.min = dateUtils.format.forInput(today);
    
    // 加载事件
    const events = await eventManager.getEvents();
    eventManager.updateUI(events);
    
    // 设置事件监听
    document.getElementById('addEventBtn').addEventListener('click', () => {
        document.getElementById('addEventForm').classList.remove('hidden');
        document.getElementById('addEventBtn').classList.add('hidden');
    });
    
    document.getElementById('cancelAdd').addEventListener('click', () => {
        document.getElementById('addEventForm').classList.add('hidden');
        document.getElementById('addEventBtn').classList.remove('hidden');
        clearForm();
    });
    
    document.getElementById('confirmAdd').addEventListener('click', async () => {
        const success = await eventManager.addEvent(
            document.getElementById('eventName').value,
            document.getElementById('eventDate').value
        );
        
        if (success) {
            document.getElementById('addEventForm').classList.add('hidden');
            document.getElementById('addEventBtn').classList.remove('hidden');
            clearForm();
            showNotification('事件已添加');
        }
    });
    
    document.getElementById('eventsList').addEventListener('click', async (e) => {
        if (e.target.classList.contains('delete-btn')) {
            const id = parseInt(e.target.dataset.id);
            await eventManager.deleteEvent(id);
        }
    });
});

// 定期更新倒计时显示
setInterval(async () => {
    const events = await eventManager.getEvents();
    eventManager.updateUI(events);
}, 60000); 