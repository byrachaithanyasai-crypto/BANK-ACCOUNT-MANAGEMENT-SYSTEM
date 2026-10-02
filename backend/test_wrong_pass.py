import pymysql
try:
    conn = pymysql.connect(host='localhost', user='root', password='wrongpassword', database='bankx')
except Exception as e:
    import traceback
    traceback.print_exc()
