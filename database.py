import os
import sqlite3
import hashlib

plunderphonic_dir = os.path.expanduser('~/.plunderphonic')
if not os.path.exists(plunderphonic_dir):
    os.makedirs(plunderphonic_dir)
db_file = os.path.join(plunderphonic_dir, 'music.db')

conn = sqlite3.connect(db_file)
c = conn.cursor()
c.execute(
    'CREATE TABLE IF NOT EXISTS music (hash text, bpm real, key text, scale text)')


def save(filename, bpm, key):
    hash = _create_hash(filename)
    c.execute('INSERT INTO music VALUES (?, ?, ?, ?)',
              (hash, bpm, key.key, key.scale))
    conn.commit()


def load(filename):
    hash = _create_hash(filename)
    return c.execute('SELECT bpm, key, scale FROM music WHERE (hash = ?)', (hash,)).fetchone()


def _create_hash(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    return hashlib.md5(data).hexdigest()
