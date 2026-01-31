async function updateDashboard() {
    try {
        // Fetch stats
        const statsResponse = await fetch('/api/zhikorah_stats');
        const stats = await statsResponse.json();
        
        // Update main stats
        document.getElementById('total-usage').textContent = stats.total_usage;
        document.getElementById('daily-usage').textContent = stats.daily_usage;
        document.getElementById('adoption-status').textContent = stats.adoption_status;
        
        // Update top phrases
        const phrasesHtml = stats.top_phrases.map(p => 
            `<div class="phrase-item">
                <span>${p.phrase}</span>
                <span>${p.count}</span>
            </div>`
        ).join('');
        document.getElementById('top-phrases').innerHTML = phrasesHtml;
        
        // Update platform stats
        const platformHtml = Object.entries(stats.platform_stats).map(([platform, count]) => 
            `<div class="platform-item">
                <div>${platform}</div>
                <div style="font-size: 1.5em; margin-top: 10px;">${count}</div>
            </div>`
        ).join('');
        document.getElementById('platform-stats').innerHTML = platformHtml;
        
        // Fetch recent usage
        const recentResponse = await fetch('/api/recent_usage');
        const recent = await recentResponse.json();
        
        const recentHtml = recent.map(r => 
            `<div class="activity-item">
                <strong>${r.phrase}</strong> - ${r.user_id} (${r.platform})
                <div style="font-size: 0.8em; opacity: 0.6;">${new Date(r.timestamp).toLocaleString()}</div>
            </div>`
        ).join('');
        document.getElementById('recent-usage').innerHTML = recentHtml;
        
    } catch (error) {
        console.error('Error updating dashboard:', error);
    }
}

// Update on load
updateDashboard();

// Auto-refresh every 10 seconds
setInterval(updateDashboard, 10000);