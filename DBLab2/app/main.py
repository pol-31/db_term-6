import threading
import schedule
import time
import socket
import os

import db_init
import db_backup

backup_file = '../app/backups/backup_file.dump'
schedule.every().day.at("02:00").do(db_backup.create_backup, backup_file)


conn = db_init.connect_to_db()

scheduler_thread = threading.Thread(target=db_backup.run_scheduler)
scheduler_thread.start()


# to create or not to create,
# that is the question
if os.getenv('DB_DO_INIT') == 'False':
    conn = db_backup.restore_backup(conn, backup_file, do_db_init=False)
else:
    conn = db_backup.restore_backup(conn, backup_file)
    conn = db_init.execute_querries(conn)
    

# creating backup file
conn.commit()

db_init.timer()
db_backup.create_backup(backup_file)
print("Backup created --> \t{};".format(db_init.timer()), flush=True)

print("\n--python script main.py is done--")


HOST = 'flyway'
PORT = 3000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Main table is ready for migration')

conn.commit()
conn.close()
