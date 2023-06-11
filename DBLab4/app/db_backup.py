import time
import os
import subprocess
import shutil
import schedule

import psycopg2

import db_init
import db_config

def create_backup(_backup_file: str):
    _path = _backup_file[:_backup_file.rfind('/')]
    os.makedirs(_path, exist_ok=True)  # Create the backup directory if it doesn't exist
    open(_backup_file, 'w').close()
    dump_command = [
        'pg_dump',
        '--dbname=postgresql://{}:{}@{}:{}/{}'.format(db_config.db_main_user, db_config.db_main_password, db_config.db_main_host, db_config.db_main_port, db_config.db_main_name),
        '-F', 'c',
        '-b',
        '-v',
        '-f', _backup_file
    ]
    try:
        subprocess.run(dump_command, check=True)
        print('Backup created', flush=True)
    except Exception as e:
        print("Failed to create backup: ", e, flush=True)


def restore_backup(_conn, _backup_file: str, do_db_init = True):
    if os.path.exists(_backup_file):
        db_init.timer()
        restore_command = [
            'pg_restore',
            '--dbname=postgresql://{}:{}@{}:{}/{}'.format(db_config.db_main_user, db_config.db_main_password, db_config.db_main_host, db_config.db_main_port, db_config.db_main_name),
            '-F', 'c',
            '-v',
            _backup_file
        ]
        try:
            subprocess.run(restore_command, check=True)
            print(f'Database restored from reserve copy {_backup_file}', flush=True)
            print("Backup loaded --> \t{};".format(db_init.timer()), flush=True)
        except Exception as e:
            print("Failed to restore from backup: ", e, flush=True)

            if (do_db_init == True):
                _conn = db_init.create_db(_conn)
                _conn = db_init.fill_db(_conn)
    else:
        db_init.timer()
        print('Backup does not exist, proceed to recreate db', flush=True)
        if (do_db_init == True):
            _conn = db_init.create_db(_conn)
            _conn = db_init.fill_db(_conn)
        
    return _conn


def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)


