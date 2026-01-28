import pymysql

def create_connection():
    cn = pymysql.connect(
            port=3306,
            host='localhost',
            user='root',
            password='',
            db='project',
            autocommit=True
        )
    cur = cn.cursor()
    return cur

def admin_data(email):
    cur = create_connection()
    sql = "select * from admindata where email='" + email + "'"
    cur.execute(sql)
    n = cur.rowcount
    data=None
    if (n == 1):
        data = cur.fetchone()
    return data

def medical_data(email):
    cur = create_connection()
    sql = "select * from medicaldata where email='" + email + "'"
    cur.execute(sql)
    n = cur.rowcount
    data=None
    if (n == 1):
        data = cur.fetchone()
    return data

def check_photo(email):
    cur = create_connection()
    sql = "select * from photodata where email='" + email + "'"
    cur.execute(sql)
    n = cur.rowcount
    photo="no"

    if (n > 0):
        row= cur.fetchone()
        photo=row[1]
    return photo