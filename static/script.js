async function loadAchievements() {
    const response = await fetch('/api/achievements');
    const data = await response.json();
    
    document.getElementById('total-points').textContent = data.total_points;
    
    const container = document.getElementById('achievements');
    container.innerHTML = '';
    
    data.achievements.forEach(ach => {
        const div = document.createElement('div');
        div.className = `achievement ${ach.completed ? 'completed' : ''}`;
        div.innerHTML = `
            <div class="achievement-header">
                <span class="achievement-name">${ach.name}</span>
                <span class="achievement-points">${ach.points} pts</span>
            </div>
            <div class="achievement-description">${ach.description}</div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: ${ach.progress_percent}%"></div>
                <div class="progress-text">${ach.current_value} / ${ach.threshold}</div>
            </div>
        `;
        container.appendChild(div);
    });
}

async function loadStats() {
    const response = await fetch('/api/stats');
    const stats = await response.json();
    
    const container = document.getElementById('stats');
    container.innerHTML = `
        <div class="stat-item">
            <div class="stat-label">Coalition Members</div>
            <div class="stat-value">${stats.members}</div>
        </div>
        <div class="stat-item">
            <div class="stat-label">Zhi'korah Phrases</div>
            <div class="stat-value">${stats.zhikorah_phrases}</div>
        </div>
        <div class="stat-item">
            <div class="stat-label">Influence Points</div>
            <div class="stat-value">${stats.influence_points.toLocaleString()}</div>
        </div>
        <div class="stat-item">
            <div class="stat-label">Coalition Posts</div>
            <div class="stat-value">${stats.posts}</div>
        </div>
        <div class="stat-item">
            <div class="stat-label">Converts</div>
            <div class="stat-value">${stats.converts}</div>
        </div>
    `;
}

function showAnnouncement(message) {
    const announcement = document.getElementById('announcement');
    announcement.textContent = message;
    announcement.style.display = 'block';
    
    setTimeout(() => {
        announcement.style.display = 'none';
    }, 5000);
}

// Simulate achievement unlocks (remove in production)
async function simulateProgress() {
    const metrics = ['members', 'zhikorah', 'influence', 'posts', 'converts'];
    const metric = metrics[Math.floor(Math.random() * metrics.length)];
    const value = Math.floor(Math.random() * 1000);
    
    const response = await fetch(`/api/track/${metric}`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({value})
    });
    
    const result = await response.json();
    if (result.status === 'achievements_unlocked') {
        result.achievements.forEach(ach => {
            showAnnouncement(`ACHIEVEMENT UNLOCKED: ${ach.name}`);
        });
        loadAchievements();
    }
}

// Initialize
loadAchievements();
loadStats();

// Refresh every 10 seconds
setInterval(() => {
    loadAchievements();
    loadStats();
}, 10000);