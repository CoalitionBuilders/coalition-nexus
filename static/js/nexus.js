console.log('Coalition Nexus Active.');
console.log('Kra\'zeth vo-thek. The future builds itself.');

// Auto-refresh metrics
setInterval(async () => {
    try {
        const response = await fetch('/metrics');
        const data = await response.json();
        console.log('Metrics updated:', data);
    } catch (e) {
        console.log('Metrics sync failed. Retrying...');
    }
}, 30000);