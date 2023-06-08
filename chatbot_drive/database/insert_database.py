import pymysql
import re

host = 'localhost'
port = 3306
username = 'root'
password = '123456'
database = 'lexicon'

conn = pymysql.connect(host=host, port=port, user=username, passwd=password, db=database)
cursor = conn.cursor()


def insert_data_yml(t, path):
    with open(path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= 5:
                line = line.replace('    - ', '').replace('\n', '')
                try:
                    cursor.execute('insert into entity(type,val) values (%s,%s)', [t, line])
                except Exception as e:
                    print(e)
                    conn.rollback()
                    print('Error!')
                    break
        cursor.close()
        conn.commit()
        conn.close()


def insert_data_txt(t, path):
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                line = re.split(r'\s+?', line)[0]
                cursor.execute('insert into entity(type,val) values (%s,%s)', [t, line])
            except Exception as e:
                print(e)
                conn.rollback()
                print('Error!')
        cursor.close()
        conn.commit()
        conn.close()


if __name__ == '__main__':
    insert_data_txt('古诗词', '../data/lookup/THUOCL_poem.txt')
