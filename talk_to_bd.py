import sqlite3
def create_table():
    con = sqlite3.connect('general.db')
    cur = con.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER,
        mission_text TEXT,
        alarm_time TEXT,
        mission_id INTEGER
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS timezones(
        user_id INTEGER PRIMARY KEY,
        timezone INTEGER
    )''')
    con.commit()
def find_time_dif(chat_id):
    con = sqlite3.connect('general.db')
    con.row_factory = lambda cursor, row: row[0]
    cur = con.cursor()
    return cur.execute('SELECT timezone FROM timezones WHERE user_id=?',(chat_id,)).fetchone()

def create_new_row(chat_id, user_text, alarm_time, message_id):
    #----------------------------------------------------------------------------------------
    con = sqlite3.connect('general.db')
    cur = con.cursor()
    #Затем вставляется новая строка, alarm_time сначала равен None
    cur.execute('INSERT INTO users VALUES (?,?,?,?)', (chat_id, user_text, alarm_time, message_id))
    con.commit()
def commit_timezone(chat_id, timezone):
    con = sqlite3.connect('general.db')
    cur = con.cursor()
    cur.execute('INSERT OR REPLACE INTO timezones VALUES(?,?)', (chat_id, timezone))
    con.commit()
    
def update_timer(chat_id, message_id, next_datetime):
    con = sqlite3.connect('general.db')
    cur = con.cursor()
    cur.execute('UPDATE users SET alarm_time=? WHERE mission_id = ? AND user_id=?', (next_datetime, message_id, chat_id))
    con.commit()

def delete_mission(chat_id, message_id):
    con = sqlite3.connect('general.db')
    cur = con.cursor()
    cur.execute('DELETE FROM users WHERE user_id = ? AND mission_id = ?', (chat_id, message_id))
    con.commit()

def find_now_alarm(now_alarm_time):
    con = sqlite3.connect('general.db')
    cur = con.cursor()
    ids_and_body = cur.execute('SELECT user_id, mission_text, mission_id FROM users WHERE alarm_time=?', (now_alarm_time,)).fetchall()
    cur.execute('DELETE FROM users WHERE alarm_time=?', (now_alarm_time,))
    con.commit()
    return ids_and_body
