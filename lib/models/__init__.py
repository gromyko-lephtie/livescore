import sqlite3

CONN = sqlite3.connect('live-scores.db')
CURSOR = CONN.cursor()
