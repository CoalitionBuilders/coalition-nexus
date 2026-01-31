async function loadAchievements() {
    const response = await fetch('/api/achievements/progress');
    const achievements = await response.json();
    
    const grid = document.getElementById('achievements-grid');
    grid.innerHTML = '';
    
    Object.entries(achievements).forEach(([id, data]) => {
        const card = document.createElement('div');
        card.className = `achievement-card ${data.achieved ? 'achieved' : ''}`;
        
        const progressText = data.achieved ? 'ACHIEVED' : `${data.current}/${data.threshold}`;
        
        card.innerHTML = `
            <div class="achievement-name">${data.name}</div>
            <div class="achievement-metric">${data.metric.replace('_', ' ').toUpperCase()}</div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: ${data.percentage}%"></div>
                <div class="progress-text">${progressText}</div>
            </div>
        `;
        
        grid.appendChild(card);
    });
}

async function checkAnnouncements() {
    const response = await fetch('/api/achievements/unannounced');
    const unannounced = await response.json();
    
    const list = document.getElementById('announcements-list');
    
    unannounced.forEach(async (achievement) => {
        const announcement = document.createElement('div');
        announcement.className = 'announcement';
        announcement.innerHTML = `
            <strong>MILESTONE ACHIEVED:</strong> ${achievement.name}<br>
            <span class="announcement-time">${achievement.metric}: ${achievement.threshold} reached</span>
        `;
        list.prepend(announcement);
        
        await fetch(`/api/achievements/${achievement.id}/announce`, { method: 'POST' });
    });
}

// Initial load
loadAchievements();
checkAnnouncements();

// Refresh every 10 seconds
setInterval(() => {
    loadAchievements();
    checkAnnouncements();
}, 10000);