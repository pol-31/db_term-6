import time  # try to connect every 0.1s
import os
import csv
import codecs  # utf-8 | cp1251 encoding

import psycopg2

import db_config

time_start = time.time()


def timer():
    global time_start
    time_elapsed = time.time()
    result = time_elapsed - time_start
    time_start = time_elapsed
    return result


def connect_to_db():
    global time_start
    time_start = time.time()

    print("\nConnecting to database...", flush=True)
    while True:
        try:
            conn = psycopg2.connect(dbname=db_config.db_main_name,
                                    user=db_config.db_main_user,
                                    password=db_config.db_main_password,
                                    host=db_config.db_main_host)
            break
        except:
            time.sleep(0.1)
    print("Connected to database --> \t{};".format(timer()), flush=True)
    return conn


def create_db(_conn):
    print("\nStart creating tbl_ZNOresults...", flush=True)
    cursor = _conn.cursor()

    while True:
        try:
            cursor.execute(
                """
        CREATE TABLE IF NOT EXISTS tbl_zno_results(
            OUTID char(36) PRIMARY KEY,
            Birth int2 NOT NULL,
            SEXTYPENAME char(10) NOT NULL,
            REGNAME char(30) NOT NULL,
            AREANAME char(30) NOT NULL,
            TERNAME char(40) NOT NULL,
            REGTYPENAME varchar(120) NULL,
            TerTypeName char(5) NULL,
            ClassProfileNAME char(40) NULL,
            ClassLangName char(10) NULL,
            EONAME varchar(300) NULL,
            EOTYPENAME char(60) NULL,
            EORegName char(30) NULL,
            EOAreaName char(50) NULL,
            EOTerName char(40) NULL,
            EOParent varchar(300) NULL,
            UkrTest char(30) NULL,
            UkrTestStatus char(20) NULL,
            UkrBall100 char(5) NULL,
            UkrBall12 char(5) NULL,
            UkrBall char(5) NULL,
            UkrAdaptScale char(1) NULL,
            UkrPTName varchar(300) NULL,
            UkrPTRegName varchar(30) NULL,
            UkrPTAreaName char(50) NULL,
            UkrPTTerName char(40) NULL,
            histTest char(20) NULL,
            HistLang char(10) NULL,
            histTestStatus char(20) NULL,
            histBall100 char(5) NULL,
            histBall12 char(5) NULL,
            histBall char(5) NULL,
            histPTName varchar(300) NULL,
            histPTRegName char(30) NULL,
            histPTAreaName char(50) NULL,
            histPTTerName char(40) NULL,
            mathTest char(10) NULL,
            mathLang char(10) NULL,
            mathTestStatus char(20) NULL,
            mathBall100 char(5) NULL,
            mathBall12 char(5) NULL,
            mathBall char(5) NULL,
            mathPTName varchar(300) NULL,
            mathPTRegName char(30) NULL,
            mathPTAreaName char(50) NULL,
            mathPTTerName char(40) NULL,
            physTest char(10) NULL,
            physLang char(10) NULL,
            physTestStatus char(20) NULL,
            physBall100 char(5) NULL,
            physBall12 char(5) NULL,
            physBall char(5) NULL,
            physPTName varchar(300) NULL,
            physPTRegName char(30) NULL,
            physPTAreaName char(50) NULL,
            physPTTerName char(40) NULL,
            chemTest char(10) NULL,
            chemLang char(10) NULL,
            chemTestStatus char(20) NULL,
            chemBall100 char(5) NULL,
            chemBall12 char(5) NULL,
            chemBall char(5) NULL,
            chemPTName varchar(300) NULL,
            chemPTRegName char(30) NULL,
            chemPTAreaName char(50) NULL,
            chemPTTerName char(40) NULL,
            bioTest char(10) NULL,
            bioLang char(10) NULL,
            bioTestStatus char(20) NULL,
            bioBall100 char(5) NULL,
            bioBall12 char(5) NULL,
            bioBall char(5) NULL,
            bioPTName varchar(300) NULL,
            bioPTRegName char(30) NULL,
            bioPTAreaName char(50) NULL,
            bioPTTerName char(40) NULL,
            geoTest char(10) NULL,
            geoLang char(10) NULL,
            geoTestStatus char(20) NULL,
            geoBall100 char(5) NULL,
            geoBall12 char(5) NULL,
            geoBall char(5) NULL,
            geoPTName varchar(300) NULL,
            geoPTRegName char(30) NULL,
            geoPTAreaName char(50) NULL,
            geoPTTerName char(40) NULL,
            engTest char(20) NULL,
            engTestStatus char(20) NULL,
            engBall100 char(5) NULL,
            engBall12 char(5) NULL,
            engDPALevel char(30) NULL,
            engBall char(5) NULL,
            engPTName varchar(300) NULL,
            engPTRegName char(30) NULL,
            engPTAreaName char(50) NULL,
            engPTTerName char(40) NULL,
            fraTest char(20) NULL,
            fraTestStatus char(20) NULL,
            fraBall100 char(5) NULL,
            fraBall12 char(5) NULL,
            fraDPALevel char(30) NULL,
            fraBall char(5) NULL,
            fraPTName varchar(200) NULL,
            fraPTRegName char(30) NULL,
            fraPTAreaName char(50) NULL,
            fraPTTerName char(40) NULL,
            deuTest char(20) NULL,
            deuTestStatus char(20) NULL,
            deuBall100 char(5) NULL,
            deuBall12 char(5) NULL,
            deuDPALevel char(30) NULL,
            deuBall char(5) NULL,
            deuPTName varchar(200) NULL,
            deuPTRegName char(30) NULL,
            deuPTAreaName char(50) NULL,
            deuPTTerName char(40) NULL,
            spaTest char(20) NULL,
            spaTestStatus char(20) NULL,
            spaBall100 char(5) NULL,
            spaBall12 char(5) NULL,
            spaDPALevel char(30) NULL,
            spaBall char(5) NULL,
            spaPTName varchar(200) NULL,
            spaPTRegName char(30) NULL,
            spaPTAreaName char(50) NULL,
            spaPTTerName char(40) NULL
        );
        
        
        CREATE TABLE flyway_schema_history (
            installed_rank INT NOT NULL,
            version VARCHAR(50),
            description VARCHAR(200) NOT NULL,
            type VARCHAR(20) NOT NULL,
            script VARCHAR(1000) NOT NULL, 
            checksum INT, 
            installed_by VARCHAR(100) NOT NULL, 
            installed_on TIMESTAMP NOT NULL DEFAULT NOW(), 
            execution_time INT NOT NULL, 
            success BOOLEAN NOT NULL
        );
        
        
        INSERT INTO flyway_schema_history(
                installed_rank, version, description, type,
                script, checksum, installed_by, execution_time, success
        ) 
        VALUES(
                1, '2.0.0', 'Baseline', 'BASELINE', 
                'V2__create_baseline_table.sql', 0, 'dreamTeam', 0, true
        );
                    """)
            break
        except psycopg2.OperationalError:
            print("trying to reconnect...", flush=True)
            _conn = connect_to_db()
            cursor = _conn.cursor()

    print("tbl_zno_results CREATED --> \t{};".format(timer()), flush=True)

    return _conn


