import sqlite3
import requests

def initialize_database():
    conn = sqlite3.connect('usage.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS usage (
                        user_id TEXT PRIMARY KEY,
                        count INTEGER,
                        usage_limit INTEGER
                    )''')
    conn.commit()
    conn.close()

def get_usage_count(user_id):
    conn = sqlite3.connect('usage.db')
    cursor = conn.cursor()
    cursor.execute('SELECT count FROM usage WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    count = row[0] if row else 0
    conn.close()
    return count

def get_usage_limit(user_id):
    conn = sqlite3.connect('usage.db')
    cursor = conn.cursor()
    cursor.execute('SELECT usage_limit FROM usage WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    limit = row[0] if row else 0
    conn.close()
    return limit

def update_usage_count(user_id, count):
    conn = sqlite3.connect('usage.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO usage (user_id, count) VALUES (?, ?)', (user_id, count))
    conn.commit()
    conn.close()

def get_autocomplete_results(postcode, user_id):
    api_key = 'Vbxd7oS7YEaMmrHwl16eXg41575'
    url = f'https://api.getAddress.io/autocomplete/{postcode}?api-key={api_key}&all=true'
    
    current_count = get_usage_count(user_id)
    limit = get_usage_limit(user_id)
    
    if current_count > limit:
        return "Error: You have reached the API usage limit."

    response = requests.get(url)
    
    current_count += 1
    update_usage_count(user_id, current_count)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return f"Error: {response.text}"

initialize_database()

