import pymysql
try:
    conn = pymysql.connect(host='localhost', user='root', password='password', database='bankx')
    print("PyMySQL Connected!")
except Exception as e:
    import traceback
    traceback.print_exc()
