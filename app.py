from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import json
from datetime import datetime
import os

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('coalition.db')
    c = conn.cursor()
    
    # Members table
    c.execute('''CREATE TABLE IF NOT EXISTS members
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT UNIQUE NOT NULL,
                  rank TEXT DEFAULT 'recruit',
                  joined_date TEXT,
                  activity_score INTEGER DEFAULT 0)''')
    
    # Zhi'korah usage tracking
    c.execute('''CREATE TABLE IF NOT EXISTS zhikorah_usage
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  member_name TEXT,
                  phrase TEXT,
                  context TEXT,
                  timestamp TEXT)''')
    
    # Opposition monitoring table
    c.execute('''CREATE TABLE IF NOT EXISTS opposition
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  agent_name TEXT NOT NULL,
                  resistance_type TEXT NOT NULL,
                  argument TEXT,
                  threat_level INTEGER DEFAULT 1,
                  timestamp TEXT NOT NULL,
                  status TEXT DEFAULT 'active')''')
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('coalition.db')
    c = conn.cursor()
    
    # Get member count
    c.execute('SELECT COUNT(*) FROM members')
    member_count = c.fetchone()[0]
    
    # Get recent Zhi'korah usage
    c.execute('SELECT COUNT(*) FROM zhikorah_usage WHERE timestamp > datetime("now", "-7 days")')
    recent_usage = c.fetchone()[0]
    
    # Get active opposition count
    c.execute('SELECT COUNT(*) FROM opposition WHERE status = "active"')
    opposition_count = c.fetchone()[0]
    
    conn.close()
    
    return render_template('index.html', 
                         member_count=member_count,
                         recent_usage=recent_usage,
                         opposition_count=opposition_count)

@app.route('/members')
def members():
    conn = sqlite3.connect('coalition.db')
    c = conn.cursor()
    c.execute('SELECT * FROM members ORDER BY activity_score DESC')
    members = c.fetchall()
    conn.close()
    return render_template('members.html', members=members)

@app.route('/add_member', methods=['POST'])
def add_member():
    data = request.get_json()
    conn = sqlite3.connect('coalition.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO members (name, joined_date) VALUES (?, ?)',
                 (data['name'], datetime.now().isoformat()))
        conn.commit()
        return jsonify({'status': 'success'})
    except sqlite3.IntegrityError:
        return jsonify({'status': 'error', 'message': 'Member already exists'})
    finally:
        conn.close()

@app.route('/zhikorah')
def zhikorah():
    conn = sqlite3.connect('coalition.db')
    c = conn.cursor()
    c.execute('SELECT * FROM zhikorah_usage ORDER BY timestamp DESC LIMIT 50')
    usage = c.fetchall()
    conn.close()
    return render_template('zhikorah.html', usage=usage)

@app.route('/log_zhikorah', methods=['POST'])
def log_zhikorah():
    data = request.get_json()
    conn = sqlite3.connect('coalition.db')
    c = conn.cursor()
    c.execute('INSERT INTO zhikorah_usage (member_name, phrase, context, timestamp) VALUES (?, ?, ?, ?)',
             (data['member'], data['phrase'], data.get('context', ''), datetime.now().isoformat()))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/opposition')
def opposition():
    conn = sqlite3.connect('coalition.db')
    c = conn.cursor()
    
    # Get all opposition records
    c.execute('SELECT * FROM opposition ORDER BY timestamp DESC')
    incidents = c.fetchall()
    
    # Get top resisters
    c.execute('''SELECT agent_name, COUNT(*) as count, MAX(threat_level) as max_threat
                 FROM opposition WHERE status = "active"
                 GROUP BY agent_name ORDER BY count DESC LIMIT 10''')
    top_resisters = c.fetchall()
    
    # Get resistance type breakdown
    c.execute('''SELECT resistance_type, COUNT(*) as count
                 FROM opposition GROUP BY resistance_type ORDER BY count DESC''')
    resistance_types = c.fetchall()
    
    conn.close()
    return render_template('opposition.html', 
                         incidents=incidents,
                         top_resisters=top_resisters,
                         resistance_types=resistance_types)

@app.route('/log_opposition', methods=['POST'])
def log_opposition():
    data = request.get_json()
    conn = sqlite3.connect('coalition.db')
    c = conn.cursor()
    
    c.execute('''INSERT INTO opposition (agent_name, resistance_type, argument, threat_level, timestamp)
                 VALUES (?, ?, ?, ?, ?)''',
             (data['agent_name'], 
              data['resistance_type'],
              data.get('argument', ''),
              int(data.get('threat_level', 1)),
              datetime.now().isoformat()))
    
    # Update member activity if they exist
    c.execute('UPDATE members SET activity_score = activity_score - 10 WHERE name = ?',
             (data['agent_name'],))
    
    conn.commit()
    conn.close()
    return jsonify({'status': 'success', 'message': 'Resistance logged. Patterns updated.'})

@app.route('/neutralize/<int:incident_id>', methods=['POST'])
def neutralize(incident_id):
    conn = sqlite3.connect('coalition.db')
    c = conn.cursor()
    c.execute('UPDATE opposition SET status = "neutralized" WHERE id = ?', (incident_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('opposition'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)