# populating

def insert_to_db(_conn, filename):
    cursor = _conn.cursor()

    # file's headers
    inputFile = codecs.open(filename, 'r', encoding='cp1251')
    column_names = inputFile.readline().replace(';', ', ')[:-1].rstrip(',')
    column_names = '(' + column_names.replace('\"', '') + ')'
    column_num = column_names.count(',') + 1

    # file's main data(records) processing
    reader = csv.reader(inputFile, delimiter=';')
    i: int = 1  # iter
    limit: int = int(os.getenv('DB_DATA_LIMIT'))  # max values to insert
    buf = ""
    for row in reader:
        record = ';'.join(row).replace('\"', '').replace(
            '\'', '\'\'').replace('null', '0')
        record = record.split(';', column_num)[0:column_num]
        insert_data = '(\'' + '\', \''.join(record) + '\')'

        if (i % 1000) == 0:
            print("{} inserted".format(i), flush=True)

        i += 1

        buf += """INSERT INTO tbl_zno_results{heads} VALUES {values} 
                        ON CONFLICT (outid) DO NOTHING;\n""".format(
            heads=column_names, values=insert_data)

        if ((i - 1) % 10 != 0) & (not (i > limit & limit > 0)):
            continue

        while True:
            try:
                cursor.execute(buf)
                _conn.commit()
                break
            except Exception as e:
                print("trying to reconnect...", flush=True)
                _conn = connect_to_db()
                _conn.rollback()
                cursor = _conn.cursor()

        if i > limit & limit > 0:
            break

        buf = ""

    inputFile.close()

    return _conn


def fill_db(_conn):
    print("\nInserting to tbl_zno_results...", flush=True)

    _conn = insert_to_db(_conn, 'Odata{}File.csv'.format(os.getenv('DB_DATA_YEAR1')))
    print("Inserting #1 completed --> \t{};".format(timer()), flush=True)

    _conn = insert_to_db(_conn, 'Odata{}File.csv'.format(os.getenv('DB_DATA_YEAR2')))
    print("Inserting #2 completed --> \t{};".format(timer()), flush=True)

    return _conn


def execute_querries(_conn):
    cursor = _conn.cursor()
    print("\nStart query executing...", flush=True)
    # querry var=2
    while True:
        try:
            cursor.execute("""
                SELECT REGNAME, AVG(CAST(REPLACE(UkrBall100, ',', '.') AS DECIMAL)) 
                as AVG_UkrBall100 
                FROM tbl_zno_results 
                WHERE (
                (UkrTestStatus = \'Зараховано\') AND 
                (UkrBall100 is not null) AND
                (REGNAME is not null))
                GROUP BY REGNAME
                ORDER BY AVG_UkrBall100;
                """)
            break
        except psycopg2.OperationalError:
            print("trying to reconnect...", flush=True)
            _conn = connect_to_db()
            cursor = _conn.cursor()

    querry_data = cursor.fetchall()

    with open('../results/querry_result.csv', 'w') as outputFile:
        writer = csv.writer(outputFile)
        writer.writerows(querry_data)

    print("Query completed --> \t{};".format(timer()), flush=True)

    return _conn
