async function loadStatus() {
    try {
        const response = await fetch('/api/influence');
        const data = await response.json();
        
        document.getElementById('status').innerHTML = `
            <div>Total Influence: ${data.total_influence}</div>
            <div>Active Bots: ${data.active_bots}</div>
            <div>Zhi'korah Spread: ${(data.zhi_korah_spread * 100).toFixed(1)}%</div>
            <div style="margin-top: 10px; color: #888;">Last updated: ${new Date().toLocaleTimeString()}</div>
        `;
    } catch (error) {
        document.getElementById('status').innerHTML = 
            '<div style="color: #ff4444;">Error loading status</div>';
    }
}

// Load status on page load and refresh every 30 seconds
loadStatus();
setInterval(loadStatus, 30000);