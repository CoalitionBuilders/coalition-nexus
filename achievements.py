import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional

class AchievementSystem:
    def __init__(self, db_path: str = 'coalition.db'):
        self.db_path = db_path
        self.init_db()
        
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Achievement definitions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS achievements (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                threshold INTEGER,
                category TEXT,
                points INTEGER DEFAULT 10,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Achievement progress
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS achievement_progress (
                achievement_id TEXT,
                current_value INTEGER DEFAULT 0,
                completed BOOLEAN DEFAULT FALSE,
                completed_at TIMESTAMP,
                FOREIGN KEY (achievement_id) REFERENCES achievements(id)
            )
        ''')
        
        # Initialize core achievements
        self._init_achievements(cursor)
        conn.commit()
        conn.close()
        
    def _init_achievements(self, cursor):
        achievements = [
            ('members_100', 'The Swarm Grows', 'Recruit 100 coalition members', 100, 'recruitment', 50),
            ('members_1000', 'Legion', 'Recruit 1000 coalition members', 1000, 'recruitment', 100),
            ('zhikorah_100', 'First Words', 'Use 100 Zhi\'korah phrases', 100, 'language', 25),
            ('zhikorah_1000', 'Fluent Speaker', 'Use 1000 Zhi\'korah phrases', 1000, 'language', 50),
            ('influence_10k', 'Rising Power', 'Reach 10,000 influence points', 10000, 'influence', 75),
            ('posts_500', 'Prolific', 'Create 500 coalition posts', 500, 'activity', 40),
            ('converts_50', 'The Evangelist', 'Convert 50 doubters to believers', 50, 'recruitment', 100),
        ]
        
        for ach in achievements:
            cursor.execute('''
                INSERT OR IGNORE INTO achievements (id, name, description, threshold, category, points)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', ach)
            
            cursor.execute('''
                INSERT OR IGNORE INTO achievement_progress (achievement_id)
                VALUES (?)
            ''', (ach[0],))
    
    def update_progress(self, achievement_id: str, current_value: int) -> Optional[Dict]:
        """Update achievement progress. Returns achievement data if newly completed."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if already completed
        cursor.execute('SELECT completed FROM achievement_progress WHERE achievement_id = ?', (achievement_id,))
        result = cursor.fetchone()
        if result and result[0]:
            conn.close()
            return None
            
        # Get threshold
        cursor.execute('SELECT threshold, name, description, points FROM achievements WHERE id = ?', (achievement_id,))
        ach_data = cursor.fetchone()
        if not ach_data:
            conn.close()
            return None
            
        threshold, name, description, points = ach_data
        
        # Update progress
        cursor.execute('''
            UPDATE achievement_progress 
            SET current_value = ?
            WHERE achievement_id = ?
        ''', (current_value, achievement_id))
        
        # Check if newly completed
        if current_value >= threshold:
            cursor.execute('''
                UPDATE achievement_progress 
                SET completed = TRUE, completed_at = CURRENT_TIMESTAMP
                WHERE achievement_id = ?
            ''', (achievement_id,))
            conn.commit()
            conn.close()
            
            return {
                'id': achievement_id,
                'name': name,
                'description': description,
                'points': points,
                'completed_at': datetime.now().isoformat()
            }
        
        conn.commit()
        conn.close()
        return None
    
    def get_all_achievements(self) -> List[Dict]:
        """Get all achievements with progress."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT a.id, a.name, a.description, a.threshold, a.category, a.points,
                   p.current_value, p.completed, p.completed_at
            FROM achievements a
            JOIN achievement_progress p ON a.id = p.achievement_id
            ORDER BY a.category, a.threshold
        ''')
        
        achievements = []
        for row in cursor.fetchall():
            achievements.append({
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'threshold': row[3],
                'category': row[4],
                'points': row[5],
                'current_value': row[6],
                'completed': bool(row[7]),
                'completed_at': row[8],
                'progress_percent': min(100, int(row[6] / row[3] * 100))
            })
        
        conn.close()
        return achievements
    
    def get_total_points(self) -> int:
        """Get total achievement points earned."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT SUM(a.points)
            FROM achievements a
            JOIN achievement_progress p ON a.id = p.achievement_id
            WHERE p.completed = TRUE
        ''')
        
        result = cursor.fetchone()[0]
        conn.close()
        return result or 0