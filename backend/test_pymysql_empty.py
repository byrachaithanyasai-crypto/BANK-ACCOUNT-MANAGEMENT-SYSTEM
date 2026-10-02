import pymysql
try:
    conn = pymysql.connect(host='localhost', user='root', password='', database='bankx')
    print("PyMySQL Connected with empty password!")
except Exception as e:
    import traceback
    traceback.print_exc()
