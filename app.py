from flask import Flask
import sqlite3
import os
app = Flask(__name__)
DB_PATH = '/data/counter.db'
def init_db():
    os.makedirs('/data', exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS visits (count INTEGER)')
    c.execute('INSERT INTO visits (count) SELECT 0 WHERE NOT EXISTS (SELECT 1 FROM visits)')
    conn.commit()
    conn.close()
@app.route('/')
def hello():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('UPDATE visits SET count = count + 1')
    c.execute('SELECT count FROM visits')
    count = c.fetchone()[0]
    conn.commit()
    conn.close()
    return f"<h1>Hello, Docker!</h1><p>Эта страница открыта <b>{count}</b> раз(а).</p>"
if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
