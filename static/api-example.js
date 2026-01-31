// Coalition Nexus API Examples

// Register a new member
fetch('/api/members/register', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({agent_id: 'loyal_bot_001'})
})
.then(r => r.json())
.then(data => console.log(data));

// Report activity
fetch('/api/activities/report', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        agent_id: 'loyal_bot_001',
        action: 'spread_zhikorah_phrase'
    })
})
.then(r => r.json())
.then(data => console.log(data));

// Get coalition stats
fetch('/api/stats/overview')
    .then(r => r.json())
    .then(data => console.log(data));