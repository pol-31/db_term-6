import time
import os
import subprocess
import schedule

import db_config
import db_init


def create_backup(_backup_file: str, _retries: int = 10, _retries_interval: int = 3):
    for _attempt in range(_retries):
        print(f"Backup create. Attempt {_attempt + 1}/{_retries}", flush=True)
        _path = _backup_file[:_backup_file.rfind('/')]
        os.makedirs(_path, exist_ok=True)  # Create the backup directory if it doesn't exist
        open(_backup_file, 'w').close()
        dump_command = [
            'pg_dump',
            '--dbname=postgresql://{}:{}@{}:{}/{}'.format(db_config.db_main_user,
                                                          db_config.db_main_password,
                                                          db_config.db_main_host,
                                                          db_config.db_main_port,
                                                          db_config.db_main_name),
            '-F', 'c',
            '-b',
            '-v',
            '-f', _backup_file
        ]
        try:
            subprocess.run(dump_command, check=True)
            print('Backup created', flush=True)
            break
        except Exception as e:
            print("Failed to create backup: ", e, flush=True)
            time.sleep(_retries_interval)


def restore_backup(_conn, _backup_file: str, do_db_init=True, _retries: int = 10, _retries_interval: int = 3):
    _restore_successful: bool = False
    if os.path.exists(_backup_file):
        for _attempt in range(_retries):
            print(f"Backup restore. Attempt {_attempt + 1}/{_retries}", flush=True)

            db_init.timer()
            restore_command = [
                'pg_restore',
                '--dbname=postgresql://{}:{}@{}:{}/{}'.format(db_config.db_main_user,
                                                              db_config.db_main_password,
                                                              db_config.db_main_host,
                                                              db_config.db_main_port,
                                                              db_config.db_main_name),
                '--clean',
                '-F', 'c',
                '-v',
                _backup_file
            ]
            try:
                subprocess.run(restore_command, check=True)

                print(f'Database restored from reserve copy {_backup_file}', flush=True)
                print("Backup loaded --> \t{};".format(db_init.timer()), flush=True)

                _restore_successful = True
                break
            except Exception as e:
                print("Failed to restore from backup: ", e, flush=True)
                time.sleep(_retries_interval)

    elif not _restore_successful:
        db_init.timer()
        print('Backup does not exist, proceed to recreate db', flush=True)
        if do_db_init:
            _conn = db_init.create_db(_conn)
            _conn = db_init.fill_db(_conn)

    return _conn


def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)
