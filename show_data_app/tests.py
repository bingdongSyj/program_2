from django.test import TestCase

# Create your tests here.
import MySQLdb

conn = MySQLdb.Connect(
    host='localhost',
    user='root',
    password='lk1997',
    db='test_urllib',
    port=3306,
    charset='utf8'
)
cursor = conn.cursor()

if __name__ == '__main__':
    sql = 'select cityid, city from xpath_and_more group by cityid'
    cursor.execute(sql)
    print(cursor.fetchall())
