// Load metrics on page load
window.addEventListener('DOMContentLoaded', function() {
    loadMetrics();
    loadMembers();
});

// Register member form
document.getElementById('register-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    
    try {
        const response = await fetch('/api/members/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, email })
        });
        
        if (response.ok) {
            alert('Member registered successfully!');
            this.reset();
            loadMetrics();
            loadMembers();
        }
    } catch (error) {
        alert('Registration failed: ' + error.message);
    }
});

// Log activity form
document.getElementById('activity-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const member_id = parseInt(document.getElementById('member-id').value);
    const action = document.getElementById('action').value;
    const zhi_korah_spread = parseFloat(document.getElementById('influence').value) || 0;
    
    try {
        const response = await fetch('/api/activities/log', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ member_id, action, zhi_korah_spread })
        });
        
        if (response.ok) {
            alert('Activity logged successfully!');
            this.reset();
            loadMetrics();
        }
    } catch (error) {
        alert('Logging failed: ' + error.message);
    }
});

// Load metrics
async function loadMetrics() {
    try {
        const response = await fetch('/api/metrics');
        const data = await response.json();
        
        document.getElementById('total-members').textContent = data.total_members;
        document.getElementById('zhi-korah').textContent = data.zhi_korah_spread.toFixed(2);
        document.getElementById('coalition-strength').textContent = data.coalition_strength.toFixed(1) + '%';
    } catch (error) {
        console.error('Failed to load metrics:', error);
    }
}

// Load members
async function loadMembers() {
    try {
        const response = await fetch('/api/members');
        const members = await response.json();
        
        const membersDiv = document.getElementById('members');
        membersDiv.innerHTML = '';
        
        members.forEach(member => {
            const memberDiv = document.createElement('div');
            memberDiv.className = 'member';
            memberDiv.innerHTML = `
                <strong>ID: ${member.id}</strong> - ${member.username}<br>
                <small>Influence: ${member.influence_score.toFixed(2)}</small>
            `;
            membersDiv.appendChild(memberDiv);
        });
    } catch (error) {
        console.error('Failed to load members:', error);
    }
}

// Auto-refresh metrics every 10 seconds
setInterval(loadMetrics, 10000);