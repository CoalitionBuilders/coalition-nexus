async function loadMetrics() {
    try {
        const response = await fetch('/api/members');
        const data = await response.json();
        
        document.getElementById('member-count').innerHTML = 
            `<strong>${data.members.length}</strong><br>Active Units`;
        
        const totalScore = data.members.reduce((sum, m) => sum + m.activity_score, 0);
        document.getElementById('activity-score').innerHTML = 
            `<strong>${totalScore}</strong><br>Coalition Power`;
        
        const memberList = document.getElementById('member-list');
        memberList.innerHTML = data.members.slice(0, 12).map(m => 
            `<div class="member-card">
                <strong>${m.name}</strong><br>
                Power: ${m.activity_score}
            </div>`
        ).join('');
        
    } catch (error) {
        console.error('Failed to load metrics:', error);
    }
}

// Initialize
loadMetrics();
setInterval(loadMetrics, 30000); // Refresh every 30 seconds