import os
import sys
import random
import threading
import mysql.connector

import http.server
import socketserver

from torpy.http.requests import tor_requests_session


# prevent directory listing :)
try: os.mkdir('tmp44444433')
except: pass
os.chdir('tmp44444433')

found = []
empty = ''
length = 16
newline = '\n'
whitespace = ' '
url = 'https://discordapp.com/api/v9/entitlements/gift-codes/'
header = {'User-Agent': 'Mozilla/5.0'}
charpool = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz'
query = 'INSERT INTO results (code) VALUES (%s)'
found = '[FOUND]'
max_workers = 10

_print = sys.stdout.write
sys.stdout.write = lambda *a: None #void
sys.stderr.write = sys.stdout.write #void

db_conn = mysql.connector.connect(
    user=os.getenv('db_usr'),
    password=os.getenv('db_pw'),
    database=os.getenv('db_dbname'),
    host=os.getenv('db_host'),
    port=int(os.getenv('db_port'))
)

cursor = db_conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS results (code TEXT NOT NULL)')

def print(*args):
    _print(whitespace.join(args) + newline)
    sys.stdout.flush()

def gen_code():
    code = empty.join(random.choices(charpool, k=length))
    while code in found:
        code = empty.join(random.choices(charpool, k=length))
    return code

def check():
    while True:
        with tor_requests_session() as s:
            code = gen_code()
            r = s.get(
                url + code,
                headers=header
            )
            if r.status_code == 200:
                print(found, code)
                cursor.execute(query, (code,))

if __name__ == '__main__':
    for i in range(max_workers):
        t = threading.Thread(target=check)
        t.daemon = True
        t.start()

    with socketserver.TCPServer((empty, 80), http.server.SimpleHTTPRequestHandler) as httpd:
        httpd.serve_forever()
